from django.urls import path
from .views import TodoListView, TodoCreateView, update_todo_status

urlpatterns = [
    path('', TodoListView.as_view(), name='todo-list'),
    path('new/', TodoCreateView.as_view(), name='todo-create'),
    path('<int:pk>/update-status/', update_todo_status, name='todo-update-status'),
] 