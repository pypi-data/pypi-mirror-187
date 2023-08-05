from server.settings.components.caches import *
{%- if cookiecutter.use_celery == 'y' %}
from server.settings.components.celery import *
{%- endif %}
from server.settings.components.common import *
from server.settings.components.configs import *
from server.settings.components.databases import *
from server.settings.components.django_utils import *
from server.settings.components.drf import *
from server.settings.components.logging import *
{%- if cookiecutter.use_sentry == 'y' %}
from server.settings.components.sentry import *
{%- endif %}
from server.settings.components.server_url import *
from server.settings.components.simpleui import *
from server.settings.components.storage import *
{%- if cookiecutter.use_wechat == 'y' %}
from server.settings.components.wechat import *
{%- endif %}
