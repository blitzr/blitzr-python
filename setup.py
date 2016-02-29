#!/usr/bin/python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Blitzr Python Client',
    'author': 'Blitzr',
    'url': 'URL to get it at.',
    'download_url': 'Where to download it.',
    'author_email': 'contact@blitzr.com',
    'version': '0.1.0',
    'install_requires': ['requests'],
    'packages': ['blitzrpythonclient'],
    'scripts': [],
    'name': 'blitzrpythonclient'
}

setup(**config)
