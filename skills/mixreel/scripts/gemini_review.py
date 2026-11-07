#!/usr/bin/env python3
"""Optional Gemini native-video review of suspect ranges.

Findings are hints for the person reviewing the cut. They are not a pass, a
fail, or acceptance. The call runs only when a Gemini key is available AND
review was requested (--run, MIXREEL_GEMINI_REVIEW=1, or
~/.config/mixreel/review.json {"gemini_review": true}). Otherwise this prints
a skip note and exits 0. It is never required, and it does not run as part of
qa_check.py or media_inspect.py.

Request shape follows the Gemini Interactions API video sample: static mode, fps,
and numeric start_offset/end_offset. Those offset units were not re-checked against
a live response in this repo.
"""
import argparse
import json
import os
from pathlib import Path
import urllib.error
import urllib.request


def should_call(key, requested):
    return bool(key) and bool(requested)


def skip_note(key, requested):
    if not key and not requested:
        return 'Gemini review skipped: no API key and review was not requested.'
    if not key:
        return 'Gemini review skipped: no Gemini API key in the environment or credentials file.'
    return 'Gemini review skipped: not requested. Pass --run or set MIXREEL_GEMINI_REVIEW=1.'


def resolve_key(environ=None, credentials_path=None):
    environ = os.environ if environ is None else environ
    for name in ('GEMINI_API_KEY', 'GOOGLE_API_KEY'):
        value = (environ.get(name) or '').strip()
        if value:
            return value
    path = Path.home() / '.config' / 'mixreel' / 'credentials.json' if credentials_path is None else Path(credentials_path)
    if not path.is_file():
        return ''
    try:
        data = json.loads(path.read_text())
    except ValueError:
        return ''
    keys = data.get('keys') if isinstance(data, dict) else None
    if not isinstance(keys, dict):
        return ''
    for name in ('gemini', 'google'):
        value = keys.get(name)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ''


def review_requested(cli_run=False, environ=None, config_path=None):
    if cli_run:
        return True
    environ = os.environ if environ is None else environ
    if (environ.get('MIXREEL_GEMINI_REVIEW') or '').strip().lower() in ('1', 'true', 'yes'):
        return True
    path = Path.home() / '.config' / 'mixreel' / 'review.json' if config_path is None else Path(config_path)
    if not path.is_file():
        return False
    try:
        data = json.loads(path.read_text())
    except ValueError:
        return False
    return isinstance(data, dict) and data.get('gemini_review') is True


def _mmss(t):
    t = max(0.0, float(t))
    return f'{int(t // 60):02d}:{t % 60:06.3f}'


def _prompt(plan, suspects, brand, window=None):
    shots = '\n'.join(
        f"- {s.get('id')} {_mmss(s['start'])}-{_mmss(s['end'])}: {s.get('description', s.get('function', ''))}"
        for s in plan.get('shots', []))
    flagged = '\n'.join(
        f"- {s.get('id')} {s.get('type')} {_mmss(s['start'])}-{_mmss(s['end'])} ({s.get('reason', s.get('detector', ''))})"
        for s in suspects)
    scope = f'Only judge {_mmss(window[0])}-{_mmss(window[1])}.' if window else 'Watch the whole film with sound.'
    return (
        f'You are reviewing a finished vertical ad. {scope}\n'
        f'Approved plan:\n{shots}\nBrand rules: {brand or "none supplied"}\n'
        f'Detectors flagged these places. They can be false alarms. For each, say confirmed, false_alarm, or unsure:\n'
        f'{flagged or "- none"}\n'
        'Report only what you can see or hear. Use MM:SS.sss times. Do not treat taste as a defect. '
        'List anything you could not verify, including small text and single-frame events.'
    )


def build_requests(plan, suspects, brand, fps, zoom_fps, model, limit=8):
    whole = {
        'pass': 'A_whole_film',
        'processing': {'type': 'static', 'fps': fps},
        'prompt': _prompt(plan, suspects, brand),
    }
    zooms = []
    for suspect in suspects[:limit]:
        look = suspect.get('look') or {'from': suspect['start'], 'to': suspect['end']}
        zooms.append({
            'pass': f'B_zoom_{suspect.get("id", "suspect")}',
            'processing': {
                'type': 'static', 'fps': zoom_fps,
                'start_offset': look['from'], 'end_offset': look['to'],
            },
            'prompt': _prompt(plan, [suspect], brand, (look['from'], look['to'])),
        })
    return {'model': model, 'requests': [whole, *zooms]}


def _redact(text, key):
    if key and key in text:
        return text.replace(key, '***')
    return text


def _request(url, key, payload=None, extra_headers=None, data=None, timeout=120):
    headers = {'x-goog-api-key': key}
    if data is None and payload is not None:
        headers['Content-Type'] = 'application/json'
    if extra_headers:
        headers.update(extra_headers)
    body = data if data is not None else (json.dumps(payload).encode() if payload is not None else None)
    req = urllib.request.Request(url, data=body, headers=headers, method='POST' if body is not None else 'GET')
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            raw = resp.read()
            return resp.headers, json.loads(raw.decode() or '{}') if raw else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode(errors='replace')[:500]
        raise RuntimeError(f'Gemini HTTP {exc.code}: {_redact(detail, key)}') from None


def _upload(video, key, opener=_request):
    path = Path(video)
    data = path.read_bytes()
    headers, _ = opener(
        'https://generativelanguage.googleapis.com/upload/v1beta/files', key,
        payload={'file': {'display_name': path.name}},
        extra_headers={
            'X-Goog-Upload-Protocol': 'resumable',
            'X-Goog-Upload-Command': 'start',
            'X-Goog-Upload-Header-Content-Length': str(len(data)),
            'X-Goog-Upload-Header-Content-Type': 'video/mp4',
            'Content-Type': 'application/json',
        })
    upload_url = headers.get('X-Goog-Upload-URL') or headers.get('x-goog-upload-url')
    if not upload_url:
        raise RuntimeError('Gemini upload did not return an upload URL')
    _, info = opener(upload_url, key, data=data, extra_headers={
        'Content-Length': str(len(data)),
        'X-Goog-Upload-Offset': '0',
        'X-Goog-Upload-Command': 'upload, finalize',
    })
    file_info = info.get('file') or info
    return file_info.get('uri'), file_info.get('name')


def perform(video, requests, key, opener=_request):
    import time
    uri, name = _upload(video, key, opener)
    state = 'ACTIVE'
    if name:
        state = ''
        for _ in range(15):
            _, status = opener(f'https://generativelanguage.googleapis.com/v1beta/{name}', key)
            state = status.get('state') or (status.get('file') or {}).get('state') or ''
            if state in ('ACTIVE', ''):
                break
            if state == 'FAILED':
                raise RuntimeError('Gemini file processing failed')
            time.sleep(2)
        if state not in ('ACTIVE', ''):
            raise RuntimeError('Gemini file was not ready')
    answers = []
    for item in requests['requests']:
        _, response = opener(
            'https://generativelanguage.googleapis.com/v1beta/interactions', key,
            payload={
                'model': requests['model'],
                'input': [
                    {'type': 'video', 'uri': uri, 'mime_type': 'video/mp4', 'processing': item['processing']},
                    {'type': 'text', 'text': item['prompt']},
                ],
            })
        answers.append({'pass': item['pass'], 'response': response})
    return {'called': True, 'skipped': False, 'file': name, 'answers': answers}


def review(video, plan, suspects, brand='', model='gemini-3.8-flash', fps=2, zoom_fps=10,
           key=None, requested=None, opener=None):
    """Return a skip note or the Gemini answers. opener is the HTTP function, for tests."""
    if key is None:
        key = resolve_key()
    if requested is None:
        requested = review_requested()
    body = build_requests(plan, suspects, brand, fps, zoom_fps, model)
    if not should_call(key, requested):
        return {'skipped': True, 'called': False, 'note': skip_note(key, requested), **body}
    answers = perform(video, body, key, opener or _request)
    answers.update(body)
    answers['note'] = 'Gemini returned hints for the suspect ranges. Hints are not a verdict.'
    return answers


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('video', type=Path)
    parser.add_argument('--plan', type=Path, required=True)
    parser.add_argument('--suspects', type=Path)
    parser.add_argument('--brand', default='')
    parser.add_argument('--model', default='gemini-3.8-flash')
    parser.add_argument('--fps', type=float, default=2)
    parser.add_argument('--zoom-fps', type=float, default=10)
    parser.add_argument('--run', action='store_true', help='request the Gemini call; still skipped without a key')
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    plan = json.loads(args.plan.read_text())
    suspects = []
    if args.suspects:
        payload = json.loads(args.suspects.read_text())
        suspects = payload.get('suspects', payload if isinstance(payload, list) else [])
    try:
        result = review(args.video, plan, suspects, args.brand, args.model, args.fps, args.zoom_fps,
                        requested=review_requested(args.run))
    except (OSError, RuntimeError, ValueError, urllib.error.URLError) as exc:
        parser.exit(2, f'Gemini review failed ({type(exc).__name__}).\n')
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.out:
        args.out.write_text(text)
    if result.get('skipped'):
        print(json.dumps({'skipped': True, 'note': result['note']}))
        raise SystemExit(0)
    print(json.dumps({'called': True, 'passes': [a['pass'] for a in result.get('answers', [])]}))


if __name__ == '__main__':
    main()
