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
    # Filter the tasks based on the GET params and the current user's tasks
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
    task = get_object_or_404(Task, id=task_id, user=request.user)

    previous_page = request.META.get('HTTP_REFERER', '/')

    return render(request, 'todo/task_view.html', {
        'task': task,
        'previous_page': previous_page,
    })

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
            form.save()  # Save the task with updated status
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

    # Safely get the previous page or fallback to dashboard
    previous_page = request.META.get('HTTP_REFERER')
    if not previous_page:
        from django.urls import reverse
        previous_page = reverse('dashboard')

    return render(request, 'todo/task_confirm_delete.html', {
        'task': task,
        'previous_page': previous_page
    })

def toggle_completed(request, task_id):
    if request.method == 'POST':
        try:
            # Parse incoming request body
            data = json.loads(request.body)
            is_completed = data.get('is_completed', False)

            # Retrieve the task by ID
            task = Task.objects.get(id=task_id)

            # Update the 'is_completed' field
            task.is_completed = is_completed

            # Update the 'status' field based on 'is_completed'
            task.status = 'completed' if is_completed else 'in progress'

            # Save the task instance
            task.save()

            # Return success response with updated data
            return JsonResponse({
                'success': True,
                'is_completed': task.is_completed,
                'status': task.status
            })

        except Task.DoesNotExist:
            # If the task does not exist, return an error
            return JsonResponse({'success': False, 'error': 'Task not found'}, status=404)

        except Exception as e:
            # Catch any other exceptions and return an error
            return JsonResponse({'success': False, 'error': str(e)}, status=400)

    # Handle non-POST requests
    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

def calendar_view(request):
    tasks = Task.objects.filter(user=request.user)

    context = {
        'tasks': tasks,
    }
    return render(request, 'todo/calendar_view.html', context)