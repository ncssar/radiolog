# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'newEntryWindow.ui'
#
# Created: Thu Nov  5 20:46:07 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_newEntryWindow(object):
    def setupUi(self, newEntryWindow):
        newEntryWindow.setObjectName("newEntryWindow")
        newEntryWindow.resize(1162, 545)
        self.tabWidget = QtWidgets.QTabWidget(newEntryWindow)
        self.tabWidget.setGeometry(QtCore.QRect(10, 10, 1147, 491))
        self.tabWidget.setTabBarAutoHide(True)
        self.tabWidget.setObjectName("tabWidget")
        self.autoCleanupCheckBox = QtWidgets.QCheckBox(newEntryWindow)
        self.autoCleanupCheckBox.setGeometry(QtCore.QRect(230, 510, 721, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.autoCleanupCheckBox.setFont(font)
        self.autoCleanupCheckBox.setChecked(True)
        self.autoCleanupCheckBox.setObjectName("autoCleanupCheckBox")

        self.retranslateUi(newEntryWindow)
        QtCore.QMetaObject.connectSlotsByName(newEntryWindow)
        newEntryWindow.setTabOrder(self.tabWidget, self.autoCleanupCheckBox)

    def retranslateUi(self, newEntryWindow):
        _translate = QtCore.QCoreApplication.translate
        newEntryWindow.setWindowTitle(_translate("newEntryWindow", "Radio Log - New Entry"))
        self.autoCleanupCheckBox.setText(_translate("newEntryWindow", "Auto-cleanup: automatically delete blank entries that are more than 60 seconds old"))

