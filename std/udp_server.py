import socket
import sys
import time

port = int(sys.argv[1])

host = ('0.0.0.0', port)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(host)

while True:
    try:
        print(">> waiting for incomming message from remote hosts.")
        message, peer = sock.recvfrom(1024)
        print("from (%s:%d) << %s" % (peer[0], peer[1], message.decode()))
        
        time.sleep(1)

        print("to> (%s:%d) >>" % (peer[0], peer[1]), end='')
        reply = input()
        sock.sendto(reply.encode(), peer)
    
    except KeyboardInterrupt:
        print("socket close. exit.")
        sock.close()
        break
