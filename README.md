# NOVA : mémoire de reprise (défi Projet 360)

Dossier documentaire navigable sur l'état du projet NOVA au 30 septembre 2026, 09 h 00 (Montréal). Chaque affirmation renvoie à un fichier du corpus et à un repère vérifiable.

## Ouvrir

- `site/index.html` : le dossier complet, un seul fichier, hors ligne.
- `BRIEF.md` : la reprise en une page.

## Régénérer

```bash
python -m nova.build        # écrit site/index.html et BRIEF.md
python -m pytest -q         # 117 contrôles
```

## Corpus

Le dossier `corpus/Projet360_NOVA_ETUDIANTS/` contient les 64 fichiers du défi. Les données sont fictives (README du défi). Les tests de citations lisent ce dossier ; `NOVA_CORPUS` permet de pointer ailleurs.

## Contenu

| Élément | Fichier |
|---|---|
| 10 réponses (Q01-Q10), avec sources et nuances | `nova/answers.py` |
| Chronologie (41 faits), références, contradictions, actions, budget | `nova/data.py` |
| Générateur du site et du brief | `nova/build.py` |
| Lecture du corpus et vérification des repères | `nova/corpus.py` |
| Mises à jour après l'événement (un fichier par information) | `nova/updates.py`, dossier `updates/` |
| Contrôles : repères présents, actions complètes, identifiants valides | `tests/test_nova.py` |

## Méthode

1. Lecture de chaque fichier : courriels décodés, transcriptions, tickets, logs, captures d'écran (lecture visuelle), PDF (`pdftotext`), classeurs (`openpyxl`, avec commentaires et cellules).
2. Séparation des types d'information : proposition, décision, validation, livraison, statut, information. Une proposition n'est pas une décision; une livraison n'est pas une validation.
3. Hiérarchie d'autorité : décision de comité ou ADR > ticket fermé ou accepté > rapport de statut > courriel ou brouillon. Une source en double (PJ identique à un fichier séparé, copie d'archive) n'est comptée qu'une fois.
4. Chaque action a un responsable (« confirmé » si nommé dans le corpus, « proposé » sinon), une preuve et une échéance (« à confirmer » si absente du corpus).

## Mises à jour après l'événement

Le baseline n'est jamais modifié. Chaque information nouvelle est ajoutée comme un fichier JSON dans `updates/` (schéma dans `nova/updates.py`) : type, source, approbation nommée ou non, et impacts sur les actions (avant, après). Elle apparaît dans la section *Mise à jour* du site. Sans approbation nommée, une information est présentée comme une proposition.

## Limites

- Compte rendu signé du comité du 10 septembre absent (X12); compte rendu du 26 septembre absent, seule une transcription partielle (X11).
- Aucune validation technique distincte de la migration Canada Central (A08).
- Les échéances « à confirmer » ne figurent pas dans le corpus.
- La capture du runbook date du 25 septembre; aucune version plus récente.
- Les notes personnelles non signées et la newsletter ne sont pas utilisées comme faits.
