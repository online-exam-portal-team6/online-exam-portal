from django.urls import path

from . import views

app_name = "results"

urlpatterns = [
    path("results/", views.result_list, name="result_list"),
    path("results/<int:attempt_id>/", views.result_detail, name="result_detail"),
    path("manage/results/", views.admin_result_list, name="admin_result_list"),
]
