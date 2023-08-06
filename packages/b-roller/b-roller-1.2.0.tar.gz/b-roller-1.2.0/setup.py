# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['b_roller']

package_data = \
{'': ['*']}

install_requires = \
['ffmpeg-python>=0.2.0,<0.3.0', 'python-slugify', 'pytube', 'requests', 'typer']

entry_points = \
{'console_scripts': ['broll = b_roller.__main__:app']}

setup_kwargs = {
    'name': 'b-roller',
    'version': '1.2.0',
    'description': 'Download resources from several sources across the web',
    'long_description': '# B-Roller\n\nDownload B-roll footage from YouTube **for fair use purposes**.\n\n## Usage\n\n### Download from YouTube\n\n```\nbroll yt [OPTIONS] URL [START] [END]\n\n  Download content from YouTube\n\nArguments:\n  URL      A video id or a YouTube short/long url  [required]\n  [START]  The desired start of the video in seconds or the format 00:00:00\n  [END]    The desired end of the video in seconds or the format 00:00:00\n```\n\nFor example:\n\n```shell\nbroll yt "https://www.youtube.com/watch?v=QFLiIU8g-R0" 00:10 00:17\n```\n',
    'author': 'Antonio Feregrino',
    'author_email': 'antonio.feregrino@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
