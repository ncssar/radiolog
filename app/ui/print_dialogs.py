from gwpycore.gw_gui.gw_gui_dialogs import inform_user_about_issue
from app.logic.app_state import TIMEOUT_DISPLAY_LIST
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QHeaderView
from gwpycore import AppActions
import logging

LOG = logging.getLogger('main')

PrintDialogSpec = uic.loadUiType("app/ui/printDialog.ui")[0]
PrintClueLogDialogSpec = uic.loadUiType("app/ui/printClueLogDialog.ui")[0]

class PrintDialog(QDialog, PrintDialogSpec):
    def __init__(self, parent):
        QDialog.__init__(self)
        self.parent = parent
        self.setupUi(self)
        self.opPeriodComboBox.addItem("1")
        self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
        self.setFixedSize(self.size())

    def showEvent(self, event):
        LOG.debug("show event called")
        LOG.debug("teamNameList:" + str(self.parent.teamNameList))
        LOG.debug("allTeamsList:" + str(self.parent.allTeamsList))
        if self.parent.exitClicked:
            self.buttonBox.button(QDialogButtonBox.Ok).setText("Print")
            self.buttonBox.button(QDialogButtonBox.Cancel).setText("Exit without printing")
        else:
            self.buttonBox.button(QDialogButtonBox.Ok).setText("Ok")
            self.buttonBox.button(QDialogButtonBox.Cancel).setText("Cancel")
        if len(self.parent.clueLog) > 0:
            self.clueLogField.setChecked(True)
            self.clueLogField.setEnabled(True)
        else:
            self.clueLogField.setChecked(False)
            self.clueLogField.setEnabled(False)
        self.opPeriodComboBox.setCurrentIndex(self.opPeriodComboBox.count() - 1)

    def accept(self):
        opPeriod = self.opPeriodComboBox.currentText()
        if self.radioLogField.isChecked():
            LOG.debug("PRINT radio log")
            self.parent.printLog(opPeriod)
        if self.teamRadioLogsField.isChecked():
            LOG.debug("PRINT team radio logs")
            self.parent.printTeamLogs(opPeriod)
        if self.clueLogField.isChecked():
            LOG.debug("PRINT clue log")
# 			LOG.debug("  printDialog.accept.clueLog.trace1")
            self.parent.printClueLog(opPeriod)
# 			LOG.debug("  printDialog.accept.clueLog.trace2")
# 		LOG.debug("  printDialog.accept.end.trace1")
        super(PrintDialog, self).accept()
# 		LOG.debug("  printDialog.accept.end.trace2")


class printClueLogDialog(QDialog, PrintClueLogDialogSpec):
    def __init__(self, parent):
        QDialog.__init__(self)
        self.setupUi(self)
        self.parent = parent
        self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)

    def showEvent(self, event):
        itemsToAdd = self.parent.opsWithClues
        if len(itemsToAdd) == 0:
            itemsToAdd = ['--']
        self.opPeriodComboBox.clear()
        self.opPeriodComboBox.addItems(itemsToAdd)

    def accept(self):
        opPeriod = self.opPeriodComboBox.currentText()
        LOG.trace("Open printClueLogDialog.accept")
        if opPeriod == '--':
            inform_user_about_issue("There are no clues to print.", title="No Clues to Print", parent=self)
            self.reject()
        else:
            self.parent.printClueLog(opPeriod)
            LOG.trace("Called parent printClueLogDialog.accept")
            super(printClueLogDialog, self).accept()
            LOG.trace("Called super printClueLogDialog.accept")

# actions to be performed when changing the operational period:
# - bring up print dialog for current OP if checked (and wait until it is closed)
# - delete team tabs for 'At IC' teams if checked
# - change the OP variable
# - change the OP button text
# - add radio log entry (and clue log entry) 'Operational Period # Begins: <date>'
# - add new op period to list of available op periods in print dialog

# other parts of the flow that are dependent on operational period:
# - print tools use the 'Operational Period # Begins:' entry to filter rows to print
# - clue dialog and clue log
# - filenames:
#  - radio log .csv, clue log .csv - do NOT include op period in filename, since
#        one file per incident includes all op periods
#  - generated radio log and clue log pdf - DO include op period in filename,
#        since each pdf only covers one op period
