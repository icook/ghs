import os
from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'PyMetrics',
    'pymongo'
]

testing_extras = ['nose', 'coverage', 'beautifulsoup4', 'python-coveralls']

try:
    with open(os.path.join(here, 'README.md')) as f:
        README = f.read()
except:
    README = ''

setup(name='githubmetrics',
      version='0.1',
      description='A simple stats website for Github projects',
      packages=find_packages('src'),
      include_package_data=True,
      install_requires=requires,
      test_suite='yota.tests',
      extras_require={
          'testing': testing_extras
      },
      package_dir={'': 'src'}
      )
