"""End-to-end tests of the full examination flow (OEP-84).

Every step goes through HTTP with the Django test client, using the real forms
and endpoints: an administrator logs in, creates an exam and its questions; a
student registers, starts the exam, saves answers, submits, and views the
result; the administrator then sees it in the result register.

The timeout path moves the attempt's server deadline into the past to simulate
the exam time running out, then checks that late answers are rejected and the
attempt is automatically submitted and evaluated exactly once.

All accounts are synthetic and passwords are generated at runtime.
"""

import json
import secrets
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from attempts.models import Attempt, AttemptAnswer
from exams.models import Exam
from results.models import Result

FORM_DATETIME = "%Y-%m-%dT%H:%M"
EXAM_TITLE = "E2E Demo Examination"

QUESTIONS = [
    ("Which planet is known as the Red Planet?", ("Venus", "Mars", "Jupiter", "Mercury"), "B"),
    ("What is 7 multiplied by 6?", ("36", "40", "42", "48"), "C"),
    ("Which gas do plants absorb for photosynthesis?", ("Oxygen", "Nitrogen", "Helium", "Carbon dioxide"), "D"),
]


def make_password():
    return "E2e-" + secrets.token_urlsafe(16)


class FullExamFlowTests(TestCase):
    def setUp(self):
        self.admin_password = make_password()
        self.admin = User.objects.create_user(
            "e2e_admin", password=self.admin_password, is_staff=True
        )

    # Helpers -------------------------------------------------------------

    def login(self, username, password, expected_dashboard):
        response = self.client.post(
            reverse("accounts:login"),
            {"username": username, "password": password},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain[-1][0], reverse(expected_dashboard))
        return response

    def logout(self):
        response = self.client.post(reverse("accounts:logout"))
        self.assertRedirects(response, reverse("accounts:login"), fetch_redirect_response=False)
        self.assertNotIn("_auth_user_id", self.client.session)

    def admin_creates_exam_with_questions(self):
        self.login("e2e_admin", self.admin_password, "exams:admin_dashboard")

        start = timezone.localtime() - timedelta(minutes=5)
        response = self.client.post(
            reverse("exams:exam_create"),
            {
                "title": EXAM_TITLE,
                "description": "Synthetic exam for the end-to-end flow test.",
                "duration_minutes": 30,
                "start_time": start.strftime(FORM_DATETIME),
                "end_time": (start + timedelta(hours=2)).strftime(FORM_DATETIME),
            },
        )
        self.assertRedirects(response, reverse("exams:exam_list"), fetch_redirect_response=False)
        exam = Exam.objects.get(title=EXAM_TITLE)
        self.assertTrue(exam.is_active)

        for text, options, correct in QUESTIONS:
            response = self.client.post(
                reverse("questions:question_create", args=[exam.pk]),
                {
                    "text": text,
                    "option_a": options[0],
                    "option_b": options[1],
                    "option_c": options[2],
                    "option_d": options[3],
                    "correct_option": correct,
                },
            )
            self.assertRedirects(
                response,
                reverse("questions:question_list", args=[exam.pk]),
                fetch_redirect_response=False,
            )
        self.assertEqual(exam.questions.count(), len(QUESTIONS))

        self.logout()
        return exam, list(exam.questions.order_by("id"))

    def student_registers(self, username):
        password = make_password()
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": username,
                "first_name": "Demo",
                "last_name": "Candidate",
                "email": f"{username}@example.test",
                "password1": password,
                "password2": password,
            },
            follow=True,
        )
        self.assertEqual(response.redirect_chain[-1][0], reverse("exams:student_dashboard"))
        return User.objects.get(username=username)

    def start_exam(self, exam):
        dashboard = self.client.get(reverse("exams:student_dashboard"))
        self.assertContains(dashboard, EXAM_TITLE)
        self.assertContains(dashboard, reverse("attempts:exam_start", args=[exam.pk]))

        rules = self.client.get(reverse("attempts:exam_start", args=[exam.pk]))
        self.assertEqual(rules.status_code, 200)
        self.assertTrue(rules.context["is_available"])

        response = self.client.post(reverse("attempts:exam_start", args=[exam.pk]))
        attempt = Attempt.objects.get(exam=exam)
        self.assertRedirects(
            response,
            reverse("attempts:exam_take", args=[attempt.pk]),
            fetch_redirect_response=False,
        )
        self.assertEqual(attempt.status, Attempt.Status.IN_PROGRESS)
        return attempt

    def save_answer(self, attempt, question, option):
        return self.client.post(
            reverse("attempts:save_answer", args=[attempt.pk]),
            data=json.dumps({"question_id": question.pk, "option": option}),
            content_type="application/json",
        )

    def submit(self, attempt):
        response = self.client.post(reverse("attempts:exam_submit", args=[attempt.pk]))
        self.assertRedirects(
            response,
            reverse("results:result_detail", args=[attempt.pk]),
            fetch_redirect_response=False,
        )
        attempt.refresh_from_db()
        return attempt

    # Scenarios -----------------------------------------------------------

    def test_full_exam_flow_from_creation_to_result(self):
        exam, questions = self.admin_creates_exam_with_questions()
        student = self.student_registers("e2e_student")
        attempt = self.start_exam(exam)

        take = self.client.get(reverse("attempts:exam_take", args=[attempt.pk]))
        self.assertEqual(take.status_code, 200)
        self.assertGreater(take.context["remaining_seconds"], 0)
        for text, options, _ in QUESTIONS:
            self.assertContains(take, text)
            for option_text in options:
                self.assertContains(take, option_text)

        # Answer Q1 wrongly, then change it to the correct option.
        self.assertEqual(self.save_answer(attempt, questions[0], "A").status_code, 200)
        changed = self.save_answer(attempt, questions[0], "B")
        self.assertEqual(changed.status_code, 200)
        self.assertEqual(changed.json()["option"], "B")
        self.assertEqual(self.save_answer(attempt, questions[1], "C").status_code, 200)
        self.assertEqual(self.save_answer(attempt, questions[2], "A").status_code, 200)
        self.assertEqual(AttemptAnswer.objects.filter(attempt=attempt).count(), 3)

        attempt = self.submit(attempt)
        self.assertEqual(attempt.status, Attempt.Status.SUBMITTED)
        self.assertIsNotNone(attempt.submitted_at)

        result = Result.objects.get(attempt=attempt)
        self.assertEqual((result.student, result.exam), (student, exam))
        self.assertEqual((result.score, result.total_marks), (2, 3))
        self.assertEqual(str(result.percentage), "66.67")
        self.assertTrue(result.passed)

        detail = self.client.get(reverse("results:result_detail", args=[attempt.pk]))
        self.assertEqual(detail.status_code, 200)
        self.assertContains(detail, EXAM_TITLE)
        self.assertContains(detail, "66.67%")
        self.assertContains(detail, "Passed")

        history = self.client.get(reverse("results:result_list"))
        self.assertContains(history, EXAM_TITLE)

        # The exam is no longer offered and cannot be retaken.
        dashboard = self.client.get(reverse("exams:student_dashboard"))
        self.assertNotIn(exam, list(dashboard.context["available_exams"]))
        retake = self.client.post(reverse("attempts:exam_start", args=[exam.pk]))
        self.assertEqual(retake.status_code, 200)
        self.assertContains(retake, "already completed")
        self.assertEqual(Attempt.objects.filter(exam=exam, student=student).count(), 1)

        self.logout()
        self.login("e2e_admin", self.admin_password, "exams:admin_dashboard")
        register = self.client.get(reverse("results:admin_result_list"))
        self.assertEqual(register.status_code, 200)
        self.assertContains(register, "Demo Candidate")
        self.assertContains(register, EXAM_TITLE)
        admin_detail = self.client.get(reverse("results:result_detail", args=[attempt.pk]))
        self.assertContains(admin_detail, "66.67%")

    def test_timeout_path_auto_submits_expired_attempt(self):
        exam, questions = self.admin_creates_exam_with_questions()
        student = self.student_registers("e2e_timeout_student")
        attempt = self.start_exam(exam)

        # One answer is saved while time remains.
        self.assertEqual(self.save_answer(attempt, questions[0], "B").status_code, 200)

        # Simulate the exam time running out on the server.
        Attempt.objects.filter(pk=attempt.pk).update(
            deadline_at=timezone.now() - timedelta(seconds=1)
        )

        take = self.client.get(reverse("attempts:exam_take", args=[attempt.pk]))
        self.assertEqual(take.status_code, 200)
        self.assertEqual(take.context["remaining_seconds"], 0)
        self.assertTrue(take.context["is_expired"])
        self.assertContains(take, "Your exam time has expired")

        # Answers sent after the deadline are rejected and not stored.
        late = self.save_answer(attempt, questions[1], "C")
        self.assertEqual(late.status_code, 403)
        self.assertTrue(late.json()["expired"])
        self.assertFalse(
            AttemptAnswer.objects.filter(attempt=attempt, question=questions[1]).exists()
        )

        # Submitting after the deadline (as the page timer does) auto-submits.
        attempt = self.submit(attempt)
        self.assertEqual(attempt.status, Attempt.Status.AUTO_SUBMITTED)
        first_submitted_at = attempt.submitted_at
        self.assertIsNotNone(first_submitted_at)

        result = Result.objects.get(attempt=attempt)
        self.assertEqual(result.student, student)
        self.assertEqual((result.score, result.total_marks), (1, 3))
        self.assertEqual(str(result.percentage), "33.33")
        self.assertFalse(result.passed)

        # A repeated submission does not change the attempt or duplicate the result.
        attempt = self.submit(attempt)
        self.assertEqual(attempt.status, Attempt.Status.AUTO_SUBMITTED)
        self.assertEqual(attempt.submitted_at, first_submitted_at)
        self.assertEqual(Result.objects.filter(attempt=attempt).count(), 1)

        # The attempt page is closed and the result is visible to the student.
        closed = self.client.get(reverse("attempts:exam_take", args=[attempt.pk]))
        self.assertRedirects(
            closed, reverse("exams:student_dashboard"), fetch_redirect_response=False
        )
        detail = self.client.get(reverse("results:result_detail", args=[attempt.pk]))
        self.assertEqual(detail.status_code, 200)
        self.assertContains(detail, "33.33%")
        self.assertContains(detail, "Not passed")
