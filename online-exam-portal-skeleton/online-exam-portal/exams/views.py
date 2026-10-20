"""Exam management views. Owner: Thejas. Replace the stub bodies, keep the decorators and names."""
from django.http import HttpResponse

from accounts.decorators import admin_required, student_required


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
    # TODO (Thejas, OEP-F-007): context form, exam=None
    return HttpResponse("TODO (Thejas): exam create")


@admin_required
def exam_edit(request, pk):
    # TODO (Thejas, OEP-F-008): context form, exam
    return HttpResponse("TODO (Thejas): exam edit")


@admin_required
def exam_toggle(request, pk):
    # TODO (Thejas, stretch OEP-F-009): activate / deactivate an exam
    return HttpResponse("TODO (Thejas): exam toggle")
