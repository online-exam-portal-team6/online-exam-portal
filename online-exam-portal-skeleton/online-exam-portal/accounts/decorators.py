"""Role-based access decorators (contract B6). Owner: Bhumika.

Admin   = user with is_staff True.
Student = authenticated user with is_staff False.
Anonymous users are sent to the login page; a logged-in user with the wrong role gets HTTP 403.
"""
from functools import wraps

from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


def _role_required(is_allowed):
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if not is_allowed(request.user):
                raise PermissionDenied
            return view(request, *args, **kwargs)
        return wrapper
    return decorator


student_required = _role_required(lambda user: not user.is_staff)
admin_required = _role_required(lambda user: user.is_staff)
