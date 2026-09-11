# Mise en ligne sur Railway

Le dépôt contient tout ce qu'il faut : `Dockerfile`, `.dockerignore` et
`railway.json`. Railway construit l'image, applique les migrations, sème les
articles de démarrage puis lance Gunicorn.

Durée : une quinzaine de minutes, dont l'essentiel en attente du premier build.

---

## 1. Créer le projet et la base

1. Sur <https://railway.app>, **New Project → Deploy from GitHub repo**, puis
   choisissez `fallzy2211/konformix-site`.
2. Dans le projet créé, **New → Database → Add PostgreSQL**.

Railway injecte alors automatiquement `DATABASE_URL` dans le service web. Rien
à recopier à la main.

## 2. Générer la clé secrète

Sur votre poste :

```bash
python -c "import secrets; print(secrets.token_urlsafe(64))"
```

Gardez la chaîne obtenue pour l'étape suivante. Elle ne doit jamais être
committée ni réutilisée d'un environnement à l'autre.

## 3. Renseigner les variables

Service web → onglet **Variables** → **Raw Editor**, puis collez ceci en
remplaçant la clé secrète et l'adresse de notification :

```env
DJANGO_SECRET_KEY=collez-ici-la-chaine-generee
DJANGO_DEBUG=False
DJANGO_LOG_LEVEL=INFO
WEB_CONCURRENCY=3

BRAND_NAME=Konformix
BRAND_LEGAL_NAME=Konformix SUARL
BRAND_TAGLINE=La conformité bancaire, industrialisée.
BRAND_DOMAIN=konformix.com
BRAND_EMAIL=contact@konformix.com
BRAND_SALES_EMAIL=commercial@konformix.com
BRAND_PHONE=+221 00 000 00 00
BRAND_ADDRESS=Dakar, Sénégal
BRAND_LINKEDIN=https://www.linkedin.com/company/konformix

DJANGO_EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
DEFAULT_FROM_EMAIL=contact@konformix.com
LEAD_NOTIFICATION_EMAILS=commercial@konformix.com
```

`DJANGO_ALLOWED_HOSTS` et `DJANGO_CSRF_TRUSTED_ORIGINS` ne sont pas nécessaires
tant que vous restez sur le domaine `*.up.railway.app` : `config/settings.py`
lit `RAILWAY_PUBLIC_DOMAIN` et l'autorise de lui-même.

## 4. Publier le service

Service web → **Settings → Networking → Generate Domain**. Railway attribue une
adresse en `*.up.railway.app` et relance le déploiement.

Le déploiement est réussi quand la sonde `/healthz` répond. Cette adresse teste
aussi la connexion à la base : si elle échoue, le problème vient de PostgreSQL,
pas de Django.

## 5. Créer le compte d'administration

Service web → onglet **Deployments** → bouton de terminal, ou en local avec la
ligne de commande Railway :

```bash
railway run python manage.py createsuperuser
```

L'administration est ensuite sur `https://votre-domaine/admin/`.

---

## Domaine propre

1. Service web → **Settings → Networking → Custom Domain**, saisissez
   `konformix.com`, puis créez chez votre registrar l'enregistrement CNAME que
   Railway affiche.
2. Ajoutez ensuite ces deux variables, le domaine attribué par Railway ne
   couvrant pas le vôtre :

```env
DJANGO_ALLOWED_HOSTS=konformix.com,www.konformix.com
DJANGO_CSRF_TRUSTED_ORIGINS=https://konformix.com,https://www.konformix.com
```

Le certificat TLS est émis par Railway. La redirection vers HTTPS, l'en-tête
HSTS et les cookies sécurisés s'activent seuls dès que `DJANGO_DEBUG=False`.

## Envoi réel des e-mails

Tant que `DJANGO_EMAIL_BACKEND` reste sur la console, les demandes de
démonstration sont enregistrées en base et consultables dans l'administration,
mais aucun message ne part. Pour recevoir les alertes :

```env
DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.votre-fournisseur.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=...
EMAIL_HOST_PASSWORD=...
```

## Ce que fait chaque déploiement

| Étape | Commande | Où c'est défini |
|---|---|---|
| Construction | `pip install`, puis `collectstatic` | `Dockerfile` |
| Avant bascule | `migrate --noinput` puis `seed_content --publish` | `railway.json` |
| Exécution | Gunicorn sur le port fourni par l'hébergeur | `Dockerfile` |
| Contrôle | appel de `/healthz` | `railway.json` |

`seed_content` ne crée un article que s'il n'existe pas déjà : le rejouer à
chaque déploiement n'écrase aucune modification faite depuis l'administration.

## Si quelque chose ne va pas

| Symptôme | Cause la plus fréquente |
|---|---|
| `DisallowedHost` | domaine propre ajouté sans mettre à jour `DJANGO_ALLOWED_HOSTS` |
| Échec CSRF à l'envoi du formulaire | `DJANGO_CSRF_TRUSTED_ORIGINS` sans le préfixe `https://` |
| Page sans mise en forme | `collectstatic` en échec au build, à lire dans les journaux de construction |
| Sonde de santé en échec | base PostgreSQL non rattachée, donc `DATABASE_URL` absente |
| Boucle de redirection | terminaison TLS en amont mal détectée, vérifiez que `DJANGO_DEBUG` vaut bien `False` |

Les journaux se lisent dans l'onglet **Deployments** du service, section
**Build Logs** puis **Deploy Logs**.
