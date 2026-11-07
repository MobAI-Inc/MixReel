"""Official Seedance video generation adapter (Volcengine Ark and BytePlus).

Checked against public docs on 2026-11-03:

- Volcengine create: POST https://ark.cn-beijing.volces.com/api/v3/contents/generations/tasks
  Field reference: the Ark create-video-generation-task page and the tutorial at
  https://ark.volcengine.com/region:cn-beijing/docs/video-generation-tutorial
- BytePlus create: POST https://ark.ap-southeast.bytepluses.com/api/v3/contents/generations/tasks
  https://ai.byteplus.com/ark/region:ap-southeast-1/docs/video-generation-tutorial
- Query either host: GET {base}/contents/generations/tasks/{id}
- Auth: Authorization: Bearer $ARK_API_KEY
- A succeeded task returns content.video_url. BytePlus documents that the URL is
  kept for 24 hours and can be downloaded a limited number of times. Download
  promptly. Volcengine documents task-id expiry (7 days for a normal task) on
  the create-task page; treat the file URL as short-lived either way.

Model IDs are dated and belong in your config. Examples seen in those docs on
the check date, not defaults baked into a call:

- Volcengine: doubao-seedance-2-5-260628, doubao-seedance-2-0-260128
- BytePlus: dreamina-seedance-2-5-260628, dreamina-seedance-2-0-260128

Set ARK_API_BASE to the host your key uses. The default is the Volcengine
Beijing host. Reference audio on the 2.0 series must be sent with an image or
a video. Seedance 2.5 may send audio alone. First/last frame and reference
roles cannot be mixed. This adapter does not add a prompt formula.
"""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

from .base import (
    ProviderError,
    TaskStatus,
    VideoProvider,
    VideoRequest,
    canonical_state,
    default_transport,
    download_bytes,
    http_json,
    require_key,
)

DEFAULT_BASE = "https://ark.cn-beijing.volces.com/api/v3"
BYTEPLUS_BASE = "https://ark.ap-southeast.bytepluses.com/api/v3"
DOCS = "https://ark.volcengine.com/region:cn-beijing/docs/video-generation-tutorial"
FRAME_ROLES = {"first_frame", "last_frame"}
REFERENCE_ROLES = {"reference_image", "reference_video", "reference_audio"}
KIND_TYPE = {"image": "image_url", "video": "video_url", "audio": "audio_url"}
RATIOS = ("21:9", "16:9", "4:3", "1:1", "3:4", "9:16", "adaptive")


def family(model):
    name = (model or "").lower()
    if "seedance-2-5" in name or "seedance-2.5" in name:
        return "2.5"
    if "seedance-2-0" in name or "seedance-2.0" in name:
        return "2.0"
    return ""


class SeedanceVideo(VideoProvider):
    name = "seedance"
    docs_checked = "2026-11-03"

    def __init__(self, model, api_key=None, base_url=None, transport=None):
        self.model = (model or "").strip()
        self.api_key = require_key(api_key if api_key is not None else os.environ.get("ARK_API_KEY"), "ARK_API_KEY")
        self.base_url = (base_url or os.environ.get("ARK_API_BASE") or DEFAULT_BASE).rstrip("/")
        self.transport = transport or default_transport

    def _headers(self):
        return {"Authorization": "Bearer " + self.api_key, "Content-Type": "application/json"}

    def capabilities(self) -> dict:
        kind = family(self.model)
        durations = list(range(4, 31)) + [-1] if kind == "2.5" else list(range(4, 16)) + [-1] if kind == "2.0" else []
        return {
            "provider": self.name,
            "model": self.model,
            "family": kind or "unverified",
            "docs_url": DOCS,
            "docs_checked": self.docs_checked,
            "verified": bool(kind),
            "base_url": self.base_url,
            "modes": ["text", "first_last_frame", "reference"],
            "resolutions": ["480p", "720p", "1080p"] if kind == "2.5" else ["480p", "720p", "1080p", "4k"] if kind == "2.0" else [],
            "durations": durations,
            "ratios": list(RATIOS),
            "audio": True,
            "audio_alone": kind == "2.5",
            "mutually_exclusive": ["first_last_frame", "reference"],
            "parameters": ["resolution", "ratio", "duration", "generate_audio", "watermark", "seed", "return_last_frame", "callback_url"],
            "notes": [
                "Model IDs include a date. Copy the current ID from your Ark or BytePlus console into config.",
                "2.0-series reference audio must be accompanied by an image or a video.",
                "2.5 may use reference audio alone.",
                "first_frame / last_frame cannot be combined with reference_image, reference_video, or reference_audio.",
                "BytePlus documents video_url retention of 24 hours. Download as soon as the task succeeds.",
                "Pass media as URLs the vendor can fetch. This adapter does not upload files.",
            ],
        }

    def _check(self, request: VideoRequest):
        if request.model and request.model != self.model:
            raise ProviderError("Request model does not match the configured Seedance model")
        if not request.prompt and not request.references:
            raise ProviderError("Seedance needs a prompt or at least one reference")
        kind = family(self.model)
        if not kind and not request.extra.get("allow_unverified"):
            raise ProviderError(
                "Model name does not match a Seedance 2.0 or 2.5 id. Check the current docs, "
                "then set the model in config. Pass extra allow_unverified only after that check."
            )
        if request.ratio and request.ratio not in RATIOS:
            raise ProviderError("Unsupported ratio")
        if kind and request.duration is not None:
            allowed = range(4, 31) if kind == "2.5" else range(4, 16)
            if int(request.duration) != -1 and int(request.duration) not in allowed:
                raise ProviderError(f"Duration {request.duration} is outside the documented range for Seedance {kind}")
        roles = []
        for ref in request.references:
            if ref.kind not in KIND_TYPE:
                raise ProviderError("Reference kind must be image, video, or audio")
            if ref.role not in FRAME_ROLES and ref.role not in REFERENCE_ROLES:
                raise ProviderError("Unsupported reference role: " + ref.role)
            if not ref.url.startswith(("https://", "http://")):
                raise ProviderError("Each Seedance reference needs an http(s) URL")
            roles.append(ref.role)
        frame = [role for role in roles if role in FRAME_ROLES]
        referred = [role for role in roles if role in REFERENCE_ROLES]
        if frame and referred:
            raise ProviderError("Seedance first/last frame and reference inputs cannot be mixed")
        if roles.count("first_frame") > 1 or roles.count("last_frame") > 1:
            raise ProviderError("Seedance allows at most one first frame and one last frame")
        if "last_frame" in roles and "first_frame" not in roles:
            raise ProviderError("Seedance last_frame is paired with first_frame")
        audio_only = roles and set(roles) <= {"reference_audio"}
        if audio_only and kind == "2.0":
            raise ProviderError("Seedance 2.0 reference audio must be sent with an image or a video")

    def _content(self, request: VideoRequest):
        content = []
        if request.prompt:
            content.append({"type": "text", "text": request.prompt})
        for ref in request.references:
            field = KIND_TYPE[ref.kind]
            content.append({"type": field, field: {"url": ref.url}, "role": ref.role})
        return content

    def submit(self, request: VideoRequest) -> str:
        request = request if isinstance(request, VideoRequest) else VideoRequest(**request)
        self._check(request)
        payload = {"model": self.model, "content": self._content(request)}
        if request.resolution:
            payload["resolution"] = request.resolution
        if request.ratio:
            payload["ratio"] = request.ratio
        if request.duration is not None:
            payload["duration"] = int(request.duration)
        if request.generate_audio is not None:
            payload["generate_audio"] = bool(request.generate_audio)
        if request.seed is not None:
            payload["seed"] = int(request.seed)
        if request.callback_url:
            payload["callback_url"] = request.callback_url
        for key in ("watermark", "return_last_frame"):
            if key in request.extra:
                payload[key] = request.extra[key]
        parsed = http_json(
            self.transport, "POST", self.base_url + "/contents/generations/tasks",
            self._headers(), payload, secret=self.api_key,
        )
        task_id = parsed.get("id") or parsed.get("task_id")
        if not isinstance(task_id, str) or not task_id:
            raise ProviderError("Seedance create response did not include id")
        return task_id

    def status(self, task_id: str) -> TaskStatus:
        if not str(task_id).strip():
            raise ProviderError("task_id is required")
        parsed = http_json(
            self.transport, "GET",
            self.base_url + "/contents/generations/tasks/" + str(task_id),
            {"Authorization": "Bearer " + self.api_key},
            secret=self.api_key,
        )
        raw = str(parsed.get("status") or "")
        content = parsed.get("content") if isinstance(parsed.get("content"), dict) else {}
        error = parsed.get("error")
        message = ""
        if isinstance(error, dict):
            message = str(error.get("message") or error.get("code") or "")
        elif error:
            message = str(error)
        if raw.lower() == "expired" and not message:
            message = "expired"
        return TaskStatus(str(task_id), canonical_state(raw), str(content.get("video_url") or ""), message, raw)

    def download(self, url: str, dest) -> dict:
        if not str(url).startswith(("https://", "http://")):
            raise ProviderError("Download URL must be http(s)")
        return download_bytes(self.transport, url, dest)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Call the official Seedance video API with your own key.")
    parser.add_argument("--model", default=os.environ.get("ARK_MODEL", ""))
    parser.add_argument("--base-url", default=os.environ.get("ARK_API_BASE", ""))
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("capabilities")
    submit = sub.add_parser("submit")
    submit.add_argument("request", type=Path)
    query = sub.add_parser("status")
    query.add_argument("task_id")
    fetch = sub.add_parser("download")
    fetch.add_argument("url")
    fetch.add_argument("dest", type=Path)
    args = parser.parse_args(argv)
    if args.command == "capabilities" and not args.model:
        print(json.dumps({
            "docs_url": DOCS,
            "docs_checked": "2026-11-03",
            "volcengine_base": DEFAULT_BASE,
            "byteplus_base": BYTEPLUS_BASE,
            "note": "Set ARK_MODEL and ARK_API_BASE from your own console. Model ids are dated.",
        }, indent=2))
        return 0
    client = SeedanceVideo(args.model, base_url=args.base_url or None)
    if args.command == "capabilities":
        print(json.dumps(client.capabilities(), indent=2))
    elif args.command == "submit":
        payload = json.loads(args.request.read_text())
        payload.setdefault("model", client.model)
        print(json.dumps({"task_id": client.submit(VideoRequest(**payload))}, indent=2))
    elif args.command == "status":
        print(json.dumps(client.status(args.task_id).as_dict(), indent=2))
    else:
        print(json.dumps(client.download(args.url, args.dest), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
