# QA

`qa_check.py` reads a finished file and an optional plan. It shells out to `ffmpeg`. It does not call a model unless you pass `--models`.

```sh
python3 skills/mixreel/scripts/qa_check.py master.mp4 \
  --plan plan.json --size 1080x1920 --lufs -14 --beats beats.json
python3 skills/mixreel/scripts/qa_check.py --self-check
```

Exit 0 means this pass found nothing. Exit 1 means the JSON on stdout lists issues. Exit 2 means the checker itself failed.

`--self-check` builds a synthetic clip and requires the detectors to catch a black flash, a white flash, flicker, a cut that lands at 4.292s against a plan of 4.000s, and that same cut being off the beat. An on-beat cut in the same clip must stay quiet.

## What is measured

Flash and black frames compare a frame's luma with a local median. Flicker is luma that reverses direction across a run of frames. Cut offset compares a detected picture change with the plan. A missed cut is a planned cut with no picture change. Off-beat uses beat times from `beat_grid.py` and a tolerance, default 0.06 seconds. Stray frames are a short run whose picture still belongs to the previous shot. Silence, integrated loudness, and peak come from the audio stream. `--size` checks the frame.

False alarms are listed in the README table. A detector hit is not a verdict. `frame_pack.py` builds the stills. The review skill says every one of those stills gets looked at.

```sh
python3 skills/mixreel/scripts/frame_pack.py master.mp4 pack/ \
  --plan plan.json --suspects qa.json
```

The manifest order is overview, seam, burst, curve, brand frame. `review_tiles` is a reading-weight hint, not a bill.

Optional CLIP, DINOv2, `buffalo_s`, and SyncNet flags are in [model weights](model-weights.md). Leave them off until you need them.
