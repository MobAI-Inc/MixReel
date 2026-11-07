---
name: mixreel-produce
description: Submit authorized video generation, recover existing jobs, edit accepted footage, and export a finished short with reconciled costs. Also handles edit-only cuts from existing clips and wraps app screen recordings. Needs verified provider capabilities before a paid submission.
---

# Produce the cut

Pipeline stage 6. The map is [pipeline](../mixreel/references/pipeline.md). You are here to submit authorized generation, recover jobs, cut, and export. Prompts should already be bound. If they are not, go back to [video plan](../mixreel-video-plan/SKILL.md) instead of inventing them here.

## When

Use this for authorized video generation, a resume of existing jobs, or an edit-only cut from footage you already have. Edit-only work does not need new generation. With no paid authority, deliver the execution plan or do only the local edits that were authorized.

## Inputs and outputs

| | |
| --- | --- |
| Inputs | Accepted script and generation plan, the actual reference assets, the provider profile, the journal. Edit-only: footage and the edit requirements |
| Output | The assembled master and preview, the plan, source ranges, edit settings, known limits, and costs with actual, estimated, and unknown kept apart |

## Must follow

- Start by finding the project and its brand layer, as [project](../mixreel/references/project.md) describes, and follow `brand/requirements.md` when it exists.
- Submit through the provider interface in [providers](../mixreel/references/providers.md), and record the actual model, provider, and parameters. The bundled adapters are in the MixReel clone, not in the installed skills. [Execution](../mixreel/references/execution.md#journal) says how to reach them. A simulated request is not a submitted job.
- One generation group is one submission. Follow [continues_from](../mixreel-video-plan/references/planning.md#continues_from): groups with an empty `continues_from` may be submitted at the same time, and a group that names another waits for that group's accepted result. Only these submissions are batched. Stages stay in [pipeline](../mixreel/references/pipeline.md) order.
- A rework resubmits only the groups that need changing. The scope rule is [diagnosis](../mixreel-review/references/diagnosis.md).
- Reserve each group once, as [execution](../mixreel/references/execution.md) describes. Save the submitting state before the call, then store the task id before you do anything else. On resume, query the existing job. An unknown timeout is not permission to submit again. A failed download retries retrieval only.
- A screen recording uses [app recording](references/produce-tools.md). It is not a generation job.
- Render with `render_edit.py` only after `validate_plan.py` passes. Validation is structure, not approval.
- [Brand marks](../mixreel/references/brand-fidelity.md) are composited from the real asset. The local renderer cannot write captions or design UI. Verify every approved layer survived the render.
- Every delivery is an assembled film. As soon as footage exists, assemble every approved layer, including UI, brand marks, captions, spoken lines, sound, music, and end card. When a required asset is missing, put a marked placeholder in its place and deliver the film as a draft that names the missing asset. It counts as finished only once every required brand, UI, and sound layer is the real one. Loose clips are never the deliverable. Raw clips are attachments when the user asks.
- Run the quality gate in [production](references/production.md) before you hand the file over. Fix what the edit can fix before you regenerate.
- When a film is delivered, update its row in `brand/films.md` with the final file. Delivery to somewhere outside the project needs the user's authorization for that destination.

## Read next

| When | Open | Leave closed |
| --- | --- | --- |
| Now, for the cut and the delivery checks | [Production](references/production.md) | Video prompt files |
| Before a paid call | [Execution](../mixreel/references/execution.md), [providers](../mixreel/references/providers.md), [local configuration](../mixreel/references/local-config.md) | Do not open these for an edit-only cut |
| Footage has returned and you are choosing ranges | [Video inspection](../mixreel-review/references/video-review.md) | |
| You are rendering or running the quality gate | [Produce scripts](references/produce-tools.md), which points at the review commands | Gemini, unless review tools allows it |
| Before you call the film done, or a defect | [Review](../mixreel-review/SKILL.md) | |
| Reusing a file | [Handoffs](../mixreel/references/handoffs.md) | |
