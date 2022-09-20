from setuptools import setup

setup(
    name='scheduler',
    packages=['schedule'],
    entry_points = {
        'console_scripts': ['schedule=scheduler.cli:main'],
    },
)
