# Changelog

## Unreleased

- README showcase: six unofficial concept ads for three real brands, a performance ad and a creator ad or brand film for each, with per-brand production notes in `examples/showcase/`.

## 0.0.1

First release of MixReel, for ad, e-commerce, and product short videos.

- Seven agent skills: the router, analyze, script, video plan, keyframes, produce, and review. Each stage can be invoked alone, and the router keeps them in order.
- One project folder per brand. `brand/` holds the brand context, standing requirements, audience taste, competitors, a taste library, source assets, and `films.md`, a ledger of every film idea with its state, the user's words, and a rework log. `init_project.py` creates it under `--root`, `$MIXREEL_PROJECTS_DIR`, or `mixreel-projects/`, and never overwrites a file.
- A new user can go from an empty folder to brand files and a first script with two plain requests. Skill commands are written against the installed folder, a missing reference skips analysis, and a requested script arrives whole.
- Reference analysis with time-labelled evidence, a cut list, and a rule that every extracted frame is looked at before the step counts as done.
- Scripts built from what the audience longs for and a proven moment they already know, with the theme written first, one beat per shot, each cause followed by the reaction it lands on, a dialogue checklist, an early feasibility and sound check, a review by a fresh agent that only sees the shot table, and a reference sheet of real images.
- A 3D previs for every scene told in more than one shot in one place, rendered with Blender or a pure Python raster fallback, with example scenes for a counter handoff and a product orbit.
- Video planning that groups shots into as few requests as the provider allows, plans continuations with `continues_from`, and asks for only the keyframes the groups need.
- MiniMax H3 and Seedance 2 notes with official limits and prices as of their check dates, links to the vendors' prompt guides, and the way MixReel writes each prompt: a six-section H3 prompt built from a coverage plan, and a single-setup Seedance direction.
- Image model notes for Midjourney, Ideogram, and GPT Image, with where to start for each kind of step and official request parameters. They are recommendations. The model stays the user's choice.
- Edit renderer with plan versions 1 to 3, local app recordings through `app_recording.py`, overlays, per-shot sound, and frame holds.
- Cut QA for flashes, flicker, cut offset, missed and off-beat cuts, stray frames, silence, loudness, and size, plus frame packs and keyframe diffs.
- Optional CLIP, DINOv2, InsightFace `buffalo_s`, and SyncNet checks. SyncNet runs per shot and reports an offset only at confidence 3 or above. `MIXREEL_PYTHON` picks the interpreter, and `MIXREEL_FACE_PACK` another face pack. Weights are not downloaded unless you ask.
- Optional Gemini review that returns hints and does not decide the cut.
- A budget journal that reserves before a paid call, stores the task id first, and reconciles billing apart from the download.
- Provider interface plus official MiniMax and Seedance examples. No hosted relay.
- Local quickstart that needs no API key.
