# Generated by Django 3.2.25 on 2024-04-25 00:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task_app', '0008_alter_tasksrecord_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tasks',
            name='task_group',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='task_app.taskgroup', verbose_name='所属任务组'),
        ),
    ]
