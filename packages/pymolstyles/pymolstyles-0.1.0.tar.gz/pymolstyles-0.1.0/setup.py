# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymolstyles']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pymolstyles',
    'version': '0.1.0',
    'description': 'Utilities for small-molecules visualization using Pymol',
    'long_description': "!['ALT'](img/pymolstyles.png)\n\n",
    'author': 'Attilio Chiavegatti',
    'author_email': 'attiliochiavegatti@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
