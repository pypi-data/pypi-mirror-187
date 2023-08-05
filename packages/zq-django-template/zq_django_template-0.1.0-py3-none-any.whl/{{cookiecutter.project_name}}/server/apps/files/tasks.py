from typing import Any, Dict

from zq_django_util.utils.oss.utils import split_file_name, get_random_name


def get_upload_file_info(attrs: Dict[str, Any]) -> Dict[str, Any]:
    """
    处理上传文件
    :param attrs: 待处理参数列表
    :return: 处理后参数列表
    """
    if "file" in attrs:
        attrs["name"], attrs["ext"] = split_file_name(
            attrs["name"]
        )  # 获取文件名与扩展名
        attrs["file"].name = get_random_name(attrs["file"].name)  # 文件名随机化
        attrs["size"] = attrs["file"].size  # 获取文件大小

    return attrs
