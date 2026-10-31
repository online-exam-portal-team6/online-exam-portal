# Persist one selected option per question and attempt.
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("attempts", "0001_initial"),
        ("questions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="AttemptAnswer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "selected_option",
                    models.CharField(
                        choices=[
                            ("A", "Option A"),
                            ("B", "Option B"),
                            ("C", "Option C"),
                            ("D", "Option D"),
                        ],
                        max_length=1,
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                (
                    "attempt",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="answers",
                        to="attempts.attempt",
                    ),
                ),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="attempt_answers",
                        to="questions.question",
                    ),
                ),
            ],
            options={"ordering": ["question_id"]},
        ),
        migrations.AddConstraint(
            model_name="attemptanswer",
            constraint=models.UniqueConstraint(
                fields=("attempt", "question"),
                name="unique_answer_per_attempt_question",
            ),
        ),
    ]
