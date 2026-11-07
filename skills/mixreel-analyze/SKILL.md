---
name: mixreel-analyze
description: Analyze a reference ad and target audio for time-labelled evidence about the hook, pacing, cuts, on-screen copy, music, and style. Use when a reference video or track should inform a new product spot. Does not write the script or generate media.
---

# Analyze a reference ad

Pipeline stage 1. The map is [pipeline](../mixreel/references/pipeline.md). You are here to gather time-labelled evidence. You do not clone the film, write the script, or generate media.

## When

Use this when the user supplies a reference video, a URL they are allowed to use, or a music track. With no reference, this stage has nothing to do. Say so in one line and carry on with [script](../mixreel-script/SKILL.md), or with whatever else the user asked for. Skipping this stage does not end the job. Do not invent timings, and do not go looking for someone else's ad. If the user asked for nothing but an analysis and gave you no file, ask for the file.

Missing target audio does not block visual analysis. Reuse an existing `reference-analysis.md` after you check its source, version, and coverage. If the user did not ask you to continue, stop when the analysis file is written.

## Inputs and outputs

| | |
| --- | --- |
| Inputs | The reference or URL, the user's question or what they want to borrow, target audio when supplied, the brief |
| Output | `reference-analysis.md`: source identity, time-labelled observations, what the viewer learns, observed sound and text, the dimensions worth borrowing, confidence |

Borrow structure. Do not copy footage, music, packaging, or words.

## Must follow

- Start by finding the project and its brand layer, as [project](../mixreel/references/project.md) describes, and follow `brand/requirements.md` when it exists.
- Watch the source through its cuts. A frame sample is a frame sample and does not establish movement or timing. A silent pass is a silent pass.
- Follow [frame reading](../mixreel/references/frame-reading.md) for every contact sheet and every extracted frame. Start with the overview, then look at every frame. Notes between images are fine. Cross-check the cut list. If one image is skipped or unreadable, this step is incomplete.
- If the host cannot watch or hear the source, name exactly what you could not observe and mark the result partial. Do not claim you watched a video that was only embedded in a document.
- Record content, script progression, hook, music, edit rhythm and cutting density, copy and caption mechanics, camera or performance, and style separately. Suggestions are not the user's choices. Keep the reference's creative mechanism apart from the new edit's timing.
- Product claims in the reference are not facts about the user's product. Facts come from the advertiser.
- View counts do not prove conversion or explain why a video worked. Record a lyric reveal or a sound-based joke as a link you observed.
- Run the scripts in [analysis scripts](references/analyze-tools.md) before you describe cuts, loudness, or motion. Picture evidence comes before target-audio notes. This stage does not run beside the script or later stages.

## Read next

| When | Open | Leave closed until then |
| --- | --- | --- |
| Now, to see what to write down | [What to record](references/analysis.md) | Script references, prompt files, image-model notes |
| You are about to run a script | [Analysis scripts](references/analyze-tools.md) | Review scripts (`suspects`, `frame_pack.py`, `qa_check.py`) |
| You are reusing a file or unsure an input counts | [Handoffs](../mixreel/references/handoffs.md) | The rest of the shared rules |
| The user asked for a script after this | [Script](../mixreel-script/SKILL.md) | Do not open it while analysis is still the task |
