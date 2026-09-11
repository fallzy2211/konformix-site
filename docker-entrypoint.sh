#!/bin/sh
# Demarrage du conteneur.
#
# Les migrations sont appliquees ici plutot que par une commande de
# pre-deploiement de l'hebergeur : cette etape depend d'un reglage de plateforme
# qui peut ne pas etre pris en compte, et le site repond alors "relation does
# not exist" sur toutes les pages lisant la base. migrate et seed_content sont
# idempotents, les rejouer a chaque demarrage ne coute rien.
set -e

echo "==> Migrations"
python manage.py migrate --noinput

echo "==> Contenu de demarrage"
python manage.py seed_content --publish

echo "==> Gunicorn sur le port ${PORT:-8000}"
exec gunicorn config.wsgi:application \
  --bind "0.0.0.0:${PORT:-8000}" \
  --workers "${WEB_CONCURRENCY:-3}" \
  --timeout 60 \
  --access-logfile - \
  --error-logfile -
