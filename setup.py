#!/usr/bin/env python

from setuptools import setup, find_packages

setup(name='tic',
      version='0.1-devel',
      description='Tracks In the Cloud',
      author='Sam Elkhateeb',
      author_email='same@nanosn.com',
      url='https://github.com/selkhateeb/tic',
      packages=find_packages(),
      package_dir = {'': 'src'}
     )

