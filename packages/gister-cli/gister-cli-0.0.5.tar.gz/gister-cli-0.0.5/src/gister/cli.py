"""Cli entrypoint
"""
import argparse
from pathlib import Path
import argparse
import logging
import sys
import signal

import gister.runner
import gister.version
import gister.steps.gitenv
import gister.builder.command
import gister.log.logger
from gister.utils.text import wrap

log = logging.getLogger(__name__)


def get_parser():
    parser = argparse.ArgumentParser(allow_abbrev=True, prog='gister',
                                     description='Command line interface for the gister package',
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('--envm', help=wrap("Name of the enviroment. Should define user config " "inside ~/.gister"))
    parser.add_argument('--log', '--loglevel', dest='log_level', type=int,
                        default=None,
                        help=wrap(
                            'Integer log level. Defaults to 25 (NOTIFY).\n'
                            '10=DEBUG \n'
                            '20=INFO\n'
                            '25=NOTIFY\n'
                            '30=WARNING\n'
                            '40=ERROR\n'
                            '50=CRITICAL\n'
                            'Log Level < 10 gives full traceback on errors.'))
    parser.add_argument('--logpath', dest='log_path',
                        help=wrap(
                            'Log-file path. Append log output to this path.'))
    parser.add_argument('--version', action='version',
                        help='Version number', version=f'{gister.version.get_version()}')

    gister.builder.command.command_builder(parser)

    return parser


def get_args(args):
    # subparsers = parser.add_subparsers(help='Subcommands')
    # Parse all command line arguments
    return get_parser().parse_args(args)


""" Main
"""


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    parsed_args = get_args(args)

    try:
        gister.log.logger.set_root_logger(log_level=parsed_args.log_level, log_path=parsed_args.log_path)
        return gister.runner.main(
            git_env_change=parsed_args.env,
        )
    except KeyboardInterrupt:
        sys.stdout.write("\n")
        return 128 + signal.SIGINT
    except Exception as e:
        sys.stderr.write("\n")
        sys.stderr.write(f"\033[91m{type(e).__name__}: {str(e)}\033[0;0m")
        sys.stderr.write("\n")
        return 255
