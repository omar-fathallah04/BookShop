from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Category, Product, Review


class ProductCatalogTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Romans", slug="romans")
        self.product = Product.objects.create(
            title="Le livre Django",
            slug="le-livre-django",
            author="Equipe Web",
            description="Guide pratique Django et e-commerce",
            price=120,
            category=self.category,
            stock_quantity=5,
        )

    def test_catalog_search(self):
        response = self.client.get(reverse("products:list"), {"q": "django"})
        self.assertContains(response, "Le livre Django")

    def test_average_rating(self):
        user = User.objects.create_user("client", password="pass-strong-123")
        Review.objects.create(product=self.product, user=user, rating=4, comment="Bon livre")
        self.assertEqual(self.product.average_rating, 4.0)
