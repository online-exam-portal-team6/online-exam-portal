# Generated for the initial attempt model.
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("exams", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Attempt",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("started_at", models.DateTimeField()),
                ("deadline_at", models.DateTimeField()),
                ("submitted_at", models.DateTimeField(blank=True, null=True)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("IN_PROGRESS", "In progress"),
                            ("SUBMITTED", "Submitted"),
                            ("AUTO_SUBMITTED", "Automatically submitted"),
                        ],
                        default="IN_PROGRESS",
                        max_length=20,
                    ),
                ),
                (
                    "exam",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="attempts",
                        to="exams.exam",
                    ),
                ),
                (
                    "student",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="exam_attempts",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ["-started_at"]},
        ),
        migrations.AddConstraint(
            model_name="attempt",
            constraint=models.UniqueConstraint(
                fields=("student", "exam"),
                name="unique_student_exam_attempt",
            ),
        ),
    ]
