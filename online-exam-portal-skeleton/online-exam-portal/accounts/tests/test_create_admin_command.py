"""Regression tests for the production administrator command (OEP-61)."""

import os
from unittest.mock import patch

from django.contrib.auth import get_user_model
from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import TestCase

User = get_user_model()

CREDENTIALS = {
    "DJANGO_SUPERUSER_USERNAME": "production_admin",
    "DJANGO_SUPERUSER_EMAIL": "admin@example.com",
    "DJANGO_SUPERUSER_PASSWORD": "Str0ng-Pass!23",
}


class CreateAdminCommandTests(TestCase):
    @patch.dict(os.environ, CREDENTIALS, clear=True)
    def test_TC_OEP_61_command_creates_superuser(self):
        call_command("create_admin")

        user = User.objects.get(
            username=CREDENTIALS["DJANGO_SUPERUSER_USERNAME"]
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertEqual(user.email, CREDENTIALS["DJANGO_SUPERUSER_EMAIL"])
        self.assertTrue(
            user.check_password(CREDENTIALS["DJANGO_SUPERUSER_PASSWORD"])
        )

    @patch.dict(os.environ, CREDENTIALS, clear=True)
    def test_TC_OEP_61_command_is_idempotent(self):
        existing = User.objects.create_superuser(
            username=CREDENTIALS["DJANGO_SUPERUSER_USERNAME"],
            email=CREDENTIALS["DJANGO_SUPERUSER_EMAIL"],
            password=CREDENTIALS["DJANGO_SUPERUSER_PASSWORD"],
        )

        call_command("create_admin")

        self.assertEqual(
            User.objects.filter(
                username=CREDENTIALS["DJANGO_SUPERUSER_USERNAME"]
            ).count(),
            1,
        )
        self.assertEqual(
            User.objects.get(
                username=CREDENTIALS["DJANGO_SUPERUSER_USERNAME"]
            ).pk,
            existing.pk,
        )

    def test_TC_OEP_61_command_requires_username(self):
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(CommandError):
                call_command("create_admin")

    @patch.dict(os.environ, CREDENTIALS, clear=True)
    def test_TC_OEP_61_command_rejects_non_superuser_conflict(self):
        User.objects.create_user(
            username=CREDENTIALS["DJANGO_SUPERUSER_USERNAME"],
            password="Different-Pass!23",
        )

        with self.assertRaises(CommandError):
            call_command("create_admin")
