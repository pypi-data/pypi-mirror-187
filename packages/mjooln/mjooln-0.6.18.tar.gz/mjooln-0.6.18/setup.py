# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mjooln', 'mjooln.experimental']

package_data = \
{'': ['*']}

install_requires = \
['cryptography>=39.0.0,<40.0.0',
 'python-dateutil>=2.8.2,<3.0.0',
 'pytz>=2022.7.1,<2023.0.0',
 'pyyaml>=6.0,<7.0',
 'simplejson>=3.18.1,<4.0.0']

setup_kwargs = {
    'name': 'mjooln',
    'version': '0.6.18',
    'description': '',
    'long_description': 'File handling toolbox for Microservice Developers and\nData Scientists working in Python\n\n** Documentation **\n\nhttps://mjooln.readthedocs.io/\n',
    'author': 'Vemund Halmø Aarstrand',
    'author_email': 'vemundaa@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://mjooln.readthedocs.org',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
