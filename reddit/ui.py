# -*- coding: utf-8 -*-
import click
import sys
from reddit import utils
from reddit.settings import STYLES


def _wait_input():
    """Wait user input."""

    if not click.utils.WIN:
        click.echo('[any]: next\t[q]: quit')

    if click.getchar() in ['q', u'q', b'q']:
        sys.exit(0)

    if not click.utils.WIN:
        click.echo('\033[F\033[K')


def _show_subreddit(data):
    data['about'] = data['public_description'].replace('\n', '')

    echo(u'{title}'.format(**data), **STYLES['header'])
    echo(u'subreddit: {url}'.format(**data), **STYLES['signature'])
    echo(u'url: https://reddit.com{url}'.format(**data), **STYLES['regular'])
    echo(u'about: {about}'.format(**data), **STYLES['about'])
    echo(u'subscribers: {subscribers}'.format(**data), **STYLES['regular'])
    click.echo()


def _show_submission(data):
    score = data.get('ups', 0) - data.get('downs', 0)
    data['points'] = utils.pluralize(score, 'point')
    data['time'] = utils.pretty_date(data['created_utc'])

    echo(u'{title}, {url}'.format(**data),  **STYLES['header'])
    echo(u'submitted {time} by {author}'.format(**data), **STYLES['author'])
    echo(u'submission id: {id}'.format(**data), **STYLES['regular'])
    echo(u'link: https://redd.it/{id}'.format(**data), **STYLES['regular'])
    echo(u'comments: {num_comments}'.format(**data), **STYLES['regular'])
    click.echo()


def _show_comment(comment, prepend=''):
    score = comment.get('ups', 0) - comment.get('downs', 0)
    points = utils.pluralize(score, 'point')
    name = comment.get('author', '[deleted]')
    time = utils.pretty_date(comment.get('created_utc', 0))
    echo(u"{}, {}, {}".format(name, points, time),
         prepend=prepend, **STYLES['comment'])
    for p in comment['body'].split('\n'):
        if p.lstrip().startswith('>') or \
           p.lstrip().startswith('&gt;'):
            echo(p, prepend=prepend, **STYLES['quote'])
        else:
            echo(p if p.strip() else '-', prepend=prepend, **STYLES['regular'])
    click.echo()


def _show_comment_tree(comment, prepend='  '):

    body = utils.recursive_get(comment, 'data.body') or []
    title = utils.recursive_get(comment, 'data.title') or []
    replies = utils.recursive_get(comment, "data.replies.data.children") or []

    if body:
        _show_comment(comment['data'], prepend=prepend)
        _wait_input()

        for reply in replies:
            _show_comment_tree(reply, prepend=prepend + '  ')
    elif title:
        return _show_submission(comment['data'])


def echo(text='', prepend='', initial_indent='', subsequent_indent='', fg=''):
    window_width, _ = click.get_terminal_size()
    wrapped = click.wrap_text(text,
                              width=window_width - len(initial_indent),
                              initial_indent=prepend + initial_indent,
                              subsequent_indent=prepend + subsequent_indent,
                              preserve_paragraphs=False)
    click.secho(wrapped, fg=fg)


def show_subreddits(subreddits):
    for subreddit in subreddits:
        _show_subreddit(subreddit)
        _wait_input()


def show_submissions(submissions):
    for submission in submissions:
        _show_submission(submission)
        _wait_input()


def show_comments(comments):
    for comment in comments:
        _show_comment_tree(comment)
