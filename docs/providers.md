# Providers

Generation is a paid call on an account you control. MixReel's side of that call is four methods:

| Method | Role |
| --- | --- |
| `capabilities()` | Durations, resolutions, ratios, reference caps, and inputs that cannot be mixed |
| `submit(request)` | Returns a task id. One request, one version |
| `status(task_id)` | `queued`, `running`, `succeeded`, `failed`, or `cancelled` |
| `download(url, dest)` | Writes the file and returns a SHA-256 |

Check capabilities, reserve the budget in the journal, move the job to `submitting`, then call `submit`. Store the task id before you download. If the call fails after `submitting`, look the job up. Do not send it again.

`providers/workflow.py` does that sequence for the bundled adapters.

## Environment

| Variable | Use |
| --- | --- |
| `MINIMAX_API_KEY` | Official MiniMax video API |
| `MINIMAX_API_BASE` | Optional. Default `https://api.minimax.io`. China-doc examples use `https://api.minimax.cn` |
| `MINIMAX_MODEL` | Model id from your account. Not a default in the request |
| `ARK_API_KEY` | Volcengine Ark or BytePlus |
| `ARK_API_BASE` | Beijing `https://ark.cn-beijing.volces.com/api/v3` or Singapore `https://ark.ap-southeast.bytepluses.com/api/v3` |
| `ARK_MODEL` | Dated model id from your console |
| `GEMINI_API_KEY` | Optional review hints only |

## What was checked

Checked on 2026-11-03 against public docs. Re-check before you depend on a field. CI does not call these APIs.

**MiniMax.** `POST /v2/video_generation` and `GET /v2/query/video_generation/{task_id}` on `api.minimax.io`. Auth is a bearer token. The body is `model`, `content[]`, `resolution`, `duration`, and `ratio`. `content` items are `text`, `image_url`, `video_url`, and `audio_url`, with roles `first_frame`, `last_frame`, `reference_image`, `reference_video`, and `reference_audio`. Text-only calls need a concrete ratio. First/last frame and reference roles cannot be mixed. Documented names on that date included `MiniMax-H3`, `MiniMax-H3-Highspeed`, `MiniMax-H3-Lite`, and `MiniMax-H3-Max`. A succeeded task exposes `task.content.url`.

Create reference: `https://platform.minimax.io/docs/api-reference/video-generation-v2-create`. Query is the page linked from there. China documentation examples use the host `https://api.minimax.cn`. Set `MINIMAX_API_BASE` when your key belongs to that host.

**Seedance.** `POST /contents/generations/tasks` and `GET /contents/generations/tasks/{id}`. Auth is `Authorization: Bearer $ARK_API_KEY`. A succeeded task exposes `content.video_url`. BytePlus's tutorial says that URL is retained for 24 hours. Volcengine's create-task page documents task-id expiry (7 days for an ordinary task). Download as soon as the task succeeds.

Reference audio on the 2.0 series must ship with an image or a video. Seedance 2.5 may send audio alone. First/last frame and reference roles cannot be mixed. Model ids in the docs on the check date looked like `doubao-seedance-2-5-260628` and `dreamina-seedance-2-5-260628`. Copy the id from your console. The date in the id changes.

Docs used: the Ark video-generation tutorial and the BytePlus video-generation tutorial linked from `providers/seedance_video.py`.

## Add a provider

Implement the four methods. Read the key from the environment. Put the model id in the user's config. Do not add a host you operate in the middle. Open a pull request with tests that mock HTTP and never hit the network. See [the provider package notes](../providers/README.md).
