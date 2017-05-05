#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""AsyncGithubClient test case."""
from __future__ import print_function, division, unicode_literals

from tornado import testing

from . import AsyncatTestCase


class AsyncGithubClientTestCase(AsyncatTestCase):
    @testing.gen_test
    def test_request(self):
        resp = yield self.client.request("/user")
        self.assertEqual(resp.code, 200)
        self.assertEqual(resp.data["login"], "asyncat")
