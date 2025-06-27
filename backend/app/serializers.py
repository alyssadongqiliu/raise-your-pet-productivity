from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for Task model.
    Handles conversion between Task instances and JSON.
    """
    
    class Meta:
        model = Task
        fields = ['id', 'title', 'status', 'created_at']
        read_only_fields = ['created_at']

    def validate_title(self, value):
        """Validate task title."""
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty or whitespace only.")
        return value.strip()
