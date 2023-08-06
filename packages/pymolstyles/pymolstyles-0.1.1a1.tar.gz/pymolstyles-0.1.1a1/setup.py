# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pymolstyles', 'pymolstyles.external']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pymolstyles',
    'version': '0.1.1a1',
    'description': 'Scripts for small molecule visualization using PyMOL',
    'long_description': "!['pymolstyles logo'](./docs/img/pymolstyles.png)\n\n",
    'author': 'Attilio Chiavegatti',
    'author_email': 'attiliochiavegatti@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
