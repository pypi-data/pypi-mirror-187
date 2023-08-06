# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['bagitfs']
install_requires = \
['bagit==1.8.1', 'fs>=2.2.1,<3.0.0']

setup_kwargs = {
    'name': 'bagitfs',
    'version': '0.4.0',
    'description': 'Bagit package',
    'long_description': 'None',
    'author': 'Radim Spigel',
    'author_email': 'spigel@cesnet.cz',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
