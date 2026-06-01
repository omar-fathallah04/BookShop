from django.urls import path

from . import views


app_name = "products"

urlpatterns = [
    path("", views.product_list, name="list"),
    path("favorites/", views.favorites, name="favorites"),
    path("favorite/<int:product_id>/", views.toggle_favorite, name="toggle_favorite"),
    path("admin/create/", views.product_create, name="create"),
    path("admin/<slug:slug>/edit/", views.product_update, name="update"),
    path("admin/<slug:slug>/delete/", views.product_delete, name="delete"),
    path("<slug:slug>/", views.product_detail, name="detail"),
]
