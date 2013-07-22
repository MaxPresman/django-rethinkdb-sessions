import unittest
import time
from django.contrib.sessions.backends.base import CreateError
from django.conf import settings

## on tests.. configure the settings manuall
settings.configure(
    SESSION_ENGINE='rdb_session.main'
)
####

from rethindb_session import main

class TestSequenceFunctions(unittest.TestCase):

  ##on each test run.. setup the connection
  def setUp(self):
    ''' init the storage engine '''
    self.rtdb_instance = main.SessionStore()

  def test_modify_and_keys(self):
    self.assertFalse(self.rtdb_instance.modified)
    self.rtdb_instance['test'] = 'test_me'
    self.assertTrue(self.rtdb_instance.modified)
    self.assertEquals(self.rtdb_instance['test'], 'test_me')

  """
    simple test to create a key
  """
  def test_save_and_delete(self):
    self.rtdb_instance["key"] = "value"
    self.rtdb_instance.save()

    ## test implicit
    self.assertTrue(self.rtdb_instance.exists(self.rtdb_instance.session_key))
    self.rtdb_instance.delete()
    self.assertFalse(self.rtdb_instance.exists(self.rtdb_instance.session_key))

  def test_save_and_delete_exp(self):
    self.rtdb_instance["key"] = "value"
    self.rtdb_instance.save()  

    ## test implicit
    self.assertTrue(self.rtdb_instance.exists(self.rtdb_instance.session_key))
    self.rtdb_instance.delete(self.rtdb_instance.session_key)
    self.assertFalse(self.rtdb_instance.exists(self.rtdb_instance.session_key))

  def test_save_twice(self):
    self.rtdb_instance["key"] = "value"
    self.rtdb_instance.save()

    self.rtdb_instance["key2"] = "value2"
    self.rtdb_instance.save()

  def test_flush(self):
    self.rtdb_instance['key'] = 'another_value'
    self.rtdb_instance.save()
    key = self.rtdb_instance.session_key
    self.rtdb_instance.flush()
    self.assertFalse(self.rtdb_instance.exists(key))

  def test_load(self):
    self.rtdb_instance['key'] = 'another_value'
    self.rtdb_instance.save()

    test_key = self.rtdb_instance.session_key

    self.rtdb_instance = main.SessionStore(test_key)
    
    self.assertIn("key",self.rtdb_instance)

  def test_upsert_false(self):
    self.rtdb_instance['key'] = 'another_value'
    self.rtdb_instance.save()

    self.assertRaises(CreateError,self.rtdb_instance.save,must_create=True)

  def test_expire(self):
    self.rtdb_instance.set_expiry(1)
    # Test if the expiry age is set correctly
    self.assertEquals(self.rtdb_instance.get_expiry_age(), 1)
    self.rtdb_instance['key'] = 'expiring_value'
    self.rtdb_instance.save()
    key = self.rtdb_instance.session_key
    self.assertEquals(self.rtdb_instance.exists(key), True)
    time.sleep(2)
    self.assertEquals(self.rtdb_instance.exists(key), False)

if __name__ == '__main__':
    unittest.main()