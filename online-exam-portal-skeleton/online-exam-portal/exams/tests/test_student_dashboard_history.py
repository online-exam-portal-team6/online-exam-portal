"""Student dashboard history regression tests (OEP-51 / OEP-F-023)."""
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from attempts.models import Attempt
from exams.models import Exam
from results.models import Result


class StudentDashboardHistoryTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            username="history-admin",
            password="StrongPass123!",
            is_staff=True,
        )
        self.student = User.objects.create_user(
            username="history-student",
            password="StrongPass123!",
        )
        self.other_student = User.objects.create_user(
            username="other-history-student",
            password="StrongPass123!",
        )
        self.now = timezone.now()

    def make_exam(self, title):
        return Exam.objects.create(
            title=title,
            description="Dashboard history regression test",
            duration_minutes=30,
            start_time=self.now - timedelta(minutes=5),
            end_time=self.now + timedelta(hours=1),
            created_by=self.admin,
        )

    def make_attempt(self, student, exam, status):
        return Attempt.objects.create(
            student=student,
            exam=exam,
            started_at=self.now - timedelta(minutes=30),
            deadline_at=self.now,
            submitted_at=(
                self.now if status != Attempt.Status.IN_PROGRESS else None
            ),
            status=status,
        )

    def test_dashboard_lists_only_own_submitted_attempts(self):
        evaluated_exam = self.make_exam("Evaluated examination")
        pending_exam = self.make_exam("Awaiting evaluation examination")
        in_progress_exam = self.make_exam("In progress examination")
        other_exam = self.make_exam("Another student's examination")

        evaluated_attempt = self.make_attempt(
            self.student, evaluated_exam, Attempt.Status.SUBMITTED
        )
        self.make_attempt(
            self.student, pending_exam, Attempt.Status.AUTO_SUBMITTED
        )
        self.make_attempt(
            self.student, in_progress_exam, Attempt.Status.IN_PROGRESS
        )
        self.make_attempt(
            self.other_student, other_exam, Attempt.Status.SUBMITTED
        )
        Result.objects.create(
            attempt=evaluated_attempt,
            student=self.student,
            exam=evaluated_exam,
            score=8,
            total_marks=10,
            percentage="80.00",
            passed=True,
        )

        self.client.force_login(self.student)
        response = self.client.get(reverse("exams:student_dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["completed_attempt_count"], 2)
        attempts = list(response.context["completed_attempts"])
        self.assertEqual(len(attempts), 2)
        self.assertEqual(
            {attempt.exam.title for attempt in attempts},
            {"Evaluated examination", "Awaiting evaluation examination"},
        )
        self.assertContains(response, "Evaluated examination")
        self.assertContains(response, "Awaiting evaluation examination")
        self.assertContains(response, "80.00%")
        self.assertContains(response, "Awaiting evaluation")
        self.assertNotContains(response, "In progress examination")
        self.assertNotContains(response, "Another student's examination")

    def test_dashboard_limits_history_cards_but_keeps_total_count(self):
        for index in range(7):
            exam = self.make_exam(f"History examination {index}")
            self.make_attempt(self.student, exam, Attempt.Status.SUBMITTED)

        self.client.force_login(self.student)
        response = self.client.get(reverse("exams:student_dashboard"))

        self.assertEqual(response.context["completed_attempt_count"], 7)
        self.assertEqual(len(response.context["completed_attempts"]), 5)
