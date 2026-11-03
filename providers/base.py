"""Shared provider interface: capabilities, submit, status, download."""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional
import urllib.error
import urllib.request


class ProviderError(RuntimeError):
    """A request was refused locally or the vendor returned an error."""


@dataclass
class MediaRef:
    """One image, video, or audio input. Pass a public URL the vendor can fetch."""

    kind: str
    role: str
    url: str = ""

    def __post_init__(self):
        self.kind = self.kind.strip().lower()
        self.role = self.role.strip().lower()
        self.url = self.url.strip()


@dataclass
class VideoRequest:
    prompt: str
    model: str
    duration: int
    resolution: str
    ratio: str
    references: list = field(default_factory=list)
    seed: Optional[int] = None
    generate_audio: Optional[bool] = None
    callback_url: str = ""
    extra: dict = field(default_factory=dict)

    def __post_init__(self):
        self.prompt = (self.prompt or "").strip()
        self.model = (self.model or "").strip()
        self.resolution = (self.resolution or "").strip()
        self.ratio = (self.ratio or "").strip()
        refs = []
        for item in self.references:
            refs.append(item if isinstance(item, MediaRef) else MediaRef(**item))
        self.references = refs


@dataclass
class TaskStatus:
    task_id: str
    state: str
    video_url: str = ""
    error: str = ""
    raw_state: str = ""

    def as_dict(self):
        return {
            "task_id": self.task_id,
            "state": self.state,
            "video_url": self.video_url,
            "error": self.error,
            "raw_state": self.raw_state,
        }


# transport(method, url, headers, body_bytes_or_none, timeout) -> (status, header_map, body_bytes)
Transport = Callable[[str, str, dict, Optional[bytes], int], tuple]


def default_transport(method, url, headers, body, timeout):
    request = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return response.status, dict(response.headers.items()), response.read()
    except urllib.error.HTTPError as exc:
        return exc.code, dict(exc.headers.items()), exc.read()


def _redact(text, secret):
    if secret and secret in text:
        return text.replace(secret, "***")
    return text


def http_json(transport, method, url, headers, payload=None, timeout=120, secret=""):
    body = None if payload is None else json.dumps(payload).encode()
    status, _header_map, raw = transport(method, url, headers, body, timeout)
    text = raw.decode("utf-8", errors="replace") if raw else ""
    try:
        parsed = json.loads(text) if text else {}
    except ValueError as exc:
        raise ProviderError(f"Vendor returned HTTP {status} with a non-JSON body") from exc
    if status >= 400:
        message = text[:500]
        if isinstance(parsed, dict):
            error = parsed.get("error")
            if isinstance(error, dict) and error.get("message"):
                message = str(error.get("message"))
            elif parsed.get("message"):
                message = str(parsed.get("message"))
        raise ProviderError(f"Vendor HTTP {status}: {_redact(message, secret)}")
    if not isinstance(parsed, dict):
        raise ProviderError("Vendor JSON was not an object")
    return parsed


def download_bytes(transport, url, dest, timeout=300):
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    status, _headers, raw = transport("GET", url, {}, None, timeout)
    if status >= 400 or not raw:
        raise ProviderError(f"Download failed with HTTP {status}")
    dest.write_bytes(raw)
    digest = hashlib.sha256(raw).hexdigest()
    return {"path": str(dest), "sha256": digest, "bytes": len(raw)}


def require_key(value, env_name):
    value = (value or "").strip()
    if not value:
        raise ProviderError(f"Set {env_name} to your own API key. MixReel does not supply one.")
    return value


def canonical_state(raw):
    raw = (raw or "").strip().lower()
    if raw in ("queued", "pending", "submitted"):
        return "queued"
    if raw in ("running", "processing"):
        return "running"
    if raw in ("succeeded", "success", "completed"):
        return "succeeded"
    if raw in ("cancelled", "canceled"):
        return "cancelled"
    if raw in ("failed", "error", "expired"):
        return "failed"
    return "running" if raw else "queued"


class VideoProvider:
    """capabilities / submit / status / download. Subclasses talk to one official API."""

    name = "base"
    docs_checked = "2026-11-03"

    def capabilities(self) -> dict:
        raise NotImplementedError

    def submit(self, request: VideoRequest) -> str:
        raise NotImplementedError

    def status(self, task_id: str) -> TaskStatus:
        raise NotImplementedError

    def download(self, url: str, dest) -> dict:
        raise NotImplementedError

    def describe(self) -> dict:
        info = self.capabilities()
        info["provider"] = self.name
        info["docs_checked"] = self.docs_checked
        return info
