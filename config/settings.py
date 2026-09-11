"""
Configuration Django — Site vitrine KONFORMIX.

Toute l'identité de marque est centralisée dans le bloc BRAND ci-dessous :
changer le nom de la société ne demande qu'une seule modification ici.
"""

from pathlib import Path
import os

from django.core.exceptions import ImproperlyConfigured

BASE_DIR = Path(__file__).resolve().parent.parent


def env(key, default=None):
    return os.environ.get(key, default)


def env_bool(key, default=False):
    val = os.environ.get(key)
    if val is None:
        return default
    return val.strip().lower() in {"1", "true", "yes", "on"}


def env_list(key, default=""):
    raw = os.environ.get(key, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


# ---------------------------------------------------------------------------
# IDENTITE DE MARQUE  (point unique de configuration)
# ---------------------------------------------------------------------------
BRAND = {
    "name": env("BRAND_NAME", "Konformix"),
    "legal_name": env("BRAND_LEGAL_NAME", "Konformix SUARL"),
    "tagline": env("BRAND_TAGLINE", "La conformité bancaire, industrialisée."),
    "domain": env("BRAND_DOMAIN", "konformix.com"),
    "email": env("BRAND_EMAIL", "contact@konformix.com"),
    "sales_email": env("BRAND_SALES_EMAIL", "commercial@konformix.com"),
    "phone": env("BRAND_PHONE", "+221 00 000 00 00"),
    "address": env("BRAND_ADDRESS", "Dakar, Sénégal"),
    "linkedin": env("BRAND_LINKEDIN", "https://www.linkedin.com/company/konformix"),
    "founded": "2026",
    "products": {
        "kontrol": "Konformix Kontrol",
        "vigil": "Konformix Vigil",
    },
}

# ---------------------------------------------------------------------------
# Sécurité / environnement
# ---------------------------------------------------------------------------
SECRET_KEY = env("DJANGO_SECRET_KEY", "dev-only-change-me-in-production")

# Presence d'un environnement d'hebergement gere : Railway publie ces variables
# dans chaque conteneur, y compris quand l'operateur n'en a defini aucune.
RAILWAY_PUBLIC_DOMAIN = env("RAILWAY_PUBLIC_DOMAIN")
ON_MANAGED_HOST = bool(RAILWAY_PUBLIC_DOMAIN or env("RAILWAY_ENVIRONMENT_NAME"))

# En ligne, le mode debogage ne doit jamais s'activer par oubli : il exposerait
# la configuration dans les pages d'erreur. En local, il reste actif par defaut.
DEBUG = env_bool("DJANGO_DEBUG", not ON_MANAGED_HOST)
ALLOWED_HOSTS = env_list("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1,[::1]")
CSRF_TRUSTED_ORIGINS = env_list("DJANGO_CSRF_TRUSTED_ORIGINS", "")

# Railway attribue un domaine a chaque deploiement et le publie dans
# l'environnement. On l'autorise sans intervention manuelle, sans quoi la
# premiere mise en ligne repond 400 (DisallowedHost) puis echoue en CSRF.
if RAILWAY_PUBLIC_DOMAIN:
    ALLOWED_HOSTS.append(RAILWAY_PUBLIC_DOMAIN)
    CSRF_TRUSTED_ORIGINS.append(f"https://{RAILWAY_PUBLIC_DOMAIN}")
    # La sonde de sante interrogeant le service par son domaine interne.
    ALLOWED_HOSTS.append("healthcheck.railway.app")
    private = env("RAILWAY_PRIVATE_DOMAIN")
    if private:
        ALLOWED_HOSTS.append(private)

if not DEBUG:
    SECURE_SSL_REDIRECT = env_bool("DJANGO_SECURE_SSL_REDIRECT", True)
    # La sonde de sante de l'hebergeur interroge le service en HTTP interne :
    # sans exemption, elle ne recoit qu'une redirection permanente.
    SECURE_REDIRECT_EXEMPT = [r"^healthz/?$"]
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    X_FRAME_OPTIONS = "DENY"
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_REFERRER_POLICY = "strict-origin-when-cross-origin"

# ---------------------------------------------------------------------------
# Applications
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.sitemaps",
    "django.contrib.staticfiles",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "core.context_processors.brand",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ---------------------------------------------------------------------------
# Base de données — SQLite en dev, PostgreSQL via DATABASE_URL en production
# ---------------------------------------------------------------------------
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

DATABASE_URL = env("DATABASE_URL")

# Sans base rattachee, Django retomberait sur un fichier SQLite cree dans le
# conteneur. Ce fichier disparait a chaque redemarrage et n'est pas partage avec
# l'etape de pre-deploiement : le site repondrait "no such table" sur toutes les
# pages lisant la base. Mieux vaut refuser de demarrer et le dire.
# L'etape de construction de l'image voit les variables de la plateforme mais
# pas forcement la base : collectstatic n'en a pas besoin, on lui laisse une
# sortie explicite plutot que de faire echouer le build.
SKIP_DB_CHECK = env_bool("DJANGO_SKIP_DB_CHECK", False)

if ON_MANAGED_HOST and not DATABASE_URL and not SKIP_DB_CHECK:
    raise ImproperlyConfigured(
        "DATABASE_URL est absente alors que le service tourne chez un "
        "hebergeur gere. Ajoutez une base PostgreSQL au projet, puis, dans les "
        "variables du service web, la reference DATABASE_URL=${{Postgres.DATABASE_URL}}. "
        "Voir DEPLOY.md."
    )

if DATABASE_URL:
    from urllib.parse import urlparse

    from urllib.parse import unquote

    parsed = urlparse(DATABASE_URL)
    # Les hebergeurs geres produisent des mots de passe aleatoires : le composant
    # est encode dans l'URL et doit etre decode avant d'atteindre le pilote.
    DATABASES["default"] = {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": unquote(parsed.path.lstrip("/")),
        "USER": unquote(parsed.username or ""),
        "PASSWORD": unquote(parsed.password or ""),
        "HOST": parsed.hostname,
        "PORT": parsed.port or 5432,
        "CONN_MAX_AGE": 600,
        "OPTIONS": {"sslmode": env("DJANGO_DB_SSLMODE", "prefer")},
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
     "OPTIONS": {"min_length": 12}},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------------------------
# Internationalisation — FR par défaut, EN disponible
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "fr"
LANGUAGES = [("fr", "Français"), ("en", "English")]
LOCALE_PATHS = [BASE_DIR / "locale"]
TIME_ZONE = "Africa/Dakar"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------------------------
# Fichiers statiques
# ---------------------------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
STATICFILES_DIRS = [BASE_DIR / "static"]
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage"
        if not DEBUG
        else "django.contrib.staticfiles.storage.StaticFilesStorage"
    },
}

# ---------------------------------------------------------------------------
# E-mail — les demandes de démo sont notifiées à l'équipe commerciale
# ---------------------------------------------------------------------------
EMAIL_BACKEND = env(
    "DJANGO_EMAIL_BACKEND", "django.core.mail.backends.console.EmailBackend"
)
EMAIL_HOST = env("EMAIL_HOST", "")
EMAIL_PORT = int(env("EMAIL_PORT", "587"))
EMAIL_USE_TLS = env_bool("EMAIL_USE_TLS", True)
EMAIL_HOST_USER = env("EMAIL_HOST_USER", "")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", "")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", BRAND["email"])
LEAD_NOTIFICATION_EMAILS = env_list(
    "LEAD_NOTIFICATION_EMAILS", BRAND["sales_email"]
)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "root": {"handlers": ["console"], "level": env("DJANGO_LOG_LEVEL", "INFO")},
}
