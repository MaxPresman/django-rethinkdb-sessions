import rethinkdb
from django.contrib.sessions.backends.base import SessionBase
import time

##create a rethinkdb backend
conn    = rethinkdb.connect(db='rdb_session')
r_table = "sessions"

##temp
from django.conf import settings
settings.configure()
###


class SessionStore(SessionBase):
  def __init__(self, session_key=None):
    super(SessionStore, self).__init__(session_key)

  def load(self):
    assert(1 == 2)

  def exists(self,session_key):
    """
      A method to check if the session exists in the database
    """
    return (rethinkdb.table(r_table).get(session_key).run(conn)) is not None

  def create(self):
    assert(1 == 2)

  def save(self,must_create=False):
    """
    On session save, check if the key exists, if the key exists and must_create, we error out
    else, we encode the data and update the hash
    """

    data_set = {
      "id":     self._get_or_create_session_key(),  ## this will be our pk
      "data":   self.encode(self._get_session(no_load=must_create)),  ## data storage
      "expire": time.mktime(self.get_expiry_date().timetuple())  ##keep track of when this entry is expiring
    }

    rethinkdb.table(r_table).insert(data_set).run(conn)

  def delete(self,session_key=None):
    assert(1 == 2)

  @classmethod
  def clear_expired(cls):
    """
      A method to remove all expired sessions
    """
    reference_time = time.mktime(self.timezone.now().timetuple())

    rethinkdb.table(r_table).filter(rethinkdb.row["expire"] < reference_time).delete().run(conn)