from django.urls import path

from . import views

app_name = "attempts"

urlpatterns = [
    path("exams/<int:exam_id>/start/", views.exam_start, name="exam_start"),
    path("attempts/<int:attempt_id>/take/", views.exam_take, name="exam_take"),
    path("attempts/<int:attempt_id>/answer/", views.save_answer, name="save_answer"),
    path("attempts/<int:attempt_id>/submit/", views.exam_submit, name="exam_submit"),
    path("attempts/<int:attempt_id>/result/", views.exam_result, name="exam_result"),
]
