# Execute within the approved scope

Read this before a paid call. A local edit does not need it.

## One version per paid request

One approved request produces one version. Do not ask the provider for several candidates. Options that cost nothing are fine: scripts, previs, edits, and local treatments. A paid comparison happens only when the user asks for that comparison and its maximum charge. A retry after a defect replaces the rejected version.

## Local checks before spending

Run `validate_plan.py`. Confirm the model profile is the one the user authorized, the files are the reviewed versions, and the batch fits the remaining budget.

Read-only analysis, local rendering, and downloads of files you already paid for can proceed. A new provider or a higher budget is a new decision.

## Journal

Use `job_journal.py`, or `providers/workflow.py` when you are calling a bundled adapter.

- Reserve the worst-case approved charge before the request.
- Record `submitting` before the network call.
- Record the task id as soon as it exists.
- Reconcile billing separately from the download.
- A known failure is not proof of a zero charge. Record zero only with evidence.

One generation group is one submission. Timeline shots that reuse its file do not create more paid jobs. A changed prompt, reference, or model is a new request hash.

On restart, `submitting` or `outcome_unknown` means you look the job up. You do not submit it again.

## Recovery

| What you see | Next step |
| --- | --- |
| Authentication rejected | Check the credential without printing it |
| Rate limit | Back off. Retry only if the provider says the job was not accepted |
| Submission timed out | Keep the reservation. Query. Do not send a second copy |
| Still running | Poll the same task id |
| Succeeded, download failed | Download again. Keep the billed amount |
| Creatively rejected | Record the defect and the repair scope before another paid job |
| Output matches the input | Record the pass as ineffective. Change the route before paying again |
| No quote | Get a documented maximum. Unknown is not zero |

## Privacy

Keep originals immutable. Read keys from the environment or the local credentials file. Never ask for a key in chat. Use `redact_export.py` before sharing a JSON log. It removes credential fields and signed URLs. It does not audit prose.

Costs keep their native currency and say whether they are quoted, estimated, or billed.
