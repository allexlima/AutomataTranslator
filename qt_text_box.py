import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def window():
    app = QApplication(sys.argv)
    w = QWidget()
    w.setWindowTitle("Text Box Test")

    textbox = QLineEdit(w)
    textbox.move(20, 20)
    textbox.resize(280, 40)

    w.resize(320, 150)

    button = QPushButton("Click here", w)
    button.move(20, 80)

    button.clicked.connect(on_click)

    w.show()
    sys.exit(app.exec_())

def on_click():
    textbox.setText("Button clicked")

if __name__ == '__main__':
    window()
