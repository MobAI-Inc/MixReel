# Produce scripts

No script in this list submits a paid job.

```sh
python3 skills/mixreel/scripts/validate_plan.py plan.json
python3 skills/mixreel/scripts/render_edit.py plan.json master.mp4 --size 1080x1920
python3 skills/mixreel/scripts/qa_check.py master.mp4 --plan plan.json --size 1080x1920
python3 skills/mixreel/scripts/qa_check.py --self-check
python3 skills/mixreel/scripts/frame_pack.py master.mp4 pack/ --plan plan.json --suspects qa.json
python3 skills/mixreel/scripts/job_journal.py report journal.json
python3 skills/mixreel/scripts/app_recording.py recording.mp4 --out plan.json
```

`render_edit.py` needs `ffmpeg`. Paths in the plan are relative to the plan file. `clip.duration` is the full source duration, not the piece you used.

`app_recording.py` writes a version-3 plan whose only picture is the recording. Pass `--duration` when you are drafting the plan before the file exists. The recording stays on disk. It is not uploaded by this script.

`qa_check.py --self-check` builds a synthetic clip and checks that flash, flicker, cut offset, and an off-beat cut are reported. Use it when you want to see the checker work without a project.

Optional model flags are documented in [review tools](../../mixreel-review/references/review-tools.md). Leave them off unless that file says to turn them on.
