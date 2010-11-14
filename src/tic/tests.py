from tic.env import Environment
from tic import core
import unittest
#################
## tic.core
# Setup classes

class ITest(core.Interface):
    """
    Interface class used for setting up component testing
    """
    def testing(self):
        """
        testing method used as a segnityre for this class in the testing
        """

class TestNotLoadableComponant():
    """
    Dummy component that should not be loaded
    """

class TestErrorOnInitComponant():
    """
    Dummy component that raises an exception when initialized
    """
    def __init__(self):
        """
        TODOC
        """
        raise Exception()
    
class TestComponant(core.Component):
    core.implements(ITest)
    
    def testing(self):
        """
        Testing implementation
        """
        return "testing"
    
class TestDriver(core.Component):
    i_tests = core.ExtensionPoint(ITest)
    
    def drive(self):
        """
        goes through all ITest implementation and run the testing method
        """
        for test in self.i_tests:
            pass
        
class TestComponentManager(unittest.TestCase):
    
    def setUp(self):
        """
        sets up the environment
        """
        self.component_manager = core.ComponentManager()
        
        #load our test component
        self.component = TestDriver(self.component_manager)
        
    
    def test_component_loading(self):
        """
        Tests the component manager
        """
#        UA 7493
        # we only have one component
        self.assertEqual(1, len(self.component_manager.components))
        self.assertTrue(TestDriver in self.component_manager)
        
        # make sure it is the right one!
        self.assertEqual(self.component, self.component_manager[TestDriver])
        
        def test_not_component_exception():
            """
            Raises exception when called
            """
            self.component_manager[TestNotLoadableComponant]
        self.assertRaises(core.TicError, test_not_component_exception)
        
        def test_exception_on_init():
            """
            TODOC
            """
            self.component_manager[TestErrorOnInitComponant]
        self.assertRaises(core.TicError, test_exception_on_init)

    def test_enable_disable_components(self):
        """
        TEsts the enabling and disabling the components
        """
        self.assertTrue(self.component_manager.is_enabled(TestDriver))

        #lets disable it
        self.component_manager.disable_component(self.component)
        self.assertFalse(self.component_manager.is_enabled(TestDriver))
        
        # re-enabling it for other tests
        self.component_manager.enabled[TestDriver] = True
        self.assertTrue(self.component_manager.is_enabled(TestDriver))
        
    def test_component_execution(self):
        """
        tests components loading and execution
        """
        
        # we should only have one extension point
        self.assertEqual(1, len(self.component.i_tests))
        
        # and it should run 
        for t in self.component.i_tests:
            self.assertEqual("testing", t.testing())
            
    