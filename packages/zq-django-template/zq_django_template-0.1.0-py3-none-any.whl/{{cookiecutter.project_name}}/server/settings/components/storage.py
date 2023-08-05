from server.settings.util import BASE_DIR, config

# region Static files
# https://docs.djangoproject.com/en/2.2/howto/static-files

STATIC_URL = "/static/"

STATIC_ROOT = str(BASE_DIR.joinpath("docker", "caddy", "static"))
# endregion

# region 媒体文件
MEDIA_URL = "/media/"
# endregion

# region oss
DEFAULT_FILE_STORAGE = "zq_django_util.utils.oss.backends.OssMediaStorage"

ALIYUN_OSS = {
    "ACCESS_KEY_ID": config("ALIYUN_OSS_ACCESS_KEY_ID", ""),
    "ACCESS_KEY_SECRET": config("ALIYUN_OSS_ACCESS_KEY_SECRET", ""),
    "ENDPOINT": "https://oss-cn-hangzhou.aliyuncs.com",
    "BUCKET_NAME": config("ALIYUN_OSS_BUCKET_NAME", ""),
    "URL_EXPIRE_SECOND": 60 * 60 * 24 * 30,
    "TOKEN_EXPIRE_SECOND": 60,
    "MAX_SIZE_MB": 100,
}

assert ALIYUN_OSS["ACCESS_KEY_SECRET"], "ALIYUN_OSS_ACCESS_KEY_SECRET is required"

# endregion
