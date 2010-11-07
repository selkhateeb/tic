
import unittest
from tic.appengine.development.test import setup_local_datastore_service
from google.appengine.ext import db
class Crap(db.Model):
    name = db.StringProperty()
    
class TestTestCase(unittest.TestCase):
    def setUp(self):
        """
        TODOC
        """
         # Set up a new set of stubs for each test
        setup_local_datastore_service()
        
    def test_hi(self):
        """
        TODOC
        """
        c = Crap()
        c.name = "cool"
        key = c.put()
        print key
        self.assertTrue(True)
        self.assertEqual(c.name, "cool")

import random

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.seq = range(10)

    def test_shuffle(self):
        # make sure the shuffled sequence does not lose any elements
        random.shuffle(self.seq)
        self.seq.sort()
        self.assertEqual(self.seq, range(10))

        # should raise an exception for an immutable sequence
        self.assertRaises(TypeError, random.shuffle, (1,2,3))

    def test_choice(self):
        element = random.choice(self.seq)
        self.assertTrue(element in self.seq)

if __name__ == '__main__':
    unittest.main()