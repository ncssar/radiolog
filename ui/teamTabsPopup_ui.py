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
        teamTabsPopup.resize(154, 238)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(teamTabsPopup.sizePolicy().hasHeightForWidth())
        teamTabsPopup.setSizePolicy(sizePolicy)
        teamTabsPopup.setMinimumSize(QtCore.QSize(153, 0))
        teamTabsPopup.setAutoFillBackground(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(teamTabsPopup)
        self.verticalLayout.setContentsMargins(5, 5, 5, 5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(teamTabsPopup)
        self.frame.setAutoFillBackground(False)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(2)
        self.frame.setMidLineWidth(0)
        self.frame.setObjectName("frame")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.teamTabsTableWidget = QtWidgets.QTableWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.teamTabsTableWidget.sizePolicy().hasHeightForWidth())
        self.teamTabsTableWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.teamTabsTableWidget.setFont(font)
        self.teamTabsTableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.teamTabsTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.teamTabsTableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.teamTabsTableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.teamTabsTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.teamTabsTableWidget.setTabKeyNavigation(False)
        self.teamTabsTableWidget.setProperty("showDropIndicator", False)
        self.teamTabsTableWidget.setDragDropOverwriteMode(False)
        self.teamTabsTableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.teamTabsTableWidget.setObjectName("teamTabsTableWidget")
        self.teamTabsTableWidget.setColumnCount(1)
        self.teamTabsTableWidget.setRowCount(1)
        item = QtWidgets.QTableWidgetItem()
        self.teamTabsTableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.teamTabsTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsEnabled)
        self.teamTabsTableWidget.setItem(0, 0, item)
        self.teamTabsTableWidget.horizontalHeader().setVisible(False)
        self.teamTabsTableWidget.verticalHeader().setVisible(False)
        self.teamTabsTableWidget.verticalHeader().setDefaultSectionSize(25)
        self.teamTabsTableWidget.verticalHeader().setMinimumSectionSize(25)
        self.verticalLayout_3.addWidget(self.teamTabsTableWidget)
        self.teamTabsSummaryTableWidget = QtWidgets.QTableWidget(self.frame)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.teamTabsSummaryTableWidget.sizePolicy().hasHeightForWidth())
        self.teamTabsSummaryTableWidget.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.teamTabsSummaryTableWidget.setFont(font)
        self.teamTabsSummaryTableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.teamTabsSummaryTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.teamTabsSummaryTableWidget.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.teamTabsSummaryTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.teamTabsSummaryTableWidget.setTabKeyNavigation(False)
        self.teamTabsSummaryTableWidget.setProperty("showDropIndicator", False)
        self.teamTabsSummaryTableWidget.setDragDropOverwriteMode(False)
        self.teamTabsSummaryTableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.teamTabsSummaryTableWidget.setObjectName("teamTabsSummaryTableWidget")
        self.teamTabsSummaryTableWidget.setColumnCount(1)
        self.teamTabsSummaryTableWidget.setRowCount(6)
        item = QtWidgets.QTableWidgetItem()
        self.teamTabsSummaryTableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.teamTabsSummaryTableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.teamTabsSummaryTableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(150, 150, 150))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.teamTabsSummaryTableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.teamTabsSummaryTableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.teamTabsSummaryTableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.teamTabsSummaryTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        brush = QtGui.QBrush(QtGui.QColor(150, 150, 150))
        brush.setStyle(QtCore.Qt.SolidPattern)
        item.setForeground(brush)
        self.teamTabsSummaryTableWidget.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.teamTabsSummaryTableWidget.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.teamTabsSummaryTableWidget.setItem(5, 0, item)
        self.teamTabsSummaryTableWidget.horizontalHeader().setVisible(False)
        self.teamTabsSummaryTableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.teamTabsSummaryTableWidget.horizontalHeader().setDefaultSectionSize(40)
        self.teamTabsSummaryTableWidget.horizontalHeader().setHighlightSections(False)
        self.teamTabsSummaryTableWidget.horizontalHeader().setMinimumSectionSize(40)
        self.teamTabsSummaryTableWidget.verticalHeader().setDefaultSectionSize(22)
        self.teamTabsSummaryTableWidget.verticalHeader().setHighlightSections(False)
        self.teamTabsSummaryTableWidget.verticalHeader().setMinimumSectionSize(22)
        self.verticalLayout_3.addWidget(self.teamTabsSummaryTableWidget)
        self.verticalLayout.addWidget(self.frame)

        self.retranslateUi(teamTabsPopup)
        QtCore.QMetaObject.connectSlotsByName(teamTabsPopup)

    def retranslateUi(self, teamTabsPopup):
        _translate = QtCore.QCoreApplication.translate
        teamTabsPopup.setWindowTitle(_translate("teamTabsPopup", "Dialog"))
        item = self.teamTabsTableWidget.verticalHeaderItem(0)
        item.setText(_translate("teamTabsPopup", "starter"))
        item = self.teamTabsTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("teamTabsPopup", "starter"))
        __sortingEnabled = self.teamTabsTableWidget.isSortingEnabled()
        self.teamTabsTableWidget.setSortingEnabled(False)
        self.teamTabsTableWidget.setSortingEnabled(__sortingEnabled)
        item = self.teamTabsSummaryTableWidget.verticalHeaderItem(0)
        item.setText(_translate("teamTabsPopup", "At IC"))
        item = self.teamTabsSummaryTableWidget.verticalHeaderItem(1)
        item.setText(_translate("teamTabsPopup", "In Transit"))
        item = self.teamTabsSummaryTableWidget.verticalHeaderItem(2)
        item.setText(_translate("teamTabsPopup", "Working"))
        item = self.teamTabsSummaryTableWidget.verticalHeaderItem(3)
        item.setText(_translate("teamTabsPopup", "Other"))
        item = self.teamTabsSummaryTableWidget.verticalHeaderItem(4)
        item.setText(_translate("teamTabsPopup", "Total"))
        item = self.teamTabsSummaryTableWidget.verticalHeaderItem(5)
        item.setText(_translate("teamTabsPopup", "Not At IC"))
        item = self.teamTabsSummaryTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("teamTabsPopup", "Count"))
        __sortingEnabled = self.teamTabsSummaryTableWidget.isSortingEnabled()
        self.teamTabsSummaryTableWidget.setSortingEnabled(False)
        self.teamTabsSummaryTableWidget.setSortingEnabled(__sortingEnabled)
