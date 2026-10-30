from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST
from django.template import TemplateDoesNotExist
from django.http import HttpResponseForbidden

from .forms import RegistrationForm


def root_redirect(request):
    """Redirect users to the dashboard matching their role."""
    if not request.user.is_authenticated:
        return redirect("accounts:login")

    if request.user.is_staff:
        return redirect("exams:admin_dashboard")

    return redirect("exams:student_dashboard")


def error_403(request, exception=None):
    try:
        return render(request, "403.html", status=403)
    except TemplateDoesNotExist:
        return HttpResponseForbidden("403 Forbidden")


def login_view(request):
    if request.user.is_authenticated:
        return redirect("root")

    form = AuthenticationForm(request, data=request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        login(request, user)

        messages.success(request, f"Welcome back, {user.first_name or user.username}!")

        next_url = request.POST.get("next") or request.GET.get("next")

        if next_url and url_has_allowed_host_and_scheme(
            next_url,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(next_url)

        return redirect("root")

    return render(
        request,
        "accounts/login.html",
        {
            "form": form,
            "next": request.GET.get("next", ""),
        },
    )


def register_view(request):
    if request.user.is_authenticated:
        return redirect("root")

    form = RegistrationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)

        messages.success(
            request,
            "Your account has been created successfully. Welcome!"
        )

        return redirect("root")

    return render(
        request,
        "accounts/register.html",
        {"form": form},
    )


@require_POST
@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("accounts:login")
