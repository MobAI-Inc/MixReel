#!/usr/bin/env python3
"""Pixel diff between keyframe versions, plus the input manifest.

Reports changed and unchanged outputs so a review looks at the diffs.
The manifest records model, prompt, refs and the output hash.

Pair mode:  keyframe_diff.py BEFORE AFTER [--manifest inputs.json]
Batch mode: keyframe_diff.py --batch DIR

A batch directory may contain manifest.json with an "items" list, one subdirectory
per keyframe (before.png and after.png, optional manifest.json), or flat version
pairs named name.v1.png / name.v2.png or name.prev.png / name.png.
Requires Pillow. No network.
"""
import argparse
import hashlib
import json
from pathlib import Path

try:
    from PIL import Image, ImageChops, ImageStat
except ImportError as exc:
    raise SystemExit('keyframe_diff requires Pillow. Install it with: python3 -m pip install pillow') from exc


IMAGE_EXT = {'.png', '.jpg', '.jpeg', '.webp'}


def file_hash(path):
    digest = hashlib.sha256()
    with open(path, 'rb') as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b''):
            digest.update(chunk)
    return 'sha256:' + digest.hexdigest()


def compare(before, after, epsilon=2):
    left = Image.open(before).convert('RGBA')
    right = Image.open(after).convert('RGBA')
    size_mismatch = left.size != right.size
    if size_mismatch:
        right = right.resize(left.size, Image.Resampling.LANCZOS)
    diff = ImageChops.difference(left, right)
    stat = ImageStat.Stat(diff)
    mean_abs = round(sum(stat.mean) / len(stat.mean), 3)
    max_abs = max(high for _, high in diff.getextrema())
    raw = diff.tobytes()
    total = len(raw) // 4 or 1
    changed_px = sum(1 for i in range(0, len(raw), 4) if max(raw[i:i + 4]) > epsilon)
    unchanged = (not size_mismatch) and max_abs <= epsilon
    return {
        'mean_abs': mean_abs,
        'max_abs': int(max_abs),
        'changed_fraction': round(changed_px / total, 4),
        'size_mismatch': size_mismatch,
        'unchanged': unchanged,
    }


def manifest_fields(data):
    if not isinstance(data, dict):
        return {}
    fields = {}
    for key in ('model', 'prompt', 'refs'):
        if key in data:
            fields[key] = data[key]
    if 'output_hash' in data:
        fields['manifest_output_hash'] = data['output_hash']
    elif 'output' in data and isinstance(data['output'], str) and data['output'].startswith('sha256:'):
        fields['manifest_output_hash'] = data['output']
    return fields


def judge(before, after, meta, epsilon):
    measurement = compare(before, after, epsilon)
    output_hash = file_hash(after)
    row = {
        'before': str(before), 'after': str(after), 'output_hash': output_hash,
        **manifest_fields(meta), **measurement,
    }
    expected = row.get('manifest_output_hash')
    hash_mismatch = bool(expected) and expected != output_hash
    row['hash_matches'] = (not expected) or not hash_mismatch
    if measurement['unchanged'] and not hash_mismatch:
        row['status'] = 'unchanged'
        row['reason'] = 'pixels match'
    elif hash_mismatch and measurement['unchanged']:
        row['status'] = 'changed'
        row['reason'] = 'output hash does not match the manifest'
    else:
        row['status'] = 'changed'
        row['reason'] = 'pixels differ' if not measurement['size_mismatch'] else 'frame size differs'
    return row


def _images(directory):
    return sorted(p for p in Path(directory).iterdir() if p.suffix.lower() in IMAGE_EXT and p.is_file())


def pair_dir(directory):
    directory = Path(directory)
    meta = {}
    manifest = directory / 'manifest.json'
    if manifest.is_file():
        meta = json.loads(manifest.read_text())
    before = directory / 'before.png'
    after_name = 'after.png'
    if isinstance(meta, dict) and isinstance(meta.get('output'), str) and not meta['output'].startswith('sha256:'):
        after_name = meta['output']
    after = directory / after_name
    if not before.is_file() or not after.is_file():
        images = _images(directory)
        if len(images) < 2:
            raise ValueError(f'{directory} needs before.png and after.png, or two images')
        before, after = images[0], images[-1]
    return {'id': directory.name, 'before': before, 'after': after, 'meta': meta if isinstance(meta, dict) else {}}


def batch_items(directory):
    directory = Path(directory)
    manifest = directory / 'manifest.json'
    if manifest.is_file():
        data = json.loads(manifest.read_text())
        items = data if isinstance(data, list) else data.get('items', [])
        if items and isinstance(items[0], dict) and 'before' in items[0] and 'after' in items[0]:
            rows = []
            for item in items:
                rows.append({
                    'id': item.get('id') or Path(item['after']).stem,
                    'before': directory / item['before'],
                    'after': directory / item['after'],
                    'meta': item,
                })
            return rows
    subs = sorted(p for p in directory.iterdir() if p.is_dir() and not p.name.startswith('.'))
    if subs:
        return [pair_dir(sub) for sub in subs]
    groups = {}
    prevs = {}
    for path in _images(directory):
        stem = path.stem
        if stem.endswith('.prev'):
            prevs[stem[:-5]] = path
            continue
        if '.v' in stem:
            base, _, number = stem.rpartition('.v')
            if number.isdigit():
                groups.setdefault(base, []).append((int(number), path))
                continue
        groups.setdefault(stem, []).append((10**9, path))
    rows = []
    for base, prev in sorted(prevs.items()):
        current = next((p for p in _images(directory) if p.stem == base), None)
        if current:
            rows.append({'id': base, 'before': prev, 'after': current, 'meta': {}})
    for base, versions in sorted(groups.items()):
        if base in prevs:
            continue
        versions.sort()
        if len(versions) >= 2:
            rows.append({'id': base, 'before': versions[-2][1], 'after': versions[-1][1], 'meta': {}})
    if not rows:
        raise ValueError(f'no keyframe pairs in {directory}')
    return rows


def run(pairs, epsilon=2):
    changed, unchanged = [], []
    for pair in pairs:
        row = judge(pair['before'], pair['after'], pair.get('meta') or {}, epsilon)
        row['id'] = pair.get('id') or Path(pair['after']).stem
        (changed if row['status'] == 'changed' else unchanged).append(row)
    return {
        'changed': changed, 'unchanged': unchanged,
        'note': 'Review the changed images. Reuse unchanged outputs only if they were previously accepted '
                'and the requirements and references are unchanged. A failed output stays failed after '
                'a no-op edit; unchanged pixels are not an acceptance verdict.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('before', nargs='?', type=Path)
    parser.add_argument('after', nargs='?', type=Path)
    parser.add_argument('--batch', type=Path, help='folder of keyframe pairs')
    parser.add_argument('--manifest', type=Path, help='input manifest for a single pair')
    parser.add_argument('--out', type=Path, help='write the report here; default is stdout')
    parser.add_argument('--epsilon', type=float, default=2, help='per-channel delta treated as unchanged')
    args = parser.parse_args()
    try:
        if args.batch:
            pairs = batch_items(args.batch)
        elif args.before and args.after:
            meta = json.loads(args.manifest.read_text()) if args.manifest else {}
            pairs = [{'id': args.after.stem, 'before': args.before, 'after': args.after, 'meta': meta}]
        else:
            parser.error('give BEFORE AFTER or --batch DIR')
        report = run(pairs, args.epsilon)
    except (OSError, ValueError, KeyError) as exc:
        parser.exit(2, f'{exc}\n')
    text = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    if args.out:
        args.out.write_text(text)
        print(json.dumps({'out': str(args.out), 'changed': len(report['changed']), 'unchanged': len(report['unchanged'])}))
    else:
        print(text, end='')


if __name__ == '__main__':
    main()
