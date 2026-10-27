"""Models for the exams app. Owner: Thejas (all models.py files). See team contract B5."""
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models

MAX_DURATION_MINUTES = 600


class Exam(models.Model):
    """An examination configured by an administrator (OEP-F-007)."""

    title = models.CharField(max_length=200)
    description = models.TextField()
    duration_minutes = models.PositiveIntegerField(help_text="Time allowed for one attempt, in minutes.")
    start_time = models.DateTimeField(help_text="Students can start the exam from this time.")
    end_time = models.DateTimeField(help_text="Students cannot start the exam after this time.")
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="created_exams",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-start_time"]

    def __str__(self):
        return self.title

    def clean(self):
        super().clean()
        if self.title is not None and not self.title.strip():
            raise ValidationError({"title": "Title is required."})
        if self.duration_minutes is not None:
            if not 1 <= self.duration_minutes <= MAX_DURATION_MINUTES:
                raise ValidationError(
                    {"duration_minutes": f"Duration must be between 1 and {MAX_DURATION_MINUTES} minutes."}
                )
        if self.start_time and self.end_time:
            if self.end_time <= self.start_time:
                raise ValidationError({"end_time": "End time must be after the start time."})
            window_minutes = (self.end_time - self.start_time).total_seconds() / 60
            if self.duration_minutes and window_minutes < self.duration_minutes:
                raise ValidationError(
                    {"end_time": "The availability window must be at least as long as the exam duration."}
                )
