# backend/app/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TaskViewSet

router = DefaultRouter()
router.register('tasks', TaskViewSet, basename='task')

# MUST be a list
urlpatterns = [
    path('', include(router.urls)),
]
