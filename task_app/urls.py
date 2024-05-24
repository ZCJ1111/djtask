"""
URL configuration for djtask_v2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path

from task_app.views import add_task, get_task_list, over_task, del_task, audit_task, get_task_log_list, \
    get_task_record_list, audit_task_bj, over_task_bj
from user_app.views import user_reg, user_login, get_user_info, logout, get_user, save_user, get_user_list, \
    admin_reset_pwd, admin_save_user, admin_del_user, get_resource_list, admin_add_group, admin_del_group, \
    get_group_list, admin_del_cole, admin_add_role, get_role_list, get_over_group_list, get_over_user_list

urlpatterns = [
    url('add_task/$', add_task, name="add_task"),
    url('get_task_list/$', get_task_list, name="get_task_list"),
    url('over_task/$', over_task, name="over_task"),
    url('del_task/$', del_task, name="del_task"),
    url('audit_task/$', audit_task, name="audit_task"),
    url('audit_task_bj/$', audit_task_bj, name="audit_task_bj"),
    url('over_task_bj/$', over_task_bj, name="over_task_bj"),
    url('get_task_log_list/$', get_task_log_list, name="get_task_log_list"),
    url('get_task_record_list/$', get_task_record_list, name="get_task_record_list"),

]
