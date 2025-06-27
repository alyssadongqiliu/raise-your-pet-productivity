from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

urlpatterns = [
    # Health check endpoint
    path('ping/', lambda request: HttpResponse('pong')),

    # Admin site
    path('admin/', admin.site.urls),

    # All API routes from app/urls.py live under /api/
    path('api/', include('app.urls')),
]
