---
name: mixreel
description: Route a product or ad video, or build the brand files for a new brand. Open the pipeline map first, then only the current stage. Stages stay in order and can also be invoked alone.
---

# MixReel

You are the router for an ad or product short. Stop at the requested deliverable. Read the brief, accepted artifacts, and job journal before you choose where to resume. The latest user instruction overrides an older record. Invalidate only the work that depends on it.

This edition is for ads, e-commerce, and product video. It does not have a story mode.

## Read this next

Open [the pipeline map](references/pipeline.md) and follow the row you are on. Do not open other stages' references from this page.

| If you already know the stage | Open |
| --- | --- |
| Brand files only | [Build the brand files](references/project.md#build-the-brand-files) |
| Reference analysis | [Analyze](../mixreel-analyze/SKILL.md) |
| Script and previs | [Script](../mixreel-script/SKILL.md) |
| Video plan | [Video plan](../mixreel-video-plan/SKILL.md) |
| Keyframes | [Keyframes](../mixreel-keyframes/SKILL.md) |
| Clips and the edit | [Produce](../mixreel-produce/SKILL.md) |
| QA and review | [Review](../mixreel-review/SKILL.md) |

A host without skill dispatch opens the linked `SKILL.md` and follows it. An existing adequate artifact can satisfy an input. Do not rerun a stage only because another skill did not create it.

## Must follow

- Find the project and its brand layer before anything else, as [project](references/project.md) describes.
- Stages stay in the map's order. Batch only inside the current stage.
- Client marks follow [brand fidelity](references/brand-fidelity.md).
- A repair follows [diagnosis](../mixreel-review/references/diagnosis.md). It changes only what needs changing.
- Show the script before illustrations, one sample before an image batch, and the groups plus references before video submission. A machine check is not human approval.
- Before any image call, read [image models](../mixreel-keyframes/references/image-models.md). It gives recommendations and starting points. The model stays the user's choice.
- Generation and editing may use different providers. Make one sample before a batch. Do not bake a private model route into the plan.
- Proposed creative choices stay proposals until the user approves them or has delegated that choice.

## Shared files

- [Handoffs](references/handoffs.md) and [records](references/records.md). A new project starts from [the brief](assets/BRIEF.template.md). The project folder and its brand layer are in [project](references/project.md).
- [Execution](references/execution.md), [providers](references/providers.md), and [local configuration](references/local-config.md) before a paid call.
- [Frame reading](references/frame-reading.md) before you judge stills.
- [Plan example](assets/plan.example.json) is a synthetic timing fixture, not a script the user must fill in.

Shared scripts are in `scripts/` next to this file, wherever it was installed. When a stage file writes `<mixreel>/scripts/...`, `<mixreel>` means this folder. Keep project outputs outside the skill source. The default tools analyze media, fit beat grids, validate plans, render edits, check a finished edit, pack review frames, diff keyframe versions, journal spend, initialize blank configuration, redact exports, and wrap an app recording. None of them submits a paid model job. Optional CLIP, DINOv2, face match, SyncNet, and Gemini stay off until [review tools](../mixreel-review/references/review-tools.md) says the task may call them.

Finish only after you have inspected the requested artifact, reported anything untested, and reconciled any paid work.
