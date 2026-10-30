"""Persistence for student examination attempts."""
from django.conf import settings
from django.db import models


class Attempt(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = "IN_PROGRESS", "In progress"
        SUBMITTED = "SUBMITTED", "Submitted"
        AUTO_SUBMITTED = "AUTO_SUBMITTED", "Automatically submitted"

    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="exam_attempts",
    )
    exam = models.ForeignKey(
        "exams.Exam",
        on_delete=models.PROTECT,
        related_name="attempts",
    )
    started_at = models.DateTimeField()
    deadline_at = models.DateTimeField()
    submitted_at = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN_PROGRESS,
    )

    class Meta:
        ordering = ["-started_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["student", "exam"],
                name="unique_student_exam_attempt",
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.exam} ({self.get_status_display()})"
