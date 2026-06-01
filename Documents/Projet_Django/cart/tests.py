from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from products.models import Category, Product


class CartTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user("client", password="pass-strong-123")
        category = Category.objects.create(name="Tech", slug="tech")
        self.product = Product.objects.create(
            title="Python avance",
            slug="python-avance",
            description="Programmation Python",
            price=150,
            category=category,
            stock_quantity=3,
        )

    def test_add_product_to_cart_requires_login(self):
        response = self.client.post(reverse("cart:add", args=[self.product.id]))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_can_add_product(self):
        self.client.login(username="client", password="pass-strong-123")
        self.client.post(reverse("cart:add", args=[self.product.id]))
        self.assertEqual(self.user.cart.items.count(), 1)
