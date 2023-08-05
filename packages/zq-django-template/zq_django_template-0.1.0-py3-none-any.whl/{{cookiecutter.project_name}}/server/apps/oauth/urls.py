from django.urls import path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

{%- if cookiecutter.use_wechat == 'y' %}
from .views import PasswordLoginView, OpenIdLoginView, WechatLoginView, SmsMsgView
{%- else %}
from .views import PasswordLoginView, SmsMsgView
{%- endif %}

router = routers.SimpleRouter()

router.register("sms", SmsMsgView, basename="sms")

urlpatterns = [
{%- if cookiecutter.use_wechat == 'y' %}
    path(
        "login/wechat/", WechatLoginView.as_view(), name="wechat_login"
    ),  # 微信登录
    path(
        "login/wechat/openid/", OpenIdLoginView.as_view(), name="openid_pair"
    ),  # openid登录
{%- endif %}
    path(
        "login/password/", PasswordLoginView.as_view(), name="password_login"
    ),  # 密码登录
    path(
        "login/refresh/", TokenRefreshView.as_view(), name="token_refresh"
    ),  # 刷新token
]

urlpatterns += router.urls
