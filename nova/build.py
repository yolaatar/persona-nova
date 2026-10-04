"""Generate the navigable site (site/index.html) and the one-page brief (BRIEF.md)."""

from __future__ import annotations

import html
import json
from pathlib import Path

from .answers import ANSWERS
from .corpus import CORPUS
from .data import (
    ACTIONS,
    BASELINE,
    BUDGET,
    CONDITIONS,
    CONTRADICTIONS,
    FACTS,
    REFERENCE,
    SOURCE_NOTES,
    budget_summary,
)
from .updates import load_updates

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "docs"

TEMPLATE_HEAD = """<!doctype html>
<html lang="fr"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>NOVA : mémoire de reprise</title>
<style>
:root{--bg:#f7f7f5;--fg:#1d1d1b;--mut:#6b6b66;--card:#fff;--line:#e2e1dc;--acc:#1f5fa8;--red:#b3261e;--grn:#2e7d4f;--amb:#b26a00}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#161615;--fg:#eceae4;--mut:#9b9a93;--card:#1f1f1d;--line:#34332f;--acc:#8ab4f8;--red:#ff8a80;--grn:#81c995;--amb:#ffb74d}}
body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}
header{padding:18px 20px 6px}h1{font-size:20px;margin:0}header p{margin:4px 0 0;color:var(--mut)}
nav{display:flex;flex-wrap:wrap;gap:6px;padding:10px 20px;position:sticky;top:0;background:var(--bg);border-bottom:1px solid var(--line);z-index:2}
nav button{border:1px solid var(--line);background:none;color:var(--fg);border-radius:999px;padding:5px 11px;cursor:pointer;font:inherit}
nav button[aria-pressed="true"]{background:var(--fg);color:var(--bg)}
main{padding:14px 20px 40px;max-width:1040px}
input[type=search]{width:100%;box-sizing:border-box;padding:8px 10px;border:1px solid var(--line);border-radius:8px;background:var(--card);color:var(--fg);font:inherit;margin-bottom:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 14px;margin:0 0 10px}
.card h3{margin:0 0 4px;font-size:15px}.meta{color:var(--mut);font-size:12px;margin-bottom:6px}
.tag{display:inline-block;font-size:11px;border:1px solid var(--line);border-radius:6px;padding:0 6px;margin-right:4px;color:var(--mut)}
.ok{color:var(--grn)}.bad{color:var(--red)}.warn{color:var(--amb)}
ul{margin:4px 0 0 18px;padding:0}li{margin:2px 0}
code{font-family:ui-monospace,Menlo,monospace;font-size:12px;word-break:break-all}
table{width:100%;border-collapse:collapse;font-size:13px}th,td{text-align:left;vertical-align:top;padding:6px;border-bottom:1px solid var(--line)}
.hide{display:none}
</style></head>
<body>
<header><h1>NOVA : mémoire de reprise, projet 360</h1>
<p>État au 30 septembre 2026, 09 h 00 (heure de Montréal). Les faits viennent du corpus remis; chaque élément renvoie à sa source.</p></header>
<nav id="nav"></nav>
<main>
<input type="search" id="q" placeholder="Chercher un mot, une personne, un ticket, une date…" aria-label="Rechercher">
"""

TEMPLATE_TAIL = """
</main>
<script>
const sections = Array.from(document.querySelectorAll("section[data-tab]"));
const nav = document.getElementById("nav");
const q = document.getElementById("q");
let current = "brief";
function show(id){
  current = id;
  sections.forEach(s => s.classList.toggle("hide", s.dataset.tab !== id));
  nav.querySelectorAll("button").forEach(b => b.setAttribute("aria-pressed", String(b.dataset.tab === id)));
  filter();
}
function filter(){
  const term = q.value.trim().toLowerCase();
  const sec = document.querySelector(`section[data-tab="${current}"]`);
  if(!sec) return;
  sec.querySelectorAll(".card").forEach(c => {
    c.classList.toggle("hide", term !== "" && !c.textContent.toLowerCase().includes(term));
  });
}
sections.forEach(s => {
  const b = document.createElement("button");
  b.textContent = s.dataset.label; b.dataset.tab = s.dataset.tab;
  b.onclick = () => show(s.dataset.tab);
  nav.appendChild(b);
});
q.addEventListener("input", filter);
show("brief");
</script>
</body></html>
"""


def esc(s) -> str:
    return html.escape(str(s))


def fmt(x) -> str:
    """Amounts with a space as thousands separator (French style). Never touches other commas."""
    return f"{x:,}".replace(",", " ")


def md_inline(s: str) -> str:
    return esc(s).replace("**", "")


def card(title: str, body: str, meta: str = "", tags: list[str] | None = None) -> str:
    tag_html = "".join(f'<span class="tag">{esc(t)}</span>' for t in (tags or []))
    return f'<div class="card"><h3>{esc(title)}</h3><div class="meta">{tag_html}{esc(meta)}</div>{body}</div>'


def sources_html(sources) -> str:
    items = []
    for s in sources:
        file, anchor = s["file"], s["anchor"]
        note = s.get("note", "")
        loc = f' : « {esc(anchor)} »' if anchor else ""
        extra = f' ({esc(note)})' if note else ""
        items.append(f"<li><code>{esc(file)}</code>{loc}{extra}</li>")
    return "<ul>" + "".join(items) + "</ul>"


def answers_html() -> str:
    out = []
    for a in ANSWERS:
        srcs = "<ul>" + "".join(
            f"<li><code>{esc(f)}</code> : « {esc(anc)} » ({esc(loc)})</li>" for f, anc, loc in a["sources"]
        ) + "</ul>"
        body = (
            f"<p>{md_inline(a['answer'])}</p>"
            f"<p class='muted'><em>Nuance :</em> {md_inline(a['nuance'])}</p>"
            f"<details><summary>Sources et repères</summary>{srcs}</details>"
        )
        out.append(card(f"{a['q']}. {a['question']}", body, meta="Faits : " + ", ".join(a["facts"])))
    return "".join(out)


def timeline_html() -> str:
    rows = []
    for f in sorted(FACTS, key=lambda x: (x["date"], x["time"])):
        when = f["date"] + (f" {f['time']}" if f["time"] else "")
        rows.append(
            f"<div class='card'><div class='meta'>{esc(when)} · <span class='tag'>{esc(f['kind'])}</span> {esc(f['id'])}</div>"
            f"<div>{esc(f['summary'])}</div>"
            f"<div class='meta'>Statut : {esc(f['status'])}</div>"
            f"<details><summary>Sources</summary>{sources_html(f['sources'])}</details></div>"
        )
    return "".join(rows)


def decisions_html() -> str:
    rows = [f for f in FACTS if f["kind"] in ("decision", "validation", "proposition", "livraison")]
    out = []
    for f in sorted(rows, key=lambda x: x["date"]):
        out.append(card(f"{f['date']} · {f['kind']} · {f['id']}", f"<p>{esc(f['summary'])}</p>", meta=f"Statut : {f['status']}", tags=[f["kind"]]))
    out.insert(0, card("Règle de lecture", "<p>Une <b>proposition</b> n'est pas une décision. Une <b>livraison</b> n'est pas une <b>validation</b>. "
                       "Une <b>décision</b> vient d'une autorité (comité, ADR).</p>"))
    return "".join(out)


def contradictions_html() -> str:
    return "".join(
        card(f"{c['id']} · {c['topic']}",
             f"<p><b>Ce qui est affirmé :</b> {esc(c['claims'])}</p><p><b>Résolution :</b> {esc(c['resolution'])}</p>"
             f"<div class='meta'>Faits liés : {esc(', '.join(c['sources']))}</div>")
        for c in CONTRADICTIONS
    ) + card("Documents à ne pas compter comme preuves", "<ul>" + "".join(f"<li><b>{esc(n)}</b> : {esc(t)}</li>" for n, t in SOURCE_NOTES) + "</ul>")


def actions_html() -> str:
    rows = "".join(
        f"<tr><td>{esc(a['id'])}</td><td>{esc(a['priority'])}</td><td>{esc(a['action'])}</td>"
        f"<td>{esc(a['owner'])}<br><span class='muted'>{esc(a['owner_status'])}</span></td>"
        f"<td>{esc(a['evidence'])}</td><td>{esc(a['due'])}</td><td>{esc(a['condition'])}</td></tr>"
        for a in ACTIONS
    )
    cond = "".join(f"<li><b>Condition {c['n']}</b> : {esc(c['text'])} ({esc(', '.join(c['actions']))}) : {esc(c['status'])}</li>" for c in CONDITIONS)
    return card("Conditions de go-live (comité du 26 septembre)", f"<ul>{cond}</ul>") + card(
        "Actions restantes",
        "<div class='tablewrap' style='overflow-x:auto'><table><thead><tr><th>ID</th><th>Priorité</th><th>Action</th><th>Responsable</th>"
        "<th>Preuve</th><th>Échéance</th><th>Lien</th></tr></thead><tbody>" + rows + "</tbody></table></div>",
        meta="Responsable : « confirmé » = nommé dans le corpus; « proposé » = notre suggestion, à valider.",
    )


def budget_html() -> str:
    b = budget_summary()
    rows = "".join(
        f"<tr><td>{esc(i['id'])}</td><td>{fmt(i['amount'])}</td><td>{esc(i['status'])}</td><td>{esc(i['date'])}</td><td>{esc(i['note'])}</td><td>{esc(i['ref'])}</td></tr>"
        for i in BUDGET["invoices"]
    )
    body = (
        f"<table><tbody>"
        f"<tr><td>Contrat initial</td><td>{fmt(BUDGET['contract_initial'])} $</td></tr>"
        f"<tr><td>CR-01 approuvé (14 août)</td><td>{fmt(BUDGET['cr_approved'])} $</td></tr>"
        f"<tr><td><b>Autorisé</b></td><td><b>{fmt(b['authorized'])} $</b></td></tr>"
        f"<tr><td>Facturé NOVA (3 factures)</td><td>{fmt(b['invoiced'])} $</td></tr>"
        f"<tr><td>Payé</td><td>{fmt(b['paid'])} $</td></tr>"
        f"<tr><td>En validation</td><td>{fmt(b['pending'])} $ (dont {fmt(b['cr04_to_hold'])} $ CR-04 à retenir)</td></tr>"
        f"<tr><td>Facturable et autorisé à ce jour</td><td>{fmt(b['billable_ok'])} $</td></tr>"
        f"<tr><td>Autorisé non encore facturé</td><td>{fmt(b['unbilled_authorized'])} $</td></tr>"
        f"</tbody></table>"
    )
    inv = f"<div style='overflow-x:auto'><table><thead><tr><th>Facture</th><th>Montant</th><th>Statut</th><th>Date</th><th>Détail</th><th>Fait</th></tr></thead><tbody>{rows}</tbody></table></div>"
    excl = f"<p class='meta'>Exclue : {esc(BUDGET['excluded'][0]['id'])} ({fmt(BUDGET['excluded'][0]['amount'])} $, {esc(BUDGET['excluded'][0]['note'])}, {esc(BUDGET['excluded'][0]['ref'])}).</p>"
    hyp = "<p class='meta'>Hypothèse : une demande de changement approuvée est autorisée. Montants CAD hors taxes.</p>"
    return card("Budget (au 30 septembre)", body + hyp + excl) + card("Factures NOVA", inv)


def reference_html() -> str:
    return "".join(card(r["id"], f"<p>{esc(r['summary'])}</p>" + sources_html(r["sources"])) for r in REFERENCE)


def sources_index_html() -> str:
    files = sorted(p.relative_to(CORPUS).as_posix() for p in CORPUS.rglob("*") if p.is_file() and p.name != ".DS_Store")
    used: dict[str, list[str]] = {}
    for f in FACTS:
        for s in f["sources"]:
            used.setdefault(s["file"], []).append(f["id"])
    for r in REFERENCE:
        for s in r["sources"]:
            used.setdefault(s["file"], []).append(r["id"])
    for a in ANSWERS:
        for f, _, _ in a["sources"]:
            used.setdefault(f, []).append(a["q"])
    rows = "".join(
        f"<tr><td><code>{esc(f)}</code></td><td>{esc(', '.join(sorted(set(used.get(f, [])))) or 'aucun')}</td></tr>"
        for f in files
    )
    return card("Corpus (64 fichiers)", "<p class='meta'>Chemins relatifs au dossier remis. Colonne de droite : éléments de la mémoire qui citent ce fichier.</p>"
                "<div style='overflow-x:auto'><table><thead><tr><th>Fichier</th><th>Utilisé dans</th></tr></thead><tbody>" + rows + "</tbody></table></div>")


def howto_html() -> str:
    return "".join([
        card("Ouvrir", "<p>Ouvrir <code>site/index.html</code> dans un navigateur. Aucun serveur, aucune connexion, aucun abonnement requis.</p>"),
        card("Naviguer", "<ul><li><b>Brief</b> : la reprise en une page.</li><li><b>Réponses Q01 à Q10</b> : chaque réponse a ses sources et repères.</li>"
                         "<li><b>Chronologie</b>, <b>Décisions</b>, <b>Contradictions</b> : la mémoire.</li><li><b>Actions</b>, <b>Budget</b> : ce qui reste à faire.</li>"
                         "<li><b>Corpus</b> : les 64 fichiers, avec leur usage.</li><li>La zone de recherche filtre la section ouverte.</li></ul>"),
        card("Outils et méthode", "<ul><li>Lecture de chaque fichier (courriels décodés, transcriptions, tickets, captures, PDF, classeurs) avec Python (pdftotext, openpyxl, email).</li>"
                                 "<li>Les repères sont vérifiés automatiquement : chaque citation doit exister dans son fichier (<code>pytest</code>).</li>"
                                 "<li>Les captures d'écran ont été lues visuellement.</li></ul>"),
        card("Étapes manuelles", "<ul><li>Lecture des captures et du runbook (pas d'OCR).</li><li>Choix du statut « confirmé » ou « proposé » pour chaque responsable.</li>"
                                "<li>Interprétation des contradictions (section Contradictions).</li></ul>"),
        card("Limites et incertitudes", "<ul><li>Le compte rendu signé du comité du 10 septembre n'est pas dans le corpus (X12).</li>"
                                        "<li>Le compte rendu du 26 septembre n'est pas dans le corpus; seule une transcription partielle existe (X11).</li>"
                                        "<li>Aucune validation technique de la migration Canada Central (A08).</li>"
                                        "<li>Les échéances marquées « à confirmer » ne sont pas dans le corpus.</li>"
                                        "<li>Une information nouvelle sera fournie pendant le défi : voir la section Mise à jour.</li></ul>"),
    ])


def updates_html(folder=None) -> str:
    items = load_updates(folder) if folder is not None else load_updates()
    base = card("Baseline conservé", f"<p>Le baseline (30 septembre 2026, 09 h 00) reste intact dans toutes les sections ci-dessus. "
                f"Les mises à jour sont ajoutées ci-dessous, une par fichier dans <code>updates/</code>.</p>")
    if not items:
        return base + card("Aucune mise à jour à ce stade", "<p class='meta'>Aucune nouvelle information n'a été reçue dans le dossier de travail.</p>")
    cards = []
    for u in items:
        imp = "".join(
            f"<li>{esc(i['action'])} · {esc(i['field'])} : <span class='muted'>{esc(i.get('before', ''))}</span> → <b>{esc(i.get('after', ''))}</b></li>"
            for i in u["impacts"]
        ) or "<li>Aucun impact déclaré.</li>"
        src = u.get("source", {})
        cards.append(card(f"{u['id']} · {u.get('received', '')}",
                          f"<p>{esc(u['summary'])}</p><p><b>Type :</b> {esc(u['kind'])}. <b>Approbation :</b> {esc(u['approval'])}.</p>"
                          f"<p><b>Impacts sur les actions :</b></p><ul>{imp}</ul>"
                          f"<div class='meta'>Source : <code>{esc(src.get('file', ''))}</code> « {esc(src.get('anchor', ''))} »</div>"))
    return base + "".join(cards)


def build_site(out: Path = SITE) -> Path:
    out.mkdir(parents=True, exist_ok=True)
    sections = [
        ("brief", "Brief", "<div class='card'>" + brief_html() + "</div>"),
        ("answers", "Réponses Q01-Q10", answers_html()),
        ("timeline", "Chronologie", timeline_html()),
        ("decisions", "Décisions", decisions_html()),
        ("contradictions", "Contradictions", contradictions_html()),
        ("actions", "Actions", actions_html()),
        ("budget", "Budget", budget_html()),
        ("reference", "Références", reference_html()),
        ("updates", "Mise à jour", updates_html()),
        ("sources", "Corpus", sources_index_html()),
        ("howto", "Mode d'emploi", howto_html()),
    ]
    body = "".join(f'<section data-tab="{tid}" data-label="{esc(label)}" class="hide">{content}</section>' for tid, label, content in sections)
    page = TEMPLATE_HEAD + body + TEMPLATE_TAIL
    (out / "index.html").write_text(page, encoding="utf-8")
    (ROOT / "BRIEF.md").write_text(brief_md(), encoding="utf-8")
    (ROOT / "REPONSES.md").write_text(answers_md(), encoding="utf-8")
    return out / "index.html"


def answers_md() -> str:
    lines = ["# Réponses aux dix questions initiales (NOVA)", "",
             "État au 30 septembre 2026, 09 h 00. Chaque réponse renvoie à un fichier du dépôt (`corpus/Projet360_NOVA_ETUDIANTS/`). Version navigable : https://yolaatar.github.io/persona-nova/", ""]
    for a in ANSWERS:
        lines += [f"## {a['q']}. {a['question']}", "", a["answer"], "", f"*Nuance :* {a['nuance']}", "", "**Sources :**"]
        lines += [f"- `{f}` : « {anc} » ({loc})" for f, anc, loc in a["sources"]]
        lines.append("")
    return "\n".join(lines)


def brief_html() -> str:
    b = budget_summary()
    return (
        "<h3>Brief de reprise (une page)</h3>"
        "<ul>"
        "<li><b>Responsable</b> : Nicolas Perron depuis le 16 septembre 2026 (F24). Élodie Caron avant.</li>"
        "<li><b>Date approuvée</b> : <b>22 octobre 2026</b>, comité du 10 septembre (F19). <b>Conditionnelle</b> à 3 conditions (F36) : "
        "sécurité SEC-210, fermeture ACC-303, runbook avec rollback. Ce n'est pas un go garanti.</li>"
        "<li><b>Portée</b> : phase 1 (SSO, demandes, pièces jointes, workflow, suivi, rapports standards) plus CR-01 approuvée. "
        "Mobile avancé (CR-04) reporté à la phase 2 (F34).</li>"
        f"<li><b>Budget</b> : contrat 180 000 $ + CR-01 24 000 $ = <b>{fmt(b['authorized'])} $ autorisés</b> (CAD HT). "
        f"Facturé {fmt(b['invoiced'])} $, payé {fmt(b['paid'])} $, en validation {fmt(b['pending'])} $.</li>"
        "<li><b>Factures</b> : INV-001 et INV-002 payées. INV-003 (54 000 $) en validation : retenir la ligne CR-04 de 18 000 $ (A05). INV-778 (ORION) exclue.</li>"
        "<li><b>Priorités</b> : A01 SEC-210 (re-test et acceptation); A02 ACC-303 (correctif et re-test clavier); "
        "A03 runbook (rollback et validation post-déploiement); A04 plan et communications à 22 octobre; A05 INV-003; A06 rapport de statut corrigé.</li>"
        "</ul>"
    )


def brief_md() -> str:
    b = budget_summary()
    def n(x):
        return f"{x:,}".replace(",", " ")
    return f"""# Brief de reprise : NOVA (état au 30 septembre 2026, 09 h 00)

**Responsable** : Nicolas Perron, depuis le 16 septembre 2026 (F24). Élodie Caron avant cette date.

**Date approuvée** : 22 octobre 2026, comité de direction du 10 septembre (F19). Elle est **conditionnelle** à trois éléments (comité du 26 septembre, F36) : validation sécurité de SEC-210; fermeture de ACC-303; runbook approuvé avec procédure de retour arrière. Ce n'est pas un go garanti (F39). Le 15 octobre est obsolète, mais encore présent dans la charte et les plans (X01).

**Portée** : phase 1 (SSO, création et suivi de demandes, pièces jointes, workflow, tableau de suivi, rapports standards), plus CR-01 approuvée (rapports avancés, 24 000 $). Optimisation mobile avancée (CR-04) reportée à la phase 2 (F34).

**Budget** (CAD, HT) : contrat initial {n(180000)} $ + CR-01 {n(24000)} $ = **{n(b['authorized'])} $ autorisés**. Facturé {n(b['invoiced'])} $, payé {n(b['paid'])} $, en validation {n(b['pending'])} $.

**Factures** : INV-001 (60 000 $) et INV-002 (72 000 $) payées. INV-003 (54 000 $) en validation : la ligne CR-04 de 18 000 $ n'est pas approuvée et doit être retenue (A05). INV-778 concerne ORION et est exclue.

**Priorités**
1. **A01** SEC-210 : re-test par Sophie Lambert et décision d'acceptation (condition 1). Échéance à confirmer.
2. **A02** ACC-303 : correctif de la popup (focus vers Enregistrer) par Boréal, validation par Mélissa Gagnon (condition 2). Échéance à confirmer.
3. **A03** Runbook : procédure de retour arrière et validation post-déploiement, approbation par Olivier Côté (condition 3). Échéance à confirmer.
4. **A04** Plan projet et communications à 22 octobre, conditionnel (Nicolas Perron, proposé).
5. **A05** INV-003 : retenir 18 000 $, demander une facture corrigée ou un avoir.
6. **A06** Rapport de statut du 21 septembre : sécurité et accessibilité ne sont pas VERT; ne pas diffuser le message « NOVA est au vert ».

Détail, sources et contradictions : `site/index.html`.
"""


if __name__ == "__main__":
    print(build_site())
