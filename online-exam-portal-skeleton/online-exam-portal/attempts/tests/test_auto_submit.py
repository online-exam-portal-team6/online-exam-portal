"""Tests for deadline-based automatic submission (OEP-F-019)."""

from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from attempts.models import Attempt
from attempts.services import submit_attempt
from exams.models import Exam


class AutoSubmitTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            "auto_student", password="Pass@12345"
        )
        self.other = User.objects.create_user(
            "auto_other", password="Pass@12345"
        )
        self.admin = User.objects.create_user(
            "auto_admin", password="Pass@12345", is_staff=True
        )
        now = timezone.now()
        self.exam = Exam.objects.create(
            title="Auto Submit Test",
            description="Deadline submission",
            duration_minutes=30,
            start_time=now - timedelta(minutes=5),
            end_time=now + timedelta(hours=1),
            created_by=self.admin,
        )
        self.attempt = Attempt.objects.create(
            student=self.student,
            exam=self.exam,
            started_at=now,
            deadline_at=now + timedelta(minutes=20),
        )
        self.submit_url = reverse(
            "attempts:exam_submit", args=[self.attempt.pk]
        )

    def test_expired_attempt_is_automatically_submitted_by_service(self):
        self.attempt.deadline_at = timezone.now() - timedelta(seconds=1)
        self.attempt.save(update_fields=["deadline_at"])

        submitted = submit_attempt(self.attempt)

        self.assertEqual(submitted.status, Attempt.Status.AUTO_SUBMITTED)
        self.assertIsNotNone(submitted.submitted_at)

    def test_expired_attempt_is_auto_submitted_through_endpoint(self):
        self.attempt.deadline_at = timezone.now() - timedelta(seconds=1)
        self.attempt.save(update_fields=["deadline_at"])
        self.client.force_login(self.student)

        response = self.client.post(self.submit_url)

        self.assertRedirects(
            response,
            reverse("results:result_detail", args=[self.attempt.pk]),
            fetch_redirect_response=False,
        )
        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.status, Attempt.Status.AUTO_SUBMITTED)
        self.assertIsNotNone(self.attempt.submitted_at)

    def test_submission_before_deadline_is_manual(self):
        self.client.force_login(self.student)

        self.client.post(self.submit_url)

        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.status, Attempt.Status.SUBMITTED)

    def test_other_student_cannot_submit_attempt(self):
        self.client.force_login(self.other)

        response = self.client.post(self.submit_url)

        self.assertEqual(response.status_code, 404)
        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.status, Attempt.Status.IN_PROGRESS)
