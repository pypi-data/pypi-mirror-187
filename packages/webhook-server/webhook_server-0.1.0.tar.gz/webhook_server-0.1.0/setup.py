# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['webhook_server']

package_data = \
{'': ['*']}

install_requires = \
['Flask-BasicAuth>=0.2.0,<0.3.0',
 'Flask-HTTPAuth>=4.7.0,<5.0.0',
 'Flask>=2.2.2,<3.0.0']

setup_kwargs = {
    'name': 'webhook-server',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'daisukixci',
    'author_email': 'daisuki@tuxtrooper.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
