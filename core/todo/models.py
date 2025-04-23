from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    

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
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    priority = models.CharField(max_length=6, choices=PRIORITY_CHOICES, default='low')
    deadline = models.DateTimeField(null=True, blank=True) 
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    is_completed = models.BooleanField(default=False, verbose_name='Completed')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')

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

class TaskActivity(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    changes = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']

