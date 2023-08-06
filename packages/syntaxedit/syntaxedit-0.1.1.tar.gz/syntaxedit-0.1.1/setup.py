# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['syntaxedit']

package_data = \
{'': ['*']}

install_requires = \
['pygments>=2.14.0,<3.0.0', 'qtpy>=2.3.0,<3.0.0']

setup_kwargs = {
    'name': 'syntaxedit',
    'version': '0.1.1',
    'description': 'Syntax highlighting Qt text widget',
    'long_description': '# syntaxedit\n\n> A simple Python Qt syntax highlighting widget\n',
    'author': 'David Winter',
    'author_email': 'i@djw.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/davidwinter/syntaxedit',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7.2,<3.12',
}


setup(**setup_kwargs)
