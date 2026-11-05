# Seedance 2

Open this when the user's config has settled on Seedance and you are planning for it or writing its request. MixReel does not pick a video model for you, and the user can change the model at any time. This file writes nothing and submits nothing. The adapter is `providers/seedance_video.py` in the repository, and the calling order is in [providers](../../mixreel/references/providers.md).

This file holds official facts only. It records no first-hand observations from production, so unlike [MiniMax H3](minimax-h3.md) it has no traits section. Run one sample before you rely on any of it.

## Request parameters

Checked 2026-11-04 against Volcengine Ark's [video generation tutorial](https://ark.volcengine.com/region:cn-beijing/docs/video-generation-tutorial). BytePlus uses its own model ids and pages, which were not rechecked on this date. Model ids are dated, so copy yours from your console.

| Model id | Duration | Resolution |
| --- | --- | --- |
| `doubao-seedance-2-5-260628` | 4 to 30 seconds, or `-1` | 480p, 720p, 1080p |
| `doubao-seedance-2-0-260128` | 4 to 15 seconds, or `-1` | 480p, 720p, 1080p, 4k |
| `doubao-seedance-2-0-fast-260128` | 4 to 15 seconds, or `-1` | 480p, 720p |
| `doubao-seedance-2-0-mini-260615` | 4 to 15 seconds, or `-1` | 480p, 720p |

| Input | Seedance 2.5 | Seedance 2.0 series |
| --- | --- | --- |
| Reference images | 1 to 30 | 1 to 9 |
| Reference videos | Up to 10, 30 seconds in total, 2 to 30 seconds each | Up to 3, 15 seconds in total, 2 to 15 seconds each |
| Reference audio | Up to 10, 30 seconds in total, 2 to 30 seconds each | Up to 3, 15 seconds in total, 2 to 15 seconds each. Must come with an image or a video |

All models list the ratios `21:9`, `16:9`, `4:3`, `1:1`, `3:4`, `9:16` and `adaptive`. On 2.5, editing, extension and first-frame tasks are adaptive only. First or last frame and reference roles cannot be mixed. The tutorial says reference images and videos showing real human faces cannot be uploaded directly, and points to its portrait asset guide, so plan for this before you shoot or pick references.

## Price

Listed on Ark's [model pricing page](https://ark.volcengine.com/region:cn-beijing/docs/model-pricing.md) on 2026-11-04, in yuan per million tokens. Tokens are estimated as (input video seconds + output video seconds) x width x height x frame rate / 1024, and the actual count is the `usage.completion_tokens` the API returns. The page says only successful generations are billed. BytePlus prices were not checked.

| Model and resolution | No input video | With input video |
| --- | --- | --- |
| 2.5, 480p or 720p | 70 | 42 |
| 2.5, 1080p | 77 | 46 |
| 2.0, 480p or 720p | 46 | 28 |
| 2.0, 1080p | 51 | 31 |
| 2.0, 4k | 26 | 16 |
| 2.0 fast, 480p or 720p | 37 | 22 |
| 2.0 mini, 480p or 720p | 23 | 14 |

## Prompt wording

MixReel adds no prompt format for Seedance. Follow the guide for your version, and do not reuse a prompt written for another vendor.

- [Seedance 2.5 prompt guide](https://ark.volcengine.com/region:cn-beijing/docs/seedance-2-5-prompt-guide.md)
- [Seedance 2.0 series prompt guide](https://ark.volcengine.com/region:cn-beijing/docs/seedance-2-0-prompt-guide.md)

The two versions differ on timing. The 2.5 guide says it responds to whole-second timestamps, while 2.0 responds to shot numbers and its guide calls exact time ranges unreliable. Both guides number references by upload order.
