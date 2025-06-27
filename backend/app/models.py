from django.db import models

class Task(models.Model):
    """
    Model representing a task in the productivity system.
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    
    title = models.CharField(
        max_length=200, 
        help_text="Task title"
    )
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES,
        default='pending',
        help_text="Current status of the task"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the task was created"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Tasks"

    def __str__(self):
        return self.title

    def is_completed(self):
        """Check if task is completed."""
        return self.status == 'completed'
