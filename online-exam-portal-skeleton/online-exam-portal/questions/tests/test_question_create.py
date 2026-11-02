"""Tests for OEP-F-011: adding an MCQ question to an examination."""

from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from exams.models import Exam
from questions.models import Question


class QuestionCreateTests(TestCase):
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
        self.url = reverse(
            "questions:question_create", kwargs={"exam_id": self.exam.pk}
        )
        self.payload = {
            "text": "Which keyword defines a function in Python?",
            "option_a": "func",
            "option_b": "def",
            "option_c": "function",
            "option_d": "lambda",
            "correct_option": "B",
        }

    def test_TC_QUES_01_admin_can_create_four_option_mcq(self):
        self.client.force_login(self.admin)

        response = self.client.post(self.url, self.payload)

        self.assertRedirects(
            response,
            reverse(
                "questions:question_list", kwargs={"exam_id": self.exam.pk}
            ),
            fetch_redirect_response=False,
        )
        question = Question.objects.get()
        self.assertEqual(question.exam, self.exam)
        self.assertEqual(question.text, self.payload["text"])
        self.assertEqual(
            [
                question.option_a,
                question.option_b,
                question.option_c,
                question.option_d,
            ],
            ["func", "def", "function", "lambda"],
        )
        self.assertEqual(question.correct_option, "B")

    def test_form_renders_for_admin(self):
        self.client.force_login(self.admin)

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "questions/question_form.html")

    def test_invalid_question_does_not_create_record(self):
        self.client.force_login(self.admin)

        for field, value in (("text", "   "), ("option_c", "   ")):
            with self.subTest(field=field):
                response = self.client.post(
                    self.url, {**self.payload, field: value}
                )
                self.assertEqual(response.status_code, 200)
                self.assertIn(field, response.context["form"].errors)
                self.assertEqual(Question.objects.count(), 0)

    def test_student_cannot_create_question(self):
        self.client.force_login(self.student)

        response = self.client.post(self.url, self.payload)

        self.assertEqual(response.status_code, 403)
        self.assertEqual(Question.objects.count(), 0)

    def test_anonymous_user_is_sent_to_login(self):
        response = self.client.post(self.url, self.payload)

        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response["Location"])
        self.assertEqual(Question.objects.count(), 0)
