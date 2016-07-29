# -*- coding: utf-8 -*-
import requests

from reddit.exceptions import *

API_URL = 'https://api.reddit.com'
USER_AGENT = 'reddit-cli-application'


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

    print ('call', '{}/{}.json'.format(API_URL, path))

    resp = requests.get('{}/{}.json'.format(API_URL, path),
                        params=params,
                        headers={'User-agent': USER_AGENT}).json()

    if not resp or u'error' in resp:
        raise RedditApiError(message=resp.get('message', ''))

    return resp


def search_subreddits(query=None, limit=100):
    """Search subreddits by query."""

    params = {'q': query, 'limit': limit}
    resp = _api_call('subreddits/search', params)

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

    resp = _api_call('r/{}/{}'.format(name, order), params)

    children = resp['data']['children']
    if len(children) == 0:
        raise SubredditNotFound(message=subreddit_name)
    elif len(children) > limit:
        children = children[:limit]

    return (item['data'] for item in children)


def get_comments(submission_id):
    """Fetch comments of reddit submission."""

    resp = _api_call('comments/{}'.format(submission_id))
    data = (item['data']['children'] for item in resp)
    return (item for sublist in data for item in sublist)
