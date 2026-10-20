"""Authentication views. Owner: Bhumika. Stubs below are replaced as the stories are implemented."""
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


# TODO (Bhumika, OEP-F-001/002): use Django's LoginView, template accounts/login.html, context: form
def login_view(request):
    return HttpResponse("TODO (Bhumika): login page")


# TODO (Bhumika, OEP-F-004): registration form creating User + StudentProfile, template accounts/register.html
def register_view(request):
    return HttpResponse("TODO (Bhumika): register page")


# TODO (Bhumika): POST-only logout, then redirect to accounts:login
def logout_view(request):
    return HttpResponse("TODO (Bhumika): logout")
