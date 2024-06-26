# Generated by Django 3.2.25 on 2024-04-22 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user_app', '0001_initial'),
        ('task_app', '0003_tasks_task_group'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='person',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, related_name='person', to='user_app.user', verbose_name='所属人'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tasksrecord',
            name='back_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='back_by', to='user_app.user', verbose_name='审核人'),
        ),
        migrations.AddField(
            model_name='tasksrecord',
            name='back_time',
            field=models.DateTimeField(blank=True, null=True, verbose_name='审核时间'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='creator', to='user_app.user', verbose_name='创建人'),
        ),
        migrations.AlterField(
            model_name='tasks',
            name='task_desc',
            field=models.TextField(default='', verbose_name='任务详情'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='tasks',
            name='task_group',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.PROTECT, to='task_app.taskgroup', verbose_name='所属任务组'),
            preserve_default=False,
        ),
    ]
