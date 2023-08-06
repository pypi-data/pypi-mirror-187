# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dvml', 'dvml.models']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.1,<2.0.0']

setup_kwargs = {
    'name': 'dvml',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'Daniel Viegas',
    'author_email': 'viegasdll@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
