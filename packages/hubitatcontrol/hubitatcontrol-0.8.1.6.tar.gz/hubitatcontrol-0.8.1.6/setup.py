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
    'version': '0.8.1.6',
    'description': 'Hubitat Maker API Interface',
    'long_description': "# Hubitat Elevation Maker API Interface (with Requests)\n\n[![GitHub Workflow Status (with branch)](https://img.shields.io/github/actions/workflow/status/jelloeater/hubitatcontrol/test.yml?branch=main)](https://github.com/Jelloeater/hubitatcontrol/actions/workflows/test.yml)\n![PyPI - Status](https://img.shields.io/pypi/status/hubitatcontrol)\n[![PyPI](https://img.shields.io/pypi/v/hubitatcontrol)](https://pypi.org/project/hubitatcontrol/)\n[![Libraries.io dependency status for latest release](https://img.shields.io/librariesio/release/pypi/hubitatcontrol)](https://libraries.io/pypi/hubitatcontrol)\n[![GitHub](https://img.shields.io/github/license/jelloeater/hubitatcontrol)](https://github.com/Jelloeater/hubitatcontrol/blob/main/LICENSE)\n[![Python 3.10](https://img.shields.io/badge/python-3.10-blue.svg)](https://www.python.org)\n\n## Usage\n\n```shell\npip install hubitatcontrol\n```\n\n```python\nimport hubitatcontrol as hc\n\nhub = hc.get_hub(host='Hubitat_IP_or_Hostname', token='Maker_Token', app_id='Maker_App_ID')\ndevice = hc.lookup_device(hub, 'Device_Name')\n\nprint(device.switch)\ndevice.turn_on()\nprint(device.switch)\n```\n\n## Roadmap\n\n### v0.5\n\n- [X] Advanced Zigbee RGBW Bulb\n\n### v0.7\n\n- [X] Generic Zigbee Outlet\n\n### v0.8\n\n- [X] Leviton DZ6HD Z-Wave Dimmer\n\n### v1.0\n\n- [ ] hueBridgeBulb\n\n### v1.1\n\n- [ ] hueBridgeBulbCT\n\n### v1.2\n\n- [ ] hueBridgeBulbRGBW\n\n### v1.5\n\n- [ ] Ecobee Thermostat\n\n### v2.0\n\n- [ ] Generic Z-Wave Lock\n\n### v2.5\n\n- [ ] Generic Z-Wave Plus Scene Switch\n\n### v2.6\n\n- [ ] Generic Zigbee Contact Sensor (no temp)\n- [ ] Sonoff Zigbee Button Controller\n\n## Structure\n\n```mermaid\nflowchart LR\nSpecific_Device --> Abstract_Device_Class --> Device--> Hub\n```\n\n## Development setup\n\nTesting is done with PyTest, you will need to set up the correct env vars for your local (or cloud) Hubitat API\nSee `.env.example`\n\n**Setup**\n\nInstall Go-Task --> <https://taskfile.dev/installation/>\n\n```shell\ntask setup\ntask\n```\n",
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
