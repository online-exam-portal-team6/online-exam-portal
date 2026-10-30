"""Exam management views. Owner: Thejas. Replace the stub bodies, keep the decorators and names."""
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.utils import timezone

from .models import Exam
from .services import get_available_exams_for
from accounts.decorators import admin_required, student_required

from .forms import ExamForm
from .models import Exam

from django.contrib.auth import get_user_model

from .models import Exam



@student_required
def student_dashboard(request):
    """OEP-F-010: Display available exams and the student's activity."""
    available_exams = get_available_exams_for(request.user)

    completed_attempts = []

    context = {
        "available_exams": available_exams,
        "completed_attempts": completed_attempts,
        "now": timezone.now(),
    }

    return render(request, "exams/student_dashboard.html", context)


@admin_required
def admin_dashboard(request):
    """Display examination and student statistics for administrators."""
    User = get_user_model()

    context = {
        "exam_count": Exam.objects.count(),
        "active_exam_count": Exam.objects.filter(is_active=True).count(),
        "student_count": User.objects.filter(is_staff=False).count(),
        "recent_exams": Exam.objects.select_related("created_by").order_by(
            "-created_at"
        )[:5],
    }

    return render(request, "exams/admin_dashboard.html", context)


@admin_required
def exam_list(request):
    """Display all examinations for administrators."""
    exams = Exam.objects.select_related("created_by").order_by("-created_at")

    return render(request, "exams/exam_list.html", {"exams": exams})



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
@admin_required
def exam_edit(request, pk):
    """OEP-26: Allow an administrator to update an existing examination."""

    exam = get_object_or_404(Exam, pk=pk)

    if request.method == "POST":
        form = ExamForm(request.POST, instance=exam)

        if form.is_valid():
            exam = form.save()

            messages.success(
                request,
                f'Examination "{exam.title}" was updated successfully.'
            )

            return redirect("exams:exam_list")

    else:
        form = ExamForm(instance=exam)

    return render(
        request,
        "exams/exam_form.html",
        {
            "form": form,
            "exam": exam,
        },
    )


@admin_required
def exam_toggle(request, pk):
    # TODO (Thejas, stretch OEP-F-009): activate / deactivate an exam
    return HttpResponse("TODO (Thejas): exam toggle")
