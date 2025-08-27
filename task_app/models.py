from django.db import models

from user_app.models import User, TaskGroup
from utils.base_model import BaseModel


# Create your models here.


class Tasks(BaseModel):
    task_time_start = models.TimeField(verbose_name="start time")
    task_time_end = models.TimeField(verbose_name="cutoff time")
    task_title = models.CharField(max_length=200, verbose_name="task title")
    task_desc = models.TextField(verbose_name="description")
    task_group = models.ForeignKey(to=TaskGroup, on_delete=models.SET_NULL, null=True,   verbose_name="group")
    day = models.IntegerField(verbose_name="period", default=1)

    person = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name="person", verbose_name="assign to")
    creator = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name="creator", verbose_name="creator")

    class Meta:
        app_label = "task_app"
        db_table = "tasks"
        verbose_name = "task list"
        verbose_name_plural = verbose_name




class TasksRecord(BaseModel):
    """
    任务完成记录
    """
    task = models.ForeignKey(to=Tasks, on_delete=models.DO_NOTHING, verbose_name="task", db_constraint=False)

    completed_by = models.ForeignKey(to=User, on_delete=models.PROTECT, verbose_name="submittor", related_name="completed_by")
    completed_time = models.DateTimeField( verbose_name="complete time")
    audit_by = models.ForeignKey(to=User, on_delete=models.PROTECT, null=True, blank=True, verbose_name="tl", related_name="audit_by")
    audit_time = models.DateTimeField(null=True, blank=True, verbose_name="tl ReviewTime")

    back_by = models.ForeignKey(to=User, on_delete=models.PROTECT, null=True, blank=True, verbose_name="r1.5", related_name="back_by")
    back_time = models.DateTimeField(null=True, blank=True, verbose_name="r1.5 ReviewTime")
    bz = models.TextField(null=True, blank=True, verbose_name="remark")

    class Meta:
        app_label = "task_app"
        db_table = "tasks_record"
        verbose_name = "task records list"
        verbose_name_plural = verbose_name




class TasksLog(BaseModel):
    action = models.CharField(max_length=100, verbose_name="action")
    task_group = models.ForeignKey(to=TaskGroup, on_delete=models.SET_NULL, null=True, verbose_name="group")
    person = models.ForeignKey(to=User, on_delete=models.PROTECT,  verbose_name="operator")
    content = models.TextField(verbose_name="operation content")
    task_desc = models.TextField(verbose_name="description")

    class Meta:
        app_label = "task_app"
        db_table = "tasks_log"
        verbose_name = "tasks log"
        verbose_name_plural = verbose_name
