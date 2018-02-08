#!/usr/bin/env python3
from setuptools import setup, find_packages
# configure the setup to install from specific repos and users

DESC = 'Simple Pastebin client that is not GPL 3'
setup(name='simple-pastebin-client',
      version='1.0',
      description=DESC,
      author='adam pridgen',
      author_email='dso@thecoverofnight.com',
      install_requires=[
            'toml', 'requests', 'regex', 'flask', 'xmljson',
            'selenium', 'beautifulsoup4', 'pytz', 'tzlocal',
                   ],
      packages=find_packages('src'),
      package_dir={'': 'src'},
      dependency_links=[],
      )
