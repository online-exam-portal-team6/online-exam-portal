"""Exam attempt services (contract B6)."""
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.utils import timezone

from exams.models import Exam

from .models import Attempt


def start_attempt(student, exam):
    """Create the student's single attempt after validating the exam window."""
    now = timezone.now()
    if not exam.is_active or now < exam.start_time or now > exam.end_time:
        raise ValidationError("This examination is not currently available.")

    with transaction.atomic():
        locked_exam = Exam.objects.select_for_update().get(pk=exam.pk)
        existing = Attempt.objects.filter(student=student, exam=locked_exam).first()
        if existing:
            if existing.status == Attempt.Status.IN_PROGRESS:
                if existing.deadline_at <= now:
                    raise ValidationError("Your examination time has expired.")
                return existing
            raise ValidationError("You have already completed this examination.")

        try:
            # Inner atomic block creates a savepoint, so a uniqueness race does
            # not leave the outer transaction marked as broken.
            with transaction.atomic():
                return Attempt.objects.create(
                    student=student,
                    exam=locked_exam,
                    started_at=now,
                    deadline_at=now + timedelta(minutes=locked_exam.duration_minutes),
                    status=Attempt.Status.IN_PROGRESS,
                )
        except IntegrityError:
            existing = Attempt.objects.filter(student=student, exam=locked_exam).first()
            if existing and existing.status == Attempt.Status.IN_PROGRESS:
                return existing
            raise ValidationError("An attempt for this examination already exists.")


def save_answer(attempt, question_id, option):
    raise NotImplementedError("TODO (Bhumika, OEP-F-017)")


def submit_attempt(attempt, auto=False):
    """Idempotent. Sets SUBMITTED / AUTO_SUBMITTED, then calls results.services.evaluate_attempt(attempt)."""
    raise NotImplementedError("TODO (Bhumika, OEP-F-018/019)")
