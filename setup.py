#!/usr/bin/env python

from distutils.core import setup

setup(name = 'hebi-no-shisho',
      version = '0.0.0a',
      packages = ['hebi-no-shisho'],
      requires = ['SQLObject', 'pyGTK', 'passlib'])