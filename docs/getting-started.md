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

Keep projects outside the clone, one folder per brand. Run this from the folder you want them in, using the path you installed the skills to. Each brand folder keeps the brand's facts, requirements, source assets and a record of every film, so the second film for a brand does not ask for them again.

```sh
python3 ~/.agents/skills/mixreel/scripts/init_project.py --brand "Kite Pantry" --film spring-spot
```

```text
mixreel-projects/kite-pantry/
  brand/
    brand-context.md   product facts, claims and the asset list
    requirements.md    standing rules for every deliverable
    audience-taste.md
    competitors.md
    films.md           one row per film
    taste-library/
    assets/            logo, packaging, product photos, UI recordings
  spring-spot/
    BRIEF.md
    script.md
    previs/
    plan.json
    journal.json
    master.mp4
```

The projects directory is `--root` when given, else `$MIXREEL_PROJECTS_DIR`, else `mixreel-projects/` under the current working directory. On a server, set `MIXREEL_PROJECTS_DIR` to storage that survives a redeploy. The script only adds what is missing and never overwrites a file. The agent runs it on first use when no project exists. The full convention is `skills/mixreel/references/project.md`.

Initialize an empty provider config only if you are about to call a model. The directory must not be inside a Git checkout:

```sh
python3 ~/.agents/skills/mixreel/scripts/init_config.py --directory "$HOME/.config/mixreel"
```

## Next

- [Previs](previs.md) if the camera move matters before you generate.
- [Providers](providers.md) when you are ready to pay for video.
- [QA](qa.md) after the first master exists.
