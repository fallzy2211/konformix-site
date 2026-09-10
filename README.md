# Konformix — site vitrine

Site institutionnel de **Konformix**, éditeur de logiciels de conformité pour les
banques et établissements financiers d'Afrique de l'Ouest.

Deux produits y sont présentés :

- **Konformix Kontrol** — fiabilisation et notation de la qualité des données KYC ;
- **Konformix Vigil** — profilage des clients et surveillance des transactions (LBC/FT).

Construit avec Django 5.2, sans dépendance JavaScript côté client autre qu'un
petit script pour le menu mobile.

---

## Démarrage rapide

```bash
git clone https://github.com/<votre-compte>/konformix-site.git
cd konformix-site

python -m venv .venv && source .venv/bin/activate    # Windows : .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env          # puis renseignez DJANGO_SECRET_KEY
python manage.py migrate
python manage.py seed_content --publish
python manage.py createsuperuser
python manage.py runserver
```

Le site est alors accessible sur <http://127.0.0.1:8000/> et l'administration sur
<http://127.0.0.1:8000/admin/>.

## Changer le nom de la société

Toute l'identité de marque est centralisée dans le dictionnaire `BRAND` de
`config/settings.py`, alimentable par variables d'environnement. Renommer la
société ne demande aucune modification de template :

```env
BRAND_NAME=NouveauNom
BRAND_LEGAL_NAME=NouveauNom SUARL
BRAND_DOMAIN=nouveaunom.com
BRAND_EMAIL=contact@nouveaunom.com
```

Restent à ajuster manuellement : le logo (`templates/partials/logo.html` et
`static/img/favicon.svg`), les noms de produits dans `core/content.py` et les
couleurs dans le bloc `:root` de `static/css/site.css`.

## Structure

```
config/            paramètres, routage, WSGI/ASGI
core/
  content.py       tout le contenu éditorial du site (un seul fichier à éditer)
  models.py        Lead (demandes entrantes) et Article (rubrique Ressources)
  forms.py         formulaire de contact, avec champ piège anti-robot
  views.py         vues publiques
  sitemaps.py      sitemap.xml
  management/commands/seed_content.py
templates/         base, partiels, pages
static/            CSS, JS, images
.github/workflows/ intégration continue
```

Le contenu marketing vit dans `core/content.py` : l'équipe commerciale peut le
faire évoluer sans toucher au HTML.

## Contenu éditable en ligne

Les articles de la rubrique **Ressources** sont gérés depuis l'administration
Django (`/admin/`). Trois notes de démarrage sont fournies par
`python manage.py seed_content` :

- les instructions BCEAO du 18 mars 2025 et leurs conséquences opérationnelles ;
- la méthode de mesure de la fiabilité d'un référentiel KYC en cinq indicateurs ;
- pourquoi le paramétrage par seuils fixes génère des faux positifs.

Les demandes reçues via le formulaire de contact sont consultables dans
l'administration, avec suivi « traité / non traité » et notes internes.

## Traduction FR / EN

Le site est bilingue : le sélecteur du pied de page bascule entre le français
(langue par défaut) et l'anglais. Les chaînes vivent dans `core/content.py`, les
templates et les formulaires ; le catalogue anglais est dans
`locale/en/LC_MESSAGES/`.

`makemessages` et `compilemessages` de Django dépendent des binaires GNU gettext,
absents des postes Windows. La commande `build_translations` fait le même travail
en Python pur :

```bash
pip install -r requirements-dev.txt
python manage.py build_translations            # extrait, met à jour les .po, compile les .mo
python manage.py build_translations --check    # échoue si une chaîne n'est pas traduite
```

Elle conserve les traductions déjà saisies et marque comme obsolètes les chaînes
disparues des sources. Après avoir ajouté du texte, marquez-le (`{% translate %}`
ou `{% blocktranslate %}` dans un template, `gettext_lazy` en Python), relancez la
commande, puis complétez le `msgstr` vide dans `locale/en/LC_MESSAGES/django.po`.

## Tests

```bash
pip install -r requirements-dev.txt   # polib, requis par le test du catalogue
python manage.py test
```

La suite couvre le rendu de toutes les pages publiques, la publication des
articles, la validation du formulaire (consentement obligatoire, champ piège,
e-mail invalide) et le fait que le nom de la société soit bien piloté par la
configuration.

## Déploiement

### Docker

```bash
cp .env.example .env      # renseigner les valeurs de production
docker compose up --build
```

### Hébergement classique

```bash
DJANGO_DEBUG=False python manage.py collectstatic --noinput
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

Variables indispensables en production :

| Variable | Rôle |
|---|---|
| `DJANGO_SECRET_KEY` | clé secrète, aléatoire, jamais committée |
| `DJANGO_DEBUG` | `False` |
| `DJANGO_ALLOWED_HOSTS` | `konformix.com,www.konformix.com` |
| `DJANGO_CSRF_TRUSTED_ORIGINS` | `https://konformix.com,https://www.konformix.com` |
| `DATABASE_URL` | connexion PostgreSQL |
| `EMAIL_HOST`, `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD` | notification des demandes |
| `LEAD_NOTIFICATION_EMAILS` | destinataires des alertes commerciales |

En production, les en-têtes de sécurité (HSTS, cookies `Secure`, redirection
HTTPS, `X-Frame-Options: DENY`) s'activent automatiquement dès que
`DJANGO_DEBUG=False`. Vérifiez la configuration avec :

```bash
python manage.py check --deploy
```

## SEO

`sitemap.xml` et `robots.txt` sont générés dynamiquement, les balises
Open Graph et le JSON-LD `Organization` sont présents sur toutes les pages, et
chaque page définit son `<title>`, sa méta-description et son URL canonique.

## Licence

Code sous licence MIT (voir `LICENSE`). Les contenus rédactionnels, la marque
Konformix et le logo restent la propriété de leurs auteurs.
