---
name: mixreel-video-plan
description: Group an approved ad script into generation requests and list the keyframes those requests need. Write the provider prompt only after the assets exist.
---

# Plan the generation

Pipeline stages 3 and 5. The map is [pipeline](../mixreel/references/pipeline.md). This skill does not generate images or video.

Visit it twice. Before keyframes, write groups and which frames are necessary. After the assets exist, write one prompt per approved group. Do not submit on a placeholder prompt.

## Output

`video-plan.md`: groups, why each group is split, local timing, frames needed, the capability evidence, the reference list, and the cost basis (quoted, estimated, or unknown). The provider prompt is separate from the planning note.

## Must follow

- Read [planning](references/planning.md). Group by what the verified provider can accept, not by a private prompt formula.
- Do not invent durations, reference caps, or prices. Read [providers](../mixreel/references/providers.md) and the user's config.
- Screen recordings and other real assets stay out of generation groups.
- [Brand marks](../mixreel/references/brand-fidelity.md) are composited, not drawn by the video model, unless the user has a real asset and has accepted a different route in writing.

## Read next

[Planning](references/planning.md). Prompt wording follows the provider's own public guide. This skill does not add a second, private prompt format.
