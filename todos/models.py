from django.db import models

# Create your models here.

class Todo(models.Model):
    STATUS_CHOICES = [
        ('backlog', 'Backlog'),
        ('doing', 'Doing'),
        ('review', 'Review'),
        ('done', 'Done'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='backlog'
    )
    card_color = models.CharField(max_length=7, default='#ffffff')  # Store color as hex code

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']
