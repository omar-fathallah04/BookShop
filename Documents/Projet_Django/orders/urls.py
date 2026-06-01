from django.urls import path

from . import views


app_name = "orders"

urlpatterns = [
    path("checkout/", views.checkout, name="checkout"),
    path("", views.history, name="history"),
    path("<int:pk>/", views.detail, name="detail"),
]
