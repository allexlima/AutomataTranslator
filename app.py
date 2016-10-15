#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Immportação das bibliotecas básicas para funcionamento da aplicação

import sys
from PyQt4.QtGui import QApplication
from ui import Interface

#
# - Todo o core da tradução encontra-se no arquivo engine.py
#

if __name__ == "__main__":

    # Define a codificação do sistema par a UTF-8
    reload(sys)
    sys.setdefaultencoding('utf8')

    # Define o nome da aplicação executável
    app = QApplication(["AutomataTranslator"])
    # Instancia a classe Interface
    ui = Interface()
    # Chama o método ´init_ui´, método responsável por montar a tela principal
    ui.init_ui()

    # -- Espaço para testes

    # ui.alert(u"Aplicação em modo de testes! \nIniciando...", code=1)
    # ui.set_input("Teste")

    # --

    # Execut a aplicação
    ui.show()
    sys.exit(app.exec_())
