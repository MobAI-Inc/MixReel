---
name: mixreel-keyframes
description: Create or locally repair the keyframes an approved generation group needs, choosing among image models by what each step has to solve. Settles the look, the product, and the people before a batch. Product and person consistency come from user-supplied references, not from a fixed model route.
---

# Keyframes

Pipeline stage 4, after video plan has named the frames a new production needs. The map is [pipeline](../mixreel/references/pipeline.md). You are here to make or repair stills. Do not add shots, and do not submit video.

## When

Use this for the keyframes of a video, or for a standalone still with its own visual specification. Do not invent a whole-film plan for a single image. On a video, reuse suitable assets and share a frame when one frame is enough. Generate only the new frames the plan could not cover with text.

## Inputs and outputs

| | |
| --- | --- |
| Inputs | Approved shot or visual request, the list of frames needed, composition, product, person, style, and wardrobe assets, provider access, budget |
| Output | The images, `keyframes.md`, step and version records, the ordered input manifest, comparison notes, and costs as quoted, estimated, or billed |

Pending, accepted, and rejected versions stay distinct. Hand the selected assets back to video plan for the prompt visit.

## Must follow

- Start by finding the project and its brand layer, as [project](../mixreel/references/project.md) describes, and follow `brand/requirements.md` when it exists.
- Read [image models](references/image-models.md) before any image call. It says what each model is like and where to start. The user's config and choice decide, and a model never changes silently.
- Settle the look, the product, and each recurring person before a batch, then work as [images](references/images.md) describes. Generation and editing may use different providers. Make one sample and wait before the batch. The sample checks this project's look. It does not try to rank models for later jobs.
- One composition source per new frame. Prefer a previs still when you have one. Otherwise use a user-supplied, licensed reference. Do not fetch images from a third-party site.
- Carry the user's product or person reference on every frame that must match it. Keep each input's confirmed role. Appearance, reference format, and wardrobe are the user's choices.
- [Brand marks](../mixreel/references/brand-fidelity.md) stay exact on every image. Check logos, packaging text, product copy, and app UI against the real asset.
- A repair goes back to the step that caused the problem, and changes only the images that need it. After an edit, run [keyframe diff](references/keyframe-tools.md). A pass that does not change the pixels is a failed repair. A whole regeneration does not take the same model's last version as its base. A masked or cropped local repair may use any suitable model, including the one that made the image.
- One version per paid request. See [execution](../mixreel/references/execution.md). Planning or mock mode writes a manifest. It does not claim an image was generated.
- This stage does not run beside video plan or produce.

## Read next

| When | Open | Leave closed |
| --- | --- | --- |
| Before any image call | [Image models](references/image-models.md) | Prompt files for video models |
| While generating or editing | [Images](references/images.md) | |
| Writing a request for a chosen model | [Request parameters](references/image-model-params.md) | Models you did not choose |
| No previs and no fitting reference frame | [Composition](references/composition.md) | |
| Checking a pass, or re-reviewing | [Keyframe tools](references/keyframe-tools.md) | |
| Before a paid call | [Providers](../mixreel/references/providers.md), [local configuration](../mixreel/references/local-config.md), [execution](../mixreel/references/execution.md) | Do not open these during a mock |
| A result is wrong and you are choosing the retry | [Diagnosis](../mixreel-review/references/diagnosis.md) | Do not regenerate the whole set |
| Reusing a file | [Handoffs](../mixreel/references/handoffs.md) | |
