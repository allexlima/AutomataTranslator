import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *

def window():
    app = QApplication(sys.argv)
    w = QWidget()
    w.setWindowTitle("Text Box Test")
    w.setGeometry(100, 100, 320, 150)

    textbox = QTextEdit(w)
    textbox.setGeometry(20, 20, 280, 40)

    button = QPushButton("Click here", w)
    button.move(20, 80)

    button_submit = QPushButton("submit", w)
    button_submit.move(150, 80)

    button.clicked.connect(on_click)

    w.show()
    sys.exit(app.exec_())

def on_click():
    print "clicked"

if __name__ == '__main__':
    window()
