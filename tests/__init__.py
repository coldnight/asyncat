#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""This module provides the base class of all the test case."""
from __future__ import print_function, division, unicode_literals

import os

import dotenv

from tornado import testing

from asyncat.client import AsyncGithubClient

dot_envpath = os.path.join(os.path.dirname(os.path.dirname(__file__)), '.env')

if os.path.exists(dot_envpath):
    dotenv.load_dotenv(dot_envpath)


class AsyncatTestCase(testing.AsyncTestCase):
    def setUp(self):
        super(AsyncatTestCase, self).setUp()
        token = os.environ.get("ASYNCAT_TOKEN")
        self.client = AsyncGithubClient(token)
