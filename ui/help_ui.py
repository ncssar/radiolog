# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'help.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Help(object):
    def setupUi(self, Help):
        Help.setObjectName("Help")
        Help.setEnabled(True)
        Help.resize(931, 532)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Help.sizePolicy().hasHeightForWidth())
        Help.setSizePolicy(sizePolicy)
        Help.setWhatsThis("")
        self.horizontalLayoutWidget = QtWidgets.QWidget(Help)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(12, 17, 939, 504))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_7 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_7.setFont(font)
        self.label_7.setAlignment(QtCore.Qt.AlignCenter)
        self.label_7.setObjectName("label_7")
        self.verticalLayout_3.addWidget(self.label_7)
        self.hotkeysTableWidget = QtWidgets.QTableWidget(self.horizontalLayoutWidget)
        self.hotkeysTableWidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.hotkeysTableWidget.sizePolicy().hasHeightForWidth())
        self.hotkeysTableWidget.setSizePolicy(sizePolicy)
        self.hotkeysTableWidget.setMinimumSize(QtCore.QSize(435, 0))
        self.hotkeysTableWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.hotkeysTableWidget.setStyleSheet("QTableWidget::item {border-top:1px solid lightgray}")
        self.hotkeysTableWidget.setLineWidth(1)
        self.hotkeysTableWidget.setMidLineWidth(0)
        self.hotkeysTableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.hotkeysTableWidget.setAutoScroll(True)
        self.hotkeysTableWidget.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.hotkeysTableWidget.setTabKeyNavigation(False)
        self.hotkeysTableWidget.setAlternatingRowColors(False)
        self.hotkeysTableWidget.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.hotkeysTableWidget.setTextElideMode(QtCore.Qt.ElideRight)
        self.hotkeysTableWidget.setShowGrid(False)
        self.hotkeysTableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.hotkeysTableWidget.setWordWrap(True)
        self.hotkeysTableWidget.setColumnCount(3)
        self.hotkeysTableWidget.setObjectName("hotkeysTableWidget")
        self.hotkeysTableWidget.setRowCount(14)
        item = QtWidgets.QTableWidgetItem()
        self.hotkeysTableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.hotkeysTableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.hotkeysTableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.hotkeysTableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.hotkeysTableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.hotkeysTableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.hotkeysTableWidget.setVerticalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.hotkeysTableWidget.setVerticalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.hotkeysTableWidget.setVerticalHeaderItem(8, item)
        item = QtWidgets.QTableWidgetItem()
        self.hotkeysTableWidget.setVerticalHeaderItem(9, item)
        item = QtWidgets.QTableWidgetItem()
        self.hotkeysTableWidget.setVerticalHeaderItem(10, item)
        item = QtWidgets.QTableWidgetItem()
        self.hotkeysTableWidget.setVerticalHeaderItem(11, item)
        item = QtWidgets.QTableWidgetItem()
        self.hotkeysTableWidget.setVerticalHeaderItem(12, item)
        item = QtWidgets.QTableWidgetItem()
        self.hotkeysTableWidget.setVerticalHeaderItem(13, item)
        item = QtWidgets.QTableWidgetItem()
        self.hotkeysTableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setKerning(True)
        item.setFont(font)
        self.hotkeysTableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.hotkeysTableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.hotkeysTableWidget.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.hotkeysTableWidget.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(2, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.hotkeysTableWidget.setItem(2, 1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(2, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(3, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.hotkeysTableWidget.setItem(3, 1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(3, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(4, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.hotkeysTableWidget.setItem(4, 1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(4, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(5, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.hotkeysTableWidget.setItem(5, 1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(5, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(6, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.hotkeysTableWidget.setItem(6, 1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(6, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(7, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.hotkeysTableWidget.setItem(7, 1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(7, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(8, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.hotkeysTableWidget.setItem(8, 1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(8, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(9, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.hotkeysTableWidget.setItem(9, 1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(9, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(10, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.hotkeysTableWidget.setItem(10, 1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(10, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(11, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.hotkeysTableWidget.setItem(11, 1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(11, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(12, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.hotkeysTableWidget.setItem(12, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.hotkeysTableWidget.setItem(12, 2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignVCenter)
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(13, 0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.hotkeysTableWidget.setItem(13, 1, item)
        item = QtWidgets.QTableWidgetItem()
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        item.setFont(font)
        self.hotkeysTableWidget.setItem(13, 2, item)
        self.hotkeysTableWidget.horizontalHeader().setVisible(False)
        self.hotkeysTableWidget.horizontalHeader().setCascadingSectionResizes(True)
        self.hotkeysTableWidget.horizontalHeader().setDefaultSectionSize(125)
        self.hotkeysTableWidget.horizontalHeader().setHighlightSections(False)
        self.hotkeysTableWidget.horizontalHeader().setMinimumSectionSize(10)
        self.hotkeysTableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.hotkeysTableWidget.horizontalHeader().setStretchLastSection(True)
        self.hotkeysTableWidget.verticalHeader().setVisible(False)
        self.hotkeysTableWidget.verticalHeader().setCascadingSectionResizes(False)
        self.hotkeysTableWidget.verticalHeader().setDefaultSectionSize(30)
        self.verticalLayout_3.addWidget(self.hotkeysTableWidget)
        self.horizontalLayout_3.addLayout(self.verticalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.colorLabel3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.colorLabel3.setFont(font)
        self.colorLabel3.setObjectName("colorLabel3")
        self.gridLayout_2.addWidget(self.colorLabel3, 2, 1, 1, 1)
        self.colorLabel6 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.colorLabel6.setFont(font)
        self.colorLabel6.setObjectName("colorLabel6")
        self.gridLayout_2.addWidget(self.colorLabel6, 6, 1, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 4, 1, 1)
        self.colorLabel4 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.colorLabel4.setFont(font)
        self.colorLabel4.setObjectName("colorLabel4")
        self.gridLayout_2.addWidget(self.colorLabel4, 4, 1, 1, 1)
        self.colorLabel5 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.colorLabel5.setFont(font)
        self.colorLabel5.setObjectName("colorLabel5")
        self.gridLayout_2.addWidget(self.colorLabel5, 5, 1, 1, 1)
        self.colorLabel7 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.colorLabel7.setFont(font)
        self.colorLabel7.setObjectName("colorLabel7")
        self.gridLayout_2.addWidget(self.colorLabel7, 3, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_11.setFont(font)
        self.label_11.setObjectName("label_11")
        self.gridLayout_2.addWidget(self.label_11, 6, 3, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.gridLayout_2.addWidget(self.label_10, 5, 3, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_8.setFont(font)
        self.label_8.setObjectName("label_8")
        self.gridLayout_2.addWidget(self.label_8, 2, 3, 1, 1)
        self.colorLabel1 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.colorLabel1.setFont(font)
        self.colorLabel1.setObjectName("colorLabel1")
        self.gridLayout_2.addWidget(self.colorLabel1, 0, 1, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")
        self.gridLayout_2.addWidget(self.label_6, 0, 3, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_5.setFont(font)
        self.label_5.setObjectName("label_5")
        self.gridLayout_2.addWidget(self.label_5, 1, 3, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout_2.addWidget(self.label_2, 4, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout_2.addWidget(self.label_3, 3, 3, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem2, 1, 0, 1, 1)
        self.colorLabel2 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.colorLabel2.setFont(font)
        self.colorLabel2.setObjectName("colorLabel2")
        self.gridLayout_2.addWidget(self.colorLabel2, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_2)
        spacerItem3 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem3)
        self.label_14 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_14.setFont(font)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.verticalLayout.addWidget(self.label_14)
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        spacerItem4 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem4, 1, 2, 1, 1)
        self.fsAllFilteredLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.fsAllFilteredLabel.setObjectName("fsAllFilteredLabel")
        self.gridLayout_3.addWidget(self.fsAllFilteredLabel, 2, 1, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.gridLayout_3.addWidget(self.label_13, 2, 3, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.horizontalLayoutWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 1, 3, 1, 1)
        spacerItem5 = QtWidgets.QSpacerItem(20, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem5, 1, 0, 1, 1)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem6, 1, 4, 1, 1)
        self.fsSomeFilteredLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.fsSomeFilteredLabel.sizePolicy().hasHeightForWidth())
        self.fsSomeFilteredLabel.setSizePolicy(sizePolicy)
        self.fsSomeFilteredLabel.setObjectName("fsSomeFilteredLabel")
        self.gridLayout_3.addWidget(self.fsSomeFilteredLabel, 1, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout_3)
        spacerItem7 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem7)
        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.retranslateUi(Help)
        QtCore.QMetaObject.connectSlotsByName(Help)

    def retranslateUi(self, Help):
        _translate = QtCore.QCoreApplication.translate
        Help.setWindowTitle(_translate("Help", "Help"))
        self.label_7.setText(_translate("Help", "Hotkeys"))
        item = self.hotkeysTableWidget.verticalHeaderItem(0)
        item.setText(_translate("Help", "New Row"))
        item = self.hotkeysTableWidget.verticalHeaderItem(1)
        item.setText(_translate("Help", "New Row"))
        item = self.hotkeysTableWidget.verticalHeaderItem(2)
        item.setText(_translate("Help", "New Row"))
        item = self.hotkeysTableWidget.verticalHeaderItem(3)
        item.setText(_translate("Help", "New Row"))
        item = self.hotkeysTableWidget.verticalHeaderItem(4)
        item.setText(_translate("Help", "New Row"))
        item = self.hotkeysTableWidget.verticalHeaderItem(5)
        item.setText(_translate("Help", "New Row"))
        item = self.hotkeysTableWidget.verticalHeaderItem(6)
        item.setText(_translate("Help", "New Row"))
        item = self.hotkeysTableWidget.verticalHeaderItem(7)
        item.setText(_translate("Help", "New Row"))
        item = self.hotkeysTableWidget.verticalHeaderItem(8)
        item.setText(_translate("Help", "New Row"))
        item = self.hotkeysTableWidget.verticalHeaderItem(9)
        item.setText(_translate("Help", "New Row"))
        item = self.hotkeysTableWidget.verticalHeaderItem(10)
        item.setText(_translate("Help", "New Row"))
        item = self.hotkeysTableWidget.verticalHeaderItem(11)
        item.setText(_translate("Help", "New Row"))
        item = self.hotkeysTableWidget.verticalHeaderItem(12)
        item.setText(_translate("Help", "F12"))
        item = self.hotkeysTableWidget.verticalHeaderItem(13)
        item.setText(_translate("Help", "New Row"))
        item = self.hotkeysTableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Help", "Key"))
        item = self.hotkeysTableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Help", "spacer"))
        item = self.hotkeysTableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Help", "Function"))
        __sortingEnabled = self.hotkeysTableWidget.isSortingEnabled()
        self.hotkeysTableWidget.setSortingEnabled(False)
        item = self.hotkeysTableWidget.item(0, 0)
        item.setText(_translate("Help", "[number]"))
        item = self.hotkeysTableWidget.item(0, 1)
        item.setText(_translate("Help", "-"))
        item = self.hotkeysTableWidget.item(0, 2)
        item.setText(_translate("Help", "New Entry, \'FROM\' \'Team [number]\'"))
        item = self.hotkeysTableWidget.item(1, 0)
        item.setText(_translate("Help", "\'f\', [space], [Enter], [LeftArrow]"))
        item = self.hotkeysTableWidget.item(1, 1)
        item.setText(_translate("Help", "-"))
        item = self.hotkeysTableWidget.item(1, 2)
        item.setText(_translate("Help", "New Entry, \'FROM\' \'Team \'"))
        item = self.hotkeysTableWidget.item(2, 0)
        item.setText(_translate("Help", "\'t\', [RightArrow]"))
        item = self.hotkeysTableWidget.item(2, 1)
        item.setText(_translate("Help", "-"))
        item = self.hotkeysTableWidget.item(2, 2)
        item.setText(_translate("Help", "New Entry, \'TO\' \'Team \'"))
        item = self.hotkeysTableWidget.item(3, 0)
        item.setText(_translate("Help", "\'a\'"))
        item = self.hotkeysTableWidget.item(3, 1)
        item.setText(_translate("Help", "-"))
        item = self.hotkeysTableWidget.item(3, 2)
        item.setText(_translate("Help", "New Entry, \'TO\' \'All Teams\'"))
        item = self.hotkeysTableWidget.item(4, 0)
        item.setText(_translate("Help", "F1"))
        item = self.hotkeysTableWidget.item(4, 1)
        item.setText(_translate("Help", "-"))
        item = self.hotkeysTableWidget.item(4, 2)
        item.setText(_translate("Help", "Help (this window)"))
        item = self.hotkeysTableWidget.item(5, 0)
        item.setText(_translate("Help", "F2"))
        item = self.hotkeysTableWidget.item(5, 1)
        item.setText(_translate("Help", "-"))
        item = self.hotkeysTableWidget.item(5, 2)
        item.setText(_translate("Help", "Options"))
        item = self.hotkeysTableWidget.item(6, 0)
        item.setText(_translate("Help", "F3"))
        item = self.hotkeysTableWidget.item(6, 1)
        item.setText(_translate("Help", "-"))
        item = self.hotkeysTableWidget.item(6, 2)
        item.setText(_translate("Help", "Print"))
        item = self.hotkeysTableWidget.item(7, 0)
        item.setText(_translate("Help", "F4"))
        item = self.hotkeysTableWidget.item(7, 1)
        item.setText(_translate("Help", "-"))
        item = self.hotkeysTableWidget.item(7, 2)
        item.setText(_translate("Help", "Load Existing Radio Log"))
        item = self.hotkeysTableWidget.item(8, 0)
        item.setText(_translate("Help", "F5"))
        item = self.hotkeysTableWidget.item(8, 1)
        item.setText(_translate("Help", "-"))
        item = self.hotkeysTableWidget.item(8, 2)
        item.setText(_translate("Help", "Reload FleetSync Table"))
        item = self.hotkeysTableWidget.item(9, 0)
        item.setText(_translate("Help", "F6"))
        item = self.hotkeysTableWidget.item(9, 1)
        item.setText(_translate("Help", "-"))
        item = self.hotkeysTableWidget.item(9, 2)
        item.setText(_translate("Help", "Restore Last Saved Files"))
        item = self.hotkeysTableWidget.item(10, 0)
        item.setText(_translate("Help", "F7"))
        item = self.hotkeysTableWidget.item(10, 1)
        item.setText(_translate("Help", "-"))
        item = self.hotkeysTableWidget.item(10, 2)
        item.setText(_translate("Help", "FleetSync Mute Toggle"))
        item = self.hotkeysTableWidget.item(11, 0)
        item.setText(_translate("Help", "F8"))
        item = self.hotkeysTableWidget.item(11, 1)
        item.setText(_translate("Help", "-"))
        item = self.hotkeysTableWidget.item(11, 2)
        item.setText(_translate("Help", "FleetSync Filter Setup"))
        item = self.hotkeysTableWidget.item(12, 0)
        item.setText(_translate("Help", "F12"))
        item = self.hotkeysTableWidget.item(12, 1)
        item.setText(_translate("Help", "-"))
        item = self.hotkeysTableWidget.item(12, 2)
        item.setText(_translate("Help", "Toggle Team Hotkeys (disables default alphanumeric hotkeys)"))
        item = self.hotkeysTableWidget.item(13, 0)
        item.setText(_translate("Help", "+ / -"))
        item = self.hotkeysTableWidget.item(13, 1)
        item.setText(_translate("Help", "-"))
        item = self.hotkeysTableWidget.item(13, 2)
        item.setText(_translate("Help", "Enlarge / Reduce Font"))
        self.hotkeysTableWidget.setSortingEnabled(__sortingEnabled)
        self.label.setText(_translate("Help", "Color Codes"))
        self.colorLabel3.setText(_translate("Help", "Team 1"))
        self.colorLabel6.setText(_translate("Help", "Team 1"))
        self.colorLabel4.setText(_translate("Help", "Team 1"))
        self.colorLabel5.setText(_translate("Help", "Team 1"))
        self.colorLabel7.setText(_translate("Help", "Team 1"))
        self.label_11.setText(_translate("Help", "Timed Out (no recent contact)"))
        self.label_10.setText(_translate("Help", "About to Time Out"))
        self.label_8.setText(_translate("Help", "Working"))
        self.colorLabel1.setText(_translate("Help", "Team 1"))
        self.label_6.setText(_translate("Help", "At IC"))
        self.label_5.setText(_translate("Help", "In Transit"))
        self.label_2.setText(_translate("Help", "Waiting on Transport"))
        self.label_3.setText(_translate("Help", "Standing By / Awaiting Response"))
        self.colorLabel2.setText(_translate("Help", "Team 1"))
        self.label_14.setText(_translate("Help", "Other Symbols"))
        self.fsAllFilteredLabel.setText(_translate("Help", "Team 1"))
        self.label_13.setText(_translate("Help", "All of this team\'s FleetSync devices are filtered"))
        self.label_9.setText(_translate("Help", "Some of this team\'s FleetSync devices are filtered"))
        self.fsSomeFilteredLabel.setText(_translate("Help", "Team 1"))
