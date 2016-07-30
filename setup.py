from setuptools import setup
from setuptools import find_packages


if __name__ == '__main__':

    setup(
        name='reddit-cli',
        version='0.1',
        description='Reddit command-line client',
        author='Serge B.',
        author_email='serge.bbak@gmail.com',
        url='https://github.com/mermoldy/reddit-cli',
        license='MIT',
        platforms='any',
        packages=find_packages(),
        include_package_data=True,
        install_requires=[
            'click==6.6',
            'requests==2.10.0',
        ],
        entry_points='''
            [console_scripts]
            reddit-cli=reddit.app:cli
        ''',
    )
