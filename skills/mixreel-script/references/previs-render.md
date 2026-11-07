# Render a previs

Read this for each scene that [previs](previs.md) says gets one. If the scene gets none, close this file.

`<mixreel-script>` below is this installed skill's own folder, the parent of this `references` folder. Replace it with the real path.

## Render it

Write the scene once as a scene file and render it. Scene files are JSON, in metres, Z up. `--schema` prints the format, which is also the docstring of `<mixreel-script>/scripts/previs_scene.py`. Two complete examples:

- `<mixreel-script>/assets/previs-scene.example.json`, a counter handoff
- `<mixreel-script>/assets/previs-product-orbit.example.json`, a bottle orbit with no people

```sh
python3 <mixreel-script>/scripts/previs.py SCENE.json --out previs/
```

The default `--backend auto` uses Blender when it is installed: on `PATH`, in `$BLENDER`, or in the usual install folders, such as `/Applications/Blender.app` on macOS. Let the script look, because `which blender` misses app installs. When Blender is missing, the script stops and downloads nothing. Ask the user to install Blender, free from blender.org. If they would rather not, ask before downloading its `bpy` package, several hundred MB, and rerun with `--backend bpy` for the same images. That needs `uv`. If they decline that too, or there is no network, use `--backend raster`, which needs only `numpy` and Pillow. It shows positions, occlusion, screen direction, and framing without shadows or depth of field, and marks every still as rough. Call those renders rough whenever you show or use them. Use these fallbacks only when Blender cannot be used.

## Build the blocking scene

Real scale matters more than detail.

- Each named person is a proxy in its own flat colour. Keep the colour legend fixed for the project. The product and the set pieces that matter get real positions, such as a counter, a shelf, a doorway, or a staircase.
- Actors and props move by keys on the film's one timeline, so the end of one shot and the start of the next come from the same scene. Each video shot gets a camera with start and end positions, look targets, and vertical field of view. The frame size follows the delivery aspect ratio.
- Keep the scene file beside the renders as the record of positions, facings, gaze targets, held props, and cameras.

Proxies do not prove faces, gaze nuance, hand contact, or performance. Record those as not checked.

## Review outputs

Render the plan and every video shot of the scene in one pass. It takes seconds, and a shot left unrendered is the one whose staging nobody checked.

- `plan.png` is drawn straight down, with names, movement arrows, and each camera's position and facing.
- Each shot gets a start and an end frame, and `review.png` lays them out with shot ids. `previs.json` names the backend.
- Read the stills with [frame reading](../../mixreel/references/frame-reading.md). Check that the subject is not hidden behind foreground figures, that screen direction and eyelines hold across cuts, what lies behind each subject, where the product and every prop that matters are, and whether each action fits its time. If a hand covers the label or a move crosses the line, that is a problem to fix here.
- Fix problems inside the scene file, for example by moving a camera or opening a gap between people, then render again before you write keyframes.
- With Blender or `bpy`, `--save-blend` also saves `previs.blend`, the whole film on one timeline with a marker at each cut that switches to that shot's camera. The user can scrub it in Blender, and `blender -b previs.blend -a` renders it as a moving preview. The raster backend saves no `.blend`.

## Use the results downstream

- A shot render can be the composition source for a keyframe, in place of a searched or reference-video frame.
- `storyboard.png` lays the rendered shots out in playback order with only a panel number on each. Keep captions, UI, and production notes out of any sheet given to a model.
- When the video endpoint accepts it, the storyboard sheet can be the first ordered reference image. The prompt then states the colour legend and that mannequins, numbers, colours, and grid lines must not be drawn.
- Previs renders supply layout only. Never use them as style or identity references.
