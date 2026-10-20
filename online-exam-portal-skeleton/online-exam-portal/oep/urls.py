"""Root URLs. Every app defines its own full paths (see team contract B7). Owner: Bhumika."""
from django.contrib import admin
from django.urls import include, path

from accounts.views import root_redirect

urlpatterns = [
    path("django-admin/", admin.site.urls),
    path("", root_redirect, name="root"),
    path("", include("accounts.urls")),
    path("", include("exams.urls")),
    path("", include("questions.urls")),
    path("", include("attempts.urls")),
    path("", include("results.urls")),
]

handler403 = "accounts.views.error_403"
