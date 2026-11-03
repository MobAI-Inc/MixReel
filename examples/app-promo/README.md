# App promo

**Brand (invented):** Paperlane, a notes app.

**Intended cut:** a silent screen recording of creating a note, captions and a logo added in the edit, music hits on the cuts. The interface is the recording. It is not redrawn by a model.

<!-- TODO(demo): add recording.mp4 and master.mp4.
     The recording must be of an interface we can show. Strip metadata. -->

Draft a local plan before the file exists:

```sh
python3 skills/mixreel/scripts/app_recording.py recording.mp4 \
  --out /tmp/paperlane-plan.json --duration 8 --size 1080x1920
```

Then validate, and render once `recording.mp4` sits next to the plan. See [produce scripts](../../skills/mixreel-produce/references/produce-tools.md).
