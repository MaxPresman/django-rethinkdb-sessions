django-rethinkdb-sessions 
=========================

.. image:: https://travis-ci.org/MaxPresman/django-rethinkdb-sessions.png
   :target: https://travis-ci.org/MaxPresman/django-rethinkdb-sessions


Django session backend for rethinkdb.

------------
Installation
------------

1. install the package by pypi
    pip install django-rethinkdb-sessions
2. in django settings, switch the session over to rethinkdb-sessions
    SESSION_ENGINE = 'rethinkdb_sessions.main'
3. configure the following settings to adjust the rethinkdb enviorment
    - "SESSION_RETHINK_HOST" -- host that rethinkdb is currently running on.
    - "SESSION_RETHINK_PORT" -- current rethinkdb port
    - "SESSION_RETHINK_DB"   -- rethinkdb database
    - "SESSION_RETHINK_TABLE" -- rethinkdb table
    - "SESSION_RETHINK_AUTH"  -- rethinkdb auth key (if exists)

-------------
Running Tests
-------------

Tests are included, invoke tests by running
    "python tests/tests.py"

