# -*- coding: utf-8 -*-

from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qtmodern.styles
import qtmodern.windows
import mainCol
import time
from threading import Thread
from tinydb import TinyDB, Query

from GUI.mainwindow import Ui_MainWindow
import sys
import utils as u
db = TinyDB(u.PATH_DB)


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
        self.ui.mainCol.itemClicked.connect(self.item_click)

    def buttonClicked(self):
        liste = mainCol.gen_mainCol()
        for item in liste:
            date = str(time.ctime(item.date))
            Qitem = QtWidgets.QListWidgetItem()
            QV = QVariant(item.ID)
            Qitem.setText(str(item.titre)+' | '+date)
            Qitem.setData(Qt.UserRole, item.ID)
            self.ui.mainCol.addItem(Qitem)

    def item_click(self, item):
        id = item.data(Qt.UserRole)
        if id != 0:
            article = db.search(Query().ID == id)
            title = ''
            contenu = ''
            try:
                title = article[0]["Titre"]
            except TypeError :
                title = 'Title is broken !'
            try:
                contenu = article[0]["Contenu"]
            except TypeError:
                contenu = ''

            self.ui.articleShower.append('<h1>' + title + '</h1>' + '\n' + '<p>' + contenu + '</p>')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    qtmodern.styles.dark(app)
    w = GUIActualiT()
    w.show()
    sys.exit(app.exec_())
