# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['foss505', 'foss505.ui']

package_data = \
{'': ['*'], 'foss505.ui': ['assets/fonts/*', 'assets/images/*']}

install_requires = \
['jack-client>=0.5.4,<0.6.0', 'numpy>=1.24.1,<2.0.0']

extras_require = \
{':python_version >= "3.10" and python_version < "3.12"': ['PySide6==6.4.1']}

entry_points = \
{'console_scripts': ['foss505 = foss505:run']}

setup_kwargs = {
    'name': 'foss505',
    'version': '0.1.0a0',
    'description': 'The ultimate loop station.',
    'long_description': '![](https://github.com/ramazanemreosmanoglu/foss505/blob/main/readme_assets/banner-4s-round.gif)\n\n<div align="center">\n  <b>Disclaimer:</b> This project is currently at the early development. Expect <a href="https://github.com/ramazanemreosmanoglu/foss505/blob/main/TODO.org#bugs-02">bugs</a>.\n</div>\n\n# Installation\n\nI didn\'t test for operating systems other than linux for now. A running Jack server and -<i>probably</i>- a patchbay (qpwgraph, qjackctl etc.) required.\n\n### Using pipx (Recommended)\n\n```\npipx install foss505\n```\n\npipx will install the program in a clean environment for you. But you can alternatively do the:\n\n### Using pip\n\n```\npip install foss505\n```\n\n### Development Setup\n\nMake sure you have <a href="">poetry</a> installed on your system.\n\n```\ngit clone https://github.com/ramazanemreosmanoglu/foss505\ncd foss505/\npoetry install\n```\n\nBuilding:\n\n```\npoetry build\n```\n\nInstalling:\n\n```\npip install dist/foss505-X-X-X-py3-none-any.whl\n```\n\n# Usage\n\nRunning the program:\n\n```\n# Assuming that you have $HOME/.local/bin on your PATH.\nfoss505\n```\n',
    'author': 'ramazanemreosmanoglu',
    'author_email': 'ramazanemre@protonmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ramazanemreosmanoglu/foss505',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
