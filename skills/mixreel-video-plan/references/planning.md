# Planning

You are in video plan. The stage card is [the video-plan skill](../SKILL.md). Open a model file only when that card says the model is settled and you are writing for it.

## Plan generation requests before images

Keep editorial shots separate from generation requests. Default to one request for the whole generated sequence when it fits the verified maximum duration, the prompt limit, and the provider's reference limits, including several approved shots when the provider supports them. Group connected action and shared geography together. A product screen inside a scene does not split it, as [ad script](../../mixreel-script/references/ad-script.md#product-copy-and-ui-on-screen) describes. Split only for a documented reason: the endpoint's duration or reference limits, a real scene change, incompatible inputs, or a smaller retry if one shot is likely to be rejected. In reference mode, keyframes and reference images are soft guides, so wanting a separate opening frame for each part is not, by itself, a reason to split. Do not assume grouping guarantees continuity.

Shots that are a supplied recording use `production: local`. They do not appear in `generation_groups`.

Before producing keyframes, record the ordered shot ids, requested duration, continuity requirements, references, and grouping reason in `generation_groups` as described in [records](../../mixreel/references/records.md). Keep each shot's own action and camera plan.

## Keyframes and references

Ask for the fewest new frames the groups need: reviewed images that establish identity, wardrobe, spatial layout, or a critical state that the script and other references cannot reliably convey. Reuse suitable accepted assets. A shot can share a keyframe or need no new image. Do not generate a starting and ending frame for every cut. A product-consistency or person-consistency reference is a user-supplied image, carried on every request that needs it. Name the file. Do not ask a model to invent the package.

Use the approved script and shot sequence as the main direction. When a previs exists, its storyboard sheet can carry staging and camera direction for every shot in one ordered image. How that sheet may be used is in [previs results](../../mixreel-script/references/previs-render.md#use-the-results-downstream). Read that only when a previs was built. Add reference video for the composition or motion role the user assigned, reference audio for approved timing or sound, and style or person images only in their recorded roles. A style image or clip that shows a person can transfer that person's identity. Prefer style material without faces, or an approved project frame, and check every person after generation.

Verify that the endpoint accepts these media types together, including durations, counts, ordering, and sound behavior. If a reference cannot be submitted, record the limitation and translate its observed timing or motion into text. Do not pretend that the model received the media, and do not switch providers silently. Music used for timing need not become generated background sound. Follow the script's decision on where the final score comes from. When edit-layer music will replace the model's audio, prompt for spoken lines and sound without score.

## Cost and timing

Compare grouping alternatives using the actual provider's minimum billable duration, duration steps, resolution, and the expected retry scope. Show requested and billable seconds per request, the total quoted or estimated cost, and what a rejected sequence would require regenerating. One rejected group is the unit you would regenerate. Keep unknown prices and retry rates unknown. Do not promise that fewer calls are cheaper unless the quote says so. Reserve and reconcile each generation request once in the journal, even when its file supplies several timeline shots.

Separate the duration of an action from the duration of its generated file. Give fast actions a brief execution interval, clear contact, and a readable aftermath within the sequence. Do not stretch them to the provider's minimum length. Use any extra footage for approved setup, reaction, or removable handles. Do not invent filler actions, default slow motion, or a blanket speed-up. Translate shot times and musical accents to request-local times, with the intended cuts and action speeds explicit.

## Continue past the duration limit

When the generated sequence exceeds the verified maximum and the provider documents continuation, generate the first request at that maximum and continue from its accepted result. Use the final seconds of that clip as the next request's reference video, plus its audio as reference audio when score or ambience must carry on, and write the new prompt as a continuation of that clip. Verify that the endpoint accepts these references together. Independent segments cannot share motion, sound, or music, so use them only when continuation is unsupported.

## continues_from

Record `continues_from` on every group, with the earlier group id and how much of its tail you are reusing. An empty `continues_from` means the group may be submitted at the same time as the other empty groups. A group whose `continues_from` names another group waits for that group's accepted result. Do not point a continuation at a group that does not exist yet. This batches only the submissions inside produce. Stages stay in [pipeline](../../mixreel/references/pipeline.md) order. A rework resubmits only the groups that need changing, per [diagnosis](../../mixreel-review/references/diagnosis.md).

Place each continuation boundary at a planned cut, so the continuation opens on a new camera setup. A continuation that resumes the same shot tends to reframe slightly, which reads as a jump. Inspect the seam, discard repeated or jumping head frames, and record the source ranges actually used.

## Shot motion

Read the approved shot plan and reference list before each prompt. Keep the principal camera behavior, gaze targets, visible action sequence, and final state. Name subjects by stable roles and exact reference order instead of vague pronouns. Do not substitute looking at the lens for looking toward another person or the product.

Choose camera and subject movement from the approved sequence and the reference observations. Describe what changes during the shot and what the viewer should notice as it unfolds.

Plan the approved group as one request using the selected endpoint's verified multi-shot format. If the available authoring mode handles only one camera setup, keep it for a suitable single-shot group, or resolve the capability mismatch before submission. Do not silently break a group into per-shot paid calls or introduce unapproved angles.

## Capability and reference checks

Before submission, read the selected provider profile and its current documentation. Find out whether strict start and end frames and style references can share a request. If they cannot, compare the trade-off and choose a supported mode. Never silently drop a reference. For reference-only mode, describe opening and ending images as requested anchors, and inspect whether the video actually follows them.

When a stylized look must hold, provide a supported style conditioning input and carry the approved rendering description into each clip. If none is available, propose an authorized representative sample or report the limitation before a batch. Execution belongs to produce. Provider support and practical quality are separate questions.

Allow edit handles around essential actions where the model's timing is unreliable. Choose length from readable action plus tested timing tolerance, within supported durations and budget. Do not impose the same seconds or a historic delay on all models. If complexity exceeds the slot, simplify or split before paying.

## Prompts

Write the prompt in the language the provider's current public guide expects, keeping spoken lines and visible source text in their original language. Bind images in the order the request will upload them. If you do not yet know that order, the prompt is not ready.

Say what the camera does, what the product or the person does, and the end state. Do not convert one vendor's prompt into another's by renaming fields. Limits, prices, traits, links to the official guides, and how to write each prompt are in [MiniMax H3](minimax-h3.md) and [Seedance 2](seedance-2.md). For any other model, follow that vendor's own documentation.

## Comparisons

This covers video. A resolution, motion-risk, or model comparison of clips is a paid experiment. Propose it only when the choice cannot be made otherwise, and run it only when the user asks for that comparison and names the maximum charge. Test one representative shot before you multiply the cheaper option. One-frame image comparisons follow [execution](../../mixreel/references/execution.md#one-version-per-paid-request).

## Validator

Run this only when `plan.json` is a complete production plan. Do not run it on a script-only artifact, and do not invent music or generation groups so a script will pass. `<mixreel>` is the installed `mixreel` skill folder, next to this skill's own folder.

```sh
python3 <mixreel>/scripts/validate_plan.py plan.json
```
