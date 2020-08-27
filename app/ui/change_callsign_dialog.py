import logging

from gwpycore.gw_gui.gw_gui_dialogs import ICON_WARN, ask_user_to_confirm
from PyQt5 import uic
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QDialog

LOG = logging.getLogger("main")

ChangeCallsignDialogSpec = uic.loadUiType("app/ui/changeCallsignDialog.ui")[0]


class changeCallsignDialog(QDialog, ChangeCallsignDialogSpec):
    openDialogCount = 0

    def __init__(self, parent, callsign, fleet, device):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.parent = parent
        self.currentCallsign = callsign
        self.fleet = int(fleet)
        self.device = int(device)

        LOG.debug("openChangeCallsignDialog called.  fleet=" + str(self.fleet) + "  dev=" + str(self.device))

        self.fleetField.setText(fleet)
        self.deviceField.setText(device)
        self.currentCallsignField.setText(callsign)
        self.newCallsignField.setFocus()
        self.newCallsignField.setText("Team  ")
        self.newCallsignField.setSelection(5, 1)
        self.fsFilterButton.clicked.connect(self.fsFilterConfirm)
        changeCallsignDialog.openDialogCount += 1
        self.setFixedSize(self.size())

    def fsFilterConfirm(self):
        if not ask_user_to_confirm("Filter (ignore) future incoming messages\n  from this FleetSync device?", icon=ICON_WARN, parent=self):
            self.close()
            return
        self.parent.parent.fsFilterEdit(self.fleet, self.device, True)
        self.close()
        # also close the related new entry dialog if its message field is blank, in the same manner as autoCleanup
        if self.parent.messageField.text() == "":
            self.parent.closeEvent(QEvent(QEvent.Close), accepted=False, force=True)

    def accept(self):
        found = False
        fleet = self.fleetField.text()
        dev = self.deviceField.text()
        newCallsign = self.newCallsignField.text()
        # change existing device entry if found, otherwise add a new entry
        for n in range(len(self.parent.parent.fsLookup)):
            entry = self.parent.parent.fsLookup[n]
            if entry[0] == fleet and entry[1] == dev:
                found = True
                self.parent.parent.fsLookup[n][2] = newCallsign
        if not found:
            self.parent.parent.fsLookup.append([fleet, dev, newCallsign])
        # set the current radio log entry teamField also
        self.parent.teamField.setText(newCallsign)
        # save the updated table (filename is set at the same times that csvFilename is set)
        self.parent.parent.fsSaveLookup()
        # change the callsign in fsLog
        self.parent.parent.fsLogUpdate(int(fleet), int(dev), newCallsign)
        # finally, pass the 'accept' signal on up the tree as usual
        changeCallsignDialog.openDialogCount -= 1
        self.parent.parent.sendPendingGet(newCallsign)
        # set the focus to the messageField of the active stack item - not always
        #  the same as the new entry, as determined by addTab
        self.parent.parent.newEntryWindow.tabWidget.currentWidget().messageField.setFocus()
        super(changeCallsignDialog, self).accept()
        LOG.debug("New callsign pairing created: fleet=" + fleet + "  dev=" + dev + "  callsign=" + newCallsign)
