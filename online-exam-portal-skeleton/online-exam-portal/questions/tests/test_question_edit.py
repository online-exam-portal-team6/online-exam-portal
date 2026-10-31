"""Tests for OEP-F-012: editing an existing MCQ question."""

from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from exams.models import Exam
from questions.models import Question


class QuestionEditTests(TestCase):
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
            text="Old question?",
            option_a="A1",
            option_b="B1",
            option_c="C1",
            option_d="D1",
            correct_option="A",
        )
        self.url = reverse(
            "questions:question_edit",
            kwargs={"exam_id": self.exam.pk, "pk": self.question.pk},
        )
        self.payload = {
            "text": "Updated question?",
            "option_a": "A2",
            "option_b": "B2",
            "option_c": "C2",
            "option_d": "D2",
            "correct_option": "D",
        }

    def test_admin_can_load_question_values_for_editing(self):
        self.client.force_login(self.admin)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "questions/question_form.html")
        self.assertEqual(response.context["form"].instance, self.question)
        self.assertContains(response, "Edit MCQ Question")

    def test_TC_QUES_02_admin_can_update_question(self):
        self.client.force_login(self.admin)

        response = self.client.post(self.url, self.payload)

        self.assertRedirects(
            response,
            reverse(
                "questions:question_list", kwargs={"exam_id": self.exam.pk}
            ),
            fetch_redirect_response=False,
        )
        self.question.refresh_from_db()
        self.assertEqual(self.question.text, "Updated question?")
        self.assertEqual(self.question.option_a, "A2")
        self.assertEqual(self.question.option_d, "D2")
        self.assertEqual(self.question.correct_option, "D")
        self.assertEqual(Question.objects.count(), 1)

    def test_invalid_edit_keeps_original_question(self):
        self.client.force_login(self.admin)

        response = self.client.post(
            self.url, {**self.payload, "option_b": "   "}
        )

        self.assertEqual(response.status_code, 200)
        self.assertIn("option_b", response.context["form"].errors)
        self.question.refresh_from_db()
        self.assertEqual(self.question.text, "Old question?")

    def test_question_from_another_exam_is_not_editable(self):
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
            "questions:question_edit",
            kwargs={"exam_id": other_exam.pk, "pk": self.question.pk},
        )

        self.assertEqual(self.client.get(url).status_code, 404)

    def test_student_cannot_edit_question(self):
        self.client.force_login(self.student)

        response = self.client.post(self.url, self.payload)
        self.assertEqual(response.status_code, 403)
