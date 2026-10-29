
from types import SimpleNamespace

from django.template.loader import render_to_string
from django.test import SimpleTestCase


class StudentListTemplateTests(SimpleTestCase):
    def make_student(self, username, full_name, roll_number, is_active, pk):
        user = SimpleNamespace(
            username=username,
            get_full_name=lambda: full_name,
            is_active=is_active,
            pk=pk,
        )
        return SimpleNamespace(user=user, roll_number=roll_number)

    def test_displays_active_and_inactive_students(self):
        students = [
            self.make_student(
                "rahul", "Rahul Sharma", "OEP001", True, 1
            ),
            self.make_student(
                "priya", "Priya Rao", "OEP002", False, 2
            ),
        ]

        html = render_to_string(
            "accounts/student_list.html",
            {"students": students},
        )

        self.assertIn("Rahul Sharma", html)
        self.assertIn("OEP001", html)
        self.assertIn("Active", html)
        self.assertIn("Deactivate", html)

        self.assertIn("Priya Rao", html)
        self.assertIn("OEP002", html)
        self.assertIn("Inactive", html)
        self.assertIn("Activate", html)

    def test_displays_empty_state_when_no_students_exist(self):
        html = render_to_string(
            "accounts/student_list.html",
            {"students": []},
        )

        self.assertIn("No students found", html)
