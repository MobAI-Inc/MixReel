# Getting started

You need Python 3.10 or newer, `ffmpeg`, and `ffprobe` on `PATH`.

```sh
python3 -m pip install -r requirements.txt
python3 scripts/demo.py
```

The demo is the path with no API key. It renders a rough previs, edits two synthetic clips, and runs QA. The printed directory is the only output.

## Install the skills

```sh
python3 scripts/install.py --destination ~/.agents/skills
```

Seven directories are copied: `mixreel`, `mixreel-analyze`, `mixreel-script`, `mixreel-video-plan`, `mixreel-keyframes`, `mixreel-produce`, and `mixreel-review`. If any of those names already exist at the destination, the installer stops and changes nothing it did not create.

Point your agent at the installed `mixreel` skill for a full job, or at one stage skill when you already have the previous artifact.

## A project folder

Keep projects outside the clone.

```text
my-spot/
  BRIEF.md
  brand/brand-context.md
  script.md
  previs/
  plan.json
  journal.json
  master.mp4
```

Copy `skills/mixreel/assets/BRIEF.template.md` to start the brief. Product facts go in `brand/brand-context.md`.

Initialize an empty provider config only if you are about to call a model. The directory must not be inside a Git checkout:

```sh
python3 skills/mixreel/scripts/init_config.py --directory "$HOME/.config/mixreel"
```

## Next

- [Previs](previs.md) if the camera move matters before you generate.
- [Providers](providers.md) when you are ready to pay for video.
- [QA](qa.md) after the first master exists.
