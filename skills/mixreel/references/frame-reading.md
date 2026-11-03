# How to read frames

If you can watch the video and hear the audio, do that. Stills do not prove motion, a seamless cut, or a sound. Say when a review is sampled or silent. Do not claim you watched a video that was only embedded in a document.

Suspect lists are places to look, not verdicts.

## Required coverage

View every overview and every individual frame the inspection scripts produced. Listing names, reading JSON, or looking only at a contact sheet does not count. You may take notes between images. If any image cannot be viewed, mark the step incomplete and name the gap.

## Reference contact sheets

Use this for `media_inspect.py reference`, including `contact.jpg`.

1. View the overview and contact images.
2. View every frame listed in `analysis.json`.
3. Cross-check `cut_candidates` and `shots`. Those candidates are not confirmed cuts.

Commands are in [analysis scripts](../../mixreel-analyze/references/analyze-tools.md).

## Review packs

`frame_pack.py` writes `manifest.json` in this order: overview, seam, burst, curve, full-resolution brand frames.

1. View every overview.
2. View every remaining image.
3. Cross-check the suspect report and the plan.

Commands are in [review tools](../../mixreel-review/references/review-tools.md).
