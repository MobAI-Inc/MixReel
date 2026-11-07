# Review tools

Read this when you are about to run a check. What to judge is in [video inspection](video-review.md) for footage and [review criteria](review.md) for any artifact. How to read the stills is in [frame reading](../../mixreel/references/frame-reading.md).

`<mixreel>` below is the installed `mixreel` skill folder, next to this skill's own folder. Replace it with the real path. Suspects are places to look, not verdicts. There is no OCR step. Do not add one.

## Interpreter

`<py>` below is the review interpreter. Use `$MIXREEL_PYTHON` when it is set, for example when the review packages live in their own virtual environment. Otherwise use `python3`. SyncNet is started the same way: `MIXREEL_PYTHON` when it is set, otherwise the interpreter that launched the script.

## Flash, flicker, cut offset, on-beat

```sh
<py> <mixreel>/scripts/qa_check.py master.mp4 --plan plan.json --size 1080x1920 [--lufs TARGET] [--beats beats.json]
```

Also: `--threshold 0.3`, `--window 4` (frames on each side of a planned cut), `--beat-tol 0.06` (seconds). The default treats a cut farther than 60 ms from a beat as off-beat. `--beats` is `beat_grid.py` JSON.

With a plan, a cut planned at 8.00s and observed at 8.29s is a cut offset, not a pass. The script also lists white and black flashes (frame luma against a local median), flicker (luma that steps up and down), frames from the neighbouring shot, unplanned picture changes, very short runs, silence, loudness, true peak, and size. Dialogue placement still needs listening.

```sh
<py> <mixreel>/scripts/media_inspect.py suspects master.mp4 suspects.json [--plan plan.json] [--beats beats.json]
```

writes that list on its own. It takes the same `--threshold`, `--beat-tol`, and `--models` flags.

`<py> <mixreel>/scripts/media_inspect.py motion master.mp4 motion.json` locates candidate visual changes and also lists flash and flicker suspects. A frame-difference peak can be a camera move, a flash, or a defect. `--fps` defaults to 12. Inspect the surrounding frames. Prompt timestamps are not observations.

`<py> <mixreel>/scripts/qa_check.py --self-check` builds a short clip and checks that flash, flicker, cut offset, and off-beat are caught. That checks the tool. It is not a review of the film.

## Frame pack

Build a pack on every footage review and every quality gate. With no suspects it still holds the overview, the seams, and the brand frames. Suspects add bursts around their times.

```sh
<py> <mixreel>/scripts/frame_pack.py master.mp4 pack/ --plan plan.json --suspects qa.json [--brand-times 4.5]
```

Optional: `--tile-w 320`, `--burst-fps 12`, `--max-events 8`. `--brand-times` takes seconds for full-resolution brand frames. Requires ffmpeg and Pillow. No model calls. The manifest field `review_tiles` is a size hint for how heavy the stills are to read. It is not a bill.

`manifest.json` order is overview, seam, burst, curve, `brand_fullres`. Labels are red and read `shot #frame time`. Look at every listed image, as [frame reading](../../mixreel/references/frame-reading.md) requires. Start with the overview. Notes between images are fine. Use the detected and planned cut lists alongside the pack. Making the pack, or reading only its overview, does not complete a review. A skipped or unreadable image leaves this step incomplete.

## Keyframe re-review

Use [keyframe diff](../../mixreel-keyframes/references/keyframe-tools.md) to locate changes. Apply its prior-review and requirements checks before carrying forward an unchanged image's pass.

## Optional small models

Off unless the task needs that check (product drift, identity drift, or lip sync) and the packages are installed. They are not imported by a normal QA run. Pass only the names you need, on `qa_check.py` or `media_inspect.py suspects`:

```sh
<py> <mixreel>/scripts/qa_check.py master.mp4 --plan plan.json --models clip,dino,face,syncnet
```

| Flag | Use | Weight note |
| --- | --- | --- |
| `clip` | Frame-to-frame picture drift | OpenCLIP ViT-B-32, public checkpoint. Downloaded only with `--allow-model-download`. |
| `dino` | Product or layout drift | DINOv2 ViT-S/14. Same download rule. |
| `face` | Person match against a reference still | InsightFace `buffalo_s`, about 0.7 to 1.0 s per frame on a 4-core CPU and about 850 MB peak. Set `MIXREEL_FACE_PACK` to use another pack. Research license. Do not use on a commercial job without a separate license. |
| `syncnet` | Lip-sync offset, per shot | Research weights. Set `MIXREEL_SYNCNET_DIR`. Nothing is downloaded for you. |

Pass `--ref-face` with `face` when a reference portrait exists. Without one, the checker compares the clip only with itself, which is a weaker hint.

SyncNet checks lip sync one shot at a time. It reports an offset only when confidence is at least 3, and notes a withheld offset below that. Expect about 12 to 20 seconds of compute per second of footage. Each shot has a 300 second timeout.

Install the packages, when you choose to, from `<mixreel>/scripts/requirements-review-models.txt`. Read the model-weight note in the repository docs before you do. Weights are not downloaded unless you also pass `--allow-model-download`. SyncNet is never downloaded.

If a detector is not available, or a shot times out, skip that check and say it was not checked. That is not a pass. Do not run the set because it might be useful later.

## Gemini hints

```sh
<py> <mixreel>/scripts/gemini_review.py master.mp4 --plan plan.json [--suspects qa.json] [--brand TEXT] [--out requests.json]
```

Call it only when the environment supports it and the user asked. The script runs only when a Gemini key is available (`GEMINI_API_KEY`, `GOOGLE_API_KEY`, or the credentials file) and a review was requested (`--run`, `MIXREEL_GEMINI_REVIEW=1`, or `~/.config/mixreel/review.json` with `"gemini_review": true`). Otherwise it prints a skip note and exits 0. Do not set those yourself. It is not part of `qa_check.py` or `media_inspect.py`. The answer is a hint. It is not a pass, a fail, or acceptance.

Leave `--model`, `--fps`, and `--zoom-fps` at their defaults unless the user asked for that setup. In a clone of the repository, the same entry point also lives at `providers/gemini_review.py`.
