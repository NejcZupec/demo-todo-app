from django.test import TestCase, Client
from django.urls import reverse
from .models import Todo


class TodoViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        # Create some test todos
        self.todo1 = Todo.objects.create(
            title="Test Todo 1",
            description="Description 1",
            status="backlog",
            card_color="#ffffff"
        )
        self.todo2 = Todo.objects.create(
            title="Test Todo 2",
            description="Description 2",
            status="doing",
            card_color="#f0f0f0"
        )

    def test_todo_list_view(self):
        """Test that the todo list view displays todos correctly"""
        response = self.client.get(reverse('todo-list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'todos/kanban.html')
        
        # Check if todos are properly categorized
        todos_by_status = response.context['todos_by_status']
        self.assertEqual(len(todos_by_status['backlog']), 1)
        self.assertEqual(len(todos_by_status['doing']), 1)
        self.assertEqual(len(todos_by_status['review']), 0)
        self.assertEqual(len(todos_by_status['done']), 0)

    def test_todo_create_view(self):
        """Test creating a new todo"""
        todo_data = {
            'title': 'New Todo',
            'description': 'New Description',
            'card_color': '#e1e1e1'
        }
        response = self.client.post(reverse('todo-create'), todo_data)
        
        # Check if redirect was successful
        self.assertEqual(response.status_code, 302)
        
        # Check if todo was created
        new_todo = Todo.objects.get(title='New Todo')
        self.assertEqual(new_todo.description, 'New Description')
        self.assertEqual(new_todo.status, 'backlog')  # Default status
        self.assertEqual(new_todo.card_color, '#e1e1e1')

    def test_todo_create_view_invalid_data(self):
        """Test creating a todo with invalid data"""
        todo_data = {
            'title': '',  # Title is required
            'description': 'New Description',
            'card_color': '#e1e1e1'
        }
        response = self.client.post(reverse('todo-create'), todo_data)
        
        # Check if form is invalid
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context['form'].errors)

    def test_update_todo_status(self):
        """Test updating todo status via AJAX"""
        response = self.client.post(
            reverse('todo-update-status', kwargs={'pk': self.todo1.pk}),
            {'status': 'doing'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        # Check if update was successful
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        
        # Check if status was updated in database
        updated_todo = Todo.objects.get(pk=self.todo1.pk)
        self.assertEqual(updated_todo.status, 'doing')

    def test_update_todo_status_invalid(self):
        """Test updating todo status with invalid data"""
        response = self.client.post(
            reverse('todo-update-status', kwargs={'pk': self.todo1.pk}),
            {'status': 'invalid_status'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        # Check if error response was returned
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')

    def test_update_todo_color(self):
        """Test updating todo color via AJAX"""
        response = self.client.post(
            reverse('todo-update-color', kwargs={'pk': self.todo1.pk}),
            {'color': '#ff0000'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        # Check if update was successful
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        
        # Check if color was updated in database
        updated_todo = Todo.objects.get(pk=self.todo1.pk)
        self.assertEqual(updated_todo.card_color, '#ff0000')

    def test_update_todo_color_invalid(self):
        """Test updating todo color with invalid data"""
        response = self.client.post(
            reverse('todo-update-color', kwargs={'pk': self.todo1.pk}),
            {'color': 'invalid_color'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        
        # Check if error response was returned
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['status'], 'error')

    def test_todo_not_found(self):
        """Test accessing a non-existent todo"""
        response = self.client.post(
            reverse('todo-update-status', kwargs={'pk': 9999}),
            {'status': 'doing'},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest'
        )
        self.assertEqual(response.status_code, 404)

    def test_non_ajax_request(self):
        """Test updating todo without AJAX request"""
        response = self.client.post(
            reverse('todo-update-status', kwargs={'pk': self.todo1.pk}),
            {'status': 'doing'}
        )
        self.assertEqual(response.status_code, 400)
