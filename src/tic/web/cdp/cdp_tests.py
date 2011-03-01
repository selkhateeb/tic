
import unittest
from tic.web import cdp

class TCommand(cdp.Command):
    string = cdp.StringProperty()

class CdpTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_it_should_generate_dojo_class_definition(self):
        c = TCommand()
        print c.to_js()
        self.assertTrue(False)

    