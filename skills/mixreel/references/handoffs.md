# Handoffs

Read this when you are reusing an artifact or crossing a stage. The order of stages is [the pipeline map](pipeline.md). Do not open it to re-decide a rule that already has its own file.

Install the whole collection so each stage skill can find the shared `mixreel` folder next to it. Invoke only the skill you need. Command examples write that shared folder as `<mixreel>`. Resolve it from where the skills were installed, not from the project's working directory. A missing sibling skill is an installation problem, never permission to invent its rules.

## Accept existing work

Reuse an artifact when it still matches the current brief, whoever made it. An artifact is adequate when all of these are true:

- The user accepted it, or an earlier step recorded it as accepted, and the brief has not changed in a way that affects it.
- Its inputs are still the inputs you would use now.
- A later defect has not been traced back to it.

Keep source paths, ids, and accepted versions. A standalone task needs only its own meaningful inputs. Do not demand a full film plan to review an image or write a script. Do not rerun a stage to make the folder look complete. Do not carry a rejected file forward because it is convenient.

| Stage | Minimum useful inputs | Reviewable output | Not required at this stage |
| --- | --- | --- | --- |
| Analysis | A reference you can access and the scope of the analysis, plus target audio when relevant | `reference-analysis.md`, where the evidence is, uncertainty, optional audio events | Script, keyframes, provider |
| Script | The advertiser's requirements, reference evidence, product facts | `script.md`, borrowing decisions, shot-level descriptions, sound plan, early feasibility | Paid account, generated assets, final verified request settings |
| Video plan | Accepted script or scene, reference roles, available assets, verified capabilities or explicit unknowns | `video-plan.md`, groups and frame needs, final prompts once bindings exist | New images when existing inputs are enough |
| Keyframes | Accepted visual requirement, the list of frames needed, user-chosen references, execution scope | `keyframes.md`, actual images or clearly labelled input plans, the actual input manifest | A whole-film plan or music for a standalone image |
| Produce | Accepted execution and edit plan, actual assets, capabilities, and authority for the requested operations | Jobs, selected clips, edit records, the film | New generation for an edit-only request |
| Review | The actual artifact and whatever target or evidence exists | `review.md`, located defects, repair destination, recheck status | New assets, paid API keys |

These names are defaults for new project records, not a reason to rename existing files. The brief links each artifact's version, acceptance state, and open decisions. Do not duplicate authority or budgets across stage folders. Paid work uses the same project journal. Do not open a second ledger for the same budget.

A keyframe that passed can be reused only when the shot requirements and the references are unchanged. A pixel diff does not approve an image that failed or was never reviewed. A repair that does not change the pixels stays failed.

## From a script to a production plan

Keep a script in Markdown while its production inputs are unresolved. `plan.json` versions 1 and 2 describe a music-based production and edit timeline, and version 3 adds generated or absent score, per-shot sound, edit-layer overlays, local recordings, and continuations. They are not the schema for every creative task. Do not put dummy music or generation groups into a script to pass `validate_plan.py`. For an authorized sound-only or other unsupported edit, record the real plan and use a suitable editor instead of inventing a music track.

A full script already includes a sound proposal and a provisional feasibility check against known limits. Video planning verifies and finalizes these choices. It must not silently repair a script that cannot work after approval. An outline can defer that check explicitly.

When production planning starts, keep the script's shot ids, source locators, action, timing, and approved endings. Add the actual reference list, generation groups, frame requirements, and later clip ranges. Recheck timing against the chosen audio. Keep exact copy, UI, brand, spoken-line, and sound requirements in the linked script or edit-layer plan even when the model prompt or the local renderer cannot express them.

Borrowing dimensions are creative decisions about the reference video. Provider input roles describe what each submitted asset supplies. They are different records: borrowing the reference's hook does not authorize using its frame as a style reference. Check both before submission.

## Ownership and change

The script skill owns the approved creative sequence. Video planning may propose production changes but cannot adopt them silently. Keyframes own image versions, produce owns actual jobs and edits, and review owns findings and rechecks. The router picks the earliest affected stage. A stage skill may do a simple check that belongs next door, but follows that stage's own rules instead of making a competing workflow.

When you cross a stage, name the file you are relying on and the decision it encodes, and say what is actual, proposed, accepted, rejected, or not checked. If that decision is missing, stop and ask, or produce the missing artifact if the user already authorized that stage. An agent check is not user approval. A simulated request is not a paid job. Missing evidence limits the conclusion. It does not automatically mean rerunning every earlier stage.
