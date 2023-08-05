# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['chattypy']

package_data = \
{'': ['*']}

install_requires = \
['build>=0.10.0,<0.11.0',
 'twine>=4.0.2,<5.0.0',
 'websocket-client>=1.4.2,<2.0.0']

setup_kwargs = {
    'name': 'chattypy',
    'version': '0.1.2',
    'description': 'ChattyPy is a library made in Python for making Chatty bots.',
    'long_description': None,
    'author': 'LuisAFK',
    'author_email': 'so.yl.a.fk@googlemail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8.0',
}


setup(**setup_kwargs)
