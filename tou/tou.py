import socket
from enum import Enum
from tou import *
import packet as tou_packet

class ToUSocket():
    def __init__(self):
        self.inner_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.peer_addr = '0.0.0.0'
        self.peer_port = 0
        self.host_addr = '0.0.0.0'
        self.host_port = 0
        self.state = State.CLOSED

    def recv(self, buffer_size):
        pass

    def send(self, data):
        pass

    def _is_established(self):
        return self.state is State.ESTABLISHED

    def connect(self, peer):
        self.peer_addr = peer[0]
        self.peer_port = peer[1]
        print("[INFO] active open")
        self._send_packet(tou_packet.Flag.SYN.value)

        self.state = State.SYN_SENT
        print("[INFO] SYN_SENT")

        packet, _ = self._recv_packet()
        print("hogehoge")
        if packet.flag is tou_packet.Flag.SYN + tou_packet.Flag.ACK:
            self._send_packet(tou_packet.Flag.ACK.value)
            self.state = State.SYN_RECVD
            print("[INFO] SYN_RCVD")
            
        else:
            self._send_packet(tou_packet.Flag.RST.value)
            raise ConnectionRefusedError
            return
        
        packet, _ = self._recv_packet()
        if packet.flag is tou_packet.Flag.ACK.value:
            self.state = State.ESTABLISHED
            print("[INFO] ESTAB")
            return 
        else:
            self._send_packet(tou_packet.Flag.RST.value)
            raise ConnectionRefusedError
            return


    def bind(self, host):
        print("[DEBUG] bind")
        self.host_addr = host[0]
        self.host_port = host[1]
        self.inner_socket.bind(host)

    def listen(self, listener_num=None):

        self.state = State.LISTEN
        print("[INFO] LISTEN")

    def accept(self):
        packet, peer = self._recv_packet()
        self.peer_addr = peer[0]
        self.peer_port = peer[1]
        packet.show()
        if packet.flag is tou_packet.Flag.SYN.value:
            self.state = State.SYN_RECVD
            print("[INFO] SYN_RCVD")

            self._send_packet(tou_packet.Flag.SYN + tou_packet.Flag.ACK)
        else:
            self._send_packet(tou_packet.Flag.RST.value)
            raise ConnectionRefusedError
            return

        self._send_packet(tou_packet.Flag.ACK.value)
        self.state = State.ESTABLISHED
        print("[INFO] ESTAB")

        return self

    def _send_packet(self, flag, data=None):
        packet = tou_packet.ToUPacket(flag, data)
        print("[DEBUG] _send_packet")
        packet.show()
        data = packet.build()
        self.inner_socket.sendto(data, (self.peer_addr, self.peer_port))
        return len(data)

    def _recv_packet(self):
        data, peer = self.inner_socket.recvfrom(1024)
        packet = tou_packet.parse_packet(data)
        print("[DEBUG] _recv_packet")
        return packet, peer

class ToU:
    def __init__(self,peer_addr='0.0.0.0', peer_port=0, host_addr='0.0.0.0', host_port=0):
        self.host_addr = host_addr
        self.host_port = host_port
        self.peer_addr = peer_addr
        self.peer_port = peer_port
    
    def set_host_addr(self):
        self.host_addr = socket.gethostbyname(socket.gethostname())

    def set_host_port(self, port):
        self.host_port = port

    def socket(self):
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
