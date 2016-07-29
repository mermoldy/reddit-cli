# -*- coding: utf-8 -*-
import click
from datetime import datetime


def pretty_date(timestamp):

    diff = datetime.now() - datetime.fromtimestamp(timestamp)
    second_diff = diff.seconds
    day_diff = diff.days

    if day_diff < 0:
        return ''

    if day_diff == 0:
        if second_diff < 10:
            return "just now"
        if second_diff < 60:
            return str(second_diff) + " seconds ago"
        if second_diff < 120:
            return "a minute ago"
        if second_diff < 3600:
            return str(second_diff / 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff / 3600) + " hours ago"

    if day_diff < 7:
        return str(day_diff) + " days ago"

    if day_diff < 31:
        return str(day_diff / 7) + " weeks ago"


def echo(text, indent='', subsequent_indent='', fg='white'):
    if indent:
        text = click.wrap_text(text, width=78,
                               initial_indent=indent,
                               subsequent_indent=subsequent_indent or indent,
                               preserve_paragraphs=False)
    text = click.style(text, fg=fg)
    click.echo(text)


def _show_subreddit(subreddit):
    indent = '  | '
    data = subreddit
    data['description'] = data['public_description'].replace('\n', '')
    echo(u'{title}'.format(**data), fg='yellow')
    echo(u'subreddit: {url}'.format(**data), indent=indent, fg='cyan')
    echo(u'url: https://reddit.com{url}'.format(**data), indent=indent)
    echo(u'description: {description}'.format(**data), indent=indent,
         subsequent_indent=indent + (' ' * 13))
    echo(u'subscribers: {subscribers}'.format(**data), indent=indent)
    echo('')


def _show_submission(submission):
    data = submission.__dict__
    data['short_link'] = submission.short_link
    echo(u'# {title}'.format(**data), fg='yellow')
    echo(u'[id: {id}]'.format(**data), fg='cyan')
    echo(u'[short_link: {short_link}]\n'
         u'[op: {author.name}]\n'
         u'[comments: {num_comments}]\n'
         u'[up: {ups} down: {downs}]\n'.format(**data))


def _show_comment(comment, indent='', op=''):
    name = 'deleted' if not comment.author else comment.author.name
    score = comment.ups - comment.downs
    points = "{} point{}".format(score, ['s', ''][score == 1])
    time = pretty_date(comment.created_utc)

    echo(u"{}, {}, {}".format(name, points, time), indent=indent, fg='yellow')
    for p in comment.body.split('\n'):
        if p.lstrip().startswith('>'):
            echo(p, indent=indent + '  | ', fg="green")
        elif p.strip():
            echo(p, indent=indent + '  | ')
        else:
            echo('-', indent=indent + '  | ')
    echo('')

    indent += '  '
    for reply in comment.replies:
        if hasattr(reply, 'body'):
            _show_comment(reply, indent=indent, op=op)


def show_subreddits(subreddits):
    for subreddit in subreddits:
        _show_subreddit(subreddit)


def show_submissions(submissions):
    for submission in submissions:
        _show_submission(submission)


def show_discussion(submission):
    _show_submission(submission)
    for comment in submission.comments:
        if hasattr(comment, 'body'):
            _show_comment(comment)
