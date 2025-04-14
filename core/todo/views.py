from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import TaskForm
from django_tables2.config import RequestConfig # type: ignore
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json     
from .models import Task
from .tables import TaskTable, TaskFilter


@login_required
def dashboard_view(request):
    # Apply the TaskFilter to the tasks
    task_filter = TaskFilter(request.GET, queryset=Task.objects.filter(user=request.user))
    filtered_tasks = task_filter.qs

    # Split the filtered tasks into active and completed tasks
    active_tasks = filtered_tasks.filter(is_completed=False).order_by('-created_at')
    completed_tasks = filtered_tasks.filter(is_completed=True).order_by('-created_at')

    # Separate tables for each
    active_table = TaskTable(active_tasks)
    completed_table = TaskTable(completed_tasks)

    # Paginate the tables
    RequestConfig(request, paginate={"per_page": 10}).configure(active_table)
    RequestConfig(request, paginate={"per_page": 10}).configure(completed_table)

    # Handle task creation (unchanged)
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
    task = get_object_or_404(Task, id=task_id, user=request.user)
    return render(request, 'todo/task_view.html', {'task': task})

@login_required
def task_create(request):
    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()
    
    return render(request, 'todo/task_form.html', {'form': form})

@login_required
def task_edit(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirect to the 'dashboard' view
    else:
        form = TaskForm(instance=task)

    return render(request, 'todo/task_edit.html', {'form': form})

@login_required
def task_delete(request, task_id):
    task = get_object_or_404(Task, id=task_id, user=request.user)

    if request.method == "POST":
        task.delete()
        return redirect('dashboard')  # Redirect to the 'dashboard' view

    return render(request, 'todo/task_confirm_delete.html', {'task': task})

def toggle_completed(request, task_id):
    if request.method == 'POST':
        try:
            # Parse incoming request body
            data = json.loads(request.body)
            is_completed = data.get('is_completed', False)

            # Retrieve the task by ID and update its completion status
            task = Task.objects.get(id=task_id)
            task.is_completed = is_completed
            task.save()

            # Return success response
            return JsonResponse({'success': True})

        except Task.DoesNotExist:
            # If the task does not exist, return an error
            return JsonResponse({'success': False, 'error': 'Task not found'}, status=404)

        except Exception as e:
            # Catch any other exceptions and return an error
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    # Handle non-POST requests
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

