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
from GUI.ajout_source import Ui_Dialog
from GUI.NACManageDialog import Ui_Dialog as NAC_Dialog
import sys
from FillmainCol.scrapers import utils as u
from FillmainCol import wrapperDB as wdb
from Model import article as Mart
import os
from objects.source import Source
from sources import newSource as ns


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
    cellItem = None
    def __init__(self, title="Default", parent=None):
        super(GUIActualiT, self).__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("ActualiT")
        self.setWindowIcon(QIcon('icon.png'))
        self.D = Ui_Dialog()
        self.NAC_D = NAC_Dialog()
        self.ui.refreshButton.clicked.connect(self.refreshClicked)
        self.ui.mainCol.itemClicked.connect(self.item_click)
        self.ui.RSS_manage.clicked.connect(self.openRSSManager)
        self.ui.Twitter_manage.clicked.connect(self.openTwitterManager)
        self.ui.Reddit_manage.clicked.connect(self.openRedditManager)
        self.ui.NAC_manage.clicked.connect(self.openNACManager)

    def updatetab(self, origin):
        self.cellItem = None
        liste = wdb.readOriginSources(origin)
        count = 0
        for i in reversed(range(self.D.tabSource.rowCount())):
            self.D.tabSource.removeRow(i)
        for item in liste:
            Qitem = QtWidgets.QTableWidgetItem()
            QitemL = QtWidgets.QTableWidgetItem()

            self.D.tabSource.insertRow(count)
            Qitem.setData(Qt.UserRole, item)

            # Name
            Qitem.setText(Qitem.data(Qt.UserRole).name)
            self.D.tabSource.setItem(count, 0, Qitem)

            # Link
            QitemL.setText(Qitem.data(Qt.UserRole).link)
            self.D.tabSource.setItem(count, 1, QitemL)

            # TAG || labels
            count = + 1

    def rename(self):
        if self.cellItem is not None :
            if self.cellItem.column() == 0:
                wdb.modSource(self.cellItem.data(Qt.UserRole).ID, "name", self.cellItem.text())

            self.cellItem = None

    def cellClickedMemory(self, row, column):
        self.cellItem = self.D.tabSource.item(row, 0)

    def deleteSourceInner(self, origin):
        if self.cellItem is not None:
            wdb.suprSource(self.cellItem.data(Qt.UserRole).ID)
            self.cellItem = None
            self.updatetab(origin)

    def openManagerInner(self, origin):
        add_func_name = "add" + str(origin) + "Source"
        del_func_name = "delete" + "Source" + str(origin)
        self.cellItem = None
        self.window = QtWidgets.QDialog()
        self.D.setupUi(self.window)
        self.window.show()
        self.D.ajoutButton.clicked.connect(getattr(self, add_func_name))
        self.D.tabSource.cellClicked.connect(self.cellClickedMemory)
        self.D.supprButton.clicked.connect(getattr(self, del_func_name))
        self.D.tabSource.itemChanged.connect(self.rename)
        self.updatetab(origin)

    def openNACManager(self):
        self.window = QtWidgets.QDialog()
        self.NAC_D.setupUi(self.window)
        self.window.show()

    def addSourceInner(self, origin):
        text = self.D.addSourceLine.text()
        self.D.addSourceLine.clear()
        ns.add(text, origin)
        self.updatetab(origin)

    def openRSSManager(self):
        self.openManagerInner('RSS')

    def openTwitterManager(self):
        self.openManagerInner('Twitter')

    def openRedditManager(self):
        self.openManagerInner('Reddit')

    def addRSSSource(self):
        self.addSourceInner('RSS')

    def addTwitterSource(self):
        self.addSourceInner('Twitter')

    def addRedditSource(self):
        self.addSourceInner('Reddit')

    def deleteSourceRSS(self):
        self.deleteSourceInner('RSS')

    def deleteSourceReddit(self):
        self.deleteSourceInner('Reddit')

    def deleteSourceTwitter(self):
        self.deleteSourceInner('Twitter')

    def refreshClicked(self):
        liste = mainCol.gen_mainCol()
        liste = wdb.deleteArticlesTooOld(liste, 604800)
        self.ui.mainCol.clear()

        def getDate(article):
            return article.date

        liste = sorted(liste, key=getDate, reverse=True)
        for item in liste:
            date = str(time.ctime(item.date))
            Qitem = QtWidgets.QListWidgetItem()
            Qitem.setText(str(item.titre)+' | '+date)
            Qitem.setData(Qt.UserRole, item.ID)
            self.ui.mainCol.addItem(Qitem)

    @u.MTime
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
