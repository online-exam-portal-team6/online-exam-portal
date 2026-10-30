"""Tests for starting a student attempt (OEP-F-014)."""
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from attempts.models import Attempt
from attempts.services import start_attempt
from exams.models import Exam


class StartAttemptTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user("student", password="Pass@12345")
        self.admin = User.objects.create_user("admin", password="Pass@12345", is_staff=True)
        now = timezone.now()
        self.exam = Exam.objects.create(
            title="Python Basics",
            description="Python MCQ exam",
            duration_minutes=30,
            start_time=now - timedelta(minutes=5),
            end_time=now + timedelta(hours=2),
            created_by=self.admin,
        )
        self.url = reverse("attempts:exam_start", args=[self.exam.pk])
        self.client.force_login(self.student)

    def test_TC_ATT_01_student_can_start_available_exam(self):
        response = self.client.post(self.url)
        attempt = Attempt.objects.get(student=self.student, exam=self.exam)
        self.assertRedirects(
            response,
            reverse("attempts:exam_take", args=[attempt.pk]),
            fetch_redirect_response=False,
        )
        self.assertEqual(attempt.status, Attempt.Status.IN_PROGRESS)
        self.assertEqual(attempt.deadline_at - attempt.started_at, timedelta(minutes=30))

    def test_TC_ATT_01_get_displays_exam_rules(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "attempts/exam_start.html")
        self.assertEqual(response.context["exam"], self.exam)
        self.assertTrue(response.context["is_available"])

    def test_TC_ATT_01_inactive_exam_cannot_be_started(self):
        self.exam.is_active = False
        self.exam.save()
        with self.assertRaises(ValidationError):
            start_attempt(self.student, self.exam)
        self.assertFalse(Attempt.objects.exists())

    def test_TC_ATT_01_exam_outside_window_cannot_be_started(self):
        self.exam.start_time = timezone.now() + timedelta(hours=1)
        self.exam.save()
        with self.assertRaises(ValidationError):
            start_attempt(self.student, self.exam)
        self.assertFalse(Attempt.objects.exists())

    def test_TC_ATT_01_repeated_start_returns_same_in_progress_attempt(self):
        first = start_attempt(self.student, self.exam)
        second = start_attempt(self.student, self.exam)
        self.assertEqual(first.pk, second.pk)
        self.assertEqual(Attempt.objects.count(), 1)

    def test_admin_cannot_start_student_exam(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.post(self.url).status_code, 403)
        self.assertFalse(Attempt.objects.exists())
