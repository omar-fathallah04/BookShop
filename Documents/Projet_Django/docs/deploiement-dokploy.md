# Deploiement Docker Hub + Dokploy

## 1. Preparation Docker Hub

Creer un repository Docker Hub nomme :

```text
bookshop-django
```

Dans GitHub, ajouter les secrets du depot :

```text
DOCKERHUB_USERNAME=votre_nom_dockerhub
DOCKERHUB_TOKEN=votre_token_dockerhub
```

Le token se cree dans Docker Hub : Account Settings -> Personal access tokens.

## 2. Pipeline CI/CD

## 4. Compose à utiliser dans Dokploy

1. recupere le code ;
2. installe Python ;
```text
docker-compose.yml
```
5. execute les tests ;
6. verifie le code avec flake8 ;
```text
DOCKERHUB_USERNAME/bookshop-django:latest
```

## 3. Variables Dokploy
```bash
docker compose exec web python manage.py create_demo_users

```env
APP_PORT=8022
DOCKER_IMAGE=votre_nom_dockerhub/bookshop-django:latest
docker compose exec web python manage.py seed_books
ALLOWED_HOSTS=84.8.221.206,localhost,127.0.0.1
CSRF_TRUSTED_ORIGINS=http://84.8.221.206:8022,http://localhost:8022,http://127.0.0.1:8022
DB_NAME=ecommerce_db
DB_USER=ecommerce_user
docker compose exec web python manage.py createsuperuser
DB_PORT=5432
SECURE_SSL_REDIRECT=False
SECURE_HSTS_SECONDS=0
```

Si Dokploy fournit HTTPS avec un domaine, mettre `SECURE_SSL_REDIRECT=True` apres verification du certificat.

## 4. Compose a utiliser dans Dokploy

Utiliser le fichier :

```text
docker-compose.yml
```

Il contient :

- `web` : application Django avec Gunicorn ;
- `db` : PostgreSQL ;
- `nginx` : reverse proxy expose sur `APP_PORT`, par defaut `8022`.

## 5. Commandes utiles apres deploiement

Creer les comptes de demonstration :

```bash
docker compose exec web python manage.py create_demo_users
```

Creer les livres de demonstration :

```bash
docker compose exec web python manage.py seed_books
```

Creer un administrateur reel :

```bash
docker compose exec web python manage.py createsuperuser
```

## 6. Securite

- Ne jamais publier `.env`.
- Les mots de passe sont geres par Django, jamais stockes en clair.
- CSRF reste active.
- Les pages admin sont protegees par authentification.
- `DEBUG=False` en production.
- PostgreSQL est utilise comme base de donnees.
- Les fichiers statiques et medias sont servis par Nginx via volumes Docker.
