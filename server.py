import socket
import sys
from _thread import *


def clientthread(conn, addr):
    # Sending message to connected client
    conn.send('Welcome to the server. Type something and hit enter'.encode('utf-8'))  # send only takes string
    # infinite loop so that function do not terminate and thread do not end.
    while True:
        # Receiving from client
        data = conn.recv(1024)
        print('Received from %s:%d-' % (addr[0], addr[1]) + data.decode('utf-8'))
        reply = 'OK...' + data.decode('utf-8')
        if not data:
            break
        conn.send(reply.encode('utf-8'))
    # came out of loop
    conn.close()


HOST = '10.0.1.8'  # Symbolic name meaning all available interfaces
PORT = 8888  # Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print('Socket created')

try:
    s.bind((HOST, PORT))
except socket.error as msg:
    print('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
    sys.exit()

print('Socket bind complete')

s.listen(5)  # at most five unaccepted connections are allowed
print('Socket now listening')

# now keep talking with the client
while 1:
    # wait to accept a connection - blocking call
    print('Waiting for connection...')
    conn, addr = s.accept()
    print(addr)
    print('Connected with ' + addr[0] + ':' + str(addr[1]))
    start_new_thread(clientthread, (conn, addr,))
s.close()
