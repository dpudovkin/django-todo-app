from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import Task
from .forms import TaskForm

# Create your views here.
@login_required
def index(request):
    tasks = Task.objects.all()
    form = TaskForm()

    if request.method == "POST":
        form = TaskForm(request.POST)
        if form.is_valid:
            form.save()
        return redirect('tasks:list')

    context = {'tasks': tasks, 'form': form}

    return render(request, 'tasks/list.html', context)

@login_required
def update_task(request, pk):
    task = Task.objects.get(id=pk)
    form = TaskForm(instance=task)

    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)
        if form.is_valid:
            form.save()
            return redirect('tasks:list')

    context = {'form': form}

    return render(request, 'tasks/update_task.html', context)

@login_required
def delete_task(request, pk):
    task = Task.objects.get(id=pk)

    if request.method == "POST":
        task.delete()
        return redirect('tasks:list')
    
    context = {'task': task}
    return render(request, 'tasks/delete_task.html', context)