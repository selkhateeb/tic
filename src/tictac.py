#!/usr/bin/env python


if __name__ == '__main__':

    import argparse
    from tic.development.tictac import CommandLineApplication, subcommands

    parser = argparse.ArgumentParser(
        epilog="See '%(prog)s COMMAND --help' for more information on a specific command.",
        )
    
    app = CommandLineApplication(parser=parser)
    
    
    for command in subcommands.__all__:
        c = getattr(subcommands, command)
        app.add_command(c)
        
    app.run()

