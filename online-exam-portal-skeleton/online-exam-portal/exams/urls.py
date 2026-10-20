from django.urls import path

from . import views

app_name = "exams"

urlpatterns = [
    path("student/", views.student_dashboard, name="student_dashboard"),
    path("manage/", views.admin_dashboard, name="admin_dashboard"),
    path("manage/exams/", views.exam_list, name="exam_list"),
    path("manage/exams/new/", views.exam_create, name="exam_create"),
    path("manage/exams/<int:pk>/edit/", views.exam_edit, name="exam_edit"),
    path("manage/exams/<int:pk>/toggle/", views.exam_toggle, name="exam_toggle"),
]
