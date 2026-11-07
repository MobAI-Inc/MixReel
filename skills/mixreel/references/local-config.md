# Local configuration

Read this when installing the skills or selecting paid services. Configuration is private. It stays outside the repository, outside any Git checkout, and outside film project exports. Never ask the user to paste a key into a chat or a document.

## Default files

- `~/.config/mixreel/providers.json` records the image generation, image editing, and video generation profiles. Each role names the provider that actually bills, the model, an endpoint allowlist, and which credential to read. Name more profiles when stages need different services, and bind each job to its actual profile. Generation and editing often use different models, so set them up separately. A tool whose sign-in the host already manages needs no local key.
- `~/.config/mixreel/credentials.json` holds local plaintext keys under named fields. The directory is mode `0700` and both files mode `0600` where the operating system allows it. That is file permission protection, not encryption. The environment or a host secret store is better when you have one.

Create blank files with the installed initializer. `<mixreel>` is the installed `mixreel` skill folder, the parent of this `references` folder. Replace it with the real path.

```sh
python3 <mixreel>/scripts/init_config.py --directory "$HOME/.config/mixreel"
```

The command copies the example profiles, writes empty key fields, imports no keys, makes no network calls, and keeps values you already filled on a second run. It does not load credentials into tools or configure a provider client. On Windows, restrict these files to the user with the operating system's access controls. The POSIX mode checks do not apply there.

The templates are [provider profiles](../assets/providers.example.json) and [empty credential slots](../assets/credentials.example.json). Profiles name a provider, a model, a base URL, and which credential field to read. They do not contain a key. `--directory` accepts a custom folder. Record only its location, never its contents, in project records. Do not copy real files back over the templates.

Put keys in the environment when you can:

| Use | Variable |
| --- | --- |
| MiniMax video | `MINIMAX_API_KEY` |
| MiniMax host override | `MINIMAX_API_BASE` |
| Seedance / Ark / BytePlus | `ARK_API_KEY` |
| Ark or BytePlus host | `ARK_API_BASE` |
| Optional Gemini hints | `GEMINI_API_KEY` or `GOOGLE_API_KEY` |
| Optional review interpreter | `MIXREEL_PYTHON` |

## How a key is chosen

Use exactly the profile chosen for the operation. Do not silently use an image reseller for video because it offers the same model. A changed provider or account needs the user's authorization. The selected profile alone grants no permission to spend.

`auth.source` picks one of these:

- `credentials_file` reads the value at `keys[auth.name]` in the credentials file next to the profiles.
- `env` reads exactly the named environment variable in the running process.
- `host_secret` hands the name to the host's existing secret manager.
- `host_tool` uses a tool whose sign-in the host already manages. No key file is needed.

These fields are a configuration convention for the agent and the adapters. When you use an existing tool, check that its real provider and account match the selected profile. If it cannot take this convention, configure it the documented way and record only the credential source name.

Read only the selected credential, inside the client that sends the request. Do not dump the file, the shell environment, Authorization headers, or raw authenticated requests into the conversation, logs, or the journal. Do not put keys on the command line.

Before a key is sent, check the HTTPS endpoint against `allowed_hosts` and the service the user meant. An empty key, endpoint, or allowlist means unconfigured, not permission to guess. Do not forward authentication to download hosts or across hosts on a redirect. Current documentation decides the authentication format, the operations really supported, and billing, as [providers](providers.md) describes.

A filled profile is not proof that the endpoint accepted you, and it is not permission to test a billable endpoint. Record the model id and the docs URL you checked. Leave price fields blank until you have a quote from that vendor. Handoffs record only service names, model ids, credential source names, redacted results, and known costs.

## Changing the service behind a model

When the user moves a model to a different service, update the affected profiles and their callers together. Check the new service's model id, endpoint, authentication, and operation fields in its own current documentation. Do not reuse another service's request bodies, mask rules, or polling paths without checking them. Leave unrelated profiles alone, especially the chosen video provider.

Prefer a documented model-list request to check authentication without generating anything. Record authentication, advertised capabilities, quotes, and a successful generation separately. Discovery does not prove that edits work or that output is good. Use a quote request only when it is documented as non-generating, and do not submit a paid test just to finish moving the configuration. Existing task ids are still queried through the provider and account that accepted them.
