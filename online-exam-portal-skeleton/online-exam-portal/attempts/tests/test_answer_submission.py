"""Answer saving and submission tests (TC-EXAM-08 / TC-EXAM-09)."""

import json
from datetime import timedelta
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from attempts.models import Attempt, AttemptAnswer
from exams.models import Exam
from questions.models import Question


class AnswerAndSubmissionTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user("answer_student", password="Pass@12345")
        self.other_student = User.objects.create_user("other_answer_student", password="Pass@12345")
        self.admin = User.objects.create_user("answer_admin", password="Pass@12345", is_staff=True)
        now = timezone.now()
        self.exam = Exam.objects.create(
            title="Answer API assessment",
            description="Endpoint test",
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
        self.question = Question.objects.create(
            exam=self.exam,
            text="Which is a Python collection?",
            option_a="def",
            option_b="class",
            option_c="list",
            option_d="return",
            correct_option="C",
        )
        self.answer_url = reverse("attempts:save_answer", args=[self.attempt.pk])
        self.submit_url = reverse("attempts:exam_submit", args=[self.attempt.pk])
        self.client.force_login(self.student)

    def post_answer(self, payload):
        return self.client.post(
            self.answer_url,
            data=json.dumps(payload),
            content_type="application/json",
        )

    def test_TC_EXAM_08_student_can_save_selected_option(self):
        response = self.post_answer(
            {"question_id": self.question.pk, "option": "B"}
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["option"], "B")
        self.assertTrue(response.json()["ok"])
        self.assertEqual(
            AttemptAnswer.objects.get(attempt=self.attempt, question=self.question).selected_option,
            "B",
        )

    def test_TC_EXAM_08_student_can_change_saved_option(self):
        self.post_answer({"question_id": self.question.pk, "option": "A"})
        response = self.post_answer({"question_id": self.question.pk, "option": "C"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["option"], "C")
        self.assertEqual(AttemptAnswer.objects.filter(attempt=self.attempt).count(), 1)

    def test_TC_EXAM_08_question_from_another_exam_is_rejected(self):
        other_exam = Exam.objects.create(
            title="Other assessment",
            description="Not this attempt",
            duration_minutes=20,
            start_time=timezone.now() - timedelta(minutes=1),
            end_time=timezone.now() + timedelta(hours=1),
            created_by=self.admin,
        )
        other_question = Question.objects.create(
            exam=other_exam,
            text="Other question",
            option_a="A",
            option_b="B",
            option_c="C",
            option_d="D",
            correct_option="A",
        )

        response = self.post_answer(
            {"question_id": other_question.pk, "option": "A"}
        )

        self.assertEqual(response.status_code, 400)
        self.assertFalse(AttemptAnswer.objects.exists())

    def test_TC_EXAM_08_invalid_option_is_rejected(self):
        response = self.post_answer(
            {"question_id": self.question.pk, "option": "E"}
        )
        self.assertEqual(response.status_code, 400)
        self.assertFalse(AttemptAnswer.objects.exists())

    def test_TC_EXAM_08_malformed_json_is_rejected(self):
        response = self.client.post(
            self.answer_url,
            data="{",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 400)

    def test_TC_EXAM_08_expired_attempt_cannot_save_answer(self):
        self.attempt.deadline_at = timezone.now() - timedelta(seconds=1)
        self.attempt.save()

        response = self.post_answer(
            {"question_id": self.question.pk, "option": "A"}
        )

        self.assertEqual(response.status_code, 403)
        self.assertTrue(response.json()["expired"])
        self.assertFalse(AttemptAnswer.objects.exists())

    def test_TC_EXAM_08_another_student_cannot_save_answer(self):
        self.client.force_login(self.other_student)
        response = self.post_answer(
            {"question_id": self.question.pk, "option": "A"}
        )
        self.assertEqual(response.status_code, 404)

    def test_TC_EXAM_09_manual_submission_records_attempt_and_evaluates(self):
        with patch("results.services.evaluate_attempt") as evaluator:
            response = self.client.post(self.submit_url)

        self.attempt.refresh_from_db()
        self.assertRedirects(
            response,
            reverse("results:result_detail", args=[self.attempt.pk]),
            fetch_redirect_response=False,
        )
        self.assertEqual(self.attempt.status, Attempt.Status.SUBMITTED)
        self.assertIsNotNone(self.attempt.submitted_at)
        evaluator.assert_called_once()

    def test_TC_EXAM_09_expired_attempt_is_auto_submitted(self):
        self.attempt.deadline_at = timezone.now() - timedelta(seconds=1)
        self.attempt.save()

        with patch("results.services.evaluate_attempt") as evaluator:
            self.client.post(self.submit_url)

        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.status, Attempt.Status.AUTO_SUBMITTED)
        evaluator.assert_called_once()

    def test_TC_EXAM_09_submission_is_idempotent(self):
        with patch("results.services.evaluate_attempt") as evaluator:
            self.client.post(self.submit_url)
            submitted_at = Attempt.objects.get(pk=self.attempt.pk).submitted_at
            self.client.post(self.submit_url)

        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.status, Attempt.Status.SUBMITTED)
        self.assertEqual(self.attempt.submitted_at, submitted_at)
        evaluator.assert_called_once()

    def test_TC_EXAM_09_admin_cannot_submit_student_attempt(self):
        self.client.force_login(self.admin)
        response = self.client.post(self.submit_url)
        self.assertEqual(response.status_code, 403)
        self.attempt.refresh_from_db()
        self.assertEqual(self.attempt.status, Attempt.Status.IN_PROGRESS)
