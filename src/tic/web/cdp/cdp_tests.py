
import unittest
from tic.web import cdp
from tic.conf import settings

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
        settings.JAVASCRIPT_TOOLKIT= 'dojo'
        c = TCommand()
        self.assertEqual(expected, c.to_js())

    def test_it_should_generate_closure_class_definition(self):
        expected = """
goog.provide("tic.web.cdp.cdp_tests.TCommand");
tic.web.cdp.cdp_tests.TCommand = function(args) {
    goog.mixin(this, args);
};
tic.web.cdp.cdp_tests.TCommand.prototype.string="";


"""
        settings.JAVASCRIPT_TOOLKIT= 'closure'
        c = TCommand()
        self.assertEqual(expected, c.to_js())
