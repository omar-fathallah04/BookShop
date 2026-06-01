from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "quantity", "unit_price")


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("order_id", "customer_name", "status", "total_amount", "created_at")
    list_editable = ("status",)
    list_filter = ("status", "created_at", "user")
    search_fields = ("user__username", "full_name", "phone")
    readonly_fields = ("created_at", "total_amount", "user")
    ordering = ("-created_at",)
    inlines = [OrderItemInline]
    actions = [
        "mark_as_confirmed",
        "mark_as_preparing",
        "mark_as_shipped",
        "mark_as_delivered",
        "mark_as_cancelled",
    ]

    fieldsets = (
        ("Information Client", {
            "fields": ("user", "full_name", "phone", "address", "city")
        }),
        ("Commande", {
            "fields": ("status", "total_amount", "created_at")
        }),
    )

    def order_id(self, obj):
        return f"#{obj.id}"
    order_id.short_description = "N° Commande"

    def customer_name(self, obj):
        return f"{obj.full_name} ({obj.user.username})"
    customer_name.short_description = "Client"

    def mark_as_confirmed(self, request, queryset):
        updated = queryset.update(status=Order.CONFIRMED)
        self.message_user(request, f"{updated} commande(s) marquée(s) comme confirmée(s).")
    mark_as_confirmed.short_description = "Marquer comme confirmée"

    def mark_as_preparing(self, request, queryset):
        updated = queryset.update(status=Order.PREPARING)
        self.message_user(request, f"{updated} commande(s) marquée(s) comme en préparation.")
    mark_as_preparing.short_description = "Marquer comme en préparation"

    def mark_as_shipped(self, request, queryset):
        updated = queryset.update(status=Order.SHIPPED)
        self.message_user(request, f"{updated} commande(s) marquée(s) comme expédiée(s).")
    mark_as_shipped.short_description = "Marquer comme expédiée"

    def mark_as_delivered(self, request, queryset):
        updated = queryset.update(status=Order.DELIVERED)
        self.message_user(request, f"{updated} commande(s) marquée(s) comme livrée(s).")
    mark_as_delivered.short_description = "Marquer comme livrée"

    def mark_as_cancelled(self, request, queryset):
        updated = queryset.update(status=Order.CANCELLED)
        self.message_user(request, f"{updated} commande(s) marquée(s) comme annulée(s).")
    mark_as_cancelled.short_description = "Marquer comme annulée"
