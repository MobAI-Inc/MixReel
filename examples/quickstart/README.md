# Quickstart

No API key. This is the path that should work on a fresh clone.

```sh
python3 -m pip install -r requirements.txt
python3 scripts/demo.py
```

You need `ffmpeg` and `ffprobe`. The script prints a temporary directory. Open `previs/plan.png` and `master.mp4` there. `qa.json` is the report for the synthetic edit. The self-check section must show the flash and late-cut detectors firing on the checker's own clip.

<!-- TODO(demo): optional 15-second capture of this command's previs and QA,
     saved as docs/demos/quickstart.mp4, once someone records it.
     The command itself is the demo. A missing video does not block the path. -->

Delete the temporary directory when you are finished. It is not part of the repository.
