from django.urls import path
from .views import AssistantView, ClearMessageHistory, Test

urlpatterns = [
    path('', AssistantView.as_view()),
    path('clear-history/', ClearMessageHistory.as_view()),
    path('mood/', Test.as_view())
]
