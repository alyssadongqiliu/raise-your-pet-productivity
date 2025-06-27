from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing Task objects.
    Provides CRUD operations for tasks, ordered by creation date.
    
    Additional endpoints:
    - GET /api/tasks/completed/ - Get completed tasks
    - POST /api/tasks/{id}/mark_complete/ - Mark task as complete
    """
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer

    @action(detail=False, methods=['get'])
    def completed(self, request):
        """Get all completed tasks."""
        completed_tasks = self.queryset.filter(status='completed')
        serializer = self.get_serializer(completed_tasks, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def mark_complete(self, request, pk=None):
        """Mark a specific task as completed."""
        task = self.get_object()
        task.status = 'completed'
        task.save()
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    def get_queryset(self):
        """
        Optionally filter tasks by status.
        Usage: /api/tasks/?status=pending
        """
        queryset = Task.objects.all().order_by('-created_at')
        status_filter = self.request.query_params.get('status')
        
        if status_filter:
            queryset = queryset.filter(status=status_filter)
            
        return queryset
