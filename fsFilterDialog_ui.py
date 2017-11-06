# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'fsFilterDialog.ui'
#
# Created by: PyQt5 UI code generator 5.8.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_fsFilterDialog(object):
    def setupUi(self, fsFilterDialog):
        fsFilterDialog.setObjectName("fsFilterDialog")
        fsFilterDialog.resize(552, 484)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(fsFilterDialog.sizePolicy().hasHeightForWidth())
        fsFilterDialog.setSizePolicy(sizePolicy)
        fsFilterDialog.setSizeGripEnabled(False)
        self.layoutWidget = QtWidgets.QWidget(fsFilterDialog)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 531, 461))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(7)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget)
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
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
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
        self.tableView = QtWidgets.QTableView(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.tableView.setFont(font)
        self.tableView.setAlternatingRowColors(True)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.tableView.setCornerButtonEnabled(False)
        self.tableView.setObjectName("tableView")
        self.tableView.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tableView)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.buttonBox.setFont(font)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(fsFilterDialog)
        self.buttonBox.rejected.connect(fsFilterDialog.close)
        QtCore.QMetaObject.connectSlotsByName(fsFilterDialog)

    def retranslateUi(self, fsFilterDialog):
        _translate = QtCore.QCoreApplication.translate
        fsFilterDialog.setWindowTitle(_translate("fsFilterDialog", "Radio Log - FleetSync Filter Setup"))
        self.label.setText(_translate("fsFilterDialog", "FleetSync Filter Setup"))
        self.label_2.setText(_translate("fsFilterDialog", "- No New Entry dialog will be created for filtered devices.\n"
"- Click in the \'Filtered?\' column to toggle a device\'s filter."))

