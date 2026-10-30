"""Exam services."""

from django.utils import timezone

from .models import Exam


def get_available_exams_for(student):
    """
    Return active exams that are currently within their availability window.

    Attempt-based exclusion will be added when the Attempt model is implemented.
    """
    now = timezone.now()

    exams = Exam.objects.filter(
        is_active=True,
        start_time__lte=now,
        end_time__gte=now,
    ).order_by("end_time")

    for exam in exams:
        exam.my_attempt = None

    return exams
