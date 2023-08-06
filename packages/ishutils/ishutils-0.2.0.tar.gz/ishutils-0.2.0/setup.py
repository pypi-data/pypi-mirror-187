# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ishutils', 'ishutils.common', 'ishutils.ubuntu', 'ishutils.utils']

package_data = \
{'': ['*']}

install_requires = \
['httpie>=3.2.1,<4.0.0', 'questionary>=1.10.0,<2.0.0', 'rich>=13.2.0,<14.0.0']

setup_kwargs = {
    'name': 'ishutils',
    'version': '0.2.0',
    'description': 'My Shell Utils',
    'long_description': '# ishutils\n\nMy Shell Utils\n',
    'author': 'Qin Li',
    'author_email': 'liblaf@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://liblaf.github.io/ishutils/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
