#!/usr/bin/env python


if __name__ == '__main__':
    import sys
    import logging
    import argparse
    from tic.development.tictac import CommandLineApplication, subcommands, Configuration

    logging.getLogger().setLevel(logging.DEBUG)

    parser = argparse.ArgumentParser(
        epilog="See '%(prog)s COMMAND --help' for more information on a specific command.",
        )

    config = Configuration(config_file='.tic/config')
#    try:
    if True:
        sys.path.insert(1,config.get_project_sources_path())
        app = CommandLineApplication(parser=parser, config=config)
    
        for command in subcommands.__all__:
            c = getattr(subcommands, command)
            app.add_command(c)
        
        app.run()

#    except Exception, e:
#        logging.error(e.message)
        #import traceback
        #traceback.print_exc()
