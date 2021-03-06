from __future__ import unicode_literals

import time

from prompt_toolkit.shortcuts import prompt

from .sender import Sender
from .receiver import Receiver
from .encryption import AESCipher
from .ui import UI, RegexValidator
from .conf import config


class Event:
    JOIN = 0
    JOIN_REPLY = 1
    MSG = 2
    LEAVE = 3


class ChatClient(object):
    def __init__(self):

        self.ui = UI(input_handler=self.send_message)

        if config.get('USERNAME'):
            self.username = config['USERNAME']
        else:
            self.username = prompt(
                'Enter username: ',
                validator=RegexValidator(
                    '^[A-Za-z0-9_-]{3,10}$', msg='Not a valid username')
            )
        if config.get('SECRET_KEY'):
            key = config['SECRET_KEY']
        else:
            key = prompt(
                'Enter secret key: ', is_password=True,
                validator=RegexValidator(
                    '^.{1,128}$', msg='Not a valid string for key')
            )

        aes = AESCipher(key)
        self.receiver = Receiver(self.handle, encryptor=aes)
        self.sender = Sender(encryptor=aes)

        self.sender.start()
        self.receiver.start()
        # for threads to start
        time.sleep(.1)

        self.users = {}
        self.ui.users = self.users

    def handle(self, addr, event, data):

        if event == Event.MSG and addr in self.users:
            self.ui.publish_message(addr, self.users[addr], data)

        elif event == Event.JOIN:
            self.users[addr] = data
            self.sender.send(Event.JOIN_REPLY, self.username)
            self.ui.show_notification('{} joined'.format(data))

        elif event == Event.JOIN_REPLY and addr not in self.users:
            self.users[addr] = data

        elif event == Event.LEAVE and addr in self.users:
            self.ui.show_notification('{} left'.format(self.users[addr]))
            del self.users[addr]

    def send_message(self, msg):
        self.sender.send(Event.MSG, msg)

    def run(self):
        self.sender.send(Event.JOIN, self.username)
        self.ui.run()
        self.sender.send(Event.LEAVE)
