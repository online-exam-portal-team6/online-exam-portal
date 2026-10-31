"""Tests for OEP-F-013: confirming deletion of an MCQ question."""

from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from exams.models import Exam
from questions.models import Question


class QuestionDeleteTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user(
            "admin", password="Pass@12345", is_staff=True
        )
        self.student = User.objects.create_user(
            "student", password="Pass@12345"
        )
        now = timezone.now()
        self.exam = Exam.objects.create(
            title="Python Basics",
            description="Python fundamentals",
            duration_minutes=60,
            start_time=now + timedelta(days=1),
            end_time=now + timedelta(days=1, hours=2),
            created_by=self.admin,
        )
        self.question = Question.objects.create(
            exam=self.exam,
            text="Delete me?",
            option_a="A1",
            option_b="B1",
            option_c="C1",
            option_d="D1",
            correct_option="A",
        )
        self.url = reverse(
            "questions:question_delete",
            kwargs={"exam_id": self.exam.pk, "pk": self.question.pk},
        )

    def test_admin_sees_confirmation_without_deleting(self):
        self.client.force_login(self.admin)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(
            response, "questions/question_confirm_delete.html"
        )
        self.assertContains(response, "Confirm delete")
        self.assertTrue(Question.objects.filter(pk=self.question.pk).exists())

    def test_TC_QUES_03_post_confirmation_deletes_question(self):
        self.client.force_login(self.admin)

        response = self.client.post(self.url)

        self.assertRedirects(
            response,
            reverse(
                "questions:question_list", kwargs={"exam_id": self.exam.pk}
            ),
            fetch_redirect_response=False,
        )
        self.assertFalse(Question.objects.filter(pk=self.question.pk).exists())

    def test_question_from_another_exam_cannot_be_deleted(self):
        other_exam = Exam.objects.create(
            title="Other exam",
            description="Another exam",
            duration_minutes=30,
            start_time=self.exam.start_time,
            end_time=self.exam.end_time,
            created_by=self.admin,
        )
        self.client.force_login(self.admin)
        url = reverse(
            "questions:question_delete",
            kwargs={"exam_id": other_exam.pk, "pk": self.question.pk},
        )

        self.assertEqual(self.client.post(url).status_code, 404)
        self.assertTrue(Question.objects.filter(pk=self.question.pk).exists())

    def test_student_cannot_delete_question(self):
        self.client.force_login(self.student)

        response = self.client.post(self.url)

        self.assertEqual(response.status_code, 403)
        self.assertTrue(Question.objects.filter(pk=self.question.pk).exists())
