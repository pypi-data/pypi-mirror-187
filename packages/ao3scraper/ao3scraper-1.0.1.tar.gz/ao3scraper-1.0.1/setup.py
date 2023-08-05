# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['ao3scraper', 'ao3scraper.tests']

package_data = \
{'': ['*']}

install_requires = \
['PyYAML==6.0',
 'Pygments==2.12.0',
 'SQLAlchemy>=1.4.41,<2.0.0',
 'alembic>=1.8.1,<2.0.0',
 'ao3-api>=2.3.0,<3.0.0',
 'beautifulsoup4==4.11.1',
 'certifi==2022.5.18.1',
 'chardet==4.0.0',
 'click==8.0.1',
 'commonmark==0.9.1',
 'configparser>=5.3.0,<6.0.0',
 'deepdiff[murmur]>=5.8.1,<6.0.0',
 'dictdiffer>=0.9.0,<0.10.0',
 'idna==2.10',
 'marshmallow-sqlalchemy>=0.28.1,<0.29.0',
 'pathlib>=1.0.1,<2.0.0',
 'platformdirs>=2.5.4,<3.0.0',
 'requests==2.25.1',
 'rich==12.4.1',
 'ruamel-yaml>=0.17.21,<0.18.0',
 'soupsieve==2.3.2.post1',
 'urllib3==1.26.9']

entry_points = \
{'console_scripts': ['ao3scraper = ao3scraper.cli:main']}

setup_kwargs = {
    'name': 'ao3scraper',
    'version': '1.0.1',
    'description': 'ao3scraper is a python webscraper that scrapes AO3 for fanfiction data, stores it in a database, and highlights entries when they are updated.',
    'long_description': "# ao3scraper\nA python webscraper that scrapes AO3 for fanfiction data, stores it in a database, and highlights entries when they are updated.\n\n![Fanfics Table](https://i.ibb.co/80r9vwR/Fanfic-Table.png)\n\n*Table with an updated entry highlighted.*\n\n## Installation\nInstall required packages with:\n\n    poetry install\n\n## Usage\n    Usage: python3 ao3scraper [OPTIONS]\n\n    Options:\n    -s, --scrape          Launches scraping mode.\n    -c, --cache           Prints the last scraped table.\n    -l, --list            Lists all entries in the database.\n    -a, --add TEXT        Adds a single url to the database.\n    --add-urls            Opens a text file to add multiple urls to the database.\n    -d, --delete INTEGER  Deletes an entry from the database.\n    -v, --version         Display version of ao3scraper and other info.\n    --help                Show this message and exit.\n\n## Configuration\nao3scraper is ridiculously customisable, and most aspects of the program can be modified from here.\nTo find the configuration file location, run `python3 ao3scraper -v`.\n\nao3scraper uses [rich](https://rich.readthedocs.io/en/stable/style.html)'s styling. To disable any styling options, replace the styling value with 'none'.\n\nFics have many attributes that are not displayed by default. To add these columns, create a new option under table_template, like so:\n```yaml\ntable_template:\n- column: characters # The specified attribute\n  name: Characters :) # This is what the column will be labelled as\n  styles: none # Rich styling\n```\nA complete list of attributes can be found [on the wiki](https://github.com/EthanLeitch/ao3scraper/wiki/Fic-Attributes/).\n\n## Migrating the database\nIf you're updating from a legacy version of ao3scraper (before 1.0.0), move `fics.db` to the data location. \nThis can be found by running `python3 ao3scraper -v`.\nThe migration wizard will then prompt you to upgrade your database. \nIf you accept, a backup of the current `fics.db` will be created in `/backups`, and migration will proceed.\n\n## Contributing\nContributions are always appreciated. Submit a pull request with your suggested changes!\n\n## Acknowledgements\nao3scraper would not be possible without the existence of [ao3_api](https://github.com/ArmindoFlores/ao3_api/) and the work of its [contributors](https://github.com/ArmindoFlores/ao3_api/graphs/contributors).",
    'author': 'Ethan',
    'author_email': 'ethanjohnleitch@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/EthanLeitch/ao3scraper',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
