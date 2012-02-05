#!/usr/bin/env python

if __name__ == '__main__':
    import sys
    import os
    import logging
    import argparse
    from tic.development.tictac import CommandLineApplication, \
        subcommands, Configuration
    from tic.development.tictac.argparsers import ApplicationConfigurationException
    
    

    logging.getLogger().setLevel(logging.DEBUG)
    logging.basicConfig(format=('%(message)s'), level=logging.INFO)


    parser = argparse.ArgumentParser(
        epilog="See '%(prog)s COMMAND --help' for more information on a specific command.",
        )

    config = Configuration(config_file='.tic/config')
#    try:
    if True:
        try:
            sys.path = config.get_project_deps() + sys.path

        except ApplicationConfigurationException:
            #allow for init command to complete
            pass #we dont care. Since the user is not in a tic project
        
        app = CommandLineApplication(parser=parser, config=config)
    
        for command in subcommands.__all__:
            c = getattr(subcommands, command)
            app.add_command(c)
        
        app.run()

#    except Exception, e:
#        logging.error(e.message)
        #import traceback
        #traceback.print_exc()
