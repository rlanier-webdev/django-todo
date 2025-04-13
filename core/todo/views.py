from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import TaskForm
from django_tables2.config import RequestConfig
from .models import Task
from .tables import TaskTable


@login_required
def dashboard_view(request):
    tasks = Task.objects.filter(user=request.user).order_by('-created_at')
    table = TaskTable(tasks)
    RequestConfig(request, paginate={"per_page": 10}).configure(table)

    if request.method == 'POST':
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('dashboard')
    else:
        form = TaskForm()

    return render(request, 'todo/dashboard.html', {'table': table, 'form': form})

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
