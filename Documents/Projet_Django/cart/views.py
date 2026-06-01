from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from products.models import Product

from .models import Cart, CartItem


def get_cart(user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@login_required
def detail(request):
    cart = get_cart(request.user)
    return render(request, "cart/detail.html", {"cart": cart})


@login_required
def add(request, product_id):
    product = get_object_or_404(Product, pk=product_id, available=True)
    cart = get_cart(request.user)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
    item.quantity = min(item.quantity, product.stock_quantity)
    item.save()
    messages.success(request, "Livre ajoute au panier.")
    return redirect("cart:detail")


@login_required
def update(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    quantity = max(1, int(request.POST.get("quantity", 1)))
    item.quantity = min(quantity, item.product.stock_quantity)
    item.save()
    messages.success(request, "Panier mis a jour.")
    return redirect("cart:detail")


@login_required
def remove(request, item_id):
    item = get_object_or_404(CartItem, pk=item_id, cart__user=request.user)
    item.delete()
    messages.success(request, "Livre retire du panier.")
    return redirect("cart:detail")


@login_required
def clear(request):
    get_cart(request.user).items.all().delete()
    messages.success(request, "Panier vide.")
    return redirect("cart:detail")
