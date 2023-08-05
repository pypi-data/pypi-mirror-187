# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cimlab',
 'cimlab.data_profile.cimext_2022',
 'cimlab.data_profile.rc4_2021',
 'cimlab.loaders',
 'cimlab.loaders.blazegraph',
 'cimlab.loaders.gridappsd',
 'cimlab.loaders.sparql.rc4_2021',
 'cimlab.models']

package_data = \
{'': ['*']}

install_requires = \
['SPARQLWrapper>=2.0.0,<3.0.0', 'xsdata>=22.5,<23.0']

extras_require = \
{'gridappsd': ['gridappsd-python>=2.2.2,<3.0.0']}

setup_kwargs = {
    'name': 'gridappsd-cim-profile',
    'version': '0.7.20230120212740a0',
    'description': 'CIM models used within gridappsd.',
    'long_description': 'None',
    'author': 'C. Allwardt',
    'author_email': '3979063+craig8@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7.9,<4.0',
}


setup(**setup_kwargs)
