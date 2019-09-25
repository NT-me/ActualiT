# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qtmodern.styles
import qtmodern.windows
import dbToList as dbl
import mainCol
import time
from threading import Thread

from GUI.mainwindow import Ui_MainWindow
import sys


class MainColWork(Thread):
    def __init__(self):
        Thread.__init__(self)

    def run(self):
        mainCol.gen_mainCol()


def MainColWorkFunc():
    MCW = MainColWork()
    MCW.deamon = False
    MCW.start()
    MCW.join()


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
                date = str(time.ctime(item.date))
                self.ui.mainCol.addItem(str(item.titre)+' | '+date)

        else:
            self.statusBar().showMessage('Erreur')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    qtmodern.styles.dark(app)
    w = GUIActualiT()
    w.show()
    sys.exit(app.exec_())
