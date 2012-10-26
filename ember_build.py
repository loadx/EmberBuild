import logging
import os
import re
import argparse
from ember import EmberBuild


def ember_project_type(path_to_app):
    """
    Check that path_to_app is a valid ember application.
    """
    # go back one folder from path_to_app
    app_path = os.path.normpath(os.path.join(os.path.dirname(__file__), path_to_app, '..'))

    if not os.path.isfile(os.path.join(app_path, 'index.html')) or not os.path.isfile(os.path.join(app_path, 'core.js')):
        raise argparse.ArgumentTypeError('project %s is not a valid Ember application' % path_to_app)

    return path_to_app


def build_type(build_type):
    """
    Check the build type is valid
    """
    if re.match(r'^(dev|live)$', build_type) is None:
        raise argparse.ArgumentTypeError('invalid build type supplied. May only be live or dev')

    return build_type


def verbose_type(verbosity):
    """
    Clamp the verbosity to a valid value
    """

    levels = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    verbosity = int(verbosity)

    if verbosity > len(levels) - 1:
        verbosity = levels[-1]
    elif verbosity < 0 or verbosity == None:
        verbosity = levels[0]
    else:
        verbosity = levels[verbosity]

    return verbosity

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('project', type=ember_project_type, help="Path to Ember project you want to compile")
    parser.add_argument('-t', '--type', type=build_type, metavar="dev", help="Change Ember build type (live or dev)", default=0)
    parser.add_argument('-v', type=verbose_type, metavar='', help="Change output verbosity (0-2) defaults to 0")
    args = parser.parse_args()

    if not args.v:
        args.v = logging.ERROR

    # enable logging to console setting the log level to the verbosity value
    logging.basicConfig(level=args.v, format='[%(levelname)s] %(message)s')

    EmberBuild(args.project, args.type).build_app()
