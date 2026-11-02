import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("attempts", "0002_attemptanswer"),
        ("exams", "0001_initial"),
        ("questions", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Result",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("score", models.PositiveIntegerField()),
                ("total_marks", models.PositiveIntegerField()),
                ("percentage", models.DecimalField(decimal_places=2, max_digits=6)),
                ("passed", models.BooleanField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("attempt", models.OneToOneField(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name="result",
                    to="attempts.attempt",
                )),
                ("exam", models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name="examination_results",
                    to="exams.exam",
                )),
                ("student", models.ForeignKey(
                    on_delete=django.db.models.deletion.PROTECT,
                    related_name="examination_results",
                    to=settings.AUTH_USER_MODEL,
                )),
            ],
            options={"ordering": ["-created_at"]},
        ),
    ]
