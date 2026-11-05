# Render a previs

`<mixreel-script>` below is this installed skill's own folder, the parent of this `references` folder. Replace it with the real path.

Scene files are JSON. Metres, Z up. The format is the docstring of `<mixreel-script>/scripts/previs_scene.py`.

Examples:

- `<mixreel-script>/assets/previs-scene.example.json`, a counter handoff
- `<mixreel-script>/assets/previs-product-orbit.example.json`, a bottle orbit with no people

```sh
python3 <mixreel-script>/scripts/previs.py SCENE.json --out previs/ --backend raster
```

`--backend auto` uses Blender when `blender` is on `PATH` or `$BLENDER` is set. If Blender is missing, auto stops and tells you. It does not download anything. `--backend raster` needs `numpy` and `Pillow` and marks every still as rough. `--backend bpy` downloads Blender's Python package and needs an explicit yes from the user.

Outputs:

- `plan.png`, a top view
- start and end stills per shot
- `storyboard.png` and `review.png`
- `previs.json` naming the backend

Read the stills with [frame reading](../../mixreel/references/frame-reading.md). If a hand covers the label or a move crosses the line, fix the scene file before you write keyframes.
