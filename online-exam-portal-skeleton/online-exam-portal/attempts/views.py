"""Exam-taking views. Owner: Bhumika."""

import json
import math

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.decorators import student_required
from exams.models import Exam
from questions.models import Question

from .models import Attempt, AttemptAnswer
from .services import save_answer as save_answer_service
from .services import start_attempt, submit_attempt as submit_attempt_service


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
    saved_answers = dict(
        AttemptAnswer.objects.filter(attempt=attempt).values_list(
            "question_id",
            "selected_option",
        )
    )
    for question in questions:
        question.selected_option = saved_answers.get(question.pk)
    context = {
        "attempt": attempt,
        "exam": attempt.exam,
        "questions": questions,
        "saved_answers": saved_answers,
        "remaining_seconds": remaining_seconds,
        "answer_url": reverse("attempts:save_answer", args=[attempt.pk]),
        "submit_url": reverse("attempts:exam_submit", args=[attempt.pk]),
        "is_expired": remaining_seconds <= 0,
    }
    return render(request, "attempts/exam_take.html", context)


@student_required
@require_POST
def save_answer(request, attempt_id):
    """JSON endpoint to save or change one selected MCQ option."""
    attempt = get_object_or_404(
        Attempt.objects.select_related("exam"),
        pk=attempt_id,
        student=request.user,
    )
    if attempt.status != Attempt.Status.IN_PROGRESS:
        return JsonResponse(
            {"ok": False, "error": "This examination has already been submitted."},
            status=403,
        )
    if attempt.deadline_at <= timezone.now():
        return JsonResponse({"ok": False, "expired": True}, status=403)

    try:
        payload = json.loads(request.body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return JsonResponse({"ok": False, "error": "A valid JSON body is required."}, status=400)

    if not isinstance(payload, dict):
        return JsonResponse({"ok": False, "error": "A JSON object is required."}, status=400)

    question_id = payload.get("question_id")
    option = payload.get("option")
    if isinstance(question_id, bool) or not isinstance(question_id, int):
        return JsonResponse({"ok": False, "error": "question_id must be an integer."}, status=400)
    if not isinstance(option, str):
        return JsonResponse({"ok": False, "error": "option must be A, B, C or D."}, status=400)

    try:
        answer = save_answer_service(attempt, question_id, option)
    except ValidationError as exc:
        if attempt.deadline_at <= timezone.now():
            return JsonResponse({"ok": False, "expired": True}, status=403)
        return JsonResponse(
            {"ok": False, "error": " ".join(exc.messages)},
            status=400,
        )

    remaining_seconds = max(
        0,
        math.ceil((attempt.deadline_at - timezone.now()).total_seconds()),
    )
    return JsonResponse(
        {
            "ok": True,
            "question_id": answer.question_id,
            "option": answer.selected_option,
            "remaining_seconds": remaining_seconds,
        }
    )


@student_required
@require_POST
def exam_submit(request, attempt_id):
    """Submit the current attempt manually or automatically after its deadline."""
    attempt = get_object_or_404(
        Attempt.objects.select_related("exam"),
        pk=attempt_id,
        student=request.user,
    )
    if attempt.status == Attempt.Status.IN_PROGRESS:
        auto = attempt.deadline_at <= timezone.now()
        attempt = submit_attempt_service(attempt, auto=auto)
        if attempt.status == Attempt.Status.AUTO_SUBMITTED:
            messages.info(request, "Your time expired. Your answers have been submitted automatically.")
        else:
            messages.success(request, "Your examination has been submitted successfully.")
        messages.info(
            request,
            "Your result will appear after the evaluation service has processed your submission.",
        )
    return redirect("results:result_detail", attempt_id=attempt.pk)
