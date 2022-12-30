# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\caver\Documents\GitHub\radiolog\designer\radiolog.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1276, 676)
        self.gridLayout_2 = QtWidgets.QGridLayout(Dialog)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.incidentNameLabel = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.incidentNameLabel.sizePolicy().hasHeightForWidth())
        self.incidentNameLabel.setSizePolicy(sizePolicy)
        self.incidentNameLabel.setMinimumSize(QtCore.QSize(225, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.incidentNameLabel.setFont(font)
        self.incidentNameLabel.setObjectName("incidentNameLabel")
        self.horizontalLayout.addWidget(self.incidentNameLabel)
        self.comPortLayoutWidget = QtWidgets.QWidget(Dialog)
        self.comPortLayoutWidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comPortLayoutWidget.sizePolicy().hasHeightForWidth())
        self.comPortLayoutWidget.setSizePolicy(sizePolicy)
        self.comPortLayoutWidget.setObjectName("comPortLayoutWidget")
        self.comPortSectionLayout = QtWidgets.QVBoxLayout(self.comPortLayoutWidget)
        self.comPortSectionLayout.setContentsMargins(2, 2, 2, 2)
        self.comPortSectionLayout.setSpacing(2)
        self.comPortSectionLayout.setObjectName("comPortSectionLayout")
        self.fsEnableLayout = QtWidgets.QHBoxLayout()
        self.fsEnableLayout.setObjectName("fsEnableLayout")
        self.fsCheckBox = QtWidgets.QCheckBox(self.comPortLayoutWidget)
        self.fsCheckBox.setMaximumSize(QtCore.QSize(16777215, 24))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.fsCheckBox.setFont(font)
        self.fsCheckBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.fsCheckBox.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.fsCheckBox.setStyleSheet("border:3px inset lightgray")
        self.fsCheckBox.setIconSize(QtCore.QSize(20, 20))
        self.fsCheckBox.setChecked(True)
        self.fsCheckBox.setTristate(True)
        self.fsCheckBox.setObjectName("fsCheckBox")
        self.fsEnableLayout.addWidget(self.fsCheckBox)
        self.comPortSectionLayout.addLayout(self.fsEnableLayout)
        self.comPortLightsLayout = QtWidgets.QHBoxLayout()
        self.comPortLightsLayout.setContentsMargins(-1, 0, -1, -1)
        self.comPortLightsLayout.setSpacing(7)
        self.comPortLightsLayout.setObjectName("comPortLightsLayout")
        self.firstComPortField = QtWidgets.QLineEdit(self.comPortLayoutWidget)
        self.firstComPortField.setEnabled(False)
        self.firstComPortField.setMaximumSize(QtCore.QSize(20, 16))
        font = QtGui.QFont()
        font.setPointSize(4)
        self.firstComPortField.setFont(font)
        self.firstComPortField.setObjectName("firstComPortField")
        self.comPortLightsLayout.addWidget(self.firstComPortField)
        self.secondComPortField = QtWidgets.QLineEdit(self.comPortLayoutWidget)
        self.secondComPortField.setEnabled(False)
        self.secondComPortField.setMaximumSize(QtCore.QSize(20, 16))
        font = QtGui.QFont()
        font.setPointSize(4)
        self.secondComPortField.setFont(font)
        self.secondComPortField.setObjectName("secondComPortField")
        self.comPortLightsLayout.addWidget(self.secondComPortField)
        self.comPortSectionLayout.addLayout(self.comPortLightsLayout)
        self.horizontalLayout.addWidget(self.comPortLayoutWidget)
        self.opPeriodButton = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.opPeriodButton.sizePolicy().hasHeightForWidth())
        self.opPeriodButton.setSizePolicy(sizePolicy)
        self.opPeriodButton.setMinimumSize(QtCore.QSize(80, 0))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.opPeriodButton.setFont(font)
        self.opPeriodButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.opPeriodButton.setIconSize(QtCore.QSize(20, 20))
        self.opPeriodButton.setObjectName("opPeriodButton")
        self.horizontalLayout.addWidget(self.opPeriodButton)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton.setToolTip("")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.addNonRadioClueButton = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.addNonRadioClueButton.setFont(font)
        self.addNonRadioClueButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.addNonRadioClueButton.setToolTip("")
        self.addNonRadioClueButton.setObjectName("addNonRadioClueButton")
        self.horizontalLayout.addWidget(self.addNonRadioClueButton)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.clueLogButton = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.clueLogButton.setFont(font)
        self.clueLogButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.clueLogButton.setToolTip("")
        self.clueLogButton.setObjectName("clueLogButton")
        self.horizontalLayout.addWidget(self.clueLogButton)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem3)
        self.timeoutLabel = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.timeoutLabel.setFont(font)
        self.timeoutLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.timeoutLabel.setObjectName("timeoutLabel")
        self.horizontalLayout.addWidget(self.timeoutLabel)
        self.line = QtWidgets.QFrame(Dialog)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.datumFormatLabel = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.datumFormatLabel.setFont(font)
        self.datumFormatLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.datumFormatLabel.setObjectName("datumFormatLabel")
        self.horizontalLayout.addWidget(self.datumFormatLabel)
        self.clock = QtWidgets.QLCDNumber(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.clock.sizePolicy().hasHeightForWidth())
        self.clock.setSizePolicy(sizePolicy)
        self.clock.setMinimumSize(QtCore.QSize(115, 0))
        self.clock.setMaximumSize(QtCore.QSize(200, 16777215))
        self.clock.setObjectName("clock")
        self.horizontalLayout.addWidget(self.clock)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.optionsButton = QtWidgets.QToolButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.optionsButton.sizePolicy().hasHeightForWidth())
        self.optionsButton.setSizePolicy(sizePolicy)
        self.optionsButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.optionsButton.setToolTip("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/radiolog_ui/icons/options_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.optionsButton.setIcon(icon)
        self.optionsButton.setIconSize(QtCore.QSize(30, 30))
        self.optionsButton.setObjectName("optionsButton")
        self.verticalLayout_4.addWidget(self.optionsButton)
        self.printButton = QtWidgets.QToolButton(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.printButton.sizePolicy().hasHeightForWidth())
        self.printButton.setSizePolicy(sizePolicy)
        self.printButton.setMinimumSize(QtCore.QSize(0, 0))
        self.printButton.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        self.printButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.printButton.setToolTip("")
        self.printButton.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/radiolog_ui/icons/print_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.printButton.setIcon(icon1)
        self.printButton.setIconSize(QtCore.QSize(30, 30))
        self.printButton.setObjectName("printButton")
        self.verticalLayout_4.addWidget(self.printButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout_4)
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.helpButton = QtWidgets.QToolButton(Dialog)
        self.helpButton.setFocusPolicy(QtCore.Qt.NoFocus)
        self.helpButton.setToolTip("")
        self.helpButton.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/radiolog_ui/icons/help_icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.helpButton.setIcon(icon2)
        self.helpButton.setIconSize(QtCore.QSize(30, 30))
        self.helpButton.setObjectName("helpButton")
        self.verticalLayout_5.addWidget(self.helpButton)
        self.fsFilterButton = QtWidgets.QToolButton(Dialog)
        self.fsFilterButton.setFocusPolicy(QtCore.Qt.NoFocus)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/radiolog_ui/icons/empty_filter.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.fsFilterButton.setIcon(icon3)
        self.fsFilterButton.setIconSize(QtCore.QSize(30, 30))
        self.fsFilterButton.setObjectName("fsFilterButton")
        self.verticalLayout_5.addWidget(self.fsFilterButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout_5)
        self.loginWidget = clickableWidget(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loginWidget.sizePolicy().hasHeightForWidth())
        self.loginWidget.setSizePolicy(sizePolicy)
        self.loginWidget.setMinimumSize(QtCore.QSize(80, 80))
        self.loginWidget.setMaximumSize(QtCore.QSize(80, 80))
        self.loginWidget.setStyleSheet("QWidget#loginWidget {\n"
"    background-image: url(:/radiolog_ui/icons/user_icon_80px.png);\n"
"}\n"
"QWidget#loginWidget:hover{\n"
"    background-image: url(:/radiolog_ui/icons/user_icon_blue_80px.png);\n"
"}")
        self.loginWidget.setObjectName("loginWidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.loginWidget)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.loginInitialsLabel = QtWidgets.QLabel(self.loginWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.loginInitialsLabel.setFont(font)
        self.loginInitialsLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.loginInitialsLabel.setObjectName("loginInitialsLabel")
        self.verticalLayout_6.addWidget(self.loginInitialsLabel)
        self.loginIdLabel = QtWidgets.QLabel(self.loginWidget)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(10)
        self.loginIdLabel.setFont(font)
        self.loginIdLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.loginIdLabel.setObjectName("loginIdLabel")
        self.verticalLayout_6.addWidget(self.loginIdLabel)
        self.horizontalLayout_2.addWidget(self.loginWidget)
        self.horizontalLayout.addLayout(self.horizontalLayout_2)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.splitter = QtWidgets.QSplitter(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setStyleSheet("QSplitter::handle{image:url(icons/SplitterPanelIcon.png)}")
        self.splitter.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.splitter.setMidLineWidth(-1)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setHandleWidth(6)
        self.splitter.setChildrenCollapsible(False)
        self.splitter.setObjectName("splitter")
        self.tableView = CustomTableView(self.splitter)
        font = QtGui.QFont()
        font.setPointSize(9)
        self.tableView.setFont(font)
        self.tableView.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setTabKeyNavigation(False)
        self.tableView.setProperty("showDropIndicator", False)
        self.tableView.setAlternatingRowColors(False)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setTextElideMode(QtCore.Qt.ElideNone)
        self.tableView.setVerticalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.tableView.setObjectName("tableView")
        self.tableView.verticalHeader().setVisible(False)
        self.frame = QtWidgets.QFrame(self.splitter)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.teamHotkeysWidget = QtWidgets.QWidget(self.frame)
        self.teamHotkeysWidget.setObjectName("teamHotkeysWidget")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.teamHotkeysWidget)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.teamHotkeysHLayout = QtWidgets.QHBoxLayout()
        self.teamHotkeysHLayout.setSpacing(0)
        self.teamHotkeysHLayout.setObjectName("teamHotkeysHLayout")
        self.verticalLayout_3.addLayout(self.teamHotkeysHLayout)
        self.verticalLayout_2.addWidget(self.teamHotkeysWidget)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.frame)
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        self.tabWidget.setFont(font)
        self.tabWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setTabPosition(QtWidgets.QTabWidget.North)
        self.tabWidget.setTabShape(QtWidgets.QTabWidget.Rounded)
        self.tabWidget.setIconSize(QtCore.QSize(10, 20))
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setObjectName("tabWidget")
        self.verticalLayout.addWidget(self.tabWidget)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.gridLayout_2.addWidget(self.splitter, 1, 0, 1, 1)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(-1)
        self.fsCheckBox.stateChanged['int'].connect(Dialog.fsCheckBoxCB) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.pushButton, self.tableView)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Radio Log"))
        self.incidentNameLabel.setText(_translate("Dialog", "New Incident"))
        self.fsCheckBox.setText(_translate("Dialog", "FS"))
        self.opPeriodButton.setToolTip(_translate("Dialog", "Change Operational Period"))
        self.opPeriodButton.setText(_translate("Dialog", "OP 1"))
        self.pushButton.setText(_translate("Dialog", " Add Entry "))
        self.addNonRadioClueButton.setText(_translate("Dialog", " Non-Radio Clue "))
        self.clueLogButton.setText(_translate("Dialog", " Clue Log "))
        self.timeoutLabel.setToolTip(_translate("Dialog", "Flashing red begins after this much time without contact"))
        self.timeoutLabel.setText(_translate("Dialog", "TIMEOUT:\n"
"10sec"))
        self.datumFormatLabel.setText(_translate("Dialog", "DATUM\n"
"FORMAT"))
        self.optionsButton.setShortcut(_translate("Dialog", "F2"))
        self.helpButton.setShortcut(_translate("Dialog", "F1"))
        self.fsFilterButton.setText(_translate("Dialog", "..."))
        self.loginInitialsLabel.setText(_translate("Dialog", "?"))
        self.loginIdLabel.setText(_translate("Dialog", "???"))
from radiolog import CustomTableView, clickableWidget
import radiolog_ui_rc
