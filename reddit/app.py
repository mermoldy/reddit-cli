#!/usr/bin/env python
# -*- coding: utf-8 -*-
import click
from reddit import api
from reddit import ui


class RedditCLI(click.Group):
    """This class accepts a prefix for a command. If there were a
    command called push, it would accept pus as an
    alias(so long as it was unique).
    """

    def get_command(self, ctx, cmd_name):
        rv = click.Group.get_command(self, ctx, cmd_name)
        if rv is not None:
            return rv
        matches = [x for x in self.list_commands(ctx)
                   if x.startswith(cmd_name)]
        if not matches:
            return None
        elif len(matches) == 1:
            return click.Group.get_command(self, ctx, matches[0])
        ctx.fail('Too many matches: %s' % ', '.join(sorted(matches)))


@click.command(cls=RedditCLI)
def cli():
    """Reddit command-line client"""


@cli.command()
@click.argument('search_query', metavar='<search_query>')
@click.option('--limit', '-l', default=20, help='Limit search results '
              '(default: 20)')
def search(search_query, **kwargs):
    """Search subreddit for the given query"""

    subreddits = api.search_subreddits(query=search_query, **kwargs)
    ui.show_subreddits(subreddits)


@cli.command()
@click.argument('name', metavar='<name>')
@click.option('--limit', '-l', default=10, help='Limit articles count'
              '(default: 10)')
@click.option('--order', '-o', default='hot', help='Choices: hot new rising'
              'top controversial (default: hot)')
def subreddit(name, **kwargs):
    """Display subreddit submissions"""

    submissions = api.get_submissions(subreddit_name=name, **kwargs)
    ui.show_submissions(submissions)


@cli.command()
@click.argument('submission_id', metavar='<submission_id>')
def submission(submission_id, **kwargs):
    """Display comments of reddit submission"""

    comments = api.get_comments(submission_id=submission_id)
    ui.show_comments(comments)


if __name__ == '__main__':
    cli()
