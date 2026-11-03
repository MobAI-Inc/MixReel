#!/usr/bin/env python3
"""Optional embedding, face and lip-sync checks. Not used unless a caller passes --models.

Nothing in this module imports torch, open_clip or insightface until that model is
requested. Missing packages and missing weights are skipped. Weights are not
downloaded unless the caller sets allow_download=True.

InsightFace buffalo_s weights are licensed for non-commercial research.
SyncNet weights are released for research. Do not use either on a commercial job
without a separate license. This file does not vendor or fetch those weights.
"""
import os
from contextlib import contextmanager
from pathlib import Path


LICENSE = {
    'face': 'InsightFace buffalo_s weights are licensed for non-commercial research. Commercial jobs need a separate license.',
    'syncnet': 'SyncNet weights are released for research. Commercial jobs need a separate license. Set MIXREEL_SYNCNET_DIR; weights are not downloaded.',
}


def cosine(a, b):
    dot = sum(x * y for x, y in zip(a, b))
    na = sum(x * x for x in a) ** 0.5
    nb = sum(x * x for x in b) ** 0.5
    if na < 1e-8 or nb < 1e-8:
        return 0.0
    return dot / (na * nb)


def _shot(cuts, t):
    return sum(1 for c in cuts if c <= t)


def embedding_drift(samples, cuts, name, thr_start, thr_step):
    """samples are (time, vector). Flag a drop versus the shot's first sample or the previous sample."""
    cuts = sorted(float(c) for c in cuts)
    suspects, curve = [], []
    shots = [_shot(cuts, t) for t, _ in samples]
    for k, (t, vec) in enumerate(samples):
        first = next(i for i, shot in enumerate(shots) if shot == shots[k])
        sim_start = cosine(vec, samples[first][1])
        sim_prev = cosine(vec, samples[k - 1][1]) if k and shots[k - 1] == shots[k] else 1.0
        curve.append({'t': round(float(t), 3), 'sim_to_shot_start': round(sim_start, 3), 'sim_to_prev': round(sim_prev, 3)})
        if sim_start < thr_start or sim_prev < thr_step:
            suspects.append({
                'type': f'{name}_drift',
                'start': round(float(samples[k - 1][0] if k else t), 3),
                'end': round(float(t), 3),
                'score': round(min(sim_start, sim_prev), 3),
                'reason': f'{name} similarity dropped (shot start {sim_start:.3f}, previous {sim_prev:.3f})',
                'detector': f'{name}: start<{thr_start} or step<{thr_step}',
            })
    return _merge(suspects), curve


def _merge(suspects, gap=0.3):
    out = []
    for suspect in sorted(suspects, key=lambda s: (s['type'], s['start'])):
        if out and out[-1]['type'] == suspect['type'] and suspect['start'] - out[-1]['end'] <= gap:
            out[-1]['end'] = max(out[-1]['end'], suspect['end'])
            out[-1]['score'] = min(out[-1]['score'], suspect['score'])
        else:
            out.append(dict(suspect))
    return out


def lip_sync_suspect(offset_frames, fps, duration):
    if offset_frames is None or abs(offset_frames) < 1 or not fps:
        return None
    seconds = offset_frames / fps
    return {
        'type': 'lip_sync_offset',
        'start': 0.0,
        'end': round(float(duration), 3),
        'score': round(seconds, 3),
        'reason': f'SyncNet lip-sync offset is {int(offset_frames)} frames ({seconds:.3f}s)',
        'detector': 'syncnet',
    }


@contextmanager
def _offline(allow_download):
    if allow_download:
        yield
        return
    keys = ('HF_HUB_OFFLINE', 'TRANSFORMERS_OFFLINE', 'HF_DATASETS_OFFLINE')
    previous = {key: os.environ.get(key) for key in keys}
    for key in keys:
        os.environ[key] = '1'
    try:
        yield
    finally:
        for key, value in previous.items():
            if value is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = value


def _sample_times(duration, rate=4):
    if duration <= 0:
        return [0.0]
    step = 1 / rate
    times, t = [], 0.0
    while t < duration:
        times.append(round(t, 3))
        t += step
    return times or [0.0]


def _extract_times(video, times, dest):
    import subprocess
    dest.mkdir(parents=True, exist_ok=True)
    # One seek per sample keeps this optional path independent of frame_pack.
    paths = []
    for i, t in enumerate(times):
        target = dest / f'{i:04d}.png'
        subprocess.run(
            ['ffmpeg', '-v', 'error', '-y', '-ss', f'{t:.3f}', '-i', str(video), '-frames:v', '1', str(target)],
            check=True)
        paths.append(target)
    return paths


def _clip(video, fps, duration, cuts, allow_download, ref_faces):
    import tempfile
    with _offline(allow_download):
        import open_clip
        import torch
        from PIL import Image
        model, _, preprocess = open_clip.create_model_and_transforms('ViT-B-32', pretrained='laion2b_s34b_b79k')
        model.eval()
        times = _sample_times(duration, 4)
        paths = _extract_times(video, times, Path(tempfile.mkdtemp(prefix='mixreel-clip-')))
        images = [preprocess(Image.open(p).convert('RGB')) for p in paths]
        with torch.no_grad():
            emb = model.encode_image(torch.stack(images))
            emb = emb / emb.norm(dim=-1, keepdim=True)
        samples = [(t, row.tolist()) for t, row in zip(times, emb)]
    suspects, curve = embedding_drift(samples, cuts, 'clip', 0.85, 0.9)
    return suspects, curve


def _load_dino(torch, allow_download):
    if allow_download:
        return torch.hub.load('facebookresearch/dinov2', 'dinov2_vits14',
                              trust_repo=True, verbose=False), None
    hub = Path(torch.hub.get_dir())
    sources = sorted(path for path in hub.glob('facebookresearch_dinov2*')
                     if (path / 'hubconf.py').is_file())
    weights = hub / 'checkpoints' / 'dinov2_vits14_pretrain.pth'
    if not sources or not weights.is_file():
        return None, 'dino skipped: DINOv2 source or weights are not cached locally, so nothing was downloaded'
    # HF offline flags do not constrain torch.hub. Load both inputs locally and
    # disable the backbone's automatic pretrained-weight download.
    model = torch.hub.load(str(sources[0]), 'dinov2_vits14', source='local', pretrained=False)
    model.load_state_dict(torch.load(weights, map_location='cpu', weights_only=True))
    return model, None


def _dino(video, fps, duration, cuts, allow_download, ref_faces):
    with _offline(allow_download):
        import torch
        model, note = _load_dino(torch, allow_download)
        if model is None:
            return [], note
        import numpy as np
        from PIL import Image
        model.eval()
        times = _sample_times(duration, 4)
        import tempfile
        paths = _extract_times(video, times, Path(tempfile.mkdtemp(prefix='mixreel-dino-')))
        mean = np.array([0.485, 0.456, 0.406], dtype='float32')
        std = np.array([0.229, 0.224, 0.225], dtype='float32')
        batch = []
        for path in paths:
            arr = np.asarray(Image.open(path).convert('RGB').resize((224, 224)), dtype='float32') / 255.0
            arr = (arr - mean) / std
            batch.append(arr.transpose(2, 0, 1))
        with torch.no_grad():
            emb = model(torch.tensor(np.stack(batch), dtype=torch.float32))
            emb = emb / emb.norm(dim=-1, keepdim=True)
        samples = [(t, row.tolist()) for t, row in zip(times, emb)]
    suspects, _curve = embedding_drift(samples, cuts, 'dino', 0.6, 0.8)
    return suspects, None


def _face(video, fps, duration, cuts, allow_download, ref_faces):
    cache = Path.home() / '.insightface' / 'models' / 'buffalo_s'
    if not allow_download and not any(cache.glob('*.onnx')):
        return [], 'face skipped: buffalo_s weights are not installed locally, so nothing was downloaded'
    import numpy as np
    from insightface.app import FaceAnalysis
    from PIL import Image
    import tempfile
    app = FaceAnalysis(name='buffalo_s', providers=['CPUExecutionProvider'], allowed_modules=['detection', 'recognition'])
    app.prepare(ctx_id=-1, det_size=(640, 640))
    refs = []
    for ref in ref_faces:
        image = np.asarray(Image.open(ref).convert('RGB'))[:, :, ::-1]
        found = app.get(image)
        if found:
            refs.append(found[0].normed_embedding)
    times = _sample_times(duration, 4)
    paths = _extract_times(video, times, Path(tempfile.mkdtemp(prefix='mixreel-face-')))
    suspects = []
    for t, path in zip(times, paths):
        image = np.asarray(Image.open(path).convert('RGB'))[:, :, ::-1]
        found = app.get(image)
        if not found:
            continue
        face = max(found, key=lambda item: (item.bbox[2] - item.bbox[0]) * (item.bbox[3] - item.bbox[1]))
        if not refs:
            refs.append(face.normed_embedding)
            continue
        score = float(max(face.normed_embedding @ ref for ref in refs))
        if score < 0.45:
            suspects.append({
                'type': 'identity_drift',
                'start': round(float(t), 3), 'end': round(float(t), 3), 'score': round(score, 3),
                'reason': f'ArcFace similarity to the reference face is {score:.3f}',
                'detector': 'arcface cos<0.45',
            })
    return _merge(suspects, gap=1.0), None


def _syncnet(video, fps, duration, cuts, allow_download, ref_faces):
    root = os.environ.get('MIXREEL_SYNCNET_DIR', '').strip()
    if not root:
        return [], 'syncnet skipped: MIXREEL_SYNCNET_DIR is unset. Weights are research-only and are not downloaded.'
    root = Path(root)
    if not root.is_dir():
        return [], 'syncnet skipped: MIXREEL_SYNCNET_DIR is not a directory'
    weights = list(root.glob('*.model')) + list(root.glob('**/*.model'))
    if not weights:
        return [], 'syncnet skipped: no SyncNet weights in MIXREEL_SYNCNET_DIR. Nothing was downloaded.'
    demo = root / 'demo_syncnet.py'
    if not demo.is_file():
        return [], 'syncnet skipped: demo_syncnet.py was not found in MIXREEL_SYNCNET_DIR'
    import subprocess
    proc = subprocess.run(['python3', str(demo), '--videofile', str(video)], capture_output=True, text=True, timeout=300)
    text = (proc.stdout or '') + '\n' + (proc.stderr or '')
    offset = None
    for line in text.splitlines():
        lower = line.lower()
        if 'offset' in lower:
            digits = [int(part) for part in line.replace(',', ' ').split() if part.lstrip('-').isdigit()]
            if digits:
                offset = digits[-1]
    suspect = lip_sync_suspect(offset, fps, duration)
    if suspect is None:
        return [], 'syncnet ran but reported no frame offset'
    return [suspect], None


_HANDLERS = {'clip': _clip, 'dino': _dino, 'face': _face, 'syncnet': _syncnet}


def run_optional(video, fps, duration, cuts, models, allow_download=False, ref_faces=None):
    notes, suspects, curves = [], [], {}
    for name in models:
        if name in LICENSE:
            notes.append(LICENSE[name])
        handler = _HANDLERS.get(name)
        if handler is None:
            notes.append(f'{name} skipped: unknown optional model')
            continue
        try:
            found, curve = handler(video, fps, duration, cuts, allow_download, ref_faces or [])
        except ImportError as exc:
            notes.append(f'{name} skipped: optional package is not installed ({getattr(exc, "name", None) or exc})')
            continue
        except Exception as exc:
            notes.append(f'{name} skipped: {type(exc).__name__}: {exc}')
            continue
        suspects.extend(found or [])
        if isinstance(curve, list):
            curves[name] = curve
        elif isinstance(curve, str) and curve:
            notes.append(curve)
    return notes, suspects, curves
