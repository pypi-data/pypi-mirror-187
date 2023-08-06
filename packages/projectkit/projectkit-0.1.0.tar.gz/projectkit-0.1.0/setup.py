# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['projectkit', 'projectkit.model', 'projectkit.utils']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1.10.4,<2.0.0', 'pyyaml>=6.0,<7.0', 'tomlkit>=0.11.6,<0.12.0']

setup_kwargs = {
    'name': 'projectkit',
    'version': '0.1.0',
    'description': '',
    'long_description': '# ProjectKit: File-based settings utility\n\nSupporting both YAML and TOML, your projects will have a user-friendly settings file.\n\n```python\nfrom projectkit.model.settings import ProjectKitSettings\n\nclass Settings(ProjectKitSettings):\n    \n```\n\n## Installation\n```shell\npip install projectkit\n```\nFor those that prefer poetry:\n```shell\npoetry add projectkit\n```\n\n## Usage\n',
    'author': 'caniko',
    'author_email': 'canhtart@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
