# MiniMax H3

Open this when the user's config has settled on MiniMax H3 and you are planning for it or writing its request. MixReel does not pick a video model for you. This file is a starting point, and the user can change the model at any time. It writes nothing and submits nothing. The adapter is `providers/minimax_video.py` in the repository, and the calling order is in [providers](../../mixreel/references/providers.md).

## What H3 is like

These were observed on films with painted illustration. They were not observed on product photography or photoreal people. Treat them as a place to start. What you see on this project outranks them.

- It follows its keyframes, so a frame that leans realistic gives realistic video.
- Fine details do not always obey the prompt. A rendering it should keep needs saying, such as matte skin and an animated feel.
- It cannot animate on twos from a prompt, so frame-rate reduction belongs in the edit.
- Spoken lines tend to land later than asked and rush when packed. Give each line its natural time, leave handles, and carry on in a new request as [planning](planning.md#continuations) describes.
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

MixReel adds no prompt format for H3. Use MiniMax's own material.

- [H3 feature highlights](https://platform.minimax.io/docs/guides/video-prompt) has example prompts, which cite inputs in plain words such as "Image 1".
- [Video generation guide](https://platform.minimax.io/docs/guides/video-generation) describes the input modes.
- [H3-Context-IR](https://platform.minimax.io/docs/api-reference/video-generation-v2-h3-context-ir) is an official endpoint that turns your text and media into a structured prompt, without generating video. It costs money, $0.90 per million input tokens and $3.60 per million output tokens on the pricing page above. Show the user its result before you send it.

These pages do not say how a number in the prompt maps to an uploaded file, and they do not document a dialogue syntax. Upload in the order you cite, as [planning](planning.md#prompts) says, and check both on one sample before a batch.
