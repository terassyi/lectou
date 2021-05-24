import socket
from enum import Enum

class ToUSocket():
    def __init__():
        pass

    def recv(self, buffer_size):
        pass

    def send(self, data):
        pass

    def connect(self, peer):
        pass

    def bind(self, host):
        pass

    def listen(self, listener_num=None):
        pass

    def accept(self):
        pass

class ToU:
    def __init__(peer_addr, peer_port, host_addr=None, host_port=None):
        self.host_addr = host_addr
        self.host_port = host_port
        self.peer_addr = peer_addr
        self.peer_port = peer_port
        self.state = State.CLOSED
    
    def set_host_addr(self):
        self.host_addr = socket.gethostbyname(socket.gethostname())

    def set_host_port(self, port):
        self.host_port = port

    def socket():
        return ToUSocket()

class State(Enum):
    CLOSED = 0
    LISTEN = 1
    SYN_SENT = 2
    SYN_RECVD = 3
    ESTABLISHED = 4
    FIN_WAIT1 = 5
    FIN_WAIT2 = 6
    CLOSING = 7
    TIME_WAIT = 8
    CLOSE_WAIT = 9
    LAST_ACK = 10
