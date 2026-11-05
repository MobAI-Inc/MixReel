# Local configuration

Create a blank config outside the repository and outside any Git checkout. `<mixreel>` is the installed `mixreel` skill folder, the parent of this `references` folder. Replace it with the real path.

```sh
python3 <mixreel>/scripts/init_config.py --directory "$HOME/.config/mixreel"
```

The command copies the example profiles, writes empty key fields, and does not read existing secrets. On a second run it keeps values you already filled. Files are mode `0600` and the directory is mode `0700` where the operating system allows it.

Put keys in the environment when you can:

| Use | Variable |
| --- | --- |
| MiniMax video | `MINIMAX_API_KEY` |
| MiniMax host override | `MINIMAX_API_BASE` |
| Seedance / Ark / BytePlus | `ARK_API_KEY` |
| Ark or BytePlus host | `ARK_API_BASE` |
| Optional Gemini hints | `GEMINI_API_KEY` or `GOOGLE_API_KEY` |

The example files are `assets/providers.example.json` and `assets/credentials.example.json`. Profiles name a provider, a model, a base URL, and which credential field to read. They do not contain a key.

A filled profile is not proof that the endpoint accepted you, and it is not permission to spend. Record the model id and the docs URL you checked. Leave price fields blank until you have a quote from that vendor.
