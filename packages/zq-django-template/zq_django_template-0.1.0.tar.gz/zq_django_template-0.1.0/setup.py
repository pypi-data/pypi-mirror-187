# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['{{cookiecutter.project_name}}',
 '{{cookiecutter.project_name}}.docker.django',
 '{{cookiecutter.project_name}}.server',
 '{{cookiecutter.project_name}}.server.apps',
 '{{cookiecutter.project_name}}.server.apps.async_tasks',
 '{{cookiecutter.project_name}}.server.apps.async_tasks.management',
 '{{cookiecutter.project_name}}.server.apps.async_tasks.management.commands',
 '{{cookiecutter.project_name}}.server.apps.async_tasks.migrations',
 '{{cookiecutter.project_name}}.server.apps.files',
 '{{cookiecutter.project_name}}.server.apps.files.migrations',
 '{{cookiecutter.project_name}}.server.apps.oauth',
 '{{cookiecutter.project_name}}.server.apps.oauth.migrations',
 '{{cookiecutter.project_name}}.server.apps.users',
 '{{cookiecutter.project_name}}.server.apps.users.migrations',
 '{{cookiecutter.project_name}}.server.settings',
 '{{cookiecutter.project_name}}.server.settings.components',
 '{{cookiecutter.project_name}}.server.settings.environments',
 '{{cookiecutter.project_name}}.server.utils']

package_data = \
{'': ['*'],
 '{{cookiecutter.project_name}}': ['.github/workflows/*',
                                   '.idea/*',
                                   '.idea/runConfigurations/*',
                                   'config/*',
                                   'docker/*',
                                   'docker/caddy/*',
                                   'docker/caddy/static/*',
                                   'docker/django/celery/beat/*',
                                   'docker/django/celery/flower/*',
                                   'docker/django/celery/worker/*'],
 '{{cookiecutter.project_name}}.server': ['templates/*']}

modules = \
['cookiecutter']
install_requires = \
['auto-changelog>=0.6.0,<0.7.0',
 'black>=22.12.0,<23.0.0',
 'cookiecutter>=2.1.1,<3.0.0',
 'flake8-pyproject>=1.2.2,<2.0.0',
 'flake8>=6.0.0,<7.0.0',
 'isort>=5.11.4,<6.0.0',
 'mkdocs>=1.4.2,<2.0.0',
 'mkdocstrings[python]>=0.19.1,<0.20.0',
 'pre-commit>=2.21.0,<3.0.0']

setup_kwargs = {
    'name': 'zq-django-template',
    'version': '0.1.0',
    'description': '自强 Studio Django 模板',
    'long_description': '<div align="center">\n\n# zq-django-template\n**自强 Studio Django 模板**\n\n<!-- markdownlint-disable-next-line MD036 -->\n</div>\n\n<p align="center">\n  <a href="https://zq-django-util.readthedocs.io/en/latest/?badge=latest">\n    <img src="https://readthedocs.org/projects/zq-django-template/badge/?version=latest" alt="Documentation Status" >\n  </a>\n  <a href="https://pypi.org/project/zq-django-template/">\n    <img src="https://img.shields.io/pypi/v/zq-django-template" alt="pypi">\n  </a>\n</p>\n<!-- markdownlint-enable MD033 -->\n\n[English Version](README_EN.md)\n\n## 简介\n\nzq-django-util 是自强 Studio 开发的 Django 模板，用于快速搭建 Django+DRF 项目。其中包括：\n\n- 使用 [zq-django-util](https://pypi.org/project/zq-django-util/) 工具搭建的基础框架\n- JWT 认证\n- OSS 存储、直传示例\n- 微信小程序登录示例（可选）\n- Sentry 监控（可选）\n- Celery 异步任务（可选）\n- git 提交规范与代码检查\n- Docker 配置与自动化部署\n\n## 使用说明\n\n详见 [使用说明文档](docs/usage.md)\n\n## 开发\n\n使用 poetry 安装依赖，并进行项目修改\n',
    'author': 'Nagico',
    'author_email': 'yjr888@vip.qq.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Nagico/zq-django-template',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8.1,<4.0',
}


setup(**setup_kwargs)
