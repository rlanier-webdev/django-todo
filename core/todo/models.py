from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link each task to a user
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False, verbose_name='Completed')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='low')  # Priority field with choices
    deadline = models.DateTimeField(null=True, blank=True) 


    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']