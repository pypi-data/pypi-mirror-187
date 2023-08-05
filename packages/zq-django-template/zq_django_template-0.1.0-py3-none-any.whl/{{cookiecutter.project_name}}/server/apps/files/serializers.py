from files.models import File
from files.tasks import get_upload_file_info
from rest_framework import serializers


class FileSerializer(serializers.ModelSerializer):
    """
    文件序列化器
    """

    class Meta:
        model = File
        exclude = ["user"]
        read_only_fields = ["ext", "size"]

    def validate(self, attrs):
        return get_upload_file_info(attrs)


class FileCreateSerializer(serializers.ModelSerializer):
    """
    文件新增序列化器
    """

    class Meta:
        model = File
        exclude = ["user"]
        read_only_fields = ["ext", "size"]

    def validate(self, attrs):
        """
        自动添加文件名、用户
        """
        attrs["user"] = self.context["request"].user

        return get_upload_file_info(attrs)
