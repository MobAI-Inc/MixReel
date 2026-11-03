"""Optional Gemini review. Hints only.

This module reuses the skill script so an installed collection stays
self-contained. A Gemini answer is a hint for the person reviewing the cut.
It is not a pass, a fail, or acceptance, and nothing in the pipeline requires it.

Set GEMINI_API_KEY or GOOGLE_API_KEY. The model name defaults to the public
Gemini video example checked on 2026-11-03 (gemini-3.8-flash) and can be
overridden. Docs: https://ai.google.dev/gemini-api/docs/video-understanding
"""
from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parents[1] / "skills" / "mixreel" / "scripts" / "gemini_review.py"
_spec = importlib.util.spec_from_file_location("mixreel_gemini_review", _SCRIPT)
_module = importlib.util.module_from_spec(_spec)
sys.modules[_spec.name] = _module
_spec.loader.exec_module(_module)

review = _module.review
should_call = _module.should_call
skip_note = _module.skip_note
HINT_NOTE = "Gemini output is a hint. It does not pass, fail, or accept the cut."


def main():
    return _module.main()


if __name__ == "__main__":
    raise SystemExit(main())
