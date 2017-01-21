from __future__ import print_function

import click
from macchat.client import ChatClient


def main():
    client = ChatClient()

    client.ui.cli.output.erase_screen()
    client.ui.cli.output.cursor_goto(0, 0)
    client.ui.cli.output.flush()
    width = client.ui.cli.output.get_size().columns
    print('\n' + click.style(('\n'.join((i.center(width) for i in (
        "                                                   ",
        "                                 _             _   ",
        "                                ( )           ( )_ ",
        "  ___ ___     _ _    ___    ___ | |__     _ _ | ,_)",
        "/' _ ` _ `\ /'_` ) /'___) /'___)|  _ `\ /'_` )| |  ",
        "| ( ) ( ) |( (_| |( (___ ( (___ | | | |( (_| || |_ ",
        "(_) (_) (_)`\__,_)`\____)`\____)(_) (_)`\__,_)`\__)",
        "                                                   ",
        "                                                   ",
    )))), fg='white', bold=True))
    client.ui.cli.output.cursor_goto(1024, 0)

    client.run()


if __name__ == '__main__':
    main()
