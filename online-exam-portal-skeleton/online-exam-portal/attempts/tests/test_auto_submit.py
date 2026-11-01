"""Tests for deadline-based automatic submission (OEP-F-019)."""
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


class AutoSubmitTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user("auto_student", password="Pass@12345")
        self.other = User.objects.create_user("auto_other", password="Pass@12345")
        self.admin = User.objects.create_user("auto_admin", password="Pass@12345", is_staff=True)
        now = timezone.now()
        self.exam = Exam.objects.create(
            title="Auto Submit Test", description="Deadline submission",
            duration_minutes=30, start_time=now-timedelta(minutes=5),
            end_time=now+timedelta(hours=1), created_by=self.admin,
        )
        self.attempt = Attempt.objects.create(
            student=self.student, exam=self.exam, started_at=now,
            deadline_at=now+timedelta(minutes=20),
        )
        self.question = Question.objects.create(
            exam=self.exam, text="Choose B", option_a="A", option_b="B",
            option_c="C", option_d="D", correct_option="B",
        )
        Answer.objects.create(attempt=self.attempt, question=self.question, selected_option="B")

    def test_auto_submit_is_rejected_before_deadline(self):
        with self.assertRaises(ValidationError):
            submit_attempt(self.attempt, auto=True)

    def test_expired_attempt_is_automatically_graded_and_submitted(self):
        self.attempt.deadline_at = timezone.now() - timedelta(seconds=1)
        self.attempt.save(update_fields=["deadline_at"])
        submitted = submit_attempt(self.attempt, auto=True)
        self.assertEqual(submitted.status, Attempt.Status.AUTO_SUBMITTED)
        self.assertEqual(submitted.score, 1)
        self.assertEqual(submitted.total_questions, 1)
        self.assertIsNotNone(submitted.submitted_at)

    def test_exam_page_request_finalizes_attempt_after_deadline(self):
        self.attempt.deadline_at = timezone.now() - timedelta(seconds=1)
        self.attempt.save(update_fields=["deadline_at"])
        self.client.force_login(self.student)
        response = self.client.get(reverse("attempts:exam_take", args=[self.attempt.pk]))
        self.assertRedirects(response, reverse("attempts:exam_result", args=[self.attempt.pk]))
        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.status, Attempt.Status.AUTO_SUBMITTED)

    def test_auto_submit_endpoint_requires_deadline(self):
        self.client.force_login(self.student)
        response = self.client.post(reverse("attempts:exam_auto_submit", args=[self.attempt.pk]), data="{}", content_type="application/json")
        self.assertEqual(response.status_code, 400)
        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.status, Attempt.Status.IN_PROGRESS)

    def test_other_student_cannot_auto_submit_attempt(self):
        self.attempt.deadline_at = timezone.now() - timedelta(seconds=1)
        self.attempt.save(update_fields=["deadline_at"])
        self.client.force_login(self.other)
        response = self.client.post(reverse("attempts:exam_auto_submit", args=[self.attempt.pk]), data="{}", content_type="application/json")
        self.assertEqual(response.status_code, 404)
