import sys
import exp
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication, QGridLayout, QLCDNumber)
from PyQt5.QtWidgets import (QWidget, QSlider, QLabel, QApplication)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap

'''e = exp.expression()
v, rc = e.interpret('123.22*234*2.3-23')
print(e.val)'''



class Example(QWidget):
    def __init__(self):
        super().__init__()
        self.Init_UI()

    def Init_UI(self):
        grid = QGridLayout()
        self.setLayout(grid)
        self.iput = []
        self.cnt = 1
        self.zero = ''
        self.bkc = ''

        self.setGeometry(300,300,400,300)
        self.label = QLabel(self)
        self.label.setNum(0)
        self.label.setGeometry(370,-40,500,100)
        self.setWindowTitle('Learn PyQt5')
        self.lcd =  QLCDNumber()
        self.lcd.setDigitCount(12)
        grid.addWidget(self.lcd,0,0,3,0)
        grid.setSpacing(10)

        names = ['Clr', 'Bc', '', 'Close',
                 '7', '8', '9', '/',
                 '4', '5', '6', '*',
                 '1', '2', '3', '-',
                 '0', '.', '=', '+']

        positions = [(i,j) for i in range(4,9) for j in range(4,8)]
        for position, name in zip(positions, names):
            if name == '':
                continue
            button = QPushButton(name)
            grid.addWidget(button, *position)
            button.clicked.connect(self.Cli)

        self.setLayout(grid)
        self.show()

    def Cli(self):
        sender = self.sender().text()
        self.geox = 370
            #self.iput[0] = self.iput[0]+self.iput[i]
            #i = i+1
        ls = ['/', '*', '-', '=', '+']
        if sender == 'Clr':
            self.iput.clear()
            self.geox = 370
            self.label.setGeometry(self.geox, -40, 500, 100)
            self.label.setNum(0)
            self.cnt = 1
            i = 0
            self.lcd.display(0)
            self.zero = ''

        elif sender == '=':
            e = exp.expression()
            v, rc = e.interpret(self.iput[0])
            print(e.val)
            self.lcd.display(e.val)

        elif sender == 'Bc':
            self.cnt = self.cnt -1
            print(self.cnt-1)
            self.bkc = self.iput[0]
            #self.iput.clear()
            #self.iput.append(self.bkc)
            self.iput[self.cnt-1] = ''
            self.iput[0] = self.zero + self.bkc[1:self.cnt-1]
            print(self.iput[0])
            print(self.bkc)
            self.label.setGeometry(self.geox-8.4*(self.cnt-2), -40, 500, 100)
            self.label.setText(self.iput[0])


        elif self.cnt==1:
            self.iput.append(sender)
            self.label.setText(self.iput[0])
            self.zero  = self.iput[0]
            self.cnt = self.cnt + 1

        elif self.cnt!=1:
            self.iput.append(sender)
            #for i in range(self.cnt-1,self.cnt):
            self.iput[0] = self.iput[0]+self.iput[self.cnt-1]
            self.geox = self.geox - 8.4*(self.cnt-1)
            self.label.setGeometry(self.geox, -40, 500, 100)


            self.label.setText(self.iput[0])
            self.cnt = self.cnt + 1


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    app.exit(app.exec_())



