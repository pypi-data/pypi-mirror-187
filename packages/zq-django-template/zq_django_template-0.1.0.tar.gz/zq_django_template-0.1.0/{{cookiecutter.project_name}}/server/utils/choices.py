# 枚举类型
from django.db import models


class FileTypeChoice(models.IntegerChoices):
    """
    文件类型
    """

    UNKNOWN = 0, "未知"
    RESUME = 1, "简历"
    WORK = 2, "作品"
    OTHER = 3, "其他"
