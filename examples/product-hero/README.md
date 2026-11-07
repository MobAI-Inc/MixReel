# Product hero

**Brand (invented):** Kite Pantry, a bottled oil.

**Intended cut:** 9:16, about 12 seconds. Orbit the bottle, a hand sets it down, a lockup with the real label composited in the edit.

<!-- TODO(demo): add master.mp4, previs/plan.png, and qa.json.
     Strip metadata. Do not use a real customer's product. -->

Until that file exists, render the blocking pass locally:

```sh
python3 skills/mixreel-script/scripts/previs.py \
  skills/mixreel-script/assets/previs-product-orbit.example.json \
  --out /tmp/kite-previs --backend raster
```

`plan.json` next to this file is a structural sample for the edit, not a generated spot.
