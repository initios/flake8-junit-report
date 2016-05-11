#!/usr/bin/env python
# Copyright 2015 Initios Desarrollos
#
# All rights reserved

import os
import setuptools


base_dir = os.path.dirname(__file__)

about = {}
with open(os.path.join(base_dir, 'junit_conversor', '__about__.py')) as f:
    exec(f.read(), about)

with open(os.path.join(base_dir, 'README.rst')) as readme:
    long_description = readme.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setuptools.setup(
    name=about['__title__'],
    version=about['__version__'],

    description=about['__summary__'],
    long_description=long_description,
    license=about['__license__'],
    url=about['__uri__'],

    author=about['__author__'],
    author_email=about['__email__'],

    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: BSD License',
    ],

    packages=[
        'junit_conversor',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'flake8_junit = junit_conversor.__main__:main',
        ],
    }
)
