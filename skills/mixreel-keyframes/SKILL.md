---
name: mixreel-keyframes
description: Create or locally repair the keyframes an approved generation group needs. Product and person consistency come from user-supplied references, not from a fixed model route.
---

# Keyframes

Pipeline stage 4. The map is [pipeline](../mixreel/references/pipeline.md). Make the stills the video plan asked for. Do not add shots.

## Output

The images, `keyframes.md`, the ordered input manifest, comparison notes, and costs as quoted, estimated, or billed.

## Must follow

- Start by finding the project and its brand layer, as [project](../mixreel/references/project.md) describes, and follow `brand/requirements.md` when it exists.
- Read [image models](references/image-models.md) before any image call. It says what each model is like and where to start. The user's config and choice decide, and a model never changes silently.
- One composition source per new frame. Prefer a previs still when you have one. Otherwise use a user-supplied, licensed reference. Do not fetch images from a third-party site.
- Generation and editing may use different providers. Make one sample and wait before the batch. The sample is a creative check, not a hunt for a private model ranking.
- Carry the user's product or person reference on every frame that must match it.
- [Brand marks](../mixreel/references/brand-fidelity.md) come from the real asset.
- After an edit, run [keyframe diff](references/keyframe-tools.md). A pass that does not change the pixels is a failed repair. Do not feed a model's previous output back in as the base for another pass with the same model.
- One version per paid request. See [execution](../mixreel/references/execution.md).

## Read next

| When | Open |
| --- | --- |
| Before any image call | [Image models](references/image-models.md) |
| Writing a request for a chosen model | [Request parameters](references/image-model-params.md) |
| Choosing inputs | [Images](references/images.md) |
| Choosing the composition source | [Composition](references/composition.md) |
| Running the diff | [Keyframe tools](references/keyframe-tools.md) |
