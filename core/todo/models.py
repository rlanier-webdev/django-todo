from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in progress', 'In Progress'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link each task to a user
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_completed = models.BooleanField(default=False, verbose_name='Completed')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='low')  # Priority field with choices
    deadline = models.DateTimeField(null=True, blank=True) 
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
        
    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']

@receiver(pre_save, sender=Task)
def update_task_status(sender, instance, **kwargs):
    if not instance.status:  # only set it if empty
        if instance.is_completed:
            instance.status = 'completed'
        else:
            instance.status = 'in progress'

