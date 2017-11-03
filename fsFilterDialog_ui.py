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
        fsFilterDialog.resize(746, 484)
        self.widget = QtWidgets.QWidget(fsFilterDialog)
        self.widget.setGeometry(QtCore.QRect(10, 10, 722, 461))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.tableView = QtWidgets.QTableView(self.widget)
        self.tableView.setSortingEnabled(True)
        self.tableView.setCornerButtonEnabled(False)
        self.tableView.setObjectName("tableView")
        self.tableView.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.tableView)
        self.buttonBox = QtWidgets.QDialogButtonBox(self.widget)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Close)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(fsFilterDialog)
        self.buttonBox.rejected.connect(fsFilterDialog.close)
        QtCore.QMetaObject.connectSlotsByName(fsFilterDialog)

    def retranslateUi(self, fsFilterDialog):
        _translate = QtCore.QCoreApplication.translate
        fsFilterDialog.setWindowTitle(_translate("fsFilterDialog", "FleetSync Filter Setup"))
        self.label.setText(_translate("fsFilterDialog", "Use this form to control FleetSync filtering per device ID.\n"
" \n"
"If an incoming call is detected from a filtered ID, no New Entry window will be created for that call."))

