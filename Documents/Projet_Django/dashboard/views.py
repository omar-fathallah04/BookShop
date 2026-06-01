from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.db.models import Count, Sum
from django.shortcuts import render

from orders.models import Order, OrderItem
from products.models import Product


@staff_member_required
def index(request):
    revenue = Order.objects.exclude(status=Order.CANCELLED).aggregate(total=Sum("total_amount"))["total"] or 0
    best_sellers = (
        OrderItem.objects.values("product__title")
        .annotate(total_sold=Sum("quantity"))
        .order_by("-total_sold")[:5]
    )
    status_counts = Order.objects.values("status").annotate(total=Count("id")).order_by("status")
    context = {
        "products_count": Product.objects.count(),
        "clients_count": User.objects.filter(is_staff=False).count(),
        "orders_count": Order.objects.count(),
        "revenue": revenue,
        "best_sellers": best_sellers,
        "recent_orders": Order.objects.select_related("user")[:8],
        "status_counts": status_counts,
    }
    return render(request, "dashboard/index.html", context)
