# How to read frames

Read this when you are looking at stills. If you can watch the video and hear the audio, do that. Stills do not prove motion, a seamless cut, or a sound. Say when a review is sampled or silent. Do not claim you watched a video that was only embedded in a document.

Suspect lists are places to look, not verdicts. There is no OCR step.

## Required coverage

Actually view every overview image and every individual frame the inspection scripts produced. Making the files, listing their names, reading JSON, or looking only at a contact sheet does not count as viewing the individual images. Do not pick only the interesting frames.

Starting with the overview helps you get oriented. You may view one image at a time, write notes between images, or read them in batches. No single uninterrupted pass is required. Whatever the order, view every image before you call the step complete.

Use the JSON frame list or the pack manifest to account for every image. If any image cannot be viewed clearly, or a tool or context limit prevents full coverage, mark the analysis or review incomplete, name the missing coverage, and do not call that step finished. A partial report is not permission to skip these requirements.

## Reference contact sheets

Use this for `media_inspect.py reference`, including `contact.jpg`.

1. View all overview and contact images, including `contact.jpg`. Starting here is recommended.
2. View every individual frame listed in `analysis.json` (`frames`). You may note what you see as you go.
3. Cross-check the images against `cut_candidates` and `shots` in `analysis.json`. Those candidates are evidence to inspect, not confirmed cuts. Make sure every image was viewed before you complete the analysis.

Commands are in [analysis scripts](../../mixreel-analyze/references/analyze-tools.md). Open that file when you are about to run one.

## Review packs

`frame_pack.py` writes `manifest.json` in this order: overview, seam, burst, curve, full-resolution brand frames.

1. View every overview image. Starting here is recommended.
2. View every remaining image in the pack. The manifest order is a useful guide, and notes between images are fine.
3. Cross-check the images against the suspect report's detected and planned cut lists, and the plan when you have it. Make sure every image was viewed before you complete the review.

Commands and flags are in [review tools](../../mixreel-review/references/review-tools.md). Open that file when you are about to run a script.
