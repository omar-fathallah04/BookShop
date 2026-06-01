def cart_counter(request):
    if not request.user.is_authenticated:
        return {"cart_items_count": 0}
    cart = getattr(request.user, "cart", None)
    count = cart.items.count() if cart else 0
    return {"cart_items_count": count}
