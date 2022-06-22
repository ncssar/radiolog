# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fsSendDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_fsSendDialog(object):
    def setupUi(self, fsSendDialog):
        fsSendDialog.setObjectName("fsSendDialog")
        fsSendDialog.resize(431, 386)
        self.verticalLayout = QtWidgets.QVBoxLayout(fsSendDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.sendTextRadioButton = QtWidgets.QRadioButton(fsSendDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.sendTextRadioButton.setFont(font)
        self.sendTextRadioButton.setChecked(True)
        self.sendTextRadioButton.setObjectName("sendTextRadioButton")
        self.buttonGroup = QtWidgets.QButtonGroup(fsSendDialog)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.sendTextRadioButton)
        self.verticalLayout_6.addWidget(self.sendTextRadioButton)
        self.pollGPSRadioButton = QtWidgets.QRadioButton(fsSendDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        self.pollGPSRadioButton.setFont(font)
        self.pollGPSRadioButton.setObjectName("pollGPSRadioButton")
        self.buttonGroup.addButton(self.pollGPSRadioButton)
        self.verticalLayout_6.addWidget(self.pollGPSRadioButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout_5.addLayout(self.horizontalLayout_2)
        self.line = QtWidgets.QFrame(fsSendDialog)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_5.addWidget(self.line)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.sendToAllCheckbox = QtWidgets.QCheckBox(fsSendDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.sendToAllCheckbox.setFont(font)
        self.sendToAllCheckbox.setObjectName("sendToAllCheckbox")
        self.horizontalLayout_3.addWidget(self.sendToAllCheckbox)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem3)
        self.verticalLayout_5.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(fsSendDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setStyleSheet("margin-bottom:-2")
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.fleetField = QtWidgets.QLineEdit(fsSendDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.fleetField.setFont(font)
        self.fleetField.setText("")
        self.fleetField.setObjectName("fleetField")
        self.verticalLayout_2.addWidget(self.fleetField)
        self.horizontalLayout.addLayout(self.verticalLayout_2)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.deviceLabel = QtWidgets.QLabel(fsSendDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.deviceLabel.setFont(font)
        self.deviceLabel.setStyleSheet("margin-bottom:-2")
        self.deviceLabel.setObjectName("deviceLabel")
        self.verticalLayout_3.addWidget(self.deviceLabel)
        self.deviceField = QtWidgets.QLineEdit(fsSendDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.deviceField.setFont(font)
        self.deviceField.setObjectName("deviceField")
        self.verticalLayout_3.addWidget(self.deviceField)
        self.horizontalLayout.addLayout(self.verticalLayout_3)
        self.horizontalLayout.setStretch(0, 1)
        self.horizontalLayout.setStretch(1, 2)
        self.verticalLayout_5.addLayout(self.horizontalLayout)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.label_3 = QtWidgets.QLabel(fsSendDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet("margin-bottom:-2")
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_4.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(fsSendDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_4.addWidget(self.label_4)
        self.messageField = QtWidgets.QLineEdit(fsSendDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.messageField.setFont(font)
        self.messageField.setObjectName("messageField")
        self.verticalLayout_4.addWidget(self.messageField)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        self.verticalLayout.addLayout(self.verticalLayout_5)
        self.label_2 = QtWidgets.QLabel(fsSendDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.buttonBox = QtWidgets.QDialogButtonBox(fsSendDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.buttonBox.setFont(font)
        self.buttonBox.setStyleSheet("button-layout:2;")
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(fsSendDialog)
        self.buttonBox.rejected.connect(fsSendDialog.reject) # type: ignore
        self.sendTextRadioButton.toggled['bool'].connect(fsSendDialog.functionChanged) # type: ignore
        self.sendToAllCheckbox.toggled['bool'].connect(fsSendDialog.sendAllCheckboxChanged) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(fsSendDialog)
        fsSendDialog.setTabOrder(self.sendTextRadioButton, self.pollGPSRadioButton)
        fsSendDialog.setTabOrder(self.pollGPSRadioButton, self.sendToAllCheckbox)
        fsSendDialog.setTabOrder(self.sendToAllCheckbox, self.fleetField)
        fsSendDialog.setTabOrder(self.fleetField, self.deviceField)
        fsSendDialog.setTabOrder(self.deviceField, self.messageField)

    def retranslateUi(self, fsSendDialog):
        _translate = QtCore.QCoreApplication.translate
        fsSendDialog.setWindowTitle(_translate("fsSendDialog", "FleetSync Send Console"))
        self.sendTextRadioButton.setText(_translate("fsSendDialog", "Send Text Message"))
        self.pollGPSRadioButton.setText(_translate("fsSendDialog", "Get Radio Location"))
        self.sendToAllCheckbox.setText(_translate("fsSendDialog", "Send to All"))
        self.label.setText(_translate("fsSendDialog", "Fleet ID"))
        self.deviceLabel.setText(_translate("fsSendDialog", "Device ID(s)"))
        self.label_3.setText(_translate("fsSendDialog", "Message"))
        self.label_4.setText(_translate("fsSendDialog", " 36 characters max; date and time automatically included"))
        self.label_2.setText(_translate("fsSendDialog", "Note: any of these functions (except \'Send to All\') can also be done by right-clicking a Team Tab"))
