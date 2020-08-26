from app.printing.print_clue_report import printClueReport
import re
from gwpycore.gw_gui.gw_gui_dialogs import ICON_WARN, ask_user_to_confirm, inform_user_about_issue
from app.logic.entries import rreplace
import time
from app.logic.app_state import lastClueNumber
from PyQt5 import uic
from PyQt5.QtCore import QAbstractTableModel, QEvent, QVariant, Qt
from PyQt5.QtGui import QKeySequence, QPixmap
from PyQt5.QtWidgets import QAbstractItemView, QDialog, QHeaderView
import logging

LOG = logging.getLogger('main')

ClueDialogSpec = uic.loadUiType("app/ui/clueDialog.ui")[0]
ClueLogDialogSpec = uic.loadUiType("app/ui/clueLogDialog.ui")[0]
NonRadioClueDialogSpec = uic.loadUiType("app/ui/nonRadioClueDialog.ui")[0]

class clueDialog(QDialog, ClueDialogSpec):
    ##	instances=[]
    openDialogCount = 0
    indices = [False] * 20  # allow up to 20 clue dialogs open at the same time
    dx = 20
    dy = 20
    x0 = 200
    y0 = 200

    def __init__(self, parent, t, callsign, radioLoc, newClueNumber):
        QDialog.__init__(self)
        self.setupUi(self)
        self.timeField.setText(t)
        self.dateField.setText(time.strftime("%x"))
        self.callsignField.setText(callsign)
        self.radioLocField.setText(re.sub('  +', '\n', radioLoc))
        self.clueNumberField.setText(str(newClueNumber))
        self.clueQuickTextAddedStack = []
        self.parent = parent
        self.parent.childDialogs.append(self)
##		self.parent.timer.stop() # do not timeout the new entry dialog if it has a child clueDialog open!
        self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
##		self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.descriptionField.setFocus()
##		self.i=0 # dialog box location index; set at runtime, so we know which index to free on close
##		clueDialog.instances.append(self)
        [x, y, i] = self.pickXYI()
        self.move(x, y)
        self.i = i  # save the index so we can clear it on close
        # save the clue number at init time, so that any new clueDialog opened before this one
        #  is saved will have an incremented clue number.  May need to get fancier in terms
        #  of releasing clue numbers on reject, but, don't worry about it for now - that's why
        #  the clue number field is editable.
        lastClueNumber = newClueNumber
        self.parent.clueDialogOpen = True
        clueDialog.openDialogCount += 1
        self.values = self.parent.getValues()
        amendText = ""
        if self.parent.amendFlag:
            amendText = " during amendment of previous message"
        self.values[3] = "RADIO LOG SOFTWARE: 'LOCATED A CLUE' button pressed" + amendText + "; radio operator is gathering details"
##		self.values[3]="RADIO LOG SOFTWARE: 'LOCATED A CLUE' button pressed for '"+self.values[2]+"'; radio operator is gathering details"
##		self.values[2]='' # this message is not actually from a team
        self.parent.parent.newEntry(self.values)
        self.setFixedSize(self.size())

    def pickXYI(self):
        for index in range(len(clueDialog.indices)):
            if clueDialog.indices[index] == False:
                clueDialog.indices[index] = True
                return [index * clueDialog.dx + clueDialog.x0, index * clueDialog.dy + clueDialog.y0, index]

    # treat Enter or Return like Tab: cycle through fields similar to tab sequence, and accept after last field
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Enter or key == Qt.Key_Return:
            if self.descriptionField.hasFocus():
                self.locationField.setFocus()
            elif self.locationField.hasFocus():  # make sure this is elif, not if - otherwise it just cascades!
                self.instructionsField.setFocus()
            elif self.instructionsField.hasFocus():
                self.accept()
            else:
                super().keyPressEvent(event)  # pass the event as normal
        else:
            # fix issue #338: prevent 'esc' from closing the newEntryWindow
            if event.key() != Qt.Key_Escape:
                super().keyPressEvent(event)  # pass the event as normal

    def accept(self):
        ##		self.parent.timer.start(newEntryDialogTimeoutSeconds*1000) # reset the timeout
        number = self.clueNumberField.text()
        description = self.descriptionField.toPlainText()
        location = self.locationField.text()
        instructions = self.instructionsField.text()
        team = self.callsignField.text()
        clueDate = self.dateField.text()
        clueTime = self.timeField.text()
        radioLoc = self.radioLocField.toPlainText()

        # validation: description, location, instructions fields must all be non-blank
        vText = ""
        if description == "":
            vText += "\n'Description' cannot be blank."
        if location == "":
            vText += "\n'Location' cannot be blank."
        if instructions == "":
            vText += "\n'Instructions' cannot be blank."
        LOG.debug("vText:" + vText)
        if vText:
            inform_user_about_issue("Please complete the form and try again:\n" + vText, parent=self)
            return

        self.parent.clueLogNeedsPrint = True
        textToAdd = ''
        existingText = self.parent.messageField.text()
        if existingText != '':
            textToAdd = '; '
        textToAdd += "CLUE#" + number + ": " + description + "; LOCATION: " + location + "; INSTRUCTIONS: " + instructions
        self.parent.messageField.setText(existingText + textToAdd)
        # previously, lastClueNumber was saved here - on accept; we need to save it on init instead, so that
        #  multiple concurrent clueDialogs will not have the same clue number!
        # header_labels=['CLUE#','DESCRIPTION','TEAM','TIME','DATE','OP','LOCATION','INSTRUCTIONS','RADIO LOC.']
        clueData = [number, description, team, clueTime, clueDate, self.parent.parent.opPeriod, location, instructions, radioLoc]
        self.parent.parent.clueLog.append(clueData)
        if self.clueReportPrintCheckBox.isChecked():
            self.parent.parent.printClueReport(clueData)
        LOG.trace("accepted - calling close")
        self.parent.parent.clueLogDialog.tableView.model().layoutChanged.emit()
        self.closeEvent(QEvent(QEvent.Close), True)
##		pixmap=QPixmap(":/radiolog_ui/print_icon.png")
##		self.parent.parent.clueLogDialog.tableView.model().setHeaderData(0,Qt.Vertical,pixmap,Qt.DecorationRole)
##		self.parent.parent.clueLogDialog.tableView.model().setHeaderData(1,Qt.Vertical,pixmap,Qt.DecorationRole)
##		self.parent.parent.clueLogDialog.tableView.model().headerDataChanged.emit(Qt.Vertical,0,1)
##		# don't try self.close() here - it can cause the dialog to never close!  Instead use super().accept()
        super(clueDialog, self).accept()

    def closeEvent(self, event, accepted=False):
        # note, this type of messagebox is needed to show above all other dialogs for this application,
        #  even the ones that have WindowStaysOnTopHint.  This works in Vista 32 home basic.
        #  if it didn't show up on top, then, there would be no way to close the radiolog other than kill.
        if not accepted:
            if not ask_user_to_confirm("Close this Clue Report Form?\nIt cannot be recovered.", icon=ICON_WARN, parent=self):
                event.ignore()
                return
            if clueDialog.openDialogCount == 1:
                lastClueNumber -= 1  # only release the clue# if no other clue forms are open
            self.values = self.parent.getValues()
            self.values[3] = "RADIO LOG SOFTWARE: radio operator has canceled the 'LOCATED A CLUE' form"
            self.parent.parent.newEntry(self.values)

        clueDialog.indices[self.i] = False  # free up the dialog box location for the next one
        self.parent.clueDialogOpen = False
        clueDialog.openDialogCount -= 1
        self.parent.childDialogs.remove(self)
        event.accept()
        if accepted:
            self.parent.accept()
##		NewEntryWidget.instances.remove(self)

    def clueQuickTextAction(self):
        quickText = self.sender().text()
        quickText = re.sub(r' +\[.*$', '', quickText)  # prune one or more spaces followed by open bracket, thru end
        quickText = re.sub(r'&&', '&', quickText)  # double-ampersand is needed in Qt designer for a literal ampersand
        existingText = self.instructionsField.text()
        if existingText == "":
            self.clueQuickTextAddedStack.append(quickText)
            self.instructionsField.setText(quickText)
        else:
            textToAdd = "; " + quickText
            self.clueQuickTextAddedStack.append(textToAdd)
            self.instructionsField.setText(existingText + textToAdd)
        self.instructionsField.setFocus()

    def clueQuickTextUndo(self):
        LOG.debug("ctrl+z keyBindings:" + str(QKeySequence("Ctrl+Z")))
        if len(self.clueQuickTextAddedStack):
            textToRemove = self.clueQuickTextAddedStack.pop()
            existingText = self.instructionsField.text()
            self.instructionsField.setText(rreplace(existingText, textToRemove, '', 1))
            self.instructionsField.setFocus()


class nonRadioClueDialog(QDialog, NonRadioClueDialogSpec):
    def __init__(self, parent, t, newClueNumber):
        QDialog.__init__(self)
        self.setupUi(self)
        self.timeField.setText(t)
        self.dateField.setText(time.strftime("%x"))
        self.clueNumberField.setText(str(newClueNumber))
        self.parent = parent
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
        self.setAttribute(Qt.WA_DeleteOnClose)
        # values format for adding a new entry:
        #  [time,to_from,team,message,self.formattedLocString,status,self.sec,self.fleet,self.dev,self.origLocString]
        self.values = ["" for n in range(10)]
        self.values[0] = t
        self.values[3] = "RADIO LOG SOFTWARE: 'ADD NON-RADIO CLUE' button pressed; radio operator is gathering details"
        self.values[6] = time.time()
        self.parent.newEntry(self.values)
        self.setFixedSize(self.size())

    def accept(self):
        self.parent.clueLogNeedsPrint = True
        number = self.clueNumberField.text()
        description = self.descriptionField.toPlainText()
        location = self.locationField.text()
        instructions = self.instructionsField.text()
        team = self.callsignField.text()
        clueDate = self.dateField.text()
        clueTime = self.timeField.text()
        radioLoc = ''
        textToAdd = ''
        lastClueNumber = int(self.clueNumberField.text())
        # header_labels=['CLUE#','DESCRIPTION','TEAM','TIME','DATE','OP','LOCATION','INSTRUCTIONS','RADIO LOC.']
        clueData = [number, description, team, clueTime, clueDate, self.parent.opPeriod, location, instructions, radioLoc]
        self.parent.clueLog.append(clueData)

        # add a radio log entry too
        self.values = ["" for n in range(10)]
        self.values[0] = self.timeField.text()
        self.values[3] = "CLUE#" + number + "(NON-RADIO): " + description + "; REPORTED BY: " + team + "; see clue report and clue log for details"
        self.values[6] = time.time()
        self.parent.newEntry(self.values)

        if self.clueReportPrintCheckBox.isChecked():
            printClueReport(clueData, self.parent.getPrintParams())
        LOG.debug("accepted - calling close")
##		# don't try self.close() here - it can cause the dialog to never close!  Instead use super().accept()
        self.parent.clueLogDialog.tableView.model().layoutChanged.emit()
        super(nonRadioClueDialog, self).accept()

    def closeEvent(self, event, accepted=False):
        if not accepted:
            if not ask_user_to_confirm("Close this Clue Report Form?\nIt cannot be recovered.", icon=ICON_WARN, parent=self):
                event.ignore()
                return
            self.values = ["" for n in range(10)]
            self.values[0] = self.timeField.text()
            self.values[3] = "RADIO LOG SOFTWARE: radio operator has canceled the 'NON-RADIO CLUE' form"
            self.values[6] = time.time()
            self.parent.newEntry(self.values)
# 	def reject(self):
# ##		self.parent.timer.start(newEntryDialogTimeoutSeconds*1000) # reset the timeout
# 		LOG.debug("rejected - calling close")
# 		# don't try self.close() here - it can cause the dialog to never close!  Instead use super().reject()
# 		self.closeEvent(None)
# 		super(nonRadioClueDialog,self).reject()


class clueLogDialog(QDialog, ClueLogDialogSpec):
    def __init__(self, parent):
        QDialog.__init__(self)
        self.setupUi(self)
        self.parent = parent
        self.tableModel = clueTableModel(parent.clueLog, self)
        self.tableView.setModel(self.tableModel)

        self.tableView.verticalHeader().setVisible(True)
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        # automatically expand the 'description' and 'instructions' column widths to fill available space and wrap if needed
        self.tableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.tableView.horizontalHeader().setSectionResizeMode(7, QHeaderView.Stretch)

        self.tableView.verticalHeader().sectionClicked.connect(self.headerClicked)
        self.addNonRadioClueButton.clicked.connect(self.parent.addNonRadioClue)
        self.printButton.clicked.connect(self.printClueLogCB)

        self.tableView.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableView.setFocusPolicy(Qt.NoFocus)

    def showEvent(self, event):
        self.tableView.resizeRowsToContents()
        self.tableView.scrollToBottom()
        self.tableView.setStyleSheet("font-size:" + str(self.parent.limitedFontSize) + "pt")

    def resizeEvent(self, event):
        self.tableView.resizeRowsToContents()
        self.tableView.scrollToBottom()

    def headerClicked(self, section):
        clueData = self.parent.clueLog[section]
        clueNum = clueData[0]
        if clueNum != "":  # pass through if clicking a non-clue row
            if ask_user_to_confirm("Print Clue Report for Clue #" + str(clueNum) + "?", title="Confirm - Print Clue Report", parent=self):
                self.parent.printClueReport(clueData)

    def printClueLogCB(self):
        self.parent.opsWithClues = sorted(list(set([str(clue[5]) for clue in self.parent.clueLog if str(clue[5]) != ""])))
        if len(self.parent.opsWithClues) == 0:
            inform_user_about_issue("There are no clues to print.", title="No Clues to Print", parent=self)
        else:
            self.parent.printClueLogDialog.show()


class clueTableModel(QAbstractTableModel):
    header_labels = ['#', 'DESCRIPTION', 'TEAM', 'TIME', 'DATE', 'O.P.', 'LOCATION', 'INSTRUCTIONS', 'RADIO LOC.']

    def __init__(self, datain, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.printIconPixmap = QPixmap(20, 20)
        self.printIconPixmap.load(":/radiolog_ui/print_icon.png")
##		self.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if orientation == Qt.Vertical:
            if role == Qt.DecorationRole and self.arraydata[section][0] != "":
                #icon and button won't display correctly in this use case; just make the entire header item clickable
                return self.printIconPixmap
            if role == Qt.DisplayRole:
                return ""
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header_labels[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        if len(self.arraydata) > 0:
            return len(self.arraydata[0])
        else:
            return len(clueTableModel.header_labels)

    def data(self, index, role):
        if not index.isValid():
            return QVariant()
        elif role != Qt.DisplayRole:
            return QVariant()
        try:
            rval = QVariant(self.arraydata[index.row()][index.column()])
        except:
            row = index.row()
            col = index.column()
            LOG.debug("Row=" + str(row) + " Col=" + str(col))
            LOG.debug("arraydata:")
            LOG.debug(self.arraydata)
        else:
            return rval

    def dataChangedAll(self):
        self.dataChanged.emit(self.createIndex(0, 0), self.createIndex(self.rowCount(self) - 1, self.columnCount(self) - 1))
