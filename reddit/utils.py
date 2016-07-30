# -*- coding: utf-8 -*-
from datetime import datetime


def recursive_get(d, key):
    if type(d) != dict:
        return
    head, _, tail = key.partition('.')
    h_value = d.get(head, '')
    if tail and type(h_value) == dict:
        return recursive_get(h_value, tail)
    if not tail:
        return h_value


def pluralize(digit, text):
    return "{} {}{}".format(digit, text, 's' if digit != 1 else '')


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
            return str(second_diff // 60) + " minutes ago"
        if second_diff < 7200:
            return "an hour ago"
        if second_diff < 86400:
            return str(second_diff // 3600) + " hours ago"

    if day_diff < 7:
        return str(day_diff) + " days ago"

    if day_diff < 31:
        return str(day_diff // 7) + " weeks ago"
