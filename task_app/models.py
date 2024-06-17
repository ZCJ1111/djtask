from django.db import models

from user_app.models import User, TaskGroup
from utils.base_model import BaseModel


# Create your models here.


class Tasks(BaseModel):
    task_time_start = models.TimeField(verbose_name="任务开始时间")
    task_time_end = models.TimeField(verbose_name="任务截止时间")
    task_title = models.CharField(max_length=200, verbose_name="任务名称")
    task_desc = models.TextField(verbose_name="任务详情")
    task_group = models.ForeignKey(to=TaskGroup, on_delete=models.SET_NULL, null=True,   verbose_name="所属任务组")
    day = models.IntegerField(verbose_name="间隔天数", default=1)

    person = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name="person", verbose_name="所属人")
    creator = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name="creator", verbose_name="创建人")

    class Meta:
        app_label = "task_app"
        db_table = "tasks"
        verbose_name = "任务列表"
        verbose_name_plural = verbose_name




class TasksRecord(BaseModel):
    """
    任务完成记录
    """
    task = models.ForeignKey(to=Tasks, on_delete=models.DO_NOTHING, verbose_name="任务", db_constraint=False)

    completed_by = models.ForeignKey(to=User, on_delete=models.PROTECT, verbose_name="完成人", related_name="completed_by")
    completed_time = models.DateTimeField( verbose_name="完成时间")
    audit_by = models.ForeignKey(to=User, on_delete=models.PROTECT, null=True, blank=True, verbose_name="审核人", related_name="audit_by")
    audit_time = models.DateTimeField(null=True, blank=True, verbose_name="审核时间")

    back_by = models.ForeignKey(to=User, on_delete=models.PROTECT, null=True, blank=True, verbose_name="审核人", related_name="back_by")
    back_time = models.DateTimeField(null=True, blank=True, verbose_name="审核时间")
    bz = models.TextField(null=True, blank=True, verbose_name="补交备注")

    class Meta:
        app_label = "task_app"
        db_table = "tasks_record"
        verbose_name = "任务完成列表"
        verbose_name_plural = verbose_name




class TasksLog(BaseModel):
    action = models.CharField(max_length=100, verbose_name="行为")
    task_group = models.ForeignKey(to=TaskGroup, on_delete=models.SET_NULL, null=True, verbose_name="所属任务组")
    person = models.ForeignKey(to=User, on_delete=models.PROTECT,  verbose_name="操作人")
    content = models.TextField(verbose_name="操作内容")
    task_desc = models.TextField(verbose_name="任务详情")

    class Meta:
        app_label = "task_app"
        db_table = "tasks_log"
        verbose_name = "任务日志"
        verbose_name_plural = verbose_name
