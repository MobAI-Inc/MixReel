# Image model request parameters

Open this when the user's config has settled on a model and you are writing its request. Choosing the model is in [image models](image-models.md).

Each section gives the date it was checked and the official page. Vendors change these often, so read the page again before a paid call, and follow [providers](../../mixreel/references/providers.md). Field support belongs to the service you actually call. Anything marked unverified was not confirmed on an official page.

## Midjourney

Checked 2026-11-04. Midjourney's documentation blocked direct reading, so the omni values come from a search excerpt of its [Omni Reference page](https://docs.midjourney.com/hc/en-us/articles/36285124473997). MixReel has no Midjourney adapter. Whether Midjourney offers an official public API is unverified, as are its prices. Check both, and its terms on automated use, before opening an account.

Parameters go inside the prompt text.

| Parameter | Values | Use | Status |
| --- | --- | --- | --- |
| `--oref <image>` | One image, version 7 | Omni reference. Carries a character or object from the image into new images. An upper-body portrait held the face well. Describe any costume outside the crop in the prompt | Official excerpt, plus our observation |
| `--ow` | 1 to 1000, default 100 | Omni weight. The page advises staying below 400 unless stylize is very high. We observed 700 with `--sw 250` holding a character while taking a new look | Official excerpt, plus our observation |
| `--sref <image...>`, `--sw`, `--sv` | `--sw` 0 to 1000, default 100 | Style reference, style weight, style algorithm | Unverified |
| Image at the start of the prompt, `--iw` | `--iw` 0 to 3, default 1 on version 7 | Image prompt, for composition or shape | Unverified |
| `--c`, `--weird`, `--s` | `--c` 0 to 100, `--weird` 0 to 3000 | Variety, oddness, stylize | Unverified |
| `--ar`, `--seed`, `--no`, `--raw`, `--exp`, `--v` | Unverified | Ratio, seed, exclusions, less default styling, extra detail, version | Unverified |

The same excerpt says omni costs twice the GPU time of a normal version 7 image, does not work with Fast mode, Draft mode, conversational mode or `--q 4`, and that its results cannot use Vary Region, Pan or Zoom Out. Pin `--v 7` when using omni. Which version is the current default, and how omni behaves on later versions, is unverified.

## Ideogram 4.5

Checked 2026-11-04 against the official [generate](https://developer.ideogram.ai/api-reference/images/generate/ideogram-4-5.md) and [precise edit](https://developer.ideogram.ai/api-reference/images/precise-edit/ideogram-4-5.md) pages. Host `https://api.ideogram.ai`, header `Api-Key`, multipart form data.

Both endpoints take `dry_run` as a query parameter, which validates and prices the request without generating or billing. Use it instead of quoting a price. The per-image price list is on [Ideogram's API pricing page](https://ideogram.ai/pricing/?pricing_tab=api), which we could not read as text, so no figures are given here.

`POST /v2/image/generate/ideogram-4-5`. Supplying `images` turns the request into an edit. The first image is edited, the prompt is the edit instruction and the rest are references. The page does not say how much weight each carries.

| Field | Values | Use |
| --- | --- | --- |
| `prompt` | Required | Plain language or structured JSON |
| `images` | Up to 5, 25MB each | See above. Aspect ratio 1:6 to 6:1 |
| `mask` | Black edits, white keeps | Same size as the first image, must contain both. Allows three other images at most, and `size` cannot be set |
| `size` | `auto`, `source`, `WIDTHxHEIGHT` | With no images, presets only and `source` is rejected. With images, `source` follows the first image. Up to 1024x1024 bills as 1K, above that and `auto` as 2K |
| `magic_prompt` | `auto` default, `on`, `off` | `off` keeps your wording. Images always convert it to a structured edit |
| `quality` | `very_low`, `medium`, `high` | Defaults to `medium` with images, `high` without. `very_low` needs images |
| `seed`, `num_images` | | Seed and count |
| `background` | `auto`, `opaque`, `transparent` | Transparent returns alpha |
| `async`, `webhook_url` | | Poll `GET /v2/generations/{generation_id}` |

`POST /v2/image/precise-edit/ideogram-4-5` copies unchanged pixels from the source.

| Field | Values | Use |
| --- | --- | --- |
| `image` | Required, 50MB, up to 8192x8192 | The only image edited |
| `reference_images` | Up to 4, or 3 with a mask | Guide the edit, never edited |
| `mask` | Black edits, white keeps | As above |
| `context_window` | `none` default, `auto`, `y_min,x_min,y_max,x_max` | `none` edits the whole image and scales anything above 2048x2048 down to fit. `auto` needs a mask. With `auto` or a region, only that region changes and the output keeps full size |
| `quality` | The page names `very_low` and `high` | The only field that changes the price |
| `prompt`, `seed`, `num_images`, `async`, `webhook_url` | | Plain language or structured JSON |

## GPT Image

Checked 2026-11-04 against OpenAI's [image generation guide](https://developers.openai.com/api/docs/guides/image-generation) and [pricing](https://developers.openai.com/api/docs/pricing#image-generation). `POST https://api.openai.com/v1/images/generations` and `POST https://api.openai.com/v1/images/edits`. The guide says API organization verification may be required. Our traits were observed on the 2.5 generation. The 2.6 models are untested here.

| Field | Values | Use |
| --- | --- | --- |
| `model` | `gpt-image-2.6-sunburst`, `gpt-image-2.6-flare`, `gpt-image-2.5-sunburst`, `gpt-image-2.5-flare` | Sunburst favours editing precision, Flare favours speed. Same listed price |
| `image` | Several, on edits. The guide's example uses four | The maximum is unverified |
| `mask` | Same format and size as the image, with an alpha channel, under 50MB | Applies to the first image. OpenAI says masking is prompt-based and may not follow the exact shape. Which areas get edited is not stated in that section, so confirm on a sample |
| `size` | `1024x1024`, `1536x1024`, `1024x1536`, `auto` recommended | Custom sizes on 2.6 need multiples of 16, ratio 1:3 to 3:1, no edge above 3840. Above `2560x1440` is experimental |
| `quality` | `auto` default, `low`, `medium`, `high`, `xhigh`, `max` | |
| `n` | | Number of images. The maximum is unverified |
| `background` | `auto`, `opaque`, `transparent` | Transparent needs `png` or `webp` |
| `moderation` | `auto` default, `low` | |
| `output_format`, `output_compression` | `png` default, `jpeg`, `webp`, and on generations `svg`, `gif`. Compression 0 to 100 for `jpeg` and `webp` | |
| `complexity` | `low`, `medium`, `high` default | The guide warns that higher values can add latency and unwanted changes |

Listed price on the check date, per million tokens, was $8 image input, $30 image output and $5 text input for all four models. Use the calculator in the guide for a per-image estimate.
