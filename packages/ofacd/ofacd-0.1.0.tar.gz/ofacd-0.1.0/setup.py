#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup
from ofacd.__init__ import __version__

# read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()


setup(
  name='ofacd',
  version=__version__,
  description='Organize files and clean directories',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author='Nodaa Gaji',
  author_email='c0d3r.nodiru.gaji@gmail.com',
  url='https://pypi.org/project/ofacd',
  download_url='https://github.com/ames0k0/ofacd',
  packages=['ofacd'],
  license='License :: OSI Approved :: MIT License',
  classifiers=[
    'Programming Language :: Python :: 3.10',
  ],
  platforms=[
    'Operating System :: OS Independent',
  ],
)
