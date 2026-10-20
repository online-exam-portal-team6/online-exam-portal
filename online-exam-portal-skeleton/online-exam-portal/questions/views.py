"""Question management views. Owner: Thejas."""
from django.http import HttpResponse

from accounts.decorators import admin_required


@admin_required
def question_list(request, exam_id):
    # TODO (Thejas): context exam, questions
    return HttpResponse("TODO (Thejas): question list")


@admin_required
def question_create(request, exam_id):
    # TODO (Thejas, OEP-F-011): context form, exam, question=None
    return HttpResponse("TODO (Thejas): question create")


@admin_required
def question_edit(request, exam_id, pk):
    # TODO (Thejas, OEP-F-012): context form, exam, question
    return HttpResponse("TODO (Thejas): question edit")


@admin_required
def question_delete(request, exam_id, pk):
    # TODO (Thejas, OEP-F-013): confirm page (context exam, question); POST deletes
    return HttpResponse("TODO (Thejas): question delete")
