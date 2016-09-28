# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Interface():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.w = QWidget()
        self.w.setWindowTitle("AutomataTranslator")
        self.w.setGeometry(100, 100, 320, 150)

        self.text = QTextEdit(self.w)
        self.text.setObjectName("text")
        self.text.setText("Insira JSON aqui")
        self.text.setGeometry(20, 20, 280, 40)

        self.pb = QPushButton(self.w)
        self.pb.setObjectName("convert")
        self.pb.setText("Converter")
        self.pb.clicked.connect(self.button_click)
        self.pb.move(20, 80)

        self.w.show()
        sys.exit(self.app.exec_())

    def button_click(self):
        shost = self.text.toPlainText()
        print shost.encode('utf-8')


interface = Interface()
