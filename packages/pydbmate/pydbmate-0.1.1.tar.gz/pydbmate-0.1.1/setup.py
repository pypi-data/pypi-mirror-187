# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pydbmate']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pydbmate',
    'version': '0.1.1',
    'description': '',
    'long_description': '# Pydbmate\n> Another Python migration tool\n\n[![Build Status](https://travis-ci.org/hmleal/pydbmate.svg?branch=master)](https://travis-ci.org/hmleal/pydbmate)\n\n\nThis project is inspired by ```dbmate```',
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
