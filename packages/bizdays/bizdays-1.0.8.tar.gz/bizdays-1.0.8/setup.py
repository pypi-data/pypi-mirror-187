# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['bizdays']
setup_kwargs = {
    'name': 'bizdays',
    'version': '1.0.8',
    'description': 'Functions to handle business days calculations',
    'long_description': "[![Downloads](https://img.shields.io/pypi/dm/bizdays.svg)](https://pypi.python.org/pypi/bizdays/)\n[![Latest Version](https://img.shields.io/pypi/v/bizdays.svg)](https://pypi.python.org/pypi/bizdays/)\n[![Supported Python versions](https://img.shields.io/pypi/pyversions/bizdays.svg)](https://pypi.python.org/pypi/bizdays/)\n\n# [python-bizdays](http://wilsonfreitas.github.io/python-bizdays/)\n\nIn several countries and markets, the accountability of the price of a financial\ninstrument, mainly bonds and derivatives, involves the use of different rules to\ncompute the way the days go by.\nIn Brazil, several financial instruments pay interest according to the business\ndays along their life cycle.\nSo, having a way to compute the number of business days between 2 dates is\nfairly useful to price financial instruments.\n**bizdays** was created to make it easier.\n\n**bizdays** computes business days between two dates based on the definition of\nnonworking days (usually holidays and weekends).\nIt also computes other collateral effects like adjust dates for the next or\nprevious business day, check whether a date is a business day, create sequences\nof business days, and much more.\n\nSeveral financial libraries compute the holidays, giving no option to users set\nit by their own.\nFurtherly, the financial calendar is usually a small feature of a huge library,\nas quantlib, for example, and some users, including myself, don't want to put a\nhand in such a huge library only to use the financial calendar.\n\n**bizdays** is a pure Python module without strong dependencies,\nwhat makes it appropriated for small projects.\n\n",
    'author': 'wilsonfreitas',
    'author_email': 'wilson.freitas@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
