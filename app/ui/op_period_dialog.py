import re
from gwpycore.gw_gui.gw_gui_dialogs import ICON_WARN, ask_user_to_confirm, inform_user_about_issue
from app.logic.teams import getExtTeamName, getNiceTeamName
from app.logic.entries import rreplace
import time
from gwpycore.gw_gui.gw_gui_finger_tabs import FingerTabBarWidget
from app.logic.app_state import TIMEOUT_DISPLAY_LIST, holdSec, teamStatusDict
from PyQt5 import uic
from PyQt5.QtCore import QAbstractTableModel, QEvent, QRect, QTimer, QVariant, Qt
from PyQt5.QtGui import QColor, QFont, QKeySequence, QPalette, QPixmap
from PyQt5.QtWidgets import QAbstractItemView, QDialog, QDialogButtonBox, QHBoxLayout, QHeaderView, QLabel, QSizePolicy, QTabBar, QTabWidget, QWidget
from gwpycore import AppActions
import logging

LOG = logging.getLogger('main')

OpPeriodDialogSpec = uic.loadUiType("app/ui/opPeriodDialog.ui")[0]


class opPeriodDialog(QDialog, OpPeriodDialogSpec):
    def __init__(self, parent):
        QDialog.__init__(self)
        self.setupUi(self)
        self.parent = parent
        self.currentOpPeriodField.setText(str(parent.opPeriod))
        self.newOpPeriodField.setText(str(parent.opPeriod + 1))
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
        self.setFixedSize(self.size())

    def accept(self):
        if self.printCheckBox.isChecked():
            self.parent.printDialog.exec_()  # instead of show(), to pause execution until the print dialog is closed

        if self.deleteTabsCheckBox.isChecked():
            for extTeamName in teamStatusDict:
                status = teamStatusDict[extTeamName]
                if status == "At IC":
                    self.parent.deleteTeamTab(getNiceTeamName(extTeamName))

        self.parent.opPeriod = int(self.newOpPeriodField.text())
        self.parent.opPeriodButton.setText("OP " + str(self.parent.opPeriod))
        opText = "Operational Period " + str(self.parent.opPeriod) + " Begins: " + time.strftime("%a %b %d, %Y")
        self.parent.newEntry([time.strftime("%H%M"), "", "", opText, "", "", time.time(), "", ""])
##      clueData=[number,description,team,clueTime,clueDate,self.parent.parent.opPeriod,location,instructions,radioLoc]
        self.parent.clueLog.append(['', opText, '', time.strftime("%H%M"), '', '', '', '', ''])
        self.parent.printDialog.opPeriodComboBox.addItem(self.newOpPeriodField.text())
        super(opPeriodDialog, self).accept()

