# Providers

Read this when the provider is unresolved or you are checking a capability. Credentials are in [local configuration](local-config.md), and only when you need a key.

MixReel does not ship a relay and does not pick a vendor for you. The same creative plan must survive changing the provider. A provider is anything that implements four actions:

| Action | Input | Output |
| --- | --- | --- |
| `capabilities()` | none | modes, durations, resolutions, ratios, reference caps, whether audio is supported, which inputs cannot be mixed |
| `submit(request)` | prompt, model, references, duration, ratio, resolution, audio, seed | task id |
| `status(task_id)` | task id | queued, running, succeeded, failed, or cancelled, plus a file URL or an error |
| `download(url, dest)` | URL and a local path | local file and a SHA-256 digest |

Check the request against `capabilities()` before you reserve budget. Reserve, then submit. Store the task id immediately. Download, then reconcile.

The repository includes two examples that call official public APIs with the user's own key. They live in `providers/` in the clone, not in the installed skills, as [execution](execution.md#journal) explains.

- MiniMax video, environment `MINIMAX_API_KEY`. Optional `MINIMAX_API_BASE` and `MINIMAX_MODEL`.
- Seedance on Volcengine Ark or BytePlus, environment `ARK_API_KEY`. Optional `ARK_API_BASE` and `ARK_MODEL`.

A host tool, a connector, or a documented CLI can stand in for an adapter when it keeps the same contract.

## Before the first paid request

Read the current official documentation or the host's documented integration. Record the source URL or a hash of the local document, and the date you checked. The user's chosen provider and account are authoritative. Do not replace them with a reseller exposing the same model name.

Record these for the profile:

| Field | Meaning |
| --- | --- |
| Provider and model | The service that actually bills, an account alias without credentials, the model id |
| Operations | Generate, edit, region edit, animate, query, download, and quote, as supported |
| Conditioning | Accepted image, video, and audio inputs and roles, ordering, count and duration limits, strict or soft constraints, combinations that cannot be mixed, and generated-sound behavior |
| Parameters | Supported duration range and steps, multi-shot support, size, aspect ratio, quality, count, and accepted prompt format |
| Region edit | Mask polarity, alpha meaning, and size requirements |
| Billing | Quote mechanism, currency, minimum billable duration and rounding, per request or per second, estimate or actual, chargeable failures, and cancellation |
| Recovery | Task id, lookup and idempotency support, timeouts, rate limits, and concurrency |
| Authorization | Credential source name and endpoint allowlist. Values stay in the environment or the credentials file |
| Output | Status states, artifact fields, expiry, and download verification |

Unknown fields stay unknown. Leave out unsupported parameters and report what that changes creatively. A documentation example is not proof that every parameter reaches the model.

## Submission and recovery

Before `submit`, create a journal reservation with the approved request hash, provider, model, operation, quote, and maximum authorized charge. Count batch members and trials one by one. A quote is read-only only when it is documented that way. Never try an undocumented dry-run flag on a live paid endpoint as if it were safe.

No automatic paid fallback. A documented non-acceptance can permit a retry within the same authorization. An unknown submission outcome stays reserved until a lookup or the vendor's support settles what happened. A failed download is a download retry, never a generation retry.

## Model notes

What each model tends to do, as recommendations and not a choice made for you, is in [image models](../../mixreel-keyframes/references/image-models.md), [MiniMax H3](../../mixreel-video-plan/references/minimax-h3.md), and [Seedance 2](../../mixreel-video-plan/references/seedance-2.md). Their request parameters are in [image model parameters](../../mixreel-keyframes/references/image-model-params.md) and in those video files. They describe the vendor's own API. Model ids belong in the user's config. The files record the ids they were checked against and the date of that check. Do not treat old prices or fixed concurrency limits as global facts.

Choose the H3 or Seedance prompt notes after the endpoint is verified. They are authoring rules, not API clients. If the host has its own prompt skill for the chosen model, read it only after the model is chosen and keep the approved scene. If that skill changes the shot plan, resolve the conflict explicitly. Its existence does not authorize generation.

Reference audio, when the official docs allow it, can carry a voice. First-frame inputs and reference inputs cannot share a request on either of those APIs. Independent shots can be separate requests. Connected shots stay in one request when the provider accepts that length.

## Adding a vendor

Follow the same four actions and keep the key in the user's environment. Do not add a default host you operate. A contributed adapter needs links to official sources, dated capability evidence, mocked request and response tests, safe quote behavior, and recovery from an ambiguous submission. Never ship credentials, signed URLs, or customer assets as examples.

Gemini, if used at review, is a hint. It is not a generation provider and it does not pass or fail the cut. See [review tools](../../mixreel-review/references/review-tools.md).
