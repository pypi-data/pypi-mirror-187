# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['super_cereal', 'super_cereal.cerealizer']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'super-cereal',
    'version': '0.1.0',
    'description': 'Serialize Python objects',
    'long_description': '',
    'author': 'Sean Freitag',
    'author_email': 'sean.freitag@avant.com',
    'maintainer': 'Sean Freitag',
    'maintainer_email': 'sean.freitag@avant.com',
    'url': 'https://github.com/cowboygneox/super-cereal',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
