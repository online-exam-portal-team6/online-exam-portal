"""Result-page access and rendering tests (TC-RES-04 / TC-RES-05)."""

from types import SimpleNamespace
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class EmptyManager:
    """Small queryset stand-in for result pages with no attempts."""

    def filter(self, **kwargs):
        return []

    def all(self):
        return []


class FakeAttemptModel:
    """Attempt model metadata for exercising the result-view contract."""

    _meta = type(
        "Meta",
        (),
        {"get_fields": lambda self: [SimpleNamespace(name="student")]},
    )()
    objects = EmptyManager()


class ResultPageTests(TestCase):
    def setUp(self):
        self.student = User.objects.create_user(
            username="result-student",
            password="StrongPass123!",
        )
        self.other_student = User.objects.create_user(
            username="other-student",
            password="StrongPass123!",
        )
        self.admin = User.objects.create_user(
            username="result-admin",
            password="StrongPass123!",
            is_staff=True,
        )

    @patch("results.views._attempt_model", return_value=FakeAttemptModel)
    def test_TC_RES_04_student_sees_own_results_page(self, attempt_model):
        self.client.force_login(self.student)
        response = self.client.get(reverse("results:result_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "results/result_list.html")
        self.assertContains(response, "No results available yet")

    @patch("results.views._attempt_model", return_value=FakeAttemptModel)
    def test_TC_RES_05_admin_can_open_admin_result_register(self, attempt_model):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("results:admin_result_list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "results/admin_result_list.html")
        self.assertContains(response, "Examination results")

    def test_TC_RES_05_student_cannot_open_admin_result_register(self):
        self.client.force_login(self.student)
        response = self.client.get(reverse("results:admin_result_list"))
        self.assertEqual(response.status_code, 403)

    def test_TC_RES_04_admin_cannot_open_student_result_history(self):
        self.client.force_login(self.admin)
        response = self.client.get(reverse("results:result_list"))
        self.assertEqual(response.status_code, 403)

    @patch("results.views.get_object_or_404")
    @patch("results.views._attempt_model", return_value=FakeAttemptModel)
    def test_TC_RES_04_student_cannot_view_another_students_result(
        self,
        attempt_model,
        get_attempt,
    ):
        attempt = SimpleNamespace(
            pk=17,
            student_id=self.other_student.pk,
            student=self.other_student,
            status="submitted",
            exam=SimpleNamespace(title="Private examination"),
        )
        get_attempt.return_value = attempt
        self.client.force_login(self.student)

        response = self.client.get(
            reverse("results:result_detail", kwargs={"attempt_id": attempt.pk})
        )

        self.assertEqual(response.status_code, 403)

    @patch("results.views.get_object_or_404")
    @patch("results.views._attempt_model", return_value=FakeAttemptModel)
    def test_TC_RES_04_owner_can_view_submitted_result_detail(
        self,
        attempt_model,
        get_attempt,
    ):
        attempt = SimpleNamespace(
            pk=18,
            student_id=self.student.pk,
            student=self.student,
            status="submitted",
            score=8,
            total_marks=10,
            percentage=80,
            passed=True,
            exam=SimpleNamespace(title="Mathematics assessment"),
        )
        get_attempt.return_value = attempt
        self.client.force_login(self.student)

        response = self.client.get(
            reverse("results:result_detail", kwargs={"attempt_id": attempt.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "results/result_detail.html")
        self.assertContains(response, "Mathematics assessment")
        self.assertContains(response, "80.00%")
        self.assertContains(response, "PASS")

    def test_TC_RES_04_anonymous_user_is_redirected_to_login(self):
        response = self.client.get(reverse("results:result_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response["Location"])
