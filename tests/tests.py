import unittest
from rethindb_session import main
from django.contrib.sessions.backends.base import CreateError

'''
  Tests were inspired by django-redis-session at
  https://github.com/martinrusev/django-redis-sessions/blob/master/tests/tests.py
''' 

class TestSequenceFunctions(unittest.TestCase):

  def test_modify_and_keys(self):
    rtdb_instance = main.SessionStore()

    self.assertFalse(rtdb_instance.modified)
    rtdb_instance['test'] = 'test_me'
    self.assertTrue(rtdb_instance.modified)
    self.assertEquals(rtdb_instance['test'], 'test_me')

  """
    simple test to create a key
  """
  def test_save_and_delete(self):
    rtdb_instance = main.SessionStore()
    rtdb_instance["key"] = "value"
    rtdb_instance.save()

    ## test implicit
    self.assertTrue(rtdb_instance.exists(rtdb_instance.session_key))
    rtdb_instance.delete()
    self.assertFalse(rtdb_instance.exists(rtdb_instance.session_key))

  def test_save_and_delete_exp(self):
    rtdb_instance = main.SessionStore()
    rtdb_instance["key"] = "value"
    rtdb_instance.save()  

    ## test implicit
    self.assertTrue(rtdb_instance.exists(rtdb_instance.session_key))
    rtdb_instance.delete(rtdb_instance.session_key)
    self.assertFalse(rtdb_instance.exists(rtdb_instance.session_key))

  def test_save_twice(self):
    rtdb_instance = main.SessionStore()
    rtdb_instance["key"] = "value"
    rtdb_instance.save()

    rtdb_instance["key2"] = "value2"
    rtdb_instance.save()

  def test_flush(self):
    rtdb_instance = main.SessionStore()

    rtdb_instance['key'] = 'another_value'
    rtdb_instance.save()
    key = rtdb_instance.session_key
    rtdb_instance.flush()
    self.assertFalse(rtdb_instance.exists(key))

  def test_load(self):
    rtdb_instance = main.SessionStore()
    rtdb_instance['key'] = 'another_value'
    rtdb_instance.save()

    test_key = rtdb_instance.session_key

    rtdb_instance = main.SessionStore(test_key)
    
    self.assertIn("key",rtdb_instance)

  def test_upsert_false(self):
    rtdb_instance = main.SessionStore()
    rtdb_instance['key'] = 'another_value'
    rtdb_instance.save()

    self.assertRaises(CreateError,rtdb_instance.save,must_create=True)

if __name__ == '__main__':
    unittest.main()