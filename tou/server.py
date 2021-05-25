# from tou.packet import *
# from tou.tou import *
from tou import *
import time

t = ToU()
tou_sock = t.socket()

tou_sock.bind(('0.0.0.0', 8080))
tou_sock.listen()
peer_sock = tou_sock.accept()

time.sleep(5)
data = peer_sock.recv(1024)

print(">>>> %s" % data.decode())
time.sleep(3)

peer_sock.send("nice to meet you!".encode())

time.sleep(3)
peer_sock.passive_close()
