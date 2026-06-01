from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404, redirect, render

from recommendation.services import review_sentiment_summary, similar_products

from .forms import ProductForm, ReviewForm
from .models import Category, Favorite, Product, Review


def home(request):
    recent_products = Product.objects.filter(available=True).select_related("category")[:4]
    popular_products = (
        Product.objects.filter(available=True)
        .select_related("category")
        .annotate(sold_count=Sum("orderitem__quantity"), favorite_count=Count("favorited_by"))
        .order_by("-sold_count", "-favorite_count", "-created_at")[:4]
    )
    categories = Category.objects.annotate(products_count=Count("products")).order_by("-products_count")[:6]
    stats = {
        "products": Product.objects.count(),
        "categories": Category.objects.count(),
        "available": Product.objects.filter(available=True, stock_quantity__gt=0).count(),
    }
    return render(
        request,
        "home.html",
        {
            "recent_products": recent_products,
            "popular_products": popular_products,
            "categories": categories,
            "stats": stats,
        },
    )


def product_list(request):
    products = Product.objects.select_related("category").annotate(favorite_count=Count("favorited_by")).all()
    categories = Category.objects.all()
    query = request.GET.get("q", "").strip()
    category_slug = request.GET.get("category", "").strip()
    sort = request.GET.get("sort", "-created_at")
    available_only = request.GET.get("available") == "1"

    if query:
        products = products.filter(
            Q(title__icontains=query) | Q(author__icontains=query) | Q(description__icontains=query)
        )
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if available_only:
        products = products.filter(available=True, stock_quantity__gt=0)
    if sort in {"price", "-price", "created_at", "-created_at", "title"}:
        products = products.order_by(sort)

    favorite_ids = set()
    if request.user.is_authenticated:
        favorite_ids = set(request.user.favorites.values_list("product_id", flat=True))

    return render(
        request,
        "products/list.html",
        {
            "products": products,
            "categories": categories,
            "query": query,
            "category_slug": category_slug,
            "sort": sort,
            "favorite_ids": favorite_ids,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.select_related("category"), slug=slug)
    review_form = ReviewForm()
    _remember_recent_product(request, product)

    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("login")
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            Review.objects.update_or_create(
                product=product,
                user=request.user,
                defaults=review_form.cleaned_data,
            )
            messages.success(request, "Avis enregistre.")
            return redirect(product)

    recommendations = similar_products(product)
    review_insight = review_sentiment_summary(product)
    recent_products = _recent_products(request, exclude_pk=product.pk)
    is_favorite = request.user.is_authenticated and Favorite.objects.filter(user=request.user, product=product).exists()
    return render(
        request,
        "products/detail.html",
        {
            "product": product,
            "review_form": review_form,
            "recommendations": recommendations,
            "review_insight": review_insight,
            "recent_products": recent_products,
            "is_favorite": is_favorite,
        },
    )


@login_required
def toggle_favorite(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
    if created:
        messages.success(request, "Livre ajoute a vos favoris.")
    else:
        favorite.delete()
        messages.info(request, "Livre retire de vos favoris.")
    return redirect(request.POST.get("next") or product.get_absolute_url())


@login_required
def favorites(request):
    favorites_qs = request.user.favorites.select_related("product", "product__category")
    return render(request, "products/favorites.html", {"favorites": favorites_qs})


def _remember_recent_product(request, product):
    recent = request.session.get("recent_products", [])
    recent = [pk for pk in recent if pk != product.pk]
    recent.insert(0, product.pk)
    request.session["recent_products"] = recent[:6]


def _recent_products(request, exclude_pk=None):
    recent_ids = request.session.get("recent_products", [])
    if exclude_pk:
        recent_ids = [pk for pk in recent_ids if pk != exclude_pk]
    products = Product.objects.filter(pk__in=recent_ids).select_related("category")
    by_id = {product.pk: product for product in products}
    return [by_id[pk] for pk in recent_ids if pk in by_id]


@staff_member_required
def product_create(request):
    form = ProductForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        product = form.save()
        messages.success(request, "Livre ajoute.")
        return redirect(product)
    return render(request, "products/form.html", {"form": form, "title": "Ajouter un livre"})


@staff_member_required
def product_update(request, slug):
    product = get_object_or_404(Product, slug=slug)
    form = ProductForm(request.POST or None, request.FILES or None, instance=product)
    if form.is_valid():
        product = form.save()
        messages.success(request, "Livre modifie.")
        return redirect(product)
    return render(request, "products/form.html", {"form": form, "title": "Modifier un livre"})


@staff_member_required
def product_delete(request, slug):
    product = get_object_or_404(Product, slug=slug)
    if request.method == "POST":
        product.delete()
        messages.success(request, "Livre supprime.")
        return redirect("products:list")
    return render(request, "products/confirm_delete.html", {"product": product})
