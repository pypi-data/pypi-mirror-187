# Logging
# https://docs.djangoproject.com/en/3.2/topics/logging/
from server.settings.util import config
from server.settings.components.configs import LogConfig

# See also:
# 'Do not log' by Nikita Sobolev (@sobolevn)
# https://sobolevn.me/2020/03/do-not-log


# region DRF_LOGGER
DRF_LOGGER = {
    "DATABASE": True,
    "METHODS": config(
        "DRF_API_LOGGER_METHODS",
        "POST, PUT, PATCH, DELETE",
        cast=lambda v: [s.strip() for s in v.split(",")],
    ),
}
# endregion

# 適配loguru
LOGGING = LogConfig.get_config()
