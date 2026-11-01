"""Exam attempt services (contract B6)."""
from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import F
from django.utils import timezone

from exams.models import Exam
from questions.models import Question

from .models import Answer, Attempt


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
            with transaction.atomic():
                return Attempt.objects.create(
                    student=student, exam=locked_exam, started_at=now,
                    deadline_at=now + timedelta(minutes=locked_exam.duration_minutes),
                    status=Attempt.Status.IN_PROGRESS,
                )
        except IntegrityError:
            existing = Attempt.objects.filter(student=student, exam=locked_exam).first()
            if existing and existing.status == Attempt.Status.IN_PROGRESS:
                return existing
            raise ValidationError("An attempt for this examination already exists.")


def save_answer(attempt, question_id, option):
    """Create or replace the selected option while the attempt is still open."""
    if option not in Question.Option.values:
        raise ValidationError("Select one of the available options (A, B, C or D).")
    with transaction.atomic():
        locked_attempt = Attempt.objects.select_for_update().select_related("exam").get(pk=attempt.pk)
        now = timezone.now()
        if locked_attempt.status != Attempt.Status.IN_PROGRESS:
            raise ValidationError("This examination attempt is no longer accepting answers.")
        if now >= locked_attempt.deadline_at:
            raise ValidationError("The examination deadline has passed.")
        question = Question.objects.filter(pk=question_id, exam_id=locked_attempt.exam_id).first()
        if question is None:
            raise ValidationError("That question does not belong to this examination.")
        answer, _ = Answer.objects.update_or_create(
            attempt=locked_attempt,
            question=question,
            defaults={"selected_option": option},
        )
        remaining_seconds = max(0, int((locked_attempt.deadline_at - now).total_seconds()))
        return answer, remaining_seconds


def submit_attempt(attempt, auto=False):
    """Grade and finalize an attempt manually or when its deadline expires."""
    with transaction.atomic():
        locked_attempt = (
            Attempt.objects.select_for_update()
            .select_related("exam")
            .get(pk=attempt.pk)
        )
        if locked_attempt.status != Attempt.Status.IN_PROGRESS:
            return locked_attempt
        now = timezone.now()
        if auto and now < locked_attempt.deadline_at:
            raise ValidationError("The examination deadline has not been reached.")
        if not auto and now >= locked_attempt.deadline_at:
            raise ValidationError("The examination time has expired.")
        total_questions = Question.objects.filter(exam_id=locked_attempt.exam_id).count()
        correct_count = Answer.objects.filter(
            attempt=locked_attempt,
            question__exam_id=locked_attempt.exam_id,
            selected_option=F("question__correct_option"),
        ).count()
        locked_attempt.score = correct_count
        locked_attempt.total_questions = total_questions
        locked_attempt.status = (
            Attempt.Status.AUTO_SUBMITTED if auto else Attempt.Status.SUBMITTED
        )
        locked_attempt.submitted_at = now
        locked_attempt.save(update_fields=[
            "score", "total_questions", "status", "submitted_at"
        ])
        return locked_attempt
