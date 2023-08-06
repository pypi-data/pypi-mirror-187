# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['visionai', 'visionai.util']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.2.1,<8.0.0', 'requests>=2.28.2,<3.0.0', 'typer[all]>=0.7.0,<0.8.0']

entry_points = \
{'console_scripts': ['visionai = visionai.main:app']}

setup_kwargs = {
    'name': 'visionai',
    'version': '0.1.3',
    'description': 'Vision AI toolkit',
    'long_description': "# edgectl\n\nEdge device, cameras & scenarios controller.\n\n## Overview\n\n1. Start the server instance\n\n```bash\nmake server.install\nmake server.start\n```\n\n1. Run this utility through docker:\n\n```bash\nmake cli.install\nmake cli.start\n\n# Run python edgectl.py utility from within container\npython3 edgectl.py --get-cameras\n```\n\n1. OR Run CLI from host machine\n\n```bash\n# Run python edgectl.py utility from host machine\npython3 edgectl.py --get-cameras\n```\n\n## Commands\n\nThe following set of commands are supported.\n\n- TODO: Instead of using IoT Hub connection string - support it via an API key that is generated from our website.\n- TODO: Make edgectl into its own repo (public). Create nice documentation on how this can be used in Gitbooks.\n- TODO: Connection string to API key translation through Azure Keyvault\n\nAfter the edgectl configured, we can run the following commands.\n\n```bash\n# Configure edgectl\npython3 edgectl.py --setup --api-key <api-key>\n\n#  Run edgectl utility\npython3 edgectl.py \\\n    # Device\n    --list-devices                          # list devices\n    --use-device <device-id>                # set default device to use\n    --list-modules                          # list running modules status\n    --gpu-stats                             # get device's GPU stats\n    --mem-stats                             # get device's memory stats\n    --scenarios-health                      # how many more scenarios can run\n\n    # Scenarios\n    --list-all-scenarios                    # list all available scenarios\n    --list-scenarios                        # list running scenarios for a camera\n        --camera <camera-name>\n    --start-scenario <scenario-name>        # start a scenario for a camera\n        --camera <camera-name>\n    --stop-scenario <scenario-name>         # stop a scenario for a camera\n        --camera <camera-name>\n\n    # Cameras\n    --list-cameras                          # list cameras\n    --add-camera <camera-name>              # add a camera\n        --camera-uri <camera-uri>\n    --remove-camera <camera-name>           # remove camera\n\n    # Livestream\n    --start-livestream <camera-name>        # start live-stream for camera\n    --stop-livestream <camera-name>         # stop live-stream for camera\n\n    # Events\n    --list-events                           # list supported events\n        --scenario  <scenario-name>\n\n    --event-details                         # list details for an event\n        --scenario <scenario-name>\n        --event <event-name>\n\n    --event-log                             # list last few events from camera\n        --camera <camera-name>\n        --last <duration-seconds>\n\n    # Simulation\n    --simulate-event                        # simulate generating an event\n        --camera <camera-name>\n        --scenario <scenario-name>\n        --event <event-name>\n        --event-data <event-data>\n\n```\n",
    'author': 'Harsh Murari',
    'author_email': 'hmurari@visionify.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
