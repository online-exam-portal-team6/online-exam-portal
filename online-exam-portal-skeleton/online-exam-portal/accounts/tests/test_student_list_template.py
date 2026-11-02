"""Tests for the current student directory template."""

from datetime import datetime, timezone
from types import SimpleNamespace

from django.template.loader import render_to_string
from django.test import RequestFactory, SimpleTestCase


class StudentListTemplateTests(SimpleTestCase):
    def make_student(self, username, full_name, email, is_active, pk):
        return SimpleNamespace(
            username=username,
            get_full_name=lambda: full_name,
            email=email,
            date_joined=datetime(2026, 10, 1, tzinfo=timezone.utc),
            last_login=None,
            is_active=is_active,
            pk=pk,
        )

    def render_students(self, students, search_query=""):
        request = RequestFactory().get("/manage/students/")
        request.user = SimpleNamespace(username="admin", first_name="Admin")
        request._messages = []
        return render_to_string(
            "accounts/student_list.html",
            {
                "students": students,
                "search_query": search_query,
                "total_students": len(students),
                "active_students": sum(
                    student.is_active for student in students
                ),
                "disabled_students": sum(
                    not student.is_active for student in students
                ),
            },
            request=request,
        )

    def test_displays_active_and_disabled_students(self):
        students = [
            self.make_student(
                "rahul", "Rahul Sharma", "rahul@example.com", True, 1
            ),
            self.make_student(
                "priya", "Priya Rao", "priya@example.com", False, 2
            ),
        ]

        html = self.render_students(students)

        self.assertIn("Rahul Sharma", html)
        self.assertIn("rahul@example.com", html)
        self.assertIn("Active", html)
        self.assertIn("Disable", html)
        self.assertIn("Priya Rao", html)
        self.assertIn("priya@example.com", html)
        self.assertIn("Disabled", html)
        self.assertIn("Enable", html)

    def test_displays_empty_state_when_no_students_exist(self):
        html = self.render_students([])

        self.assertIn("No students found", html)

    def test_displays_search_query(self):
        student = self.make_student(
            "rahul", "Rahul Sharma", "rahul@example.com", True, 1
        )

        html = self.render_students([student], search_query="rahul")

        self.assertIn('value="rahul"', html)
