# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ipfy_asset_management_database']

package_data = \
{'': ['*']}

install_requires = \
['numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.2,<2.0.0',
 'pylint>=2.15.10,<3.0.0',
 'pypiserver>=1.5.1,<2.0.0',
 'pytest>=7.2.0,<8.0.0',
 'typing==3.5']

setup_kwargs = {
    'name': 'ipfy-asset-management-database',
    'version': '0.0.3',
    'description': 'Python package to manage the ipfy asset management database',
    'long_description': '# package-python-ipfy-asset-management-database\nIPFY Asset management project database management.\n',
    'author': 'Yannick Flores',
    'author_email': 'yannick.flores1992@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
