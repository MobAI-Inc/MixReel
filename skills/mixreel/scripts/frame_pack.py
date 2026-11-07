#!/usr/bin/env python3
"""Build the stills a review should read, in a fixed order.

Overviews, seam strips, suspect bursts, metric curves, then full-resolution brand
frames. manifest.json lists that order. Requires ffmpeg and Pillow. No model calls.
"""
import argparse
import json
import math
from pathlib import Path
import shutil
import subprocess

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError as exc:
    raise SystemExit('frame_pack requires Pillow. Install it with: python3 -m pip install pillow') from exc


FONT_CANDIDATES = (
    '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
    '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',
    '/usr/share/fonts/TTF/DejaVuSans-Bold.ttf',
)
PRI = {
    'identity_drift': 9, 'lip_sync_offset': 8, 'flash': 8, 'missing_planned_cut': 8,
    'cut_offset': 7, 'flicker': 7, 'sudden_change': 6, 'dino_drift': 5, 'clip_drift': 5,
    'audio_silence': 4, 'unplanned_cut': 3, 'cut_off_beat': 2,
}


def font(size):
    for path in FONT_CANDIDATES:
        if Path(path).is_file():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def probe(path):
    out = subprocess.run(
        ['ffprobe', '-v', 'error', '-show_entries', 'format=duration:stream=codec_type,r_frame_rate,nb_frames',
         '-of', 'json', str(path)], capture_output=True, text=True, check=True)
    data = json.loads(out.stdout)
    video = next(s for s in data['streams'] if s.get('codec_type') == 'video')
    num, den = (int(x) for x in video['r_frame_rate'].split('/'))
    fps = num / den if den else 24
    duration = float(data['format']['duration'])
    count = video.get('nb_frames')
    nframes = int(count) if count and count != 'N/A' else max(1, int(round(duration * fps)))
    return fps, duration, nframes


def fmt(t):
    t = max(0.0, float(t))
    return f'{int(t // 60)}:{t % 60:05.2f}'


def label(img, text, pos='br'):
    """Red text on a dark box. Bottom-right by default; brand frames use the top-left."""
    img = img.copy()
    draw = ImageDraw.Draw(img)
    size = max(12, min(img.height // 14, img.width // 10))
    face = font(size)
    x0, y0, x1, y1 = draw.textbbox((0, 0), text, font=face)
    width, height = x1 - x0, y1 - y0
    margin = 4
    x = img.width - width - 2 * margin if pos[1] == 'r' else 0
    y = img.height - height - 2 * margin - y0 if pos[0] == 'b' else 0
    draw.rectangle((x, y, x + width + 2 * margin, y + height + 2 * margin + max(y0, 0)), fill=(0, 0, 0))
    draw.text((x + margin, y + margin), text, font=face, fill=(255, 40, 40))
    return img


def grid(tiles, cols, gap=6, bg=(255, 0, 255)):
    """Magenta gaps keep a white or black frame visible against its neighbours."""
    rows = math.ceil(len(tiles) / cols)
    width, height = tiles[0].size
    image = Image.new('RGB', (cols * width + (cols - 1) * gap, rows * height + (rows - 1) * gap), bg)
    for i, tile in enumerate(tiles):
        image.paste(tile, ((i % cols) * (width + gap), (i // cols) * (height + gap)))
    return image


def sample_span(start, end, count):
    start, end = int(start), int(end)
    if end < start:
        start, end = end, start
    if count <= 1 or start == end:
        return [start]
    raw = [int(round(start + (end - start) * i / (count - 1))) for i in range(count)]
    raw[0], raw[-1] = start, end
    return sorted(set(raw))


def extract(video, indices, dest):
    dest.mkdir(parents=True, exist_ok=True)
    wanted = sorted({int(i) for i in indices if i >= 0})
    if not wanted:
        return {}
    expr = '+'.join(f'eq(n\\,{i})' for i in wanted)
    pattern = str(dest / '%04d.png')
    proc = subprocess.run(
        ['ffmpeg', '-v', 'error', '-y', '-i', str(video), '-vf', f"select='{expr}'",
         '-fps_mode', 'passthrough', '-start_number', '0', pattern],
        capture_output=True, text=True)
    paths = [dest / f'{i:04d}.png' for i in range(len(wanted))]
    if proc.returncode != 0 or not all(path.is_file() for path in paths):
        for frame in wanted:
            target = dest / f'f{frame:05d}.png'
            subprocess.run(
                ['ffmpeg', '-v', 'error', '-y', '-i', str(video), '-vf', f"select='eq(n\\,{frame})'",
                 '-frames:v', '1', str(target)], check=True)
        return {frame: dest / f'f{frame:05d}.png' for frame in wanted}
    return {frame: path for frame, path in zip(wanted, paths)}


def curve_strip(curves, fps, start, end, event_start, event_end, width=900, row_h=110):
    luma = curves.get('luma') or []
    rows = [('luma', luma)]
    for key, field in (('face', 'id_sim'), ('clip', 'sim_to_shot_start'), ('dino', 'sim_to_shot_start')):
        series = curves.get(key)
        if not series:
            continue
        sparse = {}
        for item in series:
            if item.get(field) is None:
                continue
            sparse[int(round(item['t'] * fps))] = item[field]
        if sparse:
            rows.append((f'{key}.{field}', sparse))
    image = Image.new('RGB', (width, row_h * len(rows)), 'white')
    draw = ImageDraw.Draw(image)
    face = font(16)
    f0, f1 = int(round(start * fps)), int(round(end * fps))
    span = max(1, f1 - f0)

    def x_of(frame):
        return 70 + (frame - f0) / span * (width - 90)

    for r, (name, data) in enumerate(rows):
        y0 = r * row_h
        if isinstance(data, dict):
            pts = [(i, data[i]) for i in range(f0, f1 + 1) if i in data]
        else:
            pts = [(i, data[i]) for i in range(f0, f1 + 1) if 0 <= i < len(data)]
        band0, band1 = x_of(round(event_start * fps)), x_of(round(event_end * fps))
        draw.rectangle((min(band0, band1), y0, max(band0, band1, min(band0, band1) + 3), y0 + row_h - 1),
                       fill=(255, 225, 225))
        draw.text((4, y0 + 4), name, font=face, fill='black')
        if len(pts) > 1:
            values = [v for _, v in pts]
            lo, hi = min(values), max(values)
            if hi <= lo:
                hi = lo + 1
            draw.line([(x_of(i), y0 + row_h - 16 - (v - lo) / (hi - lo) * (row_h - 36)) for i, v in pts],
                      fill='blue', width=2)
            draw.text((width - 170, y0 + 4), f'{lo:.1f}..{hi:.1f}', font=face, fill='gray')
        draw.line((0, y0 + row_h - 1, width, y0 + row_h - 1), fill='gray')
    draw.text((70, row_h * len(rows) - 22), f'{fmt(start)} -> {fmt(end)}   red band = flagged', font=face, fill='red')
    return image


def shot_bounds(plan, detected, duration):
    if plan and plan.get('shots'):
        bounds = []
        for i, shot in enumerate(plan['shots']):
            bounds.append((float(shot['start']), float(shot.get('end', duration)), str(shot.get('id') or f's{i + 1}')))
        return bounds
    cuts = [0.0, *[float(c) for c in detected], float(duration)]
    uniq = []
    for t in cuts:
        if not uniq or abs(t - uniq[-1]) > 1e-3:
            uniq.append(t)
    return [(a, b, f's{i + 1}') for i, (a, b) in enumerate(zip(uniq, uniq[1:]))]


def shot_at(bounds, t):
    for start, end, sid in bounds:
        if start <= t < end:
            return sid
    return bounds[-1][2]


def merge_events(suspects):
    events = []
    for suspect in sorted(suspects, key=lambda s: s.get('start', 0)):
        if events and suspect['start'] <= events[-1]['end'] + 0.25:
            event = events[-1]
            event['end'] = max(event['end'], suspect['end'])
            event['look_from'] = min(event['look_from'], suspect.get('look', {}).get('from', suspect['start']))
            event['look_to'] = max(event['look_to'], suspect.get('look', {}).get('to', suspect['end']))
            event['types'].append(suspect['type'])
            event['ids'].append(suspect.get('id', ''))
            event['reasons'].append(suspect.get('reason', ''))
        else:
            events.append({
                'start': suspect['start'], 'end': suspect['end'],
                'look_from': suspect.get('look', {}).get('from', max(0, suspect['start'] - 0.5)),
                'look_to': suspect.get('look', {}).get('to', suspect['end'] + 0.5),
                'types': [suspect['type']], 'ids': [suspect.get('id', '')],
                'reasons': [suspect.get('reason', '')],
            })
    for event in events:
        event['id'] = 'E' + '+'.join(i[1:] for i in event['ids'] if i) or 'E'
        event['type'] = '+'.join(dict.fromkeys(event['types']))
        event['reason'] = ' ; '.join(dict.fromkeys(r for r in event['reasons'] if r))
        event['priority'] = max(PRI.get(t, 4) for t in event['types'])
    return events


def review_tiles(width, height, edge=2576, cap=4784):
    scale = min(1, edge / max(width, height))
    w, h = width * scale, height * scale
    while math.ceil(w / 28) * math.ceil(h / 28) > cap:
        scale *= 0.99
        w, h = width * scale, height * scale
    return math.ceil(w / 28) * math.ceil(h / 28)


def build(video, out, plan=None, suspects=None, tile_w=320, burst_fps=12, max_events=8, brand_times=None):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    fps, duration, nframes = probe(video)
    payload = json.loads(Path(suspects).read_text()) if suspects else {}
    suspect_list = payload.get('suspects', [])
    curves = payload.get('curves') or {}
    if curves.get('luma'):
        nframes = max(nframes, len(curves['luma']))
    detected = payload.get('detected_cuts', [])
    bounds = shot_bounds(plan, detected, duration)
    last = nframes - 1

    def clamp(frame):
        return min(max(int(frame), 0), last)

    needed = []
    overviews = []
    cols = rows = 3
    count = cols * rows
    for start, end, sid in bounds:
        f0, f1 = clamp(round(start * fps)), clamp(round(end * fps) - 1)
        frames = [clamp(i) for i in sample_span(f0, f1, count)]
        overviews.append((sid, start, end, frames))
        needed.extend(frames)
    seam_times = sorted(set(round(float(c), 3) for c in detected) | {round(b[0], 3) for b in bounds[1:]})
    seams = []
    for cut in seam_times:
        frame = clamp(round(cut * fps))
        frames = [clamp(frame + delta) for delta in (-2, -1, 0, 1)]
        seams.append((cut, frames))
        needed.extend(frames)
    events = merge_events(suspect_list)
    events.sort(key=lambda e: -e['priority'])
    dropped = events[max_events:]
    events = events[:max_events]
    bursts = []
    for event in events:
        a0, a1 = event['look_from'], event['look_to']
        if event['end'] - event['start'] <= 1.5:
            center = (event['start'] + event['end']) / 2
            a0 = max(0, center - 8 / fps)
            frames = []
            for i in range(16):
                frame = clamp(round(a0 * fps) + i)
                if frames and frame == frames[-1]:
                    break
                frames.append(frame)
        else:
            step = max(1, int(round(fps / burst_fps)))
            frames = list(range(clamp(round(a0 * fps)), clamp(round(a1 * fps)) + 1, step))
            if len(frames) > 16:
                frames = [frames[int(round(i))] for i in [n * (len(frames) - 1) / 15 for n in range(16)]]
                frames = [clamp(f) for f in frames]
        bursts.append((event, [clamp(f) for f in frames], a0, a1))
        needed.extend(bursts[-1][1])
    brands = sorted(set(round(float(t), 3) for t in (brand_times or [])))
    brand_frames = [(t, clamp(round(t * fps))) for t in brands]
    needed.extend(frame for _, frame in brand_frames)

    paths = extract(video, needed, out / '_frames')
    images = []

    def save(image, name, kind, frames, note):
        image.save(out / name)
        images.append({
            'file': name, 'kind': kind, 'frames': [int(f) for f in frames],
            'times': [round(f / fps, 3) for f in frames], 'px': list(image.size),
            'review_tiles': review_tiles(*image.size), 'note': note,
        })

    def tile(frame, sid, width=None, pos='br'):
        image = Image.open(paths[frame]).convert('RGB')
        if width and image.width != width:
            height = max(1, round(image.height * width / image.width))
            image = image.resize((width, height), Image.Resampling.LANCZOS)
        return label(image, f'{sid} #{frame} {fmt(frame / fps)}', pos)

    for sid, start, end, frames in overviews:
        save(grid([tile(f, sid, tile_w) for f in frames], cols), f'1_overview_{sid}.png', 'overview', frames,
             f'{sid} {fmt(start)}-{fmt(end)} includes first and last frame')
    for cut, frames in seams:
        save(grid([tile(f, shot_at(bounds, f / fps), tile_w) for f in frames], 4),
             f'2_seam_{fmt(cut).replace(":", "m")}.png', 'seam', frames,
             f'cut near {fmt(cut)}: last frames of the outgoing shot beside the first frames of the next')
    for event, frames, a0, a1 in bursts:
        save(grid([tile(f, shot_at(bounds, f / fps), tile_w) for f in frames], 4),
             f'3_burst_{event["id"]}.png', 'burst', frames,
             f'{event["type"]} {event["start"]}-{event["end"]}: {event["reason"]}')
        if curves.get('luma'):
            save(curve_strip(curves, fps, a0, a1, event['start'], event['end']),
                 f'3_curve_{event["id"]}.png', 'curve', [clamp(round(a0 * fps)), clamp(round(a1 * fps))],
                 'luma around the suspect; red band is the flagged range')
    for t, frame in brand_frames:
        save(label(Image.open(paths[frame]).convert('RGB'), f'{shot_at(bounds, t)} #{frame} {fmt(t)}', 'tl'),
             f'4_brand_{fmt(t).replace(":", "m")}.png', 'brand_fullres', [frame],
             'native resolution, label at the top-left so a bottom logo stays visible')
    manifest = {
        'video': Path(video).name, 'fps': round(fps, 3),
        'reading_order': ['overview', 'seam', 'burst', 'curve', 'brand_fullres'],
        'images': images,
        'dropped_events_not_imaged': [
            {'id': e['id'], 'type': e['type'], 'start': e['start'], 'priority': e['priority']} for e in dropped],
        'totals': {'images': len(images), 'review_tiles': sum(i['review_tiles'] for i in images)},
        'note': 'Read the images in this order: all overviews, then seams, then each suspect burst and its curve, then brand frames.',
    }
    (out / 'manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
    shutil.rmtree(out / '_frames', ignore_errors=True)
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video', type=Path)
    parser.add_argument('out', type=Path)
    parser.add_argument('--plan', type=Path)
    parser.add_argument('--suspects', type=Path, help='qa_check.py or media_inspect.py suspects JSON')
    parser.add_argument('--tile-w', type=int, default=320)
    parser.add_argument('--burst-fps', type=float, default=12)
    parser.add_argument('--max-events', type=int, default=8)
    parser.add_argument('--brand-times', nargs='*', type=float, default=[])
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text()) if args.plan else None
    try:
        manifest = build(args.video, args.out, plan, args.suspects, args.tile_w, args.burst_fps,
                         args.max_events, args.brand_times)
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        parser.exit(2, f'frame pack failed ({type(exc).__name__}): check the video, plan and suspects.\n')
    print(json.dumps({'out': str(args.out), 'images': manifest['totals']['images'],
                      'reading_order': manifest['reading_order']}))


if __name__ == '__main__':
    main()
