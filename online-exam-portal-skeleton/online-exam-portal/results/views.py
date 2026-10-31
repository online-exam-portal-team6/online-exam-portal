"""Student and administrator result pages.

The result UI deliberately adapts to the Attempt/Result models supplied by the
exam workflow. It does not create or mutate evaluation records; evaluation and
persistence remain the responsibility of the results service.
"""

from django.apps import apps
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.http import Http404
from django.shortcuts import get_object_or_404, render

from accounts.decorators import admin_required, student_required


def _attempt_model():
    """Return the Attempt model when the attempts app has registered it."""
    try:
        return apps.get_model("attempts", "Attempt")
    except LookupError:
        return None


def _field_names(model):
    """Return concrete model field names without assuming a particular schema."""
    return {field.name for field in model._meta.get_fields()}


def _owner_field(model):
    """Find the user relation used by the Attempt model."""
    names = _field_names(model)
    for candidate in ("student", "user", "candidate"):
        if candidate in names:
            return candidate
    return None


def _related_result(attempt):
    """Resolve a persisted result attached to an attempt, if one exists."""
    for relation_name in ("result", "exam_result"):
        try:
            related = getattr(attempt, relation_name)
        except (AttributeError, LookupError):
            continue
        if related is not None:
            return related
    try:
        result_model = apps.get_model("results", "Result")
    except LookupError:
        return None
    if "attempt" not in _field_names(result_model):
        return None
    try:
        return result_model.objects.filter(attempt=attempt).first()
    except (TypeError, ValueError):
        # Compatibility for legacy view tests/adapters that supply a lightweight
        # attempt object rather than a persisted Django model instance.
        return None


def _read_value(objects, names):
    """Read the first non-null attribute from a sequence of related objects."""
    for obj in objects:
        if obj is None:
            continue
        for name in names:
            value = getattr(obj, name, None)
            if value is not None:
                return value
    return None


def _is_completed(attempt, result):
    """Only show submitted/evaluated attempts in result history."""
    if result is not None:
        return True
    submitted_at = _read_value([attempt], ("submitted_at", "completed_at", "evaluated_at"))
    if submitted_at is not None:
        return True
    is_submitted = _read_value([attempt], ("is_submitted", "is_completed", "is_evaluated"))
    if is_submitted is not None:
        return bool(is_submitted)
    status = _read_value([attempt], ("status", "state"))
    return str(status).lower() in {"submitted", "completed", "evaluated", "graded"}


def _normalise_result(attempt):
    """Build a stable template context from an Attempt and its persisted result."""
    result = _related_result(attempt)
    exam = getattr(attempt, "exam", None)
    student = _read_value([attempt], ("student", "user", "candidate"))
    score = _read_value([result, attempt], ("score", "marks_obtained", "total_score"))
    total_marks = _read_value(
        [result, attempt, exam],
        ("total_marks", "max_marks", "maximum_score", "max_score"),
    )
    percentage = _read_value([result, attempt], ("percentage", "score_percentage"))
    passed = _read_value([result, attempt], ("passed", "is_passed"))
    if passed is None:
        passed = _read_value([result, attempt], ("pass_status",))
    completed_at = _read_value(
        [result, attempt],
        ("submitted_at", "completed_at", "evaluated_at", "created_at"),
    )
    return {
        "attempt_id": attempt.pk,
        "attempt": attempt,
        "result": result,
        "exam": exam,
        "exam_title": _read_value([exam], ("title", "name")) or "Examination",
        "student": student,
        "student_name": (
            student.get_full_name() or student.get_username()
            if student is not None and hasattr(student, "get_full_name")
            else str(student) if student is not None else "Student"
        ),
        "score": score,
        "total_marks": total_marks,
        "percentage": percentage,
        "passed": passed,
        "completed_at": completed_at,
    }


def _completed_attempts(queryset):
    """Filter a queryset to evaluated/submitted attempts before normalising it."""
    rows = []
    for attempt in queryset:
        result = _related_result(attempt)
        if _is_completed(attempt, result):
            rows.append(_normalise_result(attempt))
    return rows


@student_required
def result_list(request):
    """Show only the signed-in student's completed examination results."""
    attempt_model = _attempt_model()
    results = []
    if attempt_model is not None:
        owner = _owner_field(attempt_model)
        if owner:
            queryset = attempt_model.objects.filter(**{owner: request.user})
            results = _completed_attempts(queryset)
    return render(request, "results/result_list.html", {"results": results})


@login_required
def result_detail(request, attempt_id):
    """Show a completed result to its owner or an administrator."""
    attempt_model = _attempt_model()
    if attempt_model is None:
        raise Http404("Result not found")

    attempt = get_object_or_404(attempt_model, pk=attempt_id)
    owner = _owner_field(attempt_model)
    if not request.user.is_staff:
        if owner is None or getattr(attempt, owner + "_id", None) != request.user.pk:
            raise PermissionDenied

    result = _related_result(attempt)
    if not _is_completed(attempt, result):
        raise Http404("Result not found")

    context = _normalise_result(attempt)
    return render(request, "results/result_detail.html", context)


@admin_required
def admin_result_list(request):
    """Show completed results across students to administrators."""
    attempt_model = _attempt_model()
    results = []
    if attempt_model is not None:
        results = _completed_attempts(attempt_model.objects.all())
    passed_count = sum(
        1 for item in results
        if item["passed"] is True or str(item["passed"]).lower() in {"pass", "passed"}
    )
    return render(
        request,
        "results/admin_result_list.html",
        {"results": results, "passed_count": passed_count},
    )
