from django.urls import path
from .views import dashboard, delete_job, edit_job, login_view

urlpatterns = [
    path("login/", login_view, name="login"),
    path("", dashboard, name="dashboard"),
    path("delete/<int:job_id>/", delete_job, name="delete"),
    path("edit/<int:job_id>/", edit_job, name="edit"),
]
