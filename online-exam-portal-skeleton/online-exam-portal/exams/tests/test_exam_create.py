"""Tests for OEP-F-007 Create examination (TC-EXAM-01). Owner: Thejas."""
from datetime import timedelta

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from exams.models import Exam


def valid_payload(**overrides):
    start = timezone.localtime(timezone.now() + timedelta(days=1)).replace(second=0, microsecond=0)
    data = {
        "title": "Python Basics",
        "description": "Multiple-choice test on Python fundamentals.",
        "duration_minutes": "60",
        "start_time": start.strftime("%Y-%m-%dT%H:%M"),
        "end_time": (start + timedelta(hours=3)).strftime("%Y-%m-%dT%H:%M"),
    }
    data.update(overrides)
    return data


class ExamCreateTests(TestCase):
    def setUp(self):
        self.admin = User.objects.create_user("adm", password="Pass@12345", is_staff=True)
        self.student = User.objects.create_user("stud", password="Pass@12345")
        self.url = reverse("exams:exam_create")
        self.client.force_login(self.admin)

    def assert_rejected(self, payload, field):
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, 200)
        self.assertIn(field, response.context["form"].errors)
        self.assertEqual(Exam.objects.count(), 0)

    def test_TC_EXAM_01_valid_details_create_exam(self):
        response = self.client.post(self.url, valid_payload())
        self.assertRedirects(response, reverse("exams:exam_list"), fetch_redirect_response=False)
        exam = Exam.objects.get()
        self.assertEqual(exam.title, "Python Basics")
        self.assertEqual(exam.duration_minutes, 60)
        self.assertEqual(exam.created_by, self.admin)
        self.assertTrue(exam.is_active)

    def test_TC_EXAM_01_form_page_renders_for_admin(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "exams/exam_form.html")
        self.assertIsNone(response.context["exam"])

    def test_TC_EXAM_01_missing_title_rejected(self):
        self.assert_rejected(valid_payload(title=""), "title")

    def test_TC_EXAM_01_blank_title_rejected(self):
        self.assert_rejected(valid_payload(title="   "), "title")

    def test_TC_EXAM_01_missing_description_rejected(self):
        self.assert_rejected(valid_payload(description=""), "description")

    def test_TC_EXAM_01_missing_duration_rejected(self):
        self.assert_rejected(valid_payload(duration_minutes=""), "duration_minutes")

    def test_TC_EXAM_01_zero_duration_rejected(self):
        self.assert_rejected(valid_payload(duration_minutes="0"), "duration_minutes")

    def test_TC_EXAM_01_negative_duration_rejected(self):
        self.assert_rejected(valid_payload(duration_minutes="-5"), "duration_minutes")

    def test_TC_EXAM_01_excessive_duration_rejected(self):
        payload = valid_payload(duration_minutes="601")
        payload["end_time"] = (
            timezone.localtime(timezone.now() + timedelta(days=3)).strftime("%Y-%m-%dT%H:%M")
        )
        self.assert_rejected(payload, "duration_minutes")

    def test_TC_EXAM_01_missing_availability_window_rejected(self):
        self.assert_rejected(valid_payload(start_time=""), "start_time")
        self.assert_rejected(valid_payload(end_time=""), "end_time")

    def test_TC_EXAM_01_end_before_start_rejected(self):
        payload = valid_payload()
        payload["start_time"], payload["end_time"] = payload["end_time"], payload["start_time"]
        self.assert_rejected(payload, "end_time")

    def test_TC_EXAM_01_window_shorter_than_duration_rejected(self):
        payload = valid_payload(duration_minutes="120")
        start = timezone.localtime(timezone.now() + timedelta(days=1)).replace(second=0, microsecond=0)
        payload["start_time"] = start.strftime("%Y-%m-%dT%H:%M")
        payload["end_time"] = (start + timedelta(minutes=30)).strftime("%Y-%m-%dT%H:%M")
        self.assert_rejected(payload, "end_time")

    def test_student_cannot_create_exam(self):
        self.client.force_login(self.student)
        response = self.client.post(self.url, valid_payload())
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Exam.objects.count(), 0)

    def test_anonymous_is_sent_to_login(self):
        self.client.logout()
        response = self.client.post(self.url, valid_payload())
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("accounts:login"), response["Location"])
        self.assertEqual(Exam.objects.count(), 0)
