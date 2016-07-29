from setuptools import setup

setup(
    name='reddit-cli',
    version='0.1',
    description='Reddit command-line client',
    author="Serge B.",
    author_email="serge.bbak@gmail.com",
    url="https://github.com/mermoldy/reddit-cli",
    license="MIT",
    platforms="any",
    py_modules=['reddit'],
    include_package_data=True,
    install_requires=[
        'click==6.6',
    ],
    entry_points='''
        [console_scripts]
        reddit-cli=reddit.app:cli
    ''',
)