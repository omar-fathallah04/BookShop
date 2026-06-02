from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Favorite, Product, Review


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("image_preview", "title", "author", "category", "price", "stock_quantity", "available", "created_at")
    list_filter = ("available", "category", "created_at")
    prepopulated_fields = {"slug": ("title",)}
    search_fields = ("title", "author", "description")
    readonly_fields = ("image_preview",)

    fieldsets = (
        (None, {"fields": ("title", "author", "slug", "category", "description", "price", "image", "stock_quantity", "available")}),
        ("Informations avancées", {"fields": ("image_preview",)}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-height: 120px; object-fit: contain;"/>', obj.image.url)
        return "Aucune image"
    image_preview.short_description = "Aperçu image"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "created_at")
    list_filter = ("rating", "created_at")
    search_fields = ("product__title", "user__username", "comment")


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("user", "product", "created_at")
    list_filter = ("created_at",)
    search_fields = ("user__username", "product__title")
