#!/usr/bin/python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Blitzr Python Client',
    'author': 'Blitzr',
    'url': 'https://github.com/blitzr/blitzrpythonclient',
    'download_url': 'https://github.com/blitzr/blitzrpythonclient/tarball/0.1.0',
    'author_email': 'contact@blitzr.com',
    'version': '0.1.0',
    'install_requires': ['requests'],
    'packages': ['blitzrpythonclient'],
    'scripts': [],
    'name': 'blitzrpythonclient'
}

setup(**config)
