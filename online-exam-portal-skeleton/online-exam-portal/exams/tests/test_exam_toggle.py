"""Tests for OEP-F-009: activating and deactivating examinations."""

from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from exams.models import Exam
from exams.services import get_available_exams_for


class ExamToggleTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            "admin", password="Pass@12345", is_staff=True
        )
        self.student = User.objects.create_user(
            "student", password="Pass@12345"
        )
        now = timezone.now()
        self.exam = Exam.objects.create(
            title="Current exam",
            description="Available to students",
            duration_minutes=30,
            start_time=now - timedelta(minutes=5),
            end_time=now + timedelta(hours=1),
            created_by=self.admin,
        )
        self.url = reverse("exams:exam_toggle", kwargs={"pk": self.exam.pk})

    def test_admin_can_deactivate_exam_and_hide_it_from_students(self):
        self.client.force_login(self.admin)

        response = self.client.post(self.url)

        self.assertRedirects(
            response, reverse("exams:exam_list"), fetch_redirect_response=False
        )
        self.exam.refresh_from_db()
        self.assertFalse(self.exam.is_active)
        self.assertNotIn(self.exam, get_available_exams_for(self.student))

    def test_admin_can_reactivate_exam(self):
        self.exam.is_active = False
        self.exam.save(update_fields=["is_active"])
        self.client.force_login(self.admin)

        self.client.post(self.url)

        self.exam.refresh_from_db()
        self.assertTrue(self.exam.is_active)
        self.assertIn(self.exam, get_available_exams_for(self.student))

    def test_get_request_does_not_change_exam_state(self):
        self.client.force_login(self.admin)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 405)
        self.exam.refresh_from_db()
        self.assertTrue(self.exam.is_active)

    def test_student_cannot_toggle_exam(self):
        self.client.force_login(self.student)

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 403)
        self.exam.refresh_from_db()
        self.assertTrue(self.exam.is_active)

    def test_anonymous_user_is_sent_to_login(self):
        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response["Location"])
        self.exam.refresh_from_db()
        self.assertTrue(self.exam.is_active)
