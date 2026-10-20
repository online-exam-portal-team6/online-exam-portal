"""Result views. Owner: Vijay Suriya."""
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from accounts.decorators import admin_required, student_required


@student_required
def result_list(request):
    # TODO (Vijay): context results (current student only)
    return HttpResponse("TODO (Vijay): my results")


@login_required
def result_detail(request, attempt_id):
    # TODO (Vijay, OEP-F-023): context attempt, exam, result; owner student or staff only, otherwise 403
    return HttpResponse("TODO (Vijay): result detail")


@admin_required
def admin_result_list(request):
    # TODO (Vijay, OEP-F-024): context results (all, with student and exam)
    return HttpResponse("TODO (Vijay): admin result list")
