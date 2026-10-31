from django.core.exceptions import ValidationError
from django.db import models

from exams.models import Exam


class Question(models.Model):
    """An MCQ question belonging to an examination (OEP-F-011)."""

    OPTION_CHOICES = [
        ("A", "Option A"),
        ("B", "Option B"),
        ("C", "Option C"),
        ("D", "Option D"),
    ]

    exam = models.ForeignKey(
        Exam,
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
        choices=OPTION_CHOICES,
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.text[:80]

    def clean(self):
        super().clean()

        if self.text is not None and not self.text.strip():
            raise ValidationError({"text": "Question text is required."})

        for field in ("option_a", "option_b", "option_c", "option_d"):
            value = getattr(self, field)
            if value is not None and not value.strip():
                raise ValidationError({field: "This option cannot be empty."})

        if self.correct_option not in dict(self.OPTION_CHOICES):
            raise ValidationError(
                {"correct_option": "Select one valid correct option."}
            )
