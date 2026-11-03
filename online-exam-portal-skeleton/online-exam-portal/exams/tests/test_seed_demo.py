from io import StringIO

from django.contrib.auth import get_user_model
from django.core.management import call_command, CommandError
from django.test import TestCase, override_settings

from exams.models import Exam
from questions.models import Question


class SeedDemoCommandTests(TestCase):
    @override_settings(DEBUG=True)
    def test_creates_demo_users_exams_and_questions(self):
        call_command("seed_demo", stdout=StringIO())

        User = get_user_model()
        self.assertEqual(User.objects.filter(username="demo_admin", is_superuser=True).count(), 1)
        self.assertEqual(User.objects.filter(username__startswith="demo_student").count(), 3)
        self.assertEqual(Exam.objects.filter(title__startswith="Demo ").count(), 2)
        self.assertEqual(Question.objects.filter(exam__title__startswith="Demo ").count(), 20)
        for exam in Exam.objects.filter(title__startswith="Demo "):
            self.assertEqual(exam.questions.count(), 10)

    @override_settings(DEBUG=True)
    def test_is_safe_to_run_twice(self):
        call_command("seed_demo", stdout=StringIO())
        call_command("seed_demo", stdout=StringIO())

        User = get_user_model()
        self.assertEqual(User.objects.filter(username__startswith="demo_student").count(), 3)
        self.assertEqual(Exam.objects.filter(title__startswith="Demo ").count(), 2)
        self.assertEqual(Question.objects.filter(exam__title__startswith="Demo ").count(), 20)

    @override_settings(DEBUG=False)
    def test_refuses_to_run_when_debug_is_disabled(self):
        with self.assertRaises(CommandError):
            call_command("seed_demo", stdout=StringIO())
