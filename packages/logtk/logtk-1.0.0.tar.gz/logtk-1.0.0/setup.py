# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['logtk']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'logtk',
    'version': '1.0.0',
    'description': 'logging toolkit',
    'long_description': 'None',
    'author': 'wayfaring-stranger',
    'author_email': 'zw6p226m@duck.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
