# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cloudcheck', 'cloudcheck.lib']

package_data = \
{'': ['*'], 'cloudcheck.lib': ['cache/*']}

install_requires = \
['bs4>=0.0.1,<0.0.2',
 'click',
 'click-config-file',
 'requests>=2.27.1,<3.0.0',
 'rich']

entry_points = \
{'console_scripts': ['cloudcheck = cloudcheck.__main__:main']}

setup_kwargs = {
    'name': 'cloudcheckr',
    'version': '0.1.0',
    'description': '',
    'long_description': '<div align="center">\n\n# cloudcheck\n\ncloudcheck is a CLI utility to check if IP addresses in a file are associated with a cloud or CDN network.\n\n<br>\n\n[Installation](#installation) •\n[Usage](#usage) •\n[Getting Started](#getting-started) •\n[Coming Soon](#coming-soon)\n[Thanks](#thanks)\n\n</div><br>\n\n</div>\n<br>\n\n## Installation\n\ncloudcheck supports all major operating systems and can be installed from PyPi using the following command:\n\n```\npipx install cloudcheck\n```\n\n<br>\n\n## Getting Started\n\nThe utility supports the following cloud and CDN providers:\n\n- Akamai\n- AWS Cloudfront\n- Azure FrontDoor\n- Cloudflare\n- Fastly\n- Google\n- Succuri\n- Incapsula\n\nOn run, the tool first requests IP ranges from API endpoints hosted by each provider. These ranges are then stored in a dictionary for processing. With this, the ranges are then searched to determine if the input IP addresses are contained within the stored CIDRs.\n\n<br>\n\n## Usage\n\nTo use cloudcheck, execute a command similar to what is shown below:\n\n```\ncloudcheck cdn all /tmp/targets.txt /tmp/output.json\n```\n\nThe tool will request IP ranges from from the supported providers and then search for your target IPs in the requested IP ranges.\n\n<br>\n\n## Coming Soon\n\nSome planned features coming in the next release:\n\n- Support checking all cloud IP ranges\n- Support checking only CDN IP ranges (Done)\n- Support searching specific providers only\n- JSON output support (Done)\n- DNS support\n- Caching for ranges (Done)\n- Support silent mode (Done)\n\n<br>\n\n## Thanks\n\n- 0xdade\'s tool, [sephiroth](https://github.com/0xdade/sephiroth)\n\n- projectdiscovery\'s GO library [cdncheck](https://github.com/projectdiscovery/cdncheck)\n',
    'author': 'Nicholas',
    'author_email': 'nanastasi@sprocketsecurity.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/puzzlepeaches/cloudcheck',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
