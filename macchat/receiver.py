from __future__ import unicode_literals
from threading import Thread
from Queue import Queue
from scapy.all import sniff, Raw, Ether

from .conf import config


class Receiver(object):
    def __init__(self, handler, encryptor):
        self.handler = handler
        self.encryptor = encryptor
        self.input_q = Queue(maxsize=1024)

        flt = 'ether dst {}'.format(config['MAC_ADDR'])
        self.receiver_thread = Thread(
            target=lambda: sniff(filter=flt, prn=self.input_q.put, store=False))
        self.processor_thread = Thread(target=self.process_message)
        self.receiver_thread.daemon = True
        self.processor_thread.daemon = True

    def start(self):
        self.receiver_thread.start()
        self.processor_thread.start()

    def process_message(self):
        while True:
            pck = self.input_q.get()
            addr = pck.src
            encrypted = pck.getlayer(Raw).load
            raw = self.encryptor.decrypt(encrypted)
            if raw:
                event, data = ord(raw[0]), raw[1:].rstrip('\0')
                self.handler(addr, event, data)
            self.input_q.task_done()
