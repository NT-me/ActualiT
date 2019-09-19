# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import mainCol

from GUI.mainwindow import Ui_MainWindow
import sys


class GUIActualiT(QtWidgets.QMainWindow):
    def __init__(self, title="Default", parent=None):
        super(GUIActualiT, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.buttonClicked)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = GUIActualiT()
    w.show()
    sys.exit(app.exec_())
