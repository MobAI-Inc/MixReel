# MixReel

<p align="center"><a href="#showcase"><b>Showcase</b></a> &nbsp;&bull;&nbsp; <a href="#quickstart"><b>Quickstart</b></a> &nbsp;&bull;&nbsp; <a href="docs/getting-started.md"><b>Getting started</b></a> &nbsp;&bull;&nbsp; <a href="README.zh-CN.md"><b>简体中文</b></a></p>

Block the shot in 3D before you pay for a generation. Then let the cut tell you when a frame flashed, a cut landed late, or the package stopped matching the real product.

MixReel is an open-source agent skill for **ad, e-commerce, and product short videos**. It runs locally. You bring the model, on that vendor's own API, with your own key. This repository does not host a relay and does not lock you to one model.

[![CI](https://github.com/MobAI-Inc/MixReel/actions/workflows/ci.yml/badge.svg)](https://github.com/MobAI-Inc/MixReel/actions/workflows/ci.yml)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

<p align="center">
  <img src="docs/assets/hero.png" alt="MixReel: a grey 3D previs of a handbag next to the finished bordeaux leather frame, a film strip, a beat-marked waveform, and review checks" width="1000">
</p>

## Showcase

Six ads for three real brands, each made from an empty folder by a coding agent running MixReel. Every brand gets one performance ad and one creator-style or brand film, so you can see the same product told two ways. Each film is shown as the agent delivered it, with no manual edit or retouch, small flaws included.

### Genshin Impact · Douyin, Chinese

[Script, shot list and production notes](examples/showcase/genshin-impact/README.md)

<table>
  <tr>
    <th width="50%">Performance ad</th>
    <th width="50%">Brand film</th>
  </tr>
  <tr>
    <td><video src="https://github.com/user-attachments/assets/305adf51-c6b3-4712-ae3f-545e185dd965" controls muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/47e622dd-d435-4dc1-9788-195833cc6333" controls muted></video></td>
  </tr>
  <tr>
    <td valign="top"><p><b>"Finally in on it"</b>, 37 s. At lunch a coworker pitches the 7.2 new-player offer, pick one standard five-star, to the quiet guy who never joins in. Two old players replay a cutscene, and he finishes the line. He started playing a while back.</p><p>Built from the offer text on the official site, and the line from the official 7.2 trailer, checked for who says it.</p><p>Generation cost <b>$6.60</b></p></td>
    <td valign="top"><p><b>"This table of people"</b>, 44 s. On the night of the 7.2 update a six-year player tears up. His girlfriend asks if he is not bored of it. He turns the phone around to show the Seven Nations round table and says he met every one of them over those six years.</p><p>Built from official trailer footage and key art. The game's characters are never drawn by a model.</p><p>Generation cost <b>$4.79</b></p></td>
  </tr>
</table>

### Myfoodie cat food · Douyin, Chinese

[Script, shot list and production notes](examples/showcase/myfoodie/README.md)

<table>
  <tr>
    <th width="50%">Performance ad</th>
    <th width="50%">Creator ad</th>
  </tr>
  <tr>
    <td><video src="https://github.com/user-attachments/assets/ea549b62-cab7-4150-b72c-fe26b10e4085" controls muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/2be40599-ab40-4324-a337-3f1347ffd823" controls muted></video></td>
  </tr>
  <tr>
    <td valign="top"><p><b>"Hunting mode"</b>, 19 s. A tabby stalks its dinner bowl like prey and pounces. The offer card lands about six seconds in, and the one claim is the line printed on the pack, "≥80% meat, bone and organs".</p><p>The pack is the official photo, composited, with every word read off the real pack.</p><p>Generation cost <b>$6.43</b></p></td>
    <td valign="top"><p><b>"She can hunt now"</b>, 53 s. The cat is sure its owner cannot hunt and leaves toy mice on her pillow every morning. She carries home a box. The cat inspects the bag, reads "meat, bone, organs", and accepts her. That night it still leaves one mouse, just in case.</p><p>It uses the same pack photo and one shared cat, so both films star the same tabby.</p><p>Generation cost <b>$8.96</b></p></td>
  </tr>
</table>

### Tipsy Chat · Meta, English

[Script, shot list and production notes](examples/showcase/tipsy-chat/README.md)

<table>
  <tr>
    <th width="50%">Performance ad</th>
    <th width="50%">Creator ad</th>
  </tr>
  <tr>
    <td><video src="https://github.com/user-attachments/assets/af948568-ab5f-43c5-a32d-55706ea14d9d" controls muted></video></td>
    <td><video src="https://github.com/user-attachments/assets/2c0918ce-b603-4401-a200-45f17e74e711" controls muted></video></td>
  </tr>
  <tr>
    <td valign="top"><p><b>"Ch 47 coming soon"</b>, 23 s. At 1 a.m. she refreshes a story that stopped updating in 2021. She opens Tipsy, writes the next line herself, and the story answers.</p><p>The app screens are real Tipsy UI frames from the app's own ads, with private text blurred.</p><p>Generation cost <b>$2.15</b></p></td>
    <td valign="top"><p><b>"Who is Biscuit"</b>, 41 s. Her roommate has a secret boyfriend, or so she thinks. She opens the door on a cowboy from a Wild West story, calling from the phone. By the end she is on the bed asking what her own horse is called.</p><p>The call screen is the real Tipsy one. Every line is spoken by the video model.</p><p>Generation cost <b>$8.15</b></p></td>
  </tr>
</table>

**How they were made.** For each brand the agent built the brand files from public sources, then wrote the script from the brand's own selling point. Scenes with more than one shot were blocked in Blender first. Faces came from Midjourney and were completed with GPT Image. Shots and spoken lines came from MiniMax H3, mostly H3 Max Turbo at 1080p. Logos, packs and app screens were composited from the real assets, and the cut went through MixReel's QA plus a Gemini listening pass. Total generation cost for the six cuts was $37.08.

These are unofficial concept ads made to show the workflow. They are not affiliated with or endorsed by miHoYo, Myfoodie or Tipsy Chat. Characters, marks, packaging and app UI belong to their owners and are not covered by this repository's license.

## Four things MixReel does

<table>
<tr>
<td width="50%" valign="top">
<img src="docs/assets/feature-previs.png" alt="3D previs: a top view with two camera positions, grey clay start and end frames of a perfume bottle, and the finished amber bottle at the same two angles">
<p><b>1. 3D previs before you pay.</b> Block the camera, lens, and move in Blender (or the built-in Python fallback) first. The product shape and the camera angle stay the same from the grey plan to the finished frame.</p>
</td>
<td width="50%" valign="top">
<img src="docs/assets/feature-review.png" alt="Automatic review: a watch film strip with a flash frame flagged at 0:03.2, the regenerated frame below it, and a checklist of checks">
<p><b>2. Automatic review on the cut.</b> The checker finds flashes, flicker, late or missed cuts, and stray frames. Optional small models add product drift (CLIP, DINOv2), face identity (InsightFace), and lip sync (SyncNet). Problems get a timecode, and only the bad shot is regenerated.</p>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<img src="docs/assets/feature-beat.png" alt="Shot by shot: four jewelry shots with their grey previs, above a waveform whose cuts land on beat markers">
<p><b>3. Shot by shot, cut on the beat.</b> The script is split into shots and generation groups, each with its own timing and keyframes. <code>beat_grid.py</code> finds the beats in your track, and QA flags any cut more than 60 ms off the beat (the default tolerance).</p>
</td>
<td width="50%" valign="top">
<img src="docs/assets/feature-models.png" alt="Any model: one grey champagne shot plan branching to three finished versions labelled MiniMax, Seedance, and your model">
<p><b>4. Any model, fully open.</b> One small provider interface. Example adapters call the official MiniMax and Seedance APIs with your own key, and you can add your own. Gemini review is optional. Every line of the source is in this repository.</p>
</td>
</tr>
</table>

## Quickstart

No API key. Python 3.10+, `ffmpeg`, `ffprobe`, and the packages in `requirements.txt`.

```sh
git clone https://github.com/MobAI-Inc/MixReel.git
cd MixReel
python3 -m pip install -r requirements.txt
python3 scripts/demo.py
```

The command writes a temporary directory and prints its path. Inside it:

- a rough previs of a bottle orbit (`previs/plan.png`, start and end stills)
- a 4-second edit made from synthetic clips (`master.mp4`)
- `qa.json` for that edit
- the checker's own synthetic self-check, which must catch a white flash, a black flash, flicker, a late cut, and an off-beat cut

Nothing is downloaded. Nothing is written into the clone. Delete the temp directory when you are done.

Install the skills into an agent skills directory when you want the full pipeline. Pick the line for your agent:

```sh
# Claude Code, every project
python3 scripts/install.py --destination ~/.claude/skills
# Codex, every project
python3 scripts/install.py --destination ~/.codex/skills
```

The installer copies seven skills, refuses to overwrite a directory that already exists, and does not read keys. The destination has to be a folder your agent reads skills from. A folder named `skills/` in your project does not count.

| Agent | One project | Every project |
| --- | --- | --- |
| Claude Code | `/path/to/your-project/.claude/skills` | `~/.claude/skills` |
| Codex | Check your version's docs | `~/.codex/skills` |

Give a full path. A relative one would land inside this clone. If the agent does not list the `mixreel` skills afterwards, start a new session in that folder. Keep the clone. The provider adapters in `providers/` are not copied into the skills folder. Upgrading to a new version is in [getting started](docs/getting-started.md#upgrade).

## Pipeline

```mermaid
flowchart LR
  Z[Brand files] --> A[Analyze a reference ad, if you have one]
  A --> B[Script and 3D previs]
  B --> C[Group shots for the provider]
  C --> D[Keyframes from your assets]
  D --> E[Your video API]
  E --> F[Edit]
  F --> G[Automatic QA]
  G --> H[Review]
```

Open your agent in the folder where you want the work kept, and ask for what you need. You can stop after any step.

- `Use mixreel to build brand files for my app`
- `Write a 20-second script`

The `mixreel` skill routes the agent to one stage at a time. Stages can also be invoked on their own. Neither request needs an API key.

## What you can do with it

**Blender previs, before you spend.** Block a product orbit, a hand entering frame, or a multi-angle pack shot in 3D. You get a top view, start and end frames, and a storyboard. Blender is used when it is installed. Without it, a pure Python raster backend still shows occlusion and screen direction. It does not download Blender for you.

**QA on the cut, not on a contact sheet.** `qa_check.py` measures white and black flashes, flicker, cut offset, missed cuts, off-beat cuts, stray frames from the neighboring shot, silence, loudness, peak, and frame size. `frame_pack.py` lays out the stills an agent has to actually look at: overviews, seams, suspect bursts, curves, and full-resolution brand frames.

**Small models, only if you want them.** CLIP and DINOv2 can flag picture and product drift. InsightFace with the small `buffalo_s` pack can check face consistency. SyncNet can report a lip-sync offset. None of these are installed or downloaded by a normal run. Face and lip-sync weights are research-licensed. Read [model weights](docs/model-weights.md) before you turn them on. A public copy of `syncnet_v2.model` is in the `auxiliary/` files of [ByteDance/LatentSync-1.6](https://huggingface.co/ByteDance/LatentSync-1.6).

**Gemini is a hint.** If you set a Gemini key and ask for the pass, the script sends suspect ranges and returns notes. Those notes do not pass or fail the cut.

**A budget journal.** Reserve the worst case before a paid call, store the task id before you do anything else, and reconcile the bill separately from the download. A retry after a lost response looks the old task up. It does not submit a second one. `keyframe_diff.py` catches an edit you paid for that did not change the pixels.

**Your model, your account.** The provider interface is `capabilities`, `submit`, `status`, and `download`. Example adapters call the official MiniMax video API and the official Seedance API on Volcengine Ark or BytePlus. Keys come from your environment. Model ids come from your config. See [providers](docs/providers.md).

**Real marks.** Logos, packaging text, product copy, and app UI are composited from the asset you supply. The skills do not ask a model to invent them.

## Example slots

These slots use invented brands and are still being filled. The finished films are in the [showcase](#showcase) above.

| Slot | What it will show | Now |
| --- | --- | --- |
| [Product hero](examples/product-hero/README.md) | Previs, pack shot, QA | Coming soon |
| [App promo](examples/app-promo/README.md) | A real screen recording, captions, music hits | Coming soon |
| [Hook variants](examples/hook-variants/README.md) | One body, three openings | Coming soon |
| [Quickstart](examples/quickstart/README.md) | The no-key command above | Runs today |
| [Demo index](docs/demos/README.md) | Where to drop files | Coming soon |

## QA, in one table

| Check | What it means | A common false alarm |
| --- | --- | --- |
| Flash | A frame is far brighter or darker than its neighbors, then the picture returns | A intentional strobe or a hard white title hit |
| Flicker | Luma alternates up and down across several frames | Fine texture on a fast pan |
| Cut offset | The picture changes later or earlier than the plan | A dissolve you planned as a cut |
| Missed cut | The plan has a cut and the picture does not change | A locked-off shot that was supposed to cut to a similar frame |
| Off-beat cut | The measured cut is outside the beat tolerance | A track with no clear pulse, or a tolerance that is tighter than the edit |
| Stray frames | A few frames of the previous shot survive the cut | Very short intentional flash frames |
| Silence, loudness, peak | The soundtrack is missing, quiet, or hot against the levels you pass in | A deliberate mute |
| Frame size | The master does not match `--size` | A plan that was authored for another aspect |

Suspects are places to look. The review skill still requires someone to watch the images.

## Documentation

- [Getting started](docs/getting-started.md)
- [Providers](docs/providers.md)
- [Previs](docs/previs.md)
- [QA](docs/qa.md)
- [Model weights](docs/model-weights.md)
- [Architecture](docs/architecture.md)
- [FAQ](docs/faq.md)
- [中文说明](README.zh-CN.md)

## License

MixReel is licensed under the [Apache License 2.0](LICENSE). Generated videos belong to the user and can be used commercially. Contact: vito_zhong@mobai-game.com.

Some local tools include material first published under the MIT license by MixReel contributors. That notice is in [THIRD_PARTY_NOTICES](THIRD_PARTY_NOTICES.md).

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md). Contributions are licensed under Apache-2.0, in accordance with section 5 of the license (inbound = outbound).
