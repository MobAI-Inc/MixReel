# Review tools

`<mixreel>` below is the installed `mixreel` skill folder, next to this skill's own folder. Replace it with the real path.

## Always local

```sh
python3 <mixreel>/scripts/qa_check.py master.mp4 --plan plan.json --size 1080x1920
python3 <mixreel>/scripts/qa_check.py --self-check
python3 <mixreel>/scripts/frame_pack.py master.mp4 pack/ --plan plan.json --suspects qa.json
python3 <mixreel>/scripts/media_inspect.py motion master.mp4 motion.json
```

`frame_pack.py` needs `Pillow`. Its manifest field `review_tiles` is a size hint for how heavy the stills are to read. It is not a bill.

## Optional small models

Off unless the task needs them and the packages are installed. They are not imported by a normal QA run.

```sh
python3 <mixreel>/scripts/qa_check.py master.mp4 --plan plan.json --models clip,dino
```

| Flag | Use | Weight note |
| --- | --- | --- |
| `clip` | Frame-to-frame picture drift | OpenCLIP ViT-B-32, public checkpoint. Downloaded only with `--allow-model-download`. |
| `dino` | Product or layout drift | DINOv2 ViT-S/14. Same download rule. |
| `face` | Person match against a reference still | InsightFace `buffalo_s`. Research license. Do not use on a commercial job without a separate license. |
| `syncnet` | Lip-sync offset | Research weights. Set `MIXREEL_SYNCNET_DIR`. Nothing is downloaded for you. |

Install the packages, when you choose to, from `<mixreel>/scripts/requirements-review-models.txt`. Read the model-weight note in the repository docs before you do.

Pass `--ref-face` with `face`. Without a reference, the checker compares the clip only with itself, which is a weaker hint.

## Gemini hints

`<mixreel>/scripts/gemini_review.py` runs only when a key is present and the user asked (`--run` or `MIXREEL_GEMINI_REVIEW=1`). The answer is a hint. It is not a pass, a fail, or acceptance. In a clone of the repository, the same entry point also lives at `providers/gemini_review.py`.
