# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pasjonsfrukt']

package_data = \
{'': ['*']}

install_requires = \
['dataclass-wizard[yaml]>=0.22.2,<0.23.0',
 'fastapi>=0.88.0,<0.89.0',
 'podme-api>=0.1.3,<0.2.0',
 'rfeed>=1.1.1,<2.0.0',
 'typer>=0.7.0,<0.8.0',
 'uvicorn>=0.20.0,<0.21.0']

entry_points = \
{'console_scripts': ['pasjonsfrukt = pasjonsfrukt.cli:cli']}

setup_kwargs = {
    'name': 'pasjonsfrukt',
    'version': '0.1.0',
    'description': 'Scrape PodMe podcast streams to mp3 and host with RSS feed',
    'long_description': '# 🍹 pasjonsfrukt\n\n[![PyPI](https://img.shields.io/pypi/v/pasjonsfrukt)](https://pypi.org/project/pasjonsfrukt/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pasjonsfrukt)\n[![PyPI - License](https://img.shields.io/pypi/l/pasjonsfrukt)](https://github.com/mathiazom/pasjonsfrukt/blob/main/LICENSE)\n\nScrape PodMe podcast streams to mp3 and host with RSS feed.\n\n<i style="color:grey">Note: A valid PodMe subscription is required to access premium content</i>\n\n### Setup\n\n1. Install `pasjonsfrukt`\n\n```\npip install pasjonsfrukt\n```\n\n2. Install [`ffmpeg`](https://ffmpeg.org/) (required by dependency `youtube-dl` for the `m3u8` format).\n\n3. Define harvest and feed configurations by copying [`config.template.yaml`](config.template.yaml) to your own `config.yaml`.  \n   Most importantly, you need to provide:\n\n   - a `host` path (for links in the RSS feeds)\n   - login credentials (`auth`) for your PodMe account\n   - the `podcasts` you wish to harvest and serve\n\n### Usage\n\n##### Harvest episodes\n\nHarvest episodes of all podcasts defined in config\n\n```sh\npasjonsfrukt harvest\n```\n\nHarvest episodes of specific podcast(s)\n\n```sh\npasjonsfrukt harvest [PODCAST_SLUG]...\n```\n\n##### Update feeds\n\nUpdate all RSS feeds defined in config\n\n```sh\npasjonsfrukt sync\n```\n\nUpdate RSS feed of specific podcast\n\n```sh\npasjonsfrukt sync [PODCAST_SLUG]...\n```\n\n> The feeds are always updated after harvest, so manual feed syncing is only required if files are changed externally\n\n##### Serve RSS feeds with episodes\n\nRun web server\n\n```sh\npasjonsfrukt serve\n```\n\nRSS feeds will be served at `<host>/<podcast_slug>`, while episode files are served\nat `<host>/<podcast_slug>/<episode_id>`\n\n> `host` must be defined in the config file.\n\n##### Secret\n\nIf a `secret` has been defined in the config, a query parameter (`?secret=<secret-string>`) with matching secret string\nis required to access the served podcast feeds and episode files. This is useful for making RSS feeds accessible on the\nweb, without making them fully public. Still, the confidentiality is provided as is, with no warranties 🙃\n',
    'author': 'Mathias Oterhals Myklebust',
    'author_email': 'mathias@oterbust.no',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/mathiazom/pasjonsfrukt',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
