#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = []
requires = ['argparse']
scripts  = []

setup(
      name         = 'wm_metrics',
      version      = '0.1' ,
      author       = 'Pierre-Selim',
      author_email = 'ps.huard@gmail.com',
      url          = 'http://github.com.org/PierreSelim/wm_metrics',
      description  = 'Computing Wikimedia metrics',
      license      = '',
      packages     = packages,
      install_requires=requires,
      scripts      = scripts,
)
