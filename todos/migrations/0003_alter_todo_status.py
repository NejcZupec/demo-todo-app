# Generated by Django 5.2 on 2025-04-16 07:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0002_remove_todo_completed_todo_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todo',
            name='status',
            field=models.CharField(choices=[('backlog', 'Backlog'), ('doing', 'Doing'), ('review', 'Review'), ('done', 'Done')], default='backlog', max_length=20),
        ),
    ]
