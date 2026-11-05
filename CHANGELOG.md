# Changelog

## Unreleased

- One project folder per brand. `brand/` keeps the brand context, standing requirements, source assets and `films.md`, a record of every film. Every stage finds the project first and follows its requirements. Scripts avoid events already listed.
- `init_project.py` creates the brand folder on first use. The location is `--root`, else `$MIXREEL_PROJECTS_DIR`, else `mixreel-projects/` under the working directory. It never overwrites a file.

## 0.1.0

First public edition for ad and product short videos.

- Seven agent skills: analyze, script, video plan, keyframes, produce, review, and the router.
- Local previs with a Blender backend and a pure Python raster fallback.
- Edit renderer, media inspection, cut QA, frame packs, keyframe diffs, and a budget journal.
- Optional CLIP, DINOv2, InsightFace `buffalo_s`, and SyncNet checks. Weights are not downloaded unless you ask.
- Optional Gemini review that returns hints and does not decide the cut.
- Provider interface plus official MiniMax and Seedance examples. No hosted relay.
- Local quickstart that needs no API key.
