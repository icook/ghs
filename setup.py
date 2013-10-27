#!/usr/bin/env python

import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'PyMetrics',
    'pymongo',
    'flask',
    'requests',
    'flask-script',
    'flask-login',
    'mongoengine',
    'flask_mongoengine',
    'cryptacular',
    'Flask-OAuthlib',
    'Babel'
]

testing_extras = ['nose', 'coverage', 'beautifulsoup4', 'python-coveralls']

try:
    with open(os.path.join(here, 'README.rst')) as f:
        README = f.read()
except:
    README = ''

setup(name='ghs',
      version='0.1',
      description='A simple stats website for Github projects',
      packages=find_packages(),
      install_requires=requires,
      extras_require={
          'testing': testing_extras
      },
      )
