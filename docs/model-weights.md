# Model weight licenses

A normal MixReel run does not install or download these weights. `qa_check.py` loads one only when `--models` names it. Downloads happen only with `--allow-model-download`, and SyncNet is never downloaded by these scripts.

Install the Python packages only when you want the checks:

```sh
python3 -m pip install -r skills/mixreel/scripts/requirements-review-models.txt
```

| Check | Package | Weight | License note |
| --- | --- | --- | --- |
| `clip` | `open_clip_torch`, `torch` | OpenCLIP ViT-B-32, public LAION checkpoint named in the script | Follow that checkpoint's license. Commercial use is your check, not this repo's grant |
| `dino` | `torch` | DINOv2 ViT-S/14 from the public `facebookresearch/dinov2` hub | Follow the DINOv2 license shipped with that repository |
| `face` | `insightface`, `onnxruntime` | InsightFace **`buffalo_s`** (the small pack) | InsightFace pretrained weights are licensed for non-commercial research. Do not use them on a commercial job unless you have a separate license. The script asks for `buffalo_s` only |
| `syncnet` | none from pip | `syncnet_v2.model` | Research release. A public copy is hosted at `auxiliary/syncnet_v2.model` inside [ByteDance/LatentSync-1.6](https://huggingface.co/ByteDance/LatentSync-1.6). Put the file in a directory and set `MIXREEL_SYNCNET_DIR`. Confirm the weight license covers your job before you run it |

Face and lip-sync stay off for commercial spots unless that separate license exists. CLIP and DINOv2 are the checks that match "did the product drift" without a face model.

`MIXREEL_FACE_PACK` names another InsightFace pack when you have the right to use one. SyncNet runs one shot at a time, with a 300 second timeout per shot, and reports an offset only when its confidence is at least 3. When these packages live in their own virtual environment, set `MIXREEL_PYTHON` to that interpreter. SyncNet is started with it, and the review skill runs the checks with it.

Gemini review is not a weight in this repository. It is an optional API call. Its output is a hint, not a decision. See `providers/gemini_review.py`.

This file is not legal advice. Read the upstream license of each weight before you ship a film that depended on it.
