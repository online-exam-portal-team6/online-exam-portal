"""Smoke tests for the starter skeleton: every contract URL name resolves and access control works.
Owner: Bhumika. Keep these passing as stubs are replaced by real views."""
from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

ARGS = {
    "exams:exam_edit": {"pk": 1}, "exams:exam_toggle": {"pk": 1},
    "questions:question_list": {"exam_id": 1}, "questions:question_create": {"exam_id": 1},
    "questions:question_edit": {"exam_id": 1, "pk": 1}, "questions:question_delete": {"exam_id": 1, "pk": 1},
    "accounts:student_toggle": {"pk": 1},
    "attempts:exam_start": {"exam_id": 1}, "attempts:exam_take": {"attempt_id": 1},
    "attempts:save_answer": {"attempt_id": 1}, "attempts:exam_submit": {"attempt_id": 1},
    "results:result_detail": {"attempt_id": 1},
}
NAMES = [
    "accounts:login", "accounts:register", "accounts:logout", "accounts:student_list", "accounts:student_toggle",
    "exams:student_dashboard", "exams:admin_dashboard", "exams:exam_list", "exams:exam_create", "exams:exam_edit",
    "exams:exam_toggle", "questions:question_list", "questions:question_create", "questions:question_edit",
    "questions:question_delete", "attempts:exam_start", "attempts:exam_take", "attempts:save_answer",
    "attempts:exam_submit", "results:result_list", "results:result_detail", "results:admin_result_list",
]


class SkeletonUrlTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user("stud", password="Pass@12345")
        self.admin = User.objects.create_user("adm", password="Pass@12345", is_staff=True)

    def test_all_contract_url_names_resolve(self):
        for name in NAMES:
            with self.subTest(name=name):
                self.assertTrue(reverse(name, kwargs=ARGS.get(name, {})))

    def test_root_redirects_by_role(self):
        self.assertRedirects(self.client.get("/"), reverse("accounts:login"), fetch_redirect_response=False)
        self.client.force_login(self.student)
        self.assertRedirects(self.client.get("/"), reverse("exams:student_dashboard"), fetch_redirect_response=False)
        self.client.force_login(self.admin)
        self.assertRedirects(self.client.get("/"), reverse("exams:admin_dashboard"), fetch_redirect_response=False)

    def test_anonymous_is_sent_to_login(self):
        response = self.client.get(reverse("exams:student_dashboard"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response["Location"])

    def test_student_cannot_open_admin_pages(self):
        self.client.force_login(self.student)
        self.assertEqual(self.client.get(reverse("exams:admin_dashboard")).status_code, 403)

    def test_admin_cannot_open_student_pages(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse("exams:student_dashboard")).status_code, 403)

    def test_correct_role_reaches_stub(self):
        self.client.force_login(self.admin)
        self.assertEqual(self.client.get(reverse("exams:admin_dashboard")).status_code, 200)
        self.client.force_login(self.student)
        self.assertEqual(self.client.get(reverse("exams:student_dashboard")).status_code, 200)
