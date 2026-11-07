# Execute within the approved scope

Read this before a paid call. The stage order is [the pipeline map](pipeline.md). A local, unpaid edit does not need it. `<mixreel>` below is the installed `mixreel` skill folder.

## One version per paid request

Paid image and video generation hands the user one version per approved request. Do not ask the provider for several candidates, alternate prompts, or competing models for the user to choose from, and keep any count parameter at one. Offer options where they cost nothing: script directions, plans, previs, edits, and local treatments. For images, you may compare candidates on one frame inside the authorized budget to choose a model or setting for yourself, as [image models](../../mixreel-keyframes/references/image-models.md#compare-and-calibrate) describes. Record each attempt and report what it cost. For video, every paid comparison, whether of resolution, motion risk, or model, runs only when the user asks for it and names its maximum charge, as [planning](../../mixreel-video-plan/references/planning.md#comparisons) describes. The same holds for any image comparison the user would have to judge. A retry after a defect replaces the rejected version. It is not an extra option.

## Local checks before spending

Run `validate_plan.py` on the machine plan. Complete the separate creative reviews in the brief. Confirm the chosen model profile matches the provider and account the user authorized, the referenced files are the reviewed versions, all role bindings are ordered, and the batch fits the remaining budget.

Read-only analysis, local rendering, and downloads of files you already paid for can proceed within the task's authorization. Paid generation needs the creative approvals that apply and recorded spending authority. Do not ask again if the user already authorized the exact stage and limits. A new provider, a changed script, or a higher budget is a new decision.

## Journal

Use `<mixreel>/scripts/job_journal.py`, which the installed skills include. The bundled MiniMax and Seedance adapters and `providers/workflow.py` are not installed with the skills. They live in the `providers/` folder of the MixReel clone the skills were installed from. Ask the user where that clone is, or to clone the repository again, and run them from its top folder, for example `python3 -m providers.minimax_video capabilities`. `providers/workflow.py` does the reserve, submit, and record steps below for those adapters. Without a clone, use `job_journal.py` with the tool the user already calls the vendor with.

- Reserve the worst-case approved charge before the request.
- Record `submitting` before the network call.
- Record the task id as soon as it exists.
- Record generation success before the download.
- Reconcile billing separately from the download.
- A known failure is not proof of a zero charge. Record zero only with evidence. Image work can be billed even when the download or local processing fails.

The journal helper makes no network calls and cannot stop a separate client from bypassing it. Whoever submits must follow these steps.

For video, one generation group is one submission. Timeline shots that reuse its file do not create more paid jobs. Include the group id, the ordered shot plan, the requested duration, and every accepted image, video, and audio binding in the request hash. Keep the billed duration separate from the duration kept in the edit.

One journal is shared across the project's workers. The helper uses a local exclusive lock and atomic replacement. Network filesystems and distributed workers need a transactional shared store instead. Never split the same budget into several journals.

A prepared job may be submitted once. On restart, `submitting` or `outcome_unknown` means the outcome is unknown. Look the job up through the provider. Do not submit it again just because the task id was not saved. With provider-supported idempotency, reuse the original key. Otherwise wait for reliable evidence. Keep unknown costs reserved.

A changed prompt, reference, or model is a new request hash and a new job version. A variation the user explicitly authorized can reuse the same content hash on purpose, but needs an override reason so an accidental duplicate can be told apart.

The request file used for hashing holds the prompt, parameters, account alias, and the ordered content hashes or stable asset ids of the references. Keep temporary signed URLs and credentials out of that file, so renewing a URL cannot disguise a duplicate request. Check that the submitted request matches this record.

## Recovery

| What you see | Next step |
| --- | --- |
| Authentication rejected | Check the credential and the service's error details without printing the key |
| Rate limit | Back off as the provider says. Retry only if the provider says the job was not accepted |
| Submission timed out | Keep the reservation. Query or reconcile. Do not send a second copy |
| Still running | Poll the same task id within documented limits |
| Succeeded, download failed | Download the existing output again. Keep the billed amount |
| Creatively rejected | Record the defect and the repair scope before another paid job |
| Output identical or nearly identical to its input | Record the pass as ineffective with the measured difference, keep the billed amount, and change the route before paying again |
| No quote | Get a documented maximum and the authority to spend it. Unknown is not zero |

## Privacy and release

Keep originals immutable. Store derivatives and logs in the project folder, outside the skill source. Read keys from the environment or the local credentials file. Never ask for a key in chat. Keep raw responses that carry secrets private.

Before sharing a log, make a sanitized copy:

```sh
python3 <mixreel>/scripts/redact_export.py INPUT.json OUTPUT.json
```

It removes credential fields and signed or token-bearing URLs. It does not audit prose, binary files, or credentials it does not recognize. Inspect the copy before you share it. Never export whole configuration folders or `.env` files.

Costs keep their native currency and say whether they are quoted, estimated, or billed. Convert only with a recorded rate and date. Report the cost of kept outputs and of discarded attempts separately, and include shared inputs in the kept output's cost. Unknown amounts stay visible.
