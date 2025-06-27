from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse

urlpatterns = [
    # quick health check
    path('ping/', lambda request: HttpResponse('pong')),

    # admin site
    path('admin/', admin.site.urls),

    # mount all app routes under /api/
    path('api/', include('app.urls')),
]
