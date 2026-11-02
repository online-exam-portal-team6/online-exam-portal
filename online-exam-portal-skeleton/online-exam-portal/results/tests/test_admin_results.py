"""Admin result register authorization and data tests (OEP-F-024 / TC-RES-05)."""
from datetime import timedelta
from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from attempts.models import Attempt
from exams.models import Exam
from results.models import Result


class AdminResultsTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            "admin_result_viewer", password="Pass@12345", is_staff=True
        )
        self.student = User.objects.create_user(
            "student_result_viewer", password="Pass@12345"
        )
        now = timezone.now()
        self.exam = Exam.objects.create(
            title="Completed algebra exam",
            description="Admin result list test",
            duration_minutes=30,
            start_time=now - timedelta(minutes=5),
            end_time=now + timedelta(hours=1),
            created_by=self.admin,
        )
        self.completed_attempt = Attempt.objects.create(
            student=self.student,
            exam=self.exam,
            started_at=now - timedelta(minutes=30),
            deadline_at=now,
            submitted_at=now,
            status=Attempt.Status.SUBMITTED,
        )
        self.pending_attempt = Attempt.objects.create(
            student=self.student,
            exam=Exam.objects.create(
                title="Not yet submitted",
                description="Must not appear in admin results",
                duration_minutes=30,
                start_time=now - timedelta(minutes=5),
                end_time=now + timedelta(hours=1),
                created_by=self.admin,
            ),
            started_at=now,
            deadline_at=now + timedelta(minutes=30),
        )
        Result.objects.create(
            attempt=self.completed_attempt,
            student=self.student,
            exam=self.exam,
            score=8,
            total_marks=10,
            percentage=Decimal("80.00"),
            passed=True,
        )

    def test_TC_RES_05_admin_can_view_completed_results(self):
        self.client.force_login(self.admin)

        response = self.client.get(reverse("results:admin_result_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "results/admin_result_list.html")
        self.assertContains(response, "Completed algebra exam")
        self.assertContains(response, self.student.username)
        self.assertContains(response, "80.00%")
        self.assertContains(response, "Passed")
        self.assertNotContains(response, "Not yet submitted")

    def test_TC_RES_05_student_cannot_view_admin_results(self):
        self.client.force_login(self.student)

        response = self.client.get(reverse("results:admin_result_list"))

        self.assertEqual(response.status_code, 403)

    def test_TC_RES_05_anonymous_user_must_log_in(self):
        response = self.client.get(reverse("results:admin_result_list"))

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response["Location"])
