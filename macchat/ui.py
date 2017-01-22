from __future__ import unicode_literals
from __future__ import print_function

import re
import click
import textwrap
import itertools

from prompt_toolkit.interface import CommandLineInterface
from prompt_toolkit.keys import Keys
from prompt_toolkit.shortcuts import (
    create_eventloop, create_prompt_application, create_output)
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token
from prompt_toolkit.key_binding.manager import KeyBindingManager
from prompt_toolkit.validation import Validator, ValidationError


class RegexValidator(Validator):

    def __init__(self, pattern, msg=None):
        self.pattern = re.compile(pattern)
        self.msg = msg or 'Invalid input'

    def validate(self, document):
        if not re.match(self.pattern, document.text):
            raise ValidationError(message=self.msg)


class UI(object):

    def __init__(self, input_handler):

        self.input_handler = input_handler

        key_bindings_manager = KeyBindingManager.for_prompt()

        @key_bindings_manager.registry.add_binding(Keys.ControlJ, eager=True)
        def _(event):
            if event.current_buffer.text:
                self.input_handler(event.current_buffer.text)
                event.current_buffer.reset()

        get_prompt_tokens = lambda _: [(Token.Bottombar, '> ')]
        get_rprompt_tokens = (
            lambda _: [(Token.BBar, '[users: {}]'.format(len(self.users)))])
        style = style_from_dict({Token.Bottombar: '#ansiwhite bold'})

        self.app = create_prompt_application(
            key_bindings_registry=key_bindings_manager.registry,
            wrap_lines=True,
            erase_when_done=True,
            get_title=lambda: 'macchat',
            get_prompt_tokens=get_prompt_tokens,
            get_rprompt_tokens=get_rprompt_tokens,
            style=style,
        )
        self.cli = CommandLineInterface(
            application=self.app,
            eventloop=create_eventloop(),
            output=create_output()
        )
        self.users = {}
        self.user_colors = {}

        colors = itertools.cycle(('red', 'green', 'yellow', 'blue', 'magenta'))
        self.get_color = lambda: next(colors)


    def publish_message(self, user_id, username, msg):
        if user_id not in self.user_colors:
            self.user_colors[user_id] = self.get_color()

        color = self.user_colors[user_id]
        width = self.cli.output.get_size().columns
        text = textwrap.fill(
            msg, int(width*0.75), subsequent_indent='  '
        )
        print('{}{}'.format(
            click.style('{}: '.format(username), fg=color),
            click.style(text, fg='white')
        ))

    def show_notification(self, text):
        width = self.cli.output.get_size().columns
        print(click.style(
            '[{}]'.format(text).center(width), fg='cyan'
        ))

    def run(self):
        try:
            with self.cli.patch_stdout_context(raw=True):
                self.cli.run(reset_current_buffer=False)
        except (EOFError, KeyboardInterrupt):
            pass
        finally:
            self.cli.eventloop.close()
