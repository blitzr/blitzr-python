#!/usr/bin/python

import os

try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages

VERSION=os.environ.get('TRAVIS_TAG', '1.1.1')

setup(name='blitzr',
    version=VERSION,
    description='Blitzr Python Client',
    author='Blitzr',
    url='https://github.com/blitzr/blitzr-python',
    download_url='https://github.com/blitzr/blitzr-python/tarball/' + VERSION,
    author_email='contact@blitzr.com',
    install_requires=['requests'],
    long_description=open('README.md').read(),
    zip_safe=False,
    packages=find_packages(exclude=['tests']),
    scripts=[],
    setup_requires=['nose>=1.0'],
    test_suite='nose.collector'
)
