# Diagnosis

This file is the source for how wide a repair is. Other stages link here. Do not restate a wider rule elsewhere.

Compare the result with the approved shot, the selected references, and the inputs that were actually submitted. Describe the visible difference and the evidence for its cause.

Find the earliest stage that introduced the defect. Change only that stage's input or execution, say which later artifacts it affects, and keep accepted work elsewhere.

| Cause | Stage to reopen |
| --- | --- |
| Wrong claim, missing product, wrong action | Script |
| Wrong frame, broken package, identity drift in a still | Keyframes |
| Wrong grouping, prompt, or reference binding | Video plan |
| Bad motion inside an otherwise approved prompt | Produce, that shot only |
| Late cut, level, caption timing | Produce, the edit |

A set produced together keeps that limit: an unaffected group is not resubmitted. Carry a passed image forward only when it passed and its requirements and references are unchanged. A pixel diff cannot approve a failed or unreviewed image. A repair that does not change the image stays failed.

For a whole regeneration, revise the original inputs to the stage where the problem arose, and do not take the same model's last version as the base. A masked or cropped local repair may use any suitable model, including the one that made the image, under [images](../../mixreel-keyframes/references/images.md#when-a-frame-is-wrong).

When an accepted clip has a defect confined to one shot, regenerate only that shot. Where the endpoint supports frame conditioning, open the new request on the clip's own frame at that shot's start and ask for the minimum duration. Replace only the picture for that interval in the edit and keep the original clip's sound, so the score, dialogue timing, and cut grid continue. Check that the replacement matches the neighbouring shots.

After the repair, review the changed result against the same target, including the regions that should have stayed still. If the result is not better, revise the diagnosis before another paid attempt. Record findings and costs in the project folder. One project's result does not establish a general rule about a category, a style, or a model.

Do not close a review by switching vendor, adding an extra paid try, or rewriting the script. Those are new user decisions. A review-only request stops at the recommendation.
