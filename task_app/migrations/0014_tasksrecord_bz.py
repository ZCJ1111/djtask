# Generated by Django 3.2.25 on 2024-05-15 22:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0013_taskslog_task_desc'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasksrecord',
            name='bz',
            field=models.TextField(blank=True, null=True, verbose_name='补交备注'),
        ),
    ]
