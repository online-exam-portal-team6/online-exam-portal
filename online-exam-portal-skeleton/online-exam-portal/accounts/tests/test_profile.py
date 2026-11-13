from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class StudentProfileTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            username="student1", password="Pass@12345", first_name="Asha",
            last_name="Rao", email="asha@example.com",
        )
        self.admin = User.objects.create_user(
            username="admin1", password="Pass@12345", is_staff=True,
        )
        self.url = reverse("accounts:profile")

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response["Location"])

    def test_student_can_view_own_profile(self):
        self.client.force_login(self.student)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "asha@example.com")
        self.assertContains(response, "Asha")

    def test_student_can_update_own_profile(self):
        self.client.force_login(self.student)
        response = self.client.post(self.url, {
            "first_name": "Ananya", "last_name": "Sharma",
            "email": "ananya@example.com",
        })
        self.assertRedirects(response, self.url)
        self.student.refresh_from_db()
        self.assertEqual(self.student.first_name, "Ananya")
        self.assertEqual(self.student.last_name, "Sharma")
        self.assertEqual(self.student.email, "ananya@example.com")

    def test_username_and_privileges_are_not_editable(self):
        self.client.force_login(self.student)
        self.client.post(self.url, {
            "username": "admin1", "first_name": "Asha", "last_name": "Rao",
            "email": "asha@example.com", "is_staff": "on", "is_superuser": "on",
        })
        self.student.refresh_from_db()
        self.assertEqual(self.student.username, "student1")
        self.assertFalse(self.student.is_staff)
        self.assertFalse(self.student.is_superuser)

    def test_duplicate_email_is_rejected(self):
        User.objects.create_user("student2", password="Pass@12345", email="other@example.com")
        self.client.force_login(self.student)
        response = self.client.post(self.url, {
            "first_name": "Asha", "last_name": "Rao", "email": "other@example.com",
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "An account with this email already exists.")
        self.student.refresh_from_db()
        self.assertEqual(self.student.email, "asha@example.com")

    def test_admin_cannot_open_student_profile(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(self.url).status_code, 403)
