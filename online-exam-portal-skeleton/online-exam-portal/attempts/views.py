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

from .models import Attempt
from .services import save_answer as save_attempt_answer
from .services import start_attempt, submit_attempt


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
    return render(request, "attempts/exam_start.html", {"exam": exam, "is_available": is_available})


@student_required
def exam_take(request, attempt_id):
    attempt = get_object_or_404(Attempt.objects.select_related("exam"), pk=attempt_id, student=request.user)
    if attempt.status != Attempt.Status.IN_PROGRESS:
        return redirect("attempts:exam_result", attempt_id=attempt.pk)
    remaining_seconds = max(0, math.ceil((attempt.deadline_at - timezone.now()).total_seconds()))
    questions = list(Question.objects.filter(exam=attempt.exam).order_by("id"))
    saved_answers = dict(attempt.answers.values_list("question_id", "selected_option"))
    for question in questions:
        question.selected_option = saved_answers.get(question.pk)
    context = {
        "attempt": attempt, "exam": attempt.exam, "questions": questions,
        "saved_answers": saved_answers, "remaining_seconds": remaining_seconds,
        "answer_url": reverse("attempts:save_answer", args=[attempt.pk]),
        "submit_url": reverse("attempts:exam_submit", args=[attempt.pk]),
        "is_expired": remaining_seconds <= 0,
    }
    return render(request, "attempts/exam_take.html", context)


@student_required
@require_POST
def save_answer(request, attempt_id):
    attempt = get_object_or_404(Attempt, pk=attempt_id, student=request.user)
    try:
        payload = json.loads(request.body or b"{}")
        if not isinstance(payload, dict):
            raise ValidationError("The request body must be a JSON object.")
        question_id = payload.get("question_id")
        option = payload.get("option")
        if isinstance(question_id, bool) or not isinstance(question_id, int):
            raise ValidationError("A valid question_id is required.")
        if not isinstance(option, str):
            raise ValidationError("A selected option is required.")
        answer, remaining_seconds = save_attempt_answer(attempt, question_id, option)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"ok": False, "error": "Invalid JSON request."}, status=400)
    except ValidationError as exc:
        return JsonResponse({"ok": False, "error": " ".join(exc.messages)}, status=400)
    return JsonResponse({"ok": True, "question_id": answer.question_id,
                         "option": answer.selected_option, "remaining_seconds": remaining_seconds})


@student_required
@require_POST
def exam_submit(request, attempt_id):
    attempt = get_object_or_404(Attempt, pk=attempt_id, student=request.user)
    try:
        attempt = submit_attempt(attempt)
    except ValidationError as exc:
        messages.error(request, " ".join(exc.messages))
        return redirect("attempts:exam_take", attempt_id=attempt.pk)
    messages.success(request, "Your examination has been submitted successfully.")
    return redirect("attempts:exam_result", attempt_id=attempt.pk)


@student_required
def exam_result(request, attempt_id):
    attempt = get_object_or_404(
        Attempt.objects.select_related("exam"),
        pk=attempt_id,
        student=request.user,
    )
    if attempt.status == Attempt.Status.IN_PROGRESS:
        return redirect("attempts:exam_take", attempt_id=attempt.pk)
    percentage = (
        round(attempt.score * 100 / attempt.total_questions, 2)
        if attempt.total_questions else 0
    )
    return render(request, "attempts/exam_result.html", {
        "attempt": attempt,
        "percentage": percentage,
    })
