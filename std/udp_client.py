import socket
import sys

addr = sys.argv[1]
port = int(sys.argv[2])

peer = (addr, port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("UPD client program start\n")

while True:
    try:
        print("to> (%s:%d) >> " % (addr, port), end='')
        message = input()
        l = sock.sendto(message.encode('utf-8'), peer)
        recv, remote = sock.recvfrom(1024)
        print("from> (%s:%d) << %s" % (remote[0], remote[1], recv.decode()))
    
    except KeyboardInterrupt:
        print("socket close. exit.")
        sock.close()
        break


