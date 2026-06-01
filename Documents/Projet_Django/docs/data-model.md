# Modele de donnees minimal

| Entite | Description |
| --- | --- |
| User | Utilisateur Django : client, administrateur ou gestionnaire. |
| CustomerProfile | Telephone, adresse, ville et code postal du client. |
| Category | Categorie de livres. |
| Product | Livre vendu : titre, auteur, description, prix, image, stock, disponibilite. |
| Cart | Panier associe a un client. |
| CartItem | Ligne de panier avec produit et quantite. |
| Order | Commande validee avec client, total, statut, adresse et date. |
| OrderItem | Ligne de commande avec produit, quantite et prix unitaire. |
| Review | Avis client avec note et commentaire. |
