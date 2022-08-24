# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'printClueLogDialog.ui'
#
# Created: Tue Apr  7 12:24:34 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_printClueLogDialog(object):
    def setupUi(self, printClueLogDialog):
        printClueLogDialog.setObjectName("printClueLogDialog")
        printClueLogDialog.resize(429, 110)
        self.buttonBox = QtWidgets.QDialogButtonBox(printClueLogDialog)
        self.buttonBox.setGeometry(QtCore.QRect(210, 60, 193, 37))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_2 = QtWidgets.QLabel(printClueLogDialog)
        self.label_2.setGeometry(QtCore.QRect(10, 10, 327, 28))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.opPeriodComboBox = QtWidgets.QComboBox(printClueLogDialog)
        self.opPeriodComboBox.setGeometry(QtCore.QRect(354, 10, 61, 34))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.opPeriodComboBox.sizePolicy().hasHeightForWidth())
        self.opPeriodComboBox.setSizePolicy(sizePolicy)
        self.opPeriodComboBox.setMaximumSize(QtCore.QSize(75, 16777215))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.opPeriodComboBox.setFont(font)
        self.opPeriodComboBox.setObjectName("opPeriodComboBox")

        self.retranslateUi(printClueLogDialog)
        self.buttonBox.accepted.connect(printClueLogDialog.accept)
        self.buttonBox.rejected.connect(printClueLogDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(printClueLogDialog)

    def retranslateUi(self, printClueLogDialog):
        _translate = QtCore.QCoreApplication.translate
        printClueLogDialog.setWindowTitle(_translate("printClueLogDialog", "Print Clue Log"))
        self.label_2.setText(_translate("printClueLogDialog", "Print Clue Log for Operational Period:"))

