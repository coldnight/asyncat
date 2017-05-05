#!/usr/bin/env python
# -*- coding:utf-8 -*-
""" """
from __future__ import print_function, division, unicode_literals

from setuptools import setup

setup(
    setup_requires=["pbr>=1.9", "setuptools>=17.1", "pytest-runner"],
    tests_require=["python-dotenv", 'pytest'],
    pbr=True
)
