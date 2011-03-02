
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
        expected = """
dojo.provide("tic.web.cdp.cdp_tests.TCommand");
dojo.declare("tic.web.cdp.cdp_tests.TCommand", null, {
    constructor: function(args){
        dojo.safeMixin(this, args);
    },
    string:""
});

"""
        c = TCommand()
        self.assertEqual(expected, c.to_js())

    