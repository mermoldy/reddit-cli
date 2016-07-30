# -*- coding: utf-8 -*-
import requests
from reddit.exceptions import *
from reddit import settings


def _formalize_subreddit_name(name):
    """Formalize subreddit name."""

    if name.startswith('/r/'):
        name = name[3:]
    elif name.startswith('r/'):
        name = name[2:]
    name = name.replace('/', '')
    return name


def _api_call(path, params=None):
    """Request to reddit api."""

    resp = requests.get(u'{}/{}.json'.format(settings.REDDIT_API_URL, path),
                        params=params,
                        headers={'User-agent': settings.USER_AGENT}).json()

    if not resp or u'error' in resp:
        raise RedditApiError(message=resp.get('message', ''))

    return resp


def search_subreddits(query=None, limit=100):
    """Search subreddits by query."""

    params = {'q': query, 'limit': limit}
    resp = _api_call(u'subreddits/search', params)

    if u'data' not in resp:
        raise RedditApiError(message='Invalid response')

    children = resp['data']['children']
    if len(children) == 0:
        raise SubredditNotFound(message=query)

    return (item['data'] for item in children)


def get_submissions(subreddit_name, limit=100, order='top'):
    """Fetch submissions of subreddit."""

    if order not in ['hot', 'new', 'rising', 'top', 'controversial']:
        raise InvalidOption(message="wrong order argument")

    params = {'limit': limit}
    name = _formalize_subreddit_name(subreddit_name)

    resp = _api_call(u'r/{}/{}'.format(name, order), params)

    children = resp['data']['children']

    if len(children) == 0 or \
       any(u'domain' not in i['data'] for i in children):
        raise SubredditNotFound(message=subreddit_name)
    elif len(children) > limit:
        children = children[:limit]

    return (item['data'] for item in children)


def get_comments(submission_id, limit=1000):
    """Fetch comments of reddit submission."""

    params = {'limit': limit}
    resp = _api_call(u'comments/{}'.format(submission_id), params=params)

    data = (item['data']['children'] for item in resp)
    return (item for sublist in data for item in sublist)
