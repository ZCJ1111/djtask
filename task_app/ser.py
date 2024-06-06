# coding: utf-8
import datetime

from rest_framework import serializers

from task_app.models import Tasks, TasksRecord, TasksLog
from user_app.models import User, Resource, TaskGroup, Role


class TasksSer(serializers.ModelSerializer):
    task_group_name = serializers.CharField(source="task_group.name", default="")
    person_name = serializers.CharField(source="person.name", default="")
    creator_name = serializers.CharField(source="creator.name", default="")
    status = serializers.SerializerMethodField(read_only=True)
    over_time = serializers.SerializerMethodField(read_only=True)
    over_person = serializers.SerializerMethodField(read_only=True)
    audit_person = serializers.SerializerMethodField(read_only=True)
    audit_tm = serializers.SerializerMethodField(read_only=True)
    back_person = serializers.SerializerMethodField(read_only=True)
    back_tm = serializers.SerializerMethodField(read_only=True)
    completed_tm = serializers.SerializerMethodField(read_only=True)
    date_diff = serializers.CharField(read_only=True)
    mod_result = serializers.CharField(read_only=True)

    class Meta:
        model = Tasks
        fields = "__all__"

    def get_back_tm(self, obj: Tasks):
        now = datetime.datetime.today()

        tr = TasksRecord.objects.filter(task=obj, completed_time__date=now.date()).first()
        if not tr:
            return ""
        if tr.back_time:
            return tr.back_time.strftime("%H:%M:%S")
        return ""

    def get_back_person(self, obj: Tasks):
        now = datetime.datetime.today()

        tr = TasksRecord.objects.filter(task=obj, completed_time__date=now.date()).first()
        if not tr:
            return ""
        if tr.back_by:
            return tr.back_by.name
        return ""

    def get_audit_tm(self, obj: Tasks):
        now = datetime.datetime.today()

        tr = TasksRecord.objects.filter(task=obj, completed_time__date=now.date()).first()
        if not tr:
            return ""
        if tr.audit_time:
            return tr.audit_time.strftime("%H:%M:%S")
        return ""

    def get_completed_tm(self, obj: Tasks):
        now = datetime.datetime.today()

        tr = TasksRecord.objects.filter(task=obj, completed_time__date=now.date()).first()
        if not tr:
            return ""
        if tr.completed_time:
            return tr.completed_time.strftime("%H:%M:%S")
        return ""

    def get_audit_person(self, obj: Tasks):
        now = datetime.datetime.today()

        tr = TasksRecord.objects.filter(task=obj, completed_time__date=now.date()).first()
        if not tr:
            return ""
        if tr.audit_by:
            return tr.audit_by.name
        return ""

    def get_over_person(self, obj: Tasks):
        now = datetime.datetime.today()

        tr = TasksRecord.objects.filter(task=obj, completed_time__date=now.date()).first()
        if not tr:
            return ""
        if tr.completed_by:
            return tr.completed_by.name
        return ""

    def get_status(self, obj: Tasks):
        now = datetime.datetime.today()

        tr = TasksRecord.objects.filter(task=obj, completed_time__date=now.date()).first()
        if not tr:
            return False
        return True

    def get_over_time(self, obj: Tasks):
        now = datetime.datetime.today()

        tr = TasksRecord.objects.filter(task=obj, completed_time__date=now.date()).first()
        if not tr:
            return ""
        return tr.created_at.strftime("%H:%M:%S")



class TasksLogSer(serializers.ModelSerializer):
    task_group_name = serializers.CharField(source="task_group.name", default="")
    person_name = serializers.CharField(source="person.name", default="")
    creator_name = serializers.CharField(source="creator.name", default="")


    class Meta:
        model = TasksLog
        fields = "__all__"
