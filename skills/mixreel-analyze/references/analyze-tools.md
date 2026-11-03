# Analysis scripts

Run these from the skill that contains them. They do not call a model.

```sh
python3 skills/mixreel/scripts/media_inspect.py reference REFERENCE.mp4 analysis/
python3 skills/mixreel/scripts/media_inspect.py audio MUSIC.wav analysis/audio.json
python3 skills/mixreel/scripts/media_inspect.py motion CLIP.mp4 analysis/motion.json
python3 skills/mixreel/scripts/beat_grid.py MUSIC.wav analysis/beats.json
```

`reference` writes frames, a contact sheet, and cut candidates. Candidates are not an edit decision. `audio` reports silence and onsets. `motion` reports frame-to-frame change and flash suspects. `beat_grid.py` needs `numpy` and `librosa`; if they are missing it says so and does not guess a grid.

Reference media longer than 600 seconds is out of scope for this pass. Say so instead of sampling it silently.
