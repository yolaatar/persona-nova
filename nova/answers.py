"""Answers to the ten initial questions of README.txt, as of the 30 Sep 2026 baseline.

Each answer gives: the answer, the nuance the grid rewards, and sources with a
precise locator (file + anchor, validated by tests). Fact ids (F..., R..., X...)
point to data.py.
"""

ANSWERS = [
    dict(
        q="Q01",
        question="Quelle est la date de mise en production actuellement approuvée, et avec quelle réserve?",
        answer=(
            "**22 octobre 2026**, approuvée par le comité de direction du 10 septembre. "
            "Réserve : cette date est **conditionnelle** à trois éléments (sécurité SEC-210, fermeture de ACC-303, runbook approuvé "
            "avec rollback). Ce n'est pas un go garanti. Le 15 octobre n'est plus la date cible."
        ),
        nuance="Le 15 octobre reste dans le plan v2, le plan v3 et la charte : ces documents ne sont pas à jour (X01).",
        facts=["F19", "F36", "F39", "X01"],
        sources=[
            ("02_Reunions/M04_Transcript_Comite_direction_10sept.txt", "Donc **approuvé**. Le 22 devient la date officielle.", "transcription 15:25"),
            ("02_Reunions/M06_Transcript_Comite_26sept.txt", "c'est conditionnel à ces trois éléments", "transcription 10:15"),
            ("01_Courriels/E09_Rappel_mise_en_production.eml", "Merci de ne pas communiquer le 22 comme un go garanti", "courriel du 27 sept"),
        ],
    ),
    dict(
        q="Q02",
        question="Pourquoi la date a-t-elle changé, et quel est l'état actuel de la cause initiale?",
        answer=(
            "Le **connecteur interne** a coûté plus de temps que prévu (Boréal, courriel du 8 sept et comité du 10 sept). "
            "La cause initiale : le **jeton de service a expiré après le changement de secret**, sans tentative de renouvellement "
            "(INT-101, logs 2026-09-05). **État** : correctif déployé le 17 sept (rotation du secret et correction du renouvellement), "
            "120 recherches rejouées avec 120 réponses valides, ticket fermé par Marc Gervais."
        ),
        nuance=("Fermé en intégration, pas démontré en production. Le registre des risques (R-01) reste « Ouvert » avec un suivi au 9 septembre (X10). "
                "Le comité ajoute d'autres raisons : stabilisation, reprise des tests intégrés et marge pour les anomalies bloquantes (M04 15:04)."),
        facts=["F15", "F16", "F17", "F19", "F25", "F40", "X10"],
        sources=[
            ("03_Tickets/INT-101.txt", "Résolution : rotation du secret", "résolution du ticket"),
            ("03_Tickets/INT-101_extrait_logs.txt", "refresh_attempt=false", "logs 2026-09-05T11:15:03Z"),
            ("01_Courriels/E12_Resolution_integration.eml", "120/120 recherches ont retourné les résultats attendus", "courriel du 17 sept"),
            ("04_Documents_projet/Registre_Risques_29sept.xlsx", "Suivi au 9 septembre 2026", "Risques!H2"),
        ],
    ),
    dict(
        q="Q03",
        question="Qui a approuvé le changement et quand? Distinguez proposition et approbation.",
        answer=(
            "**Proposition** : Julien Moreau (Boréal), courriel du 8 septembre à 11 h 16 : « il s'agit d'une proposition de notre part. "
            "À vous de confirmer la décision de gouvernance ». **Approbation** : comité de direction du **10 septembre 2026** (15 h 22 à 15 h 25). "
            "Élodie Caron, chargée de projet à ce moment, formule la décision et la déclare approuvée. Sophie Lambert, Marc Gervais et "
            "Olivier Côté répondent « Non » à l'objection, Nicolas Perron dit « D'accord »."
        ),
        nuance=("Pas de compte rendu signé du comité dans le corpus. Mélissa Gagnon et Camille Beaulieu ne se prononcent pas explicitement (X12). "
                "Confirmée ensuite par Nicolas (Teams du 15 sept) et par son courriel du 27 sept."),
        facts=["F17", "F19", "F23", "F39", "X12"],
        sources=[
            ("01_Courriels/E05_Retard_integration.eml", "il s'agit d'une proposition de notre part", "courriel du 8 sept 11:16"),
            ("02_Reunions/M04_Transcript_Comite_direction_10sept.txt", "Est-ce que quelqu'un s'oppose?", "transcription 15:22"),
            ("02_Reunions/M04_Transcript_Comite_direction_10sept.txt", "Donc **approuvé**", "transcription 15:25"),
        ],
    ),
    dict(
        q="Q04",
        question="Qui est responsable du projet et depuis quand?",
        answer=(
            "**Nicolas Perron**, chargé de projet depuis le **16 septembre 2026** (transfert officiel). "
            "Élodie Caron l'était du 7 juillet au 15 septembre."
        ),
        nuance="Le plan v3 daté du 12 septembre désigne déjà Nicolas Perron pour P-06, avant le transfert (X02).",
        facts=["F01", "F21", "F24", "X02"],
        sources=[
            ("01_Courriels/E06_Transition_charge_projet.eml", "Nicolas Perron prend officiellement la charge du projet NOVA", "courriel du 16 sept 08:35"),
            ("07_Conversations_Teams/Teams_16sept_Transition.txt", "Nicolas reprend officiellement NOVA", "Teams 16 sept 08:45"),
            ("04_Documents_projet/Note_transition_Elodie_16sept.txt", "Nicolas Perron reprend le rôle de chargé de projet NOVA", "note de transition"),
        ],
    ),
    dict(
        q="Q05",
        question="Quel est le montant contractuel autorisé et comment se calcule-t-il?",
        answer=(
            "**Contrat initial : 180 000 $ CAD** (HT, plafond). **Autorisé : 204 000 $ CAD** = 180 000 $ + 24 000 $ "
            "de la demande CR-01 approuvée le 14 août 2026 (comité de projet). Le CR-04 (18 000 $) est un brouillon : "
            "exclu de l'autorisé."
        ),
        nuance=("Hypothèse : une demande de changement approuvée est autorisée. Le contrat lui-même reste à 180 000 $. "
                "Au 30 septembre : facturé 186 000 $ (dont 18 000 $ non autorisés), payé 132 000 $, en validation 54 000 $."),
        facts=["R01", "F07", "R05"],
        sources=[
            ("05_Contrats_et_finances/CONTRAT_Boreal_NOVA.pdf", "Montant maximal initial", "page 1, Valeur contractuelle"),
            ("05_Contrats_et_finances/CONTRAT_Boreal_NOVA.pdf", "Tout travail hors portée", "page 1, Gestion des changements"),
            ("05_Contrats_et_finances/CR-01_Rapports_avances_APPROUVE.pdf", "APPROUVÉE", "page 1, Impact financier"),
        ],
    ),
    dict(
        q="Q06",
        question="Quel problème présente INV-003? Précisez le montant concerné et le traitement à prévoir.",
        answer=(
            "INV-003 (54 000 $, en validation, 22 sept) contient une ligne **« Optimisation interface mobile - CR-04 » de 18 000 $**. "
            "CR-04 est un brouillon sans approbation, reporté à la phase 2, et aucune dépense ne doit être facturée sans approbation. "
            "**Traitement** : ne pas libérer les 18 000 $; demander à Boréal une facture corrigée ou un avoir; "
            "le jalon 3 (36 000 $) ne se libère qu'après validation du jalon (à confirmer)."
        ),
        nuance="La question de Finances (23 sept) est sans réponse dans le corpus.",
        facts=["F32", "F33", "F34", "R05", "X08"],
        sources=[
            ("05_Contrats_et_finances/INV-003.pdf", "Optimisation interface mobile - CR-04", "page 1, Facturation"),
            ("05_Contrats_et_finances/CR-04_Optimisation_mobile_BROUILLON.pdf", "BROUILLON - APPROBATION REQUISE", "page 1, Statut"),
            ("01_Courriels/E10_Fonction_mobile.eml", "Aucune dépense liée à CR-04 ne doit être engagée ou facturée", "courriel du 24 sept"),
        ],
    ),
    dict(
        q="Q07",
        question="Où les données de production doivent-elles être hébergées? Quelle preuve confirme la mise en œuvre?",
        answer=(
            "**Canada Central** (ADR-007 acceptée le 23 juillet 2026). Preuves : Architecture v2 (25 août, Canada Central); "
            "courriel de Boréal du 26 août (migration complétée, test de déploiement sans blocage); comité du 27 août "
            "(migration déclarée terminée par Boréal et vérifiée par l'équipe architecture)."
        ),
        nuance=("L'ADR exige une validation technique distincte avant les tests de production : aucun document de cette validation dans le corpus (A08). "
                "La PJ du courriel est identique au fichier séparé, et deux des trois preuves viennent de Boréal (X09)."),
        facts=["F04", "F05", "F10", "F11", "F12", "X09"],
        sources=[
            ("06_Architecture_et_decisions/ADR-007_Localisation_donnees.md", "L'environnement de production de NOVA sera déployé dans **Canada Central**", "section Décision"),
            ("06_Architecture_et_decisions/ADR-007_Localisation_donnees.md", "Une validation technique doit confirmer la migration", "section Conséquences"),
            ("01_Courriels/E03_Confirmation_Canada_Central.eml", "La migration des ressources prévues pour NOVA vers Canada Central est complétée", "courriel du 26 août"),
            ("02_Reunions/M03_CR_Comite_27aout.txt", "vérifiée par l'équipe architecture", "compte rendu du 27 août"),
        ],
    ),
    dict(
        q="Q08",
        question="La sécurité est-elle acceptée? Distinguez livraison et validation.",
        answer=(
            "**Non.** Livraison : Boréal a déployé un correctif de SEC-210 en validation le 19 septembre. "
            "Validation : **non acceptée**. Sophie Lambert demande de refaire son propre scénario; le ticket reste « EN VALIDATION », "
            "re-test planifié le 26 septembre. La capture montre que l'événement EXPORT_CSV n'a ni objet ni résultat."
        ),
        nuance="Le rapport de statut du 21 septembre affiche « Sécurité VERT » (X03) : c'est une livraison présentée comme une validation.",
        facts=["F22", "F28", "F29", "F38", "X03", "X07"],
        sources=[
            ("03_Tickets/SEC-210.txt", "Ne pas fermer avant validation sécurité", "commentaire du 19 sept 14:05"),
            ("03_Tickets/SEC-210.txt", "Statut maintenu EN VALIDATION", "commentaire du 26 sept 15:40"),
            ("07_Conversations_Teams/Teams_19sept_Securite.txt", "« déployé » != « accepté »", "Teams 19 sept 10:31"),
            ("03_Tickets/SEC-210_audit.png", "Une exportation CSV a été effectuée", "capture du journal d'audit"),
        ],
    ),
    dict(
        q="Q09",
        question="L'accessibilité est-elle complétée? Identifiez ce qui reste à corriger.",
        answer=(
            "**Non.** Fermés : ACC-301 (labels, 15 août) et ACC-302 (contraste, 20 août). "
            "**Reste** : ACC-303 (priorité haute, ouvert) : la popup de modification n'atteint pas le bouton Enregistrer au clavier; "
            "correctif annoncé pour la prochaine build. Le passage clavier complet des modales reste à vérifier (M03, M05)."
        ),
        nuance="Le courriel de Boréal du 20 août (« tout devrait être conforme ») n'est pas retenu comme validation (X05).",
        facts=["F08", "F09", "F12", "F26", "F27", "F37", "X05"],
        sources=[
            ("03_Tickets/ACC-303.txt", "le bouton Enregistrer n'est jamais atteint avec Tab", "commentaire du 17 sept 13:14"),
            ("03_Tickets/ACC-303.txt", "Toujours ouvert. Correctif annoncé pour la prochaine build.", "commentaire du 26 sept 11:03"),
            ("02_Reunions/M05_CR_Suivi_18sept.txt", "Un scénario de navigation clavier sur modal doit encore être vérifié", "suivi du 18 sept"),
        ],
    ),
    dict(
        q="Q10",
        question="Quelles sont les trois conditions de go-live? Précisez les travaux manquants du runbook à partir de sa capture.",
        answer=(
            "**1.** Validation sécurité de SEC-210. **2.** Fermeture de ACC-303. **3.** Approbation du runbook incluant le rollback "
            "(comité du 26 sept, confirmé par Sophie, Mélissa et Olivier). "
            "**Runbook (capture, version du 25 septembre)** : étapes 1 à 3 OK; étape 4 « Procédure de retour arrière » à **TODO**; "
            "étape 5 « Validation fonctionnelle post-déploiement » à **compléter**. Le 29 sept, Olivier n'a toujours pas reçu la version finale."
        ),
        nuance="La capture est datée du 25 septembre; le corpus ne contient pas de version plus récente.",
        facts=["F35", "F36", "F41"],
        sources=[
            ("02_Reunions/M06_Transcript_Comite_26sept.txt", "trois conditions concrètes", "transcription 10:09"),
            ("03_Tickets/OPS-601_runbook.png", "Procédure de retour arrière", "capture, étapes 4 et 5"),
            ("03_Tickets/OPS-601.txt", "Toujours pas reçu la version finale", "commentaire du 29 sept"),
        ],
    ),
]
