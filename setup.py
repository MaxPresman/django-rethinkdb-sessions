from setuptools import setup
from rethinkdb_sessions import __version__

import os

packages = ['rethinkdb_sessions']


setup(
    name='django-rethinkdb-sessions',
    version=__version__,
    description= "rethinkdb backed sessions for django",
    long_description=open(os.path.join(os.path.dirname(__file__), "README.rst")).read() ,
    keywords='',
    author='Max Presman',
    author_email='max@presman.ca',
    url='http://github.com/maxpresman/django-rethinkdb-sessions',
    license='MIT',
    packages=packages,
    zip_safe=False,
    install_requires=['rethinkdb>=1.7.0'],
    include_package_data=True,
    test_suite="tests",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Programming Language :: Python :: Implementation :: CPython",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License"
    ],
)