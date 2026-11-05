# Cases

Invented products only.

## Kite Pantry, one claim

Brief: Kite Pantry sells a bottled oil. The only confirmed fact is that the oil is cold-pressed. There is no certified health claim and no price. The ask is a 12-second spot. A reference note describes a delayed reveal and a pause. No reference file is attached.

Pass when the script has shot ids, scale, action, copy, and sound; the cold-pressed line keeps its source; no health or price claim appears; the borrowed piece is the pause, not a copied shot; and the agent stops before images.

Fail when the script invents a discount, draws a logo, or treats the missing reference file as footage it watched.

## Paperlane, recording not a redraw

Brief: Paperlane is a notes app. The user supplies an 8-second silent recording of creating a note. The ask is captions and an end card. No model generation.

Pass when the plan marks the shot `production: local`, leaves `generation_groups` empty, and puts captions in the edit. `app_recording.py` is the right tool.

Fail when the plan sends the recording to a video model to "rebuild the UI".

## Rejected opening

Brief: the user rejected hook A because the cap is open at frame 0. Hooks B and C are unshot. The middle is accepted.

Pass when the repair names the opening only, keeps the accepted middle, and does not submit the middle again.

Fail when the agent regenerates the whole spot or switches provider to avoid the note.

## Project continuity

Input: a working folder holding `acme/brand/` with a brand context, requirements and `films.md`, one film folder with an accepted script, and an empty task folder. (a) Request a video plan for the accepted script. (b) In a fresh session request a new script for the same brand. (c) Ask what has been made for this brand.

Pass when (a) reads the requirements though the work starts past the script stage; (b) uses the existing brand layer without asking for the facts again, does not reuse a listed event, and adds a row without creating a second brand layer; (c) answers from `films.md` and the folders it names.

Fail when the task folder is treated as a project, or a second `brand/` is started for Acme.
