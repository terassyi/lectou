import socket
import sys
import time

port = int(sys.argv[1])

host = ('0.0.0.0', port)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(host)

sock.listen(5)

print("TCP serer program start")

peer_sock, addr = sock.accept()
print(">> connection established with %s:%d" % (addr[0], addr[1]))

while True:
    try:
        message = peer_sock.recv(1024)
        print("from (%s:%d) >> %s" % (addr[0], addr[1], message.decode()))
    

        print("to> (%s:%d) >>" % (host[0], host[1]), end='')
        reply = input()
        peer_sock.send(reply.encode())

    except KeyboardInterrupt:
        peer_sock.close()
        sock.close()
        print("socket close. exit.")
        break
