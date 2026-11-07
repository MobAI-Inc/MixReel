# Produce scripts

Read this when you are rendering or checking a master. Edit decisions stay in [production](production.md). Brand overlays follow [brand fidelity](../../mixreel/references/brand-fidelity.md).

No script in this list submits a paid job. `<mixreel>` below is the installed `mixreel` skill folder, next to this skill's own folder. Replace it with the real path.

## Validate and render

```sh
python3 <mixreel>/scripts/validate_plan.py plan.json
python3 <mixreel>/scripts/render_edit.py plan.json master.mp4 --size 1080x1920 [--preview preview.mp4] [--holds 12]
```

Render once every shot has `clip {asset, in, duration, speed}`. `render_edit.py` needs `ffmpeg`. Paths in the plan are relative to the plan file. `clip.duration` is the full source duration, not the piece you used.

Version 1 and 2 plans lay the music track only and discard the clips' own audio. Version 3 also keeps each shot's sound, overlays edit-layer images, and adds sound layers. The helper adds a 0.3-second fade-out on a music track, a limiter on the mix, and sharpening on clips narrower than the output width. Review those treatments before delivery. Another editor is fine when you need different finishing. This helper cannot write captions or design UI by itself.

## App recording

```sh
python3 <mixreel>/scripts/app_recording.py recording.mp4 --out plan.json
```

`app_recording.py` writes a version-3 plan whose only picture is the recording. Pass `--duration` when you are drafting the plan before the file exists. The recording stays on disk. It is not uploaded by this script.

## Listen

`python3 <mixreel>/scripts/media_inspect.py audio master.mp4 audio.json` reports duration, silence, and candidate onsets. Then listen. Intended silence is not an automatic defect.

## Quality gate

```sh
python3 <mixreel>/scripts/qa_check.py master.mp4 --plan plan.json --size 1080x1920
python3 <mixreel>/scripts/frame_pack.py master.mp4 pack/ --plan plan.json --suspects qa.json
```

The full flags, the interpreter, and the optional small models are in [review tools](../../mixreel-review/references/review-tools.md). Leave the model flags off unless that file says to turn them on. Read the pack in that file's frame-pack order. Dialogue placement still needs listening.

`qa_check.py --self-check` builds a synthetic clip and checks that flash, flicker, cut offset, and an off-beat cut are reported. Use it when you want to see the checker work without a project.

## Journal

`python3 <mixreel>/scripts/job_journal.py report journal.json` summarizes reservations, task ids, and billed amounts. The rest of the journal commands are in [execution](../../mixreel/references/execution.md).
