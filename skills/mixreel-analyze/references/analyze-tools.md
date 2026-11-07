# Analysis scripts

Read this when you are about to run a local script for reference analysis. What to write down, and what a beat grid does not prove, is in [what to record](analysis.md). How to look at the stills is in [frame reading](../../mixreel/references/frame-reading.md). These tools do not replace watching or listening.

`<mixreel>` below is the installed `mixreel` skill folder, next to this skill's own folder. Replace it with the real path. These scripts do not call a model.

## Reference stills

```sh
python3 <mixreel>/scripts/media_inspect.py reference REFERENCE.mp4 analysis/
```

Optional: `--interval 0.5` (seconds between stills), `--threshold 0.3` (cut-candidate sensitivity, between 0 and 1).

The output includes `contact.jpg`, every `frame_*.jpg` indexed by `analysis.json.frames`, and the `cut_candidates` and `shots` lists. Candidates are not an edit decision. Look at every produced image, as frame reading requires. Start with the overview. Notes between images are fine. Use the cut list alongside the images. Automated cuts can miss dissolves and slow reveals. Missing any produced image leaves this step incomplete.

Reference media longer than 600 seconds is out of scope for this pass. Say so instead of sampling it silently.

## Audio

```sh
python3 <mixreel>/scripts/media_inspect.py audio MUSIC.wav analysis/audio.json
```

Reports duration, silence, and candidate onsets. Then listen.

## Motion

```sh
python3 <mixreel>/scripts/media_inspect.py motion CLIP.mp4 analysis/motion.json
```

Reports frame-to-frame change and flash suspects.

## Beat grid

Optional. Requires `numpy` and `librosa`. If they are missing the script says so and does not guess a grid.

```sh
python3 <mixreel>/scripts/beat_grid.py MUSIC.wav analysis/beats.json [--bpm HINT]
```

Fits a regular grid and reports kick and hat strength per beat. `--bar` (default 4) only groups that grid. Read the cautions in [what to record](analysis.md) before you treat any of those fields as musical facts.

Flash, flicker, cut offset, and off-beat checks are for a cut you are reviewing, not for this stage. They are in [review tools](../../mixreel-review/references/review-tools.md).
