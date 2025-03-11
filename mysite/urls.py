from django.urls import path, include
from django.contrib import admin
from django.conf import settings

import os
from .views import csrf_token
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())
urlpatterns = [
    path('csrf-token/', csrf_token),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    from django.conf.urls.static import static

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if os.getenv('POSTGRES_LOCALLY') == 'True':
    urlpatterns += [path('kampretlegendbos/', admin.site.urls)]
