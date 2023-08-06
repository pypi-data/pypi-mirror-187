# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['lonedruid']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['int_to_eso = stufftoeso.eso:int_to_eso',
                     'multieso = stufftoeso.eso:multieso',
                     'power_find = stufftoeso.eso:power_find']}

setup_kwargs = {
    'name': 'lonedruid',
    'version': '0.1.0',
    'description': '',
    'long_description': '',
    'author': 'NikitaNightBot',
    'author_email': 'enikita332@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
