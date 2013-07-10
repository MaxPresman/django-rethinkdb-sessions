from setuptools import setup

packages = ['rethindb_session']


setup(
    name='django-rethinkdb-sessions',
    version="0.0.1",
    description= "123",
    long_description="1234",
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
        "Programming Language :: Python :: 2",
        "Framework :: Django",
    ],
)