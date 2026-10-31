"""Administrator result register integration tests (TC-RES-05)."""
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from attempts.models import Attempt
from exams.models import Exam
from questions.models import Question
from results.services import evaluate_attempt


class AdminResultRegisterTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            "results_admin", password="Pass@12345", is_staff=True
        )
        self.student = User.objects.create_user(
            "results_student", password="Pass@12345"
        )
        now = timezone.now()
        self.exam = Exam.objects.create(
            title="Admin result exam",
            description="Admin result register test",
            duration_minutes=30,
            start_time=now - timedelta(minutes=5),
            end_time=now + timedelta(hours=1),
            created_by=self.admin,
            pass_percentage=Decimal("50.00"),
        )
        self.attempt = Attempt.objects.create(
            student=self.student,
            exam=self.exam,
            started_at=now,
            deadline_at=now + timedelta(minutes=20),
            status=Attempt.Status.SUBMITTED,
            submitted_at=now,
        )
        Question.objects.create(
            exam=self.exam,
            text="Admin result question",
            option_a="A",
            option_b="B",
            option_c="C",
            option_d="D",
            correct_option="A",
            marks=1,
        )
        evaluate_attempt(self.attempt)

    def test_TC_RES_05_admin_sees_completed_result_data(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse("results:admin_result_list"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Admin result exam")
        self.assertContains(response, self.student.username)
        self.assertContains(response, "100.00%")
        self.assertContains(response, "Passed")

    def test_TC_RES_05_student_is_forbidden_from_admin_results(self):
        self.client.force_login(self.student)

        response = self.client.get(reverse("results:admin_result_list"))

        self.assertEqual(response.status_code, 403)

    def test_TC_RES_05_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(reverse("results:admin_result_list"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response["Location"])
