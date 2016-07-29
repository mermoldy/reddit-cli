#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
import utils
from api import Reddit

@click.command()
@click.option('--search', default=None, help='Search subreddits')
@click.option('--subreddit', default=None, help='Show subreddit')
@click.option('--submission', default=None, help='Show comments')
@click.option('--limit', default=10, help='Limit display results, '
                                          '10 by default')
def cli(**kwargs):

    api = Reddit()

    if kwargs['search']:
        subreddits = api.search_subreddits(query=kwargs['search'],
                                           limit=kwargs['limit'])
        utils.show_subreddits(subreddits)

    if kwargs['subreddit']:
        submissions = api.get_submissions(subreddit=['subreddit'],
                                          limit=kwargs['limit'])
        utils.show_submissions(submissions)

    if kwargs['submission']:
        submission = api.get_submission(subreddit=kwargs['subreddit'],
                                        submission=kwargs['submission'])
        utils.show_discussion(submission)


if __name__ == '__main__':
    cli()
