from django.urls import path
from .views import AssistantView, ClearMessageHistory, MoodItems

urlpatterns = [
    path('', AssistantView.as_view()),
    path('clear-history/', ClearMessageHistory.as_view()),
    path('mood/', MoodItems.as_view())
]
