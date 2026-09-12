"""
Contenu éditorial du site vitrine.

Centralisé ici plutôt que dispersé dans les templates : l'équipe peut faire
évoluer le discours commercial sans toucher au HTML.
"""

from django.utils.translation import gettext_lazy as _

HERO = {
    "eyebrow": _("Logiciels de conformité pour les banques d'Afrique de l'Ouest"),
    "title": _("Vos données clients sont votre premier risque de conformité."),
    "subtitle": (
        _("Konformix industrialise les chantiers que les banques de l'UEMOA "
        "traitent encore sous Excel : la fiabilisation des dossiers KYC et la "
        "surveillance des clients et des transactions. Conçu à Dakar, pour les "
        "exigences de la BCEAO et du GIABA.")
    ),
    "cta_primary": _("Demander une démonstration"),
    "cta_secondary": _("Voir nos modules"),
}

TRUST_STATS = [
    {
        "value": "161",
        "label": _("établissements de crédit agréés dans l'UEMOA à fin 2025"),
        "source": "BCEAO",
    },
    {
        "value": "3",
        "label": _("nouvelles instructions BCEAO LBC/FT entrées en vigueur le 18 mars 2025"),
        "source": "Instructions n°001, 002 et 003-03-2025",
    },
    {
        "value": "8",
        "label": _("pays couverts par un cadre réglementaire unique"),
        "source": "Loi uniforme UEMOA du 31 mars 2023",
    },
]

PROBLEM = {
    "title": _("Le problème n'est pas le manque de règles. C'est la qualité de la donnée."),
    "intro": (
        _("Les instructions BCEAO du 18 mars 2025 ont considérablement relevé le "
        "niveau d'exigence sur l'identification du client, la connaissance du "
        "bénéficiaire effectif et le dispositif de contrôle interne. Or la "
        "plupart des établissements de la zone butent sur le même mur : un "
        "référentiel client incomplet, dupliqué et non daté, sur lequel aucun "
        "dispositif de surveillance ne peut produire de résultats fiables.")
    ),
    "pains": [
        {
            "title": _("Des dossiers KYC incomplets"),
            "icon": "id-card",
            "text": (
                _("Pièces d'identité expirées, professions non renseignées, "
                "bénéficiaires effectifs absents des dossiers personnes morales. "
                "Personne ne sait chiffrer précisément le taux de complétude.")
            ),
        },
        {
            "title": _("Des doublons clients invisibles"),
            "icon": "duplicate",
            "text": (
                _("Le même client existe sous trois identités dans le core banking. "
                "Résultat : un risque sous-évalué et des seuils de surveillance "
                "contournés sans intention.")
            ),
        },
        {
            "title": _("Des alertes ingérables"),
            "icon": "alert",
            "text": (
                _("Un paramétrage par seuils fixes produit des milliers d'alertes "
                "par mois, dont plus de 95 % de faux positifs. L'équipe conformité "
                "traite le volume, pas le risque.")
            ),
        },
        {
            "title": _("Des contrôles non traçables"),
            "icon": "clipboard-check",
            "text": (
                _("Le contrôle permanent s'exécute dans des classeurs Excel non "
                "versionnés. À l'inspection, prouver qu'un contrôle a bien été "
                "réalisé — et par qui — devient un exercice périlleux.")
            ),
        },
    ],
}

PRODUCTS = [
    {
        "key": "kontrol",
        "icon": "shield-check",
        "name": "Konformix Kontrol",
        "kicker": _("Fiabilisation et notation des données KYC"),
        "summary": (
            _("Mesure en continu la qualité du référentiel client, détecte les "
            "anomalies et pilote les campagnes de régularisation jusqu'à leur "
            "clôture.")
        ),
        "outcome": _("Passer d'un taux de complétude inconnu à un indicateur suivi mensuellement."),
        "features": [
            {
                "title": _("Score de fiabilité par dossier"),
                "icon": "gauge",
                "text": (
                    _("Chaque client reçoit une note de 0 à 100 fondée sur des règles "
                    "paramétrables : complétude, validité des pièces, cohérence "
                    "inter-champs, fraîcheur de la mise à jour, présence du "
                    "bénéficiaire effectif.")
                ),
            },
            {
                "title": _("Moteur de règles sans code"),
                "icon": "sliders",
                "text": (
                    _("Le responsable conformité crée et teste ses propres règles de "
                    "contrôle depuis l'interface, sans passer par la DSI. Chaque "
                    "règle est versionnée et horodatée.")
                ),
            },
            {
                "title": _("Détection de doublons"),
                "icon": "duplicate",
                "text": (
                    _("Rapprochement approximatif sur les noms, dates de naissance et "
                    "pièces d'identité, adapté aux graphies ouest-africaines "
                    "(variantes Mamadou/Mamadu, Ndiaye/Ndiaye/Niaye, translittérations arabes).")
                ),
            },
            {
                "title": _("Campagnes de régularisation"),
                "icon": "target",
                "text": (
                    _("Les anomalies sont affectées aux agences ou aux chargés de "
                    "clientèle, avec échéance, relance automatique et suivi du taux "
                    "de traitement par entité.")
                ),
            },
            {
                "title": _("Tableau de bord direction"),
                "icon": "chart",
                "text": (
                    _("Évolution du score global, classement des agences, top des "
                    "anomalies, projection de la date d'atteinte de la cible. "
                    "Exportable pour le comité des risques.")
                ),
            },
            {
                "title": _("Piste d'audit complète"),
                "icon": "history",
                "text": (
                    _("Qui a modifié quelle règle, quand, et quel dossier a été "
                    "régularisé par qui. Exportable au format attendu par "
                    "l'inspection et le contrôle permanent.")
                ),
            },
        ],
    },
    {
        "key": "vigil",
        "icon": "radar",
        "name": "Konformix Vigil",
        "kicker": _("Profilage des clients et surveillance des transactions"),
        "summary": (
            _("Classe les clients par niveau de risque, apprend leur comportement "
            "normal et n'alerte que sur les écarts qui méritent un examen humain.")
        ),
        "outcome": _("Réduire le volume d'alertes tout en augmentant le taux de déclarations de soupçon pertinentes."),
        "features": [
            {
                "title": _("Scoring de risque client"),
                "icon": "user-shield",
                "text": (
                    _("Notation multi-critères — pays, activité, canal de distribution, "
                    "statut PPE, structure de détention — avec pondérations "
                    "ajustables selon la cartographie des risques de l'établissement.")
                ),
            },
            {
                "title": _("Profils comportementaux"),
                "icon": "pulse",
                "text": (
                    _("Chaque client dispose d'un profil transactionnel de référence "
                    "construit sur son historique. L'alerte se déclenche sur l'écart "
                    "au profil, pas sur un seuil universel arbitraire.")
                ),
            },
            {
                "title": _("Scénarios typologiques"),
                "icon": "globe",
                "text": (
                    _("Bibliothèque de scénarios calibrés sur les typologies GIABA : "
                    "fractionnement, comptes de passage, flux transfrontaliers "
                    "atypiques, écarts entre activité déclarée et flux constatés, "
                    "mobile money vers compte bancaire.")
                ),
            },
            {
                "title": _("Filtrage des listes"),
                "icon": "list-check",
                "text": (
                    _("Criblage des clients et des donneurs d'ordre contre les listes "
                    "de sanctions, les listes nationales de gel des avoirs et les "
                    "bases de personnes politiquement exposées, avec gestion des "
                    "homonymies.")
                ),
            },
            {
                "title": _("Gestion du cycle d'alerte"),
                "icon": "file-search",
                "text": (
                    _("File d'attente priorisée, affectation, investigation "
                    "documentée, décision motivée et génération du projet de "
                    "déclaration de soupçon à destination de la CENTIF.")
                ),
            },
            {
                "title": _("Réduction des faux positifs"),
                "icon": "radar",
                "text": (
                    _("Le moteur apprend des décisions de clôture des analystes et "
                    "réordonne les alertes en conséquence — sans jamais supprimer "
                    "automatiquement une alerte, pour rester explicable en contrôle.")
                ),
            },
        ],
    },
]

DIFFERENTIATORS = [
    {
        "title": _("Calibré sur la réglementation UEMOA"),
        "icon": "scale",
        "text": (
            _("Les référentiels de contrôle sont livrés pré-paramétrés sur les "
            "instructions BCEAO n°001, 002 et 003-03-2025 et la loi uniforme du "
            "31 mars 2023 — pas sur une réglementation européenne adaptée après coup.")
        ),
    },
    {
        "title": _("Un coût aligné sur les budgets locaux"),
        "icon": "coins",
        "text": (
            _("Les solutions internationales sont facturées en devises fortes, avec "
            "des projets d'intégration de douze à dix-huit mois. Nous vendons en "
            "FCFA, avec un déploiement initial mesuré en semaines.")
        ),
    },
    {
        "title": _("Vos données restent chez vous"),
        "icon": "lock",
        "text": (
            _("Déploiement sur l'infrastructure de la banque ou en hébergement "
            "souverain régional. Aucune donnée client ne quitte le territoire, ce "
            "qui règle d'emblée la question du superviseur.")
        ),
    },
    {
        "title": _("Une équipe qui a fait le métier"),
        "icon": "team",
        "text": (
            _("Konformix est fondée par des praticiens du contrôle permanent et de "
            "la conformité bancaire en Afrique de l'Ouest. Nous connaissons la "
            "réalité d'un référentiel client de core banking, pas seulement la théorie.")
        ),
    },
]

APPROACH_STEPS = [
    {
        "step": "01",
        "title": _("Diagnostic de fiabilité"),
        "duration": _("2 semaines"),
        "text": (
            _("Extraction d'un échantillon du référentiel client, mesure du taux de "
            "complétude réel et chiffrage des anomalies. Livrable : un rapport de "
            "diagnostic chiffré, utile même sans suite commerciale.")
        ),
    },
    {
        "step": "02",
        "title": _("Pilote cadré"),
        "duration": _("6 à 8 semaines"),
        "text": (
            _("Déploiement sur un périmètre restreint — un segment de clientèle ou "
            "un réseau d'agences — avec des objectifs chiffrés convenus à l'avance.")
        ),
    },
    {
        "step": "03",
        "title": _("Généralisation"),
        "duration": _("3 mois"),
        "text": (
            _("Extension à l'ensemble du référentiel, intégration au core banking, "
            "formation des équipes conformité et contrôle permanent.")
        ),
    },
    {
        "step": "04",
        "title": _("Exploitation et veille"),
        "duration": _("en continu"),
        "text": (
            _("Mise à jour des référentiels réglementaires, ajout de scénarios, "
            "revue trimestrielle des indicateurs avec la direction de la conformité.")
        ),
    },
]

AUDIENCES = [
    {
        "role": _("Directeur de la Conformité / RCCI"),
        "icon": "shield-check",
        "need": (
            _("Démontrer au superviseur et au conseil que le dispositif LBC/FT est "
            "effectif, mesuré et documenté.")
        ),
    },
    {
        "role": _("Responsable du Contrôle Permanent"),
        "icon": "clipboard-check",
        "need": (
            _("Exécuter et tracer les contrôles de second niveau sans reconstruire "
            "un classeur Excel à chaque campagne.")
        ),
    },
    {
        "role": _("Directeur des Risques"),
        "icon": "chart",
        "need": (
            _("Disposer d'une cartographie des risques clients alimentée par des "
            "données à jour plutôt que par une enquête annuelle.")
        ),
    },
    {
        "role": _("Directeur des Systèmes d'Information"),
        "icon": "server",
        "need": (
            _("Ajouter une brique de conformité sans projet de refonte du core "
            "banking, avec une intégration par fichiers ou API.")
        ),
    },
]

FAQ = [
    {
        "q": _("Faut-il remplacer notre core banking ?"),
        "a": (
            _("Non. Konformix se connecte en lecture à votre référentiel existant, "
            "par extraction de fichiers ou par API. Aucune modification de votre "
            "système de production n'est nécessaire pour démarrer.")
        ),
    },
    {
        "q": _("Où sont hébergées les données ?"),
        "a": (
            _("Au choix : sur votre propre infrastructure, ou dans un centre de "
            "données de la région. Nous n'exportons jamais de données clients hors "
            "du périmètre que vous définissez.")
        ),
    },
    {
        "q": _("Combien de temps avant les premiers résultats ?"),
        "a": (
            _("Le diagnostic de fiabilité produit des chiffres exploitables en deux "
            "semaines. Un pilote complet est opérationnel en six à huit semaines.")
        ),
    },
    {
        "q": _("Comment se situe Konformix face aux solutions internationales ?"),
        "a": (
            _("Les plateformes internationales couvrent un périmètre fonctionnel plus "
            "large et conviennent aux grands groupes disposant d'une équipe projet "
            "dédiée. Nous nous adressons aux établissements qui ont besoin d'un "
            "dispositif effectif rapidement, à un coût cohérent avec un bilan de la "
            "zone, et pré-calibré sur la réglementation UEMOA.")
        ),
    },
    {
        "q": _("Le moteur d'alerte est-il explicable ?"),
        "a": (
            _("Oui, et c'est un choix structurant. Chaque alerte affiche la règle ou "
            "le scénario qui l'a déclenchée et les valeurs en cause. Aucune décision "
            "ne repose sur un modèle que vous ne pourriez pas justifier devant un "
            "inspecteur.")
        ),
    },
    {
        "q": _("Proposez-vous un accompagnement au-delà du logiciel ?"),
        "a": (
            _("Oui : cadrage du dispositif, rédaction des procédures associées, "
            "formation des équipes et préparation aux missions d'inspection font "
            "partie de nos prestations.")
        ),
    },
]

FOUNDERS = [
    {
        "name": "Mamadou Fallou Sylla",
        "role": _("Cofondateur — Produit & Conformité"),
        "bio": (
            _("Praticien de la conformité et du contrôle permanent en banque, "
            "concepteur de la première plateforme de notation de la fiabilité des "
            "données KYC dont Konformix Kontrol est issu.")
        ),
    },
    {
        "name": "Mansour Diop",
        "role": _("Cofondateur — Technologie & Opérations"),
        "bio": (
            _("En charge de l'architecture logicielle, des déploiements chez les "
            "établissements clients et de la sécurité de la plateforme.")
        ),
    },
]

RESOURCES_SEED = [
    {
        "title": _("Instructions BCEAO du 18 mars 2025 : ce qui change concrètement pour votre dispositif"),
        "slug": "instructions-bceao-mars-2025",
        "category": "regulation",
        "excerpt": (
            _("Les trois instructions adoptées le 18 mars 2025 opérationnalisent la "
            "loi uniforme UEMOA de 2023. Lecture pratique de leurs conséquences sur "
            "l'organisation de la conformité, le KYC et le contrôle interne.")
        ),
        "reading_minutes": 8,
    },
    {
        "title": _("Mesurer la fiabilité d'un référentiel KYC : la méthode en cinq indicateurs"),
        "slug": "mesurer-fiabilite-referentiel-kyc",
        "category": "method",
        "excerpt": (
            _("Complétude, validité, cohérence, fraîcheur, unicité. Comment "
            "construire un score de fiabilité défendable devant un inspecteur, et "
            "quels seuils viser la première année.")
        ),
        "reading_minutes": 10,
    },
    {
        "title": _("Faux positifs : pourquoi le paramétrage par seuils fixes a atteint sa limite"),
        "slug": "faux-positifs-seuils-fixes",
        "category": "method",
        "excerpt": (
            _("Un seuil unique appliqué à une clientèle hétérogène génère du bruit et "
            "manque les vrais signaux. Le passage au profil comportemental, "
            "expliqué sans jargon statistique.")
        ),
        "reading_minutes": 7,
    },
]
