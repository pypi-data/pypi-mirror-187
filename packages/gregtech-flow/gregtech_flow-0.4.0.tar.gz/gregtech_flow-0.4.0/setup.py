# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['gregtech',
 'gregtech.flow',
 'gregtech.flow.config',
 'gregtech.flow.data',
 'gregtech.flow.graph',
 'gregtech.flow.gtnh',
 'gregtech.flow.module']

package_data = \
{'': ['*'], 'gregtech.flow': ['resources/*']}

install_requires = \
['PyYAML>=6.0,<7.0',
 'graphviz>=0.20.1,<0.21.0',
 'prompt-toolkit>=3.0.36,<4.0.0',
 'rich>=13.0.0,<14.0.0',
 'schema>=0.7.5,<0.8.0',
 'sympy>=1.11.1,<2.0.0',
 'typer>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['flow = gregtech:main']}

setup_kwargs = {
    'name': 'gregtech-flow',
    'version': '0.4.0',
    'description': 'Factory Optimization Flowcharts for Gregtech: New Horizons',
    'long_description': '<p></p>\n<p align="center"><img src="assets/gt_flow.png"/></p>\n<br>\n<p align="center">\n    <img alt="PyPI - Python Version" src="https://img.shields.io/pypi/pyversions/gregtech.flow?style=for-the-badge">\n    <img src="https://img.shields.io/github/license/velolib/gregtech-flow?style=for-the-badge" alt="License MIT"/>\n    <a href="https://codecov.io/github/velolib/gregtech-flow" >\n        <img src="https://img.shields.io/codecov/c/github/velolib/gregtech-flow?style=for-the-badge&token=Y59FTD1UC1" alt="Code Coverage"/>\n    </a>\n</p>\n<p></p>\n\n## ❓ What is it?\n<img align="right" width="192" height="192" src="assets/logo_512x.png"/>\n\nThis is a fork of OrderedSet86\'s [gtnh-flow](https://github.com/OrderedSet86/gtnh-flow). In addition to the functionalities of the original tool, this fork has:\n1. Extended formatting of projects\n2. Added stylization add formatting of graphs\n3. Standards to increase readability\n4. A custom command line interface\n\nTo view the full documentation see the official [GT: Flow website](https://velolib.github.io/gregtech-flow/).\n\n## 📖 Samples\nSamples of the graphs included in the repository.\n<details open>\n    <summary><strong>Samples</strong></summary>\n    <img src="samples/rutile-titanium.svg" alt="Rutile -> Titanium">\n    <img src="samples/epoxid.svg" alt="Epoxid">\n</details>\n',
    'author': 'velolib',
    'author_email': 'vlocitize@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
