# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['usermgr']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'usermgr',
    'version': '0.0.1',
    'description': '',
    'long_description': '# User Management API\n\n## Memo\n\n* unittest\n\n```\npoetry run python -m unittest discover\n```\n\n* build\n\n```\npoetry build\n```\n\n* public\n\n```\npoetry publish\n```\n',
    'author': 'tamuto',
    'author_email': 'tamuto@infodb.jp',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/tamuto/usermgr',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
