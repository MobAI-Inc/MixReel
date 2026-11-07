---
name: mixreel-script
description: Write or revise a product-ad script. Builds the idea from what the audience longs for and what they already know, using the project's brand files, and can borrow a reference ad's chosen dimensions. Produces shot-level scenes, exact copy, a sound plan, a reference sheet, and a 3D previs for every multi-shot scene, with no generation.
---

# Script a product ad

Pipeline stage 2. The map is [pipeline](../mixreel/references/pipeline.md). You are here to write a script the user can approve and watch in their head. Do not generate images or video from this skill.

## When

Use this for an ad idea, a hook, a script, or a storyboard-only request, including a revision of an existing script. Do not require a new illustration, a provider account, or a finished production plan.

Before step 1, make the film's folder with `--film` as [project](../mixreel/references/project.md) describes, picking a short name yourself if the user gave none, and start its `BRIEF.md`. A request as short as "write a 20-second script" is enough to start. Fill the brief from the request and the brand files, mark the rest `unknown`, and ask only when the answer would change the script. When the brand context is missing or still the starter text, the one pause is the one [build the brand files](../mixreel/references/project.md#build-the-brand-files) describes. The stop point is the script unless the user asked for more.

## Inputs and outputs

| | |
| --- | --- |
| Inputs | The request, the film brief, the brand layer, any reference analysis, product sources, confirmed appearance, target music |
| Output | `script.md` from [the template](assets/SCRIPT.template.md), and `reference-sheet.jpg` when the project has images for its shots |

A complete script fills every column of its shot table, and has the sound plan and the early feasibility findings. Blocking detail is required when you build a previs, and optional when the shot is a locked-off product or a supplied recording. An outline may leave production fields pending. Final provider bindings, prices, and keyframes stay pending. Do not invent them to satisfy the production validator.

## Must follow

- Start by finding the project and its brand layer, as [project](../mixreel/references/project.md) describes, and follow `brand/requirements.md` when it exists.
- Read one reference when its step below arrives. Do not open the others yet.
- Product facts come from the advertiser. Logos, packaging, product copy, and UI follow [brand fidelity](../mixreel/references/brand-fidelity.md). Read it before you write any of them.
- One message per film unless the user asked for more.
- Build a previs for every scene told in more than one shot in one place, however simple. A single-shot scene, an image shot, and a post shot get none. The rule is in [previs](references/previs.md).
- If reference evidence is missing, ask for access or label the draft limited. Do not make up an analysis.
- Respect known duration limits. Do not invent unknown endpoint capabilities. If the music changes, rebuild the timing and do not quietly replace the approved idea.
- Show the script before any illustration. Do not mark your own review as user approval. Record the script version and the requested next step in the brief. This skill does not submit images or videos, publish, or promise better ad results.
- This stage finishes before video planning, unless the user told you to stop earlier.

## Steps

Open the row you are on. The steps are serial inside this stage.

| Step | Open |
| --- | --- |
| 1. Facts, message, and limits | `brand/brand-context.md`, or build it from [ad script](references/ad-script.md) |
| 2. What the viewer longs for | `brand/audience-taste.md` and `brand/competitors.md`, or [audience](references/audience-taste.md) |
| 3. The idea | [Marketing idea](references/marketing-idea.md) |
| 4. Borrow from a reference, only when there is one | [Adaptation](references/adaptation.md) |
| 5. Shots. Mark each shot video, image, or post | [Storyboard](references/storyboard.md). Post shots also use [product, copy, and UI](references/ad-script.md#product-copy-and-ui-on-screen). Image shots get composition at keyframes |
| 6. Previs, for every scene with more than one shot in one place | [When to previs](references/previs.md), then [how to render](references/previs-render.md) |
| 7. Sound and feasibility | [Early feasibility check](references/storyboard.md#early-feasibility-check) |
| 8. Read the script back and deliver | [Review before delivery](references/ad-script.md#review-before-delivery). Write product or audience corrections back into the brand files, and add this film to `brand/films.md`. When the user approves or rejects the script, update its row and record the reason in `brand/audience-taste.md` |

[Handoffs](../mixreel/references/handoffs.md) is for reusing a file or crossing into the next stage. [Project](../mixreel/references/project.md) is for the brand folder and the film record. After the script is accepted, or the user delegated it, the next stage is [video plan](../mixreel-video-plan/SKILL.md).
