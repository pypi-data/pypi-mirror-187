# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['textual_bee']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['textual-bee = textual_bee:run_app']}

setup_kwargs = {
    'name': 'textual-bee',
    'version': '0.5.0',
    'description': '',
    'long_description': "# textual-bee\n\n![preview](https://raw.githubusercontent.com/torshepherd/textual-bee/main/preview.png)\n\nGet it on PyPI:\n\n```sh\npip install textual-bee\ntextual-bee\n```\n\n## How to play\n\nSubmit words that include the center letter and are at least 4 letters long.\n\n- Press the shuffle button (spacebar) to shuffle the outer letters.\n- Press CTRL-C to quit.\n- Press CTRL-R to reset and choose a new set of letters.\n- Press (tab) to view your already-found words.\n\n## Scoring\n\nYour grade is based on how many of the possible words you find:\n\n| Words found | Grade      |\n| ----------- | ---------- |\n| 0-2%        | Beginner   |\n| 2-5%        | Good Start |\n| 5-8%        | Moving Up  |\n| 8-15%       | Good       |\n| 15-25%      | Solid      |\n| 25-40%      | Nice       |\n| 40-50%      | Great      |\n| 50-70%      | Amazing    |\n| 70-100%     | Genius     |\n| 100%        | Queen Bee  |\n\n### Notes:\n\nThe word list doesn't correspond exactly to Sam's, but it was the closest I could find (margin of error seemed to be about 10%). In general, this game allows more proper nouns and fewer esoteric words, but it varies depending on the setup.\n\n_Inspired by https://github.com/ajeetdsouza/clidle_\n",
    'author': 'torshepherd',
    'author_email': 'tor.aksel.shepherd@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
