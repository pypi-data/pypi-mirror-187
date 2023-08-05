# 本地模式
from server.settings import config, ZQ_EXCEPTION
from server.settings.components.configs import CacheConfig, DatabaseConfig

DEBUG = True

ALLOWED_HOSTS = ["*"]

SERVER_URL = "http://127.0.0.1:8000"

# region Database

# MySQL
# DatabaseConfig.url = "mysql://USERNAME:PASSWORD@HOST:PORT/DB"
# DATABASES = DatabaseConfig.get()

# SQLite
DATABASES = DatabaseConfig.get()
# endregion

# region Cache

# Redis
# CacheConfig.url = "redis://USERNAME:PASSWORD@HOST:PORT/"
# CACHE = CacheConfig.get()
{%- if cookiecutter.use_celery == 'y' %}
CELERY_BROKER_URL = config("CELERY_BROKER_URL", config("REDIS_URL"))
{%- endif %}
# endregion

ZQ_EXCEPTION["EXCEPTION_UNKNOWN_HANDLE"] = False
