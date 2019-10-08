# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ajout_source.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(400, 300)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(220, 260, 161, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 381, 241))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.tabSource = QtWidgets.QTableWidget(self.verticalLayoutWidget)
        self.tabSource.setObjectName("tabSource")
        self.tabSource.setColumnCount(2)
        self.tabSource.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tabSource.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tabSource.setHorizontalHeaderItem(1, item)
        self.verticalLayout.addWidget(self.tabSource)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.addSourceLine = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.addSourceLine.setObjectName("addSourceLine")
        self.horizontalLayout.addWidget(self.addSourceLine)
        self.ajoutButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.ajoutButton.setObjectName("ajoutButton")
        self.horizontalLayout.addWidget(self.ajoutButton)
        self.supprButton = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.supprButton.setObjectName("supprButton")
        self.horizontalLayout.addWidget(self.supprButton)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Ajout de source"))
        item = self.tabSource.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Sources"))
        item = self.tabSource.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Labels"))
        self.ajoutButton.setText(_translate("Dialog", "Ajout"))
        self.supprButton.setText(_translate("Dialog", "Suppresion"))
