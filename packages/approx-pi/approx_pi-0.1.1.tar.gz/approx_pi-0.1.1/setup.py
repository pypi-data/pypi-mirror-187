# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['approx_pi']

package_data = \
{'': ['*']}

install_requires = \
['cowsay>=5.0,<6.0']

setup_kwargs = {
    'name': 'approx-pi',
    'version': '0.1.1',
    'description': 'A simple package approximating Pi to learn the basics of Python packaging. (https://www.youtube.com/watch?v=ApDThpsr2Fw)',
    'long_description': '',
    'author': 'Patrick Merlot',
    'author_email': 'patrick.merlot@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
