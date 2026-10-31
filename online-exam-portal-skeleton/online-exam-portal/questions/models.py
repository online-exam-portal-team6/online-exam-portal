
"""MCQ questions belonging to an examination."""

from django.core.exceptions import ValidationError
from django.db import models


class Question(models.Model):
    class Option(models.TextChoices):
        A = "A", "Option A"
        B = "B", "Option B"
        C = "C", "Option C"
        D = "D", "Option D"

    exam = models.ForeignKey(
        "exams.Exam",
        on_delete=models.CASCADE,
        related_name="questions",
    )
    text = models.TextField()
    option_a = models.CharField(max_length=500)
    option_b = models.CharField(max_length=500)
    option_c = models.CharField(max_length=500)
    option_d = models.CharField(max_length=500)
    correct_option = models.CharField(
        max_length=1,
        choices=Option.choices,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    @property
    def options(self):
        return (
            ("A", self.option_a),
            ("B", self.option_b),
            ("C", self.option_c),
            ("D", self.option_d),
        )

    def __str__(self):
        return self.text[:80]

    def clean(self):
        super().clean()

        if self.text is not None and not self.text.strip():
            raise ValidationError(
                {"text": "Question text is required."}
            )

        for field in ("option_a", "option_b", "option_c", "option_d"):
            value = getattr(self, field)
            if value is not None and not value.strip():
                raise ValidationError(
                    {field: "This option cannot be empty."}
                )

        if self.correct_option not in self.Option.values:
            raise ValidationError(
                {"correct_option": "Select one valid correct option."}
            )
