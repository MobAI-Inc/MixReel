---
name: mixreel
description: Route a product or ad video, or build the brand files for a new brand. Open the pipeline map first, then only the current stage. Use for end-to-end work or to resume. Stages stay in order and can also be invoked alone.
---

# MixReel

You are the router for an ad or product short. Stop at the requested deliverable. Read the project's brief, accepted artifacts, and job journal before you choose where to resume. The latest user instruction overrides an older record. Invalidate only the work that depends on it.

This edition is for ads, e-commerce, and product video. It does not have a story mode.

## Read this next

Open [the pipeline map](references/pipeline.md) and follow the row you are on. Do not open other stages' references from this page.

| If you already know the stage | Open |
| --- | --- |
| Brand files only | [Build the brand files](references/project.md#build-the-brand-files) |
| Reference analysis | [Analyze](../mixreel-analyze/SKILL.md) |
| Script and previs | [Script](../mixreel-script/SKILL.md) |
| Video plan, before images or again for prompts | [Video plan](../mixreel-video-plan/SKILL.md) |
| Keyframes | [Keyframes](../mixreel-keyframes/SKILL.md) |
| Clips and the edit | [Produce](../mixreel-produce/SKILL.md) |
| QA and review | [Review](../mixreel-review/SKILL.md) |

A host without skill dispatch opens the linked `SKILL.md` and follows it. No stage requires spawning another agent. Where one helps, such as the fresh read-back of a script, the stage says what to do when the host cannot start one. An existing adequate artifact can satisfy an input. Do not rerun a stage only because another skill did not create it.

## Must follow

- Find the project and its brand layer before anything else, as [project](references/project.md) describes.
- Stages stay in the map's order. Batch only inside the current stage.
- Before any image call, read [image models](../mixreel-keyframes/references/image-models.md). It gives recommendations and starting points. The model stays the user's choice.
- Client marks follow [brand fidelity](references/brand-fidelity.md).
- A repair follows [diagnosis](../mixreel-review/references/diagnosis.md). It changes only what needs changing.
- Show the script before illustrations, one representative sample before an image batch, and the groups, references, and cost before video submission. A machine check is not human approval.
- Generation and editing may use different providers. The plan names the steps and the reasons, and leaves the provider and model to the user's config, so the same plan still works when the user switches.
- Proposed creative choices stay proposals until the user approves them or has delegated that choice. Keep accepted identity, wardrobe, style, and composition choices. Do not ask again.

## Shared files

Open one of these only when the map or the current stage names it. Do not copy budgets or decision records into a stage folder.

- [Handoffs](references/handoffs.md) and [records](references/records.md) for authority and continuation. A new project starts from [the brief template](assets/BRIEF.template.md). The project folder and its brand layer are in [project](references/project.md).
- [Execution](references/execution.md), [providers](references/providers.md), and [local configuration](references/local-config.md) before a paid call or a credential.
- [Frame reading](references/frame-reading.md) before you judge stills.
- [Plan example](assets/plan.example.json) is a synthetic timing fixture, not something a script-only task must fill in.

Shared scripts are in `scripts/` next to this file, wherever it was installed. When a stage file writes `<mixreel>/scripts/...`, `<mixreel>` means this folder. Keep project outputs outside the skill source. The default tools analyze media, fit beat grids, validate plans, render edits, check a finished edit, pack review frames, diff keyframe versions, journal spend, initialize blank configuration and project folders, redact exports, and wrap an app recording. None of them submits a paid model job. Optional CLIP, DINOv2, face match, SyncNet, and Gemini run only at a review or quality-gate step, and only when [review tools](../mixreel-review/references/review-tools.md) says the task may call them. Open that file only at such a step.

Finish only after you have inspected the requested artifact, reported anything untested or unresolved, and reconciled any paid work. A successful generation or a valid file is not creative approval.
