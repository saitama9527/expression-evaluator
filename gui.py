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
        self.inp = ''
        self.bkc = ''

        self.setGeometry(300,300,500,300)
        self.pic = QLabel(self)
        self.pic.setPixmap(QPixmap('self.JPG'))
        self.pic.setGeometry(30,160,160,120)
        self.label = QLabel(self.inp,self)
        self.label.setStyleSheet("border: 1px solid black")
        self.label.setNum(0)
        self.label.setAlignment(Qt.AlignRight)
        self.label.setGeometry(20,20,460,20)
        self.setWindowTitle('楊景勛_410421211-Calculator')
        self.lcd =  QLCDNumber()
        self.lcd.setDigitCount(15)
        grid.addWidget(self.lcd,0,0,3,0)
        grid.setSpacing(5)

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
        ls = ['/', '*', '-', '+']
        if sender == 'Clr':
            self.label.setNum(0)
            self.lcd.display(0)
            self.inp = ''


        elif sender == '=':
            e = exp.expression()
            decount = 0
            for i in range(0, len(self.inp)-1):
                if self.inp[i] in ls:
                    if self.inp[i-1] in ls:
                        #print(v)
                        v = 0
                        break
                    else:
                        v = 1

            for p in range(0, len(self.inp) - 1):
                if self.inp[p+1] in ls:
                    decount = 0
                if self.inp[p] == '.':
                    decount += 1
                    if decount >= 2:
                        v = 0

            if v == 0:
                self.lcd.display('Error')
            else:
               # print(e.val)
               # print(v)
                v, rc = e.interpret(self.inp)
                self.lcd.display(e.val)

        elif sender == 'Bc':
            self.bkc = ''
            for i in range(0 , len(self.inp)-1):
                self.bkc += self.inp[i]

            self.inp = self.bkc
            self.label.setText(self.inp)

        elif sender == 'Close':
            quit()

       # elif sender in ls:
          #  if self.inp[len(self.inp) - 1] in ls:
            #    self.label.setText('Error')

            #else:
                #self.inp += str(sender)
                #self.label.setText(self.inp)

        else:
            self.inp += str(sender)
            self.label.setText(self.inp)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    app.exit(app.exec_())



