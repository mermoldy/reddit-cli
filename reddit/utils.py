# -*- coding: utf-8 -*-
import struct
from platform import platform
from datetime import datetime

PLATFORM = platform().lower()


def _get_terminal_size_nix():
    import fcntl
    import termios
    data = fcntl.ioctl(0, termios.TIOCGWINSZ, struct.pack('HHHH', 0, 0, 0, 0))
    height, width, _, _ = struct.unpack('HHHH', data)
    return width, height


def _get_terminal_size_windows():
    from ctypes import windll, create_string_buffer
    h = windll.kernel32.GetStdHandle(-12)
    csbi = create_string_buffer(22)
    res = windll.kernel32.GetConsoleScreenBufferInfo(h, csbi)
    if res:
        (bufx, bufy, curx, cury, wattr,
         left, top, right, bottom,
         maxx, maxy) = struct.unpack("hhhhHhhhhhh", csbi.raw)
        width = right - left + 1
        height = bottom - top + 1
        return width, height


def get_terminal_width():
    try:
        if 'windows' in PLATFORM:
            return _get_terminal_size_windows()[0]
        elif any(item in PLATFORM for item in ['linux', 'darwin']):
            return _get_terminal_size_nix()[0]
    except:
        pass


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
