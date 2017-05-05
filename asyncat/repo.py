#!/usr/bin/env python
# -*- coding:utf-8 -*-
""" Implement Github operation """
from __future__ import print_function, division, unicode_literals

from tornado import gen

from .enum import StatusState


class GithubEntity(object):
    def __init__(self, client, *args, **kwargs):
        """Initialize

        :param client: Github client instance
        :type client: :class:`~asyncat.client.AsyncGithubClient`
        :param *args: arguments to initialize
        :param **kargs: keyword arguments to initialize
        """
        #: Entity content
        self.c = {}
        self.client = client
        self.initialize(*args, **kwargs)
        self._sync_info = {}

    def initialize(self):
        """Override this method to initialize in subclass."""
        pass

    @gen.coroutine
    def sync(self):
        """Synchronize with Github, use Github's data to fill current entity.

        :returns: self
        """
        yield self.do_sync()
        raise gen.Return(self)

    def do_sync(self):
        """Override this method to implemente synchronizes with Github.
        This method must returns an instance of
        :class:`tornado.concurrent.Future`
        """
        raise NotImplementedError()

    def make(self, entity_cls, *args, **kwargs):
        return entity_cls(self.client, *args, **kwargs)


class _CommentMixin(object):
    def create_comment(self, body):
        """Create comment on issues or pull requests.

        See also:
            https://developer.github.com/v3/issues/comments/#create-a-comment
        """
        return self.client.request(
            "{}/issues/{}/comments".format(self.repo.base_path, self.num),
            params={"body": body},
            method="POST"
        )


class PullRequest(GithubEntity, _CommentMixin):
    """Representes a pull reuqest of Github.

    See also: https://developer.github.com/v3/pulls/#get-a-single-pull-request
    """
    def initialize(self, repo, num):
        """Initialize

        :type repo: :class:`Repository`
        :param num: number of pull request
        """
        self.repo = repo
        self.num = num

    @gen.coroutine
    def do_sync(self):
        self.c = yield self.client.request(
            '{}/pulls/{}'.format(self.repo.base_path, self.num))


class Repository(GithubEntity):
    """Representes a repository of Github."""
    def initialize(self, owner, label):
        self.owner = owner
        self.label = label

    @property
    def base_path(self):
        return "/repos/{}/{}".format(self.owner, self.label)

    def pull(self, num):
        """

        :rtype: :class:`PullRequest`
        """

        pull = self.make(PullRequest, self, self.num)
        return pull.sync()

    def merge(self, base, head, message):
        """Perform a merge.

        See also:
            https://developer.github.com/v3/repos/merging/#perform-a-merge
        """
        return self.client.request(
            "{}/merges".format(self.base_path, self.num),
            params={
                "base": base,
                "head": head,
                "commit_message": message
            }, method="POST")

    def create_ref(self, ref, sha):
        """Create a reference

        See also: https://developer.github.com/v3/git/refs/#create-a-reference
        """
        return self.client.request(
            self.base_path + "/git/refs",
            params={
                "ref": ref,
                "sha": sha
            }, method="POST")

    def update_ref(self, ref, sha, force=False):
        """Update a reference

        See also: https://developer.github.com/v3/git/refs/#update-a-reference
        """
        return self.client.request(
            self.base_path + "/git/refs/" + ref,
            params={
                "sha": sha,
                "force": force,
            }, method="PATCh")

    def create_status(self, sha, state, **kwargs):
        """Create a status

        See also:
            https://developer.github.com/v3/repos/statuses/#create-a-status
        """
        state = StatusState(state)
        params = {
            "state": state.value,
        }

        params.update(kwargs)

        return self.client.request(
            self.base_path + "/statuses/" + sha, params=params, method="POST")

    def get_statuses(self, sha):
        """Returns statuses for a specific SHA.

        See also:
            https://developer.github.com/v3/repos/statuses/#list-statuses-for-a-specific-ref
        """
        return self.client.request(
            self.base_path + "/commits/" + sha + "/statuses")
