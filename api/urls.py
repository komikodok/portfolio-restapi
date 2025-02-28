from django.urls import path, include
from .views import ApiRootView

urlpatterns = [
    path('', ApiRootView.as_view()),
    path('contact/', include('contact.urls')),
    path('projects/', include('projects.urls')),
    path('assistant/', include('assistant.urls')),
]
