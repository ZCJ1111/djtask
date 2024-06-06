# coding: utf-8
"""
分页相关
"""
from django.core.paginator import Paginator


class ExPage:
    def __init__(self, data, limit=10):
        self.data = data
        self.limit = limit
        self.paginator = Paginator(data, int(self.limit))

    def get_count(self):
        """
        获取总数
        :return:
        """
        return self.paginator.count

    def get_page_data(self, values, page=1):
        """
        获取分页数据
        :return:
        """
        try:
            data = self.paginator.page(int(page))
            return data.object_list.values(*values)
        except Exception as e:
            print(e)
            return []

    def get_obj_data(self, page=1):
        """
        获取分页数据对象
        :return:
        """
        try:
            data = self.paginator.page(int(page))
            return data
        except Exception as e:
            print(e)
            return []
