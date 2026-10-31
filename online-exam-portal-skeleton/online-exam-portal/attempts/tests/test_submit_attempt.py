"""Tests for manual examination submission (OEP-F-018)."""
import json
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from attempts.models import Answer, Attempt
from attempts.services import submit_attempt
from exams.models import Exam
from questions.models import Question


class SubmitAttemptTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user("submit_student", password="Pass@12345")
        self.other = User.objects.create_user("submit_other", password="Pass@12345")
        self.admin = User.objects.create_user("submit_admin", password="Pass@12345", is_staff=True)
        now = timezone.now()
        self.exam = Exam.objects.create(
            title="Submission Test", description="Manual submit",
            duration_minutes=30, start_time=now-timedelta(minutes=5),
            end_time=now+timedelta(hours=1), created_by=self.admin,
        )
        self.attempt = Attempt.objects.create(
            student=self.student, exam=self.exam, started_at=now,
            deadline_at=now+timedelta(minutes=20),
        )
        self.q1 = Question.objects.create(
            exam=self.exam, text="Question one", option_a="A", option_b="B",
            option_c="C", option_d="D", correct_option="B",
        )
        self.q2 = Question.objects.create(
            exam=self.exam, text="Question two", option_a="A", option_b="B",
            option_c="C", option_d="D", correct_option="D",
        )

    def test_submission_grades_and_finalizes_attempt(self):
        Answer.objects.create(attempt=self.attempt, question=self.q1, selected_option="B")
        Answer.objects.create(attempt=self.attempt, question=self.q2, selected_option="A")
        submitted = submit_attempt(self.attempt)
        self.assertEqual(submitted.status, Attempt.Status.SUBMITTED)
        self.assertEqual(submitted.score, 1)
        self.assertEqual(submitted.total_questions, 2)
        self.assertIsNotNone(submitted.submitted_at)

    def test_submission_is_idempotent(self):
        first = submit_attempt(self.attempt)
        first_submitted_at = first.submitted_at
        second = submit_attempt(self.attempt)
        self.assertEqual(second.pk, first.pk)
        self.assertEqual(second.submitted_at, first_submitted_at)

    def test_expired_attempt_cannot_be_manually_submitted(self):
        self.attempt.deadline_at = timezone.now() - timedelta(seconds=1)
        self.attempt.save(update_fields=["deadline_at"])
        with self.assertRaises(ValidationError):
            submit_attempt(self.attempt)

    def test_only_attempt_owner_can_open_result(self):
        submitted = submit_attempt(self.attempt)
        self.client.force_login(self.other)
        response = self.client.get(reverse("attempts:exam_result", args=[submitted.pk]))
        self.assertEqual(response.status_code, 404)

    def test_student_can_submit_and_view_result(self):
        self.client.force_login(self.student)
        response = self.client.post(reverse("attempts:exam_submit", args=[self.attempt.pk]))
        self.assertRedirects(response, reverse("attempts:exam_result", args=[self.attempt.pk]))
        result = self.client.get(reverse("attempts:exam_result", args=[self.attempt.pk]))
        self.assertEqual(result.status_code, 200)
        self.assertContains(result, "EXAMINATION SUBMITTED")
        self.assertEqual(Attempt.objects.get(pk=self.attempt.pk).status, Attempt.Status.SUBMITTED)
