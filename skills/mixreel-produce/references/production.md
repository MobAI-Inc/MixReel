# Production

Assemble the film the user will watch. Review generated footage inside that cut, not as loose clips. Play each returned file from start to end, including cuts inside the file.

## Edit

`plan.json` is the edit. Version 3 holds overlays, per-shot audio, and local recordings. Put logos, captions, and UI on overlay tracks or on the recording. Do not ask the video model to draw them.

A repair of one shot regenerates that shot, or replaces its picture, and keeps the original sound and the edit grid unless the user asked to change them.

## Quality gate

Run `qa_check.py` with the plan. It reports flash and black frames, flicker, cut offset, missed cuts, off-beat cuts, short shots, silence, loudness, peak, and frame size. Then run `frame_pack.py` when a suspect needs eyes. Read every image under [frame reading](../../mixreel/references/frame-reading.md).

Suspects are places to look. Your note says what you watched and what you did not.

A late cut is not a pass. Report what remains, each with a repair and whether it costs money.

## Delivery

Watch once without the notes and once with the sound. Creative problems and technical problems stay in separate lists. Hand over the file only if the user asked for that path. Include the plan, the export settings, and the costs.
