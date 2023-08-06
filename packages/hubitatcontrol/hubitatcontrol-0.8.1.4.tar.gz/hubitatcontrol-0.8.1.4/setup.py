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
    'version': '0.8.1.4',
    'description': 'Hubitat Maker API Interface',
    'long_description': "# Hubitat Elevation Maker API Interface (with Requests)\n\n[![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/jelloeater/hubitatcontrol/test.yml?branch=main)](https://github.com/Jelloeater/hubitatcontrol/actions/workflows/test.yml)\n[![GitHub issues by-label](https://img.shields.io/github/issues/jelloeater/hubitatcontrol/bug)](https://github.com/Jelloeater/hubitatcontrol/labels/bug)\n[![GitHub pull requests](https://img.shields.io/github/issues-pr/jelloeater/hubitatcontrol)](https://github.com/Jelloeater/hubitatcontrol/pulls)\n[![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/hubitatcontrol)](https://libraries.io/pypi/hubitatcontrol)\n[![GitHub](https://img.shields.io/github/license/jelloeater/hubitatcontrol)](https://github.com/Jelloeater/hubitatcontrol/blob/main/LICENSE)\n\n[![Packaged with Poetry](https://img.shields.io/badge/packaging-poetry-cyan.svg)](https://python-poetry.org/)\n[![PyPI](https://img.shields.io/pypi/v/hubitatcontrol)](https://pypi.org/project/hubitatcontrol/)\n![PyPI - Format](https://img.shields.io/pypi/format/hubitatcontrol)\n![PyPI - Status](https://img.shields.io/pypi/status/hubitatcontrol)\n[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org)\n![GitHub top language](https://img.shields.io/github/languages/top/jelloeater/hubitatcontrol)\n![GitHub commit activity](https://img.shields.io/github/commit-activity/m/jelloeater/hubitatcontrol)\n![Lines of code](https://img.shields.io/tokei/lines/github/jelloeater/hubitatcontrol)\n\n\n## Usage\n```shell\npip install hubitatcontrol\n```\n\n```python\nimport hubitatcontrol as hc\n\nhub = hc.get_hub(host='Hubitat_IP_or_Hostname', token='Maker_Token', app_id='Maker_App_ID')\ndevice = hc.lookup_device(hub, 'Device_Name')\n\nprint(device.switch)\ndevice.turn_on()\nprint(device.switch)\n```\n\n## Roadmap\n### v0.5\n- [X] Advanced Zigbee RGBW Bulb\n### v0.7\n- [X] Generic Zigbee Outlet\n### v0.8\n- [X] Leviton DZ6HD Z-Wave Dimmer\n### v1.0\n- [ ] hueBridgeBulb\n### v1.1\n- [ ] hueBridgeBulbCT\n### v1.2\n- [ ] hueBridgeBulbRGBW\n### v1.5\n- [ ] Ecobee Thermostat\n### v2.0\n- [ ] Generic Z-Wave Lock\n### v2.5\n- [ ] Generic Z-Wave Plus Scene Switch\n### v2.6\n- [ ] Generic Zigbee Contact Sensor (no temp)\n- [ ] Sonoff Zigbee Button Controller\n\n## Structure\n\n```mermaid\nflowchart LR\nSpecific_Device --> Abstract_Device_Class --> Device--> Hub\n```\n\n## Development setup\nTesting is done with PyTest, you will need to set up the correct env vars for your local (or cloud) Hubitat API\nSee `.env.example`\n\n**Setup**\n\nInstall Go-Task --> <https://taskfile.dev/installation/>\n\n```shell\ntask setup\ntask\n```\n",
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
