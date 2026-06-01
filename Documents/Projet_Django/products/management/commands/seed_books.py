from django.core.management.base import BaseCommand
from django.utils.text import slugify

from products.models import Category, Product


BOOKS = [
    ("Programmation Python", "Guido Mentor", "Informatique", 180, "Bases solides de Python pour projets web et data."),
    ("Django Professionnel", "Nadia Web", "Informatique", 220, "Architecture Django, securite, tests et deploiement."),
    (
        "Machine Learning Clair",
        "Samir Data",
        "Intelligence artificielle",
        260,
        "Introduction pratique au machine learning avec scikit-learn.",
    ),
    (
        "Roman de Casablanca",
        "Amina Rami",
        "Romans",
        95,
        "Roman contemporain autour de la ville, de la famille et du changement.",
    ),
    ("Gestion de Projet Agile", "Karim Lead", "Management", 140, "Scrum, Kanban, planification et pilotage d'equipe."),
    ("Design UX Simple", "Lina Studio", "Design", 160, "Methodes UX, interfaces lisibles et experience utilisateur."),
]


class Command(BaseCommand):
    help = "Cree des categories et livres de demonstration."

    def handle(self, *args, **options):
        for title, author, category_name, price, description in BOOKS:
            category, _ = Category.objects.get_or_create(
                name=category_name,
                defaults={"slug": slugify(category_name), "description": f"Livres de la categorie {category_name}."},
            )
            Product.objects.get_or_create(
                slug=slugify(title),
                defaults={
                    "title": title,
                    "author": author,
                    "category": category,
                    "price": price,
                    "description": description,
                    "stock_quantity": 12,
                    "available": True,
                },
            )
        self.stdout.write(self.style.SUCCESS("Livres de demonstration crees."))
