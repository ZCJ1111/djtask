import random
import time
import uuid

import qrcode
from django.db import IntegrityError
from django.db.models import ProtectedError
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.request import Request
from rest_framework.response import Response

from user_app.models import User, Resource, TaskGroup, Role
from user_app.ser import RegUserSer, GetUserSer, ResourceSer, TaskGroupSer, RoleSer
from utils.auth import UserAuthentication
from utils.paginator import ExPage


# Create your views here.

def make_qrcode(data):
    # 生成二维码
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill='black', back_color='white')
    img.save(f"./static/qrc/{data}.png")


@api_view(["POST"])
def user_reg(request: Request):
    """
    注册
    """

    ser = RegUserSer(data=request.data)
    if not ser.is_valid():
        return Response({"code": 0, "message": ser.errors})
    try:
        u = ser.save()
        u.student_id = int(time.time() * 100)
        u.save()
        make_qrcode(u.student_id)

        return Response({"code": 20000, "message": "注册成功"})
    except Exception as e:
        return Response({"code": 0, "message": "用户已存在"})


@api_view(["POST"])
def user_login(request: Request):
    """
    登录
    """
    username = request.data.get("username")
    password = request.data.get("password")
    u = User.objects.filter(name=username, password=password).first()
    if not u:
        return Response({"code": 0, "message": "账号密码错误"})
    token = uuid.uuid4()
    u.token = token
    u.save()

    return Response({"code": 20000, "data": {"token": token}})


@api_view(["GET"])
def get_user_info(request: Request):
    """
    获取用户信息
    """
    token = request.query_params.get("token")
    u = User.objects.filter(token=token).first()
    roles = ["user"]
    power = "用户端"
    resource = {}
    if u.power == User.OA:
        roles = ["user"]
        power = "用户端"
        if u.role and u.role.resource:
            for i in u.role.resource.all():
                resource[i.action] = True

    elif u.power == User.OC:
        roles = ["admin"]
        power = "管理端"
        for i in Resource.objects.all():
            resource[i.action] = True

    image = "/static/image/user.png"
    return Response({"code": 20000, "data": {"roles": roles, "introduction": power,
                                             "avatar": 'http://127.0.0.1:8000' + image,
                                             "name": u.name,
                                             "power": power,
                                             "resource": resource
                                             }})


@api_view(["GET"])
@authentication_classes((UserAuthentication,), )
def get_user(request: Request):
    """
    获取用户信息
    """
    ser = GetUserSer(instance=request.user)

    return Response({"code": 20000, "data": ser.data})


@api_view(["GET"])
@authentication_classes((UserAuthentication,), )
def get_user_list(request: Request):
    """
    获取用户列表
    """
    name = request.query_params.get("name")
    limit = int(request.query_params.get("limit", 10))
    page = int(request.query_params.get("page", 1))
    kw = {}
    if name:
        kw["name__contains"] = name
    u = User.objects.filter(**kw).order_by("-pk")
    pg = ExPage(data=u, limit=limit)
    count = pg.get_count()
    staff_objs = pg.get_obj_data(page)

    ser = GetUserSer(instance=staff_objs, many=True)

    return Response({"code": 20000, "data": {"count": count, "data": ser.data}})

@api_view(["GET"])
@authentication_classes((UserAuthentication,), )
def get_over_user_list(request: Request):
    """
    获取特定用户列表
    """
    task_group_id = request.query_params.get("task_group_id")

    u = User.objects.filter(task_group_id=task_group_id).order_by("-pk")
    ser = GetUserSer(instance=u, many=True)

    return Response({"code": 20000, "data": ser.data})


@api_view(["POST"])
@authentication_classes((UserAuthentication,), )
def admin_reset_pwd(request: Request):
    """
    重置密码
    """
    ...
    pk = request.data.get("pk")
    u = User.objects.filter(pk=pk).first()
    pwd = random.randrange(111111, 999999)
    u.password = pwd
    u.save()
    return Response({"code": 20000, "data": pwd})


@api_view(["POST"])
@authentication_classes((UserAuthentication,), )
def save_user(request: Request):
    """
    保存用户信息
    """

    ser = RegUserSer(instance=request.user, data=request.data)
    if not ser.is_valid():
        return Response({"code": 0, "message": ser.errors})
    ser.save()

    return Response({"code": 20000, "message": "保存成功"})


@api_view(["POST"])
@authentication_classes((UserAuthentication,), )
def admin_save_user(request: Request):
    """
    保存用户信息
    """
    pk = request.data.get("id")
    user = User.objects.filter(pk=pk).first()
    ser = RegUserSer(instance=user, data=request.data)
    if not ser.is_valid():
        return Response({"code": 0, "message": ser.errors})
    try:
        ser.save()
    except IntegrityError as e:
        return Response({"code": 0, "message": "用户名已存在"})

    return Response({"code": 20000, "message": "保存成功"})


@api_view(["POST"])
@authentication_classes((UserAuthentication,), )
def admin_del_user(request: Request):
    """
    删除用户信息
    """
    pk = request.data.get("id")
    try:
        User.objects.filter(pk=pk).delete()
    except ProtectedError as e:
        return Response({"code": 0, "message": "用户以关联数据不能删除"})

    return Response({"code": 20000, "message": "删除成功"})


@api_view(["POST"])
def logout(request: Request):
    return Response({"code": 20000, "data": "success"})


@api_view(["GET"])
@authentication_classes((UserAuthentication,), )
def get_resource_list(request: Request):
    """
    获取资源列表
    """

    u = Resource.objects.filter().order_by("-pk")

    ser = ResourceSer(instance=u, many=True)

    return Response({"code": 20000, "data": ser.data})



@api_view(["GET"])
@authentication_classes((UserAuthentication,), )
def get_group_list(request: Request):
    """
    获取组列表
    """

    name = request.query_params.get("name")
    limit = int(request.query_params.get("limit", 10))
    page = int(request.query_params.get("page", 1))
    kw = {}
    if name:
        kw["name__contains"] = name
    u = TaskGroup.objects.filter(**kw).order_by("-pk")
    pg = ExPage(data=u, limit=limit)
    count = pg.get_count()
    staff_objs = pg.get_obj_data(page)

    ser = TaskGroupSer(instance=staff_objs, many=True)

    return Response({"code": 20000, "data": {"count": count, "data": ser.data}})



@api_view(["GET"])
@authentication_classes((UserAuthentication,), )
def get_over_group_list(request: Request):
    """
    获取特定组列表
    """
    user : User = request.user
    if user.power == User.OC:
        # 超级用户
        group = TaskGroup.objects.filter().order_by("-pk")
        ser = TaskGroupSer(instance=group, many=True)
        data = ser.data
    else:
        ser = TaskGroupSer(instance=user.task_group)
        data = [ser.data]

    return Response({"code": 20000, "data": data})


@api_view(["POST"])
@authentication_classes((UserAuthentication,), )
def admin_add_group(request: Request):
    """
    添加组
    """
    pk = request.data.get("id")
    if pk:
        group = TaskGroup.objects.filter(pk=pk).first()
        ser = TaskGroupSer(instance=group, data=request.data)
    else:
        ser = TaskGroupSer(data=request.data)
    if not ser.is_valid():
        return Response({"code": 0, "message": ser.errors})
    ser.save()
    return Response({"code": 20000, "message": "保存成功"})


@api_view(["POST"])
@authentication_classes((UserAuthentication,), )
def admin_del_group(request: Request):
    """
    删除组
    """
    pk = request.data.get("id")
    group = TaskGroup.objects.filter(pk=pk).first()
    group.delete()
    return Response({"code": 20000, "message": "删除成功"})





@api_view(["GET"])
@authentication_classes((UserAuthentication,), )
def get_role_list(request: Request):
    """
    获角色列表
    """

    name = request.query_params.get("name")
    limit = int(request.query_params.get("limit", 10))
    page = int(request.query_params.get("page", 1))
    kw = {}
    if name:
        kw["name__contains"] = name
    u = Role.objects.filter(**kw).order_by("-pk")
    pg = ExPage(data=u, limit=limit)
    count = pg.get_count()
    staff_objs = pg.get_obj_data(page)

    ser = RoleSer(instance=staff_objs, many=True)

    return Response({"code": 20000, "data": {"count": count, "data": ser.data}})


@api_view(["POST"])
@authentication_classes((UserAuthentication,), )
def admin_add_role(request: Request):
    """
    添加角色
    """
    pk = request.data.get("id")
    if pk:
        group = Role.objects.filter(pk=pk).first()
        ser = RoleSer(instance=group, data=request.data)
    else:
        ser = RoleSer(data=request.data)
    if not ser.is_valid():
        return Response({"code": 0, "message": ser.errors})
    ser.save()
    return Response({"code": 20000, "message": "保存成功"})


@api_view(["POST"])
@authentication_classes((UserAuthentication,), )
def admin_del_cole(request: Request):
    """
    删除角色
    """
    pk = request.data.get("id")
    group = Role.objects.filter(pk=pk).first()
    group.delete()
    return Response({"code": 20000, "message": "删除成功"})

