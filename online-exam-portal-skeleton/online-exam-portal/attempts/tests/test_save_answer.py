"""Tests for answer persistence (OEP-F-017)."""
import json
from datetime import timedelta

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from attempts.models import Answer, Attempt
from attempts.services import save_answer
from exams.models import Exam
from questions.models import Question


class SaveAnswerTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user("answer_student", password="Pass@12345")
        self.other = User.objects.create_user("other_student", password="Pass@12345")
        self.admin = User.objects.create_user("answer_admin", password="Pass@12345", is_staff=True)
        now = timezone.now()
        self.exam = Exam.objects.create(title="Python Basics", description="MCQ exam",
            duration_minutes=30, start_time=now-timedelta(minutes=5),
            end_time=now+timedelta(hours=1), created_by=self.admin)
        self.attempt = Attempt.objects.create(student=self.student, exam=self.exam,
            started_at=now, deadline_at=now+timedelta(minutes=20))
        self.question = Question.objects.create(exam=self.exam, text="Which keyword defines a function?",
            option_a="func", option_b="def", option_c="function", option_d="lambda", correct_option="B")
        self.url = reverse("attempts:save_answer", args=[self.attempt.pk])

    def test_TC_ATT_04_student_can_save_answer(self):
        self.client.force_login(self.student)
        response = self.client.post(self.url, data=json.dumps({"question_id":self.question.pk,"option":"B"}),
                                    content_type="application/json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json()["ok"])
        self.assertEqual(Answer.objects.get().selected_option, "B")

    def test_TC_ATT_05_student_can_change_answer_without_duplicate(self):
        save_answer(self.attempt, self.question.pk, "A")
        save_answer(self.attempt, self.question.pk, "D")
        self.assertEqual(Answer.objects.count(), 1)
        self.assertEqual(Answer.objects.get().selected_option, "D")

    def test_invalid_option_is_rejected(self):
        with self.assertRaises(ValidationError): save_answer(self.attempt, self.question.pk, "E")

    def test_question_from_another_exam_is_rejected(self):
        other_exam = Exam.objects.create(title="Other", description="Other", duration_minutes=20,
            start_time=timezone.now()-timedelta(minutes=1), end_time=timezone.now()+timedelta(hours=1),
            created_by=self.admin)
        question = Question.objects.create(exam=other_exam, text="Other?", option_a="A", option_b="B",
            option_c="C", option_d="D", correct_option="A")
        with self.assertRaises(ValidationError): save_answer(self.attempt, question.pk, "A")

    def test_expired_attempt_rejects_answer(self):
        self.attempt.deadline_at=timezone.now()-timedelta(seconds=1); self.attempt.save()
        with self.assertRaises(ValidationError): save_answer(self.attempt, self.question.pk, "A")

    def test_submitted_attempt_rejects_answer(self):
        self.attempt.status=Attempt.Status.SUBMITTED; self.attempt.save()
        with self.assertRaises(ValidationError): save_answer(self.attempt, self.question.pk, "A")

    def test_other_student_cannot_save_answer(self):
        self.client.force_login(self.other)
        response=self.client.post(self.url,data=json.dumps({"question_id":self.question.pk,"option":"A"}),
                                  content_type="application/json")
        self.assertEqual(response.status_code,404)
