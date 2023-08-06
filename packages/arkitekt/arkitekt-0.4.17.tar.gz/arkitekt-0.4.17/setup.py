# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['arkitekt',
 'arkitekt.apps',
 'arkitekt.cli',
 'arkitekt.cli.dev',
 'arkitekt.cli.logic',
 'arkitekt.cli.prod',
 'arkitekt.qt']

package_data = \
{'': ['*'], 'arkitekt.qt': ['assets/dark/*', 'assets/light/*']}

install_requires = \
['fakts>=0.3.8',
 'fluss>=0.1.33',
 'herre>=0.3.6',
 'mikro>=0.3.18',
 'rekuest>=0.1.19',
 'unlok>=0.1.5']

entry_points = \
{'console_scripts': ['arkitekt = arkitekt.cli.main:entrypoint']}

setup_kwargs = {
    'name': 'arkitekt',
    'version': '0.4.17',
    'description': 'client for the arkitekt platform',
    'long_description': 'None',
    'author': 'jhnnsrs',
    'author_email': 'jhnnsrs@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
