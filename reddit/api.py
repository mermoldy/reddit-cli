# -*- coding: utf-8 -*-
import praw
import requests
from reddit.exceptions import RedditApiError


class Reddit(object):

    def __init__(self):
        self._api_url = 'https://api.reddit.com'
        self._user_agent = 'reddit-cli-application'
        self.praw_api = praw.Reddit(user_agent='reddit-cli-application')

    def _call_api(self, path, params):
        resp = requests.get('{}/{}.json'.format(self._api_url, path),
                            params=params,
                            headers={'User-agent': self._user_agent}).json()
        if u'error' in resp:
            raise RedditApiError(message=resp.get('message', ''))
        if u'data' not in resp:
            raise RedditApiError(message='Invalid response')
        return resp['data']

    def search_subreddits(self, query=None, limit=100):
        params = {'q': query, 'limit': limit}
        data = self._call_api('subreddits/search', params)
        return (item['data'] for item in data['children'])
        # https://api.reddit.com/subreddits/search/?q=te&limit=1
        #return self.praw_api.get_content(url, params=params, limit=limit)

    def get_submissions(self, subreddit, limit=100):
        return self.praw_api.get_subreddit(subreddit).get_hot(limit=limit)

    def get_submission(self, subreddit, submission, limit=100):
        submissions = self.get_submissions(subreddit, limit=None)
        data = filter(lambda item: item.id == submission, submissions)
        if data:
            return data[0]
