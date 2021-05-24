import socket
import sys

addr = sys.argv[1]
port = int(sys.argv[2])

peer = (addr, port)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("TCP client program start\n")

sock.connect(peer)

while True:
    try:
        print("to> (%s:%d) >> " % (addr, port), end='')
        message = input()
        sock.send(message.encode())

        res = sock.recv(1024)
        print("from> (%s:%d) << %s" % (peer[0], peer[1], res.decode()))
    
    except KeyboardInterrupt:
        sock.close()
        print("socket close. exit.")
        break
