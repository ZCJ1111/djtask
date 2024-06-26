"""
re_path configuration for djtask_v2 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a re_path to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a re_path to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a re_path to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, re_path

from user_app.views import user_reg, user_login, get_user_info, logout, get_user, save_user, get_user_list, \
    admin_reset_pwd, admin_save_user, admin_del_user, get_resource_list, admin_add_group, admin_del_group, \
    get_group_list, admin_del_cole, admin_add_role, get_role_list, get_over_group_list, get_over_user_list

urlpatterns = [
    re_path('user_reg/$', user_reg, name="user_reg"),
    re_path('user_login/$', user_login, name="user_login"),
    re_path('get_user_info/$', get_user_info, name="get_user_info"),
    re_path('logout/$', logout, name="logout"),
    re_path('get_user/$', get_user, name="get_user"),
    re_path('get_user_list/$', get_user_list, name="get_user_list"),
    re_path('get_over_user_list/$', get_over_user_list, name="get_over_user_list"),
    re_path('save_user/$', save_user, name="save_user"),
    re_path('admin_save_user/$', admin_save_user, name="admin_save_user"),
    re_path('admin_del_user/$', admin_del_user, name="admin_del_user"),

    # 资源列表
    re_path('get_resource_list/$', get_resource_list, name="get_resource_list"),

    # 组管理
    re_path('admin_add_group/$', admin_add_group, name="admin_add_group"),
    re_path('admin_del_group/$', admin_del_group, name="admin_del_group"),
    re_path('get_group_list/$', get_group_list, name="get_group_list"),
    re_path('get_over_group_list/$', get_over_group_list, name="get_over_group_list"),

    # 角色管理
    re_path('admin_add_role/$', admin_add_role, name="admin_add_role"),
    re_path('admin_del_cole/$', admin_del_cole, name="admin_del_cole"),
    re_path('get_role_list/$', get_role_list, name="get_role_list"),
]
