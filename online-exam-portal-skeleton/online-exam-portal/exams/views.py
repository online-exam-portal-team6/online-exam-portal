"""Exam management views. Owner: Thejas. Replace the stub bodies, keep the decorators and names."""
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render

from accounts.decorators import admin_required, student_required

from .forms import ExamForm


@student_required
def student_dashboard(request):
    # TODO (Thejas, OEP-F-010): context available_exams (via services), completed_attempts
    return HttpResponse("TODO (Thejas): student dashboard")


@admin_required
def admin_dashboard(request):
    # TODO (Thejas): context exam_count, student_count, recent_exams
    return HttpResponse("TODO (Thejas): admin dashboard")


@admin_required
def exam_list(request):
    # TODO (Thejas): context exams
    return HttpResponse("TODO (Thejas): exam list")


@admin_required
def exam_create(request):
    """OEP-F-007: an administrator creates an examination."""
    if request.method == "POST":
        form = ExamForm(request.POST)
        if form.is_valid():
            exam = form.save(commit=False)
            exam.created_by = request.user
            exam.save()
            messages.success(request, f'Examination "{exam.title}" was created.')
            return redirect("exams:exam_list")
    else:
        form = ExamForm()
    return render(request, "exams/exam_form.html", {"form": form, "exam": None})


@admin_required
def exam_edit(request, pk):
    # TODO (Thejas, OEP-F-008): context form, exam
    return HttpResponse("TODO (Thejas): exam edit")


@admin_required
def exam_toggle(request, pk):
    # TODO (Thejas, stretch OEP-F-009): activate / deactivate an exam
    return HttpResponse("TODO (Thejas): exam toggle")
