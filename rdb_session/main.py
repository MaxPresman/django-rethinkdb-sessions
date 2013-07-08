import rethinkdb
from django.contrib.sessions.backends.base import SessionBase

##create a rethinkdb backend
conn = rethinkdb.connect(db='rdb_session')

class SessionStore(SessionBase):
  def __init__(self, session_key=None):
    super(SessionStore, self).__init__(session_key)

