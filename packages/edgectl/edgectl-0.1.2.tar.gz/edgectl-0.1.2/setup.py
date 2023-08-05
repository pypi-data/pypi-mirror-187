# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['edgectl']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.28.2,<3.0.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['edgectl = edgectl.main:app']}

setup_kwargs = {
    'name': 'edgectl',
    'version': '0.1.2',
    'description': '',
    'long_description': '# edgectl\n\nControl edge devices through this utility\n\n',
    'author': 'Harsh Murari',
    'author_email': 'hmurari@visionify.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
