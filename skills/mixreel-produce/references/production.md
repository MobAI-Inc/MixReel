# Production

You are cutting and delivering. The stage card is [the produce skill](../SKILL.md). Render commands are in [produce scripts](produce-tools.md). Open that file when you are about to render or run the quality gate.

Assemble the film the user will watch. Review generated footage inside that cut, not as loose clips. Play each returned file from start to end, including cuts inside the file.

## Edit plan

`plan.json` is the edit. Version 3 holds overlays, per-shot audio, and local recordings.

Keep a satisfactory generated sequence intact wherever its actual timing fits. For timeline shots drawn from one result, use the same source asset with observed in-points and its full duration. Do not regenerate those shots just to get separate files. Avoid replaying or skipping action at joins that share a source. A repair of one shot regenerates that shot, or replaces its picture, and keeps the original sound and the edit grid unless the user asked to change them. Record both sources for that interval.

Record each clip's source in-point, source duration, output interval, playback speed, and transition. For a clip with speed `s`, source accent `a`, target accent `T`, and timeline start `t`, use `clip_in = a - s * (T - t)`. Then check that the selected range exists. A negative in-point means the edit needs changing, not silent clamping.

Put cuts and reveals on chosen musical events. Keep reactions readable and the ending coherent. Not every beat needs an event. Mark intentional off-beat cuts. Dissolves consume overlap and need handles. Model them explicitly so they do not shorten the film unexpectedly. Retiming limits follow the scene and acceptable motion, not a fixed universal percentage. Keep synchronous sound in time when retiming, or leave out unusable sound deliberately.

Composite exact UI, captions, logos, and brand layers on overlay tracks or on the recording, over the interval reserved for them. Do not ask the video model to draw them. Follow [brand fidelity](../../mixreel/references/brand-fidelity.md): prefer the real client asset in that overlay over a generated mark. Keep live footage under partial overlays, and use a held or blurred frame only where the product screen covers the picture. Keep score and sound continuous through the overlay. Interface sounds sit on top.

Frame holds, such as twelve distinct drawings per second played at twenty-four frames per second, give a hand-drawn cadence. Offer or use this according to the recorded preference. Compare motion and cut timing after applying it. It is an editing treatment, not a reason to regenerate acceptable footage.

## Quality gate

Render a quality master and a mobile-friendly preview. The render command, what plan versions 1, 2, and 3 keep, and the audio check are in [produce scripts](produce-tools.md). Any other editing tool on the host is equally valid. Check duration, frame size, aspect ratio, frame rate, audio coverage, silence, clipping, cut boundaries, and encoding quality. Then listen. Intended silence is not an automatic defect.

Run the gate before each delivery and fix what editing can fix first. `qa_check.py` with the plan reports flash and black frames, flicker, cut offset, missed cuts, off-beat cuts, short shots, silence, loudness, peak, and frame size. Then build the frame pack, every time, and read every image under [frame reading](../../mixreel/references/frame-reading.md). Compare detected cuts with the plan, look for runs of a few frames from a neighbouring shot, inspect every continuation seam, listen for score the plan did not ask for, and find each spoken line in its intended shot. How to read the pack is in [video inspection](../../mixreel-review/references/video-review.md). Suspects are places to look. Your note says what you watched and what you did not.

Dialogue placement still needs listening. Generated lines can land late, so trim from where a line measurably sits, never from its planned time. Spoken lines come from the model's synchronized audio or a real recording. Text-to-speech is at most a marked placeholder.

A late cut is not a pass. Any review fail, or a cut that visibly leaves the script or the continuity of a person or product, is not a finished deliverable. Fix it within the authorized budget, or stop and ask. Reporting an unresolved issue is not delivery. When you stop and ask, name each repair and whether it costs money.

## Delivery

Export for the channels the user named: a master plus one version per platform, meeting its resolution, duration, and loudness targets, with captions, logo, and UI clear of the platform's own interface overlays.

When an edit-only choice is still open, such as two music candidates, two openings, or frame holds against motion blur, deliver the recommended version with labelled variants instead of stopping to ask. Variants come only from edit-layer choices, never from extra paid generation, and they double as test material. Each version carries a short note of what changed since the previous one.

Watch once without the notes and once with the sound. Creative problems and technical problems stay in separate lists. Hand over the file only to a location the user authorized. Include the plan, the accepted references, the export settings, and the costs, with estimates kept visibly apart from billed amounts.
