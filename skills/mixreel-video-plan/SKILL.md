---
name: mixreel-video-plan
description: Group an approved ad script into generation requests, list the few keyframes those requests need, and write model-specific prompts with ordered references once the assets exist. Use before keyframes and again to finish prompts. Never submits paid video jobs.
---

# Plan the generation

Pipeline stages 3 and 5. The map is [pipeline](../mixreel/references/pipeline.md). This skill does not generate images or video.

Visit it twice on a new production. Before keyframes, write the groups and name the frames that are actually needed. After the assets exist, bind them and write one prompt per approved group. Do not submit on a placeholder prompt.

## When

Use this when an approved script or scene needs generation groups, a short keyframe list, or model prompts. If the provider is unresolved, write a provider-neutral group proposal and the capability questions. Do not invent model limits, picture labels, prices, or API fields. A standalone prompt does not need unrelated film metadata.

## Inputs and outputs

| | |
| --- | --- |
| Inputs | Approved script or scene, camera and action intent, reference roles, timing, assets you actually have, verified capabilities or explicit unknowns |
| Output | `video-plan.md`: groups, why each group is split, local timing, frames needed, capability evidence, the reference list, the cost basis (quoted, estimated, or unknown), prompt readiness. The provider prompt is separate from the planning note |

Add production fields to `plan.json` only when you have them. Keep version 1 and 2 compatibility. Use version 3 for continuations, per-shot sound, or overlays.

## Must follow

- Start by finding the project and its brand layer, as [project](../mixreel/references/project.md) describes, and follow `brand/requirements.md` when it exists.
- Group by what the verified provider can accept. Do not invent durations, reference caps, or prices. Read [providers](../mixreel/references/providers.md) and the user's config.
- Report editorial shots, generation requests, and new images as three counts. Do not turn cuts into separate paid requests in silence, and do not stretch a fast action to a file's minimum length.
- Record every group's `continues_from` as [planning](references/planning.md#continues_from) defines it. Groups with an empty `continues_from` may be submitted together. A group that names another waits for that group's accepted result. That batching happens later, inside produce. This stage stays in pipeline order.
- A rework resubmits only the groups that need changing. The scope rule is [diagnosis](../mixreel-review/references/diagnosis.md).
- Screen recordings and other real assets stay out of generation groups.
- [Brand marks](../mixreel/references/brand-fidelity.md), exact UI, and captions are composited in the edit, not drawn by the video model, unless the user has a real asset and has accepted a different route in writing. Keep them in the script and the edit. Do not delete them, and do not promise the model will render them.
- Keep action, gaze, geography, fast intervals, cause and effect, and authored endings. A new creative cut goes back to the script. Do not hide it in the prompt.

## Read next

| When | Open | Leave closed |
| --- | --- | --- |
| Now, on either visit | [Planning](references/planning.md) | Model files, until the model is settled |
| The provider is unresolved, or you are checking a capability | [Providers](../mixreel/references/providers.md) | Credentials, until a later stage is about to pay |
| The user's config uses MiniMax H3 | [MiniMax H3](references/minimax-h3.md), which links its coverage and format files when you write the prompt. Write it from the approved script. Do not edit that script to fit the prompt | The Seedance file |
| The user's config uses Seedance | [Seedance 2](references/seedance-2.md) | The H3 files. Do not use a Seedance draft as a step toward H3 |
| `plan.json` is a complete production plan | The validator command in [planning](references/planning.md#validator) | Do not run it on a script-only file |
| You are reusing a file | [Handoffs](../mixreel/references/handoffs.md) | |

For any other model, read that vendor's own documentation and its prompt guide. After the first visit, necessary new frames go to [keyframes](../mixreel-keyframes/SKILL.md). After the second visit, authorized submission goes to [produce](../mixreel-produce/SKILL.md).
