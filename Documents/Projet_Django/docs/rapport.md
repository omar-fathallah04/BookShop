# Rapport du projet - BookShop Django

## Introduction generale

BookShop Django est une plateforme e-commerce moderne developpee avec Django pour la vente de livres. Elle couvre les besoins d'un visiteur, d'un client authentifie et d'un administrateur.

## Contexte du projet

Le commerce electronique permet de presenter un catalogue, gerer les clients, suivre les commandes et analyser les ventes. Ce projet applique ces principes dans un domaine simple a comprendre : la librairie en ligne.

## Problematique

Comment concevoir, developper, securiser et deployer une plateforme e-commerce Django tout en integrant une fonctionnalite intelligente qui ameliore l'experience utilisateur ?

## Objectifs

- Concevoir une architecture Django modulaire.
- Gerer produits, categories, panier, commandes et avis.
- Proteger les acces selon les roles.
- Integrer une recommandation IA.
- Preparer l'application pour Docker, CI/CD et deploiement.

## Analyse des besoins

Le visiteur consulte le catalogue, recherche des livres, filtre par categorie et cree un compte. Le client gere son profil, son panier, ses commandes et ses avis. L'administrateur gere les produits, les stocks, les commandes et consulte les statistiques.

## Diagramme de cas d'utilisation

Voir `docs/use-case.puml`.

## Diagramme de classes

Voir `docs/class-diagram.puml`.

## Architecture technique

L'application est composee des modules `accounts`, `products`, `cart`, `orders`, `dashboard` et `recommendation`. Django Templates et Bootstrap assurent l'interface. PostgreSQL est utilise en Docker, avec SQLite possible en developpement local sans variable `DB_HOST`.

## Choix technologiques

- Backend : Django.
- Frontend : Django Templates, Bootstrap, CSS local.
- Base de donnees : PostgreSQL en production, SQLite en developpement simple.
- IA : scikit-learn, TF-IDF, similarite cosinus.
- Production : Gunicorn, Nginx, WhiteNoise.
- CI/CD : GitHub Actions.

## Description des fonctionnalites

Le catalogue affiche les livres en grille avec recherche, filtres et tris. Le panier permet l'ajout, la modification de quantite, la suppression et la validation. La commande stocke client, produits, quantites, prix unitaire, total, date et statut. Les avis permettent une note de 1 a 5 et un commentaire. Le dashboard affiche les indicateurs exiges.

## Fonctionnalite IA

Lorsqu'un client consulte un livre, le service `recommendation.services.similar_products` construit un corpus a partir du titre, auteur, categorie, description, tranche de prix et note moyenne. TF-IDF transforme les textes en vecteurs, puis la similarite cosinus classe les livres les plus proches. Le score est ensuite ajuste par des signaux metier simples : meme categorie, meme auteur, prix proche et note client elevee. L'interface affiche aussi une raison lisible pour chaque recommandation.

## Securite

Les commandes exigent l'authentification. Les mots de passe sont geres par Django. CSRF reste active. Les pages de gestion produits et dashboard utilisent `staff_member_required`. Les secrets sont externalises dans `.env`, ignore par Git.

## Deploiement

Le projet fournit `Dockerfile`, `docker-compose.yml`, `nginx.conf` et `.env`. En production, `DEBUG=False`, `SECRET_KEY` et les variables PostgreSQL doivent etre definies. Gunicorn sert Django et Nginx agit comme reverse proxy.

## Pipeline CI/CD

Le workflow `.github/workflows/ci-cd.yml` installe Python, les dependances, lance flake8, applique les migrations, execute les tests, construit l'image Docker et la publie sur GitHub Container Registry lors d'un push sur `main`.

## Captures d'ecran

Prevoir des captures de la page d'accueil, du catalogue, du detail produit, du panier, de la commande, de l'historique et du dashboard apres lancement.

## Difficultes rencontrees

Les principaux points de vigilance sont la synchronisation du stock lors de la commande, la protection des pages administrateur et la preparation du projet pour un environnement Docker reproductible.

## Conclusion et perspectives

BookShop Django repond au cahier des charges principal. Les perspectives possibles sont le paiement en ligne, la recommandation personnalisee selon l'historique, une API REST et un chatbot d'aide a l'achat.
