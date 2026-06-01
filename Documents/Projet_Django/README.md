# BookShop Django

Plateforme e-commerce Django pour la vente de livres, realisee pour le projet de fin de module 2025-2026.

## Fonctionnalites

- Inscription, connexion, profil client et roles Django.
- Catalogue de livres avec recherche, categorie, disponibilite, tri par prix/date/titre.
- Gestion CRUD des produits pour les administrateurs.
- Panier authentifie avec quantites, suppression, vidage et total.
- Commandes avec lignes, total, statut et decrement automatique du stock.
- Avis clients avec note moyenne.
- Dashboard administrateur : produits, clients, commandes, chiffre d'affaires, meilleures ventes, statuts.
- Recommandation IA par TF-IDF et similarite cosinus sur titre, auteur, categorie, description, prix et note.
- Configuration securisee par variables d'environnement, Docker, Docker Compose, Nginx, Gunicorn et CI/CD GitHub Actions.

## Installation locale

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_books
python manage.py runserver
```

Application : `http://127.0.0.1:8000/`

## Docker Compose

Un fichier `.env` local est fourni pour lancer Docker directement. Il connecte Django au service PostgreSQL `db` avec `DB_HOST=db`.

```powershell
docker compose up --build
```

Application via Django : `http://127.0.0.1:8000/`  
Application via Nginx : `http://127.0.0.1:8080/`

Commandes utiles :

```powershell
docker compose exec web python manage.py createsuperuser
docker compose exec web python manage.py seed_books
docker compose exec web python manage.py create_demo_users
docker compose exec db psql -U ecommerce_user -d ecommerce_db
```

Comptes de demonstration :

- admin : `admin` / `Admin12345!`
- client : `client` / `Client12345!`

L'administrateur peut ajouter des livres et images depuis `http://127.0.0.1:8080/products/admin/create/` ou depuis le lien `Ajouter` visible apres connexion.

## Tests

```powershell
python manage.py test
flake8 . --exclude=.venv,venv,migrations --max-line-length=120
```

## Structure

```text
accounts/        utilisateurs et profils
products/        catalogue, categories, livres, avis
cart/            panier et lignes panier
orders/          commandes et lignes commande
dashboard/       statistiques administrateur
recommendation/  IA de recommandation
templates/       interfaces Django Templates
static/          CSS
docs/            rapport et diagrammes
```
