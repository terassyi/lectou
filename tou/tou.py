import socket
import time
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
        print("[DEBUG] recv")
        if not self._is_established():
            raise ConnectionError
        packet, _ = self._recv_packet()
        if packet.flag is not tou_packet.Flag.ACK.value:
            self._send_packet(tou_packet.Flag.RST.value)
        
        data = packet.data

        self._send_packet(tou_packet.Flag.ACK.value)
        return data

    def send(self, data):
        if not self._is_established():
            raise ConnectionError
        print("[DEBUG] send: ", data)
        self._send_packet(tou_packet.Flag.ACK.value, data)

        # wait ack
        packet, _ = self._recv_packet()
        if packet.flag is tou_packet.Flag.ACK.value:
            return 
        else:
            self._send_packet(tou_packet.Flag.RST.value)
            raise ConnectionRefusedError

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
        if packet.flag is tou_packet.Flag.SYN + tou_packet.Flag.ACK:
            self._send_packet(tou_packet.Flag.ACK.value)
            
        else:
            self._send_packet(tou_packet.Flag.RST.value)
            raise ConnectionRefusedError
            return
        
        self.state = State.ESTABLISHED
        print("[INFO] ESTAB")
        return self
        


    def bind(self, host):
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

        packet, _ = self._recv_packet()
        if packet.flag is tou_packet.Flag.ACK.value:
            self.state = State.ESTABLISHED
            print("[INFO] ESTAB")
            
        else:
            self._send_packet(tou_packet.Flag.RST.value)
            raise ConnectionRefusedError
            return

        return self

    def active_close(self):
        if not self._is_established():
            raise ConnectionError
        
        self._send_packet(tou_packet.Flag.FIN + tou_packet.Flag.ACK)
        self.state = State.FIN_WAIT1
        print("[INFO] FIN_WAIT1")

        # ack of fin
        packet, _ = self._recv_packet()
        if packet.flag is not tou_packet.Flag.ACK.value:
            self._send_packet(tou_packet.Flag.RST.value)
            print("[ERROR] ack of fin is not found")
            raise ConnectionError
        
        self.state = State.FIN_WAIT2
        print("[INFO] FIN_WAIT2")
        
        # fin
        packet, _ = self._recv_packet()
        if packet.flag is not tou_packet.Flag.FIN + tou_packet.Flag.ACK:
            print("[ERROR] fin|ack is not found (active close)")
            raise ConnectionError
        
        self.state = State.TIME_WAIT
        print("[INFO] TIME_WAIT")
        self._send_packet(tou_packet.Flag.ACK.value)
        self._timer()
        
        self.state = State.CLOSED
        print("[INFO] CLOSED")


    def passive_close(self):
        packet, _ = self._recv_packet()
        if packet.flag is not tou_packet.Flag.FIN + tou_packet.Flag.ACK:
            print("[ERROR] fin is not set (passive close)")
            raise ConnectionError
        
        self.state = State.CLOSE_WAIT
        self._send_packet(tou_packet.Flag.ACK.value)

        self.state = State.LAST_ACK
        self._send_packet(tou_packet.Flag.FIN + tou_packet.Flag.ACK)

        self.state = State.CLOSED
        print("[INFO] CLOSED")

    def _timer(self):
        time.sleep(20)

    def _send_packet(self, flag, data=None):
        packet = tou_packet.ToUPacket(flag, data=data)
        packet.show()
        p = packet.build()
        self.inner_socket.sendto(p, (self.peer_addr, self.peer_port))
        return len(p)

    def _recv_packet(self):
        data, peer = self.inner_socket.recvfrom(1024)
        packet = tou_packet.parse_packet(data)
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
