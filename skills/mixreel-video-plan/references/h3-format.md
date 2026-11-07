# H3 format

Open this only while writing a MiniMax H3 prompt, after [MiniMax H3](minimax-h3.md) tells you to. Otherwise close it.

This file writes prompts only. It does not submit generation jobs. Verify the endpoint with [providers](../../mixreel/references/providers.md) before execution. This format is MixReel's own way of writing an H3 prompt. It has been used on real H3 requests. MiniMax's official pages do not describe it, so try it on one request before a batch.

Use it after the clip has been divided into a coherent shot sequence.

## Exact section order

The prompt contains these six fields in this order:

```text
subject_definitions:
...

summary:
...

retention_analysis:
...

detailed_description:
...

overall_soundscape:
...

non_diegetic_music:
N/A
```

## Reference labels

`<Subject N>` names reusable visible content such as a product, a person, an environment, a prop, or a visual style. Define each subject once and keep its meaning stable.

`<Picture N>` identifies an input image by its actual upload order. When an image supplies identity, outfit, packaging, environment, or style, cite it inside the matching subject definition. One picture may supply several subjects, and one subject may combine several pictures when each role is stated.

Write a standalone `<Picture N>` definition only when the image is an exact first frame, keyframe, last frame, edited frame, storyboard, or composition anchor. Ordinary identity and environment references do not become frame anchors.

## `subject_definitions`

Give every reused product, person, environment, prop, style, standalone picture, video, or audio reference one clear definition. When a visual style is a hard requirement, define it as the first subject so the prompt opens with it. Name its source references and the motion texture it implies, and render every shot in it. State which asset supplies each subject and what must stay stable. Do not invent visual traits the references do not show.

Example:

```text
<Subject 1> is the courier as shown in <Picture 1>; preserve her identity, current outfit, proportions, and rendering while changing only pose, gaze, expression, and action.
<Subject 2> is the insulated delivery bag as shown in <Picture 2>; preserve its shape, colour, and printed logo exactly.
```

## `summary`

Begin with `[reference generation]` for ordinary reference-image generation. Summarize the target event, the shot flow, and the main reference relationships in one short English paragraph. Use only labels already defined.

Use other task types only when the input really requires them:

- `keyframe completion` for an exact target frame anchor.
- `video editing` when an existing source video is directly modified.
- `video continuation` when the target continues an existing video.
- `audio reuse` when the same audio signal is copied.
- `audio reference` when timbre, rhythm, voice, or sound texture guides new audio.

Combine real relationships with ` + ` inside one bracketed prefix.

## `retention_analysis`

Write one line for every defined label. Name the shots where visible subjects appear.

Use only the matching markers:

- `fully_preserved` when the defined identity, outfit, product, environment, prop, or style role stays intact.
- `partially_preserved` when part of that role changes or appears only partly.
- `attribute_transfer` when referenced traits move to another identifiable target.
- `weak_reference` when only broad style, atmosphere, composition, or category remains.

New actions the scene requires do not count as lost identity fidelity.

## `detailed_description`

Open with one or two English sentences establishing the visual style. Then write the video in playback order.

- `[Shot 1]` has no timestamp.
- Every later shot begins `[Shot N] At MM:SS.mmm, ...` with a strictly increasing cut time inside the requested duration.
- For every shot, describe composition, visible subjects, environment, action, camera behavior, synchronous sound, and continuity from the shot before.
- Insert each reference label where its role first becomes visible and wherever a concrete frame, video, or audio relationship applies.
- End on the script's final image without a fade.

Keep speaker ids stable in the order people actually speak. A referenced speaking person appears as `<Subject N> (S1)`. Put exact spoken words inside `<d>[Language] ...</d>`. Keep the original wording and language. Do not turn thoughts or meaning into dialogue.

## Sound fields

Keep dialogue and sound events tied to shots in `detailed_description`.

`overall_soundscape` summarizes continuous ambience, physical action sounds, and non-verbal human sounds. Do not repeat dialogue there.

`non_diegetic_music` describes score only the audience hears. Use `N/A` when the approved plan calls for no generated score, including music added separately in the edit. If the approved script asks for model-composed music and the endpoint supports it, write the cue progression, texture, accents, and ending here. Do not silently replace an authored score with `N/A`. Unsupported audio needs an explicit production alternative. Separate generated clips need a documented plan for musical continuity or transition.

## Prompt exclusions

The finished prompt body contains no raw tags, URLs, local paths, YAML, model name, duration field, ratio field, resolution field, request schema, subtitles, logos, watermark, or command. The outer result carries the chosen whole-second `duration`. That value controls shot timing but is not repeated inside the six-section body.
