#!/usr/bin/env python3
"""Quality gate for a finished edit before delivery. Read-only; uses ffmpeg/ffprobe, no network.

With a plan, cuts outside overlay intervals are checked frame by frame: the few frames just before the cut should look
like the outgoing shot and those just after it like the incoming shot. Frames that look like the wrong
side are stray frames, for example a few frames of the next shot left at the end of the previous one.
Measured picture changes are also compared with the planned times, so a cut planned at 8.00s that
actually happens at 8.29s is reported instead of passing. White/black flashes and luma flicker are
listed as suspects. With --beats (beat_grid.py output), cuts farther than 60ms from a beat are too.
Picture changes the plan does not explain, such as sparks, fast motion or an unplanned cut, are listed
as candidates for a person to inspect. Suspects are places to look, not verdicts. Also reports
silences, loudness, true peak, duration and frame size.

Optional --models is off unless named. It does not download weights unless --allow-model-download is set.
"""
import argparse
import importlib.util
import json
import math
from pathlib import Path
import re
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def load_media():
    spec = importlib.util.spec_from_file_location('media_inspect', HERE / 'media_inspect.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run(args):
    return subprocess.run(args, capture_output=True, text=True)


def probe(path):
    out = run(['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type,width,height,r_frame_rate',
               '-of', 'json', str(path)])
    if out.returncode:
        raise ValueError(f'cannot read {path}: {out.stderr.strip()}')
    data = json.loads(out.stdout)
    video = next((s for s in data.get('streams', []) if s.get('codec_type') == 'video'), None)
    if not video:
        raise ValueError(f'{path} has no video stream')
    num, den = (int(x) for x in video['r_frame_rate'].split('/'))
    return {'duration': float(data['format']['duration']), 'width': video['width'], 'height': video['height'],
            'fps': num / den if den else 0, 'audio': any(s.get('codec_type') == 'audio' for s in data['streams'])}


def detect_changes(path, threshold):
    err = run(['ffmpeg', '-v', 'info', '-nostdin', '-i', str(path), '-an', '-vf',
               f"select='gt(scene,{threshold})',showinfo", '-f', 'null', '-']).stderr
    return [round(float(t), 3) for t in re.findall(r'pts_time:([0-9.]+)', err)]


def frame(path, at, w=32, h=56):
    """A tiny YUV 4:4:4 frame: luma averaged over 4x4 blocks plus mean chroma."""
    raw = subprocess.run(['ffmpeg', '-v', 'error', '-nostdin', '-ss', f'{max(0, at):.4f}', '-i', str(path),
                          '-frames:v', '1', '-vf', f'scale={w}:{h},format=yuv444p', '-f', 'rawvideo', '-'],
                         capture_output=True).stdout
    n = w * h
    if len(raw) < 3 * n:
        return None
    luma = raw[:n]
    blocks = [sum(luma[(y * 4 + j) * w + x * 4 + i] for j in range(4) for i in range(4)) / 16
              for y in range(h // 4) for x in range(w // 4)]
    return blocks, sum(raw[n:2 * n]) / n, sum(raw[2 * n:]) / n


def likeness(a, b):
    """Higher means more alike: layout correlation, minus penalties for colour and brightness shift."""
    la, lb = a[0], b[0]
    ma, mb = sum(la) / len(la), sum(lb) / len(lb)
    da, db = [x - ma for x in la], [y - mb for y in lb]
    sa, sb = sum(x * x for x in da) ** 0.5, sum(y * y for y in db) ** 0.5
    if sa > 1e-6 and sb > 1e-6:
        corr = sum(x * y for x, y in zip(da, db)) / (sa * sb)
    else:
        corr = 1.0 if abs(ma - mb) < 4 else 0.0
    return corr - (abs(a[1] - b[1]) + abs(a[2] - b[2])) / 64 - abs(ma - mb) / 255


def check_cut(path, cut, fps, window, room_before, room_after):
    """Count frames on each side of a planned cut that resemble the other shot more than their own."""
    before_n = min(window, int(room_before * fps) - 1)
    after_n = min(window, int(room_after * fps) - 1)
    if before_n < 1 or after_n < 1:
        return None
    k = round(cut * fps)
    # Seeking returns the first frame at or after the time, so aim just before frame k + i starts.
    at = lambda i: (k + i - 0.25) / fps
    outgoing, incoming = frame(path, at(-before_n - 1)), frame(path, at(after_n))
    if not outgoing or not incoming:
        return None
    early = late = 0
    for i in range(-before_n, 0):
        f = frame(path, at(i))
        if f and likeness(f, incoming) > likeness(f, outgoing): early += 1
    for i in range(0, after_n):
        f = frame(path, at(i))
        if f and likeness(f, outgoing) > likeness(f, incoming): late += 1
    return {'cut': cut, 'frames_like_next_shot_before_cut': early, 'frames_like_previous_shot_after_cut': late}


def detect_silence(path, noise_db, minimum):
    err = run(['ffmpeg', '-v', 'info', '-nostdin', '-i', str(path), '-vn', '-af',
               f'silencedetect=n={noise_db}dB:d={minimum}', '-f', 'null', '-']).stderr
    starts = [float(x) for x in re.findall(r'silence_start: (-?[0-9.]+)', err)]
    ends = [float(x) for x in re.findall(r'silence_end: ([0-9.]+)', err)]
    return [{'start': round(max(0, s), 3), 'end': round(e, 3) if e is not None else None}
            for s, e in zip(starts, ends + [None] * (len(starts) - len(ends)))]


def measure_loudness(path):
    err = run(['ffmpeg', '-v', 'info', '-nostdin', '-i', str(path), '-vn', '-af', 'loudnorm=print_format=json',
               '-f', 'null', '-']).stderr
    block = err[err.rfind('{'):err.rfind('}') + 1]
    try:
        data = json.loads(block)
        values = {'integrated_lufs': float(data['input_i']), 'true_peak_db': float(data['input_tp'])}
        return {key: value if math.isfinite(value) else None for key, value in values.items()}
    except (ValueError, KeyError):
        return None


def check(video, plan=None, threshold=0.3, window=4, size=None, lufs=None, noise_db=-50, min_silence=0.5,
          beat_times=None, beat_tolerance=0.06, models=None, allow_model_download=False, ref_faces=None):
    info = probe(video)
    fps, duration = info['fps'] or 24, info['duration']
    tolerance = 2 / fps
    issues = []
    overlays = [(o['start'], o['end']) for o in (plan or {}).get('overlays', [])]
    covered = lambda t: any(a - tolerance <= t <= b + tolerance for a, b in overlays)

    cut_checks, planned, offset_targets, overlay_excluded = [], [], [], []
    if plan:
        shots = plan.get('shots', [])
        for prev, shot in zip(shots, shots[1:]):
            if shot.get('transition', {}).get('type', 'cut') != 'cut':
                continue
            planned.append(shot['start'])
            if covered(shot['start']):
                overlay_excluded.append(shot['start'])
                continue
            offset_targets.append(shot['start'])
            result = check_cut(video, shot['start'], fps, window,
                               shot['start'] - prev['start'], shot['end'] - shot['start'])
            if result:
                cut_checks.append(result)
        stray = [c for c in cut_checks
                 if c['frames_like_next_shot_before_cut'] or c['frames_like_previous_shot_after_cut']]
        if stray:
            issues.append(f'{len(stray)} planned cut(s) with frames from the neighbouring shot')
        if abs(duration - plan.get('duration', duration)) > 1 / fps:
            issues.append(f'duration {duration:.3f}s differs from plan {plan["duration"]}s')

    # Everything the plan does not explain is listed for a person to look at, not judged here.
    changes = [c for c in detect_changes(video, threshold) if not covered(c)]
    unplanned = [c for c in changes if not any(abs(c - t) <= tolerance for t in planned)]
    bounds = [0.0] + changes + [duration]
    short_runs = [{'start': a, 'end': round(b, 3), 'frames': round((b - a) * fps)}
                  for a, b in zip(bounds, bounds[1:]) if 0 < round((b - a) * fps) < window]

    silences, loud = [], None
    if not info['audio']:
        issues.append('no audio stream')
    else:
        silences = detect_silence(video, noise_db, min_silence)
        if silences: issues.append(f'{len(silences)} silence(s) of {min_silence}s or more')
        loud = measure_loudness(video)
        if loud and loud['true_peak_db'] is not None and loud['true_peak_db'] > -1:
            issues.append(f'true peak {loud["true_peak_db"]} dB above -1 dB')
        if loud and loud['integrated_lufs'] is not None and lufs is not None and abs(loud['integrated_lufs'] - lufs) > 1.5:
            issues.append(f'loudness {loud["integrated_lufs"]} LUFS, target {lufs}')
    if size and (info['width'], info['height']) != size:
        issues.append(f'frame size {info["width"]}x{info["height"]}, expected {size[0]}x{size[1]}')
    report = load_media().suspect_report(
        video, fps, duration, changes, offset_targets, beat_times, beat_tolerance,
        models or [], allow_model_download, ref_faces or [])
    for suspect in report['suspects']:
        if suspect['type'] in ('cut_offset', 'missing_planned_cut'):
            issues.append(suspect['reason'])
    return {'video': str(video), 'duration': round(duration, 3), 'size': f'{info["width"]}x{info["height"]}',
            'fps': round(fps, 3), 'cut_checks': cut_checks, 'unplanned_changes': unplanned,
            'short_runs_between_changes': short_runs, 'silences': silences, 'loudness': loud, 'issues': issues,
            'detected_cuts': report['detected_cuts'], 'planned_cuts': report['planned_cuts'],
            'all_planned_cuts': [round(float(t), 3) for t in planned],
            'overlay_excluded_cuts': [round(float(t), 3) for t in overlay_excluded],
            'cut_coverage_note': 'planned_cuts contains only cuts outside overlay intervals. '
                                 'overlay_excluded_cuts are not checked for neighbouring-shot frames or cut offset; '
                                 'any overlay excludes its whole time interval, including a two-frame margin. '
                                 'Excluded cuts are unchecked, not passed.',
            'suspects': report['suspects'], 'curves': report['curves'], 'model_notes': report['model_notes'],
            'suspects_note': report['note'],
            'scope': 'Only planned cuts outside overlay intervals are eligible for picture-change alignment; '
                     'cut_checks lists the neighbouring-frame checks that could be completed. '
                     'See all_planned_cuts and overlay_excluded_cuts for coverage. '
                     'An empty issues list does not establish that excluded cuts passed. Flashes, flicker, '
                     'cut offset and off-beat cuts are suspects to look at, not automatic creative verdicts. '
                     'Dialogue placement, gaze and taste need watching and listening.'}


def _solid(rgb, width, height):
    return bytes(rgb) * (width * height)


def write_signal_clip(directory):
    """Write a synthetic clip with a white flash, a black flash, a late cut, flicker, and one on-beat cut.

    Planned cuts are 2.00s and 4.00s. The picture changes at 2.00s and at frame 103 (4.292s).
    Beats are every 0.5s, so 2.00s is on the grid and 4.292s is not.
    """
    directory = Path(directory)
    directory.mkdir(parents=True, exist_ok=True)
    width, height, fps, frames = 96, 160, 24, 144
    shot_a, shot_b, shot_c = (20, 90, 30), (180, 140, 40), (40, 50, 160)
    raw = bytearray()
    for i in range(frames):
        t = i / fps
        if 0.50 <= t < 0.50 + 2 / fps:
            rgb = (0, 0, 0)  # two black frames
        elif 1.00 <= t < 1.00 + 3 / fps:
            rgb = (255, 255, 255)  # three white frames
        elif t < 2.0:
            rgb = shot_a
        elif t < 103 / fps:
            rgb = shot_b  # planned cut was 4.00s; this shot runs seven frames long
        elif 5.0 <= t < 5.5:
            rgb = (100, 100, 100) if i % 2 == 0 else (128, 128, 128)
        else:
            rgb = shot_c
        raw += _solid(rgb, width, height)
    video = directory / 'signals.mp4'
    proc = subprocess.run(
        ['ffmpeg', '-v', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{width}x{height}',
         '-r', str(fps), '-i', '-', '-f', 'lavfi', '-i', 'sine=frequency=440:sample_rate=48000:duration=6',
         '-filter:a', 'volume=0.2', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '16', '-preset', 'ultrafast',
         '-shortest', '-c:a', 'aac', str(video)],
        input=bytes(raw), check=True)
    del proc
    plan = {'duration': 6.0, 'shots': [
        {'id': 's1', 'start': 0, 'end': 2},
        {'id': 's2', 'start': 2, 'end': 4},
        {'id': 's3', 'start': 4, 'end': 6},
    ], 'overlays': []}
    beats = {'beats': [{'time': round(i * 0.5, 3)} for i in range(13)]}
    (directory / 'plan.json').write_text(json.dumps(plan))
    (directory / 'beats.json').write_text(json.dumps(beats))
    return video, plan, beats


def self_check(directory=None):
    """Build a clip with known defects and require flash, flicker, cut offset and an off-beat cut."""
    import tempfile
    own = directory is None
    tmp = tempfile.TemporaryDirectory() if own else None
    root = Path(directory) if directory else Path(tmp.name)
    try:
        video, plan, beats = write_signal_clip(root)
        beat_times = [b['time'] for b in beats['beats']]
        report = check(video, plan, beat_times=beat_times)
        found = {}
        for suspect in report['suspects']:
            found.setdefault(suspect['type'], []).append({
                'start': suspect['start'], 'end': suspect['end'], 'score': suspect['score'],
                'reason': suspect['reason'],
            })
        def near(items, t, slack=0.15):
            return [item for item in items if abs(item['start'] - t) <= slack or abs(item.get('end', item['start']) - t) <= slack
                    or (item['start'] - slack <= t <= item['end'] + slack)]
        caught = {
            'flash': near(found.get('flash', []), 1.0) or near(found.get('flash', []), 0.5),
            'black_flash': near(found.get('flash', []), 0.5, 0.08),
            'white_flash': near(found.get('flash', []), 1.0, 0.08),
            'flicker': near(found.get('flicker', []), 5.0, 0.3),
            'cut_offset': [item for item in found.get('cut_offset', []) if abs((item['score'] or 0) - 0.292) < 0.08],
            'cut_off_beat': near(found.get('cut_off_beat', []), 4.292, 0.12),
        }
        on_beat_flagged = near(found.get('cut_off_beat', []), 2.0, 0.08)
        ok = all(caught.values()) and not on_beat_flagged
        summary = {'ok': ok, 'video': video.name, 'caught': {key: value for key, value in caught.items()},
                   'on_beat_cut_flagged': on_beat_flagged, 'issues': report['issues'],
                   'suspects': [{'id': s['id'], 'type': s['type'], 'start': s['start'], 'end': s['end'],
                                 'score': s['score'], 'reason': s['reason']} for s in report['suspects']]}
        return ok, summary
    finally:
        if tmp:
            tmp.cleanup()


def main():
    if len(sys.argv) > 1 and sys.argv[1] == '--self-check':
        ok, summary = self_check()
        print(json.dumps(summary, indent=2))
        raise SystemExit(0 if ok else 1)
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video', type=Path)
    parser.add_argument('--plan', type=Path, help='plan.json whose timeline the video follows')
    parser.add_argument('--threshold', type=float, default=0.3, help='scene-change threshold for listing candidates')
    parser.add_argument('--window', type=int, default=4, help='frames checked on each side of a planned cut')
    parser.add_argument('--size', help='expected frame size, e.g. 1080x1920')
    parser.add_argument('--lufs', type=float, help='target integrated loudness for the platform')
    parser.add_argument('--beats', type=Path, help='beat_grid.py JSON; measured cuts are checked against its beat times')
    parser.add_argument('--beat-tol', type=float, default=0.06, help='seconds from the nearest beat before a cut is off-beat')
    parser.add_argument('--models', default='', help='optional, comma-separated: clip,dino,face,syncnet')
    parser.add_argument('--allow-model-download', action='store_true',
                        help='let an opted-in model fetch weights; default is to skip when weights are absent')
    parser.add_argument('--ref-face', type=Path, nargs='*', default=[], help='reference face images for --models face')
    args = parser.parse_args()
    try:
        plan = json.loads(args.plan.read_text()) if args.plan else None
        size = tuple(int(x) for x in args.size.lower().split('x')) if args.size else None
        beat_times = load_media().beat_times_from(json.loads(args.beats.read_text())) if args.beats else None
        models = [part.strip().lower() for part in args.models.split(',') if part.strip()]
        result = check(args.video, plan, args.threshold, args.window, size, args.lufs,
                       beat_times=beat_times, beat_tolerance=args.beat_tol, models=models,
                       allow_model_download=args.allow_model_download, ref_faces=args.ref_face)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(2, f'{exc}\n')
    print(json.dumps(result, indent=2))
    raise SystemExit(1 if result['issues'] else 0)


if __name__ == '__main__':
    main()
