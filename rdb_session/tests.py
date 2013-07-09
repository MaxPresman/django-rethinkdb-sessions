import unittest
import main

class TestSequenceFunctions(unittest.TestCase):

  """
    simple test to create a key
  """
  def test_save_key(self):
    rtdb_instance = main.SessionStore()
    rtdb_instance["hi"] = "max2"

    print rtdb_instance.save()

    print rtdb_instance["hi"]

if __name__ == '__main__':
    unittest.main()