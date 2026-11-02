"""Tests for the platform health endpoint."""

from django.test import TestCase
from django.urls import reverse


class HealthCheckTests(TestCase):
    def test_health_check_returns_ok(self):
        response = self.client.get(reverse("health_check"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b"ok")

    def test_health_check_rejects_non_get_requests(self):
        response = self.client.post(reverse("health_check"))

        self.assertEqual(response.status_code, 405)
