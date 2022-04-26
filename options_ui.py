# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'options.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_optionsDialog(object):
    def setupUi(self, optionsDialog):
        optionsDialog.setObjectName("optionsDialog")
        optionsDialog.resize(616, 378)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        optionsDialog.setFont(font)
        self.gridLayout = QtWidgets.QGridLayout(optionsDialog)
        self.gridLayout.setObjectName("gridLayout")
        self.timeoutField = QtWidgets.QSlider(optionsDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.timeoutField.setFont(font)
        self.timeoutField.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.timeoutField.setMinimum(0)
        self.timeoutField.setMaximum(12)
        self.timeoutField.setSingleStep(1)
        self.timeoutField.setPageStep(2)
        self.timeoutField.setProperty("value", 0)
        self.timeoutField.setTracking(True)
        self.timeoutField.setOrientation(QtCore.Qt.Horizontal)
        self.timeoutField.setTickPosition(QtWidgets.QSlider.TicksAbove)
        self.timeoutField.setTickInterval(1)
        self.timeoutField.setObjectName("timeoutField")
        self.gridLayout.addWidget(self.timeoutField, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(optionsDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(optionsDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 2, 0, 1, 1)
        self.buttonBox = QtWidgets.QDialogButtonBox(optionsDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.gridLayout.addWidget(self.buttonBox, 9, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(optionsDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.datumField = QtWidgets.QComboBox(optionsDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.datumField.setFont(font)
        self.datumField.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.datumField.setObjectName("datumField")
        self.datumField.addItem("")
        self.datumField.addItem("")
        self.gridLayout.addWidget(self.datumField, 1, 1, 1, 1)
        self.formatField = QtWidgets.QComboBox(optionsDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.formatField.setFont(font)
        self.formatField.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.formatField.setObjectName("formatField")
        self.formatField.addItem("")
        self.formatField.addItem("")
        self.formatField.addItem("")
        self.formatField.addItem("")
        self.formatField.addItem("")
        self.gridLayout.addWidget(self.formatField, 2, 1, 1, 1)
        self.secondWorkingDirCheckBox = QtWidgets.QCheckBox(optionsDialog)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.secondWorkingDirCheckBox.setFont(font)
        self.secondWorkingDirCheckBox.setWhatsThis("")
        self.secondWorkingDirCheckBox.setChecked(True)
        self.secondWorkingDirCheckBox.setObjectName("secondWorkingDirCheckBox")
        self.gridLayout.addWidget(self.secondWorkingDirCheckBox, 8, 1, 1, 1)
        self.timeoutLabel = QtWidgets.QLabel(optionsDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.timeoutLabel.setFont(font)
        self.timeoutLabel.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.timeoutLabel.setObjectName("timeoutLabel")
        self.gridLayout.addWidget(self.timeoutLabel, 3, 0, 1, 1)
        self.incidentField = QtWidgets.QLineEdit(optionsDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.incidentField.setFont(font)
        self.incidentField.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.incidentField.setObjectName("incidentField")
        self.gridLayout.addWidget(self.incidentField, 0, 1, 1, 1)
        self.fsSendButton = QtWidgets.QPushButton(optionsDialog)
        self.fsSendButton.setObjectName("fsSendButton")
        self.gridLayout.addWidget(self.fsSendButton, 9, 0, 1, 1)

        self.retranslateUi(optionsDialog)
        self.buttonBox.accepted.connect(optionsDialog.accept) # type: ignore
        self.buttonBox.rejected.connect(optionsDialog.reject) # type: ignore
        self.secondWorkingDirCheckBox.stateChanged['int'].connect(optionsDialog.secondWorkingDirCB) # type: ignore
        self.fsSendButton.clicked.connect(optionsDialog.fsSendCB) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(optionsDialog)

    def retranslateUi(self, optionsDialog):
        _translate = QtCore.QCoreApplication.translate
        optionsDialog.setWindowTitle(_translate("optionsDialog", "Options"))
        self.label.setText(_translate("optionsDialog", "Incident Name"))
        self.label_4.setText(_translate("optionsDialog", "Coordinate Format"))
        self.label_3.setText(_translate("optionsDialog", "Datum"))
        self.datumField.setItemText(0, _translate("optionsDialog", "NAD27 CONUS"))
        self.datumField.setItemText(1, _translate("optionsDialog", "WGS84"))
        self.formatField.setItemText(0, _translate("optionsDialog", "UTM 5x5"))
        self.formatField.setItemText(1, _translate("optionsDialog", "UTM 7x7"))
        self.formatField.setItemText(2, _translate("optionsDialog", "D.d°"))
        self.formatField.setItemText(3, _translate("optionsDialog", "D° M.m\'"))
        self.formatField.setItemText(4, _translate("optionsDialog", "D° M\' S.s\""))
        self.secondWorkingDirCheckBox.setText(_translate("optionsDialog", "Use Second Working Directory"))
        self.timeoutLabel.setText(_translate("optionsDialog", "Timeout"))
        self.incidentField.setText(_translate("optionsDialog", "New Incident"))
        self.fsSendButton.setText(_translate("optionsDialog", "FleetSync Send Console"))