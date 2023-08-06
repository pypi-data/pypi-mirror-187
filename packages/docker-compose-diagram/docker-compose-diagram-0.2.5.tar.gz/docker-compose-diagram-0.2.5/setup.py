# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['docker_compose_diagram',
 'docker_compose_diagram.docker_compose',
 'docker_compose_diagram.docker_images']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML>=5.3.4,<6.0.0',
 'click>=8.0.3,<9.0.0',
 'diagrams==0.23.3',
 'dockerfile-parse>=1.2.0,<2.0.0',
 'rich>=12.2.0,<13.0.0',
 'safety==2.3.5']

entry_points = \
{'console_scripts': ['compose-diagram = docker_compose_diagram:process_cli']}

setup_kwargs = {
    'name': 'docker-compose-diagram',
    'version': '0.2.5',
    'description': '',
    'long_description': None,
    'author': 'Skonik',
    'author_email': 's.konik.dev@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
