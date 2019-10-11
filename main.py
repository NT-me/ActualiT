# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import qtmodern.styles
import qtmodern.windows
from FillmainCol import mainCol
import time
from threading import Thread
from GUI.GUI_2 import Ui_MainWindow
import sys
from FillmainCol.scrapers import utils as u
from FillmainCol import wrapperDB as wdb
from Model import article as Mart
import os


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
        self.old_List = []
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("ActualiT")
        self.setWindowIcon(QIcon('icon.png'))
        self.ui.refreshButton.clicked.connect(self.buttonClicked)
        self.ui.mainCol.itemClicked.connect(self.item_click)

    def buttonClicked(self):
        liste = mainCol.gen_mainCol()

        def getDate(article):
            return article.date

        liste = sorted(liste, key=getDate, reverse=True)
        for item in liste:
            if item not in self.old_List:
                date = str(time.ctime(item.date))
                Qitem = QtWidgets.QListWidgetItem()
                Qitem.setText(str(item.titre)+' | '+date)
                Qitem.setData(Qt.UserRole, item.ID)
                self.ui.mainCol.addItem(Qitem)
        self.old_List = liste

    def item_click(self, item):
        id = item.data(Qt.UserRole)
        if id != 0:
            article = wdb.readArticle(id)
            print(id)
            title = ''
            contenu = ''
            try:
                title = article.titre
            except TypeError:
                title = 'Title is broken !'
            try:
                contenu = article.resume
            except TypeError:
                contenu = ''
            self.ui.articleShower.clear()
            self.ui.articleShower.append(Mart.model(article))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    #qtmodern.styles.dark(app)
    w = GUIActualiT()
    w.show()
    sys.exit(app.exec_())
