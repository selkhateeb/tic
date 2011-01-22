from tic.admin.api import IAdminCommandProvider
from tic.core import Component, implements

class TestMigrationCommand(Component):
    implements(IAdminCommandProvider)

    def get_admin_commands(self):
        """

        """
	#(command, args, help, complete, execute)
        command = "migrate"
        args = None
        help = """test`ing API."""

        complete = None
        execute = self._execute

        return ((command, args, help, complete, execute), )

    def _execute(self, args=None):
        print "sweet"
        #set up datastore
        from tic.appengine.development.test import setup_local_datastore_service
        setup_local_datastore_service()

        from google.appengine.api import datastore
        from google.appengine.api import datastore_errors

#        m = models.Make()
#        m.name = "asdfghjk"
#        m.put()
#
#
#        a = datastore.Query('Make').Get(1)
#        print dir(a[0])
#        print a[0].name


def get_entities(keys): 
    rpc = datastore.GetRpcFromKwargs({}) 
    keys, multiple = datastore.NormalizeAndTypeCheckKeys(keys) 
    entities = None 
    try: 
        entities = datastore.Get(keys, rpc=rpc) 
    except datastore_errors.EntityNotFoundError: 
        assert not multiple 
    return entities 

def put_entities(entities):
    rpc = datastore.GetRpcFromKwargs({})
    keys = datastore.Put(entities, rpc=rpc)
    return keys


class Migrate(object):
#    model = models.Car
    def list_date(self, value):
        """
        value: old value
        returns: new value
        """
        return value

    def run(self):
        """Runs the schema
        """

