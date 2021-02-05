from django.urls import path

from . import views

urlpatterns = [
    path('start/', views.CreateGame.as_view(), name="start"),
    path('guess/', views.CreatePollResponse.as_view(), name="guess"),
    path('play/', views.PlayGame.as_view(), name="play"),
]
