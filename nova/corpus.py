"""Read the NOVA corpus (read-only) and check that citations are really there."""

from __future__ import annotations

import email
import email.policy
import re
import subprocess
from functools import lru_cache
from pathlib import Path

import openpyxl

CORPUS = Path(__file__).resolve().parents[2] / "loto-quebec-nova-participants" / "Projet360_NOVA_ETUDIANTS"


def _norm(text: str) -> str:
    text = text.replace("’", "'").replace(" ", " ")
    return re.sub(r"\s+", " ", text)


@lru_cache(maxsize=None)
def text_of(relpath: str) -> str:
    path = CORPUS / relpath
    suffix = path.suffix.lower()
    if suffix == ".eml":
        msg = email.message_from_bytes(path.read_bytes(), policy=email.policy.default)
        parts = [f"{h}: {msg[h]}" for h in ("Date", "From", "To", "Subject") if msg[h]]
        for part in msg.walk():
            if not part.is_multipart() and not part.get_filename() and part.get_content_type() == "text/plain":
                parts.append(part.get_content())
        return _norm("\n".join(parts))
    if suffix in {".txt", ".md", ".csv"}:
        return _norm(path.read_text(encoding="utf-8"))
    if suffix == ".pdf":
        out = subprocess.run(["pdftotext", "-layout", str(path), "-"], capture_output=True, text=True, check=True).stdout
        return _norm(out)
    if suffix == ".xlsx":
        wb = openpyxl.load_workbook(path, data_only=True)
        cells = []
        for ws in wb.worksheets:
            for row in ws.iter_rows():
                for c in row:
                    if c.value is not None:
                        cells.append(f"{ws.title}!{c.coordinate}={c.value}")
        return _norm("\n".join(cells))
    return ""


def exists(relpath: str) -> bool:
    return (CORPUS / relpath).exists()


def anchor_found(relpath: str, anchor: str) -> bool:
    if not anchor:
        return exists(relpath)
    return _norm(anchor) in text_of(relpath)
