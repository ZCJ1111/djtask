# Generated by Django 3.2.25 on 2024-04-25 00:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0005_alter_tasksrecord_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasksrecord',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='task_app.tasks', verbose_name='任务'),
        ),
    ]
