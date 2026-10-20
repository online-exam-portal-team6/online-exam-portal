from django.urls import path

from . import views, views_admin

app_name = "accounts"

urlpatterns = [
    path("accounts/login/", views.login_view, name="login"),
    path("accounts/register/", views.register_view, name="register"),
    path("accounts/logout/", views.logout_view, name="logout"),
    path("manage/students/", views_admin.student_list, name="student_list"),
    path("manage/students/<int:pk>/toggle/", views_admin.student_toggle, name="student_toggle"),
]
