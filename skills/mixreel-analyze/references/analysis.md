# What to record

You are in reference analysis. The stage card is [the analyze skill](../SKILL.md). Open [analysis scripts](analyze-tools.md) when you run a tool. Open [frame reading](../../mixreel/references/frame-reading.md) when you look at stills.

Write times as `MM:SS.sss`. Separate observation from inference.

## Reference evidence

Inspect the actual video, not just its thumbnail or a few middle frames. Get a local copy through a tool the user is allowed to use, and keep the source URL and where it came from in the project records. If access fails, report which observations are missing. Do not invent camera motion from a still.

Cut candidates and time-labelled stills come from the reference command in [analysis scripts](analyze-tools.md). Automated cuts can miss dissolves and slow reveals. Watch each candidate shot and its boundaries. A sequence of stills helps, but cannot prove smoothness or motion direction. Look at every produced still, as frame reading requires. A contact sheet alone is not enough. Use the cut candidates and shot ranges in `analysis.json` alongside the images, and keep the uncertainty where a cut is not confirmed.

Write one row per shot: source time range, subject placement and size, viewing angle, gaze target, camera start, movement and end, subject movement, occlusion, light, transition, what the shot does for the viewer, and how sure you are. Cover how the product or the UI enters. Separate observed movement from inferred technique. A widening view may come from the subject moving away while the camera stays put.

Then say what makes the viewer anticipate the next image. Name the opening question in the first seconds, what changes at each cut, the peak feeling, and what the ending holds back or resolves. Performance data counts only when the user supplied it or it was verified. Aesthetic analysis cannot prove a video's commercial success.

Classify movement per shot as mainly camera, mainly performance, or mixed. This is a production choice, not a demand for uniformly static or uniformly dramatic footage.

## Target music

The target track controls the new timeline. Keep source offsets when you use an excerpt. Honor an excerpt that was already selected. If only a full track is supplied, propose a short excerpt that ends on a complete phrase within the requested duration.

Audio and beat-grid commands are in [analysis scripts](analyze-tools.md). Listen around the events you keep. The kick and hat fields are frequency-band energy estimates, not verified instrument labels. `bar_start` groups the fitted grid using `--bar` (default 4). It does not detect downbeats. A regular fitted grid does not establish where the musical phrase begins. Do not assume every song is four-four, every phrase has eight beats, or every detected transient needs a cut.

Sketch the available visual slots from music events, silence, and the time each action needs. Report timeline shots, generation requests, and unique new images separately. Decide the last two after [grouping the sequence](../../mixreel-video-plan/references/planning.md). Do not equate one beat with one image.

## Dimensions and handoff

Record content and composition, script and information, hook, music and sound, edit rhythm and motion, and style and presentation independently, with source times and uncertainty. Describe pacing and cutting density from the cut list (candidate count over the measured duration, with confirmed and uncertain cuts kept apart), and how changes in captions or on-screen copy create the hook, joke, reveal, or other information pattern. Do not infer spoken content or sound from visible text. Quote copy and any spoken line only when you actually have them. Explain which event changes what the viewer expects. Record what the audience has to know already, and any dependence on lyrics or sound. Do not use a generic label such as viral or cinematic in place of an observation.

The user's intent decides which dimensions to borrow. Suggest options with reasons: what a new spot could borrow (structure, pacing, reveal) and what it must not borrow (identity, footage, claims, brand marks). The script stage records the chosen treatments with [adaptation decisions](../../mixreel-script/references/adaptation.md). Target audio may need new timing without replacing the chosen creative mechanism. Missing audio leaves that part pending.

End with open questions. Do not score the reference and do not promise that a similar structure will perform.

Stop at analysis when that was the request. Script writing maps the chosen functions to new content and timing. Keyframes look for missing composition evidence only after a concrete need exists. Do not search image sites or generate extra images to complete an analysis report.

## Where the note goes

The note goes in the film folder as `reference-analysis.md`. When the user wants the ad kept for this brand, copy the note and its contact sheet to `brand/taste-library/<ad>/`. When the ad is a competitor's, add what it does and what its audience reacts to in `brand/competitors.md`, keeping to what you watched or the user reported.
