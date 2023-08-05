from server.settings.components import config
from server.settings.components.configs import CacheConfig, DatabaseConfig

# debug 模式
DEBUG = config("DJANGO_DEBUG", False, cast=bool)

ALLOWED_HOSTS = ["*"]

SERVER_URL = "https://"

# region CORS
CORS_ORIGIN_WHITELIST = [
    "http://127.0.0.1:8080",
    "http://localhost:8080",
    "https://127.0.0.1:8080",
    "https://localhost:8080",
]

CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie

# endregion

CSRF_TRUSTED_ORIGINS = [
    SERVER_URL,
]

# region Database
# MySQL
# DatabaseConfig.url = "mysql://USERNAME:PASSWORD@HOST:PORT/DB"
# DATABASES = DatabaseConfig.get_config()
# endregion

# region Cache
# Redis
CacheConfig.url = "redis://redis"
CACHES = CacheConfig.get()

{%- if cookiecutter.use_celery == 'y' %}
CELERY_BROKER_URL = "redis://redis/0"
{%- endif %}
# endregion
