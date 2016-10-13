#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4.QtGui import QApplication
# from engine import Translator
from ui import Interface


if __name__ == "__main__":
    reload(sys)
    sys.setdefaultencoding('utf8')

    app = QApplication(["AutomataTranslator"])
    ui = Interface()
    ui.init_ui()

    # -- Espaço para testes

    ui.alert(u"Aplicação em modo de testes! \nIniciando...", code=1)
    # ui.set_input("Teste")

    # --

    ui.show()
    sys.exit(app.exec_())
