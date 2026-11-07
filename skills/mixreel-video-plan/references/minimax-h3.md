# MiniMax H3

Open this when the user's config has settled on MiniMax H3 and you are planning for it or writing its request. If the model is not settled yet, return to [the video-plan skill](../SKILL.md). MixReel does not pick a video model for you. This file is a starting point, and the user can change the model at any time. It writes prompts and submits nothing. Do not write this and a [Seedance 2](seedance-2.md) prompt for the same scene. The adapter is `providers/minimax_video.py` in the repository, and the calling order is in [providers](../../mixreel/references/providers.md).

## What H3 is like

These were observed on films with painted illustration. They were not observed on product photography or photoreal people. Treat them as a place to start. What you see on this project outranks them.

- It follows its keyframes, so a frame that leans realistic gives realistic video.
- Fine details do not always obey the prompt. A rendering it should keep needs saying, such as matte skin and an animated feel.
- It cannot animate on twos from a prompt, so frame-rate reduction belongs in the edit.
- Spoken lines tend to land later than asked and rush when packed. Give each line its natural time, leave handles, and carry on in a new request as [planning](planning.md#continue-past-the-duration-limit) describes.
- Every clip we received carried a stereo track.
- Listeners who only act need their own reaction beats, or they stand frozen.
- Naming a prop or person in a shot where it must stay out of frame tends to put it in the picture. Describe the gaze or the screen position, and name the thing only in shots that show it.
- A request packed with cuts reads as rushed. An action that can fail, such as opening, cutting or handing over, needs enough screen time to finish.
- A composition or ending reference is a soft guide. Do not promise an exact ending from prose alone. A label in the prompt does not switch on reference handling. The request's roles do that.

## Request parameters

Checked 2026-11-04 against MiniMax's [create-task page](https://platform.minimax.io/docs/api-reference/video-generation-v2-create). Read it again before a paid call. Model names come from the user's config.

| Model | `resolution` | `duration`, whole seconds |
| --- | --- | --- |
| `MiniMax-H3` | `768P`, `2K` | 4 to 15 |
| `MiniMax-H3-Highspeed` | `480P`, `768P` | 4 to 15 |
| `MiniMax-H3-Lite` | `480P`, `768P` | 4 to 15 |
| `MiniMax-H3-Max` | `480P`, `768P` | 5 to 15 |

| Field | Values | Notes |
| --- | --- | --- |
| `ratio` | `adaptive`, `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, `9:16` | Text-only needs a fixed ratio. Frame mode is always adaptive. Lite has no adaptive in reference mode |
| Text | Up to 7,000 characters | One non-empty item is always required |
| `first_frame`, `last_frame` | One each | Cannot share a request with any reference |
| `reference_image` | Up to 9, 30MB each | JPG, PNG, WEBP, HEIC. Aspect ratio 0.4 to 2.5 |
| `reference_video` | Up to 3, 2 to 15 seconds each, 15 in total, 50MB each | MP4 or MOV |
| `reference_audio` | Up to 3, 2 to 15 seconds each, 15 in total, 15MB each | WAV or MP3 |
| Request body | 64MB in total | Use URLs or uploaded file ids for large media |
| `extra.prompt_expansion_mode` | `disabled`, `balanced` default, `quality` | Max only |

The page lists no seed, watermark, or quote field.

## Price

Listed on MiniMax's [pricing page](https://platform.minimax.io/docs/pricing/overview#models/video) on 2026-11-04, in US dollars per second. There is no quote field on the create-task page, so estimate from this list and send no test request.

| Model and resolution | Output | Input reference video |
| --- | --- | --- |
| H3, 2K | 0.13 | 0.13 |
| H3, 768P | 0.08 | 0.08 |
| Highspeed, 768P | 0.06 | 0.06 |
| Highspeed, 480P | 0.04 | 0.04 |
| Lite, 768P | 0.04 | 0.04 |
| Lite, 480P | 0.025 | 0.025 |
| Max, 768P | 0.08 | 0.143 |
| Max, 480P | 0.05 | 0.0553 |

Input reference video is billed by its duration. Each task includes some images free, five on the flagship models and two on Max, and the page lists a per-image price for the rest. Audio input is free.

## Prompt wording

MiniMax's own material comes first.

- [H3 feature highlights](https://platform.minimax.io/docs/guides/video-prompt) has example prompts, which cite inputs in plain words such as "Image 1".
- [Video generation guide](https://platform.minimax.io/docs/guides/video-generation) describes the input modes.
- [H3-Context-IR](https://platform.minimax.io/docs/api-reference/video-generation-v2-h3-context-ir) is an official endpoint that turns your text and media into a structured prompt, without generating video. It costs money, $0.90 per million input tokens and $3.60 per million output tokens on the pricing page above. Show the user its result before you send it.

These pages do not say how a number in the prompt maps to an uploaded file, and they do not document a dialogue syntax. [H3 format](h3-format.md) is MixReel's own way of writing the prompt. It uses `<Picture N>` for images in upload order and `<d>...</d>` for spoken lines. It has been used on real H3 requests, and MiniMax's official pages do not describe it. Upload in the order you cite, as [planning](planning.md#prompts) says, and check both on one sample before a batch.

## Writing the prompt

Turn one approved scene, with its ordered shots for one generation group, directly into the final H3 prompt. Do not write a Seedance-style description first as a step toward it. Write it from the approved script. Do not edit that script to fit the prompt. Keep the event, people, location, product and props, spatial relationships, gaze, action order, reactions, and final image the script supplies.

### Reference mode and approved cuts

Use this format only when the endpoint is verified to accept references this way. A label in the prompt does not switch on reference handling. A composition or ending reference is a soft guide unless the endpoint offers a verified strict frame constraint.

The approved plan controls shot boundaries and music events. Write one prompt for the approved group, with request-local timing for its cuts and actions. Do not make a paid call per shot. Bind video and audio references only through documented syntax, and keep picture labels for images. Say when timing has to be carried in text because a media input is unsupported. When a clip is one approved continuous shot, keep it continuous, and propose any new internal cut before generation.

### Inputs

- The approved scene and its ordered shot descriptions for one group.
- The ordered reference list. Each image has its exact `<Picture N>` number and role, such as product, person identity, outfit, environment, visual style, or a frame anchor. Video and audio inputs keep their own identifiers and roles.
- The chosen visual style, when no reference already supplies it.
- Any exact spoken line.
- The target aspect ratio, when it changes the composition.
- Any duration or duration ceiling the user gave. Otherwise the duration comes from the finished shot plan.

The upload order is authoritative. Never derive picture numbers from prose order, file names, URLs, or tag order. If the real order is unknown, stop and report that the picture labels cannot be bound safely.

Product photos, person portraits, outfit references, backgrounds, and style images are reusable visual references. Treat them as `reference generation`. Do not call an image a first frame, keyframe, or last frame unless the request really assigns that role.

### 1. Lock the event

List the ordered visible beats before choosing shots. Track where every person, the product, and every prop that matters begins, what changes, who sees what, and which image must end the clip. Do not move a person to another place, merge separate spaces, reverse a cause and its reaction, or invent a new event.

For every decisive physical action or change in a prop's state, write its four parts: the starting state, the contact or force that causes the change, the visible transition, and the result. Give actions that tend to fail, such as cutting, locking, opening, pouring, or handing over, enough screen time to finish. Describe positive geometry and cause instead of words such as `really` or repeated prohibitions. When the model's usual way of performing an action would break the scene, such as a carried ladder swinging across a coworker, specify a concrete pose or path that cannot break it, for example the ladder held upright against the carrier's own shoulder.

Write the feeling as an arc: the opening state, the beat that changes or intensifies it, and what is left in the final image. A mood that is meant to stay still can stay still. Name the atmosphere once, then carry it through what can be seen and heard: pace, a held breath, gaze, distance between bodies, hesitation, light, movement in the setting, synchronous sound. In every shot where a person's reaction matters, write the performance: where the eyes go, the brows, jaw, and breath, its timing, and a held beat after each decisive action so it can land.

When distance, safety, or who holds the product carries the beat, decide what proves it on screen before you direct: the exact hands, feet, gap, threshold, obstruction, or object that must stay readable. Keep that proof in the decisive shot and, when it is the outcome, in the final image.

### 2. Design the coverage

Read [cinematic coverage](cinematic-coverage.md). Keep every cut or composition the script states. Where the script leaves coverage open, choose the shots needed to make its action and reaction readable.

A clip may use one shot or several. Do not default to one fixed composition, and do not add cuts to reach a quota. For two people, make the spatial relationship clear and use eyeline-matched over-the-shoulder shots, reverse shots, or reaction close-ups when the exchange depends on what each person sees. Use an environment shot or a product insert only when it establishes place, mood, a transition, evidence, or a change of state.

Each shot gets one camera behavior. A static shot stays locked. A moving shot uses one principal movement such as a track, pan, tilt, or push-in. A later shot may choose a different behavior. Keep screen direction, eyelines, prop continuity, and body positions across cuts.

Finish the whole shot plan before assigning any timestamp, and confirm that each shot has a job. Find where each action completes, where the feeling turns, and where the proof becomes visible. One shot may carry several of these. None may exist only in explanatory prose.

### 3. Derive the duration

Estimate how long each planned shot needs for its action, camera movement, spoken line, and reaction to read naturally, using the timing in [cinematic coverage](cinematic-coverage.md). Add them and round up to a whole second, then to a duration the endpoint supports that lets the action finish.

Keep a brief action separate from its setup and reaction, even when the file must meet the endpoint's minimum. Do not stretch a simple event to a familiar default or squeeze a complex one to reuse another clip's length. Do not cut reactions below their readable time to keep more shots. A request packed with cuts reads as rushed and flattens the performance. If the honest estimate exceeds the maximum, first remove decorative coverage or merge shots that stay readable. If the event still cannot fit, stop and report that it needs more than one clip instead of dropping beats.

When the user gives an exact duration, fit the coverage to it without damaging the event, and report a conflict if the action cannot read inside it. When the user gives a ceiling, choose the shortest natural duration at or below it. Then give every later shot a strictly increasing cut time inside the duration, with time for the final action or reaction to finish before the clip ends.

### 4. Bind references

Give each product, person, background, prop, and style reference a stable `<Subject N>`, and cite its exact `<Picture N>` in the definition. Keep only the roles assigned to each reference. A face reference does not supply wardrobe. For an approved wardrobe change, bind the chosen outfit separately and keep the approved action, pose, gaze, and expression.

Keep appearance bound to references. Do not invent hair, facial features, clothing, packaging, architecture, colours, or materials that the references should supply. Give every prop that matters an explicit position and state change in the shot where it matters. Do not name a prop or person in a shot where it must stay out of frame, even in a negative sentence. Describe the gaze direction or screen position instead.

### 5. Write the prompt

Read [H3 format](h3-format.md) and write its six sections in their exact order, in English prose, with spoken lines and visible source text in their original language.

Use `[Shot 1]` without a timestamp. Start every later shot with `[Shot N] At MM:SS.mmm, ...`. Put exact spoken words inside `<d>[Language] ...</d>` and give speakers stable `(S1)`, `(S2)` ids in the order they actually speak. Do not invent dialogue.

Write synchronous ambience, action sounds, and non-verbal human sounds, following the approved sound plan. Use `non_diegetic_music` for a model-composed score only when native music output is verified. Use `N/A` for no generated score, or for score added in the edit. Do not erase the script's music request with a template default.

Keep the prompt compact. `summary` is one short sentence, `retention_analysis` covers reference fidelity, and `detailed_description` carries the staging. Do not repeat the same appearance, geography, mood, or prohibition in all three. When shortening, cut repeated style language and explanation before any beat, cause, change of feeling, spatial proof, spoken line, or the final image.

### 6. Check it

Before returning the prompt, confirm:

- The shots keep every beat of the script and its final image.
- Every decisive action shows its starting state, contact or force, transition, and result.
- The feeling has an opening state, a turn when the script has one, and what is left at the end, all carried by things the camera or microphone can catch.
- Any distance, safety, or ownership the beat depends on stays visible as physical evidence.
- Cuts reveal action, reaction, space, mood, or information.
- Geography and eyelines between two people stay coherent.
- Gaze targets are explicit during turns, looks back, and shifts of attention, including when a camera move reveals a face.
- Every reference label matches the upload order and keeps one meaning.
- Every prop that matters has continuous position, ownership, and state.
- Nothing that must stay out of a shot is named in that shot.
- Risky actions name a concrete safe pose or path instead of a prohibition.
- Cut times increase and stay inside the duration.
- Spoken lines, sound, and visible text are in sync and not invented.
- The prompt has no unresolved tags, URLs, local paths, model settings, commands, subtitles, logos, watermarks, or fade to black.
- The whole prompt fits the endpoint's character limit.

### Output

Return one JSON object. `duration` is the chosen whole number of seconds. `description` holds the full six-section prompt. Do not repeat the duration inside the prompt body.

```json
{"duration":10,"description":"subject_definitions:\n...\n\nsummary:\n...\n\nretention_analysis:\n...\n\ndetailed_description:\n...\n\noverall_soundscape:\n...\n\nnon_diegetic_music:\nN/A"}
```

This file authors a prompt only. It does not call a provider API, upload media, or start any paid generation, and it does not edit the approved script.
