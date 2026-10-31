from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("attempts", "0002_answer")]

    operations = [
        migrations.AddField(
            model_name="attempt",
            name="score",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="attempt",
            name="total_questions",
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
