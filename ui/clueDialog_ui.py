# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'clueDialog.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_clueDialog(object):
    def setupUi(self, clueDialog):
        clueDialog.setObjectName("clueDialog")
        clueDialog.resize(728, 561)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        clueDialog.setFont(font)
        self.label_4 = QtWidgets.QLabel(clueDialog)
        self.label_4.setGeometry(QtCore.QRect(10, 370, 141, 37))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.buttonBox = QtWidgets.QDialogButtonBox(clueDialog)
        self.buttonBox.setGeometry(QtCore.QRect(550, 440, 161, 51))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.label_3 = QtWidgets.QLabel(clueDialog)
        self.label_3.setGeometry(QtCore.QRect(20, 310, 131, 37))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(clueDialog)
        self.label.setGeometry(QtCore.QRect(0, 170, 151, 37))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.instructionsField = QtWidgets.QLineEdit(clueDialog)
        self.instructionsField.setGeometry(QtCore.QRect(160, 370, 551, 40))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.instructionsField.setFont(font)
        self.instructionsField.setObjectName("instructionsField")
        self.locationField = QtWidgets.QLineEdit(clueDialog)
        self.locationField.setGeometry(QtCore.QRect(160, 310, 551, 39))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.locationField.setFont(font)
        self.locationField.setObjectName("locationField")
        self.label_2 = QtWidgets.QLabel(clueDialog)
        self.label_2.setGeometry(QtCore.QRect(270, 20, 191, 41))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_2.setFont(font)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.clueNumberField = QtWidgets.QLineEdit(clueDialog)
        self.clueNumberField.setGeometry(QtCore.QRect(640, 20, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.clueNumberField.setFont(font)
        self.clueNumberField.setObjectName("clueNumberField")
        self.label_6 = QtWidgets.QLabel(clueDialog)
        self.label_6.setGeometry(QtCore.QRect(560, 20, 71, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label_6.setFont(font)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")
        self.groupBox = QtWidgets.QGroupBox(clueDialog)
        self.groupBox.setGeometry(QtCore.QRect(30, 70, 661, 92))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.callsignField = QtWidgets.QLineEdit(self.groupBox)
        self.callsignField.setEnabled(False)
        self.callsignField.setGeometry(QtCore.QRect(240, 20, 161, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.callsignField.setFont(font)
        self.callsignField.setFocusPolicy(QtCore.Qt.NoFocus)
        self.callsignField.setText("")
        self.callsignField.setObjectName("callsignField")
        self.label_5 = QtWidgets.QLabel(self.groupBox)
        self.label_5.setEnabled(False)
        self.label_5.setGeometry(QtCore.QRect(240, 40, 161, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setEnabled(False)
        self.label_8.setGeometry(QtCore.QRect(424, 59, 221, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_8.setFont(font)
        self.label_8.setAlignment(QtCore.Qt.AlignCenter)
        self.label_8.setObjectName("label_8")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setEnabled(False)
        self.label_7.setGeometry(QtCore.QRect(130, 40, 91, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.timeField = QtWidgets.QLineEdit(self.groupBox)
        self.timeField.setEnabled(False)
        self.timeField.setGeometry(QtCore.QRect(130, 20, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.timeField.setFont(font)
        self.timeField.setFocusPolicy(QtCore.Qt.NoFocus)
        self.timeField.setText("")
        self.timeField.setObjectName("timeField")
        self.dateField = QtWidgets.QLineEdit(self.groupBox)
        self.dateField.setEnabled(False)
        self.dateField.setGeometry(QtCore.QRect(20, 20, 91, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.dateField.setFont(font)
        self.dateField.setFocusPolicy(QtCore.Qt.NoFocus)
        self.dateField.setText("")
        self.dateField.setObjectName("dateField")
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setEnabled(False)
        self.label_9.setGeometry(QtCore.QRect(20, 40, 91, 41))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName("label_9")
        self.radioLocField = QtWidgets.QTextEdit(self.groupBox)
        self.radioLocField.setEnabled(False)
        self.radioLocField.setGeometry(QtCore.QRect(429, 6, 211, 63))
        font = QtGui.QFont()
        font.setPointSize(11)
        self.radioLocField.setFont(font)
        self.radioLocField.setFocusPolicy(QtCore.Qt.NoFocus)
        self.radioLocField.setObjectName("radioLocField")
        self.clueQuickTextButton1 = QtWidgets.QPushButton(clueDialog)
        self.clueQuickTextButton1.setGeometry(QtCore.QRect(20, 430, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.clueQuickTextButton1.setFont(font)
        self.clueQuickTextButton1.setFocusPolicy(QtCore.Qt.NoFocus)
        self.clueQuickTextButton1.setObjectName("clueQuickTextButton1")
        self.clueQuickTextButton3 = QtWidgets.QPushButton(clueDialog)
        self.clueQuickTextButton3.setGeometry(QtCore.QRect(400, 430, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.clueQuickTextButton3.setFont(font)
        self.clueQuickTextButton3.setFocusPolicy(QtCore.Qt.NoFocus)
        self.clueQuickTextButton3.setObjectName("clueQuickTextButton3")
        self.clueQuickTextButton4 = QtWidgets.QPushButton(clueDialog)
        self.clueQuickTextButton4.setGeometry(QtCore.QRect(20, 470, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.clueQuickTextButton4.setFont(font)
        self.clueQuickTextButton4.setFocusPolicy(QtCore.Qt.NoFocus)
        self.clueQuickTextButton4.setObjectName("clueQuickTextButton4")
        self.clueQuickTextButton2 = QtWidgets.QPushButton(clueDialog)
        self.clueQuickTextButton2.setGeometry(QtCore.QRect(200, 430, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.clueQuickTextButton2.setFont(font)
        self.clueQuickTextButton2.setFocusPolicy(QtCore.Qt.NoFocus)
        self.clueQuickTextButton2.setObjectName("clueQuickTextButton2")
        self.clueQuickTextUndoButton = QtWidgets.QPushButton(clueDialog)
        self.clueQuickTextUndoButton.setGeometry(QtCore.QRect(20, 520, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.clueQuickTextUndoButton.setFont(font)
        self.clueQuickTextUndoButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.clueQuickTextUndoButton.setObjectName("clueQuickTextUndoButton")
        self.clueReportPrintCheckBox = QtWidgets.QCheckBox(clueDialog)
        self.clueReportPrintCheckBox.setGeometry(QtCore.QRect(180, 520, 381, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.clueReportPrintCheckBox.setFont(font)
        self.clueReportPrintCheckBox.setChecked(True)
        self.clueReportPrintCheckBox.setObjectName("clueReportPrintCheckBox")
        self.clueQuickTextButton5 = QtWidgets.QPushButton(clueDialog)
        self.clueQuickTextButton5.setGeometry(QtCore.QRect(200, 470, 181, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.clueQuickTextButton5.setFont(font)
        self.clueQuickTextButton5.setFocusPolicy(QtCore.Qt.NoFocus)
        self.clueQuickTextButton5.setObjectName("clueQuickTextButton5")
        self.descriptionField = QtWidgets.QPlainTextEdit(clueDialog)
        self.descriptionField.setGeometry(QtCore.QRect(160, 170, 551, 121))
        self.descriptionField.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.descriptionField.setMouseTracking(True)
        self.descriptionField.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.descriptionField.setStyleSheet("font: 14pt \"Segoe UI\";")
        self.descriptionField.setInputMethodHints(QtCore.Qt.ImhNone)
        self.descriptionField.setTabChangesFocus(True)
        self.descriptionField.setObjectName("descriptionField")
        self.clueQuickTextButton6 = QtWidgets.QPushButton(clueDialog)
        self.clueQuickTextButton6.setGeometry(QtCore.QRect(400, 470, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.clueQuickTextButton6.setFont(font)
        self.clueQuickTextButton6.setFocusPolicy(QtCore.Qt.NoFocus)
        self.clueQuickTextButton6.setObjectName("clueQuickTextButton6")
        self.line = QtWidgets.QFrame(clueDialog)
        self.line.setGeometry(QtCore.QRect(100, 500, 531, 20))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.groupBox.raise_()
        self.label_4.raise_()
        self.buttonBox.raise_()
        self.label_3.raise_()
        self.label.raise_()
        self.instructionsField.raise_()
        self.locationField.raise_()
        self.label_2.raise_()
        self.clueNumberField.raise_()
        self.label_6.raise_()
        self.clueQuickTextButton1.raise_()
        self.clueQuickTextButton3.raise_()
        self.clueQuickTextButton4.raise_()
        self.clueQuickTextButton2.raise_()
        self.clueQuickTextUndoButton.raise_()
        self.clueReportPrintCheckBox.raise_()
        self.clueQuickTextButton5.raise_()
        self.descriptionField.raise_()
        self.clueQuickTextButton6.raise_()
        self.line.raise_()

        self.retranslateUi(clueDialog)
        self.buttonBox.accepted.connect(clueDialog.accept)
        self.buttonBox.rejected.connect(clueDialog.close)
        self.clueQuickTextButton1.clicked.connect(clueDialog.clueQuickTextAction)
        self.clueQuickTextButton2.clicked.connect(clueDialog.clueQuickTextAction)
        self.clueQuickTextButton3.clicked.connect(clueDialog.clueQuickTextAction)
        self.clueQuickTextButton4.clicked.connect(clueDialog.clueQuickTextAction)
        self.clueQuickTextUndoButton.clicked.connect(clueDialog.clueQuickTextUndo)
        self.clueQuickTextButton5.clicked.connect(clueDialog.clueQuickTextAction)
        self.clueQuickTextButton6.clicked.connect(clueDialog.clueQuickTextAction)
        QtCore.QMetaObject.connectSlotsByName(clueDialog)
        clueDialog.setTabOrder(self.clueNumberField, self.descriptionField)
        clueDialog.setTabOrder(self.descriptionField, self.locationField)
        clueDialog.setTabOrder(self.locationField, self.instructionsField)
        clueDialog.setTabOrder(self.instructionsField, self.clueReportPrintCheckBox)

    def retranslateUi(self, clueDialog):
        _translate = QtCore.QCoreApplication.translate
        clueDialog.setWindowTitle(_translate("clueDialog", "Clue Report"))
        self.label_4.setText(_translate("clueDialog", "Instructions"))
        self.label_3.setText(_translate("clueDialog", "Location"))
        self.label.setText(_translate("clueDialog", "Description"))
        self.label_2.setText(_translate("clueDialog", "Clue Report"))
        self.label_6.setText(_translate("clueDialog", "Clue #"))
        self.label_5.setText(_translate("clueDialog", "REPORTED BY"))
        self.label_8.setText(_translate("clueDialog", "RADIO LOCATION"))
        self.label_7.setText(_translate("clueDialog", "TIME"))
        self.label_9.setText(_translate("clueDialog", "DATE"))
        self.clueQuickTextButton1.setText(_translate("clueDialog", "COLLECT  [F1]"))
        self.clueQuickTextButton1.setShortcut(_translate("clueDialog", "F1"))
        self.clueQuickTextButton3.setText(_translate("clueDialog", "DISREGARD  [F3]"))
        self.clueQuickTextButton3.setShortcut(_translate("clueDialog", "F3"))
        self.clueQuickTextButton4.setText(_translate("clueDialog", "HOLD POSITION  [F4]"))
        self.clueQuickTextButton4.setShortcut(_translate("clueDialog", "F4"))
        self.clueQuickTextButton2.setText(_translate("clueDialog", "MARK && LEAVE  [F2]"))
        self.clueQuickTextButton2.setShortcut(_translate("clueDialog", "F2"))
        self.clueQuickTextUndoButton.setText(_translate("clueDialog", "UNDO  [Ctrl+Z]"))
        self.clueQuickTextUndoButton.setShortcut(_translate("clueDialog", "Ctrl+Z"))
        self.clueReportPrintCheckBox.setText(_translate("clueDialog", "Print a Clue Report Form as soon as this clue is saved"))
        self.clueQuickTextButton5.setText(_translate("clueDialog", "PROTECT THE CLUE  [F5]"))
        self.clueQuickTextButton5.setShortcut(_translate("clueDialog", "F5"))
        self.clueQuickTextButton6.setText(_translate("clueDialog", "STANDBY [F6]"))
        self.clueQuickTextButton6.setShortcut(_translate("clueDialog", "F6"))
