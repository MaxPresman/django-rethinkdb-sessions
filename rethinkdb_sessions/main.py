import rethinkdb
from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase,CreateError
from django.utils import timezone
import time

##push defaults
SESSION_RETHINK_HOST  = getattr(settings, 'SESSION_RETHINK_HOST', 'localhost')
SESSION_RETHINK_PORT  = getattr(settings, 'SESSION_RETHINK_PORT', '28015')
SESSION_RETHINK_DB    = getattr(settings, 'SESSION_RETHINK_DB', 'rdb_session')
SESSION_RETHINK_TABLE = getattr(settings, 'SESSION_RETHINK_TABLE', 'sessions')
SESSION_RETHINK_AUTH  = getattr(settings, 'SESSION_RETHINK_AUTH', '')
##


class SessionStore(SessionBase):
  def __init__(self, session_key=None):
    super(SessionStore, self).__init__(session_key)

    self.rtdb_table_handle = rethinkdb.table(SESSION_RETHINK_TABLE)

  def __establish_rethinkdb(self):
    return rethinkdb.connect(host=SESSION_RETHINK_HOST,
                              db=SESSION_RETHINK_DB,
                              auth_key=SESSION_RETHINK_AUTH
                            )

  def load(self):
    rethinkdb_conn     = self.__establish_rethinkdb_conn()

    reference_time     = time.mktime(timezone.now().timetuple())
    session_query      = self.rtdb_table_handle.get(self.session_key)
    session_result     = session_query.run(rethinkdb_conn)

    if not session_result or session_result["expire"] < reference_time:
      self.create()
      return {}

    ##restore the session
    return self.decode(session_result["data"])

  def exists(self,session_key):
    """
      A method to check if the session exists in the database
    """
    rethinkdb_handler = self.__establish_rethinkdb()
    key_found         = rethinkdb_handler.get(session_key).run(conn)
    reference_time    = time.mktime(timezone.now().timetuple())

    if not key_found or key_found["expire"] < reference_time:
      return False

    return True

  def create(self):
    """
      find a unique key in the system
    """
    while True:
      self._session_key = self._get_new_session_key()

      try:
        self.save(must_create=True)
      except CreateError:
        continue

      self.modified = True
      self._session_cache = {}
      return

  ## TO-DO must create.... and updates
  def save(self,must_create=False):
    """
    On session save, check if the key exists, if the key exists and must_create, we error out
    else, we encode the data and update the hash
    """
    rethinkdb_handler  = self.__establish_rethinkdb()

    ##if we are not in must_create, we can instruct rethink to update the key
    if must_create and self.exists(self._get_or_create_session_key()):
      raise CreateError

    if must_create:
      upsert_setting = False
    else:
      upsert_setting = True

    data_set = {
      "id":     self._get_or_create_session_key(),  ## this will be our pk
      "data":   self.encode(self._get_session(no_load=must_create)),  ## data storage
      "expire": time.mktime(self.get_expiry_date().timetuple())  ##keep track of when this entry is expiring
    }

    insert_result = rethinkdb_handler.insert(data_set,upsert=upsert_setting).run(conn)

    if "errors" in insert_result and insert_result["errors"]:
      raise CreateError

    #print insert_result

  def delete(self,session_key=None):
    """
      delete the supplied session_key or if that is not present, delete the global session_key
    """
    rethinkdb_handler  = self.__establish_rethinkdb()

    if session_key is None:
      if self.session_key is None:
        return

      session_key = self.session_key

    rethinkdb_handler.get(session_key).delete().run(conn)

  @classmethod
  def clear_expired(cls):
    """
      A method to remove all expired sessions
    """
    rethinkdb_handler  = self.__establish_rethinkdb()
    reference_time = time.mktime(self.timezone.now().timetuple())

    delete_request = rethinkdb.table(r_table).filter(rethinkdb.row["expire"] < reference_time).delete()
    delete_result  = delete_request.run(conn)

    ##print delete_result

