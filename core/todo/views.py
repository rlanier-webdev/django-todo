"""
Views for the todo application.

Handles task management including CRUD operations, dashboard display,
calendar views, and category management.
"""

import json
import logging

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django_tables2.config import RequestConfig

from .forms import TaskForm
from .models import Category, Task
from .tables import TaskFilter, TaskTable
from billing.services import track_todo_created

logger = logging.getLogger(__name__)

@login_required
def dashboard_view(request):
    """
    Display the user's task dashboard with filtering and pagination.

    Shows active and completed tasks in separate tables with filter options.
    """
    task_filter = TaskFilter(request.GET, queryset=Task.objects.filter(user=request.user))
    filtered_tasks = task_filter.qs

    # Split the filtered tasks after the filter has been applied
    active_tasks = filtered_tasks.filter(is_completed=False).order_by('-created_at')
    completed_tasks = filtered_tasks.filter(is_completed=True).order_by('-created_at')

    # Separate tables for active and completed tasks
    active_table = TaskTable(active_tasks)
    completed_table = TaskTable(completed_tasks)

    # Paginate the tables
    RequestConfig(request, paginate={"per_page": 10}).configure(active_table)
    RequestConfig(request, paginate={"per_page": 10}).configure(completed_table)

    # Handle task creation
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()

    context = {
        'form': form,
        'active_table': active_table,
        'completed_table': completed_table,
        'filter': task_filter,  # Pass the filter to the template
    }
    return render(request, 'todo/dashboard.html', context)



@login_required
def task_view(request, task_id):
    """Display detailed view of a single task with activity history."""
    task = get_object_or_404(Task, id=task_id, user=request.user)

    previous_page = request.META.get('HTTP_REFERER', '/')

    return render(request, 'todo/task_view.html', {
        'task': task,
        'previous_page': previous_page,
    })

@login_required
def task_create(request):
    """Create a new task for the current user."""
    if request.method == "POST":
        form = TaskForm(request.POST)

        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()

            try:
                track_todo_created(task)
            except Exception:
                # Billing should never block task creation
                logger.exception(
                    "Failed to track todo.created event",
                    extra={
                        "task_id": task.id,
                        "user_id": request.user.id,
                    },
                )

            return redirect("dashboard")

    else:
        form = TaskForm()

    return render(request, "todo/task_form.html", {"form": form})

@login_required
def task_edit(request, task_id):
    """Edit an existing task owned by the current user."""
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()  # Save the task with updated status
            return redirect('dashboard')
    else:
        form = TaskForm(instance=task)

    return render(request, 'todo/task_edit.html', {'form': form})


@login_required
def task_delete(request, task_id):
    """Delete a task owned by the current user with confirmation."""
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        task.delete()
        return redirect('dashboard')

    # Safely get the previous page or fallback to dashboard
    previous_page = request.META.get('HTTP_REFERER')
    if not previous_page:
        from django.urls import reverse
        previous_page = reverse('dashboard')

    return render(request, 'todo/task_confirm_delete.html', {
        'task': task,
        'previous_page': previous_page
    })

@login_required
@require_POST
def toggle_completed(request, task_id):
    """Toggle the completion status of a task via AJAX."""
    try:
        data = json.loads(request.body)
        is_completed = data.get('is_completed', False)

        # Only allow users to toggle their own tasks
        task = get_object_or_404(Task, id=task_id, user=request.user)

        task.is_completed = is_completed
        task.status = 'completed' if is_completed else 'in progress'
        task.save()

        return JsonResponse({
            'success': True,
            'is_completed': task.is_completed,
            'status': task.status
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON'}, status=400)

    except Exception as e:
        logger.exception("Error toggling task completion")
        return JsonResponse(
            {'success': False, 'error': 'An unexpected error occurred.'},
            status=500
        )

@login_required
def calendar_view(request):
    """Display tasks in a calendar format."""
    tasks = Task.objects.filter(user=request.user).select_related('category')

    context = {
        'tasks': tasks,
    }
    return render(request, 'todo/calendar_view.html', context)

@login_required
@require_POST
def add_category(request):
    """Create a new category via AJAX request."""
    name = request.POST.get('name')
    if name:
        category, created = Category.objects.get_or_create(name=name)
        return JsonResponse({
            'id': category.id,
            'name': category.name
        })
    return JsonResponse({'error': 'Name is required'}, status=400)