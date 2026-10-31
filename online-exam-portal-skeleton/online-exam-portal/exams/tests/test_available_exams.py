"""Available examination filtering tests (OEP-F-010 / TC-EXAM-04)."""
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from attempts.models import Attempt
from exams.models import Exam
from exams.services import get_available_exams_for


class AvailableExamsTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            "available_admin", password="Pass@12345", is_staff=True
        )
        self.student = User.objects.create_user(
            "available_student", password="Pass@12345"
        )
        self.now = timezone.now()

    def make_exam(self, title, **overrides):
        values = {
            "title": title,
            "description": "Available exam service test",
            "duration_minutes": 30,
            "start_time": self.now - timedelta(minutes=5),
            "end_time": self.now + timedelta(hours=1),
            "created_by": self.admin,
            "is_active": True,
        }
        values.update(overrides)
        return Exam.objects.create(**values)

    def make_attempt(self, exam, status):
        return Attempt.objects.create(
            student=self.student,
            exam=exam,
            started_at=self.now,
            deadline_at=self.now + timedelta(minutes=30),
            status=status,
            submitted_at=(
                self.now if status != Attempt.Status.IN_PROGRESS else None
            ),
        )

    def test_TC_EXAM_04_only_active_exams_inside_window_are_listed(self):
        available = self.make_exam("Available")
        self.make_exam("Inactive", is_active=False)
        self.make_exam(
            "Not started",
            start_time=self.now + timedelta(hours=1),
            end_time=self.now + timedelta(hours=2),
        )
        self.make_exam(
            "Expired",
            start_time=self.now - timedelta(hours=2),
            end_time=self.now - timedelta(hours=1),
        )

        exams = get_available_exams_for(self.student)

        self.assertEqual([exam.pk for exam in exams], [available.pk])

    def test_TC_EXAM_04_submitted_exam_is_excluded(self):
        exam = self.make_exam("Already submitted")
        self.make_attempt(exam, Attempt.Status.SUBMITTED)

        self.assertNotIn(exam, get_available_exams_for(self.student))

    def test_TC_EXAM_04_auto_submitted_exam_is_excluded(self):
        exam = self.make_exam("Automatically submitted")
        self.make_attempt(exam, Attempt.Status.AUTO_SUBMITTED)

        self.assertNotIn(exam, get_available_exams_for(self.student))

    def test_TC_EXAM_04_in_progress_exam_remains_available_to_resume(self):
        exam = self.make_exam("In progress")
        attempt = self.make_attempt(exam, Attempt.Status.IN_PROGRESS)

        available = get_available_exams_for(self.student)

        self.assertIn(exam, available)
        self.assertEqual(available[0].my_attempt.pk, attempt.pk)

    def test_TC_EXAM_04_other_students_attempt_does_not_hide_exam(self):
        exam = self.make_exam("Other student's attempt")
        other_student = User.objects.create_user(
            "another_available_student", password="Pass@12345"
        )
        Attempt.objects.create(
            student=other_student,
            exam=exam,
            started_at=self.now,
            deadline_at=self.now + timedelta(minutes=30),
            status=Attempt.Status.SUBMITTED,
            submitted_at=self.now,
        )

        self.assertIn(exam, get_available_exams_for(self.student))
