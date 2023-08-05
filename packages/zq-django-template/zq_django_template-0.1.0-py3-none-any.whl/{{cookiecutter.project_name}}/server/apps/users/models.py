from django.db import models
from zq_django_util.utils.user.models import AbstractUser


class User(AbstractUser):
    """
    基本用户表
    """
    # 自定义字段
    openid = models.CharField(
        max_length=64, unique=True, verbose_name="微信openid"
    )

    class Meta:
        app_label = "users"
        db_table = "zq_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name
