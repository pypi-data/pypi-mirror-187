# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hubitatcontrol']

package_data = \
{'': ['*']}

install_requires = \
['requests']

setup_kwargs = {
    'name': 'hubitatcontrol',
    'version': '0.8.1.3',
    'description': 'Hubitat Maker API Interface',
    'long_description': "# Hubitat Elevation Maker API Interface (with Requests)\n\n![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/jelloeater/hubitatcontrol/test.yml?branch=main)\n![GitHub issues by-label](https://img.shields.io/github/issues/jelloeater/hubitatcontrol/bug)\n[![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/hubitatcontrol)](https://libraries.io/pypi/hubitatcontrol)\n![GitHub](https://img.shields.io/github/license/jelloeater/hubitatcontrol)\n\n[![Packaged with Poetry](https://img.shields.io/badge/packaging-poetry-cyan.svg)](https://python-poetry.org/)\n[![PyPI version](https://badge.fury.io/py/hubitatcontrol.svg)](https://badge.fury.io/py/hubitatcontrol)\n![PyPI - Format](https://img.shields.io/pypi/format/hubitatcontrol)\n![PyPI - Status](https://img.shields.io/pypi/status/hubitatcontrol)\n[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org)\n![GitHub top language](https://img.shields.io/github/languages/top/jelloeater/hubitatcontrol)\n![GitHub commit activity](https://img.shields.io/github/commit-activity/m/jelloeater/hubitatcontrol)\n![Lines of code](https://img.shields.io/tokei/lines/github/jelloeater/hubitatcontrol)\n\n\n## Usage\n```python\nfrom hubitatcontrol import *\nh = get_hub(host='Hubitat_IP_or_Hostname', token='Maker_Token', app_id='Maker_App_ID')\nd = lookup_device(h, 'Device_Name')\nprint(d.switch)\nd.turn_on()\nprint(d.switch)\n```\n\n## Roadmap\n### v0.5\n- [X] Advanced Zigbee RGBW Bulb\n### v0.7\n- [X] Generic Zigbee Outlet\n### v0.8\n- [X] Leviton DZ6HD Z-Wave Dimmer\n### v1.0\n- [ ] hueBridgeBulb\n### v1.1\n- [ ] hueBridgeBulbCT\n### v1.2\n- [ ] hueBridgeBulbRGBW\n### v1.5\n- [ ] Ecobee Thermostat\n### v2.0\n- [ ] Generic Z-Wave Lock\n### v2.5\n- [ ] Generic Z-Wave Plus Scene Switch\n### v2.6\n- [ ] Generic Zigbee Contact Sensor (no temp)\n- [ ] Sonoff Zigbee Button Controller\n\n\n## Development setup\n**Tooling**\n- Need Python > 3.10 Installed\n- Doc gen w/ pdoc3 and pyreverse\n- Poetry for package management + Build\n- Code Complexity with Radon and Xenon\n- isort for imports\n- Black for formatting\n- Vulture for dead code\n- Bandit for security\n- Testing with PyTest\n\n- **Setup**\n- Install Go-Task (<https://taskfile.dev/>)(Optional, it's NEAT!)\n  - Linux (`sudo snap install task --classic`)\n\n## Structure\n\n```mermaid\nflowchart LR\nHub --> Device --> Abstract_Device_Class --> Specific_Device\n```\n## Test\n\n```sh\ntask\n```\n",
    'author': 'Jesse Schoepfer',
    'author_email': 'jelloeater@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/Jelloeater/hubitatcontrol',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
