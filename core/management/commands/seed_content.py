from django.core.management.base import BaseCommand
from django.utils import timezone

from core.content import RESOURCES_SEED
from core.models import Article

BODIES = {
    "instructions-bceao-mars-2025": """
<p>Le 18 mars 2025, la BCEAO a adopté trois instructions qui opérationnalisent la
loi uniforme UEMOA du 31 mars 2023 relative à la lutte contre le blanchiment de
capitaux et le financement du terrorisme. Elles s'appliquent aux établissements
de crédit, aux compagnies financières, aux systèmes financiers décentralisés,
aux établissements de monnaie électronique et aux établissements de paiement.</p>

<h2>Ce que couvre chaque texte</h2>
<p><strong>Instruction n°001-03-2025</strong> — organisation, contrôle interne et
conformité. Elle impose une fonction conformité identifiée, des dispositifs de
contrôle documentés et des mécanismes de surveillance des opérations.</p>
<p><strong>Instruction n°002-03-2025</strong> — seuils de déclaration du
transport physique d'espèces et de titres au porteur.</p>
<p><strong>Instruction n°003-03-2025</strong> — identification, vérification de
l'identité et connaissance de la clientèle.</p>

<h2>La conséquence opérationnelle la moins commentée</h2>
<p>Ces textes déplacent la charge de la preuve. Il ne suffit plus de disposer
d'une procédure : il faut pouvoir démontrer, chiffres à l'appui, que le
dispositif est appliqué. Cette démonstration suppose un référentiel client dont
la qualité est mesurée et suivie dans le temps — ce que très peu
d'établissements de la zone savent aujourd'hui produire.</p>

<h2>Par où commencer</h2>
<p>Avant d'investir dans un outil de surveillance, mesurez la fiabilité de votre
référentiel : taux de complétude par champ obligatoire, part des dossiers
personnes morales sans bénéficiaire effectif, ancienneté médiane de la dernière
mise à jour, volume de doublons. Ces quatre chiffres déterminent le niveau de
confiance que vous pouvez accorder à n'importe quel dispositif de détection
branché en aval.</p>
""",
    "mesurer-fiabilite-referentiel-kyc": """
<p>Un score de fiabilité n'a de valeur que s'il est défendable. Voici la
décomposition en cinq dimensions que nous utilisons, et pourquoi chacune compte
séparément.</p>

<h2>1. Complétude</h2>
<p>Part des champs obligatoires effectivement renseignés, pondérée par la
criticité réglementaire du champ. Un numéro de téléphone manquant et un
bénéficiaire effectif manquant ne pèsent pas le même poids.</p>

<h2>2. Validité</h2>
<p>Le champ est renseigné, mais la valeur est-elle plausible ? Pièce d'identité
non expirée, format de numéro cohérent avec le pays, date de naissance
compatible avec la majorité légale.</p>

<h2>3. Cohérence</h2>
<p>Contrôles croisés entre champs : profession déclarée compatible avec le
segment, adresse cohérente avec l'agence de rattachement, nationalité cohérente
avec le type de pièce fournie.</p>

<h2>4. Fraîcheur</h2>
<p>Ancienneté de la dernière revue du dossier, rapportée à la périodicité
attendue pour le niveau de risque du client. Un client à risque élevé revu il y
a trois ans est une anomalie ; un client à risque faible dans le même cas ne
l'est pas nécessairement.</p>

<h2>5. Unicité</h2>
<p>Absence de doublon. C'est la dimension la plus souvent oubliée et la plus
coûteuse : un client dupliqué fausse simultanément son scoring de risque et les
seuils de surveillance appliqués à ses flux.</p>

<h2>Quels seuils viser</h2>
<p>La première année, un objectif réaliste est de porter la complétude des
champs critiques au-delà de 90 % et de ramener le taux de doublons sous 1 %. La
progression du score compte davantage que sa valeur absolue : c'est la tendance
que le superviseur regarde.</p>
""",
    "faux-positifs-seuils-fixes": """
<p>Le paramétrage par seuils fixes reste la norme dans la plupart des
établissements de la zone : au-delà de tel montant, ou de tel nombre
d'opérations, une alerte se déclenche. Ce choix a une conséquence mécanique.</p>

<h2>Le problème du seuil unique</h2>
<p>Appliqué à une clientèle hétérogène, un seuil unique est simultanément trop
bas pour les gros commerçants — qui déclenchent des alertes en permanence sans
que rien d'anormal ne se produise — et trop haut pour les particuliers modestes,
chez qui un flux réellement atypique passe sous le radar. Le résultat est un
taux de faux positifs qui dépasse couramment 95 %, et une équipe conformité qui
traite du volume au lieu de traiter du risque.</p>

<h2>Le profil comportemental, sans jargon</h2>
<p>L'alternative consiste à construire, pour chaque client, une référence de ce
qui est normal <em>pour lui</em> : montant habituel, fréquence habituelle,
contreparties habituelles, saisonnalité. L'alerte se déclenche alors sur l'écart
à cette référence, pas sur une valeur absolue. Un virement de 500 000 FCFA n'est
pas suspect chez un client qui en reçoit chaque mois ; il l'est chez un client
dont le flux mensuel n'a jamais dépassé 50 000 FCFA.</p>

<h2>La condition préalable</h2>
<p>Cette approche suppose un historique propre et un client correctement
identifié. Si le même client existe sous trois identités, son profil de
référence sera construit sur un tiers de ses flux — et l'écart mesuré n'aura
aucun sens. C'est la raison pour laquelle nous déconseillons de déployer un
moteur comportemental avant d'avoir traité les doublons.</p>

<h2>Rester explicable</h2>
<p>Quelle que soit la sophistication du moteur, chaque alerte doit afficher la
règle déclenchée et les valeurs en cause. Une alerte qu'un analyste ne peut pas
justifier devant un inspecteur est une alerte inutilisable.</p>
""",
}


class Command(BaseCommand):
    help = "Crée les articles de démarrage de la rubrique Ressources."

    def add_arguments(self, parser):
        parser.add_argument(
            "--publish",
            action="store_true",
            help="Publie immédiatement les articles (par défaut ils restent en brouillon).",
        )

    def handle(self, *args, **options):
        publish = options["publish"]
        created = 0
        for i, seed in enumerate(RESOURCES_SEED):
            obj, was_created = Article.objects.get_or_create(
                slug=seed["slug"],
                defaults={
                    "title": seed["title"],
                    "category": seed["category"],
                    "excerpt": seed["excerpt"],
                    "body": BODIES.get(seed["slug"], "<p>À rédiger.</p>").strip(),
                    "reading_minutes": seed["reading_minutes"],
                    "is_published": publish,
                    "published_at": timezone.localdate(),
                },
            )
            if was_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"{created} article(s) créé(s), "
                f"{Article.objects.count()} au total "
                f"({'publiés' if publish else 'en brouillon'})."
            )
        )
