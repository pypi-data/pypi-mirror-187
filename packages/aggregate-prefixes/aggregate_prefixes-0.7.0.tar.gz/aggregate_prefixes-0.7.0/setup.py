# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['aggregate_prefixes']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['aggregate-prefixes = aggregate_prefixes.__main__:main']}

setup_kwargs = {
    'name': 'aggregate-prefixes',
    'version': '0.7.0',
    'description': '',
    'long_description': '# aggregate-prefixes\nFast IPv4 and IPv6 prefix aggregator written in Python.  \n\nGets a list of unsorted IPv4 or IPv6 prefixes from argument or SDTIN and returns a sorted list of aggregates to STDOUT\nErrors go to STDERR.\n\n# Install\n```\ngit clone https://github.com/lamehost/aggregate-prefixes.git\ncd aggregate_prefixes\npoetry build\npip install dist/aggregate_prefixes-0.7.0-py3-none-any.whl\n```\n\n# CLI Syntax for executable\n```\nusage: aggregate-prefixes [-h] [--max-length LENGTH] [--strip-host-mask] [--truncate MASK] [--verbose] [--version] [prefixes]\n\nAggregates IPv4 or IPv6 prefixes from file or STDIN\n\npositional arguments:\n  prefixes              Text file of unsorted list of IPv4 or IPv6 prefixes. Use \'-\' for STDIN.\n\noptions:\n  -h, --help            show this help message and exit\n  --max-length LENGTH, -m LENGTH\n                        Discard longer prefixes prior to processing\n  --strip-host-mask, -s\n                        Do not print netmask if prefix is a host route (/32 IPv4, /128 IPv6)\n  --truncate MASK, -t MASK\n                        Truncate IP/mask to network/mask\n  --verbose, -v         Display verbose information about the optimisations\n  --version, -V         show program\'s version number and exit\n```\n\n# Usage as module\n```\n$ python\nPython 3.9.1+ (default, Feb  5 2021, 13:46:56)\n[GCC 10.2.1 20210110] on linux\nType "help", "copyright", "credits" or "license" for more information.\n>>>\n>>> from aggregate_prefixes import aggregate_prefixes\n>>> list(aggregate_prefixes([\'192.0.2.0/32\', \'192.0.2.1/32\', \'192.0.2.2/32\']))\n[\'192.0.2.0/31\', \'192.0.2.2/32\']\n>>>\n```\n\n# Python version compatibility\nTested with:\n - Python 3.9\n - Python 3.10\n - Python 3.11\n',
    'author': 'Marco Marzetti',
    'author_email': 'marco@lamehost.it',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
