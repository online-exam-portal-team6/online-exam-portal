"""Exam attempt services (contract B6)."""

from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.utils import timezone

from exams.models import Exam
from questions.models import Question

from .models import Attempt, AttemptAnswer


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
    """Persist or replace an answer while the student's attempt is active."""
    if option not in AttemptAnswer.Option.values:
        raise ValidationError("Select one of the available options A, B, C or D.")

    now = timezone.now()
    with transaction.atomic():
        locked_attempt = Attempt.objects.select_for_update().get(pk=attempt.pk)
        if locked_attempt.status != Attempt.Status.IN_PROGRESS:
            raise ValidationError("This examination has already been submitted.")
        if locked_attempt.deadline_at <= now:
            raise ValidationError("Your examination time has expired.")

        question = Question.objects.filter(
            pk=question_id,
            exam_id=locked_attempt.exam_id,
        ).first()
        if question is None:
            raise ValidationError("The selected question does not belong to this examination.")

        answer, _ = AttemptAnswer.objects.update_or_create(
            attempt=locked_attempt,
            question=question,
            defaults={"selected_option": option},
        )
        return answer


def submit_attempt(attempt, auto=False):
    """Submit once, then invoke the configured evaluation service.

    Evaluation is owned by the results module. Until that service is merged,
    the submission itself remains persisted and the evaluation call is safely
    deferred rather than turning a valid submission into an HTTP 500.
    """
    now = timezone.now()
    with transaction.atomic():
        locked_attempt = Attempt.objects.select_for_update().get(pk=attempt.pk)
        if locked_attempt.status != Attempt.Status.IN_PROGRESS:
            return locked_attempt

        expired = locked_attempt.deadline_at <= now
        locked_attempt.status = (
            Attempt.Status.AUTO_SUBMITTED if auto or expired else Attempt.Status.SUBMITTED
        )
        locked_attempt.submitted_at = now
        locked_attempt.save(update_fields=["status", "submitted_at"])

    from results.services import evaluate_attempt

    evaluate_attempt(locked_attempt)
    return locked_attempt
