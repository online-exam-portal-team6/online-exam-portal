
"""Authentication views. Owner: Bhumika."""
from django.contrib.auth.views import LoginView
from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import redirect, render
from django.template import TemplateDoesNotExist


def root_redirect(request):
    """/ sends each kind of user to the right place."""
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


# OEP-F-001/002: login and invalid-credential handling
def login_view(request):
    view = LoginView.as_view(
        template_name="accounts/login.html",
        redirect_authenticated_user=True,
        next_page="/",
    )
    return view(request)


# TODO (Bhumika, OEP-F-004): registration form creating User + StudentProfile

def register_view(request):
    from django.contrib import messages
    from django.contrib.auth.models import User
    from django.contrib.auth.password_validation import validate_password
    from django.core.exceptions import ValidationError
    from django.db import IntegrityError, transaction

    if request.user.is_authenticated:
        return redirect("root")

    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        errors = []

        if not username:
            errors.append("Username is required.")
        elif User.objects.filter(username=username).exists():
            errors.append("That username is already taken.")

        if password != confirm_password:
            errors.append("Passwords do not match.")
        else:
            try:
                validate_password(password)
            except ValidationError as exc:
                errors.extend(exc.messages)

        if errors:
            return render(
                request,
                "accounts/register.html",
                {"errors": errors, "username": username, "email": email},
            )

        try:
            with transaction.atomic():
                User.objects.create_user(
                    username=username,
                    email=email,
                    password=password,
                )
        except IntegrityError:
            return render(
                request,
                "accounts/register.html",
                {
                    "errors": ["That username is already taken."],
                    "username": username,
                    "email": email,
                },
            )

        messages.success(request, "Registration successful! You can now log in.")
        return redirect("accounts:login")

    return render(request, "accounts/register.html")



# TODO (Bhumika): POST-only logout, then redirect to accounts:login
def logout_view(request):
    return HttpResponse("TODO (Bhumika): logout")
