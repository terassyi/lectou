from tou import *
import time

t = ToU()
tou_sock = t.socket()

peer_sock = tou_sock.connect(('172.20.0.3', 8080))

time.sleep(7)
peer_sock.send("hi via tou protocol!".encode())

time.sleep(1)
data = peer_sock.recv(1024)

print(">>>> %s" % data.decode())

time.sleep(5)
peer_sock.active_close()
