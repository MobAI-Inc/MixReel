# Video inspection

You are looking at footage. The stage card is [the review skill](../SKILL.md). Commands are in [review tools](review-tools.md). Open that file when you are about to run one. Look at every `frame_pack.py` image, as [frame reading](../../mixreel/references/frame-reading.md) requires. Start with the overview. Notes between images are fine.

Judge the master, not a pile of selects. Watch each returned sequence through its internal cuts, including the beginning and the end, before you select footage. Check that positions, screen direction, contacts, and action speed stay continuous and that the planned events are present. Compare observed cuts and accents with the plan for that request. Prompt timestamps are not proof of frame-accurate timing. Check identity, rendering, contact, direction, gaze, final state, and camera movement.

Inspect gaze through each clip against the approved targets, especially during turns, looks back, and camera moves that reveal a face. If a person unexpectedly looks into the lens, first try moving the in-point or changing the playback speed to leave that interval out while keeping the required action and timing. Regenerate only if editing cannot avoid it. A finished provider job can still be unusable.

## Order for a cut you are judging

1. Run the suspect scripts in [review tools](review-tools.md), with the small models that file allows for this task. They flag flash, flicker, cut offset, missed cuts, off-beat cuts, silence, loudness, and size. Those are places to look, not a verdict.
2. Build a frame pack every time. It holds the overview, seams, and brand frames, plus bursts around any suspects. Look at every overview and every remaining image. Cross-check the detected and planned cut lists with those images. An overview-only or selected-frame inspection is incomplete.
3. Watch the master with sound when you can. Gemini only when review tools says the environment supports it and the user asked. There is no OCR step.
4. Decide, and write `review.md`. Apply the delivery rule in the review skill before calling the film finished.

A detector time is a place to look. Confirm, reject, or mark uncertain. Pixel defects (a one-frame white flash, a stray frame of the previous shot, a mark that does not match the client asset) are settled on the frames. A line landing in the wrong shot, a look to the wrong place, or a product that never appears are settled on playback, plus Gemini only if it actually ran. If the frames and the playback disagree, write uncertain. Do not force a verdict.

Off-beat means the cut is farther from the measured beat than the tolerance. It is not a taste comment about the track.

`media_inspect.py motion` is the candidate-change list, including flash and flicker peaks. A peak can be a camera move, a flash, or a defect. Inspect the surrounding frames and record the time you observed.

Brand frames are full resolution so a logo at the edge can be compared with the asset. A soft or substituted mark fails. Before delivery, the assembled film also passes the quality gate in [production](../../mixreel-produce/references/production.md).

Keyframe re-review is not this pack. Use [keyframe diff](../../mixreel-keyframes/references/keyframe-tools.md) and its prior-review and requirements checks. Unchanged pixels alone do not establish a pass.
