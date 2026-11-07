# Contributing

MixReel is published by MobAI Inc. Issues and pull requests are welcome.
Please keep the project usable by someone who has never seen an internal
checkout: no private hosts, no private product names, and no customer material.

## How to propose a change

1. Open an issue for a behavior change before a large pull request.
2. Branch from `main`.
3. Add or update tests for code you change.
4. Run the same checks as CI:

```sh
python3 -m pip install -r requirements.txt
python3 -m unittest discover -s tests -v
python3 scripts/check_package.py
```

`ffmpeg` must be on `PATH` for the media tests. The optional review-model
packages are not required for CI.

5. Open a pull request. The description should say what changed and how you
   checked it.

## What belongs here

- Provider adapters that call a vendor's own public API with the user's key.
- QA checks, previs improvements, and skill instructions for ads and product video.
- Docs and examples that use invented brands, or media you have rights to.

## What does not belong here

- A hosted relay, a shared key, or a default account.
- Prompt recipes copied from a private integration or from confidential material. A prompt format worked out for MixReel itself is welcome in the skills when it says what was verified, on which model, and what the vendor's own guide says.
- Customer names, private hosts, or recordings of a real client's product.
- Story-only review rules. This edition is for ads and product video.

## Contribution licensing

Contributions intentionally submitted for inclusion in this repository are
licensed under the [Apache License 2.0](LICENSE), in accordance with section 5
of that license (inbound = outbound), unless you explicitly state otherwise.

The original MIT grant on portions listed in `THIRD_PARTY_NOTICES.md` remains
unchanged.

## Reports

Security reports go to the contact in `SECURITY.md`.
