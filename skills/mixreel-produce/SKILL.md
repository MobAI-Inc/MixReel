---
name: mixreel-produce
description: Submit authorized video generation, recover an existing job, edit accepted footage, and export a short with reconciled costs. Also edits local clips with no generation.
---

# Produce the cut

Pipeline stage 6. The map is [pipeline](../mixreel/references/pipeline.md).

## Output

The master, the plan, source ranges, known limits, and costs with actual, estimated, and unknown kept apart.

## Must follow

- Submit through the provider interface in [providers](../mixreel/references/providers.md). Reserve the budget first. See [execution](../mixreel/references/execution.md).
- One group, one submission. Store the task id before you do anything else.
- A screen recording uses [app recording](references/produce-tools.md). It is not a generation job.
- Render with `render_edit.py` only after `validate_plan.py` passes. Validation is structure, not approval.
- Run the quality gate in [production](references/production.md) before you hand the file over. Fix what the edit can fix before you regenerate.

## Read next

| When | Open |
| --- | --- |
| Cutting and the gate | [Production](references/production.md) |
| Commands | [Produce scripts](references/produce-tools.md) |
| A defect | [Review](../mixreel-review/SKILL.md) |
