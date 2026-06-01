from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="CustomerProfile",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("phone", models.CharField(blank=True, max_length=30, verbose_name="telephone")),
                ("address", models.TextField(blank=True, verbose_name="adresse")),
                ("city", models.CharField(blank=True, max_length=80, verbose_name="ville")),
                ("postal_code", models.CharField(blank=True, max_length=20, verbose_name="code postal")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("user", models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name="profile", to=settings.AUTH_USER_MODEL)),
            ],
            options={"verbose_name": "profil client", "verbose_name_plural": "profils clients"},
        ),
    ]
