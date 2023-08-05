"""
Django settings for server project.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their config, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import datetime

from server.settings.util import BASE_DIR, config

SECRET_KEY = config("DJANGO_SECRET_KEY")

# region Application

DJANGO_APPS: list[str] = [
    "simpleui",  # admin ui（必须在第一行）
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles"
]

THIRD_PARTY_APPS: list[str] = [
    "rest_framework",  # DRF
    "corsheaders",  # CORS 跨域
    "rest_framework_simplejwt",  # JWT
    "drf_spectacular",  # api 文档
    "django_filters",  # 过滤器
    "zq_django_util.utils.oss",  # oss
    "method_override",  # 方法重写
    "drf_standardized_errors",  # drf错误初步处理
    'django_extensions',  # Django 扩展
{%- if cookiecutter.use_celery == 'y' %}
    "django_celery_results",  # celery兼容支持
    "django_celery_beat",  # celery定时任务
{%- endif %}
    'zq_django_util.logs',  # 日志记录
]

LOCAL_APPS: list[str] = [
{%- if cookiecutter.use_celery == 'y' %}
    "async_tasks",  # celery异步任务
{%- endif %}
    "users",  # 用户
    "oauth",  # 认证
    "files",  # 文件
]

INSTALLED_APPS: list[str] = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE: list[str] = [
    "corsheaders.middleware.CorsMiddleware",  # CORS 跨域(最外层)
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "method_override.middleware.MethodOverrideMiddleware",  # 请求方法修改
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "zq_django_util.logs.middleware.APILoggerMiddleware",  # 请求日志
]

ROOT_URLCONF = "server.urls"

WSGI_APPLICATION = "server.wsgi.application"
ASGI_APPLICATION = "server.asgi.application"

# endregion

# region Templates
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR.joinpath("server", "templates"),
        ],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]
# endregion

# region Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]
# endregion

# region Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_L10N = True

USE_TZ = True
# endregion

# region CORS
CORS_ORIGIN_WHITELIST = (
    "http://127.0.0.1:8000",
    "http://localhost:8000",
    "https://127.0.0.1:8000",
    "https://localhost:8000",
)

CORS_ALLOW_CREDENTIALS = True  # 允许携带cookie
# endregion

# region JWT
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(days=1),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=10),
    "ALGORITHM": "HS256",
    "AUTH_HEADER_TYPES": ("Bearer",),
    "AUTH_HEADER_NAME": "HTTP_AUTHORIZATION",
}
# endregion

# region 用户模型
AUTH_USER_MODEL = "users.User"
USER_ID_FIELD = "id"
# endregion

RUNSERVER_PLUS_EXCLUDE_PATTERNS = [
    "*\\Lib\\*",
    "*/Lib/*",
]
