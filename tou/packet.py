from enum import Enum
from struct import *

class ToUPacket:
    def __init__(self, flag, 
                src_host='0.0.0.0', src_port=0, 
                dst_host='0.0.0.0', dst_port=0, 
                seq=0, ack=0,
                window=0,
                checksum=0,
                data=None):
        self.src_host = src_host
        self.src_port = src_port
        self.dst_host = dst_host
        self.dst_port = dst_port
        self.flag = flag
        self.ack = ack
        self.seq = seq
        self.window = window
        self.checksum = checksum
        self.data = data 

    def build(self):
        hdr = pack(
            '!HHIIBBHHH',
            self.src_port,
            self.dst_port,
            self.seq,
            self.ack,
            5 << 4,
            self.flag,
            self.window,
            self.checksum,
            0,
        )
        if self.data is not None:
            return hdr + self.data.encode()
        return hdr 

    def show(self):
        print("----- tou packet -----")
        print("src_port: ", self.src_port)
        print("dst_port: ", self.dst_port)
        print("flag: ", self.flag)
        print("seq: ", self.seq)
        print("ack: ", self.ack)
        print("window: ", self.window)
        print("checksum: ", self.checksum)
        # print("data len: ", len(self.data))

def parse_packet(data):
    hdr_data = data[:20]
    hdr = unpack(
        '!HHIIBBHHH',
        hdr_data
    )
    data = data[20:]
    return ToUPacket(
        src_port=hdr[0],
        dst_port=hdr[1],
        seq=hdr[2],
        ack=hdr[3],
        flag=hdr[5],
        window=hdr[6],
        checksum=hdr[7],
        data=data
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
