# from tou.packet import *
# from tou.tou import *
from tou import *

t = ToU()
tou_sock = t.socket()

tou_sock.bind(('0.0.0.0', 8080))
tou_sock.listen()
tou_sock.accept()
