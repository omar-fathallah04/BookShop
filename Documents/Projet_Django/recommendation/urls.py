from django.urls import path

from . import views


app_name = "recommendation"

urlpatterns = [
    path("assistant/", views.assistant, name="assistant"),
]
