from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class AuthenticationTests(TestCase):

    def test_login_with_valid_credentials(self):
        User.objects.create_user(
            username="student1",
            password="SafePass!4821",
        )

        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "student1",
                "password": "SafePass!4821",
            },
        )

        self.assertRedirects(
            response, "/",
            fetch_redirect_response=False,
        )
        self.assertTrue(
            User.objects.filter(username="student1").exists()
        )

    def test_login_with_invalid_password(self):
        User.objects.create_user(
            username="student1",
            password="SafePass!4821",
        )

        response = self.client.post(
            reverse("accounts:login"),
            {
                "username": "student1",
                "password": "wrong-password",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.wsgi_request.user.is_authenticated)

    def test_registration_creates_user(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "newstudent",
                "email": "student@example.com",
                "password": "UniquePass!8392",
                "confirm_password": "UniquePass!8392",
            },
        )

        self.assertRedirects(
            response,
            reverse("accounts:login"),
            fetch_redirect_response=False,
        )
        self.assertTrue(
            User.objects.filter(username="newstudent").exists()
        )

    def test_registration_rejects_mismatched_passwords(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "newstudent",
                "email": "student@example.com",
                "password": "UniquePass!8392",
                "confirm_password": "DifferentPass!8392",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertFalse(
            User.objects.filter(username="newstudent").exists()
        )

    def test_logout_requires_post(self):
        user = User.objects.create_user(
            username="student1",
            password="SafePass!4821",
        )
        self.client.force_login(user)

        response = self.client.get(reverse("accounts:logout"))

        self.assertEqual(response.status_code, 405)

    def test_logout_post_logs_user_out(self):
        user = User.objects.create_user(
            username="student1",
            password="SafePass!4821",
        )
        self.client.force_login(user)

        response = self.client.post(reverse("accounts:logout"))

        self.assertRedirects(
            response,
            reverse("accounts:login"),
            fetch_redirect_response=False,
        )
        self.assertNotIn("_auth_user_id", self.client.session)