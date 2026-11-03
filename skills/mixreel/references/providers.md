# Providers

MixReel does not ship a relay and does not pick a vendor for you. A provider is anything that implements four actions:

| Action | Input | Output |
| --- | --- | --- |
| `capabilities()` | none | modes, durations, resolutions, ratios, reference caps, whether audio is supported, which inputs cannot be mixed |
| `submit(request)` | prompt, model, references, duration, ratio, resolution, audio, seed | task id |
| `status(task_id)` | task id | queued, running, succeeded, failed, or cancelled, plus a file URL or an error |
| `download(url, dest)` | URL and a local path | local file and a SHA-256 digest |

Check the request against `capabilities()` before you reserve budget. Reserve, then submit. Store the task id immediately. Download, then reconcile.

The repository includes two examples that call official public APIs with the user's own key:

- MiniMax video, environment `MINIMAX_API_KEY`. Optional `MINIMAX_API_BASE` and `MINIMAX_MODEL`.
- Seedance on Volcengine Ark or BytePlus, environment `ARK_API_KEY`. Optional `ARK_API_BASE` and `ARK_MODEL`.

Model ids belong in the user's config. The examples document the ids they were checked against and the date of that check. They are not a price list and they are not a private prompt format.

Reference audio, when the official docs allow it, can carry a voice. First-frame inputs and reference inputs are mutually exclusive on both of those APIs. Independent shots can be separate requests. Connected shots stay in one request when the provider accepts that length.

To add another vendor, follow the same four actions and keep the key in the user's environment. Do not add a default host you operate.

Gemini, if used at review, is a hint. It is not a generation provider and it does not pass or fail the cut. See [review tools](../../mixreel-review/references/review-tools.md).

Local configuration is [local configuration](local-config.md).
