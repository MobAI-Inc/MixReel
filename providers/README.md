# Provider adapters

Add a vendor by implementing `VideoProvider` in `providers/base.py`:

- `capabilities()` returns the envelope you verified in that vendor's docs, and the date you checked
- `submit()` posts one job and returns a task id
- `status()` maps the vendor's words onto `queued`, `running`, `succeeded`, `failed`, `cancelled`
- `download()` writes the file and a SHA-256

Rules for a patch:

- Call the vendor's public API. Do not insert a host this project operates.
- Read the key from an environment variable. Do not add a default key.
- Take the model id from the caller. If you special-case known ids, refuse unknown ids unless the caller sets `extra.allow_unverified` after reading the current docs.
- Tests use a fake transport. CI does not make network calls.
- Do not add a private prompt template. Point at the vendor's public prompt guide if you need to mention wording.

`workflow.py` reserves a local journal, marks the job `submitting`, submits once, and stores the task id. A failed submit becomes `outcome_unknown`.

MiniMax and Seedance are the two worked examples. Gemini review is optional and does not generate video.
