from django.contrib.auth.models import User
from django.test import TestCase

from cart.models import Cart, CartItem
from products.models import Category, Product

from .models import Order


class OrderTests(TestCase):
    def test_create_order_from_cart_decreases_stock(self):
        user = User.objects.create_user("client", password="pass-strong-123")
        category = Category.objects.create(name="Essais", slug="essais")
        product = Product.objects.create(
            title="Commerce web",
            slug="commerce-web",
            description="Vente en ligne",
            price=90,
            category=category,
            stock_quantity=4,
        )
        cart = Cart.objects.create(user=user)
        CartItem.objects.create(cart=cart, product=product, quantity=2)

        order = Order.create_from_cart(
            cart,
            {"full_name": "Client Test", "address": "Rue 1", "city": "Casa", "phone": "0600000000"},
        )
        product.refresh_from_db()

        self.assertEqual(order.total_amount, 180)
        self.assertEqual(product.stock_quantity, 2)
        self.assertFalse(cart.items.exists())
