from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [("exams", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="exam",
            name="pass_percentage",
            field=models.DecimalField(
                decimal_places=2,
                default=50,
                help_text="Minimum percentage required to pass.",
                max_digits=5,
            ),
        ),
    ]
