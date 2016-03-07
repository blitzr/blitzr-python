#!/usr/bin/python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Blitzr Python Client',
    'author': 'Blitzr',
    'url': 'https://github.com/blitzr/blitzr-python',
    'download_url': 'https://github.com/blitzr/blitzr-python/tarball/0.1.2',
    'author_email': 'contact@blitzr.com',
    'version': '0.1.2',
    'install_requires': ['requests'],
    'packages': ['blitzr'],
    'scripts': [],
    'name': 'blitzr'
}

setup(**config)
