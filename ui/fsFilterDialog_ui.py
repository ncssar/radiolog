# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\caver\Documents\GitHub\radiolog\designer\fsFilterDialog.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_fsFilterDialog(object):
    def setupUi(self, fsFilterDialog):
        fsFilterDialog.setObjectName("fsFilterDialog")
        fsFilterDialog.resize(658, 449)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(fsFilterDialog.sizePolicy().hasHeightForWidth())
        fsFilterDialog.setSizePolicy(sizePolicy)
        fsFilterDialog.setSizeGripEnabled(False)
        self.verticalLayout = QtWidgets.QVBoxLayout(fsFilterDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(fsFilterDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(fsFilterDialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label_2.setFont(font)
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(fsFilterDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.tableView = QtWidgets.QTableView(fsFilterDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        self.tableView.setFont(font)
        self.tableView.setMidLineWidth(0)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableView.setCornerButtonEnabled(False)
        self.tableView.setObjectName("tableView")
        self.tableView.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tableView)
        self.buttonBox = QtWidgets.QDialogButtonBox(fsFilterDialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(False)
        font.setWeight(50)
        self.buttonBox.setFont(font)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(fsFilterDialog)
        self.buttonBox.rejected.connect(fsFilterDialog.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(fsFilterDialog)

    def retranslateUi(self, fsFilterDialog):
        _translate = QtCore.QCoreApplication.translate
        fsFilterDialog.setWindowTitle(_translate("fsFilterDialog", "Radio Log - FleetSync Filter Setup"))
        self.label.setText(_translate("fsFilterDialog", "FleetSync Filter Setup"))
        self.label_2.setText(_translate("fsFilterDialog", "- No New Entry dialog will be created for filtered devices."))
        self.label_3.setText(_translate("fsFilterDialog", "- Click in the \'Filtered?\' column to toggle a device\'s filter."))
