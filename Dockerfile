FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE=config.settings

WORKDIR /app

RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential libpq5 \
 && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# DJANGO_SKIP_DB_CHECK : la base n'est pas jointe pendant la construction, et
# collectstatic ne l'interroge pas.
RUN DJANGO_SECRET_KEY=build-only DJANGO_DEBUG=False DJANGO_SKIP_DB_CHECK=1 \
    python manage.py collectstatic --noinput

RUN useradd --create-home appuser && chown -R appuser /app
USER appuser

EXPOSE 8000

# Invoque par "sh" plutot que par le bit d'execution : celui-ci ne survit pas
# toujours a un depot clone depuis Windows.
ENTRYPOINT ["sh", "/app/docker-entrypoint.sh"]
