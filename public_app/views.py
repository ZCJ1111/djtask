import uuid

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.request import Request

# Create your views here.

@api_view(["POST"])
def save_upload_file(request: Request):
    """
    保存上传的文件
    :return:
    """
    file = request.FILES.get("file")
    file_path = f"/static/update/{uuid.uuid4()}.{str(file.name).rsplit(',', 1)[-1]}"
    f = open("." + file_path, 'wb')
    for chunk in file.chunks():
        f.write(chunk)

    return Response({"code": 20000, "data": file_path})
