---
name: mixreel-review
description: Review a script, keyframe, generated clip, or finished ad against the approved brief. Name the narrowest repair and recheck it. Works on existing artifacts and does not generate footage.
---

# Review

Pipeline stage 7. The map is [pipeline](../mixreel/references/pipeline.md). Judge the artifact. Name the narrowest repair. Recheck it. Do not keep a second generation workflow here.

## When

Use this for a script, keyframe, generated clip, or finished video, including a review-only request. For a production, review the assembled film the user will receive. Judge generated footage inside that cut, not as loose clips. If the approved target is missing, separate defects you can see from judgments that need the target.

## Inputs and outputs

| | |
| --- | --- |
| Inputs | The artifact, the quality question, the approved brief or script, source evidence |
| Output | `review.md`: findings, the repair destination, the affected artifacts, how to recheck, and a status of pass, fail, or not checked for each item |

A valid file is not creative approval. An agent review is not user acceptance unless the user accepted that version.

## Must follow

- Start by finding the project and its brand layer, as [project](../mixreel/references/project.md) describes, and follow `brand/requirements.md` when it exists.
- Watch and listen when you can. A sampled review says sampled. A silent review says silent. Do not claim a camera move, a seamless cut, or a sound from one still.
- Follow [frame reading](../mixreel/references/frame-reading.md) for every inspection image, including reference contact sheets and `frame_pack.py` packs. Start with the overview, then look at every remaining frame. Notes between images are fine. Cross-check the cut lists. If one image is skipped or unreadable, the review is incomplete and cannot pass.
- On footage, run the suspect script, then build the frame pack every time, then decide. Suspects are not the verdict. Pixel problems use the frames. Action, line, and gaze problems use the real-time playback. If those disagree, write "uncertain". There is no OCR step.
- CLIP, DINOv2, face match, and SyncNet run when [review tools](references/review-tools.md) says the environment has them and the task needs them. Follow that file for the interpreter, per-shot SyncNet, and the confidence cutoff. Gemini, if the user asked, returns hints and does not decide.
- [Brand marks](../mixreel/references/brand-fidelity.md) on a keyframe or a film match the client asset.
- Audience-facing captions do not contain production notes. Required disclosures stay.
- Play returned files from the start through internal cuts.
- Route the repair to the earliest stage that owns the cause: script, keyframes, video plan, or clips. A single bad shot is regenerated as that shot. Keep the original sound and the edit grid. A review-only request stops at the recommendation.
- Any review fail, or a cut that visibly leaves the script or the continuity of a person or product, is not a finished deliverable. Fix it within the authorized budget, or stop and ask. Reporting an unresolved issue is not delivery. A review-only request still stops at the recommendation and does not ship the film.
- Follow [diagnosis](references/diagnosis.md) for how wide the repair is. A whole regeneration does not take the same model's last version as its base. A masked or cropped local repair may use any suitable model, including the one that made the image. Carry forward an unchanged image's pass only if it already passed and its requirements and references are unchanged. A pixel diff cannot approve a failed or unreviewed image. A repair that does not change pixels stays failed. After a repair, look for regressions, including regions that should have stayed still. Close a finding only with new evidence.

## Read next

| When | Open | Leave closed |
| --- | --- | --- |
| Now, for the checklist of this artifact | [Review criteria](references/review.md) | Generation procedures, until a repair is authorized |
| You are choosing the repair | [Diagnosis](references/diagnosis.md) | |
| The artifact is footage | [Video inspection](references/video-review.md) | |
| You are about to run a script | [Review tools](references/review-tools.md) | Do not open it just to decide the stage |
| The artifact is the script | [Ad checks](../mixreel-script/references/ad-script.md) | The rest of the script skill |
| Reusing a file | [Handoffs](../mixreel/references/handoffs.md) | |

A repair uses the responsible stage's skill, inside the authorized budget, and the same journal. Do not change provider, add a paid attempt, or rewrite the script just to close a review comment.
