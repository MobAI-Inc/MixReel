# Images

You are producing or repairing a frame. Read [image models](image-models.md) first if you have not. [Brand marks](../../mixreel/references/brand-fidelity.md) stay exact.

Use the user's chosen style source, such as their own artwork, their product photography, or frames from a reference they supplied. If it is undecided, ask. Plan the [generation groups](../../mixreel-video-plan/references/planning.md) first and create only the new keyframes needed to settle a visual question. Reuse accepted references, or share a keyframe across shots, when that is enough. Keep text-only visual designs for shots without a generated image. Resolve an unavailable tool before submitting. Record the actual model, since a product label alone does not verify a version.

## Settle the look, the product, and the people first

Frames made in parallel from loose references drift apart. Before a batch, get one frame's look approved, and one image of the product and of each recurring person in the target look. Those approved images then carry the batch.

The user's product and person references are the authority for appearance, and their form is the user's choice. Inspect what each covers and record it in `BRIEF.md`. A reference brings its rendering along with its face. When the only image of a person is in a different style from the target, feeding it directly can pull the frame back to that style, so make that person's image in the target look first. A style reference is not a license to copy a third party's product or face. Do not substitute anyone else's artwork or likeness without the user's confirmation.

## Select the composition source

Each new keyframe has one composition source. When a [previs](../../mixreel-script/references/previs.md) exists, the shot's render is that source. It supplies layout only. Its proxy colours and body shapes must not appear in the image. Without a previs, follow [composition](composition.md).

Check what the model does with a supplied image, and confirm it on the first frame. A finished picture given to an editing endpoint stays a finished picture. To change a pose or layout, build a blocking sketch from the composition source and blur it until no face, hand, or fabric edge can be read while positions and sizes still can. It replaces the source as the edited image. A whole repaint can drift a place the user wants kept, so composite the approved background back with a feathered mask when it does.

## Make the frame

Supply the composition source, the approved look, and the product or person image, and state each image's role in the prompt. A style image that shows a person can pass that person's face, hair, or figure to your people, so prefer images without faces, or crops limited to rendering and background. Before a person's appearance and wardrobe are approved, keep earlier finished images out so old clothing does not lock in. When several people share an image, state their order within it separately from each one's target position and clothing. Reference order does not decide placement in the scene. Carry the user's product or person reference on every frame that must match it.

Keep composition, shot scale, and time of day. Turn off automatic prompt rewriting where the endpoint offers it. Use each endpoint's own field names.

Keep wardrobe consistent across a continuous scene, using the choice recorded in `BRIEF.md`. Once the first keyframe showing a new outfit is approved, crop a wardrobe reference from it and include it in later generations and edits of that person.

Settle a new model or a changed step on the one frame that tests the most, calibrating as [image models](image-models.md#compare-and-calibrate) describes, then show the user the result you stand behind. Once it is approved, submit every remaining keyframe of that step together, review them together, and fix only the images that fail.

`reference-sheet.jpg` in the film folder, when there is one, shows which real file supports which shot. Send the real file as the input, never the sheet.

## Judge the whole picture

You are the first reviewer, and a frame that fails your review goes no further. Put the frame beside the approved frames and the product or person image, at full size. Ask first whether the whole picture is attractive and holds together, then whether the look matches, then whether the product or person is recognizable. A picture is one thing to the viewer. A closer likeness that leaves the person less attractive, or a repair that breaks the rendering, has failed. Unless the user says otherwise, appeal comes before likeness for a person. The product, its logo, and its packaging must still match the asset exactly. A frame that leans realistic produces realistic video, so catch that here.

## When a frame is wrong

Find which problem this is, then go back to the step that owns it.

| What you see | Go back to |
| --- | --- |
| Wrong look, too realistic, oily, drifted rendering | The look. Change the inputs on a model strong at style. A local edit cannot restore it |
| Wrong layout or pose | The composition source, then generate again |
| Not the same person or product, by a lot | The reference image and how it is supplied, then generate again |
| Not the same person, by a little | A masked precise edit. Larger moves follow [image models](image-models.md) |
| Hand, prop, garment, label, or clutter | A local edit that names the defect and its region and lists what stays |

A local edit changes the region that failed and keeps the camera, action, and subject size. Small or obscured faces stay that way. An identity reference does not authorize replacing the chosen wardrobe. If an edit reaches outside its region, composite the region back onto the pre-edit image with a feathered mask and check the seam at enlarged scale. The picture has to look made in one pass. Compare the repaired area's texture, edges, and light with what surrounds it at full size. When it reads smoother or cleaner, narrow the edit or list the rendering it must keep. A masked precise edit over the join may bring the texture back (untested). A patch that looks pasted has failed. A whole regeneration does not take the same model's last version as its base. A masked or cropped local repair may use any suitable model, including the one that made the image. How wide a retry may be is in [diagnosis](../../mixreel-review/references/diagnosis.md).

If the repair does not improve the defect, stop and reread diagnosis before you pay again. Do not switch providers to make a review comment go away. A provider change is a user decision.

## Confirm that the pass did its job

A finished job and a charge do not prove that anything changed. Measure it with [keyframe diff](keyframe-tools.md). When a model proves ineffective for a step, record the evidence and move to the next candidate the user has configured, within the budget.

## Record what was actually submitted

For each new keyframe record the composition source and why it was the one source, any style references, the product or person reference and what it is allowed to constrain, and the provider and model id that actually ran.

Before submission, state each input image's role according to `BRIEF.md`. Save an ordered input manifest for every generation or edit, with step, shot or job id, file or stable asset id, content hash, role and person mapping, plus model, parameters, prompt, and output ids. Pass `--manifest`, or a batch `manifest.json`, to `keyframe_diff.py` so the report keeps them. Check the inputs actually sent against this manifest. Keep credentials and temporary signed links out of shareable records. Keep originals and previous versions.
