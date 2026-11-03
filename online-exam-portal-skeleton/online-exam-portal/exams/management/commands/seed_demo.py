"""Seed a small, repeatable dataset for local development and demos."""
import os
from datetime import timedelta

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.utils import timezone

from exams.models import Exam
from questions.models import Question


class Command(BaseCommand):
    help = "Create a demo admin, three students, two exams, and ten MCQs per exam."

    def add_arguments(self, parser):
        parser.add_argument(
            "--password",
            default=os.environ.get("DEMO_USER_PASSWORD", "DemoOnly123!"),
            help="Password assigned only to newly-created demo accounts.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if not settings.DEBUG:
            raise CommandError(
                "seed_demo is development-only and requires DEBUG=True."
            )

        password = options["password"]
        if len(password) < 8:
            raise CommandError("Demo password must contain at least 8 characters.")

        User = get_user_model()
        admin_user, admin_created = User.objects.get_or_create(
            username="demo_admin",
            defaults={
                "email": "demo_admin@example.test",
                "is_staff": True,
                "is_superuser": True,
                "is_active": True,
            },
        )
        if admin_created:
            admin_user.set_password(password)
            admin_user.save(update_fields=["password"])
        else:
            # Do not overwrite an existing account's password or permissions.
            self.stdout.write("Keeping existing demo_admin account unchanged.")

        students = []
        for number in range(1, 4):
            student, created = User.objects.get_or_create(
                username=f"demo_student{number}",
                defaults={
                    "email": f"demo_student{number}@example.test",
                    "is_staff": False,
                    "is_superuser": False,
                    "is_active": True,
                },
            )
            if created:
                student.set_password(password)
                student.save(update_fields=["password"])
            students.append(student)

        now = timezone.now()
        exam_specs = (
            ("Demo Python Fundamentals", "Sample Python multiple-choice exam."),
            ("Demo Django Fundamentals", "Sample Django multiple-choice exam."),
        )
        for exam_index, (title, description) in enumerate(exam_specs):
            exam, exam_created = Exam.objects.get_or_create(
                title=title,
                defaults={
                    "description": description,
                    "duration_minutes": 30,
                    "start_time": now - timedelta(days=1),
                    "end_time": now + timedelta(days=30),
                    "is_active": True,
                    "pass_percentage": 50,
                    "created_by": admin_user,
                },
            )
            if exam_created or not exam.questions.exists():
                if not exam_created:
                    exam.questions.all().delete()
                for question_number in range(1, 11):
                    topic = "Python" if exam_index == 0 else "Django"
                    Question.objects.create(
                        exam=exam,
                        text=f"{topic} demo question {question_number}: choose option A.",
                        option_a="Correct sample answer",
                        option_b="Sample distractor B",
                        option_c="Sample distractor C",
                        option_d="Sample distractor D",
                        correct_option="A",
                        marks=1,
                    )

        self.stdout.write(self.style.SUCCESS(
            "Demo data is ready: 1 admin, 3 students, 2 exams, and 20 questions."
        ))
        self.stdout.write("New demo accounts use the supplied --password value.")
        self.stdout.write("Usernames: demo_admin, demo_student1, demo_student2, demo_student3")
