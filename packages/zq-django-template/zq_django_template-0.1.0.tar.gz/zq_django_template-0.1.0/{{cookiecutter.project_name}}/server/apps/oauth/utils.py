import random

from django.core.cache import cache
from loguru import logger
from zq_django_util.exceptions import ApiException
from zq_django_util.response import ResponseType
{%- if cookiecutter.use_celery == 'y' %}

from .tasks import send_sms_msg
{%- endif %}


class VerifyCodeUtil:
    VERIFY_KEY = "sms:verify_code:phone_{}"
    VERIFY_TIMEOUT = 3 * 60

    FLAG_KEY = "sms:flag:phone_{}"
    FLAG_TIMEOUT = 60

    @staticmethod
    def _generate_code() -> int:
        code = random.randint(100000, 999999)
        return code

    @classmethod
    def _get_cache_code(cls, phone: str) -> int | None:
        key = cls.VERIFY_KEY.format(phone)
        code = cache.get(key)
        return code

    @classmethod
    def _set_cache_code(cls, phone: str, code: int | None) -> None:
        key = cls.VERIFY_KEY.format(phone)
        if code is not None:
            # 记录验证码
            cache.set(key, code, cls.VERIFY_TIMEOUT)
        else:
            # 删除验证码
            cache.delete(key)

    @classmethod
    def _get_cache_flag(cls, phone: str) -> bool:
        key = cls.FLAG_KEY.format(phone)
        flag = cache.get(key)
        return flag or False

    @classmethod
    def _set_cache_flag(cls, phone: str) -> None:
        key = cls.FLAG_KEY.format(phone)
        cache.set(key, True, cls.FLAG_TIMEOUT)

    @classmethod
    def send_sms_verify_code(cls, phone: str) -> None:
        """
        发送短信验证码

        :param phone: 手机号
        """
        if cls._get_cache_flag(phone):
            raise ApiException(ResponseType.APIThrottled, msg="短信发送过于频繁，请在1分钟后重试")

        code = cls._generate_code()

{%- if cookiecutter.use_celery == 'y' %}
        send_sms_msg.delay(phone, code)
{%- else %}
        logger.info("发送短信验证码: phone={}, code={}", phone, code)
{%- endif %}

        cls._set_cache_code(phone, code)
        cls._set_cache_flag(phone)

    @classmethod
    def verify_sms_code(cls, phone: str, code: int) -> bool:
        """
        验证短信验证码

        :param phone: 手机号
        :param code: 验证码
        :return: 是否验证成功
        """
        cache_code = cls._get_cache_code(phone)
        if cache_code is None or cache_code != code:
            return False

        cls._set_cache_code(phone, None)
        return True
