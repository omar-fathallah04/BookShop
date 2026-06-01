from django.contrib.auth.models import User
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Cree ou met a jour les comptes demo admin et client."

    def handle(self, *args, **options):
        admin, _ = User.objects.update_or_create(
            username="admin",
            defaults={
                "email": "admin@example.com",
                "first_name": "Admin",
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )
        admin.set_password("Admin12345!")
        admin.save()

        client, _ = User.objects.update_or_create(
            username="client",
            defaults={
                "email": "client@example.com",
                "first_name": "Client",
                "is_staff": False,
                "is_superuser": False,
                "is_active": True,
            },
        )
        client.set_password("Client12345!")
        client.save()

        self.stdout.write(self.style.SUCCESS("Comptes demo prets : admin/Admin12345! et client/Client12345!"))
