#!/usr/bin/env python
# pushstore_parser.py
# Copyright 2016 Jake Valletta (@jake_valletta)
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
"""pushstore_parser.py Setup Script"""

from __future__ import print_function
from __future__ import absolute_import
from setuptools import setup

import os

def read(fname):

    """Read file"""
    
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='pushstore-parser',
    version='0.1.0',
    description='Python script to parse Apple Push Notification ("APN") .pushstore files',
    long_description=read('README.md'),

    url='https://github.com/jakev/pushstore-parser',
    download_url='https://github.com/jakev/pushstore-parser',

    author='Jake Valletta',
    author_email='javallet@gmail.com',
    license='ASL',

    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Information Technology',
        'Topic :: Security',
        'Topic :: System :: Recovery Tools',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'],

    keywords='iOS apple push notification service forensics device security mobile parser',

    packages=["pushstore_parser"],

    install_requires=['biplist'],

    entry_points={
      'console_scripts': [
          'pushstore_parser = pushstore_parser.pushstore_parser:main'
      ]
    },
)
