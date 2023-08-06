# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cli_openai', 'cli_openai.commands', 'cli_openai.core']

package_data = \
{'': ['*']}

install_requires = \
['volunor==1.0.0rc3']

entry_points = \
{'console_scripts': ['openai = cli_openai.cli:entry_point']}

setup_kwargs = {
    'name': 'cli-openai',
    'version': '1.0.0',
    'description': 'CHANGE_ME',
    'long_description': '# openai-cli\n\n',
    'author': 'John Doe',
    'author_email': 'contact@john.dev',
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
