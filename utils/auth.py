# coding: utf-8
"""

全局登录认证，权限认证
"""
import datetime

from django.contrib.auth.models import AnonymousUser
from django.core.cache import cache
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission
from rest_framework.request import Request

from user_app.models import User


class UserAuthentication(BaseAuthentication):
    """
    登录认证
    """

    def authenticate(self, request: Request):
        '''
        认证代码编写区域
        '''

        # if request.method == 'GET':
        #     method = request.query_params.get('method')
        # else:
        #     method = request.data.get('method')
        # # 跳过认证
        # print(method)
        # if method in config.FILTER_PERMISSIONS:
        #     return "", ""

        token = request.headers.get('X-Token')

        u = User.objects.filter(token=token).first()
        if u:
            return u, u.token
        ret = {'code': 403, 'message': '用户认证失败'}
        raise exceptions.AuthenticationFailed(ret)

    def authenticate_header(self, request):
        # 验证失败时，返回的响应头WWW-Authenticate对应的值
        return False


