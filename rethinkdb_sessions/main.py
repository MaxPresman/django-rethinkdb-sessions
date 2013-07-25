import rethinkdb
from django.conf import settings
from django.contrib.sessions.backends.base import SessionBase,CreateError
from django.utils import timezone
import time

##push defaults
SESSION_RETHINK_HOST  = getattr(settings, 'SESSION_RETHINK_HOST', 'localhost')
SESSION_RETHINK_PORT  = getattr(settings, 'SESSION_RETHINK_PORT', '28015')
SESSION_RETHINK_DB    = getattr(settings, 'SESSION_RETHINK_DB', 'test')
SESSION_RETHINK_TABLE = getattr(settings, 'SESSION_RETHINK_TABLE', 'django_sessions')
SESSION_RETHINK_AUTH  = getattr(settings, 'SESSION_RETHINK_AUTH', '')
##


class SessionStore(SessionBase):
  def __init__(self, session_key=None):
    super(SessionStore, self).__init__(session_key)

    self.table_handle = rethinkdb.table(SESSION_RETHINK_TABLE)

  @classmethod
  def __establish_rethinkdb(self):
    connection_handler = rethinkdb.connect(host=SESSION_RETHINK_HOST,
                              db=SESSION_RETHINK_DB,
                              auth_key=SESSION_RETHINK_AUTH
                            )


    ##create the requested db if it does not exist
    if SESSION_RETHINK_DB not in rethinkdb.db_list().run(connection_handler):
      rethinkdb.db_create(SESSION_RETHINK_DB).run(connection_handler)

    ##create the required table if it does not exist
    if SESSION_RETHINK_TABLE not in rethinkdb.db(SESSION_RETHINK_DB).table_list().run(connection_handler):
      rethinkdb.db(SESSION_RETHINK_DB).table_create(SESSION_RETHINK_TABLE).run(connection_handler)

    return connection_handler

  def load(self):
    rethinkdb_conn     = self.__establish_rethinkdb()

    reference_time     = time.mktime(timezone.now().timetuple())
    session_query      = self.table_handle.get(self.session_key)
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
    key_found         = self.table_handle.get(session_key).run(rethinkdb_handler)
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

    insert_result = self.table_handle.insert(data_set,upsert=upsert_setting).run(rethinkdb_handler)

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

    self.table_handle.get(session_key).delete().run(rethinkdb_handler)

  @classmethod
  def clear_expired(cls):
    """
      A method to remove all expired sessions
    """
    rethinkdb_handler  = cls.__establish_rethinkdb()
    reference_time = time.mktime(timezone.now().timetuple())

    delete_request = rethinkdb.table(SESSION_RETHINK_TABLE).filter(rethinkdb.row["expire"] < reference_time).delete()
    delete_result  = delete_request.run(rethinkdb_handler)

    ##print delete_result

