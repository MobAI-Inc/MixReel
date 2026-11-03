# Architecture

MixReel is a set of agent skills plus local Python tools. The skills tell an agent what to read and what not to skip. The tools do the deterministic work: previs, validation, editing, QA, journaling, and redaction.

```text
skills/mixreel                 router and shared rules
skills/mixreel-analyze         reference evidence
skills/mixreel-script          ad script and previs
skills/mixreel-video-plan      generation groups
skills/mixreel-keyframes       stills
skills/mixreel-produce         submit, edit, export
skills/mixreel-review          QA judgment and repair routing
providers/                     official API adapters
```

Shared scripts live in `skills/mixreel/scripts` so a copied skill collection still runs. Previs scripts live next to the script skill because that is the stage that decides to block a shot.

The edit plan is JSON, versions 1 through 3. Version 3 adds local recordings, overlays, and per-shot audio. `validate_plan.py` checks structure and timing. It does not approve the creative work.

Providers are not imported by the skills at runtime. An agent, or `providers/workflow.py`, calls them when a user has authorized a spend. Tests mock HTTP.

There is no service process in this repository.
