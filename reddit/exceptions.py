# -*- coding: utf-8 -*-
from views import echo
from click.exceptions import ClickException


class RedditException(ClickException):

    def __init__(self, message):
        ClickException.__init__(self, message)
        self.message = message

    def show(self):
        echo('{}: {}'.format(self.__class__.__name__, self.message), fg='red')


class RedditApiError(RedditException):

    def __init__(self, message):
        RedditException.__init__(self, message)
        self.message = message


class SubredditNotFound(RedditException):

    def __init__(self, message):
        RedditException.__init__(self, message)
        self.message = message


class InvalidOption(RedditException):

    def __init__(self, message):
        RedditException.__init__(self, message)
        self.message = message
