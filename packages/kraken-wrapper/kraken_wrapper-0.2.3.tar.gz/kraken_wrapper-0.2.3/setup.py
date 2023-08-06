# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['wrapper']

package_data = \
{'': ['*']}

install_requires = \
['keyring>=23.8.2,<24.0.0',
 'kraken-common>=0.5.2,<0.6.0',
 'pex>=2.1.103,<3.0.0',
 'setuptools>=33.0.0',
 'termcolor>=1.1.0,<2.0.0']

entry_points = \
{'console_scripts': ['krakenw = kraken.wrapper.main:main']}

setup_kwargs = {
    'name': 'kraken-wrapper',
    'version': '0.2.3',
    'description': '',
    'long_description': '# kraken-wrapper\n\nProvides the `krakenw` command which is a wrapper around Kraken build scripts to construct an isolated and\nreproducible build environment as per the dependencies specified in the script.\n\nFor more information, check out the [Kraken Documentation](https://kraken-build.github.io/docs/).\n',
    'author': 'Unknown',
    'author_email': 'me@unknown.org',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
