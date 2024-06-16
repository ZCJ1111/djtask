import datetime

from django.db.models.expressions import RawSQL
from django.db.models.functions import Now, Cast
from django.shortcuts import render
from rest_framework.decorators import api_view, authentication_classes
from rest_framework.request import Request
from rest_framework.response import Response
from django.db.models import F, ExpressionWrapper, fields, IntegerField
from task_app.models import Tasks, TasksRecord, TasksLog
from task_app.ser import TasksSer, TasksLogSer
from user_app.models import User
from utils.auth import UserAuthentication
from utils.paginator import ExPage


# Create your views here.

@api_view(["POST"])
@authentication_classes((UserAuthentication,), )
def add_task(request: Request):
    """
    添加任务
    """
    pk = request.data.get("id")
    tks = Tasks.objects.filter(pk=pk).first()
    data = request.data
    data["creator"] = request.user.pk
    edit = False
    if not tks:
        ser = TasksSer(data=data)
    else:
        ser = TasksSer(instance=tks, data=data)
        edit = True

    if not ser.is_valid():
        return Response({"code": 0, "message": ser.errors})
    tk = ser.save()

    if edit:
        # 插入编辑日志
        content = f"{tk.creator.name} Edit {tk.task_title} task, assigns to {tk.person.name}"

        TasksLog(action="Edit", task_group=tk.task_group, person=request.user, content=content,
                 task_desc=tk.task_desc).save()
    else:
        content = f"{tk.creator.name} Add {tk.task_title} task, assigns to {tk.person.name}"
        TasksLog(action="Add", task_group=tk.task_group, person=request.user, content=content,
                 task_desc=tk.task_desc).save()

    return Response({"code": 20000, "message": "Add Successfully"})


@api_view(["GET"])
@authentication_classes((UserAuthentication,), )
def get_task_list(request: Request):
    """
    获取任务列表
    """
    user: User = request.user
    name = request.query_params.get("name")
    limit = int(request.query_params.get("limit", 10))
    page = int(request.query_params.get("page", 1))
    kw = {}
    if name:
        kw["name__contains"] = name
    if user.power == User.OA:
        # Staff
        kw["task_group"] = user.task_group
    # 获取当前日期减去创建日期的天数
    date_diff : ExpressionWrapper = ExpressionWrapper(Cast(datetime.date.today() - F('created_at__date'), output_field=fields.IntegerField())/(1000*1000)/(60*60*24), output_field=fields.IntegerField())
    # 计算天数的模2
    mod_result = ExpressionWrapper(date_diff % F("day") , output_field=fields.IntegerField())
    # mod_result=mod_result  .filter(mod_result=0) mod_result=mod_result
    u = Tasks.objects.filter(**kw).annotate(mod_result=mod_result, date_diff=date_diff).filter(mod_result=0).order_by("-pk")


    pg = ExPage(data=u, limit=limit)
    count = pg.get_count()
    staff_objs = pg.get_obj_data(page)


    ser = TasksSer(instance=staff_objs, many=True)

    return Response({"code": 20000, "data": {"count": count, "data": ser.data}})


@api_view(["POST"])
@authentication_classes((UserAuthentication,), )
def over_task(request: Request):
    """
    完成任务
    """
    pk = request.data.get("id")
    now = datetime.datetime.today()
    tk: Tasks = Tasks.objects.filter(pk=pk).first()

    if not tk:
        return Response({"code": 0, "message": "Task does not exist!"})
    tr = TasksRecord.objects.filter(task=tk, created_at__date=now.date(), completed_by=request.user)
    if tr:
        return Response({"code": 0, "message": "The task has been completed. Please do not submit it again."})
    if now.time() < tk.task_time_start or now.time() > tk.task_time_end:
        return Response({"code": 0, "message": "Please submit the task within the specified time"})
    TasksRecord(task=tk, completed_by=request.user, completed_time=now).save()

    # 插入日志
    content = f"{request.user.name} complete {tk.task_title} task"
    TasksLog(action="complete", task_group=tk.task_group, person=request.user, content=content,
             task_desc=tk.task_desc).save()

    return Response({"code": 20000, "message": "Submit Successfully"})


@api_view(["POST"])
@authentication_classes((UserAuthentication,), )
def del_task(request: Request):
    """
    del task
    """
    pk = request.data.get("id")
    tks = Tasks.objects.filter(pk=pk).first()
    if tks:
        # insert work log
        content = f"{request.user.name} delete {tks.task_title} task"
        TasksLog(action="delete", task_group=tks.task_group, person=request.user, content=content,
                 task_desc=tks.task_desc).save()
        tks.delete()

    return Response({"code": 20000, "message": "delete successuffly"})


@api_view(["POST"])
@authentication_classes((UserAuthentication,), )
def audit_task(request: Request):
    """R1.5 check
    """
    pk = request.data.get("id")
    status = request.data.get("status")
    now = datetime.datetime.now()
    tk = Tasks.objects.filter(pk=pk).first()
    if not tk:
        return Response({"code": 0, "message": "task does not exist"})
    tr = TasksRecord.objects.filter(task=tk, completed_time__date=now.date()).first()
    if not tr:
        return Response({"code": 0, "message": "task is not completed"})

    if status == 1:
        tr.audit_by = request.user
        tr.audit_time = now
        tr.save()
        
        content = f"{request.user.name} review {tk.task_title} task"
        TasksLog(action="review", task_group=tk.task_group, person=request.user, content=content,
                 task_desc=tk.task_desc).save()
    else:
        # 回溯
        tr.back_by = request.user
        tr.back_time = now
        tr.save()
        # 插入日志
        content = f"{request.user.name} r1.5 check {tk.task_title} task"
        TasksLog(action="R1.5Check", task_group=tk.task_group, person=request.user, content=content,
                 task_desc=tk.task_desc).save()
    return Response({"code": 20000, "message": "review successufully"})


@api_view(["POST"])
@authentication_classes((UserAuthentication,), )
def audit_task_bj(request: Request):
    """
    补交 审核/回溯任务
    """
    record_id = request.data.get("record_id")
    status = request.data.get("status")
    now = datetime.datetime.today()

    tr: TasksRecord = TasksRecord.objects.filter(pk=record_id).first()
    if not tr:
        return Response({"code": 0, "message": "task is not completed"})
    if status == 1:
        
        tr.audit_by = request.user
        tr.audit_time = now
        tr.save()
        
        content = f"{request.user.name} review {tr.task.task_title} task"
        TasksLog(action="resubmission review", task_group=tr.task.task_group, person=request.user, content=content,
                 task_desc=tr.task.task_desc).save()
    else:
        
        tr.back_by = request.user
        tr.back_time = now
        tr.save()
        
        content = f"{request.user.name} R1.5 Check {tr.task.task_title} task"
        TasksLog(action="resubmission check", task_group=tr.task.task_group, person=request.user, content=content,
                 task_desc=tr.task.task_desc).save()
    return Response({"code": 20000, "message": "review successfully"})


@api_view(["POST"])
@authentication_classes((UserAuthentication,), )
def over_task_bj(request: Request):
    """
    补缴完成任务
    """
    pk = request.data.get("id")
    bj_dt = request.data.get("bj_dt")
    bz = request.data.get("bz")
    now = datetime.datetime.strptime(bj_dt, "%Y-%m-%d")
    tk = Tasks.objects.filter(pk=pk).first()
    if not tk:
        return Response({"code": 0, "message": "task does not exist"})
    tr = TasksRecord.objects.filter(task=tk, created_at__date=now.date(), completed_by=request.user)
    # print("tr: ", tr, now.date(), tk)
    if tr:
        return Response({"code": 0, "message": " Please do not submit it again."})
    t = TasksRecord(task=tk, completed_by=request.user, completed_time=now, bz=bz)
    t.save()
    # 插入日志
    content = f"{request.user.name} submit {tk.task_title} task"
    TasksLog(action="resubmit completion", task_group=tk.task_group, person=request.user, content=content,
             task_desc=tk.task_desc).save()

    return Response({"code": 20000, "message": "submit successfully"})


@api_view(["GET"])
@authentication_classes((UserAuthentication,), )
def get_task_log_list(request: Request):
    """
    获取任务日志列表
    """
    user: User = request.user
    name = request.query_params.get("name")
    limit = int(request.query_params.get("limit", 10))
    page = int(request.query_params.get("page", 1))
    kw = {}
    if name:
        kw["name__contains"] = name
    if user.power == User.OA:
        # Staff
        kw["task_group"] = user.task_group
    u = TasksLog.objects.filter(**kw).order_by("-pk")
    pg = ExPage(data=u, limit=limit)
    count = pg.get_count()
    staff_objs = pg.get_obj_data(page)

    ser = TasksLogSer(instance=staff_objs, many=True)

    return Response({"code": 20000, "data": {"count": count, "data": ser.data}})


@api_view(["GET"])
@authentication_classes((UserAuthentication,), )
def get_task_record_list(request: Request):
    """
    获取任务记录
    """
    user: User = request.user
    query_date = request.query_params.getlist("query_date[]")
    limit = int(request.query_params.get("limit", 10))
    page = int(request.query_params.get("page", 1))
    kw = {}
    if not query_date:
        return Response({"code": 0, "message": "date must be selected"})
    # print(query_date)
    start_date = datetime.datetime.strptime(query_date[0], "%Y-%m-%d")
    end_date = datetime.datetime.strptime(query_date[1], "%Y-%m-%d")
    now_date = datetime.date.today()
    if end_date.date()>now_date:
        return Response({"code": 0, "message": "The deadline cannot be later than today."})

    # print(start_date)
    # print(end_date)
    # kw["created_at__gte"] = query_date[0]
    # kw["created_at__lte"] = query_date[1]
    if user.power == User.OA:
        # Staff
        kw["task_group"] = user.task_group
    u = Tasks.objects.filter(**kw).order_by("-pk")
    # pg = ExPage(data=u, limit=limit)
    # count = pg.get_count()
    # staff_objs = pg.get_obj_data(page)
    now = datetime.datetime.today()
    res_data = []
    # print((end_date - start_date).days, "*" * 50)
    for i in range((end_date - start_date).days + 1):
        record_dt = start_date + datetime.timedelta(days=i)
        # print(record_dt, "11111111111")
        for j in u:
            j: Tasks
            record_date = {"completed_by_name": "", "audit_by_name": "", "audit_time": "",
                           "back_by_name": "", "back_time": "", "completed_time": "",

                           "created_at": j.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                           "task_time_start": j.task_time_start,
                           "task_time_end": j.task_time_end,
                           "task_title": j.task_title,
                           "task_desc": j.task_desc,
                           "task_group_name": j.task_group.name if j.task_group else "",
                           "creator_name": j.creator.name if j.creator else "",
                           "person_name": j.person.name if j.person else "",
                           "record_time": record_dt.strftime("%Y-%m-%d"),
                           "task_id": j.id,
                           "record_id": "",
                           "day": j.day
                           }
            record = TasksRecord.objects.filter(task=j, completed_time__date=record_dt.date()).first()
            if record:
                record_date["completed_by_name"] = record.completed_by.name if record.completed_by else ""
                record_date["audit_by_name"] = record.audit_by.name if record.audit_by else ""
                record_date["back_by_name"] = record.back_by.name if record.back_by else ""
                # record_date["completed_by_time"] = record.created_at.strftime("%Y-%m-%d %H:%M:%S")
                record_date["audit_time"] = record.audit_time.strftime("%Y-%m-%d %H:%M:%S") if record.audit_time else ""
                record_date["back_time"] = record.back_time.strftime("%Y-%m-%d %H:%M:%S") if record.back_time else ""
                record_date["completed_time"] = record.completed_time.strftime(
                    "%Y-%m-%d %H:%M:%S") if record.completed_time else ""
                record_date["record_id"] = record.pk
                record_date["bz"] = record.bz
            # print(record_dt.date(), j.created_at.date(), j.day, (record_dt.date() - j.created_at.date()).days % j.day)
            if (record_dt.date() - j.created_at.date()).days % j.day == 0:
                res_data.append(record_date)

    return Response({"code": 20000, "data": {"data": res_data}})
