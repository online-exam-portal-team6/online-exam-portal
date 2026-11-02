"""Tests for displaying the timed exam page (OEP-F-015/016)."""
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from attempts.models import Attempt
from exams.models import Exam
from questions.models import Question


class ExamTakeViewTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user("exam_student", password="Pass@12345")
        self.other_student = User.objects.create_user("other_student", password="Pass@12345")
        self.admin = User.objects.create_user("exam_admin", password="Pass@12345", is_staff=True)
        now = timezone.now()
        self.exam = Exam.objects.create(
            title="Python Basics",
            description="Timed MCQ exam",
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
            text="Which keyword defines a function?",
            option_a="func",
            option_b="def",
            option_c="function",
            option_d="lambda",
            correct_option="B",
        )
        self.url = reverse("attempts:exam_take", args=[self.attempt.pk])

    def test_TC_ATT_02_student_sees_exam_questions_and_remaining_time(self):
        self.client.force_login(self.student)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "attempts/exam_take.html")
        self.assertEqual(response.context["exam"], self.exam)
        self.assertEqual(list(response.context["questions"]), [self.question])
        self.assertGreater(response.context["remaining_seconds"], 0)

    def test_TC_ATT_02_student_cannot_view_another_students_attempt(self):
        self.client.force_login(self.other_student)
        self.assertEqual(self.client.get(self.url).status_code, 404)

    def test_TC_ATT_02_admin_cannot_view_student_attempt(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(self.url).status_code, 403)

    def test_TC_ATT_03_expired_attempt_has_zero_remaining_time(self):
        self.attempt.deadline_at = timezone.now() - timedelta(seconds=1)
        self.attempt.save()
        self.client.force_login(self.student)
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["remaining_seconds"], 0)
        self.assertTrue(response.context["is_expired"])
