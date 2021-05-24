from enum import Enum
from struct import *

class ToUPacket:
    def __init__(flag, src_host=None, src_port=None, dst_host=None, dst_port=None):
        self.src_host = src_host
        self.src_port = src_port
        self.dst_host = dst_host
        self.dst_port = dst_port
        self.flag = flag
        self.ack = 0
        self.seq = 0
        self.window = 0
        self.checksum = 0

    def build(self):
        packet = pack(
            '!HHIIBBHHH',
            self.src_port,
            self.dst_port,
            self.seq,
            self.ack,
            5 << 4,
            self.flag,
            self.window,
            self.checksum,
            0
        )

class Flag(Enum):
    FIN = 0x01
    SYN = 0x02
    RST = 0x04
    PSH = 0x08
    ACK = 0x10
    URG = 0x20 # don't use
    ECN = 0x40 # don't use
    CWR = 0x80 # don't use

    def __add__(self, flag):
        return self.value + flag.value

    def __or__(self, flag):
        return self.value + flag.value
    
    def __sub__(self, flag):
        return self.value - flag.value
