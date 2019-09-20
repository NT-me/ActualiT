# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import dbToList as dbl
import mainCol
import time

from GUI.mainwindow import Ui_MainWindow
import sys


class GUIActualiT(QtWidgets.QMainWindow):
    def __init__(self, title="Default", parent=None):
        super(GUIActualiT, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        a = mainCol.gen_mainCol()
        if a == 0:
            self.statusBar().showMessage('Accomplit avec succès')
            liste = dbl.sortMainCol()
            for item in liste:
                self.ui.mainCol.addItem(str(item.titre)+' | '+str(time.ctime(item.date)))

        else:
            self.statusBar().showMessage('Erreur')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = GUIActualiT()
    w.show()
    sys.exit(app.exec_())
