import logging
import re
import time

from gwpycore import ICON_WARN, ask_user_to_confirm, inform_user_about_issue
from PyQt5 import uic
from PyQt5.QtCore import QEvent, Qt
from PyQt5.QtWidgets import QDialog

LOG = logging.getLogger("main")

SubjectLocatedDialog = uic.loadUiType("app/ui/subjectLocatedDialog.ui")[0]


class subjectLocatedDialog(QDialog, SubjectLocatedDialog):
    openDialogCount = 0

    def __init__(self, parent, t, callsign, radioLoc):
        QDialog.__init__(self)
        self.setupUi(self)
        self.timeField.setText(t)
        self.dateField.setText(time.strftime("%x"))
        self.callsignField.setText(callsign)
        self.radioLocField.setText(re.sub("  +", "\n", radioLoc))
        self.parent = parent
        self.parent.subjectLocatedDialogOpen = True
        self.parent.childDialogs.append(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.locationField.setFocus()
        self.values = self.parent.getValues()
        self.values[3] = "RADIO LOG SOFTWARE: 'SUBJECT LOCATED' button pressed; radio operator is gathering details"
        self.parent.parent.newEntry(self.values)
        subjectLocatedDialog.openDialogCount += 1
        self.setFixedSize(self.size())

    def accept(self):
        location = self.locationField.text()
        condition = self.conditionField.toPlainText()
        resources = self.resourcesField.toPlainText()
        other = self.otherField.toPlainText()
        team = self.callsignField.text()
        subjDate = self.dateField.text()
        subjTime = self.timeField.text()
        radioLoc = self.radioLocField.toPlainText()

        # validation: description, location, instructions fields must all be non-blank
        vText = ""
        if location == "":
            vText += "\n'Location' cannot be blank."
        if condition == "":
            vText += "\n'Condition' cannot be blank."
        if resources == "":
            vText += "\n'Resources Needed' cannot be blank."
        LOG.debug("vText:" + vText)
        if vText:
            inform_user_about_issue("Please complete the form and try again:\n" + vText, parent=self)
            return

        textToAdd = ""
        existingText = self.parent.messageField.text()
        if existingText != "":
            textToAdd = "; "
        textToAdd += "SUBJECT LOCATED: LOCATION: " + location + "; CONDITION: " + condition + "; RESOURCES NEEDED: " + resources
        if other != "":
            textToAdd += "; " + other
        self.parent.messageField.setText(existingText + textToAdd)
        self.closeEvent(QEvent(QEvent.Close), True)
        super(subjectLocatedDialog, self).accept()

    # 	def reject(self):
    # 		LOG.debug("rejected - calling close")
    # 		# don't try self.close() here - it can cause the dialog to never close!  Instead use super().reject()
    # 		self.closeEvent(None)
    # 		self.values=self.parent.getValues()
    # 		self.values[3]="RADIO LOG SOFTWARE: radio operator has canceled the 'SUBJECT LOCATED' form"
    # 		self.parent.parent.newEntry(self.values)
    # 		super(subjectLocatedDialog,self).reject()

    def closeEvent(self, event, accepted=False):
        # note, this type of messagebox is needed to show above all other dialogs for this application,
        #  even the ones that have WindowStaysOnTopHint.  This works in Vista 32 home basic.
        #  if it didn't show up on top, then, there would be no way to close the radiolog other than kill.
        if not accepted:
            if not ask_user_to_confirm("Close this Subject Located form?\nIt cannot be recovered.", icon=ICON_WARN, parent=self):
                event.ignore()
                return
            self.values = self.parent.getValues()
            self.values[3] = "RADIO LOG SOFTWARE: radio operator has canceled the 'SUBJECT LOCATED' form"
            self.parent.parent.newEntry(self.values)
        self.parent.subjectLocatedDialogOpen = False
        subjectLocatedDialog.openDialogCount -= 1
        self.parent.childDialogs.remove(self)
        if accepted:
            self.parent.accept()

    # fix issue #338: prevent 'esc' from closing the newEntryWindow
    def keyPressEvent(self, event):
        if event.key() != Qt.Key_Escape:
            super().keyPressEvent(event)  # pass the event as normal
