# Pousser ce projet sur GitHub

Le dépôt `konformix-site` est déjà créé et vide sur votre compte. L'historique Git
(deux commits) est inclus dans cette archive — vous n'avez rien à recréer.

## Windows (PowerShell ou Git Bash)

Décompressez l'archive, puis depuis le dossier `konformix-site` :

```
git remote set-url origin https://github.com/fallzy2211/konformix-site.git
git push -u origin main
```

Git vous demandera vos identifiants : entrez votre nom d'utilisateur
`fallzy2211` et, comme mot de passe, un token GitHub (pas votre mot de passe
de compte — GitHub ne l'accepte plus).

Si vous avez GitHub CLI installé, `gh auth login` une fois, puis `git push -u origin main`
suffit, sans manipuler de token.

## Vérifier avant de pousser

```
git log --oneline        # doit afficher 2 commits
git status               # doit afficher "working tree clean"
```

## Ensuite

Révoquez les tokens que vous avez partagés :
https://github.com/settings/tokens

## Faire tourner le site en local

```
python -m venv .venv
.venv\Scripts\activate          # Windows
pip install -r requirements.txt
copy .env.example .env          # puis renseignez DJANGO_SECRET_KEY
python manage.py migrate
python manage.py seed_content --publish
python manage.py createsuperuser
python manage.py runserver
```

Le site répond alors sur http://127.0.0.1:8000/ et l'administration sur /admin/.
