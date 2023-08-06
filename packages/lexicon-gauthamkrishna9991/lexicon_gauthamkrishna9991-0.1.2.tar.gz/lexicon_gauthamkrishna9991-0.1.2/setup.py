# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['lexicon']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==5.4.1',
 'blessed>=1.19.1,<2.0.0',
 'colorama==0.4.4',
 'inquirer>=3.1.2,<4.0.0',
 'six==1.15.0',
 'wcwidth==0.2.5']

entry_points = \
{'console_scripts': ['lexicon = lexicon.main:main']}

setup_kwargs = {
    'name': 'lexicon-gauthamkrishna9991',
    'version': '0.1.2',
    'description': 'A Verilog Project Management Tool',
    'long_description': '# Lexicon\n\nThis is a Verilog Project Manager.\n\nThis documentation consists of different parts. To go to one click one of the following:\n\n- [`Project Specification`](Project/README.md)\n\n    This descrbes the project specification of the project-manager.\n\n## Installation\n\nFor Install Instructions, Click [here](INSTALL.md)\n\n## License\n\nCopyright (c) 2021 Goutham Krishna K V\n\nAll rights reserved, as per defined by [MIT License](../LICENSE)\n',
    'author': 'Goutham Krishna K V',
    'author_email': 'gauthamkrishna9991@live.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
