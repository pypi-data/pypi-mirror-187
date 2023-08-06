# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['syscord']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'syscord',
    'version': '0.1.0',
    'description': 'the simple python discord system api',
    'long_description': '',
    'author': 'Andrew',
    'author_email': 'contact@andrew.us',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
