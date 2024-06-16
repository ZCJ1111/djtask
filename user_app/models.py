import uuid

from django.db import models

from utils.base_model import BaseModel


# Create your models here.


class Resource(BaseModel):
    """
    资源
    """
    name = models.CharField(max_length=100, verbose_name="资源名称")
    action = models.CharField(max_length=100, verbose_name="操作代号")

    class Meta:
        app_label = "user_app"
        db_table = "resource"
        verbose_name = "资源列表"


class Role(BaseModel):
    """
    角色
    """
    name = models.CharField(max_length=100, verbose_name="角色名")
    resource = models.ManyToManyField(to=Resource, verbose_name="资源")

    class Meta:
        app_label = "user_app"
        db_table = "role"
        verbose_name = "校色列表"



class TaskGroup(BaseModel):
    """
    任务组
    """
    name = models.CharField(max_length=100, verbose_name="组名称")

    class Meta:
        app_label = "task_app"
        db_table = "task_group"
        verbose_name = "任务组列表"


class User(BaseModel):
    """
    用户模型
    """
    name = models.CharField(max_length=50, unique=True, verbose_name="用户名")
    password = models.CharField(max_length=50, verbose_name="密码")
    user_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="姓名")
    task_group = models.ForeignKey(to=TaskGroup, on_delete=models.SET_NULL, null=True, verbose_name="所属任务组")
    role = models.ForeignKey(to=Role, on_delete=models.SET_NULL, null=True, verbose_name="角色")
    SA = 1  # Male
    SB = 2  # Female
    SC = 3  # 未知

    SEX = ((SA, "Male"), (SB, "Female"), (SC, "未知"))
    sex = models.IntegerField(choices=SEX, null=True, blank=True, verbose_name="性别")
    address = models.CharField(max_length=350, null=True, blank=True, verbose_name="地址")

    OA = 1  # Staff
    OC = 3  # Admin
    POWER = ((OA, "Staff"), (OC, "Admin"))
    power = models.IntegerField(choices=POWER, default=OA, verbose_name="用户类别")
    phone = models.CharField(max_length=50, null=True, blank=True, verbose_name="电话")
    token = models.CharField(max_length=50, null=True, blank=True, verbose_name="用户token")

    class Meta:
        app_label = "user_app"
        db_table = "users"
        verbose_name = "用户列表"
