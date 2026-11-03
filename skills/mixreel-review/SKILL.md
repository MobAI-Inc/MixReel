---
name: mixreel-review
description: Review a script, keyframe, generated clip, or finished ad against the approved brief. Name the narrowest repair and recheck it. Does not generate footage.
---

# Review

Pipeline stage 7. The map is [pipeline](../mixreel/references/pipeline.md). Judge the artifact. Name the narrowest repair. Recheck it. Do not keep a second generation workflow here.

## Output

`review.md`: findings, the repair destination, what to recheck, and a status of pass, fail, or not checked for each item. An agent review is not user acceptance.

## Must follow

- Watch and listen when you can. A sampled review says sampled. A silent review says silent.
- Follow [frame reading](../mixreel/references/frame-reading.md). Every inspection image gets looked at. If one is skipped, the review is incomplete.
- Run the suspect script, then the frame pack, then decide. Suspects are not the verdict. Pixel problems use the frames. Action, line, and gaze problems use the real-time playback. If those disagree, write "uncertain".
- [Brand marks](../mixreel/references/brand-fidelity.md) match the asset.
- Audience-facing captions do not contain production notes. Required disclosures stay.
- Review generated footage inside the cut the user will receive. Play returned files from the start through internal cuts.
- Route the repair to the earliest stage that owns the cause. A single bad shot is regenerated as that shot. Keep the original sound and the edit grid.
- Follow [diagnosis](references/diagnosis.md). Do not feed a model's last output back in as the base for the same model. A repair that does not change pixels stays failed. After a repair, look for regressions, including regions that should have stayed still.
- Do not change provider, add a paid attempt, or rewrite the script just to close a review comment.
- CLIP, DINOv2, face match, and SyncNet run only when [review tools](references/review-tools.md) says the environment has them and the task needs them. Gemini, if the user asked, returns hints and does not decide.

## Read next

| When | Open |
| --- | --- |
| The checklist | [Review criteria](references/review.md) |
| How wide the repair is | [Diagnosis](references/diagnosis.md) |
| The artifact is footage | [Video inspection](references/video-review.md) |
| You are about to run a script | [Review tools](references/review-tools.md) |
| The artifact is the script | [Ad checks](../mixreel-script/references/ad-script.md) |
