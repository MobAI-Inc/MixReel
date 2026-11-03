# Project records

Keep the project outside the skill source. A typical folder:

```text
project/
  BRIEF.md
  brand/brand-context.md
  reference-analysis.md
  script.md
  previs/
  video-plan.md
  keyframes/
  journal.json
  plan.json
  master.mp4
  review.md
```

Start `BRIEF.md` from [the brief template](../assets/BRIEF.template.md). Product facts and claim limits live in `brand/brand-context.md`, shared by every film for that brand. The brief points at that file. It does not copy a private catalog into the chat.

Record, as they become known:

- the message, the audience, the length, the aspect ratio, and the ask
- what was borrowed from a reference, and what was excluded
- provider, model id, and account alias (never the key)
- generation groups, keyframes that are new versus reused, and duration asked versus duration kept
- quoted, estimated, and billed amounts in their own currencies
- review decisions: pass, fail, or not checked, with the artifact version

Unknown amounts stay unknown. Do not turn a blank quote into zero.

Generation records are one row per paid request: group id, task id, request hash, state, and where the file landed. The journal script is the ledger. The prose record explains the creative choice.
