# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['scrapemove', 'scrapemove.models', 'tests']

package_data = \
{'': ['*'], 'tests': ['test_data/*']}

install_requires = \
['beautifulsoup4>=4.11.1,<5.0.0',
 'click',
 'inflection>=0.5.1,<0.6.0',
 'pydantic>=1.10.2,<2.0.0',
 'requests>=2.28.1,<3.0.0']

entry_points = \
{'console_scripts': ['scrapemove = scrapemove.cli:main']}

setup_kwargs = {
    'name': 'scrapemove',
    'version': '0.1.2',
    'description': 'Top-level package for scrapemove.',
    'long_description': '==========\nscrapemove\n==========\n\n\n.. image:: https://img.shields.io/pypi/v/scrapemove.svg\n        :target: https://pypi.python.org/pypi/scrapemove\n\n.. image:: https://img.shields.io/travis/briggySmalls/scrapemove.svg\n        :target: https://travis-ci.com/briggySmalls/scrapemove\n\n.. image:: https://readthedocs.org/projects/scrapemove/badge/?version=latest\n        :target: https://scrapemove.readthedocs.io/en/latest/?badge=latest\n        :alt: Documentation Status\n\n\n\n\nScraper for rightmove property data\n\n\n* Free software: MIT\n* Documentation: https://scrapemove.readthedocs.io.\n\n\nFeatures\n--------\n\n* TODO\n\nCredits\n-------\n\nThis package was created with Cookiecutter_ and the `briggySmalls/cookiecutter-pypackage`_ project template.\n\n.. _Cookiecutter: https://github.com/audreyr/cookiecutter\n.. _`briggySmalls/cookiecutter-pypackage`: https://github.com/briggySmalls/cookiecutter-pypackage\n',
    'author': 'Sam Briggs',
    'author_email': 'briggySmalls90@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/briggySmalls/scrapemove',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4',
}


setup(**setup_kwargs)
