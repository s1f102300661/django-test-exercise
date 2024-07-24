from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from todo.models import Task
from django.conf import settings
from django.http import HttpResponse
from PIL import Image

# Create your views here.


def index(request):
    if request.method == 'POST':

        task = Task(title=request.POST['title'], due_at=make_aware(parse_datetime(request.POST['due_at'])), photo=request.FILES.get('photo'))

        if 'like' in request.POST:
            task_id = request.POST['like']
            task = get_object_or_404(Task, pk=task_id)
            task.likes_count += 1
            task.save()
            return redirect('detail', task_id=task_id)

        task = Task(title=request.POST['title'], due_at=make_aware(parse_datetime(request.POST['due_at'])), genre=request.POST.get('genre', 'other') )

        task.save()

    if request.GET.get('order') == 'due':
        tasks = Task.objects.order_by('due_at')
    else:
        tasks = Task.objects.order_by('-posted_at')

    favorite_tasks = Task.objects.filter(favorite=True)

    context = {
        'tasks': tasks,
        'favorite_tasks': favorite_tasks
    }
    return render(request, 'todo/index.html', context)

def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    context = {
        'task': task,
    }
    return render(request, 'todo/detail.html', context)

def update(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    if request.method == 'POST':
        task.title = request.POST['title']
        task.due_at = make_aware(parse_datetime(request.POST['due_at']))
        task.save()
        return redirect(detail, task_id)
    
    context = {
        'task': task
    }
    return render(request, "todo/edit.html", context)

def delete(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.delete()
    return redirect(index)

def close(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")
    task.completed = True
    task.save()
    return redirect(index)

def toggle_favorite(request, task_id):
    task = get_object_or_404(Task, id=task_id)
    task.favorite = not task.favorite
    task.save()
    return redirect('index')

def test_pillow(request):
    try:
        img = Image.new('RGB', (100, 100), color = (73, 109, 137))
        img.save('test_image.png')
        return HttpResponse("Pillow is working correctly.")
    except Exception as e:
        return HttpResponse(f"Error: {e}")

