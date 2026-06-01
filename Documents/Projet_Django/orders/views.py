from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from cart.views import get_cart

from .forms import CheckoutForm
from .models import Order


@login_required
def checkout(request):
    cart = get_cart(request.user)
    if not cart.items.exists():
        messages.warning(request, "Votre panier est vide.")
        return redirect("cart:detail")

    initial = {
        "full_name": request.user.get_full_name() or request.user.username,
        "address": request.user.profile.address,
        "city": request.user.profile.city,
        "phone": request.user.profile.phone,
    }
    form = CheckoutForm(request.POST or None, initial=initial)
    if form.is_valid():
        try:
            order = Order.create_from_cart(cart, form.cleaned_data)
        except ValueError as exc:
            messages.error(request, str(exc))
            return redirect("cart:detail")
        messages.success(request, "Commande validee.")
        return redirect("orders:detail", pk=order.pk)
    return render(request, "orders/checkout.html", {"form": form, "cart": cart})


@login_required
def history(request):
    if request.user.is_staff:
        # Admin voit toutes les commandes
        orders = Order.objects.select_related("user").prefetch_related("items__product").order_by("-created_at")
    else:
        # Client voit seulement ses commandes
        orders = request.user.orders.prefetch_related("items__product")
    return render(request, "orders/history.html", {"orders": orders})


@login_required
def detail(request, pk):
    if request.user.is_staff:
        # Admin peut voir les détails de toutes les commandes
        order = get_object_or_404(Order.objects.prefetch_related("items__product"), pk=pk)
    else:
        # Client ne voit que ses propres commandes
        order = get_object_or_404(Order.objects.prefetch_related("items__product"), pk=pk, user=request.user)
    return render(request, "orders/detail.html", {"order": order})


@staff_member_required
@require_POST
def update_order_status(request, pk):
    order = get_object_or_404(Order, pk=pk)
    new_status = request.POST.get("status")
    
    if new_status not in dict(Order.STATUS_CHOICES):
        messages.error(request, "Statut invalide.")
        return redirect("orders:detail", pk=order.pk)
    
    old_status = order.get_status_display()
    order.status = new_status
    order.save(update_fields=["status"])
    
    new_status_display = order.get_status_display()
    messages.success(request, f"Commande #{{ order.id }} : statut mis à jour de '{old_status}' à '{new_status_display}'.")
    return redirect("orders:detail", pk=order.pk)


