from tou import *

t = ToU()
tou_sock = t.socket()

tou_sock.connect(('172.20.0.3', 8080))
