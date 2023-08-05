import sys
from pathlib import Path

from server.settings.components import *

from server.settings.util import _ENV
if _ENV == "development":
    from server.settings.environments.development import *
elif _ENV == "production":
    from server.settings.environments.production import *

from server.settings.environments.local import *

# Build paths inside the project like this: BASE_DIR.joinpath('some')
# `pathlib` is better than writing: dirname(dirname(dirname(__file__)))
BASE_DIR = Path(__file__).parent.parent.parent
# 添加导包路径
sys.path.insert(0, str(BASE_DIR.joinpath("server", "apps")))
