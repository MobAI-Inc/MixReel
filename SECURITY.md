# Security

MixReel runs on your machine and calls APIs with your keys. It does not
operate an account service.

## Reporting a vulnerability

Write to vito_zhong@mobai-game.com with:

- the version or commit
- the file and the behavior
- whether a key, a local journal, or a media file can be exposed

Please do not open a public issue for an unfixed vulnerability that exposes
credentials or local project files.

## What to expect

A maintainer will confirm receipt and say whether the report is accepted.
This repository does not publish a bounty or a response-time promise.

## Practices in this tree

- Example credentials are empty strings.
- `init_config.py` refuses to write keys inside a Git checkout.
- `redact_export.py` strips credential fields and signed query tokens from a
  JSON export. It does not review free-form prose.
- CI runs the heuristic scan in `scripts/check_package.py`. It is not a substitute for review.
