# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\caver\Documents\GitHub\radiolog\designer\findDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_findDialog(object):
    def setupUi(self, findDialog):
        findDialog.setObjectName("findDialog")
        findDialog.resize(311, 56)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(findDialog.sizePolicy().hasHeightForWidth())
        findDialog.setSizePolicy(sizePolicy)
        self.verticalLayout = QtWidgets.QVBoxLayout(findDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.findField = QtWidgets.QLineEdit(findDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.findField.sizePolicy().hasHeightForWidth())
        self.findField.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.findField.setFont(font)
        self.findField.setObjectName("findField")
        self.verticalLayout.addWidget(self.findField)

        self.retranslateUi(findDialog)
        QtCore.QMetaObject.connectSlotsByName(findDialog)

    def retranslateUi(self, findDialog):
        _translate = QtCore.QCoreApplication.translate
        findDialog.setWindowTitle(_translate("findDialog", "Find"))
        self.findField.setPlaceholderText(_translate("findDialog", "Enter text to search for..."))
