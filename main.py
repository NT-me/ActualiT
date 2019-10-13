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
    def __init__(self, title="Default", parent=None):
        super(GUIActualiT, self).__init__(parent)
        self.old_List = []
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("ActualiT")
        self.setWindowIcon(QIcon('icon.png'))
        self.D = Ui_Dialog()
        self.ui.refreshButton.clicked.connect(self.buttonClicked)
        self.ui.mainCol.itemClicked.connect(self.item_click)
        self.ui.RSS_manage.clicked.connect(self.openRSSManager)
        self.ui.Twitter_manage.clicked.connect(self.openTwitterManager)
        self.ui.Reddit_manage.clicked.connect(self.openRedditManager)


    def updatetab(self, origin):
        liste = wdb.readOriginSources(origin)
        count = 0
        for i in reversed(range(self.D.tabSource.rowCount())):
            self.D.tabSource.removeRow(i)
        for item in liste :
            self.D.tabSource.insertRow(count)
            self.D.tabSource.setItem(count,0, QtWidgets.QTableWidgetItem(item.name))
            count =+ 1


    def openRSSManager(self):
        self.window = QtWidgets.QDialog()
        self.D.setupUi(self.window)
        self.window.show()
        self.D.ajoutButton.clicked.connect(self.addRSSSource)
        self.updatetab('RSS')

    def openTwitterManager(self):
        self.window = QtWidgets.QDialog()
        self.D.setupUi(self.window)
        self.window.show()
        self.D.ajoutButton.clicked.connect(self.addTwitterSource)
        self.updatetab('Twitter')



    def openRedditManager(self):
        self.window = QtWidgets.QDialog()
        self.D.setupUi(self.window)
        self.window.show()
        self.D.ajoutButton.clicked.connect(self.addRedditSource)
        self.updatetab('Reddit')


    def addRSSSource(self):
        text = self.D.addSourceLine.text()
        ns.add(text, 'RSS')
        self.updatetab('RSS')



    def addTwitterSource(self):
        text = self.D.addSourceLine.text()
        ns.add(text, 'Twitter')
        self.updatetab('Twitter')



    def addRedditSource(self):
        text = self.D.addSourceLine.text()
        ns.add(text, 'Reddit')
        self.updatetab('Reddit')



    def buttonClicked(self):
        liste = mainCol.gen_mainCol()
        self.ui.mainCol.clear()

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
