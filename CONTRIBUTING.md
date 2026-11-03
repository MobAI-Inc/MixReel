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
- Prompt recipes copied from a private integration.
- Customer names, private hosts, or recordings of a real client's product.
- Story-only review rules. This edition is for ads and product video.

## Contributor License Agreement

By submitting a contribution to this repository, you agree to the following.

1. You have the legal right to submit the contribution, and it does not
   include material you are not allowed to license.
2. You license the contribution under the MixReel License in `LICENSE`.
3. You grant MobAI Inc a perpetual, irrevocable, worldwide, non-exclusive,
   royalty-free, sublicensable license to use, reproduce, modify, display,
   distribute, and relicense the contribution, including under other terms
   and in commercial products.
4. MobAI Inc may use the contribution in commercial offerings, including
   hosted services that the public MixReel License does not allow other
   parties to operate.
5. You are not required to provide support for the contribution.

This agreement does not change the license of MIT portions listed in
`THIRD_PARTY_NOTICES`. If your contribution modifies a MIT portion, the
original MIT grant on that portion remains, and your new expression is also
covered by this agreement.

## Reports

Security reports go to the contact in `SECURITY.md`. License questions for
hosted or resale use go to vito_zhong@mobai-game.com.
