"""Exam-taking views. Owner: Bhumika."""
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.decorators import student_required
from exams.models import Exam

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
    # TODO (Bhumika, OEP-F-015/016): context attempt, exam, questions, saved_answers,
    # remaining_seconds, answer_url, submit_url
    return HttpResponse("TODO (Bhumika): exam take")


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
