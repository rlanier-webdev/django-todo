"""
Models for the todo application.

Defines Task, Category, and TaskActivity models for task management.
"""

from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Category for organizing tasks."""

    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Task(models.Model):
    """A task or todo item belonging to a user."""

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

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    priority = models.CharField(
        max_length=6,
        choices=PRIORITY_CHOICES,
        default='low'
    )
    deadline = models.DateTimeField(null=True, blank=True)
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='pending'
    )
    is_completed = models.BooleanField(default=False, verbose_name='Completed')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='tasks'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Created')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Updated')

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Ensure status and is_completed are always in sync."""
        # Sync is_completed based on status
        if self.status == 'completed':
            self.is_completed = True
        elif self.is_completed:
            self.status = 'completed'
        super().save(*args, **kwargs)


class TaskActivity(models.Model):
    """Audit log for tracking changes to tasks."""

    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    action = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    changes = models.JSONField(blank=True, null=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = "Task Activity"
        verbose_name_plural = "Task Activities"

    def __str__(self):
        return f"{self.action} - {self.task.title}"
