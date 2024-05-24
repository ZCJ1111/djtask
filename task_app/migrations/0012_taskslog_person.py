# Generated by Django 3.2.25 on 2024-05-08 22:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
        ('task_app', '0011_taskslog_task_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskslog',
            name='person',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='user_app.user', verbose_name='操作人'),
            preserve_default=False,
        ),
    ]
