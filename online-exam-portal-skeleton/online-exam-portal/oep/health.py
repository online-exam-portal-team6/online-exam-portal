"""Minimal unauthenticated health endpoint for the hosting platform."""

from django.http import HttpResponse
from django.views.decorators.http import require_GET


@require_GET
def health_check(request):
    return HttpResponse("ok", content_type="text/plain")
