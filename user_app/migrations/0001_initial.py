# Generated by Django 3.2.25 on 2024-04-21 02:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('task_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('name', models.CharField(max_length=100, verbose_name='资源名称')),
                ('action', models.CharField(max_length=100, verbose_name='操作代号')),
            ],
            options={
                'verbose_name': '资源列表',
                'db_table': 'resource',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('name', models.CharField(max_length=100, verbose_name='角色名')),
                ('resource', models.ManyToManyField(to='user_app.Resource', verbose_name='资源')),
            ],
            options={
                'verbose_name': '校色列表',
                'db_table': 'role',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, help_text='创建时间', verbose_name='创建时间')),
                ('updated_at', models.DateTimeField(auto_now=True, help_text='更新时间', verbose_name='更新时间')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=50, verbose_name='密码')),
                ('user_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='姓名')),
                ('sex', models.IntegerField(blank=True, choices=[(1, 'Male'), (2, 'Female'), (3, '未知')], null=True, verbose_name='性别')),
                ('address', models.CharField(blank=True, max_length=350, null=True, verbose_name='地址')),
                ('power', models.IntegerField(choices=[(1, 'Staff'), (3, 'Admin')], default=1, verbose_name='用户类别')),
                ('phone', models.CharField(blank=True, max_length=50, null=True, verbose_name='电话')),
                ('token', models.CharField(blank=True, max_length=50, null=True, verbose_name='用户token')),
                ('role', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='user_app.role', verbose_name='角色')),
                ('task_group', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='task_app.taskgroup', verbose_name='所属任务组')),
            ],
            options={
                'verbose_name': '用户列表',
                'db_table': 'users',
            },
        ),
    ]
