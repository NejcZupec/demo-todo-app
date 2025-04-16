from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .models import Todo

# Create your views here.

class TodoListView(ListView):
    model = Todo
    template_name = 'todos/kanban.html'
    context_object_name = 'todos'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['todos_by_status'] = {
            'backlog': self.object_list.filter(status='backlog'),
            'doing': self.object_list.filter(status='doing'),
            'review': self.object_list.filter(status='review'),
            'done': self.object_list.filter(status='done'),
        }
        return context

class TodoCreateView(CreateView):
    model = Todo
    template_name = 'todos/todo_form.html'
    fields = ['title', 'description', 'card_color']
    success_url = reverse_lazy('todo-list')

@csrf_exempt
@require_POST
def update_todo_status(request, pk):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        todo = get_object_or_404(Todo, pk=pk)
        new_status = request.POST.get('status')
        if new_status in dict(Todo.STATUS_CHOICES):
            todo.status = new_status
            todo.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

@csrf_exempt
@require_POST
def update_todo_color(request, pk):
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        todo = get_object_or_404(Todo, pk=pk)
        new_color = request.POST.get('color')
        if new_color and new_color.startswith('#'):
            todo.card_color = new_color
            todo.save()
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
