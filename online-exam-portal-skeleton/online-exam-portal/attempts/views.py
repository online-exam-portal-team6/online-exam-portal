"""Exam-taking views. Owner: Bhumika."""
import math

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.decorators import student_required
from exams.models import Exam
from questions.models import Question

from .models import Attempt
from .services import start_attempt


@student_required
def exam_start(request, exam_id):
    exam = get_object_or_404(Exam, pk=exam_id)
    if request.method == "POST":
        try:
            attempt = start_attempt(request.user, exam)
        except ValidationError as exc:
            messages.error(request, " ".join(exc.messages))
        else:
            return redirect("attempts:exam_take", attempt_id=attempt.pk)

    now = timezone.now()
    is_available = exam.is_active and exam.start_time <= now <= exam.end_time
    return render(
        request,
        "attempts/exam_start.html",
        {"exam": exam, "is_available": is_available},
    )


@student_required
def exam_take(request, attempt_id):
    attempt = get_object_or_404(
        Attempt.objects.select_related("exam"),
        pk=attempt_id,
        student=request.user,
    )
    if attempt.status != Attempt.Status.IN_PROGRESS:
        messages.info(request, "This examination attempt has already been submitted.")
        return redirect("exams:student_dashboard")

    remaining_seconds = max(
        0,
        math.ceil((attempt.deadline_at - timezone.now()).total_seconds()),
    )
    questions = Question.objects.filter(exam=attempt.exam).order_by("id")
    context = {
        "attempt": attempt,
        "exam": attempt.exam,
        "questions": questions,
        "saved_answers": {},
        "remaining_seconds": remaining_seconds,
        "answer_url": None,
        "submit_url": None,
        "is_expired": remaining_seconds <= 0,
    }
    return render(request, "attempts/exam_take.html", context)


@student_required
@require_POST
def save_answer(request, attempt_id):
    # TODO (Bhumika, OEP-F-017): JSON in {question_id, option}; out {ok, remaining_seconds} or 403 {expired: true}
    return HttpResponse("TODO (Bhumika): save answer")


@student_required
@require_POST
def exam_submit(request, attempt_id):
    # TODO (Bhumika, OEP-F-018/019): submit_attempt(...), redirect to results:result_detail
    return HttpResponse("TODO (Bhumika): exam submit")
