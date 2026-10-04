"""Checks on the NOVA memory: every citation must exist in the corpus, every action must be complete."""

import re
from pathlib import Path

import pytest

from nova.answers import ANSWERS
from nova.corpus import CORPUS, anchor_found, exists
from nova.data import ACTIONS, CONDITIONS, CONTRADICTIONS, FACTS, REFERENCE, budget_summary

ROOT = Path(__file__).resolve().parents[1]
ALL_SOURCES = (
    [(f["id"], s) for f in FACTS for s in f["sources"]]
    + [(r["id"], s) for r in REFERENCE for s in r["sources"]]
    + [(a["q"], {"file": s[0], "anchor": s[1], "kind": s[0].rsplit(".", 1)[-1]}) for a in ANSWERS for s in a["sources"]]
)


@pytest.mark.skipif(not CORPUS.exists(), reason="corpus not available")
@pytest.mark.parametrize("ident,src", ALL_SOURCES, ids=lambda x: x if isinstance(x, str) else x["file"][:40])
def test_citation_exists(ident, src):
    assert exists(src["file"]), f"{ident}: missing file {src['file']}"
    if src["kind"] == "png":
        return
    assert anchor_found(src["file"], src["anchor"]), f"{ident}: anchor not found in {src['file']}: {src['anchor']!r}"


def test_ten_questions_answered():
    assert [a["q"] for a in ANSWERS] == [f"Q{i:02d}" for i in range(1, 11)]
    for a in ANSWERS:
        assert len(a["sources"]) >= 1
        assert a["answer"].strip()


def test_at_least_three_answers_with_file_and_locator_and_two_distinct_sources():
    with_locator = [a for a in ANSWERS if all(s[1] for s in a["sources"])]
    cross = [a for a in ANSWERS if len({s[0].split("/")[0] for s in a["sources"]}) >= 2]
    assert len(with_locator) >= 3
    assert len(cross) >= 2


def test_every_action_has_owner_evidence_and_deadline():
    for a in ACTIONS:
        assert a["owner"] and a["owner_status"], a["id"]
        assert a["evidence"], a["id"]
        assert a["due"], a["id"]


def test_three_conditions_linked_to_actions():
    ids = {a["id"] for a in ACTIONS}
    assert len(CONDITIONS) == 3
    for c in CONDITIONS:
        assert c["actions"] and set(c["actions"]) <= ids


def test_referenced_fact_ids_exist():
    known = {f["id"] for f in FACTS} | {r["id"] for r in REFERENCE} | {c["id"] for c in CONTRADICTIONS}
    for a in ANSWERS:
        for ref in a["facts"]:
            assert ref in known, (a["q"], ref)
    for c in CONTRADICTIONS:
        for ref in c["sources"]:
            assert ref in known, (c["id"], ref)


def test_budget_is_consistent():
    b = budget_summary()
    assert b["authorized"] == 204_000
    assert b["invoiced"] == 186_000
    assert b["paid"] == 132_000
    assert b["pending"] == 54_000
    assert b["billable_ok"] == 168_000


def test_no_em_dash_in_deliverable_text():
    for path in list((ROOT / "nova").glob("*.py")) + list((ROOT / "tests").glob("*.py")):
        assert "\u2014" not in path.read_text(encoding="utf-8"), path.name


def test_no_external_script_in_site_template():
    from nova.build import TEMPLATE_HEAD, TEMPLATE_TAIL

    page = TEMPLATE_HEAD + TEMPLATE_TAIL
    assert "<script src=" not in page and "cdn" not in page.lower()


def test_update_is_added_and_baseline_kept(tmp_path):
    import json

    from nova.build import updates_html
    from nova.updates import load_updates

    (tmp_path / "U01.json").write_text(json.dumps({
        "id": "U01", "received": "2026-10-01T10:00", "summary": "Mise à jour synthétique",
        "kind": "statut", "source": {"file": "updates/U01.json", "anchor": "Mise", "kind": "json"},
        "approval": "none", "impacts": [{"action": "A03", "field": "status", "before": "TODO", "after": "fait"}],
    }), encoding="utf-8")
    updates = load_updates(tmp_path)
    assert len(updates) == 1 and updates[0]["id"] == "U01"
    rendered = updates_html(tmp_path)
    assert "U01" in rendered and "Mise à jour synthétique" in rendered and "Baseline conservé" in rendered
    # the baseline is not modified by an update
    assert len(FACTS) == 41 and len(ACTIONS) == 10


def test_every_identifier_mentioned_in_text_exists():
    """A reference like "(F26)" in any text must point to an existing item."""
    import re

    from nova.answers import ANSWERS as ANS
    from nova.data import CONDITIONS as COND

    known = {f["id"] for f in FACTS} | {r["id"] for r in REFERENCE} | {c["id"] for c in CONTRADICTIONS} | {a["id"] for a in ACTIONS}
    known |= {a["q"] for a in ANS}
    texts = []
    texts += [f["summary"] + " " + f["status"] for f in FACTS]
    texts += [r["summary"] for r in REFERENCE]
    texts += [c["claims"] + " " + c["resolution"] for c in CONTRADICTIONS]
    texts += [a["action"] + " " + a["evidence"] + " " + a["due"] + " " + a["condition"] for a in ACTIONS]
    texts += [a["answer"] + " " + a["nuance"] for a in ANS]
    texts += [c["status"] for c in COND]
    pattern = re.compile(r"\b(?:F|R|X|A)\d{2}\b")
    for t in texts:
        for ref in pattern.findall(t):
            assert ref in known, f"unknown reference {ref} in: {t[:80]}"
