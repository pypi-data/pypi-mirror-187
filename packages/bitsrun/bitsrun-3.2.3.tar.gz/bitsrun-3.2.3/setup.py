# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bitsrun']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'platformdirs>=2.6.2,<3.0.0', 'requests>=2.28.2,<3.0.0']

entry_points = \
{'console_scripts': ['bitsrun = bitsrun.cli:cli']}

setup_kwargs = {
    'name': 'bitsrun',
    'version': '3.2.3',
    'description': 'A headless login / logout script for 10.0.0.55',
    'long_description': '# bitsrun\n\n![PyPI](https://img.shields.io/pypi/v/bitsrun) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/bitsrun) ![PyPI - Downloads](https://img.shields.io/pypi/dm/bitsrun)\n\n_A headless login / logout script for 10.0.0.55 at BIT._\n\n## Install\n\nYou need at least **Python 3.8**. We recommend installing with `pipx`.\n\n```bash\npython3 -m pip install --user pipx\npython3 -m pipx ensurepath\n```\n\nAfter which, install `bitsrun` with `pipx`.\n\n```bash\npipx install bitsrun\n```\n\n## Usage\n\n### CLI\n\n```text\nUsage: bitsrun login/logout [OPTIONS]\n\n  Log in/out the BIT network.\n\nOptions:\n  -u, --username TEXT  Username.\n  -p, --password TEXT  Password.\n  -v, --verbose        Verbose output.\n  -s, --silent         Silent output.\n  -nc, --no-color      No color output.\n  --help               Show this message and exit.\n```\n\n### Configuration file\n\nCreate new file named `bit-user.json`:\n\n```json\n{\n    "username": "xxxx",\n    "password": "xxxx"\n}\n```\n\nThis file should be put under the following directory:\n\n- Windows: `%APPDATA%\\bitsrun`\n- macOS and Linux: `~/.config/bitsrun` (Following the XDG spec)\n\nNow you can simply call:\n\n```bash\nbitsrun login\nbitsrun logout\n```\n\nBesides, a system-wide configuration file is supported, and the location also depends on your platform.\n\nTo list all possible paths for your system (including those only for backward compatibility), call:\n\n```shell\nbitsrun config-paths\n```\n\n### Raycast script (macOS)\n\n![CleanShot 2023-01-22 at 21 55 40@2x](https://user-images.githubusercontent.com/32114380/213919582-eff6d58f-1bd2-47b2-a5da-46dc6e2eaffa.png)\n\nImport the two Raycast scripts from [`./scripts`](./scripts/) and setup your config file in `~/.config/bit-user.json`. The script uses `/usr/bin/python3` by default, so you either need to install `bitsrun` with this Python interpreter or setup your own Python interpreter path in the script.\n\n## Developing\n\nInstall and run:\n\n```bash\n# Create virtual env and install deps\npoetry install\n\n# Enter poetry virtual env\npoetry shell\n```\n\nBuild:\n\n```bash\n# Bump version\npoetry version x.x.x\n\n# Building the wheel\npoetry build\n```\n\nPublish:\n\n```bash\npoetry publish\n```\n\n## License\n\n[WTFPL License](LICENSE)\n',
    'author': 'spencerwooo',
    'author_email': 'spencer.woo@outlook.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/BITNP/bitsrun',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
