# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydbmate']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pydbmate',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Henrique Leal',
    'author_email': 'hm.leal@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
