#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""asyncat.repo test cases."""
from __future__ import print_function, division, unicode_literals

from tornado import testing

from asyncat import repository

from . import AsyncatTestCase


class RepositoryTestCase(AsyncatTestCase):
    @testing.gen_test
    def test_sync(self):
        repo = repository.Repository(self.client, "asyncat", "demo")

        yield repo.sync()
        self.assertEqual(repo.c["id"], 90337889)
