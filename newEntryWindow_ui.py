# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newEntryWindow.ui'
#
# Created: Sun Mar 15 15:33:52 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_newEntryWindow(object):
    def setupUi(self, newEntryWindow):
        newEntryWindow.setObjectName("newEntryWindow")
        newEntryWindow.resize(1081, 375)
        self.tabWidget = QtWidgets.QTabWidget(newEntryWindow)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 1061, 355))
        self.tabWidget.setTabBarAutoHide(True)
        self.tabWidget.setObjectName("tabWidget")

        self.retranslateUi(newEntryWindow)
        QtCore.QMetaObject.connectSlotsByName(newEntryWindow)

    def retranslateUi(self, newEntryWindow):
        _translate = QtCore.QCoreApplication.translate
        newEntryWindow.setWindowTitle(_translate("newEntryWindow", "Radio Log - New Entry"))

