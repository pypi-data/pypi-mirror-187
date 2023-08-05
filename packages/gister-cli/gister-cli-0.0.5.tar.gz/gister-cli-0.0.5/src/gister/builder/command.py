""" Commnad builder"""
from gister.log.print import PrintLog


def git_env(parser):
    subparser = parser.add_subparsers(help="Sub-commands")
    subparser_a = subparser.add_parser(
        'gitenv', help="Change git config environment")
    subparser_a.add_argument(
        '--env', help="Enviroment name", required=False)
    # subparser_a.add_argument('count', action='store', type=int)


switcher = {
    "gitenv": git_env,
}

""" Command builder
    Iterate hover switcher to initialize subcommands.
    To create new subcommands must define initializar function
    and integrate in switcher variable
"""


def command_builder(parser=None):
    # TODO: Validate subparser value and delete command argument
    for command in switcher:
        if switcher.get(command) is None:
            PrintLog.error("Command " f"{command} not found!")
            break
        func_exec = switcher.get(command)
        func_exec(parser)
