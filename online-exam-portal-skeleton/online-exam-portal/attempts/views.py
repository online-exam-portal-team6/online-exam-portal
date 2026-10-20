"""Exam-taking views. Owner: Bhumika."""
from django.http import HttpResponse
from django.views.decorators.http import require_POST

from accounts.decorators import student_required


@student_required
def exam_start(request, exam_id):
    # TODO (Bhumika, OEP-F-014): GET shows rules (context exam); POST calls start_attempt and redirects to exam_take
    return HttpResponse("TODO (Bhumika): exam start")


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
