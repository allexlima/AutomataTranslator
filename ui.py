# -*- coding: utf-8 -*-
import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from datetime import datetime

class Interface():
    def __init__(self):
        # Confiduração da janela principal
        self.app = QApplication(sys.argv)
        self.width = 790
        self.height = 480
        self.w = QWidget()
        self.w.setWindowTitle("AutomataTranslator")
        self.w.setFixedSize(self.width, self.height)
        self.center_widget()

        # Configuração da barra de menu
        self.build_menu()

        # Caixas de texto(input e output)
        self.build_io()

        # Botões Inferiores
        self.build_buttons()

        # Execução do Aplicativo e Condição de Saída
        self.w.show()
        sys.exit(self.app.exec_())


    # Construção da Barra de Menu
    def build_menu(self):
        self.menu_bar = QMenuBar(self.w)
        self.menu_bar.setFixedWidth(self.width)
        self.menu_arquivo = self.menu_bar.addMenu(u"Arquivo")
        self.menu_ajuda = self.menu_bar.addMenu(u"Ajuda")

        self.abrir_arquivo = QAction("Abrir JSON", self.w)
        self.abrir_arquivo.triggered.connect(self.open_json)
        self.salvar_arquivo = QAction("Salvar JSON", self.w)
        self.salvar_arquivo.triggered.connect(self.save_afd)
        self.exportar = QAction("Exportar JFLAP", self.w)
        self.exportar.triggered.connect(self.export_jflap)
        self.importar = QAction("Importar JFLAP", self.w)
        self.importar.triggered.connect(self.import_jflap)
        self.sair = QAction("Sair", self.w)
        self.sair.triggered.connect(qApp.quit)

        self.menu_arquivo.addAction(self.abrir_arquivo)
        self.menu_arquivo.addAction(self.salvar_arquivo)
        self.menu_arquivo.addSeparator()
        self.menu_arquivo.addAction(self.importar)
        self.menu_arquivo.addAction(self.exportar)
        self.menu_arquivo.addSeparator()
        self.menu_arquivo.addAction(self.sair)

        self.sobre = QAction("Sobre", self.w)

        self.menu_ajuda.addAction(self.sobre)

    # Construção das Caixas de Texto
    def build_io(self):
        self.input = QTextEdit(self.w)
        self.input.setObjectName("text")
        self.input.setText("Insira JSON aqui")
        self.input.setTabStopWidth(12)
        self.input.setGeometry(30, 40, 350, 360)

        self.output = QTextEdit(self.w)
        self.output.setReadOnly(True)
        self.output.setStyleSheet("background: #EBEBE4;")
        self.output.setObjectName("output")
        self.output.setTabStopWidth(12)
        self.output.setGeometry(410, 40, 350, 360)

    # Construção dos Botões Inferiores
    def build_buttons(self):
        # Botão para executar conversão do input
        self.convert_button = QPushButton(self.w)
        self.convert_button.setObjectName("convert")
        self.convert_button.setText("Converter")
        self.convert_button.clicked.connect(self.convert_input)
        self.convert_button.move(self.width - 115, 425)

        # Botão para limpar a caixa de texto "input"
        self.clear_button = QPushButton(self.w)
        self.clear_button.setObjectName("clear")
        self.clear_button.setText("Limpar Input")
        self.clear_button.clicked.connect(self.clear_input)
        self.clear_button.move(self.width - 220, 425)

    # Converter Input
    def convert_input(self):
        texto = self.input.toPlainText()
        return texto

    # Limpar Input
    def clear_input(self):
        self.input.setText("")

    # Centralizar Aplicação na Tela do Computador
    def center_widget(self):
        resolution = QDesktopWidget().screenGeometry()
        self.w.move((resolution.width() / 2) - (self.width / 2),
                  (resolution.height() / 2) - (self.height / 2))

    # Abrir Arquivos
    def open_json(self):
        #fi_le = QFileDialog()
        file_path = QFileDialog().getOpenFileName(self.w, "Abrir Arquivo", "/home", "JSON (*.json)")

        if file_path:
            with open(file_path, 'r') as my_file:
                data = my_file.read()
            self.input.setText(data)

    def import_jflap(self):
        file_path = QFileDialog().getOpenFileName(self.w, "Importar JFLAP", "/home", "JFLAP (*.jff)")

        if file_path:
            with open(file_path, 'r') as jflap_file:
                data = jflap_file.read()
            return data

    # Salvar Arquivos
    def save_afd(self):
        afd_content = self.output.toPlainText()
        save_path = QFileDialog().getSaveFileName(self.w, "Salvar Arquivo", "/home", "JSON (*.json)")

        if save_path:
            with open(save_path + ".json", "w+") as afd:
                afd.write(afd_content)
            return True

    def export_jflap(self):
        save_path = QFileDialog().getSaveFileName(self.w, "Exportar JFLAP", "/home", "JFLAP (*.jff)")
        afd_content = self.output.toPlainText()

        if save_path:
            with open(save_path + ".jff", 'w+') as jflap_file:
                jflap_file.write(afd_content)
            return True

    # Manipulador de Erros
    def show_error(self, msg):
        message = QMessageBox(self.w)
        message.setIcon(2)
        message.setText(msg)
        message.setWindowTitle("Erro")
        message.setWindowModality(Qt.ApplicationModal)

        message.exec_()



interface = Interface()
