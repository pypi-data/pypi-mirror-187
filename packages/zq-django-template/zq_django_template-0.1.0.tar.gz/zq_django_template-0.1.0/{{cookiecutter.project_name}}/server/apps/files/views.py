import datetime

from django.conf import settings
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from zq_django_util.exceptions import ApiException
from zq_django_util.response import ResponseType
from zq_django_util.utils.oss.utils import split_file_name, get_token, check_callback_signature

from files.models import File
from files.serializers import FileCreateSerializer, FileSerializer
from users.models import User

from server.utils.choices import FileTypeChoice


class FileViewSet(ModelViewSet):
    """
    文件视图集
    """

    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # 动态设置序列化器
        if self.action == "create":
            return FileCreateSerializer
        else:
            return FileSerializer

    def get_queryset(self):
        # 获取当前用户的文件
        if self.action == "callback":
            return self.queryset
        return self.queryset.filter(user=self.request.user)

    def get_permissions(self):
        if self.action in ["callback"]:
            return [AllowAny()]
        return super(FileViewSet, self).get_permissions()

    def perform_destroy(self, instance):
        instance.file.delete()  # 删除文件
        instance.delete()

    def perform_update(self, serializer):
        if "file" in self.request.data:  # 更新文件时删除源文件
            instance = self.get_object()
            instance.file.delete()
            serializer.save()
        else:
            serializer.save()

    @action(methods=["post"], detail=False)
    def token(self, request):
        """
        获取OSS直传token
        """
        user: User = request.user
        if not user.is_authenticated:
            raise ApiException(ResponseType.NotLogin, "您尚未登录，请登录后重试")

        upload_type = request.data.get("type")
        filename = request.data.get("name")
        if not upload_type:
            raise ApiException(
                ResponseType.ParamValidationFailed,
                "请传入type参数",
                record=True
            )
        if not filename:
            raise ApiException(
                ResponseType.ParamValidationFailed,
                "请传入name参数",
                record=True
            )

        info: dict | None = None

        if upload_type in FileTypeChoice.choices:
            name, ext = split_file_name(filename)
            file = File.objects.create(user=user, name=name, ext=ext)

            callback_dict = {
                "callbackUrl": f"{settings.SERVER_URL}/api/files/{file.id}/callback/?type={upload_type}",
                "callbackBody": "file=${object}&size=${size}",
                "callbackBodyType": "application/x-www-form-urlencoded",
            }

            info = get_token(
                f"media/files/{filename}",
                callback=callback_dict,
            )
            info["file_id"] = file.id

        if info:
            return Response(info)
        else:
            raise ApiException(
                ResponseType.PermissionDenied,
                "您没有权限上传此文件",
                record=True
            )

    @action(methods=["post"], detail=True)
    def callback(self, request, pk=None):
        """
        OSS回调
        """
        if not check_callback_signature(request):
            raise ApiException(
                ResponseType.PermissionDenied,
                "OSS回调签名检验失败",
                record=True
            )

        instance = self.get_object()
        upload_type = request.GET.get("type")
        url = request.data.get("file")
        name = url.lstrip(settings.MEDIA_URL.lstrip("/"))

        if upload_type in FileTypeChoice.choices:
            instance.file.name = name
            instance.size = request.data.get("size")
            instance.type = FileTypeChoice(upload_type)
        else:
            raise ApiException(
                ResponseType.ParamValidationFailed,
                "type参数错误",
                record=True
            )

        instance.update_time = datetime.datetime.now()
        instance.save()

        return Response(FileSerializer(instance).data)
