# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Interface():
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.width = 800
        self.height = 480
        self.w = QWidget()
        self.w.setWindowTitle("AutomataTranslator")
        #self.w.setGeometry(100, 100, 800, 450)
        self.w.setFixedSize(self.width, self.height)
        self.center_widget()

        self.menu_bar = QMenuBar(self.w)
        self.menu_opcoes = self.menu_bar.addMenu("Opcoes")
        self.sair = QAction("Sair", self.w)
        self.sair.triggered.connect(qApp.quit)
        self.abrir_arquivo = QAction("Abrir", self.w)
        self.abrir_arquivo.triggered.connect(qApp.quit)
        self.menu_opcoes.addAction(self.abrir_arquivo)
        self.menu_opcoes.addAction(self.sair)


        self.txt = QTextEdit(self.w)
        self.txt.setObjectName("text")
        self.txt.setText("Insira JSON aqui")
        self.txt.setGeometry(30, 40, 300, 360)

        self.out = QTextEdit(self.w)
        self.out.setReadOnly(True)
        self.out.setStyleSheet("background: #EBEBE4;")
        self.out.setObjectName("output")
        self.out.setGeometry(470, 40, 300, 360)

        self.convert_button = QPushButton(self.w)
        self.convert_button.setObjectName("convert")
        self.convert_button.setText("Converter")
        self.convert_button.clicked.connect(self.button_convert)
        self.convert_button.move(686, 420)

        self.clear_button = QPushButton(self.w)
        self.clear_button.setObjectName("clear")
        self.clear_button.setText("Limpar Input")
        self.clear_button.clicked.connect(self.button_clear)
        self.clear_button.move(576, 420)

        self.w.show()
        sys.exit(self.app.exec_())

    def button_convert(self):
        texto = self.txt.toPlainText()
        print texto

    def button_clear(self):
        self.txt.setText("")

    def center_widget(self):
        resolution = QDesktopWidget().screenGeometry()
        self.w.move((resolution.width() / 2) - (self.width / 2),
                  (resolution.height() / 2) - (self.height / 2))

interface = Interface()
