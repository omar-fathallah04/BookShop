from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models

from products.models import Product


class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="cart")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "panier"
        verbose_name_plural = "paniers"

    def __str__(self):
        return f"Panier de {self.user.username}"

    @property
    def total(self):
        return sum(item.subtotal for item in self.items.select_related("product"))


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])

    class Meta:
        verbose_name = "ligne panier"
        verbose_name_plural = "lignes panier"
        unique_together = ("cart", "product")

    def __str__(self):
        return f"{self.product} x {self.quantity}"

    @property
    def subtotal(self):
        return self.product.price * self.quantity
