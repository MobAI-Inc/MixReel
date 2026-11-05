# The project folder

Read this when you start any stage, including a stage entered on its own. Everything the user wants kept between films lives here, on a laptop or on a server alike.

A project holds one brand or client and outlives any film, task or session. Keep it outside the installed skill. The user works in this folder and may never open the skill, so it is where they read, correct and reuse everything.

```
<project>/
  brand/                  one per brand, shared by every film
    brand-context.md      product, audience, positioning, key messages, what each may claim, asset list
    requirements.md       the client's standing rules for deliverables, when they have any
    audience-taste.md     longings broken down, familiar material, approved scripts, rejected approaches
    competitors.md        how competitors advertise and what their audience reacts to
    films.md              every film written or made for this brand, one row each
    taste-library/        analyzed ads with frames and breakdowns
    assets/               logos, packaging, product photos, character art, screenshots, UI recordings
  <film>/                 one per ad or film
    BRIEF.md
    script.md
    reference-sheet.jpg
    plan.json, providers/, journal.json, media/, review.md   once production starts
```

Every source file the brand supplies goes in `brand/assets/`, so each film takes its logo, packaging and UI from one place. `brand-context.md` lists what is there and what each file may be used for.

## Where it lives

Projects sit in one projects directory, one folder per brand. The same rule holds on a laptop and on a server, with nothing tied to one host.

1. The folder the user or the host names.
2. Otherwise `$MIXREEL_PROJECTS_DIR/<brand>/`, when that variable is set.
3. Otherwise `mixreel-projects/<brand>/` under the current working directory.

`<brand>` is the brand name in lowercase, with spaces turned into hyphens. On a server, point `MIXREEL_PROJECTS_DIR` at storage that survives a restart or redeploy and that every agent working for this user can read.

## Find it before you work

1. Use the folder the user or the host names. Otherwise look in the working directory, its parents and the projects directory above for a `brand/` folder or a folder named for the brand, including folders the user keeps under other names. Map those, and do not copy them.
2. When you find one, use it and say which. When there is none, create it with `python3 <mixreel>/scripts/init_project.py --brand "<brand>"` and say where. `<mixreel>` is the installed `mixreel` skill folder, the parent of this `references` folder. Replace it with the real path, and run the command from the folder the user is working in. Add `--film <film>` to create the film folder with its brief. The script never overwrites a file and makes no network request.
3. A task, thread or session folder is not a project. If the host wants a separate folder per task, that folder is the film's, inside the project. Never start a second brand layer for a brand that already has one.
4. If this storage will not outlast the session, or other agents working for this user cannot read it, tell the user. The next film would start from nothing.

A one-off with no brand, such as a single illustration or a film with no advertising, keeps its own folder and needs no brand layer.

## Build the brand files

This is row 0 on [the pipeline map](pipeline.md). Do it when the user asks for brand files, and before a first script when `brand/brand-context.md` is still the starter text. It needs no film folder, no reference video and no API key.

1. Ask for the brand name if you do not have it, then find or create the project as above.
2. Ask for whatever the user has not already given you, all in one message and in everyday words.
   - the product's name and what it does
   - what is actually different about it, and a screenshot or photo that shows it
   - who it is for, in which market and language, and where the ads will run
   - the one or two things they most want people to know
   - what must not be claimed, and the source of any price, "free", guarantee or result they want to state
   - the logo, packaging, photos, screenshots and recordings they have
3. Write the answers into `brand/brand-context.md` under its headings. A page or document the user points you at can fill a heading when you name it as the source. An answer nobody has stays marked `unknown`. Do not fill a gap from general knowledge or from someone else's ad.
4. Copy each file they supply into `brand/assets/` and list it with what it may be used for. Put any standing rules they mention in `brand/requirements.md`.
5. Show them `brand/brand-context.md` and write their corrections back. If brand files were all they asked for, stop here and say that a script is the usual next step.

## Read what this stage needs

Each stage reads only what bears on it. Follow `brand/requirements.md` wherever it applies, also when the work begins partway, such as from an accepted script. When the brand keeps a file under another name, its `brand/README.md` says so. Where these files differ from this skill's defaults the brand files win, and the latest user instruction wins over both.

When a brand file is missing, build it from what the user supplies and show it to them before relying on it. Write the user's corrections about the product, the audience or the deliverables back into the brand files so the next film starts from them.

## Record every film

`brand/films.md` is how the next person finds what exists. Each row has the film folder, the event in one sentence, the key message, the idea or situation used, the state (drafted, approved, rejected or delivered), the script path, the final file and what the user said.

Add the row when a script is written. Update it when the script is approved or rejected and when the film is delivered. Read it before writing a new script, and do not reuse an event or idea it lists without saying so. When someone asks what has been made, answer from it and check the folders it names.
