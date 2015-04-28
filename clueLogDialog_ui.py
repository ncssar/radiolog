# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clueLogDialog.ui'
#
# Created: Tue Apr  7 12:50:43 2015
#      by: PyQt5 UI code generator 5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_clueLogDialog(object):
    def setupUi(self, clueLogDialog):
        clueLogDialog.setObjectName("clueLogDialog")
        clueLogDialog.resize(1000, 500)
        self.verticalLayout = QtWidgets.QVBoxLayout(clueLogDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QtWidgets.QLabel(clueLogDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout.addWidget(self.label_2)
        self.addNonRadioClueButton = QtWidgets.QPushButton(clueLogDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.addNonRadioClueButton.sizePolicy().hasHeightForWidth())
        self.addNonRadioClueButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.addNonRadioClueButton.setFont(font)
        self.addNonRadioClueButton.setObjectName("addNonRadioClueButton")
        self.horizontalLayout.addWidget(self.addNonRadioClueButton)
        self.printButton = QtWidgets.QToolButton(clueLogDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.printButton.sizePolicy().hasHeightForWidth())
        self.printButton.setSizePolicy(sizePolicy)
        self.printButton.setMinimumSize(QtCore.QSize(0, 0))
        self.printButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.printButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.printButton.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/radiolog_ui/print_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.printButton.setIcon(icon)
        self.printButton.setIconSize(QtCore.QSize(30, 30))
        self.printButton.setObjectName("printButton")
        self.horizontalLayout.addWidget(self.printButton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tableView = QtWidgets.QTableView(clueLogDialog)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setObjectName("tableView")
        self.tableView.verticalHeader().setVisible(False)
        self.tableView.verticalHeader().setHighlightSections(False)
        self.verticalLayout.addWidget(self.tableView)

        self.retranslateUi(clueLogDialog)
        QtCore.QMetaObject.connectSlotsByName(clueLogDialog)

    def retranslateUi(self, clueLogDialog):
        _translate = QtCore.QCoreApplication.translate
        clueLogDialog.setWindowTitle(_translate("clueLogDialog", "Clue Log"))
        self.label_2.setText(_translate("clueLogDialog", "Clue Log"))
        self.addNonRadioClueButton.setText(_translate("clueLogDialog", "Add Non-Radio Clue"))

import radiolog_ui_rc
