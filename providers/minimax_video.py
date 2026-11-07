"""Official MiniMax video generation adapter.

Checked against the public international docs on 2026-11-03:

- Create: POST https://api.minimax.io/v2/video_generation
- Query:  GET  https://api.minimax.io/v2/query/video_generation/{task_id}
- Auth:   Authorization: Bearer $MINIMAX_API_KEY
- Docs:   https://platform.minimax.io/docs/api-reference/video-generation-v2-create
          https://platform.minimax.io/docs/api-reference/video-generation-v2-query

The China documentation examples use the host api.minimax.cn. Set
MINIMAX_API_BASE if your key belongs to that host. This file does not add a
relay, and it does not invent a prompt template. Put the model name in your
own config. The names below are the public names from that docs page, used
only to check duration and resolution before a paid call.

A successful query returns the file at task.content.url. Download it yourself;
this adapter does not keep the file.
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

DOCS = "https://platform.minimax.io/docs/api-reference/video-generation-v2-create"
DEFAULT_BASE = "https://api.minimax.io"

# Public model envelopes from the create-task reference on 2026-11-03.
MODELS = {
    "MiniMax-H3": {"resolutions": ("768P", "2K"), "durations": range(4, 16)},
    "MiniMax-H3-Highspeed": {"resolutions": ("480P", "768P"), "durations": range(4, 16)},
    "MiniMax-H3-Lite": {"resolutions": ("480P", "768P"), "durations": range(4, 16), "no_adaptive": True},
    "MiniMax-H3-Max": {"resolutions": ("480P", "768P"), "durations": range(5, 16)},
}
RATIOS = ("21:9", "16:9", "4:3", "1:1", "3:4", "9:16", "adaptive")
FRAME_ROLES = {"first_frame", "last_frame"}
REFERENCE_ROLES = {"reference_image", "reference_video", "reference_audio"}
KIND_TYPE = {"image": "image_url", "video": "video_url", "audio": "audio_url"}


class MiniMaxVideo(VideoProvider):
    name = "minimax"
    docs_checked = "2026-11-03"

    def __init__(self, model, api_key=None, base_url=None, transport=None):
        self.model = (model or "").strip()
        self.api_key = require_key(api_key if api_key is not None else os.environ.get("MINIMAX_API_KEY"), "MINIMAX_API_KEY")
        self.base_url = (base_url or os.environ.get("MINIMAX_API_BASE") or DEFAULT_BASE).rstrip("/")
        self.transport = transport or default_transport

    def _headers(self):
        return {"Authorization": "Bearer " + self.api_key, "Content-Type": "application/json"}

    def capabilities(self) -> dict:
        known = MODELS.get(self.model)
        return {
            "provider": self.name,
            "model": self.model,
            "docs_url": DOCS,
            "docs_checked": self.docs_checked,
            "verified": known is not None,
            "modes": ["text", "first_last_frame", "reference"],
            "resolutions": list(known["resolutions"]) if known else [],
            "durations": list(known["durations"]) if known else [],
            "ratios": list(RATIOS),
            "audio": True,
            "mutually_exclusive": ["first_last_frame", "reference"],
            "limits": {
                "reference_image": 9,
                "reference_video": 3,
                "reference_audio": 3,
                "reference_video_seconds_total": 15,
                "reference_audio_seconds_total": 15,
                "prompt_characters": 7000,
            },
            "notes": [
                "Text-only requests must set a concrete ratio. adaptive is refused.",
                "first_frame and last_frame cannot be combined with reference_image, reference_video, or reference_audio.",
                "MiniMax-H3-Lite, as documented on the check date, does not accept adaptive in reference mode.",
                "Pass reference media as URLs the vendor can fetch. This adapter does not upload files.",
            ],
        }

    def _check(self, request: VideoRequest):
        if request.model and request.model != self.model:
            raise ProviderError("Request model does not match the configured MiniMax model")
        if not request.prompt:
            raise ProviderError("MiniMax requires one non-empty text prompt")
        if len(request.prompt) > 7000:
            raise ProviderError("MiniMax prompt length exceeds the documented 7000-character limit")
        known = MODELS.get(self.model)
        allow = bool(request.extra.get("allow_unverified"))
        if known is None and not allow:
            raise ProviderError(
                "Model is not in the documented MiniMax set checked on "
                f"{self.docs_checked}. Pass extra allow_unverified only after you check the current docs."
            )
        if known is not None:
            if request.resolution not in known["resolutions"]:
                raise ProviderError(f"Resolution {request.resolution!r} is not documented for {self.model}")
            if int(request.duration) not in known["durations"]:
                raise ProviderError(f"Duration {request.duration} is not documented for {self.model}")
        roles = [ref.role for ref in request.references]
        kinds = [ref.kind for ref in request.references]
        if any(kind not in KIND_TYPE for kind in kinds):
            raise ProviderError("Reference kind must be image, video, or audio")
        if any(not ref.url.startswith(("https://", "http://")) for ref in request.references):
            raise ProviderError("Each MiniMax reference needs an http(s) URL")
        frame = [role for role in roles if role in FRAME_ROLES]
        referred = [role for role in roles if role in REFERENCE_ROLES]
        unknown = [role for role in roles if role not in FRAME_ROLES and role not in REFERENCE_ROLES]
        if unknown:
            raise ProviderError("Unsupported reference role: " + ", ".join(unknown))
        if frame and referred:
            raise ProviderError("MiniMax first/last frame and reference inputs cannot be mixed")
        if roles.count("first_frame") > 1 or roles.count("last_frame") > 1:
            raise ProviderError("MiniMax allows at most one first frame and one last frame")
        if roles.count("reference_image") > 9 or roles.count("reference_video") > 3 or roles.count("reference_audio") > 3:
            raise ProviderError("MiniMax reference caps are 9 images, 3 videos, and 3 audio clips")
        if request.ratio not in RATIOS:
            raise ProviderError("Unsupported ratio")
        if not roles and request.ratio == "adaptive":
            raise ProviderError("Text-to-video requires a concrete ratio, not adaptive")
        if known and known.get("no_adaptive") and referred and request.ratio == "adaptive":
            raise ProviderError("This MiniMax model does not document adaptive ratio for reference mode")

    def _content(self, request: VideoRequest):
        content = [{"type": "text", "text": request.prompt}]
        for ref in request.references:
            field = KIND_TYPE[ref.kind]
            content.append({"type": field, field: {"url": ref.url}, "role": ref.role})
        return content

    def submit(self, request: VideoRequest) -> str:
        request = request if isinstance(request, VideoRequest) else VideoRequest(**request)
        self._check(request)
        payload = {
            "model": self.model,
            "content": self._content(request),
            "resolution": request.resolution,
            "duration": int(request.duration),
            "ratio": request.ratio,
        }
        if request.callback_url:
            payload["callback_url"] = request.callback_url
        if request.extra.get("prompt_expansion_mode"):
            payload["extra"] = {"prompt_expansion_mode": request.extra["prompt_expansion_mode"]}
        parsed = http_json(
            self.transport, "POST", self.base_url + "/v2/video_generation",
            self._headers(), payload, secret=self.api_key,
        )
        task_id = parsed.get("task_id")
        if not isinstance(task_id, str) or not task_id:
            raise ProviderError("MiniMax create response did not include task_id")
        return task_id

    def status(self, task_id: str) -> TaskStatus:
        if not str(task_id).strip():
            raise ProviderError("task_id is required")
        parsed = http_json(
            self.transport, "GET",
            self.base_url + "/v2/query/video_generation/" + str(task_id),
            {"Authorization": "Bearer " + self.api_key},
            secret=self.api_key,
        )
        task = parsed.get("task") if isinstance(parsed.get("task"), dict) else parsed
        raw = str(task.get("status") or "")
        content = task.get("content") if isinstance(task.get("content"), dict) else {}
        error = task.get("error")
        message = ""
        if isinstance(error, dict):
            message = str(error.get("message") or error.get("code") or "")
        elif error:
            message = str(error)
        return TaskStatus(str(task_id), canonical_state(raw), str(content.get("url") or ""), message, raw)

    def download(self, url: str, dest) -> dict:
        if not str(url).startswith(("https://", "http://")):
            raise ProviderError("Download URL must be http(s)")
        return download_bytes(self.transport, url, dest)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Call the official MiniMax video API with your own key.")
    parser.add_argument("--model", default=os.environ.get("MINIMAX_MODEL", ""))
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
        print(json.dumps({"models": sorted(MODELS), "docs_url": DOCS, "docs_checked": "2026-11-03"}, indent=2))
        return 0
    client = MiniMaxVideo(args.model or "MiniMax-H3")
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
