# Pipeline map

Read this when you are choosing where to work, or when a stage finishes and you need the next file. Then open only that row's `SKILL.md`. Do not open the next stage's references until this stage's deliverable exists, or the user told you to stop or to skip.

The stages stay in this order. Speed up inside the current stage. Do not speed up by running stages at the same time. Video plan is one stage with two visits: groups before keyframes, prompts after the assets exist. Do not submit clips on placeholder prompts.

| Order | Stage | Open | Stop when you have |
| --- | --- | --- | --- |
| 0 | Brand files, once per brand | [Build the brand files](project.md#build-the-brand-files) | `brand/brand-context.md` the user has read |
| 1 | Reference analysis, when the user supplied a reference | [Analyze](../../mixreel-analyze/SKILL.md) | `reference-analysis.md` |
| 2 | Script and previs | [Script](../../mixreel-script/SKILL.md) | `script.md`, and previs stills for every scene with more than one shot in one place |
| 3 | Video plan, before images | [Video plan](../../mixreel-video-plan/SKILL.md) | groups, frame needs, `continues_from` |
| 4 | Keyframes | [Keyframes](../../mixreel-keyframes/SKILL.md) | accepted images and the input manifest |
| 5 | Video plan, prompts | the same video-plan skill, second visit | one submit-ready prompt per approved group |
| 6 | Clips and the edit | [Produce](../../mixreel-produce/SKILL.md) | the assembled master |
| 7 | QA and review | [Review](../../mixreel-review/SKILL.md) | `review.md`, then the one stage a finding names |

A row with nothing to work on is skipped, and the job carries on at the next row. With no reference video or track, for example, go straight to the script. An existing adequate artifact can satisfy an input. Do not rerun a stage only because this map lists it. Stop at the deliverable the user asked for.

## One file per shared rule

Open the file when the row applies. Do not copy the rule into another note.

| Rule | Source | Open it when |
| --- | --- | --- |
| This order, and that stages stay serial | this file | You are choosing what to do next |
| What counts as an accepted input | [Handoffs](handoffs.md) | You are reusing a file or crossing a stage |
| Project folder and brand layer | [Project](project.md) | You are starting any stage |
| Brief, journal, and plan | [Records](records.md) | You are writing one of them |
| Logos, packaging text, product copy, UI | [Brand fidelity](brand-fidelity.md) | The work shows or describes a client mark |
| How to look at stills | [Frame reading](frame-reading.md) | You are about to read frames instead of watching |
| Which image model fits a step | [Image models](../../mixreel-keyframes/references/image-models.md) | Before any image generation or edit |
| Which groups may be submitted together | [continues_from](../../mixreel-video-plan/references/planning.md#continues_from) | You are writing groups or submitting them |
| How wide a repair is | [Diagnosis](../../mixreel-review/references/diagnosis.md) | Something failed and you are deciding what to change |
| Spending, recovery, privacy | [Execution](execution.md) | Before a paid call |
| Provider capabilities | [Providers](providers.md) | The provider is unresolved, or you are checking a capability |
| Credentials | [Local configuration](local-config.md) | You need a key or a private config path |

Inside a stage, the stage's own `SKILL.md` says what may run together. Across stages, nothing does. A rework follows [diagnosis](../../mixreel-review/references/diagnosis.md): it changes only what needs changing.
