# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['multiwidth']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'multiwidth',
    'version': '1.0.0',
    'description': '',
    'long_description': 'None',
    'author': 'John Carter',
    'author_email': 'john.carter@leapyear.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
