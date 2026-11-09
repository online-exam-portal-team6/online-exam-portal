from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class StudentProfileTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            username="profile_student",
            password="Pass@12345",
            first_name="Bhu",
            last_name="Mika",
            email="student@example.com",
        )
        self.url = reverse("accounts:profile")

    def test_student_can_view_own_profile(self):
        self.client.force_login(self.student)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "profile_student")
        self.assertContains(response, "student@example.com")

    def test_student_can_update_permitted_fields(self):
        self.client.force_login(self.student)
        response = self.client.post(self.url, {
            "first_name": "Bhumi",
            "last_name": "Sharma",
            "email": "bhumi@example.com",
        })
        self.assertRedirects(response, self.url)
        self.student.refresh_from_db()
        self.assertEqual(self.student.first_name, "Bhumi")
        self.assertEqual(self.student.last_name, "Sharma")
        self.assertEqual(self.student.email, "bhumi@example.com")
        self.assertEqual(self.student.username, "profile_student")

    def test_duplicate_email_is_rejected(self):
        User.objects.create_user("another", email="taken@example.com")
        self.client.force_login(self.student)
        response = self.client.post(self.url, {
            "first_name": "Bhu",
            "last_name": "Mika",
            "email": "taken@example.com",
        })
        self.assertEqual(response.status_code, 200)
        self.student.refresh_from_db()
        self.assertNotEqual(self.student.email, "taken@example.com")

    def test_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(self.url)
        self.assertRedirects(response, f"{reverse('accounts:login')}?next={self.url}")

    def test_staff_cannot_use_student_profile(self):
        staff = User.objects.create_user("profile_staff", password="Pass@12345", is_staff=True)
        self.client.force_login(staff)
        self.assertEqual(self.client.get(self.url).status_code, 403)
