from django.conf import settings
from django.db import models


class CustomerProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
    phone = models.CharField("telephone", max_length=30, blank=True)
    address = models.TextField("adresse", blank=True)
    city = models.CharField("ville", max_length=80, blank=True)
    postal_code = models.CharField("code postal", max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "profil client"
        verbose_name_plural = "profils clients"

    def __str__(self):
        return f"Profil de {self.user.username}"
