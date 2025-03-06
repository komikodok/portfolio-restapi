from django.urls import path, re_path, include
from django.contrib import admin
from django.conf import settings

from .views import csrf_token # ProtectedMediaView

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('kampretlegendbos/', admin.site.urls),
    path('csrf-token/', csrf_token),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)