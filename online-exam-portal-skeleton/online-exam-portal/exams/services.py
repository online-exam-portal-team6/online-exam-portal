"""Exam services."""
from django.db.models import Exists, OuterRef
from django.utils import timezone

from attempts.models import Attempt
from .models import Exam


def get_available_exams_for(student):
    """Return in-window active exams the student has not submitted.

    An in-progress attempt remains available so the student can resume it.
    Submitted and automatically submitted attempts are excluded.
    """
    now = timezone.now()
    submitted_attempts = Attempt.objects.filter(
        student=student,
        exam_id=OuterRef("pk"),
        status__in=(Attempt.Status.SUBMITTED, Attempt.Status.AUTO_SUBMITTED),
    )
    exams = list(
        Exam.objects.filter(
            is_active=True,
            start_time__lte=now,
            end_time__gte=now,
        )
        .annotate(has_submitted_attempt=Exists(submitted_attempts))
        .filter(has_submitted_attempt=False)
        .order_by("end_time")
    )

    exam_ids = [exam.pk for exam in exams]
    in_progress = Attempt.objects.filter(
        student=student,
        exam_id__in=exam_ids,
        status=Attempt.Status.IN_PROGRESS,
    )
    attempts_by_exam = {attempt.exam_id: attempt for attempt in in_progress}
    for exam in exams:
        exam.my_attempt = attempts_by_exam.get(exam.pk)

    return exams
