# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mp3cloud']

package_data = \
{'': ['*'], 'mp3cloud': ['scripts/*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'requests>=2.28.1,<3.0.0', 'rich>=12.6.0,<13.0.0']

setup_kwargs = {
    'name': 'mp3cloud',
    'version': '0.1.1',
    'description': 'Search and download any music from freemp3cloud.com',
    'long_description': '# FreeMp3Cloud Downloader\nA lightweight wrapper around [FreeMp3Cloud.com](https://freemp3cloud.com) to download songs by the given query.\n\n## Installation\n```\npip install mp3cloud\n```\n**`cURL` should be installed too**\n\n## Usage\n### CLI\nDownloading a song:\n```\npython -m mp3cloud "[TRACK_NAME] [ARTIST_NAME]"\n```\nGetting all the URLs provided for the query gathered in a `.txt` file:\n```\npython -m mp3cloud "[TRACK_NAME] [ARTIST_NAME]" --save-urls --no-download\n```\n### Python programs\nSeeing the results of the query:\n```py\nfrom mp3cloud import search\n\nsongs = search("[TRACK_NAME] [ARTIST_NAME]")\nfor song in songs:\n    print(song.name, song.artist, song.url, song.duration, song.is_high_quality)\n```\nTo download a song:\n```py\nfrom mp3cloud.utils import download_song\ndownload_song(songs[0])\n```\n\n## Todo\n- [ ] Setting metadata for the downloaded song\n- [ ] Filter by quality\n',
    'author': 'Momo',
    'author_email': 'lo3me@proton.me',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rtcq/freemp3cloud-downloader',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
