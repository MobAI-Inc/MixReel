# Project records and continuation

Read this when you are writing the brief, the journal, or a plan. The project folder and its brand layer, including where it lives and how it is created, are in [project](project.md). The stage order is [the pipeline map](pipeline.md). A film folder inside the project typically holds:

```text
<film>/
  BRIEF.md
  reference-analysis.md
  script.md
  previs/
  video-plan.md
  keyframes/
  journal.json
  plan.json
  master.mp4
  review.md
```

## Files and authority

Keep each decision in one place.

| File | Holds |
| --- | --- |
| `brand/` files | Product facts and claim limits, standing requirements, audience taste, competitor evidence, and the record of films, shared across films |
| `BRIEF.md` | This film's intent, where its sources came from, creative choices, review decisions, the next action |
| `plan.json` | Timed shots, reference roles, keyframe ids, source ranges, and transitions |
| `providers/` | Verified service capabilities and this project's parameter mappings |
| `journal.json` | The life of each paid job, reservations, and billing evidence |
| `media/` | Generated or downloaded files, never edited in place, addressed by version or hash |
| `review.md` | Visual and meaning findings tied to artifact versions, and delivery checks |

Start `BRIEF.md` from [the brief template](../assets/BRIEF.template.md). The brief points at the other records and does not copy them, or a private catalog, into the chat. The latest user instruction overrides an older brief. Update the brief instead of silently following a stale approval. Write which artifact version an approval covers, who approved it, its scope, and where the evidence is. Agent review is labelled agent review, never user approval.

Record, as they become known:

- the message, the audience, the length, the aspect ratio, and the ask
- what was borrowed from a reference, and what was excluded
- provider, model id, and account alias (never the key)
- generation groups, keyframes that are new versus reused, and duration asked versus duration kept
- quoted, estimated, and billed amounts in their own currencies
- review decisions: pass, fail, or not checked, with the artifact version

Unknown amounts stay unknown. Do not turn a blank quote into zero. Generation records are one row per paid request: group id, task id, request hash, state, and where the file landed. The journal script is the ledger. The prose record explains the creative choice.

## Stage artifacts

Read [handoffs](handoffs.md) for entering a stage on its own and for each stage's output. `reference-analysis.md`, `script.md`, `video-plan.md`, and `keyframes.md` are default names. Keep suitable names the project already uses. Link versions and review states from the brief. Borrowing dimensions and the advertiser's claim evidence belong in the brief and script. The roles of media actually submitted belong in the asset list and job manifests. A script-only task does not need a complete production plan.

## Plan shape

[The bundled example](../assets/plan.example.json) uses version 2 and passes `validate_plan.py`. A version 3 example covers sound, overlays, local recordings, and continuations. Version 1 plans stay readable with their original per-shot keyframe requirements. Migrate explicitly before using generation groups. The example's durations and names are synthetic. The validator checks timeline and dependency consistency. It cannot judge taste or check that a person or product is recognizable.

`duration` is the target timeline length. `music.duration` describes the source track, and `music.offset` marks the selected excerpt. Musical events are relative to that excerpt. Shots tile the timeline without gaps. `references` is a stable asset list. In version 2 every reference declares `media_type` as `image`, `video`, or `audio`, with its user-assigned `role` and `contribution`. Roles also include `motion`, `timing`, and `sound`. Declaring a role does not prove the endpoint supports it. Shot `bindings` name the references that shot needs. Group `bindings` give the ordered request list and must include every member shot's bindings. Save the image list actually submitted with each job, as described in [images](../../mixreel-keyframes/references/images.md), and reconcile any difference before treating the stage as reviewed. Each shot has a visible scene, a keyframe design, source evidence, camera behavior, and a starting and ending state.

Version 2 requires a nonempty `generation_groups` list. Each entry has a unique `id`, ordered `shot_ids`, `requested_duration` in seconds, ordered reference `bindings`, a `reason` for the grouping or split, and `continuity` describing the spatial and action states to keep. `provider_prompt` is text, or null while pending, and belongs to the group, not to a separate call per shot. Groups cover every generated shot exactly once, in timeline order, without interleaving. The requested duration must cover the group's planned timeline span. Choose a supported duration with the handles you need, and check limits and billing separately in the provider profile.

In version 2, a shot's `keyframe_design` still describes its visual intent, but `keyframes` may be empty or share image ids with other shots. List only planned new images there, each with a reason in the visual design. Existing assets belong in `references`. `illustration_count` counts the unique new image ids across shots, not references, intermediate passes, or paid attempts. The group's image outputs are the union of its members' keyframe ids. Save their stable assets or hashes with the references actually submitted before execution. Report `len(shots)`, `len(generation_groups)`, and `illustration_count` separately. Keyframe review still records whether the selected visual inputs are enough, even when no new image is needed.

The bundled plan shows two editorial shots sharing one generation request with one new keyframe, plus video and audio reference roles. It does not claim any particular endpoint supports those inputs. Record capability evidence, estimated billable seconds, quotes, and retry scope in the provider profile, brief, and journal. Requested seconds are not billed seconds.

`transition.duration` is the overlap leading into the incoming shot. It uses extra source handles, not extra output time. A rendered shot's `clip.in` includes the handle before the transition, and the clip must supply `(shot duration + incoming overlap) * speed` source seconds. `clip.duration` is the total duration of the source file, not the length of the piece you use. The validator checks that `clip.in + (shot duration + incoming overlap) * speed` does not exceed that total. The shot's main event begins after the overlap. The generator may provide more footage. The editor chooses the usable interval.

After generation, member shots in a group use the same `clip.asset` and full source `clip.duration`, each with its own observed `clip.in` and playback `speed`. Keep internal timing intact where it fits, and adjust only from inspected footage. Several excerpts can be rendered from that one file without separate generation jobs. Shot times inside a prompt do not establish these in-points.

`reviews` records creative checks. Pending, approved, and rejected describe the human review state. Passing tests cannot turn a pending review into approved. Costs and authority live in the journal and brief, not in a made-up approval flag in the plan.

## Version 3 additions

[The version 3 example](../assets/plan.v3.example.json) shows the fields below. Version 1 and 2 plans keep their meaning, and a version 3 field in them is an error, not something ignored.

- A shot's `production` is `generated` by default. Set `production: "local"` for an existing locally rendered or supplied clip, such as an app recording. It needs complete `clip {asset, in, duration, speed}` fields. Generation groups cover only generated shots, in timeline order, and an all-local plan uses `generation_groups: []`. Local shots still obey the same timeline, source-range, transition, and sound checks. The renderer checks that clip files exist. Do not fake a model request for a local UI render.
- `music.source` is `track` (the version 2 fields), `generated` when the score comes from the clips' own sound, or `none`. Events may still mark beats on the timeline.
- A shot's `audio` names where its sound comes from: `{"from": "clip"}` by default, `{"from": "asset", "asset", "in", "duration", "speed"}` for another file, or `{"from": "none"}`. A picture-only replacement points `clip` at the new footage and `audio` at the original clip.
- `clip.repair` explains a regenerated single shot. Such a clip is exempt from the rule that a group's shots share one source.
- A shot's `holds` sets distinct drawings per second for that shot, overriding the render option.
- `overlays` place edit-layer images, image sequences (`asset` with a frame pattern plus `fps`), or video from `start` to `end` on the final timeline. Reserve that time inside generated shots instead of inserting extra seconds.
- `sound.ducking` lowers a music track between `start` and `end` by `gain`. `sound.layers` places extra sound files at `at` with an optional `gain`.
- A generation group's `continues_from` names an earlier group and the `tail` seconds of its accepted result used as the continuation reference.

## What to recheck after a change

| Change | Recheck |
| --- | --- |
| Reference, audience, or the feeling aimed for | The idea, the shot plan, and all dependent media |
| Music excerpt or tempo reading | Timing, shot count, edits, and only the media that no longer fits |
| Product, person, or style reference | The affected images and clips, not unrelated analysis |
| A local image correction | That frame and the generation groups using it, plus their clips |
| Generation grouping or reference type | The group prompt, capability checks, duration and cost estimate, and the affected source-to-edit mappings |
| In or out point, or an export setting | Timeline, audio, and export. Do not regenerate images |
| Provider or model | Capability profile, affected prompts, cost, and one representative quality sample |

Query existing jobs before preparing new ones. Keep rejected assets and the reasons, so a resume cannot promote them by accident. Stop at the requested deliverable, including proposal-only or image-only work.
