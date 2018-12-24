from PyQt5.QtWidgets import (QApplication, QMessageBox, QWidget, QPushButton)
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication, QGridLayout, QLCDNumber)
from PyQt5.QtWidgets import (QWidget, QSlider, QLabel, QApplication)
from PyQt5.QtCore import Qt
import socket  # for sockets
import sys  # for exit
import struct
import time
from PyQt5.QtGui import QPixmap
from random import randint

class client():
    def __init__(self):
        super().__init__()

    def recv_timeout(the_socket, timeout=2):
        # make socket non blocking
        the_socket.setblocking(0)

        # total data partwise in an array
        total_data = [];
        data = '';

        # beginning time
        begin = time.time()
        while 1:
            # if you got some data, then break after timeout
            if total_data and time.time() - begin > timeout:
                break

            # if you got no data at all, wait a little longer, twice the timeout
            elif time.time() - begin > timeout * 2:
                break

            # recv something
            try:
                data = the_socket.recv(8192)
                if data:
                    total_data.append(data.decode('utf-8'))
                    # change the beginning time for measurement
                    begin = time.time()
                else:
                    # sleep for sometime to indicate a gap
                    time.sleep(0.1)
            except:
                pass

        # join all parts to make final string
        return ''.join(total_data)

    # create an INET, STREAMing socket
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket')
        sys.exit()

    print('Socket Created')

    host = '10.0.1.8';
    port = 8888;

    try:
        remote_ip = socket.gethostbyname(host)

    except socket.gaierror:
        # could not resolve
        print('Hostname could not be resolved. Exiting')
        sys.exit()

    # Connect to remote server
    s.connect((remote_ip, port))

    print('Socket Connected to ' + host + ' on ip ' + remote_ip)
    print(recv_timeout(s))  # Get and print reply from server

    try:
         # Set the whole string
        message = 'Ready'  # enter an empty string to abort the server
         # Send some data to remote server
        s.send(message.encode('utf-8'))
        print('Message send successfully')
        # Get and print the server's response
        print(recv_timeout(s))
    except socket.error:
        # Send failed
         print('Send failed')
         sys.exit()

class Bot(QWidget,client):

    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
        self.setGeometry(200, 200, 300, 300)
        self.setWindowTitle('Learn PyQt5')
        self.inp = '1'
        self.label = QLabel(self.inp,self)
        self.label.setStyleSheet("border: 1px solid black")
        self.label.setAlignment(Qt.AlignRight)
        self.label.setGeometry(120, 30, 150, 30)

        bt1 = QPushButton('left',self)
        bt1.setGeometry(50,180,50,50)

        bt2 = QPushButton('down',self)
        bt2.setGeometry(120,180,50,50)

        bt3 = QPushButton('up',self)
        bt3.setGeometry(120,100,50,50)

        bt4 = QPushButton('right', self)
        bt4.setGeometry(190, 180, 50, 50)

        bt1.clicked.connect(self.buttonclicked)
        bt2.clicked.connect(self.buttonclicked)
        bt3.clicked.connect(self.buttonclicked)
        bt4.clicked.connect(self.buttonclicked)

        self.show()

    def buttonclicked(self): # override the button press slot
        sender = self.sender().text()
        self.inp = sender
        message = self.inp
        client.s.send(message.encode('utf-8'))
        print('Message send successfully')
        print(client.recv_timeout(client.s))
        self.label.setText(self.inp)








if __name__ == '__main__':
    app = QApplication(sys.argv)
    bot = Bot()
    sys.exit(app.exec_())


