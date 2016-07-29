# -*- coding: utf-8 -*-
import click
import fcntl
import termios
import struct
from datetime import datetime


try:
    data = fcntl.ioctl(0, termios.TIOCGWINSZ, struct.pack('HHHH', 0, 0, 0, 0))
    _, WINDOW_WIDTH, _, _ = struct.unpack('HHHH', data)
    if 0 > WINDOW_WIDTH > 200:
        raise Exception
except Exception as e:
    WINDOW_WIDTH = 80


STYLES = {
    'header': {
        'initial_indent': '# ',
        'subsequent_indent': '  ',
        'fg': 'blue'
    },
    'regular': {
        'initial_indent': '  | ',
        'subsequent_indent': '  | '
    },
    'signature': {
        'initial_indent': '  | ',
        'fg': 'cyan'
    },
    'author': {
        'initial_indent': '  | ',
        'fg': 'yellow'
    },
    'comment': {
        'initial_indent': '',
        'fg': 'yellow'
    },
    'quote': {
        'initial_indent': '  | ',
        'fg': 'green'
    },
    'about': {
        'initial_indent': '  | ',
        'subsequent_indent': '  | ' + ' ' * 7,
    },
}


def _pluralize(digit, text):
    return "{} {}{}".format(digit, text, 's' if digit != 1 else '')


def _pretty_date(timestamp):

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


def _show_subreddit(data):
    data['about'] = data['public_description'].replace('\n', '')

    echo(u'{title}'.format(**data), **STYLES['header'])
    echo(u'subreddit: {url}'.format(**data), **STYLES['signature'])
    echo(u'url: https://reddit.com{url}'.format(**data), **STYLES['regular'])
    echo(u'about: {about}'.format(**data), **STYLES['about'])
    echo(u'subscribers: {subscribers}'.format(**data), **STYLES['regular'])
    echo()


def _show_submission(data):
    score = data.get('ups', 0) - data.get('downs', 0)
    data['points'] = _pluralize(score, 'point')
    data['time'] = _pretty_date(data['created_utc'])

    echo(u'{title}, {url}'.format(**data),  **STYLES['header'])
    echo(u'submitted {time} by {author}'.format(**data), **STYLES['author'])
    echo(u'id {id}'.format(**data), **STYLES['regular'])
    echo(u'link: https://redd.it/{id}'.format(**data), **STYLES['regular'])
    echo(u'comments: {num_comments}'.format(**data), **STYLES['regular'])
    echo()


def _show_comment(comment, prepend=''):
    score = comment.get('ups', 0) - comment.get('downs', 0)
    points = _pluralize(score, 'point')
    name = comment.get('author', '') or 'deleted'
    time = _pretty_date(comment.get('created_utc', 0))
    echo(u"{}, {}, {}".format(name, points, time),
         prepend=prepend, **STYLES['comment'])
    for p in comment['body'].split('\n'):
        if p.lstrip().startswith('>'):
            echo(p, prepend=prepend, **STYLES['quote'])
        else:
            echo(p if p.strip() else '-', prepend=prepend, **STYLES['regular'])
    echo()


def _show_comment_tree(comment, prepend='  '):
    data = comment.get('data', None)
    if not data:
        return

    if 'body' in data:
        _show_comment(data, prepend=prepend)
    elif 'title' in data:
        return _show_submission(data)

    if 'replies' in data:
        for reply in data['replies']['data']['children']:
            _show_comment_tree(reply, prepend=prepend + '  ')


def echo(text='', prepend='', initial_indent='', subsequent_indent='', fg=''):
    wrapped = click.wrap_text(text,
                              width=WINDOW_WIDTH - len(initial_indent),
                              initial_indent=prepend + initial_indent,
                              subsequent_indent=prepend + subsequent_indent,
                              preserve_paragraphs=False)
    click.secho(wrapped, fg=fg)


def show_subreddits(subreddits):
    for subreddit in subreddits:
        _show_subreddit(subreddit)


def show_submissions(submissions):
    for submission in submissions:
        _show_submission(submission)


def show_comments(comments):
    for comment in comments:
        _show_comment_tree(comment)

