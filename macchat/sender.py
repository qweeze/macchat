import random
import atexit
from threading import Thread
from Queue import Queue
from scapy.all import Ether, Raw, sendp

from . import conf


class Sender(object):

    # min/max size of an ethernet frame payload minus
    # 32-48 bytes reserved for additional encryption data
    MIN_MSG_LENGTH = 46 - 16*2
    MAX_MSG_LENGTH = 1500 - 16*3

    def __init__(self, encryptor):
        self.encryptor = encryptor
        self.sender_q = Queue(maxsize=1024)
        # generating a fake mac address
        self.src = (conf.MAC_ADDR[:9] + ':'.join('{:02x}'.format(
            random.randint(0x00, i)) for i in (0x7f, 0xff, 0xff)))

        def send_packet():
            while True:
                sendp(self.sender_q.get(), iface=conf.get('IFACE'), verbose=False)
                self.sender_q.task_done()

        self.sender_thread = Thread(target=send_packet)
        self.sender_thread.daemon = True
        atexit.register(self.sender_q.join)

    def start(self):
        self.sender_thread.start()

    def send(self, event, data=''):
        payload = bytearray(self.MIN_MSG_LENGTH)
        payload[0] = event
        data = data.encode('utf8')
        payload[1:1 + len(data)] = data
        payload = payload[:self.MAX_MSG_LENGTH]
        encrypted = self.encryptor.encrypt(str(payload))
        pck = Ether(src=self.src, dst=conf.MAC_ADDR)/Raw(load=encrypted)
        self.sender_q.put(pck)
