#!/usr/bin/env python

from distutils.core import setup

setup(name = 'pybrarius',
      version = '0.0.0a',
      packages = ['pybrarius'],
      install_requires = ['sqlobject>=3.0.0a', 'PyQt5', 'passlib', 'reportlab'])