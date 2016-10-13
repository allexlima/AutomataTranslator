#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtCore, QtGui
from engine import Translator
import webbrowser


class Interface(QtGui.QWidget):
    def __init__(self):
        super(Interface, self).__init__()
        self.app_name = "AutomataTranslator"
        self.width = 790
        self.height = 480
        self.engine = None
        self.__field_input = None
        self.__field_output = None
        self.is_jflap = False

    def init_ui(self):
        self.setWindowTitle(self.app_name)
        self.setWindowIcon(QtGui.QIcon('models/icon/favicon.ico'))
        self.setFixedSize(self.width, self.height)
        self.__menu_bar()
        self.__fields_io()
        self.__buttons()
        self.__center_widget()

    def __menu_bar(self):
        menu = QtGui.QMenuBar(self)
        menu.setFixedWidth(self.width)

        m_file = menu.addMenu(u"Arquivo")
        m_help = menu.addMenu(u"Ajuda")

        sub_file_json_open = QtGui.QAction(u"Abrir", self)
        sub_file_json_save = QtGui.QAction(u"Salvar", self)
        sub_file_jflap_import = QtGui.QAction(u"Importar arquivo JFLAP", self)
        sub_file_jflap_export = QtGui.QAction(u"Exportar para formato JFLAP", self)
        sub_file_table = QtGui.QAction(u"Ver tabela de transição", self)
        sub_file_exit = QtGui.QAction(u"Sair", self)
        sub_help_github = QtGui.QAction(u"GitHub", self)
        sub_help_wiki = QtGui.QAction(u"Documentação", self)
        sub_help_about = QtGui.QAction(u"Sobre", self)

        sub_file_json_open.triggered.connect(self.__open_json)
        sub_file_json_save.triggered.connect(self.__save_json)
        sub_file_jflap_import.triggered.connect(self.__open_jflap)
        sub_file_jflap_export.triggered.connect(self.__save_jflap)
        sub_file_table.triggered.connect(self.__show_table)
        sub_file_exit.triggered.connect(QtGui.QApplication.exit)
        sub_help_about.triggered.connect(self.about)
        sub_help_github.triggered.connect(self.github)
        sub_help_wiki.triggered.connect(self.wiki)

        m_file.addAction(sub_file_json_open)
        m_file.addAction(sub_file_json_save)
        m_file.addSeparator()
        m_file.addAction(sub_file_jflap_import)
        m_file.addAction(sub_file_jflap_export)
        m_file.addSeparator()
        m_file.addAction(sub_file_table)
        m_file.addSeparator()
        m_file.addAction(sub_file_exit)

        m_help.addAction(sub_help_github)
        m_help.addAction(sub_help_wiki)
        m_help.addSeparator()
        m_help.addAction(sub_help_about)

    def __fields_io(self):
        self.__field_input = QtGui.QTextEdit(self)
        self.__field_input.setObjectName("input")
        self.__field_input.setText(u"Escreva seu autômato aqui...")
        self.__field_input.setTabStopWidth(20)
        self.__field_input.setGeometry(30, 40, 350, 360)

        self.__field_output = QtGui.QTextEdit(self)
        self.__field_output.setObjectName("output")
        self.__field_output.setReadOnly(True)
        self.__field_output.setStyleSheet("background: #EBEBE4;")
        self.__field_output.setTabStopWidth(20)
        self.__field_output.setGeometry(410, 40, 350, 360)

    def __buttons(self):
        convert_button = QtGui.QPushButton(self)
        convert_button.setObjectName("convert")
        convert_button.setText("Converter")
        convert_button.clicked.connect(self.__translate_input)
        convert_button.move(self.width - 115, 425)

        clear_button = QtGui.QPushButton(self)
        clear_button.setObjectName("clear")
        clear_button.setText("Novo/Limpar")
        clear_button.clicked.connect(self.clear_input)
        clear_button.move(self.width - 225, 425)

    def __center_widget(self):
        resolution = QtGui.QDesktopWidget().screenGeometry()
        self.move((resolution.width() / 2) - (self.width / 2), (resolution.height() / 2) - (self.height / 2))

    def __open(self, path):
        with open(path, 'r') as my_file:
            data = my_file.read()
            self.set_input(data)

    @staticmethod
    def __save(path, content, extension):
        with open(path + extension, "w+") as new_file:
            new_file.write(content)

    def __open_json(self):
        file_path = QtGui.QFileDialog().getOpenFileName(self, "Abrir Arquivo", "models/json", "JSON (*.json)")
        if file_path:
            self.__open(file_path)

    def __open_jflap(self):
        file_path = QtGui.QFileDialog().getOpenFileName(self, "Importar arquivo JFLAP", "models/jflap", "JFLAP (*.jff)")
        if file_path:
            self.__open(file_path)
            self.is_jflap = True

    def __save_json(self):
        path = QtGui.QFileDialog().getSaveFileName(self, "Salvar Input", "models/json", "JSON (*.json)")
        if path:
            self.__save(path, self.get_input(), ".json")

    def __save_jflap(self):
        path = QtGui.QFileDialog().getSaveFileName(self, "Exportar Output para formato JFLAP", "models/jflap", "JFLAP (*.jff)")
        if path and self.get_output():
            data = self.engine.make_jff(self.get_output())
            self.__save(path, data, ".jff")

    def get_input(self):
        return str(self.__field_input.toPlainText())

    def set_input(self, text):
        self.__field_input.setText(text)

    def clear_input(self):
        self.set_input("")
        self.clear_output()
        self.is_jflap = False

    def get_output(self):
        return str(self.__field_output.toPlainText())

    def set_output(self, text):
        self.__field_output.setText(text)

    def clear_output(self):
        self.set_output("")

    def alert(self, text, title="Alert", code=2):
        message = QtGui.QMessageBox(self)
        message.setIcon(code)
        message.setText(unicode(text))
        message.setWindowTitle(title)
        message.setWindowModality(QtCore.Qt.ApplicationModal)
        message.exec_()

    def __translate_input(self):
        if self.get_input():
            self.engine = Translator(self.get_input())
            self.engine.jff2json() if self.is_jflap is True else None
            self.engine.convert()

            if self.engine.alerts() is not None:
                self.alert(self.engine.alerts(), title=u"Erro ao traduzir autômato", code=3)
            else:
                from json import dumps
                self.set_output(dumps(self.engine.entry, sort_keys=True, indent=4, separators=(',', ': ')))
                self.alert("Processo de tradução finalizado", title=u"Tradução realizada com sucesso!", code=1)
        else:
            self.alert(u"Escreva, abra ou importe algum autômato não determinístico para começar",
                       title="Input vazio!", code=4)

    def __show_table(self):
        if self.get_output():
            self.alert(self.engine.show_automaton(), title=u"Tabela de transições", code=0)
        else:
            self.alert(u"Nenhum AFN foi gerado para exibir a tabela de transição!", title="Output vazio!", code=4)

    def about(self):
        self.alert(
            u"\nTrabalho desenvolvido para compor a nota parcial da 1ª ARE da disciplina de Compiladores/Linguagens Formais e Autômatos, ministrada pelo Profº M.Sc. Camilo Souza. \n\nDesenvolvido por: Allex Lima & Daniel Bispo",
            title="Sobre",
            code=1
        )

    @staticmethod
    def github():
        webbrowser.open("https://github.com/allexlima/AutomataTranslator")

    @staticmethod
    def wiki():
        webbrowser.open("https://github.com/allexlima/AutomataTranslator/wiki")
