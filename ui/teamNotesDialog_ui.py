# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\caver\Documents\GitHub\radiolog\designer\teamNotesDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_teamNotesDialog(object):
    def setupUi(self, teamNotesDialog):
        teamNotesDialog.setObjectName("teamNotesDialog")
        teamNotesDialog.resize(400, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(teamNotesDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.teamField = QtWidgets.QComboBox(teamNotesDialog)
        self.teamField.setObjectName("teamField")
        self.verticalLayout.addWidget(self.teamField)
        self.notesField = QtWidgets.QPlainTextEdit(teamNotesDialog)
        self.notesField.setObjectName("notesField")
        self.verticalLayout.addWidget(self.notesField)
        self.buttonBox = QtWidgets.QDialogButtonBox(teamNotesDialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(teamNotesDialog)
        self.buttonBox.accepted.connect(teamNotesDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(teamNotesDialog.reject) # type: ignore
        self.teamField.currentTextChanged['QString'].connect(teamNotesDialog.teamChanged) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(teamNotesDialog)

    def retranslateUi(self, teamNotesDialog):
        _translate = QtCore.QCoreApplication.translate
        teamNotesDialog.setWindowTitle(_translate("teamNotesDialog", "Dialog"))
