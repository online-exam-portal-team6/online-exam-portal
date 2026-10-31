"""Evaluation and persisted-result tests (TC-RES-01/02/03/SEC-05)."""
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.utils import timezone

from attempts.models import Attempt, AttemptAnswer
from exams.models import Exam
from questions.models import Question
from results.models import Result
from results.services import (
    calculate_score,
    compare_submitted_answers,
    evaluate_attempt,
)


class EvaluationServiceTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            "evaluation_admin", password="Pass@12345", is_staff=True
        )
        self.student = User.objects.create_user(
            "evaluation_student", password="Pass@12345"
        )
        now = timezone.now()
        self.exam = Exam.objects.create(
            title="Weighted evaluation",
            description="Evaluation service test",
            duration_minutes=30,
            start_time=now - timedelta(minutes=5),
            end_time=now + timedelta(hours=1),
            created_by=self.admin,
            pass_percentage=Decimal("60.00"),
        )
        self.attempt = Attempt.objects.create(
            student=self.student,
            exam=self.exam,
            started_at=now,
            deadline_at=now + timedelta(minutes=20),
            status=Attempt.Status.SUBMITTED,
            submitted_at=now,
        )
        self.q1 = Question.objects.create(
            exam=self.exam,
            text="Question one",
            option_a="A",
            option_b="B",
            option_c="C",
            option_d="D",
            correct_option="B",
            marks=2,
        )
        self.q2 = Question.objects.create(
            exam=self.exam,
            text="Question two",
            option_a="A",
            option_b="B",
            option_c="C",
            option_d="D",
            correct_option="D",
            marks=3,
        )
        self.q3 = Question.objects.create(
            exam=self.exam,
            text="Question three",
            option_a="A",
            option_b="B",
            option_c="C",
            option_d="D",
            correct_option="A",
            marks=5,
        )

    def test_TC_RES_01_answers_are_compared_with_stored_correct_options(self):
        AttemptAnswer.objects.create(
            attempt=self.attempt, question=self.q1, selected_option="B"
        )
        AttemptAnswer.objects.create(
            attempt=self.attempt, question=self.q2, selected_option="C"
        )

        correct_ids, questions = compare_submitted_answers(self.attempt)

        self.assertEqual(correct_ids, {self.q1.pk})
        self.assertEqual(len(questions), 3)

    def test_TC_RES_02_score_percentage_and_pass_are_calculated_by_marks(self):
        AttemptAnswer.objects.create(
            attempt=self.attempt, question=self.q1, selected_option="B"
        )
        AttemptAnswer.objects.create(
            attempt=self.attempt, question=self.q2, selected_option="D"
        )
        AttemptAnswer.objects.create(
            attempt=self.attempt, question=self.q3, selected_option="B"
        )

        values = calculate_score(self.attempt)

        self.assertEqual(values["score"], 5)
        self.assertEqual(values["total_marks"], 10)
        self.assertEqual(values["percentage"], Decimal("50.00"))
        self.assertFalse(values["passed"])

    def test_TC_RES_02_student_passes_at_configured_threshold(self):
        AttemptAnswer.objects.create(
            attempt=self.attempt, question=self.q1, selected_option="B"
        )
        AttemptAnswer.objects.create(
            attempt=self.attempt, question=self.q2, selected_option="D"
        )

        values = calculate_score(self.attempt)

        self.assertEqual(values["score"], 5)
        self.assertEqual(values["percentage"], Decimal("50.00"))
        self.assertFalse(values["passed"])

        self.exam.pass_percentage = Decimal("50.00")
        self.exam.save(update_fields=["pass_percentage"])
        self.assertTrue(calculate_score(self.attempt)["passed"])

    def test_TC_RES_03_evaluated_result_is_persisted(self):
        AttemptAnswer.objects.create(
            attempt=self.attempt, question=self.q1, selected_option="B"
        )

        result = evaluate_attempt(self.attempt)

        self.assertEqual(Result.objects.count(), 1)
        self.assertEqual(result.attempt, self.attempt)
        self.assertEqual(result.score, 2)
        self.assertEqual(result.total_marks, 10)
        self.assertEqual(result.percentage, Decimal("20.00"))

    def test_TC_RES_03_re_evaluation_updates_instead_of_duplicating(self):
        AttemptAnswer.objects.create(
            attempt=self.attempt, question=self.q1, selected_option="B"
        )
        first = evaluate_attempt(self.attempt)
        AttemptAnswer.objects.filter(
            attempt=self.attempt, question=self.q1
        ).update(selected_option="A")

        second = evaluate_attempt(self.attempt)

        self.assertEqual(first.pk, second.pk)
        self.assertEqual(Result.objects.filter(attempt=self.attempt).count(), 1)
        self.assertEqual(second.score, 0)

    def test_TC_SEC_05_result_is_unique_per_attempt(self):
        result = evaluate_attempt(self.attempt)
        self.assertEqual(Result.objects.filter(attempt=result.attempt).count(), 1)

    def test_unsubmitted_attempt_cannot_be_evaluated(self):
        self.attempt.status = Attempt.Status.IN_PROGRESS
        self.attempt.submitted_at = None
        self.attempt.save(update_fields=["status", "submitted_at"])

        with self.assertRaises(ValidationError):
            evaluate_attempt(self.attempt)
