
import unittest
from tic.web import cdp

class TCommand(cdp.Command):
    list = cdp.ListProperty(str)
    string = cdp.StringProperty()
    datetime = cdp.DateTimeProperty()

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
    list:null,
    string:"",
    datetime:null
});

"""
        c = TCommand('dojo')
        self.assertEqual(expected, c.to_js())

    def test_it_should_generate_closure_class_definition(self):
        expected = """
goog.provide("tic.web.cdp.cdp_tests.TCommand");
tic.web.cdp.cdp_tests.TCommand = function(args) {
    goog.mixin(this, args);
};
tic.web.cdp.cdp_tests.TCommand.prototype.list=null;
tic.web.cdp.cdp_tests.TCommand.prototype.string="";
tic.web.cdp.cdp_tests.TCommand.prototype.datetime=null;


"""
        c = TCommand('closure')
        self.assertEqual(expected, c.to_js())

