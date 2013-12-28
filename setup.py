#!/usr/bin/python
# -*- coding: utf-8 -*-

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = []
requires = ['argparse', 'httplib2']
scripts  = ['new_editor.py']

setup(
      name         = 'wm_metrics',
      version      = '0.1' ,
      author       = 'Pierre-Selim, Jean-Frédéric',
      author_email = 'ps.huard@gmail.com',
      url          = 'http://github.com.org/Commonists/wm_metrics',
      description  = 'Computing Wikimedia metrics',
      license      = 'MIT',
      packages     = packages,
      install_requires=requires,
      scripts      = scripts,
)
