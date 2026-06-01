from django.conf import settings
from django.db import models, transaction

from products.models import Product


class Order(models.Model):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PREPARING = "preparing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"

    STATUS_CHOICES = [
        (PENDING, "En attente"),
        (CONFIRMED, "Confirmee"),
        (PREPARING, "En preparation"),
        (SHIPPED, "Expediee"),
        (DELIVERED, "Livree"),
        (CANCELLED, "Annulee"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders")
    full_name = models.CharField(max_length=160)
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "commande"
        verbose_name_plural = "commandes"
        ordering = ["-created_at"]

    def __str__(self):
        return f"Commande #{self.pk} - {self.user.username}"

    @classmethod
    @transaction.atomic
    def create_from_cart(cls, cart, data):
        order = cls.objects.create(user=cart.user, **data)
        total = 0
        for item in cart.items.select_related("product"):
            product = item.product
            if item.quantity > product.stock_quantity:
                raise ValueError(f"Stock insuffisant pour {product.title}")
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item.quantity,
                unit_price=product.price,
            )
            product.stock_quantity -= item.quantity
            if product.stock_quantity == 0:
                product.available = False
            product.save(update_fields=["stock_quantity", "available", "updated_at"])
            total += product.price * item.quantity
        order.total_amount = total
        order.save(update_fields=["total_amount"])
        cart.items.all().delete()
        return order

    def set_status(self, status):
        self.status = status
        self.save(update_fields=["status"])

    def confirm(self):
        self.set_status(self.CONFIRMED)

    def prepare(self):
        self.set_status(self.PREPARING)

    def ship(self):
        self.set_status(self.SHIPPED)

    def deliver(self):
        self.set_status(self.DELIVERED)

    def cancel(self):
        self.set_status(self.CANCELLED)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        verbose_name = "ligne commande"
        verbose_name_plural = "lignes commande"

    @property
    def subtotal(self):
        return self.unit_price * self.quantity
