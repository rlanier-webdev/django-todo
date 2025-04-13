import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from .models import Task

class TaskTable(tables.Table):
    priority = tables.Column()
    actions = tables.Column(empty_values=(), orderable=False)
    is_completed = tables.Column(empty_values=())

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
        # Generates 'Edit' and 'Delete' buttons for each task
        edit_url = reverse('task_edit', args=[record.pk])
        delete_url = reverse('task_delete', args=[record.pk])
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary me-1">Edit</a>'
            '<a href="{}" class="btn btn-sm btn-danger">Delete</a>',
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
