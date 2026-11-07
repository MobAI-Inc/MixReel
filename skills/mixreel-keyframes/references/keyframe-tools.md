# Keyframe tools

Read this when you are checking that a pass changed the image, or re-reviewing keyframes. Models are chosen in [image models](image-models.md). The fields you must record are in [images](images.md), under what was actually submitted.

`keyframe_diff.py` measures whether a paid edit changed the pixels. `<mixreel>` below is the installed `mixreel` skill folder, next to this skill's own folder. Replace it with the real path. The script needs Pillow. It does not call a provider and uses no network.

```sh
python3 <mixreel>/scripts/keyframe_diff.py BEFORE.png AFTER.png [--manifest inputs.json]
python3 <mixreel>/scripts/keyframe_diff.py --batch frames/
```

Optional: `--out report.json`, `--epsilon 2` (a per-channel change treated as unchanged). A batch folder may hold a `manifest.json` with an `items` list, one subfolder per keyframe with `before.png` and `after.png`, or flat pairs named `name.v1.png` and `name.v2.png`, or `name.prev.png` and `name.png`. The manifest records the model id, the prompt, and the reference files.

The report lists `changed` and `unchanged`. Review the changed frames and any image whose requirements or references changed. Carry forward an unchanged image's pass only if it already passed and its requirements and references are unchanged. A pixel diff cannot approve a failed or unreviewed image. A repair with no effect stays failed. When the manifest includes them, the report keeps `model`, `prompt`, `refs`, and the output hash.

A finished job and a charge do not prove the picture changed. Compare at full size. An output identical or nearly identical to its input means the pass had no effect, even when it was billed. Record it as ineffective, keep the billed amount, and stop that route. Do not resubmit the same request.
