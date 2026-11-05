# Keyframe diff

`keyframe_diff.py` measures whether a paid edit changed the pixels. `<mixreel>` below is the installed `mixreel` skill folder, next to this skill's own folder. Replace it with the real path.

```sh
python3 <mixreel>/scripts/keyframe_diff.py frames/
```

Put `before.png`, `after.png`, and `manifest.json` in a folder per frame. The manifest records the model id, the prompt, and the reference files. The report lists changed and unchanged ids. Unchanged means the repair did nothing. Keep the billed amount and do not repeat the same request.

The script needs `Pillow`. It does not call a provider.
