# Previs

A previs is a blocking pass. It answers whether the hand covers the label and whether the camera crosses the line. It is not the finished picture.

The script skill builds one for every scene told in more than one shot in one place, such as a product orbit, a hand entering to open or pour, or several angles that must share one layout. Skip it for a single locked-off pack shot or a recording you already have.

## Render

```sh
python3 skills/mixreel-script/scripts/previs.py \
  skills/mixreel-script/assets/previs-product-orbit.example.json \
  --out /tmp/previs --backend raster
```

`--backend auto` selects Blender when the executable is on `PATH`, `$BLENDER` points at it, or it is in the usual install folders such as `/Applications/Blender.app`. If Blender is missing, auto stops. It does not download a package. `--backend raster` uses `numpy` and `Pillow` and labels the stills as rough. `--backend bpy` downloads Blender's Python module through `uv` and should be a decision you make on purpose.

You get `plan.png`, start and end frames, `storyboard.png`, `review.png`, and `previs.json`. With Blender, `--save-blend` also writes `previs.blend`, the whole film on one timeline with a camera switch at each cut.

The other sample, `previs-scene.example.json`, is a counter handoff with two stand-ins. Geometry tests use it. The orbit sample is the one the quickstart renders.

Scene units are metres, Z up. The field list is the module docstring in `skills/mixreel-script/scripts/previs_scene.py`.

Read the stills before you spend money on keyframes. Fix the scene file when the blocking is wrong. Do not prompt your way out of a covered label.
