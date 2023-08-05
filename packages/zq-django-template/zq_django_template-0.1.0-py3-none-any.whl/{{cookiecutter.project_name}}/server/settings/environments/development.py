"""
This file contains all the settings that defines the development server.

SECURITY WARNING: don't run with debug turned on in production!
"""

from loguru import logger
import socket

from server.settings.components.common import INSTALLED_APPS, MIDDLEWARE
from server.settings.components.drf import REST_FRAMEWORK

# Setting the development status:

DEBUG = True

SERVER_URL = "https://"

ALLOWED_HOSTS = ["*"]

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1:8000",
    "http://localhost:8000",
]

CSRF_TRUSTED_ORIGINS += [SERVER_URL]

# Installed apps for development only:

INSTALLED_APPS += [
    # Better debug:
    "debug_toolbar",
    "nplusone.ext.django",

    # Linting migrations:
    "django_migration_linter",

    # django-extra-checks:
    'extra_checks',
]


# Django debug toolbar:
# https://django-debug-toolbar.readthedocs.io

MIDDLEWARE += [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    # https://github.com/bradmontgomery/django-querycount
    # Prints how many queries were executed, useful for the APIs.
    "querycount.middleware.QueryCountMiddleware",
]

# https://django-debug-toolbar.readthedocs.io/en/stable/installation.html#configure-internal-ips
try:  # This might fail on some OS
    INTERNAL_IPS = [
        "{0}.1".format(ip[: ip.rfind(".")])
        for ip in socket.gethostbyname_ex(socket.gethostname())[2]
    ]
except socket.error:  # pragma: no cover
    INTERNAL_IPS = []
INTERNAL_IPS += ["127.0.0.1"]


def _custom_show_toolbar(request):
    """Only show the debug toolbar when in the debug mode"""
    return DEBUG


DEBUG_TOOLBAR_CONFIG = {
    "SHOW_TOOLBAR_CALLBACK": "server.settings.environments.development._custom_show_toolbar",
}


# nplusone
# https://github.com/jmcarp/nplusone

# Should be the first in line:
MIDDLEWARE = [  # noqa: WPS440
    "nplusone.ext.django.NPlusOneMiddleware",
] + MIDDLEWARE

# Logging N+1 requests:
NPLUSONE_RAISE = False  # comment out if you want to allow N+1 requests
NPLUSONE_LOGGER = logger
NPLUSONE_LOG_LEVEL = logger.level("INFO")
NPLUSONE_WHITELIST = [
    {"model": "admin.*"},
]


# django-test-migrations
# https://github.com/wemake-services/django-test-migrations

# Set of badly named migrations to ignore:
DTM_IGNORED_MIGRATIONS = frozenset((("axes", "*"),))


# django-extra-checks
# https://github.com/kalekseev/django-extra-checks

EXTRA_CHECKS = {
    "checks": [
        # 所有模型字段需要verbose_name解释:
        "field-verbose-name",
        # Forbid `unique_together`:
        "no-unique-together",
        # Require non empty `upload_to` argument:
        "field-file-upload-to",
        # Use the indexes option instead:
        "no-index-together",
        # Each model must be registered in admin:
        "model-admin",
        # FileField/ImageField must have non-empty `upload_to` argument:
        "field-file-upload-to",
        # Text fields shouldn't use `null=True`:
        "field-text-null",
        # Don't pass `null=False` to model fields (this is django default)
        "field-null",
        # ForeignKey fields must specify db_index explicitly if used in
        # other indexes:
        {"id": "field-foreign-key-db-index", "when": "indexes"},
        # If field nullable `(null=True)`,
        # then default=None argument is redundant and should be removed:
        "field-default-null",
        # Fields with choices must have companion CheckConstraint
        # to enforce choices on database level
        "field-choices-constraint",
        # Related fields must specify related_name explicitly:
        "field-related-name",
    ],
}

# DRF Browsable API Login
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = REST_FRAMEWORK.get(
    "DEFAULT_RENDERER_CLASSES", []
) + [
    "rest_framework.renderers.BrowsableAPIRenderer"
]

REST_FRAMEWORK["DEFAULT_AUTHENTICATION_CLASSES"] = REST_FRAMEWORK.get(
    "DEFAULT_AUTHENTICATION_CLASSES", []
) + [
    "rest_framework.authentication.SessionAuthentication",
]
