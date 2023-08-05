import re
import random
from typing import Dict, Any

from rest_framework import serializers
from rest_framework_simplejwt.serializers import PasswordField
from zq_django_util.exceptions import ApiException
{%- if cookiecutter.use_wechat == 'y' %}
from zq_django_util.utils.auth.serializers import OpenIdLoginSerializer
{%- endif %}

from oauth.utils import VerifyCodeUtil
{%- if cookiecutter.use_wechat == 'y' %}
from server.utils.wechat import get_openid
{%- endif %}


{%- if cookiecutter.use_wechat == 'y' %}
class WechatLoginSerializer(OpenIdLoginSerializer):
    """
    微信登录序列化器
    """

    code = PasswordField(label="前端获取code")  # 前端传入 code

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields.pop("openid")  # 删除 openid 字段

    def get_open_id(self, attrs: Dict[str, Any]) -> str:
        """
        重写获取 open_id 方法
        """
        return get_openid(attrs["code"])["openid"]
{%- endif %}


class SmsMsgSerializer(serializers.Serializer):
    """
    发送短信验证码序列化器
    """
    phone = serializers.CharField(max_length=11, min_length=11, label="手机号", write_only=True)
    code = serializers.IntegerField(min_value=100000, max_value=999999, label="验证码", write_only=True, required=False)
    status = serializers.CharField(max_length=2, min_length=10, label="状态", read_only=True)

    def validate_phone(self, value: str) -> str:
        """
        验证手机号
        """
        if not re.match(r"^1[3456789]\d{9}$", value):
            raise ApiException

        return value

    def create(self, validated_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        短信验证码
        """
        phone = validated_data["phone"]

        if not validated_data.get("code"):
            # 发送短信验证码
            VerifyCodeUtil.send_sms_verify_code(phone)
            return {"status": "send code"}
        else:
            # 验证短信验证码
            code = validated_data["code"]
            status = VerifyCodeUtil.verify_sms_code(phone, code)
            return {"status": "verify code " + str(status)}
