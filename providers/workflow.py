"""Reserve a budget, submit once, and record the vendor task id.

The provider adapters do not keep a ledger. Call this helper when a project
journal exists. It uses the local journal in the MixReel skill:

1. Check the request against capabilities by calling submit's own validator
   only after the reservation is on disk.
2. Move the job to ``submitting`` before the network call.
3. Store the task id as soon as the vendor returns one.
4. On a transport failure, leave the job as ``outcome_unknown`` so a later
   lookup can reconcile it. Do not submit the same request again.
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path

from .base import ProviderError, VideoRequest

JOURNAL = Path(__file__).resolve().parents[1] / "skills" / "mixreel" / "scripts" / "job_journal.py"


def _journal():
    spec = importlib.util.spec_from_file_location("mixreel_job_journal", JOURNAL)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def prepare_and_submit(provider, request, journal_path, job_id, currency, ceiling, evidence,
                       quote=None, quote_kind="unavailable"):
    """Reserve ``ceiling``, submit once, and return the task id."""
    request = request if isinstance(request, VideoRequest) else VideoRequest(**request)
    journal = _journal()
    path = Path(journal_path)
    canonical = {
        "prompt": request.prompt,
        "model": provider.model,
        "duration": request.duration,
        "resolution": request.resolution,
        "ratio": request.ratio,
        "references": [{"kind": ref.kind, "role": ref.role, "url": ref.url} for ref in request.references],
        "seed": request.seed,
        "generate_audio": request.generate_audio,
    }
    with journal.locked(path):
        data = json.loads(path.read_text())
        journal.reserve(
            data, job_id, canonical, provider.name, provider.model, "video_generation",
            currency, ceiling, evidence, quote, quote_kind,
        )
        journal.transition(data, job_id, "submitting", evidence)
        journal.save(path, data)
    try:
        task_id = provider.submit(request)
    except Exception as exc:
        with journal.locked(path):
            data = json.loads(path.read_text())
            journal.transition(data, job_id, "outcome_unknown", type(exc).__name__)
            journal.save(path, data)
        raise
    with journal.locked(path):
        data = json.loads(path.read_text())
        journal.transition(data, job_id, "submitted", "vendor accepted the task", task_id=task_id)
        journal.save(path, data)
    return task_id


def init_journal(path, budgets):
    """Create a journal. ``budgets`` maps a 3-letter currency code to a maximum."""
    journal = _journal()
    path = Path(path)
    if path.exists():
        raise ProviderError("journal already exists")
    data = {"version": 1, "budgets": {}, "jobs": {}}
    for code, value in budgets.items():
        if not isinstance(code, str) or len(code) != 3 or not code.isalpha() or code != code.upper():
            raise ProviderError("currency code must be three uppercase letters")
        data["budgets"][code] = str(journal.amount(value))
    path.parent.mkdir(parents=True, exist_ok=True)
    journal.save(path, data)
    return data
