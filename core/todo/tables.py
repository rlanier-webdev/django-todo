import django_tables2 as tables # type: ignore
from django.urls import reverse
from django.utils.html import format_html
import django_filters
from django import forms
from .models import Task

class TaskFilter(django_filters.FilterSet):
    # Define filters for task fields
    title = django_filters.CharFilter(
        lookup_expr='icontains',
        label='Title',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search title...'})
    )
    priority = django_filters.ChoiceFilter(
        choices=Task.PRIORITY_CHOICES,
        label='Priority',
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    deadline = django_filters.DateFilter(
        lookup_expr='gte',
        label='Deadline After',
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )


    class Meta:
        model = Task
        fields = ['title', 'priority', 'deadline']  # filterable fields


class TaskTable(tables.Table):
    title = tables.Column()
    priority = tables.Column()
    actions = tables.Column(empty_values=(), orderable=False)
    is_completed = tables.Column(empty_values=())

    def render_title(self, value, record):
        return format_html(
            '<a href="{}" class="fw-bold text-body text-decoration-none">{}</a>',
            reverse('task_view', args=[record.id]),
            value
        )
    
    def render_priority(self, value):
        # Normalize the priority to lowercase for consistent class application
        priority = str(value).lower().strip()  # normalize it to lowercase string

        # Define CSS classes for different priority levels
        css_class = {
            'low': 'badge bg-success',
            'medium': 'badge bg-info text-dark',
            'high': 'badge bg-warning text-dark',
            'urgent': 'badge bg-danger',
        }.get(priority, 'badge bg-secondary')  # fallback to gray

        return format_html('<span class="{}">{}</span>', css_class, priority.capitalize())

    def render_actions(self, record):
        # Generates 'View', 'Edit' and 'Delete' buttons for each task
        view_url = reverse('task_view', args=[record.pk])
        edit_url = reverse('task_edit', args=[record.pk])
        delete_url = reverse('task_delete', args=[record.pk])
        return format_html(
            '<a href="{}" class="btn btn-sm btn-success me-1" title="View Details"><i class="fa-solid fa-eye"></i></a>'
            '<a href="{}" class="btn btn-sm btn-primary me-1" title="Edit Task"><i class="fa-solid fa-pencil"></i></a>'
            '<a href="{}" class="btn btn-sm btn-danger" title="Delete Task"><i class="fa-solid fa-trash"></i></a>',
            view_url,
            edit_url,
            delete_url
        )

    def render_is_completed(self, record):
        # Renders the checkbox for completion toggle
        return format_html(
            '<input type="checkbox" class="form-check-input toggle-completed" data-id="{}" {}>',
            record.pk,
            'checked' if record.is_completed else ''
        )
    
    class Meta:
        model = Task
        template_name = "django_tables2/bootstrap5.html"  # Use bootstrap5 template for styling
        fields = ("title", "description", "priority", "deadline", "is_completed")  # Fields to display
        sequence = ("title", "description", "priority", "deadline", "is_completed", "actions")  # Column order
