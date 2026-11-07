#!/usr/bin/env python3
"""Local reference frames, audio diagnostics, motion changes and review suspects. Requires ffmpeg.

`suspects` writes white/black flashes, luma flicker, planned-cut offset and off-beat cuts.
`--models` is not loaded unless named, and weights are not downloaded unless `--allow-model-download` is set.
"""
import argparse
from array import array
import importlib.util
import json
import math
from pathlib import Path
import re
import subprocess
import sys


def run(args):
    return subprocess.run(args, check=True, capture_output=True)


def probe(path):
    if not path.is_file(): raise ValueError('input must be an existing local file')
    result = json.loads(run(['ffprobe', '-v', 'error', '-protocol_whitelist', 'file,pipe',
                             '-show_format', '-show_streams', '-of', 'json', str(path)]).stdout)
    duration = float(result['format']['duration'])
    if not math.isfinite(duration) or duration <= 0 or duration > 600:
        raise ValueError('diagnostic input must have a known duration between 0 and 600 seconds')
    return result, duration


def ffinput(path):
    return ['ffmpeg', '-v', 'error', '-nostdin', '-protocol_whitelist', 'file,pipe', '-i', str(path)]


def write_new(path, value):
    with path.open('x') as f:
        json.dump(value, f, ensure_ascii=False, indent=2, allow_nan=False); f.write('\n')


def peaks(values, spacing, count):
    chosen = []
    for i in sorted(range(len(values)), key=lambda j: values[j], reverse=True):
        if values[i] <= 0: break
        if all(abs(i - x) >= spacing for x in chosen): chosen.append(i)
        if len(chosen) >= count: break
    return sorted(chosen)


def _median(values):
    ordered = sorted(values)
    mid = len(ordered) // 2
    if len(ordered) % 2:
        return ordered[mid]
    return (ordered[mid - 1] + ordered[mid]) / 2


def _runs(mask):
    out, i = [], 0
    while i < len(mask):
        if mask[i]:
            j = i
            while j + 1 < len(mask) and mask[j + 1]:
                j += 1
            out.append((i, j))
            i = j + 1
        else:
            i += 1
    return out


def stream_fps(meta):
    video = next(s for s in meta['streams'] if s['codec_type'] == 'video')
    num, den = (int(x) for x in video['r_frame_rate'].split('/'))
    if den == 0 or num <= 0:
        raise ValueError('video frame rate is missing')
    return num / den


def luma_series(path, width=96, height=160):
    """Mean luma of every frame. Small frames are enough for flash and flicker."""
    size = width * height
    proc = subprocess.Popen(ffinput(path) + ['-an', '-vf', f'scale={width}:{height},format=gray',
                                              '-f', 'rawvideo', '-'], stdout=subprocess.PIPE)
    luma = []
    try:
        while True:
            buf = proc.stdout.read(size)
            if len(buf) < size:
                break
            luma.append(sum(buf) / size)
    finally:
        proc.stdout.close()
        code = proc.wait()
    if code:
        raise subprocess.CalledProcessError(code, 'ffmpeg')
    return luma


def detect_flash_flicker(luma, fps, flash_dev=35, return_delta=15, flicker_step=4):
    """White/black flashes sit far from the local median and then the picture returns.

    Flicker is a run of luma steps whose sign keeps reversing. A short flash is not
    also reported as flicker. Thresholds are starting points for flat and generated footage.
    """
    n = len(luma)
    if n == 0 or not fps:
        return []
    med = [_median(luma[max(0, i - 4):i + 5]) for i in range(n)]
    dev = [abs(luma[i] - med[i]) for i in range(n)]
    suspects, i = [], 0
    while i < n:
        if dev[i] > flash_dev:
            j = i
            while j + 1 < n and dev[j + 1] > flash_dev:
                j += 1
            # A flash returns to the same picture. A fade or a real cut does not.
            back = abs(luma[max(i - 1, 0)] - luma[min(j + 1, n - 1)]) < return_delta
            if j - i + 1 <= 4 and back:
                suspects.append({
                    'type': 'flash',
                    'start': round(i / fps, 3),
                    'end': round((j + 1) / fps, 3),
                    'score': round(max(dev[i:j + 1]), 1),
                    'reason': 'frame luma is far from the local median, then the picture returns',
                    'detector': 'luma_vs_local_median',
                })
            i = j + 1
        else:
            i += 1
    diffs = [luma[k + 1] - luma[k] for k in range(n - 1)]
    signs = [0 if abs(d) <= flicker_step else (1 if d > 0 else -1) for d in diffs]
    flag = [False] * n
    for k in range(max(0, len(signs) - 7)):
        window = [s for s in signs[k:k + 8] if s != 0]
        if len(window) >= 6 and sum(a != b for a, b in zip(window, window[1:])) >= 5:
            for t in range(k, min(n, k + 9)):
                flag[t] = True
    for a, b in _runs(flag):
        start, end = a / fps, (b + 1) / fps
        if any(s['type'] == 'flash' and s['start'] <= end and s['end'] >= start for s in suspects):
            continue
        segment = [abs(d) for d in diffs[a:max(a, b)]] or [0.0]
        suspects.append({
            'type': 'flicker',
            'start': round(start, 3),
            'end': round(end, 3),
            'score': round(sum(segment) / len(segment), 1),
            'reason': 'frame luma alternates up and down',
            'detector': 'luma_sign_alternation',
        })
    return suspects


def scene_times(path, threshold):
    command = ffinput(path)
    command[2] = 'info'
    log = run(command + ['-an', '-vf', f"select='gt(scene,{threshold})',showinfo", '-f', 'null', '-']).stderr.decode(errors='replace')
    return sorted(set(round(float(x), 3) for x in re.findall(r'pts_time:([0-9.]+)', log)))


def cuts_outside(cuts, ranges, fps):
    """Drop scene hits that are the flash or the flicker itself, not a new shot."""
    pad = 1.5 / fps if fps else 0.05
    def inside(t):
        return any(s['start'] - pad <= t <= s['end'] + pad for s in ranges)
    return [c for c in cuts if not inside(c)]


def align_cuts(detected, planned, fps, match_window=0.5):
    """Compare measured picture changes with planned cut times.

    A planned cut whose nearest change is only a few frames away is in tolerance.
    A change such as 8.29s against a plan of 8.00s is a cut_offset. No nearby
    change is a missing_planned_cut. Looking only at frames around the planned
    time reports OK when the real cut is later than that window.
    """
    tolerance = 2 / fps if fps else 0.08
    suspects = []
    for planned_time in planned:
        if not detected:
            nearest = None
        else:
            nearest = min(detected, key=lambda t: abs(t - planned_time))
        planned_time = float(planned_time)
        if nearest is None or abs(nearest - planned_time) > match_window:
            suspects.append({
                'type': 'missing_planned_cut',
                'start': round(planned_time, 3),
                'end': round(planned_time, 3),
                'score': None,
                'planned': round(planned_time, 3),
                'actual': None,
                'reason': f'no picture change within {match_window:.2f}s of the planned cut at {planned_time:.3f}s',
                'detector': 'planned_vs_detected_cuts',
            })
        elif abs(nearest - planned_time) > tolerance:
            suspects.append({
                'type': 'cut_offset',
                'start': round(min(planned_time, nearest), 3),
                'end': round(max(planned_time, nearest), 3),
                'score': round(nearest - planned_time, 3),
                'planned': round(planned_time, 3),
                'actual': round(float(nearest), 3),
                'reason': f'planned cut at {planned_time:.3f}s but the picture changes at {nearest:.3f}s',
                'detector': 'planned_vs_detected_cuts',
            })
    return suspects


def beat_times_from(data):
    if isinstance(data, list):
        return [float(item['time'] if isinstance(item, dict) else item) for item in data]
    return [float(beat['time']) for beat in data.get('beats', [])]


def off_beat(cuts, beat_times, tolerance=0.06):
    """Flag measured cuts farther than tolerance (default 60 ms) from beat_grid output."""
    beats = sorted(float(t) for t in beat_times)
    suspects = []
    if not beats:
        return suspects
    for cut in cuts:
        nearest = min(beats, key=lambda t: abs(cut - t))
        distance = abs(cut - nearest)
        if distance > tolerance:
            suspects.append({
                'type': 'cut_off_beat',
                'start': round(cut, 3),
                'end': round(cut, 3),
                'score': round(distance, 3),
                'nearest_beat': round(nearest, 3),
                'reason': f'cut is {distance:.3f}s from the nearest beat at {nearest:.3f}s',
                'detector': 'beat_grid',
            })
    return suspects


def annotate_suspects(suspects, duration):
    ordered = sorted(suspects, key=lambda s: (s.get('start', 0), s.get('type', '')))
    for i, suspect in enumerate(ordered, 1):
        suspect['id'] = f'S{i:02d}'
        end = duration if duration is not None else suspect['end'] + 0.5
        suspect['look'] = {
            'from': round(max(0.0, suspect['start'] - 0.5), 3),
            'to': round(min(end, suspect['end'] + 0.5), 3),
        }
    return ordered


def suspect_report(path, fps, duration, detected_changes, planned_cuts, beat_times=None,
                   beat_tolerance=0.06, models=None, allow_model_download=False, ref_faces=None):
    luma = luma_series(path)
    pixel = detect_flash_flicker(luma, fps)
    transient = [s for s in pixel if s['type'] in ('flash', 'flicker')]
    measured = [round(c, 3) for c in cuts_outside(detected_changes, transient, fps)]
    suspects = list(pixel)
    suspects += align_cuts(measured, planned_cuts, fps)
    if beat_times is not None:
        suspects += off_beat(measured, beat_times, beat_tolerance)
    notes, model_curves = [], {}
    if models:
        notes, extra, model_curves = _optional_models(path, fps, duration, measured, models, allow_model_download, ref_faces or [])
        suspects += extra
    curves = {'fps': round(fps, 3), 'luma': [round(v, 1) for v in luma]}
    curves.update(model_curves or {})
    return {
        'detected_cuts': measured,
        'planned_cuts': [round(float(t), 3) for t in planned_cuts],
        'suspects': annotate_suspects(suspects, duration),
        'curves': curves,
        'model_notes': notes,
        'note': 'Suspects are places to look, not verdicts.',
    }


def _optional_models(path, fps, duration, cuts, models, allow_download, ref_faces):
    spec = importlib.util.spec_from_file_location('review_models', Path(__file__).resolve().parent / 'review_models.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.run_optional(path, fps, duration, cuts, models, allow_download=allow_download, ref_faces=ref_faces)


def reference(path, out, interval, threshold):
    meta, duration = probe(path)
    if not any(s['codec_type'] == 'video' for s in meta['streams']): raise ValueError('no video stream')
    if math.ceil(duration / interval) > 240: raise ValueError('too many preview frames; increase --interval')
    out.mkdir(parents=True, exist_ok=False)
    command = ffinput(path)
    command[2] = 'info'
    log = run(command + ['-an', '-vf', f"select='gt(scene,{threshold})',showinfo", '-f', 'null', '-']).stderr.decode(errors='replace')
    cuts = sorted(set(float(x) for x in re.findall(r'pts_time:([0-9.]+)', log)))
    cuts = [x for x in cuts if 0 < x < duration]
    bounds = [0.0, *cuts, duration]
    run(ffinput(path) + ['-an', '-vf', f'fps=1/{interval},scale=320:-2', '-frames:v', '240', str(out/'frame_%04d.jpg')])
    frames = sorted(out.glob('frame_*.jpg'))
    # fps samples are approximate representatives of interval bins, not exact shot boundaries.
    frame_index = [{'file': f.name, 'approx_time': round(i * interval, 3)} for i, f in enumerate(frames)]
    cols = 6; rows = math.ceil(len(frames) / cols)
    if rows:
        run(['ffmpeg', '-v', 'error', '-nostdin', '-framerate', '1', '-i', str(out/'frame_%04d.jpg'),
             '-vf', f'tile={cols}x{rows}', '-frames:v', '1', str(out/'contact.jpg')])
    result = {'duration': duration, 'source': path.name, 'scene_threshold': threshold,
              'cut_candidates': cuts, 'shots': [{'start': a, 'end': b} for a,b in zip(bounds,bounds[1:])],
              'frames': frame_index, 'note': 'Automated candidates; inspect actual video for camera motion and dissolves.'}
    write_new(out/'analysis.json', result)
    return result


def audio(path, out):
    meta, duration = probe(path)
    if not any(s['codec_type'] == 'audio' for s in meta['streams']): raise ValueError('no audio stream')
    raw = run(ffinput(path) + ['-vn', '-ac', '1', '-ar', '8000', '-f', 's16le', '-']).stdout
    samples = array('h'); samples.frombytes(raw)
    if sys.byteorder != 'little': samples.byteswap()
    step = 160  # 20 ms RMS windows
    rms = []
    for i in range(0, len(samples), step):
        window = samples[i:i+step]
        rms.append(math.sqrt(sum(x*x for x in window) / len(window)) / 32768)
    changes = [max(0.0, r - (rms[i-1] if i else 0.0)) for i, r in enumerate(rms)]
    silence = []; start = None
    for i, value in enumerate([*rms, 1.0]):
        if value < 10**(-50/20) and start is None: start = i * .02
        elif value >= 10**(-50/20) and start is not None:
            if i * .02 - start >= .25: silence.append({'start': round(start, 3), 'end': round(min(i*.02, duration),3)})
            start = None
    result = {'duration': duration, 'source': path.name, 'window_seconds': .02,
              'silence_candidates': silence,
              'onset_candidates': [{'time': round(i*.02, 3), 'strength': changes[i]} for i in peaks(changes, 10, 32)],
              'note': 'Energy changes are not a beat grid or phrase analysis. Listen and verify.'}
    write_new(out, result); return result


def motion(path, out, fps):
    meta, duration = probe(path)
    if not any(s['codec_type'] == 'video' for s in meta['streams']): raise ValueError('no video stream')
    w, h = 64, 112
    raw = run(ffinput(path) + ['-an', '-vf', f'fps={fps},scale={w}:{h},format=gray', '-f', 'rawvideo', '-']).stdout
    size = w*h; values = []
    for i in range(size, len(raw), size):
        before, after = raw[i-size:i], raw[i:i+size]
        if len(after) == size: values.append(sum(abs(a-b) for a,b in zip(before,after))/size)
    native_fps = stream_fps(meta)
    pixel_suspects = annotate_suspects(detect_flash_flicker(luma_series(path), native_fps), duration)
    result = {'duration': duration, 'source': path.name, 'fps': fps,
              'change_candidates': [{'time': round((i+1)/fps, 4), 'difference': values[i]} for i in peaks(values, max(1,int(fps*.2)), 10)],
              'curve': [{'time': round((i+1)/fps, 4), 'difference': v} for i,v in enumerate(values)],
              'suspects': pixel_suspects,
              'note': 'Camera motion, flashes and defects also create peaks. suspects lists white/black flashes and luma flicker. Confirm visually.'}
    write_new(out, result); return result


def planned_cut_times(plan):
    shots = (plan or {}).get('shots', [])
    times = []
    for shot in shots[1:]:
        if shot.get('transition', {}).get('type', 'cut') != 'cut':
            continue
        times.append(float(shot['start']))
    return times


def suspects(path, out, plan=None, beats=None, threshold=0.3, beat_tolerance=0.06,
             models=None, allow_model_download=False, ref_faces=None):
    meta, duration = probe(path)
    if not any(s['codec_type'] == 'video' for s in meta['streams']):
        raise ValueError('no video stream')
    fps = stream_fps(meta)
    if not 0 < threshold < 1:
        raise ValueError('scene threshold must be between 0 and 1')
    detected = [t for t in scene_times(path, threshold) if 0 < t < duration]
    beat_times = None
    if beats is not None:
        beat_times = beat_times_from(json.loads(Path(beats).read_text()))
    report = suspect_report(path, fps, duration, detected, planned_cut_times(plan), beat_times,
                            beat_tolerance, models or [], allow_model_download, ref_faces or [])
    report.update({'duration': duration, 'source': path.name, 'fps': round(fps, 3)})
    write_new(out, report)
    return report


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    for name in ('reference', 'audio', 'motion', 'suspects'):
        sp = sub.add_parser(name); sp.add_argument('source', type=Path); sp.add_argument('output', type=Path)
        if name == 'reference':
            sp.add_argument('--interval', type=float, default=.5); sp.add_argument('--threshold', type=float, default=.3)
        if name == 'motion': sp.add_argument('--fps', type=int, default=12)
        if name == 'suspects':
            sp.add_argument('--plan', type=Path, help='plan.json; measured cuts are compared with planned cut times')
            sp.add_argument('--beats', type=Path, help='beat_grid.py JSON; cuts farther than --beat-tol are suspects')
            sp.add_argument('--threshold', type=float, default=.3)
            sp.add_argument('--beat-tol', type=float, default=0.06, help='seconds from the nearest beat before a cut is off-beat')
            sp.add_argument('--models', default='', help='optional, comma-separated: clip,dino,face,syncnet')
            sp.add_argument('--allow-model-download', action='store_true',
                            help='let an opted-in model fetch weights; default is to skip when weights are absent')
            sp.add_argument('--ref-face', type=Path, nargs='*', default=[], help='reference face images for --models face')
    a = p.parse_args()
    try:
        if a.command == 'reference':
            if not math.isfinite(a.interval) or a.interval <= 0 or not 0 < a.threshold < 1: raise ValueError('invalid sampling settings')
            result = reference(a.source, a.output, a.interval, a.threshold)
        elif a.command == 'audio': result = audio(a.source, a.output)
        elif a.command == 'suspects':
            plan = json.loads(a.plan.read_text()) if a.plan else None
            models = [part.strip().lower() for part in a.models.split(',') if part.strip()]
            result = suspects(a.source, a.output, plan, a.beats, a.threshold, a.beat_tol,
                              models, a.allow_model_download, a.ref_face)
            print(json.dumps({'output': str(a.output), 'duration': result['duration'],
                              'suspects': len(result['suspects']), 'model_notes': result['model_notes']}))
            return
        else:
            if not 1 <= a.fps <= 60: raise ValueError('fps must be 1 through 60')
            result = motion(a.source, a.output, a.fps)
        print(json.dumps({'output': str(a.output), 'duration': result['duration']}))
    except (ValueError, KeyError, OSError, subprocess.CalledProcessError) as exc:
        # Avoid dumping ffmpeg output containing private paths or metadata.
        p.exit(2, f'Inspection failed ({type(exc).__name__}): check local media and output path.\n')


if __name__ == '__main__':
    main()
