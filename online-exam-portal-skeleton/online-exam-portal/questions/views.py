"""Question management views. Owner: Thejas."""

from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.decorators import admin_required
from exams.models import Exam

from .forms import QuestionForm
from .models import Question


@admin_required
def question_list(request, exam_id):
    """Display all questions belonging to an examination."""
    exam = get_object_or_404(Exam, pk=exam_id)
    questions = Question.objects.filter(exam=exam)

    return render(
        request,
        "questions/question_list.html",
        {
            "exam": exam,
            "questions": questions,
        },
    )


@admin_required
def question_create(request, exam_id):
    """Add an MCQ question to an examination."""
    exam = get_object_or_404(Exam, pk=exam_id)

    if request.method == "POST":
        form = QuestionForm(request.POST)

        if form.is_valid():
            question = form.save(commit=False)
            question.exam = exam
            question.save()

            messages.success(request, "Question added successfully.")
            return redirect("questions:question_list", exam_id=exam.id)
    else:
        form = QuestionForm()

    return render(
        request,
        "questions/question_form.html",
        {
            "form": form,
            "exam": exam,
            "question": None,
        },
    )


@admin_required
def question_edit(request, exam_id, pk):
    """Edit an MCQ question belonging to an examination."""
    exam = get_object_or_404(Exam, pk=exam_id)
    question = get_object_or_404(Question, pk=pk, exam=exam)

    if request.method == "POST":
        form = QuestionForm(request.POST, instance=question)
        if form.is_valid():
            form.save()
            messages.success(request, "Question updated successfully.")
            return redirect("questions:question_list", exam_id=exam.id)
    else:
        form = QuestionForm(instance=question)

    return render(
        request,
        "questions/question_form.html",
        {
            "form": form,
            "exam": exam,
            "question": question,
        },
    )


@admin_required
def question_delete(request, exam_id, pk):
    # TODO (Thejas, OEP-F-013): show confirmation; delete only on POST.
    return HttpResponse("TODO (Thejas): question delete")
