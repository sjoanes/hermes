from django.urls import path
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    path("start/", views.CreateGame.as_view(), name="start"),
    path("guess/", views.CreatePollResponse.as_view(), name="guess"),
    path("", TemplateView.as_view(template_name="index.html")),
]
