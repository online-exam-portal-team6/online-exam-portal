
"""Admin student management views."""

from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .decorators import admin_required


User = get_user_model()


@admin_required
def student_list(request):
    """Display and search registered student accounts."""

    search_query = request.GET.get("q", "").strip()

    students = User.objects.filter(
        is_staff=False,
        is_superuser=False,
    ).order_by("-date_joined")

    if search_query:
        students = students.filter(
            Q(username__icontains=search_query)
            | Q(first_name__icontains=search_query)
            | Q(last_name__icontains=search_query)
            | Q(email__icontains=search_query)
        )

    context = {
        "students": students,
        "search_query": search_query,
        "total_students": User.objects.filter(
            is_staff=False,
            is_superuser=False,
        ).count(),
        "active_students": User.objects.filter(
            is_staff=False,
            is_superuser=False,
            is_active=True,
        ).count(),
        "disabled_students": User.objects.filter(
            is_staff=False,
            is_superuser=False,
            is_active=False,
        ).count(),
    }

    return render(request, "accounts/student_list.html", context)


@admin_required
@require_POST
def student_toggle(request, pk):
    """Enable or disable a student account."""

    student = get_object_or_404(
        User,
        pk=pk,
        is_staff=False,
        is_superuser=False,
    )

    student.is_active = not student.is_active
    student.save(update_fields=["is_active"])

    if student.is_active:
        messages.success(
            request,
            f"{student.username}'s account has been enabled.",
        )
    else:
        messages.success(
            request,
            f"{student.username}'s account has been disabled.",
        )

    return redirect("accounts:student_list")
