from app.logic.app_state import CONFIG, TIMEOUT_DISPLAY_LIST
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
import logging

LOG = logging.getLogger('main')

OptionsDialogSpec = uic.loadUiType("app/ui/options.ui")[0]


class OptionsDialog(QDialog, OptionsDialogSpec):
    def __init__(self, parent):
        QDialog.__init__(self)
        self.parent = parent
        self.setupUi(self)
        self.timeoutField.valueChanged.connect(self.displayTimeout)
        self.displayTimeout()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
##		self.setAttribute(Qt.WA_DeleteOnClose)
        self.datumField.setEnabled(False)  # since convert menu is not working yet, TMG 4-8-15
        self.formatField.setEnabled(False)  # since convert menu is not working yet, TMG 4-8-15
        self.setFixedSize(self.size())
        self.secondWorkingDirCB()

    def showEvent(self, event):
        # clear focus from all fields, otherwise previously edited field gets focus on next show,
        # which could lead to accidental editing
        self.incidentField.clearFocus()
        self.datumField.clearFocus()
        self.formatField.clearFocus()
        self.timeoutField.clearFocus()
        self.secondWorkingDirCheckBox.clearFocus()

    def displayTimeout(self):
        self.timeoutLabel.setText("Timeout: " + TIMEOUT_DISPLAY_LIST[self.timeoutField.value()][0])

    def secondWorkingDirCB(self):
        self.parent.use2WD = self.secondWorkingDirCheckBox.isChecked()
        CONFIG.use2WD = self.secondWorkingDirCheckBox.isChecked()

    def accept(self):
        # only save the rc file when the options dialog is accepted interactively;
        #  saving from self.optionsAccepted causes errors because that function
        #  is called during init, before the values are ready to save
        self.parent.saveRcFile()
        super(OptionsDialog, self).accept()
