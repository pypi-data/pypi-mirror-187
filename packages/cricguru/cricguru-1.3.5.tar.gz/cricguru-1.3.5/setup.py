# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cricguru']

package_data = \
{'': ['*']}

install_requires = \
['bs4>=0.0.1,<0.0.2', 'pandas>=1.5.2,<2.0.0']

setup_kwargs = {
    'name': 'cricguru',
    'version': '1.3.5',
    'description': '',
    'long_description': '<h2 align="center">Cricguru</h2>\n\n## Overview\nCricguru is a data extraction module for extracting data from the Statsguru data query on Cricinfo. I was inspired to build a simple tool to extract dataframes from statsguru for analyzing cricket data and was finding it difficult to obtain overall figures from the website as they did not have an API for it. Cricinfo has a large variety of cricket data for all classes of cricket matches and also in-depth player data. However without an API it is impossible to extract any useful information from it. Hence this module has functions to easily get the cricket data we want without having to manually scrape the website. The data output is currently returned in the form of Pandas dataframes. You can find the full documentation <a href="https://cricguru.readthedocs.io/en/stable/overview.html" target="_blank">here</a>.\n\n## Team Data\nData by team can be obtained for the three main classes of cricket formats which are <b>Test</b>, <b>One-day</b> and <b>T20</b>. Excluding the class argument would return the overall data. In order to filter by teams and opposition you must provide one of the following ids to the team and opposition arguments respectively for some popular teams.\n\n{"all teams": "", "Afghanistan": "40", "Australia": "2", "Bangladesh": "25", "England": "1", "ICC World XI": "140", "India": "6", "Ireland": "29", "New Zealand": "5", "Pakistan": "7", "South Africa": "3", "Sri Lanka": "8", "West Indies": "4", "Zimbabwe": "9"}\n\n## Player Data\nData by player can be obtained for the same classes mentioned above. The player class however requires a player id which can be obtained from Cricinfo by selecting a team followed by a player from that team. For example <a href="https://www.espncricinfo.com/player/angelo-mathews-49764">Angelo Mathew\'s</a> id is 49764 which can be found appended to the url of the player\'s stats page on Cricinfo.\n\n## Built With\nThis project primarily uses Python 3.8 in combination with Pandas. Pandas is used to get the tables directly from the Statsguru query pages and convert them to dataframes. Urllib is used to format the url and append the query parameters. Poetry is used for packaging and publishing.\n\n## Getting Started\nYou can install the package using the following command.\n```sh\npip install cricguru\n```\n\n## Usage\nYou can get overall figures for all teams with the following. You must pass in the query parameters in a dictionary as shown.\n```sh\nfrom cricguru import team\n\nteam = team.Team()\nquery_params = {"template": "results"}\ncric_data = team.overall(query_params)\n\n#Returns a pandas dataframe\ncric_data.head()\n```\nFor player data you have to provide the player id to initialize the player object and then call the function for the type of data you require. You have to specify what type of player data you need such as allround, batting or bowling.\n\n```sh\nfrom cricguru import player\n\nplayer = player.Player(49764)\nquery_params = {\n    \'class\' : \'1\',\n    \'type\' : \'allround\'\n}\n\ncric_data = player.career_summary(query_params)\nprint(cric_data.head())\n```\n\n## Contributing\nThis is an amateur project at best and I am still a complete beginner to Python and would greatly welcome any suggestions, advice, constructive criticism, best practices or contributions to the project.  Simply open a pull request or issue and I will check it out.\n\n## Contact\nYou can also contact me at pavithranthilakanathan@gmail.com or on twitter - <a href="https://twitter.com/pavin_v1">@pavin_v1</a>\n\n## License\nDistributed under the MIT license. See `LICENSE.md\' for more information.\n\n## Acknowledgements\n<ul>\n  <li><a href="https://www.espncricinfo.com/">ESPN Cricinfo</a></li>\n</ul>\n\n## Todo\n<ul>\n  <li>100% code coverage</li>\n  <li>Additional data formats</li>\n</ul>\n',
    'author': 'Pavithran',
    'author_email': 'pavithranthilakanathan@gmai.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/puppetmaster12/cricguru',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
