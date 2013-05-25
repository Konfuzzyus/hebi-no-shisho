import argparse
import sys

import app_admin
import app_user

def get_argument_parser():
    parser = argparse.ArgumentParser(prog='hebi-no-shisho',
                                     description='A simple database system for running a small public library.')
    parser.add_argument('subapp', 
                        action='store', 
                        nargs=1,
                        choices=['admin', 'user'],
                        help='Selects the subapplication hebi-no-shisho should run.')
    parser.add_argument('-v', '--version',
                        action='version', 
                        version='%(prog)s v0.0.0')
    return parser

def main():
    parser = get_argument_parser()
    options = parser.parse_args()
    if options.subapp.count('admin') != 0:
        app = app_admin.AppAdmin()
    else:
        app = app_user.AppUser()
    return app.run()

if __name__ == '__main__':
    sys.exit(main())
