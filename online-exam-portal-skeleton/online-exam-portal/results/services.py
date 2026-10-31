"""Answer comparison, scoring, and idempotent result persistence."""
from decimal import Decimal, ROUND_HALF_UP

from django.core.exceptions import ValidationError
from django.db import transaction

from attempts.models import Attempt, AttemptAnswer

from .models import Result


def compare_submitted_answers(attempt):
    """Return the set of correctly answered question IDs and exam questions."""
    questions = list(attempt.exam.questions.all())
    answers = {
        answer.question_id: answer.selected_option
        for answer in AttemptAnswer.objects.filter(
            attempt=attempt,
            question__exam_id=attempt.exam_id,
        )
    }
    correct_ids = {
        question.pk
        for question in questions
        if answers.get(question.pk) == question.correct_option
    }
    return correct_ids, questions


def calculate_score(attempt):
    """Calculate awarded marks, possible marks, percentage, and pass outcome."""
    correct_ids, questions = compare_submitted_answers(attempt)
    total_marks = sum(question.marks for question in questions)
    score = sum(
        question.marks for question in questions if question.pk in correct_ids
    )
    percentage = (
        (Decimal(score) * Decimal("100") / Decimal(total_marks)).quantize(
            Decimal("0.01"), rounding=ROUND_HALF_UP
        )
        if total_marks
        else Decimal("0.00")
    )
    passed = percentage >= attempt.exam.pass_percentage if total_marks else False
    return {
        "score": score,
        "total_marks": total_marks,
        "percentage": percentage,
        "passed": passed,
    }


@transaction.atomic
def evaluate_attempt(attempt):
    """Evaluate a submitted attempt and persist exactly one result record."""
    locked_attempt = Attempt.objects.select_for_update().select_related(
        "student", "exam"
    ).get(pk=attempt.pk)
    if locked_attempt.status not in (
        Attempt.Status.SUBMITTED,
        Attempt.Status.AUTO_SUBMITTED,
    ):
        raise ValidationError("Only submitted examinations can be evaluated.")
    if not locked_attempt.exam.questions.exists():
        raise ValidationError("An examination with no questions cannot be evaluated.")

    values = calculate_score(locked_attempt)
    result, _ = Result.objects.update_or_create(
        attempt=locked_attempt,
        defaults={
            "student": locked_attempt.student,
            "exam": locked_attempt.exam,
            **values,
        },
    )
    return result
