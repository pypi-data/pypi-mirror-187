# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['nysmix']

package_data = \
{'': ['*']}

install_requires = \
['pandera>=0.13.4,<0.14.0',
 'psycopg2[binary]>=2.9.5,<3.0.0',
 'pydantic>=1.10.1,<2.0.0',
 'sqlmodel>=0.0.8,<0.0.9']

extras_require = \
{'book': ['jupyter-book>=0.13.0,<0.14.0',
          'jupytext>=1.14.0,<2.0.0',
          'altair>=4.2.0,<5.0.0',
          'autodocsumm>=0.2.10,<0.3.0'],
 'google': ['fs-gcsfs>=1.5.1,<2.0.0'],
 'test': ['pytest>=7.1.2,<8.0.0']}

setup_kwargs = {
    'name': 'nysmix',
    'version': '0.9.0',
    'description': 'pulling nys fuel mix data from nysiso',
    'long_description': 'None',
    'author': 'Gautam Sisodia',
    'author_email': 'gautam.sisodia@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
