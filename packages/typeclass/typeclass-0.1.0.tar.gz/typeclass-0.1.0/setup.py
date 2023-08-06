# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['typeclass']

package_data = \
{'': ['*']}

install_requires = \
['extype>=0.1.0,<0.2.0']

setup_kwargs = {
    'name': 'typeclass',
    'version': '0.1.0',
    'description': 'A small Python package that adds typeclasses',
    'long_description': None,
    'author': 'Binyamin Y Cohen',
    'author_email': 'binyamincohen555@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
