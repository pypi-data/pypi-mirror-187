# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nonebot_plugin_molar_mass']

package_data = \
{'': ['*']}

install_requires = \
['nonebot2[fastapi]>=2.0.0rc3,<3.0.0', 'rply>=0.7.8,<0.8.0']

setup_kwargs = {
    'name': 'nonebot-plugin-molar-mass',
    'version': '0.1.0',
    'description': 'A tool to calculate molar mass for middle school students.',
    'long_description': '# nonebot-plugin-molar-mass\n\n本项目为 `Nonebot2` 插件，用来计算摩尔质量或相对分子质量。\n\n因为我每次遇到计算题都要去翻课本，然后按计算器，不胜其烦，导致了这个库的出现。\n\n如果想要使用 `CLI` 版本，可以切换到 `cli` 分支，其实本项目原本就是一个 `CLI` 后面改成的 `Nonebot2` 插件。\n\n# 安装\n\n使用 `pip` 安装：\n\n```bash\n> pip install nonebot-plugin-molar-mass\n```\n\n# 使用\n\n发送 `/摩尔质量 化学式` 或者 `/相对分子质量 化学式`，以下为几组输入输出的例子：\n\n```\n> NaOH\n40\n> H2SO4\n98\n> 2HCl\n73\n> (NH4)2SO4\n132\n> CuSO4+5H2O\n250\n```\n\n注意，这里的斜杠指的是 `COMMAND_START`，你可以参考 Nonebot 官方文档配置这个选项。\n',
    'author': 'kifuan',
    'author_email': 'kifuan@foxmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
