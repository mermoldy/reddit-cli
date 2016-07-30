# -*- coding: utf-8 -*-
"""
reddit api tests.
"""

from random import randint
from reddit import utils
from reddit import api

SUBREDDITS = [
    '/r/python/',
    '/r/pokemongo//',
    'opensource'
]


def _calc_replies(comments):
    count = 0
    for comment in comments:
        count += 1
        replies = utils.recursive_get(comment, "data.replies.data.children")
        if replies:
            count += _calc_replies(replies)
    return count


def test_reddit_search():
    for name in SUBREDDITS:
        limit = randint(1, 5)
        subreddits = api.search_subreddits(query=name, limit=limit)
        assert len(list(subreddits)) == limit


def test_reddit_submissions():
    for name in SUBREDDITS:
        limit = randint(1, 5)
        submissions = api.get_submissions(subreddit_name=name, limit=limit)
        assert len(list(submissions)) == limit


def test_reddit_comments():
    for name in SUBREDDITS:
        submissions = list(api.get_submissions(subreddit_name=name))
        comments = api.get_comments(submission_id=submissions[0]['id'])
        assert submissions[0]['num_comments'] == _calc_replies(comments) - 1
