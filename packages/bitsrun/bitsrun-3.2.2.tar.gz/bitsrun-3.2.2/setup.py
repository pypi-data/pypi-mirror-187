# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bitsrun']

package_data = \
{'': ['*']}

install_requires = \
['click>=8.1.3,<9.0.0', 'requests>=2.28.2,<3.0.0']

entry_points = \
{'console_scripts': ['bitsrun = bitsrun.cli:main']}

setup_kwargs = {
    'name': 'bitsrun',
    'version': '3.2.2',
    'description': 'A headless login / logout script for 10.0.0.55',
    'long_description': '# bitsrun\n\n> A headless login / logout script for 10.0.0.55 at BIT.\n\n## Install\n\nYou need at least Python 3.8. We recommend installing with `pipx`.\n\n```bash\npython3 -m pip install --user pipx\npython3 -m pipx ensurepath\n```\n\nAfter which, install `bitsrun` with `pipx`.\n\n```bash\npipx install bitsrun\n```\n\n## Usage\n\n### CLI\n\n```bash\nbitsrun login -u|--username xxxx -p|--password xxxx\nbitsrun logout -u|--username xxxx -p|--password xxxx\n```\n\nOptional params:\n\n- `-s|--silent`: No output what-so-ever.\n- `-nc|--no-color`: No color in error or verbose output.\n- `-v|--verbose`: Output verbose information including full response from the API.\n\n### Config file\n\nEither `/etc/bit-user.json` or `~/.config/bit-user.json`:\n\n```json\n{\n    "username": "xxxx",\n    "password": "xxxx"\n}\n```\n\n```bash\nbitsrun login\nbitsrun logout\n```\n\n### Raycast script (macOS)\n\n![Raycast Script Screenshot](assets/raycast-screenshot.png)\n\nImport the two Raycast scripts from [`./scripts`](./scripts/) and setup your config file in `~/.config/bit-user.json`. The script uses `/usr/bin/python3` by default, so you either need to install `bitsrun` with this Python interpreter or setup your own Python interpreter path in the script.\n\n<details>\n<summary>Using networkmanager-dispatcher (deprecated).</summary>\n\n### 使用 NetworkManager-dispacher\n\n将 `bitsrun.py` 复制为 `/usr/bin/bit-login`，权限+x\n\n将 `login-bit.sh` 复制到 `/etc/NetworkManager/dispatcher.d/`\n\n将配置文件保存在 `/etc/bit-user.json`\n\nstart 并且 enable NetworkManager-dispatcher\n\n</details>\n\n## Developing\n\nInstall and run:\n\n```bash\n# Create virtual env and install deps\npoetry install\n\n# Enter poetry virtual env\npoetry shell\n```\n\nBuild:\n\n```bash\n# Bump version\npoetry version x.x.x\n\n# Building the wheel\npoetry build\n```\n\nPublish:\n\n```bash\npoetry publish\n```\n\n## License\n\n[WTFPL License](LICENSE)\n',
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
