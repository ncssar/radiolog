# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\caver\Documents\GitHub\radiolog\designer\teamTabsPopup.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_teamTabsPopup(object):
    def setupUi(self, teamTabsPopup):
        teamTabsPopup.setObjectName("teamTabsPopup")
        teamTabsPopup.resize(223, 308)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(11)
        teamTabsPopup.setFont(font)
        self.verticalLayout = QtWidgets.QVBoxLayout(teamTabsPopup)
        self.verticalLayout.setObjectName("verticalLayout")
        self.teamTabsTableWidget = QtWidgets.QTableWidget(teamTabsPopup)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.teamTabsTableWidget.setFont(font)
        self.teamTabsTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.teamTabsTableWidget.setObjectName("teamTabsTableWidget")
        self.teamTabsTableWidget.setColumnCount(1)
        self.teamTabsTableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.teamTabsTableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.teamTabsTableWidget.setHorizontalHeaderItem(0, item)
        self.teamTabsTableWidget.horizontalHeader().setVisible(False)
        self.teamTabsTableWidget.verticalHeader().setVisible(False)
        self.verticalLayout.addWidget(self.teamTabsTableWidget)
        self.teamTabsSummaryTableWidget = QtWidgets.QTableWidget(teamTabsPopup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.teamTabsSummaryTableWidget.sizePolicy().hasHeightForWidth())
        self.teamTabsSummaryTableWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.teamTabsSummaryTableWidget.setFont(font)
        self.teamTabsSummaryTableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.teamTabsSummaryTableWidget.setObjectName("teamTabsSummaryTableWidget")
        self.teamTabsSummaryTableWidget.setColumnCount(1)
        self.teamTabsSummaryTableWidget.setRowCount(7)
        item = QtWidgets.QTableWidgetItem()
        self.teamTabsSummaryTableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.teamTabsSummaryTableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.teamTabsSummaryTableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.teamTabsSummaryTableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.teamTabsSummaryTableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.teamTabsSummaryTableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.teamTabsSummaryTableWidget.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.teamTabsSummaryTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.teamTabsSummaryTableWidget.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.teamTabsSummaryTableWidget.setItem(6, 0, item)
        self.teamTabsSummaryTableWidget.horizontalHeader().setVisible(False)
        self.teamTabsSummaryTableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.teamTabsSummaryTableWidget.horizontalHeader().setDefaultSectionSize(40)
        self.teamTabsSummaryTableWidget.horizontalHeader().setMinimumSectionSize(40)
        self.teamTabsSummaryTableWidget.verticalHeader().setDefaultSectionSize(25)
        self.verticalLayout.addWidget(self.teamTabsSummaryTableWidget)

        self.retranslateUi(teamTabsPopup)
        QtCore.QMetaObject.connectSlotsByName(teamTabsPopup)

    def retranslateUi(self, teamTabsPopup):
        _translate = QtCore.QCoreApplication.translate
        teamTabsPopup.setWindowTitle(_translate("teamTabsPopup", "Callsigns"))
        item = self.teamTabsTableWidget.verticalHeaderItem(0)
        item.setText(_translate("teamTabsPopup", "starter"))
        item = self.teamTabsTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("teamTabsPopup", "starter"))
        item = self.teamTabsSummaryTableWidget.verticalHeaderItem(0)
        item.setText(_translate("teamTabsPopup", "At IC"))
        item = self.teamTabsSummaryTableWidget.verticalHeaderItem(1)
        item.setText(_translate("teamTabsPopup", "In Transit"))
        item = self.teamTabsSummaryTableWidget.verticalHeaderItem(2)
        item.setText(_translate("teamTabsPopup", "Working"))
        item = self.teamTabsSummaryTableWidget.verticalHeaderItem(3)
        item.setText(_translate("teamTabsPopup", "Wtng.ForTrans."))
        item = self.teamTabsSummaryTableWidget.verticalHeaderItem(4)
        item.setText(_translate("teamTabsPopup", "STANDBY"))
        item = self.teamTabsSummaryTableWidget.verticalHeaderItem(5)
        item.setText(_translate("teamTabsPopup", "Total"))
        item = self.teamTabsSummaryTableWidget.verticalHeaderItem(6)
        item.setText(_translate("teamTabsPopup", "Not At IC"))
        item = self.teamTabsSummaryTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("teamTabsPopup", "Count"))
        __sortingEnabled = self.teamTabsSummaryTableWidget.isSortingEnabled()
        self.teamTabsSummaryTableWidget.setSortingEnabled(False)
        self.teamTabsSummaryTableWidget.setSortingEnabled(__sortingEnabled)
