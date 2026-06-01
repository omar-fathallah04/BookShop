from django.conf import settings
from django.db import migrations, models
import django.core.validators
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True, verbose_name="nom")),
                ("slug", models.SlugField(max_length=140, unique=True)),
                ("description", models.TextField(blank=True)),
            ],
            options={"verbose_name": "categorie", "verbose_name_plural": "categories", "ordering": ["name"]},
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=180, verbose_name="titre")),
                ("slug", models.SlugField(max_length=200, unique=True)),
                ("author", models.CharField(blank=True, max_length=150, verbose_name="auteur")),
                ("description", models.TextField()),
                ("price", models.DecimalField(decimal_places=2, max_digits=9, verbose_name="prix")),
                ("image", models.ImageField(blank=True, null=True, upload_to="products/")),
                ("stock_quantity", models.PositiveIntegerField(default=0, verbose_name="quantite en stock")),
                ("available", models.BooleanField(default=True, verbose_name="disponible")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="date d'ajout")),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("category", models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name="products", to="products.category")),
            ],
            options={"verbose_name": "produit", "verbose_name_plural": "produits", "ordering": ["-created_at"]},
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("rating", models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ("comment", models.TextField(blank=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("product", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to="products.product")),
                ("user", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="reviews", to=settings.AUTH_USER_MODEL)),
            ],
            options={"verbose_name": "avis", "verbose_name_plural": "avis", "ordering": ["-created_at"], "unique_together": {("product", "user")}},
        ),
    ]
