
REDDIT_API_URL = 'https://api.reddit.com'

USER_AGENT = 'reddit-cli-application'

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
