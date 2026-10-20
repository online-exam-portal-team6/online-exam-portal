"""Admin student management (OEP-F-006). Owner: Thejas."""
from django.http import HttpResponse

from .decorators import admin_required


@admin_required
def student_list(request):
    # TODO (Thejas): list students with profile, template accounts/student_list.html, context: students
    return HttpResponse("TODO (Thejas): student list")


@admin_required
def student_toggle(request, pk):
    # TODO (Thejas): activate / deactivate a student (is_active), then redirect to accounts:student_list
    return HttpResponse("TODO (Thejas): student toggle")
