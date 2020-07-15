import argparse
from .version import __version__


def get_args():
    """
    Get CLI arguments
    """

    _description = 'A simple, configurable and automatic youtube-dl wrapper for\
    updating your local library.'
    _usage = '%(prog)s [add | remove | list | update | edit] [URL ..] [OPTION ..]\nRun \"aytld COMMAND --help\" for more information.'
    _conflict_handler = 'resolve'

    parser = argparse.ArgumentParser(
        description=_description,
        conflict_handler=_conflict_handler,
        usage=_usage)

    subs = parser.add_subparsers()
    subs.required = True
    subs.dest = "COMMANDS"

    #
    add_parser = subs.add_parser('add')
    add_parser.add_argument(
        'add', nargs='+',
        help="add one or more channel (urls) as music source")

    #
    remove_parser = subs.add_parser('remove')
    remove_parser.add_argument('remove', nargs='+',
                               help="remove a channel from tracking")
    #
    list_parser = subs.add_parser('list')
    list_parser.add_argument('list', action='store_true',
                             help="list all channels")

    #
    edit_parser = subs.add_parser('edit')
    edit_parser.add_argument(
        'edit', action='store_true', help='edit config file')

    #
    update_parser = subs.add_parser('update')
    update_parser.add_argument('update', nargs='*',
                               help="download all new music from every added channels,\
                or all new music from the specified channel")

    update_parser.add_argument("--include-old", action='store_true',
                               help="download old videos, else only music posted\
                                after the current date will be download")
    update_parser.add_argument("--force", action='store_true',
                               help="force download of (preferably one) url,\
                                       even if does not look like music")
    update_parser.add_argument("-p", "--playing", action='store_true',
                               help="download the video currently playing\
                                        on your browser (chrome/youtube only)")

    parser.add_argument('--version', action='version',
                        version='%(prog)s {0}'.format(__version__))
    args = vars(parser.parse_args())
    return args
