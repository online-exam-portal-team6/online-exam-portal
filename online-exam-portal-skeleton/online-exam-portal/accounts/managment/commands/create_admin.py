import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Create the production admin account if it does not exist."

    def handle(self, *args, **kwargs):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL")
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD")

        if not username:
            raise CommandError("DJANGO_SUPERUSER_USERNAME is missing.")

        User = get_user_model()
        existing_user = User.objects.filter(username=username).first()

        if existing_user:
            if not existing_user.is_superuser:
                raise CommandError(
                    "This username already exists but is not a superuser."
                )

            self.stdout.write("Admin account already exists.")
            return

        if not email or not password:
            raise CommandError("Admin email or password is missing.")

        User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
        )

        self.stdout.write(
            self.style.SUCCESS("Admin account created successfully.")
        )