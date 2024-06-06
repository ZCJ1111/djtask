# coding: utf-8
from rest_framework import serializers

from user_app.models import User, Resource, TaskGroup, Role


class RegUserSer(serializers.ModelSerializer):
    name = serializers.CharField(min_length=5, max_length=15, required=True)
    password = serializers.CharField(min_length=6, max_length=15, required=True)

    class Meta:
        model = User
        fields = "__all__"

class GetUserSer(serializers.ModelSerializer):
    role_name = serializers.CharField(source="role.name", default="")
    sex_name = serializers.CharField(source="get_sex_display", default="")
    power_name = serializers.CharField(source="get_power_display", default="")
    task_group_name = serializers.CharField(source="task_group.name", default="", read_only=True)
    class Meta:
        model = User
        fields = "__all__"
class UserSer(serializers.ModelSerializer):
    power_name = serializers.CharField(source="get_power_display", default="")
    class Meta:
        model = User
        fields = "__all__"


class ResourceSer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = "__all__"


class TaskGroupSer(serializers.ModelSerializer):
    class Meta:
        model = TaskGroup
        fields = "__all__"


class RoleSer(serializers.ModelSerializer):
    resource_name = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Role
        fields = "__all__"

    def get_resource_name(self, obj: Role):
        msg = ""
        if obj.resource:
            for i in obj.resource.all():
                msg += f"{i.name} | "
        return msg
