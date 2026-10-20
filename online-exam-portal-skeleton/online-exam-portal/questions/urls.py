from django.urls import path

from . import views

app_name = "questions"

urlpatterns = [
    path("manage/exams/<int:exam_id>/questions/", views.question_list, name="question_list"),
    path("manage/exams/<int:exam_id>/questions/new/", views.question_create, name="question_create"),
    path("manage/exams/<int:exam_id>/questions/<int:pk>/edit/", views.question_edit, name="question_edit"),
    path("manage/exams/<int:exam_id>/questions/<int:pk>/delete/", views.question_delete, name="question_delete"),
]
