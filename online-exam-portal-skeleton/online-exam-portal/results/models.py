"""Persisted, one-per-attempt examination results."""
from django.conf import settings
from django.db import models


class Result(models.Model):
    """Evaluated outcome for one submitted attempt."""

    attempt = models.OneToOneField(
        "attempts.Attempt",
        on_delete=models.PROTECT,
        related_name="result",
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="examination_results",
    )
    exam = models.ForeignKey(
        "exams.Exam",
        on_delete=models.PROTECT,
        related_name="examination_results",
    )
    score = models.PositiveIntegerField()
    total_marks = models.PositiveIntegerField()
    percentage = models.DecimalField(max_digits=6, decimal_places=2)
    passed = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"Result for attempt {self.attempt_id}: {self.score}/{self.total_marks}"
