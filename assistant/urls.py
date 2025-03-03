from django.urls import path
from .views import AssistantView, ClearMessageHistory

urlpatterns = [
    path('', AssistantView.as_view()),
    path('clear-history/', ClearMessageHistory.as_view())
]
