# -*- coding: utf-8 -*-
from utils import echo
from click.exceptions import ClickException


class RedditApiError(ClickException):
    """An internal exception that signals api request error."""

    def __init__(self, message):
        ClickException.__init__(self, message)
        self.message = message

    def show(self):
        echo('Reddit api error: {}'.format(self.message), fg='red')
