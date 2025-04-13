import django_tables2 as tables
from django.urls import reverse
from django.utils.html import format_html
from .models import Task

class TaskTable(tables.Table):
    priority = tables.Column()
    actions = tables.Column(empty_values=(), orderable=False)

    def render_priority(self, value):
        priority = str(value).lower().strip()  # normalize it to lowercase string

        css_class = {
            'low': 'badge bg-success',
            'medium': 'badge bg-info text-dark',
            'high': 'badge bg-warning text-dark',
            'urgent': 'badge bg-danger',
        }.get(priority, 'badge bg-secondary')  # fallback to gray

        return format_html('<span class="{}">{}</span>', css_class, priority.capitalize())

    def render_actions(self, record):
        edit_url = reverse('task_edit', args=[record.pk])
        delete_url = reverse('task_delete', args=[record.pk])
        return format_html(
            '<a href="{}" class="btn btn-sm btn-primary me-1">Edit</a>'
            '<a href="{}" class="btn btn-sm btn-danger">Delete</a>',
            edit_url,
            delete_url
        )

    class Meta:
        model = Task
        template_name = "django_tables2/bootstrap5.html"
        fields = ("title", "description", "priority", "deadline", "is_completed")  # don't include 'actions' here
        sequence = ("title", "description", "priority", "deadline", "is_completed", "actions")

