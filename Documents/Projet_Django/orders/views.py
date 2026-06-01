from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

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
    orders = request.user.orders.prefetch_related("items__product")
    return render(request, "orders/history.html", {"orders": orders})


@login_required
def detail(request, pk):
    order = get_object_or_404(Order.objects.prefetch_related("items__product"), pk=pk, user=request.user)
    return render(request, "orders/detail.html", {"order": order})
