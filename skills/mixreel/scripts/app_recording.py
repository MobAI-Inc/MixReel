#!/usr/bin/env python3
"""Wrap a silent app recording into a local edit plan.

The recording is an existing asset. It is not sent to an image or video model.
Pass a caption file later as an overlay in the plan this script writes.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent


def probe_duration(video):
    run = subprocess.run(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=noprint_wrappers=1:nokey=1", str(video)],
        capture_output=True, text=True, check=False,
    )
    if run.returncode != 0:
        raise RuntimeError(run.stderr.strip() or "ffprobe failed")
    return float(run.stdout.strip())


def build_plan(video, duration, width=1080, height=1920, fps=30):
    duration = round(float(duration), 3)
    name = Path(video).name
    return {
        "version": 3,
        "duration": duration,
        "fps": fps,
        "illustration_count": 0,
        "music": {"source": "none", "events": []},
        "references": [],
        "reviews": {"storyboard": "pending", "style": "pending", "keyframes": "pending"},
        "generation_groups": [],
        "overlays": [],
        "sound": {"ducking": [], "layers": []},
        "shots": [{
            "id": "screen-1",
            "start": 0.0,
            "end": duration,
            "production": "local",
            "function": "Show the real product interface.",
            "source_evidence": "User-supplied screen recording. Not a generated picture.",
            "keyframe_design": "No generated keyframe. The recording is the picture.",
            "description": f"Play {name} full frame. Add captions and a logo in the edit, not in a model.",
            "opening": "First frame of the recording.",
            "ending": "Last frame of the recording.",
            "camera": {"behavior": "fixed", "start": "Screen recording", "end": "Screen recording"},
            "bindings": [],
            "keyframes": [],
            "transition": {"type": "cut", "duration": 0},
            "clip": {"asset": name, "in": 0, "duration": duration, "speed": 1},
            "audio": {"from": "none"},
        }],
        "delivery": {"width": width, "height": height},
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--duration", type=float)
    parser.add_argument("--fps", type=float, default=30)
    parser.add_argument("--size", default="1080x1920")
    args = parser.parse_args(argv)
    if not args.video.is_file() and args.duration is None:
        parser.error("video must exist, or pass --duration for a plan that will be filled later")
    duration = args.duration if args.duration is not None else probe_duration(args.video)
    width, height = (int(part) for part in args.size.lower().split("x"))
    plan = build_plan(args.video, duration, width, height, args.fps)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(plan, indent=2) + "\n")
    spec_path = HERE / "validate_plan.py"
    run = subprocess.run([sys.executable, str(spec_path), str(args.out)], capture_output=True, text=True)
    if run.returncode != 0:
        parser.exit(1, run.stdout + run.stderr)
    print(run.stdout.strip())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
