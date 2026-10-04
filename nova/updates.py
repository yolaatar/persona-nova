"""Post-event updates. The baseline is never edited; each update is a separate file.

An update file (JSON, in nova/updates/) looks like:
  {
    "id": "U01",
    "received": "2026-10-01T10:00",
    "summary": "What the new information says",
    "kind": "decision | proposition | validation | livraison | statut | information",
    "source": {"file": "updates/U01_note.pdf", "anchor": "exact text", "kind": "pdf"},
    "approval": "none | <who approved, with a source>",
    "impacts": [
      {"action": "A03", "field": "status", "before": "...", "after": "..."}
    ]
  }
An update may change the status of an action or of a fact. It never removes a
baseline entry. Without a named approval, it is shown as a proposition.
"""

from __future__ import annotations

import json
from pathlib import Path

UPDATES_DIR = Path(__file__).resolve().parents[1] / "updates"


def load_updates(folder: Path = UPDATES_DIR) -> list[dict]:
    if not folder.exists():
        return []
    items = []
    for path in sorted(folder.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        data.setdefault("kind", "information")
        data.setdefault("impacts", [])
        data.setdefault("approval", "none")
        items.append(data)
    return items
