# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['python_openet']

package_data = \
{'': ['*']}

install_requires = \
['arrow>=1.2.3,<2.0.0',
 'geopandas>=0.12.2,<0.13.0',
 'pandas>=1.5.3,<2.0.0',
 'requests>=2.28.2,<3.0.0']

setup_kwargs = {
    'name': 'python-openet',
    'version': '0.1.0',
    'description': '',
    'long_description': None,
    'author': 'Denver Noell',
    'author_email': 'dnoell@ppeng.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
