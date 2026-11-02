"""Tests for manual examination submission (OEP-F-018)."""

from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from attempts.models import Attempt
from attempts.services import submit_attempt
from exams.models import Exam
from questions.models import Question


class SubmitAttemptTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            "submit_student", password="Pass@12345"
        )
        self.other = User.objects.create_user(
            "submit_other", password="Pass@12345"
        )
        self.admin = User.objects.create_user(
            "submit_admin", password="Pass@12345", is_staff=True
        )
        now = timezone.now()
        self.exam = Exam.objects.create(
            title="Submission Test",
            description="Manual submit",
            duration_minutes=30,
            start_time=now - timedelta(minutes=5),
            end_time=now + timedelta(hours=1),
            created_by=self.admin,
        )
        Question.objects.create(
            exam=self.exam,
            text="Test question",
            option_a="Option A",
            option_b="Option B",
            option_c="Option C",
            option_d="Option D",
            correct_option=Question.Option.A,
        )
        self.attempt = Attempt.objects.create(
            student=self.student,
            exam=self.exam,
            started_at=now,
            deadline_at=now + timedelta(minutes=20),
        )

    def test_submission_finalizes_attempt(self):
        submitted = submit_attempt(self.attempt)

        self.assertEqual(submitted.status, Attempt.Status.SUBMITTED)
        self.assertIsNotNone(submitted.submitted_at)

    def test_submission_is_idempotent(self):
        first = submit_attempt(self.attempt)
        first_submitted_at = first.submitted_at

        second = submit_attempt(self.attempt)

        self.assertEqual(second.pk, first.pk)
        self.assertEqual(second.submitted_at, first_submitted_at)

    def test_expired_attempt_is_automatically_submitted(self):
        self.attempt.deadline_at = timezone.now() - timedelta(seconds=1)
        self.attempt.save(update_fields=["deadline_at"])

        submitted = submit_attempt(self.attempt)

        self.assertEqual(submitted.status, Attempt.Status.AUTO_SUBMITTED)
        self.assertIsNotNone(submitted.submitted_at)

    def test_only_attempt_owner_can_open_result(self):
        submit_attempt(self.attempt)
        self.client.force_login(self.other)

        response = self.client.get(
            reverse("results:result_detail", args=[self.attempt.pk])
        )

        self.assertEqual(response.status_code, 403)

    def test_student_can_submit_and_view_result(self):
        self.client.force_login(self.student)
        response = self.client.post(
            reverse("attempts:exam_submit", args=[self.attempt.pk])
        )

        self.assertRedirects(
            response,
            reverse("results:result_detail", args=[self.attempt.pk]),
            fetch_redirect_response=False,
        )
        result = self.client.get(
            reverse("results:result_detail", args=[self.attempt.pk])
        )
        self.assertEqual(result.status_code, 200)
        self.assertEqual(
            Attempt.objects.get(pk=self.attempt.pk).status,
            Attempt.Status.SUBMITTED,
        )
