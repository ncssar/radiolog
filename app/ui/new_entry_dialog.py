import logging
import re
import time

from gwpycore import (ICON_WARN, FingerTabBarWidget, ask_user_to_confirm,
                      inform_user_about_issue)
from PyQt5 import uic
from PyQt5.QtCore import QEvent, QRect, Qt, QTimer
from PyQt5.QtGui import QColor, QFont, QKeySequence, QPalette
from PyQt5.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel,
                             QSizePolicy, QTabBar, QTabWidget, QWidget)

from app.logic.app_state import holdSec, lastClueNumber, teamStatusDict
from app.logic.entries import rreplace
from app.logic.teams import getExtTeamName, getNiceTeamName
from app.ui.change_callsign_dialog import changeCallsignDialog
from app.ui.clue_dialogs import clueDialog
from app.ui.subject_located_dialog import subjectLocatedDialog

LOG = logging.getLogger("main")

NewEntryWindowSpec = uic.loadUiType("app/ui/newEntryWindow.ui")[0]
NewEntryWidgetSpec = uic.loadUiType("app/ui/newEntryWidget.ui")[0]


class NewEntryWindow(QDialog, NewEntryWindowSpec):
    """
    newEntryWindow is the window that has a QTabWidget;
    each tab's widget (except the first and last which are just labels) is a NewEntryWidget
    the name newEntryWindow is to distinguish it from the previous newEntryDialog
    which had one instance (one dialog box) created per new entry
    """

    ##	def __init__(self,parent,sec,formattedLocString='',fleet='',dev='',origLocString='',amendFlag=False,amendRow=None):
    def __init__(self, parent):
        QDialog.__init__(self)

        ##		self.amendFlag=amendFlag
        ##		self.amendRow=amendRow
        ##		self.sec=sec
        ##		self.formattedLocString=formattedLocString
        ##		self.origLocString=origLocString
        ##		self.fleet=fleet
        ##		self.dev=dev
        ##		self.parent=parent
        ##		if amendFlag:
        ##			row=parent.radioLog[amendRow]
        ##			self.sec=row[0]
        ##			self.formattedLocString=row[4]
        self.setWindowFlags(self.windowFlags() | Qt.FramelessWindowHint)
        self.parent = parent
        self.tabWidth = 175
        self.tabHeight = 25
        self.setupUi(self)
        self.tabWidget.setTabBar(FingerTabBarWidget(width=self.tabWidth, height=self.tabHeight))
        self.tabWidget.setTabPosition(QTabWidget.West)
        ##		self.i=0 # unique persistent tab index; increments with each newly added tab; values are never re-used

        self.tabWidget.insertTab(0, QWidget(), "NEWEST")
        self.tabWidget.setTabEnabled(0, False)
        self.tabWidget.insertTab(1, QWidget(), "OLDEST")
        self.tabWidget.setTabEnabled(1, False)

        self.tabWidget.currentChanged.connect(self.tabChanged)
        ##		self.tabWidget.currentChanged.connect(self.throb)
        ##		self.tabWidget.currentChanged.connect(self.activeTabMessageFieldFocus)

        # 'hold' time: number of seconds that a given tab is 'held' / keeps focus after any mouse or keyboard
        #   input; if a new entry is spawned inside the 'hold' time then it will appear at the top of the
        #   stack, but will not be selected.  The 'hold' means that the most recently
        #   edited tab will stay selected, to prevent any user input from being interrupted and unexpectedly
        #   diverted to a different entry in the middle of typing.
        #
        #  at the end of the hold time, release the hold: do not automatically change the selected tab, but,
        #   new entries will automatically be seleted / get focus if there is no hold.
        #
        # 'continue' time: when an incoming entry is detected for a given callsign, check to see if there
        #   is any already open tab for that same callsign.  If there is, and it has been edited or was spawned
        #   within the 'continue' time, then, do not create a new entry widget or tab, i.e. assume it is part
        #   of the same continued conversation.  If the continue time has expired, then go ahead and open a new tab.

        ##		self.holdSeconds=10
        ##		self.continueSeconds=20

        # display the tabs at the bottom of the west side, to look like a stack;
        #  their order will still be top-down, so, remember to account for that
        # also, must assign something to QTabBar::tab:enabled otherwise the button
        #  will be offset vertically by half of the tab height; see
        # http://stackoverflow.com/questions/29024686
        self.tabWidget.setStyleSheet(
            """
            QTabWidget::tab-bar {
                alignment:right;
            }
            QTabBar::tab {
                padding-left:0px;
                margin-left:0px;
                padding-bottom:0px;
                margin-bottom:0px;
                background-color:lightgray;
                border:1px solid gray;
                border-top-left-radius:4px;
                border-bottom-left-radius:4px;
            }
            QTabBar::tab:selected {
                background-color:white;
                border:3px outset gray;
                border-right:0px;
            }
            QTabBar::tab:!selected {
                margin-left:3px;
            }
            QTabBar::tab:disabled {
                width:80px;
                color:black;
                font-weight:bold;
                background:transparent;
                border:transparent;
                padding-bottom:3px;
            }
        """
        )

        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.autoCleanup)

    # prevent 'esc' from closing the newEntryWindow
    def keyPressEvent(self, event):
        if event.key() != Qt.Key_Escape:
            QDialog.keyPressEvent(self, event)

    def tabChanged(self, throb=True):
        ##	def throb(self):
        tabCount = self.tabWidget.count()
        currentIndex = self.tabWidget.currentIndex()
        # 		LOG.debug("tabCount="+str(tabCount)+" currentIndex="+str(currentIndex))
        if tabCount > 2:  # skip all this if 'NEWEST' and 'OLDEST' are the only tabs remaining
            if (tabCount - currentIndex) > 1:  # don't try to throb the 'OLDEST' label - it has no throb method
                currentWidget = self.tabWidget.widget(currentIndex)
                if currentWidget.needsChangeCallsign:
                    QTimer.singleShot(500, lambda: currentWidget.openChangeCallsignDialog())
                if throb:
                    currentWidget.throb()

                ##	def activeTabMessageFieldFocus(self):
                ##		currentIndex=self.tabWidget.currentIndex()
                self.tabWidget.widget(currentIndex).messageField.setFocus()

    ##	def updateTabColors(self):

    ##		if tabCount<4:
    ##			self.tabWidget.tabBar().setHidden(True)
    ##			self.tabWidget.resize(initialTabWidgetWidth+20,initialTabWidgetHeight+20)
    ##		else:
    ##			self.tabWidget.tabBar().setHidden(False)
    ##			self.tabWidget.resize(initialTabWidgetWidth+self.tabWidth+20,initialTabWidgetHeight+20)
    ##		self.adjustSize()
    ##		currentIndex=self.tabWidget.currentIndex()

    ##			# code to set tab colors based on sequence
    ##			for i in range(1,currentIndex):
    ##				self.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).layout().itemAt(1).widget().setStyleSheet(statusStyleDict["TIMED_OUT_RED"])
    ##			for i in range(currentIndex+1,tabCount-1):
    ##				self.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).layout().itemAt(1).widget().setStyleSheet(statusStyleDict["TIMED_OUT_ORANGE"])
    ##			try:
    ##				self.tabWidget.tabBar().tabButton(currentIndex,QTabBar.LeftSide).layout().itemAt(1).widget().setStyleSheet("")
    ##			except: # the line above has no meaning if the currentIndex is gone and there are no items left
    ##				pass

    def addTab(self, labelText, widget=None):  # always adds at index=1 (index 0 = "NEWEST") i.e. the top of the stack
        ##		self.i+=1
        ##		self.tabWidget.insertTab(1,newEntryTabWidget(self,self.i),tabText)
        if widget:
            ##			widget=NewEntryWidget(self.parent) # NewEntryWidget constructor calls this function
            ##			widget=QWidget()
            ##			self.tabWidget.insertTab(1,widget,labelText)

            self.tabWidget.insertTab(1, widget, "")

            label = QLabel(labelText)
            font = QFont()
            font.setFamily("Segoe UI")
            font.setPointSize(9)
            label.setFont(font)
            spacer = QWidget()
            topWidget = QWidget()
            ##			label.setStyleSheet("border:1px outset black")
            ##			spacer.setStyleSheet("border:1px outset black")

            ##			label.setAlignment(Qt.AlignVCenter)
            ##			label.setIndent(20)
            ##			label.setMidLineWidth(20)
            ##			label.frameRect().moveBottom(20)

            ##			subWidget=QWidget()
            layout = QHBoxLayout()
            layout.addWidget(spacer)
            layout.addWidget(label)
            layout.setSpacing(0)  # to make the rest of the sizing more predictable

            label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            label.setGeometry(QRect(0, 0, self.tabWidth - 8, self.tabHeight - 8))
            spacer.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            spacer.setMinimumSize(8, 4)
            layout.setContentsMargins(0, 0, 0, 0)
            topWidget.setLayout(layout)
            topWidget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Expanding)
            topWidget.setGeometry(QRect(4, 0, self.tabWidth, self.tabHeight - 8))
            ##			label.setGeometry(QRect(16,4,self.tabWidth-3,self.tabHeight-8))

            ##			self.tabWidget.tabBar().setTabButton(1,QTabBar.LeftSide,label)
            ##			self.tabWidget.tabBar().tabButton(1,QTabBar.LeftSide).move(1,1)

            self.tabWidget.tabBar().setTabButton(1, QTabBar.LeftSide, topWidget)

            ##			self.tabWidget.tabBar().tabButton(1,QTabBar.LeftSide).setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
            ##			# if any existing entry widget is still within the hold time, don't change the active tab
            ##			hold=False
            ##			for entry in NewEntryWidget.instances:
            ##				if entry.lastModAge<holdSec:
            ##					hold=True
            # if the current active widget has had no activity within the hold time, then
            #  make this new entry the active tab; otherwise leave it alone
            ##			currentIndex=self.tabWidget.currentIndex()
            ##			if self.tabWidget.widget(currentIndex).lastModAge>holdSec or self.tabWidget.count()==3:
            if self.parent.currentEntryLastModAge > holdSec or self.tabWidget.count() == 3:
                self.tabWidget.setCurrentIndex(1)
                widget.messageField.setFocus()
        ##			if not self.parent.entryHold:
        ##			if not hold:
        ##				self.tabWidget.setCurrentIndex(1)
        ##				self.parent.entryHold=True

        ##			self.tabWidget.setStyleSheet("QTabWidget::tab {background-color:lightgray;}")
        else:  # this should be fallback dead code since addTab is always called with a widget:
            self.parent.openNewEntry()

    ##	def clearHold(self):
    ##		self.entryHold=False
    ##
    ##	def clearContinue(self):
    ##		self.entryContinue=False

    def removeTab(self, caller):
        # determine the current index of the tab that owns the widget that called this function
        i = self.tabWidget.indexOf(caller)
        # determine the number of tabs BEFORE removal of the tab in question
        count = self.tabWidget.count()
        # 		LOG.debug("removeTab: count="+str(count)+" i="+str(i))
        # remove that tab
        self.tabWidget.removeTab(i)
        # activate the next tab upwards in the stack, if there is one
        if i > 1:
            self.tabWidget.setCurrentIndex(i - 1)
        # otherwise, activate the tab at the bottom of the stack, if there is one
        elif i < count - 3:  # count-1 no longer exists; count-2="OLDEST"; count-3=bottom item of the stack
            self.tabWidget.setCurrentIndex(count - 3)

        if count < 4:  # lower the window if the stack is empty
            # 			LOG.debug("lowering: count="+str(count))
            self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint)  # disable always on top
            self.lower()

    ##	def autoCleanupStateChanged(self):
    ##		if self.autoCleanupCheckBox.isChecked():
    ##			self.cleanupNowButton.setEnabled(False)
    ##		else:
    ##			self.cleanupNowButton.setEnabled(True)

    # cleanup rules:
    # if subject dialog or clue dialog is open, do not increment the tab's idle timer
    # if there is any text in the tab's message field, or if the cleanup checkbox is False, ignore the idle timer or set it to zero on every timer count (never auto-close the tab)
    def autoCleanup(self):  # this function is called every second by the timer
        if self.autoCleanupCheckBox.isChecked():
            for tab in NewEntryWidget.instances:
                # 				LOG.debug("lastModAge:"+str(tab.lastModAge))
                # note the pause happens in NewEntryWidget.updateTimer()
                if tab.messageField.text() == "" and tab.lastModAge > 60:
                    tab.closeEvent(QEvent(QEvent.Close), accepted=False, force=True)


##			if not tab.clueDialogOpen and not tab.subjectLocatedDialogOpen and tab.messageField.text()=="" and time.time()-tab.sec>60:


class NewEntryWidget(QWidget, NewEntryWidgetSpec):
    instances = []
    ##	newEntryDialogPositionList=[]
    ##	newEntryDialogUsedPositionList=[]
    ##	for n in range(50):
    ##		newEntryDialogPositionList.append([newEntryDialog_x0+n*newEntryDialog_dx,newEntryDialog_y0+n*newEntryDialog_dy])
    ##		newEntryDialogUsedPositionList.append(False)
    ##	def __init__(self,parent,position,sec,formattedLocString='',fleet='',dev='',origLocString='',amendFlag=False,amendRow=None):
    def __init__(self, parent, sec=0, formattedLocString="", fleet="", dev="", origLocString="", amendFlag=False, amendRow=None):
        QDialog.__init__(self)
        self.buttonsEnabled = True
        self.throbTimer = None
        self.amendFlag = amendFlag
        self.amendRow = amendRow
        self.attachedCallsignList = []
        ##		self.position=position # dialog x,y to show at
        self.sec = sec
        self.formattedLocString = formattedLocString
        self.origLocString = origLocString
        self.fleet = fleet
        self.needsChangeCallsign = False  # can be set to True by openNewEntry
        self.dev = dev
        self.parent = parent
        if amendFlag:
            row = parent.radioLog[amendRow]
            self.sec = row[6]
            self.formattedLocString = row[4]
        ##		newEntryDialog.newEntryDialogUsedPositionList[self.position]=True
        NewEntryWidget.instances.append(self)
        self.setupUi(self)

        # blank-out the label under the callsign field if this was a manually / hotkey
        #  generated NewEntryWidget; the label only applies to fleetsync-spawned entries
        if not fleet:
            self.label_2.setText("")

        self.setAttribute(Qt.WA_DeleteOnClose)  # so that closeEvent gets called when closed by GUI
        self.app_palette = QPalette()
        self.setAutoFillBackground(True)
        self.clueDialogOpen = False  # only allow one clue dialog at a time per NewEntryWidget
        self.subjectLocatedDialogOpen = False

        # 		LOG.debug(" new entry widget opened.  allteamslist:"+str(self.parent.allTeamsList))
        if len(self.parent.allTeamsList) < 2:
            self.teamComboBox.setEnabled(False)
        else:
            self.teamComboBox.clear()
            for team in self.parent.allTeamsList:
                if team != "dummy":
                    self.teamComboBox.addItem(team)

        ##		# close and accept the dialog as a new entry if message is no user input for 30 seconds

        ##		QTimer.singleShot(100,lambda:self.changeBackgroundColor(0))

        # 		LOG.debug("NewEntryWidget created")
        self.quickTextAddedStack = []

        self.childDialogs = []  # keep track of exactly which clueDialog or
        # subjectLocatedDialogs are 'owned' by this NED, for use in closeEvent

        ##		self.messageField.setToolTip("<table><tr><td>a<td>b<tr><td>c<td>d</table>")
        if amendFlag:
            self.timeField.setText(row[0])
            self.teamField.setText(row[2])
            if row[0] == "TO":
                self.to_fromField.setCurrentIndex(1)
            oldMsg = row[3]
            amendIndex = oldMsg.find("\n[AMENDED")
            if amendIndex > -1:
                self.messageField.setText(row[3][:amendIndex])
            else:
                self.messageField.setText(row[3])
            self.label.setText("AMENDED Message:")
        else:
            self.timeField.setText(time.strftime("%H%M"))
        # self.teamField.textChanged.connect(self.setStatusFromTeam)
        QApplication.instance().focusChanged.connect(self.focusChanged)

        self.teamField.textChanged.connect(self.updateTabLabel)
        self.to_fromField.currentIndexChanged.connect(self.updateTabLabel)
        self.messageField.textChanged.connect(self.messageTextChanged)
        self.statusButtonGroup.buttonClicked.connect(self.setStatusFromButton)

        self.teamField.textChanged.connect(self.resetLastModAge)
        self.messageField.textChanged.connect(self.resetLastModAge)
        self.radioLocField.textChanged.connect(self.resetLastModAge)
        self.statusButtonGroup.buttonClicked.connect(self.resetLastModAge)

        self.lastModAge = 0

        # add this NewEntryWidget as a new tab in the newEntryWindow.tabWidget
        self.parent.newEntryWindow.addTab(time.strftime("%H%M"), self)
        # do not raise the window if there is an active clue report form
        # or an active changeCallsignDialog
        # 		LOG.debug("clueLog.openDialogCount="+str(clueDialog.openDialogCount))
        # 		LOG.debug("changeCallsignDialog.openDialogCount="+str(changeCallsignDialog.openDialogCount))
        # 		LOG.debug("subjectLocatedDialog.openDialogCount="+str(subjectLocatedDialog.openDialogCount))
        # 		LOG.debug("showing")
        if not self.parent.newEntryWindow.isVisible():
            self.parent.newEntryWindow.show()
        # 		self.parent.newEntryWindow.setFocus()
        if clueDialog.openDialogCount == 0 and subjectLocatedDialog.openDialogCount == 0 and changeCallsignDialog.openDialogCount == 0:
            # 			LOG.debug("raising")
            self.parent.newEntryWindow.raise_()
        # the following line is needed to get fix the apparent Qt bug (?) that causes
        #  the messageField text to all be selected when a new message comes in
        #  during the continue period.
        self.parent.newEntryWindow.tabWidget.currentWidget().messageField.deselect()

        self.timer = QTimer(self)
        self.timer.start(1000)
        self.timer.timeout.connect(self.updateTimer)

        self.relayed = None
        # store field values in case relayed checkbox is toggled accidentally
        self.relayedByTypedTemp = None
        self.relayedByTemp = None
        self.callsignTemp = None
        self.radioLocTemp = None
        self.datumFormatTemp = None

        self.relayedByComboBox.lineEdit().editingFinished.connect(self.relayedByComboBoxChanged)

        self.updateButtonsEnabled()

    ##		# unless an entry is currently being edited, activate the newly added tab
    ##		if newEntryWidgetHold:
    ##			blink 1
    ##		else:
    ##			self.parent.newEntryWindow.tabWidget.setCurrentIndex(1)

    # update the tab label to include callsign
    ##		self.teamField.textC
    ##		LOG.debug("ctrl+z keyBindings:"+str(QKeySequence("Ctrl+Z")))

    ##		# install actions for messageField
    ##		for entry in quickTextList:
    ##			if entry != "separator":
    ##				LOG.debug("adding:"+entry[0]+" "+str(entry[1]))
    ##				# calling the slot with arguments: lambda evaluates at the time the action is called, so, won't work here;
    ##				#  functools.partial evaluates at addAction time so will do what we want.a
    ##				action=QAction(entry[0],None)
    ##				action.setShortcutContext(Qt.WidgetShortcut)
    ##				action.setShortcut(entry[1])
    ##				self.messageField.addAction(action)
    ##				action.triggered.connect(functools.partial(self.quickTextAction,entry[0]))
    ##
    ##		self.messageField.setContextMenuPolicy(Qt.CustomContextMenu)
    ##		self.messageField.customContextMenuRequested.connect(self.messageContextMenu)
    ##
    ##		self.updateBannerText()
    ##		self.setStatusFromTeam()
    ##		# all new entry dialogs should stay on top of everything, even other programs
    ##		self.setWindowFlags(Qt.WindowStaysOnTopHint)
    ##
    ##	def messageContextMenu(self,pos):
    ##		menu=QMenu()
    ##		for entry in quickTextList:
    ##			if entry=="separator":
    ##				menu.addSeparator()
    ##			else:
    ##				# calling the slot with arguments: lambda evaluates at the time the action is called, so, won't work here;
    ##				#  functools.partial evaluates at addAction time so will do what we want.a
    ##				menu.addAction(entry[0],functools.partial(self.quickTextAction,entry[0]),entry[1])
    ####				action=menu.addAction(entry[0],functools.partial(self.quickTextAction,entry[0]),entry[1])
    ####				self.messageField.addAction(action)
    ##
    ####		act2=menu.addAction("STUFF",functools.partial(self.quickTextAction,"STUFF"),"Ctrl+F")
    ####		self.addAction(act2)
    ####		f1Action=menu.addAction("DEPARTING IC",self.dummySlot,Qt.Key_F1)
    ####		f2Action=menu.addAction("BEGINNING ASSIGNMENT")
    ####		f3Action=menu.addAction("COMPLETED ASSIGNMENT")
    ####		f4Action=menu.addAction("ARRIVING AT IC")
    ####		action=menu.exec_(self.messageField.mapToGlobal(pos))
    ##		menu.exec_(self.messageField.mapToGlobal(pos))
    ####		if action:
    ####			self.messageField.setText(action.text())

    ##	def quickTextAction(self,quickText):
    ##		LOG.debug("quickText:"+quickText)

    ##	def changeEvent(self,event):
    ##		self.throb(0)

    def updateButtonsEnabled(self):
        setButtons = False
        if self.buttonsEnabled == False:
            if self.teamField.text() != "":
                # enable all buttons
                setButtons = True
                self.buttonsEnabled = True
        else:
            if self.teamField.text() == "":
                # disable all buttons
                setButtons = True
                self.buttonsEnabled = False
        if setButtons:
            self.quickTextButton1.setEnabled(self.buttonsEnabled)
            self.quickTextButton2.setEnabled(self.buttonsEnabled)
            self.quickTextButton3.setEnabled(self.buttonsEnabled)
            self.quickTextButton4.setEnabled(self.buttonsEnabled)
            self.quickTextButton5.setEnabled(self.buttonsEnabled)
            self.quickTextButton6.setEnabled(self.buttonsEnabled)
            self.quickTextButton7.setEnabled(self.buttonsEnabled)
            self.quickTextButton8.setEnabled(self.buttonsEnabled)
            self.quickTextButton9.setEnabled(self.buttonsEnabled)
            self.quickTextButton10.setEnabled(self.buttonsEnabled)
            self.quickTextButton11.setEnabled(self.buttonsEnabled)
            self.quickTextButton1_2.setEnabled(self.buttonsEnabled)
            self.quickTextUndoButton.setEnabled(self.buttonsEnabled)
            self.statusGroupBox.setEnabled(self.buttonsEnabled)

    def throb(self, n=0):
        # this function calls itself recursivly 25 times to throb the background blue->white
        # 		LOG.debug("throb:n="+str(n))
        self.app_palette.setColor(QPalette.Background, QColor(n * 10, n * 10, 255))
        self.setPalette(self.app_palette)
        if n < 25:
            # fix #333: make throbTimer a normal timer and then call throbTimer.setSingleShot,
            # so we can just stop it using .stop() when the widget is closed
            # to avert 'wrapped C/C++ object .. has been deleted'
            # 			self.throbTimer=QTimer.singleShot(15,lambda:self.throb(n+1))
            self.throbTimer = QTimer()
            self.throbTimer.timeout.connect(lambda: self.throb(n + 1))
            self.throbTimer.setSingleShot(True)
            self.throbTimer.start(15)
        else:
            # 			LOG.debug("throb complete")
            self.throbTimer = None
            self.app_palette.setColor(QPalette.Background, QColor(255, 255, 255))
            self.setPalette(self.app_palette)

    def updateTimer(self):
        # pause all timers if there are any clue or subject or changeCallsign dialogs open
        if clueDialog.openDialogCount == 0 and subjectLocatedDialog.openDialogCount == 0 and changeCallsignDialog.openDialogCount == 0:
            self.lastModAge += 1
        self.parent.currentEntryLastModAge = self.lastModAge

    ##		if self.lastModAge>holdSec:
    ##			if self.entryHold: # each entry widget has its own lastModAge and its last entryHold
    ##				LOG.debug("releasing entry hold for self")
    ##				self.parent.entryHold=False

    def resetLastModAge(self):
        # 		LOG.debug("resetting last mod age for "+self.teamField.text())
        self.lastModAge = -1
        self.parent.currentEntryLastModAge = self.lastModAge

    def quickTextAction(self):
        quickText = self.sender().text()
        # 		LOG.debug("  quickTextAction called: text="+str(quickText))
        quickText = re.sub(r" +\[.*$", "", quickText)  # prune one or more spaces followed by open bracket, thru end
        existingText = self.messageField.text()
        if existingText == "":
            textToAdd = quickText
        elif existingText.endswith("]"):
            textToAdd = " " + quickText
        elif existingText.endswith("] "):
            textToAdd = quickText
        else:
            textToAdd = "; " + quickText
        self.quickTextAddedStack.append(textToAdd)
        self.messageField.setText(existingText + textToAdd)
        self.messageField.setFocus()

    def quickTextUndo(self):
        LOG.debug("ctrl+z keyBindings:" + str(QKeySequence("Ctrl+Z")))
        if len(self.quickTextAddedStack):
            textToRemove = self.quickTextAddedStack.pop()
            existingText = self.messageField.text()
            self.messageField.setText(rreplace(existingText, textToRemove, "", 1))
            self.messageField.setFocus()

    def quickTextClueAction(self):  # do not push clues on the quick text stack, to make sure they can't be undone
        LOG.debug(str(self.clueDialogOpen))
        if not self.clueDialogOpen:  # only allow one open clue diolog at a time per radio log entry; see init and clueDialog init and closeEvent
            self.newClueDialog = clueDialog(self, self.timeField.text(), self.teamField.text(), self.radioLocField.toPlainText(), lastClueNumber + 1)
            self.newClueDialog.show()

    def quickTextSubjectLocatedAction(self):
        self.subjectLocatedDialog = subjectLocatedDialog(self, self.timeField.text(), self.teamField.text(), self.radioLocField.toPlainText())
        self.subjectLocatedDialog.show()

    # if Enter or Return is pressed while in the teamField, jump to messageField
    #  as if the user pressed the tab key
    def keyPressEvent(self, event):
        key = event.key()
        if key == Qt.Key_Enter or key == Qt.Key_Return:
            if self.teamField.hasFocus():
                self.messageField.setFocus()
            elif self.messageField.hasFocus():
                self.accept()
            else:
                super().keyPressEvent(event)  # pass the event as normal
        elif key == Qt.Key_Escape:
            # need to force focus away from callsignField so that
            #  callsignLostFocus gets called, to keep callsign and tab name in sync,
            #  otherwise this will cause a crash (hitting the cancel button does
            #  not cause a crash because the button takes focus before closing)
            self.messageField.setFocus()
            self.close()
        else:
            super().keyPressEvent(event)  # pass the event as normal

    def openChangeCallsignDialog(self):
        # problem: changeCallsignDialog does not stay on top of newEntryWindow!
        # only open the dialog if the NewEntryWidget was created from an incoming fleetSync ID
        #  (it has no meaning for hotkey-opened newEntryWidgets)
        self.needsChangeCallsign = False
        if self.fleet:
            self.changeCallsignDialog = changeCallsignDialog(self, self.teamField.text(), self.fleet, self.dev)
            self.changeCallsignDialog.exec_()  # required to make it stay on top

    def accept(self):
        if not self.clueDialogOpen and not self.subjectLocatedDialogOpen:
            # getValues return value: [time,to_from,team,message,self.formattedLocString,status,self.sec,self.fleet,self.dev,self.origLocString]
            LOG.debug("Accepted")
            val = self.getValues()

            # validation: callsign field must be non-blank
            vText = ""
            if val[2] == "":
                vText += "\nCallsign cannot be blank."
            LOG.debug("vText:" + vText)
            if vText:
                inform_user_about_issue("Please complete the form and try again:\n" + vText, parent=self)
                return

            if self.amendFlag:
                prevToFrom = self.parent.radioLog[self.amendRow][1]
                newToFrom = self.to_fromField.currentText()
                prevTeam = self.parent.radioLog[self.amendRow][2]
                newTeam = self.teamField.text()
                ##			if self.parent.radioLog[self.amendRow][1]!=self.to_fromField.currentText() or self.parent.radioLog[self.amendRow][2]!=self.teamField.text():
                if prevToFrom != newToFrom or prevTeam != newTeam:
                    tmpTxt = " " + self.parent.radioLog[self.amendRow][1] + " " + self.parent.radioLog[self.amendRow][2]
                    # if the old team tab is now empty, remove it
                    if prevTeam != newTeam:
                        prevEntryCount = len([entry for entry in self.parent.radioLog if entry[2] == prevTeam])
                        LOG.debug("number of entries for the previous team:" + str(prevEntryCount))
                        if prevEntryCount == 1:
                            prevExtTeamName = getExtTeamName(prevTeam)
                            self.parent.deleteTeamTab(prevExtTeamName)
                else:
                    tmpTxt = ""
                # oldMsg = entire message value before the amendment is accepted; may have previous amendments
                # lastMsg = only the last message, i.e. oldMsg minus any previous amendments
                oldMsg = self.parent.radioLog[self.amendRow][3]
                amendIndex = oldMsg.find("\n[AMENDED")
                if amendIndex > -1:
                    lastMsg = oldMsg[:amendIndex]
                    olderMsgs = oldMsg[amendIndex:]
                else:
                    lastMsg = oldMsg
                    olderMsgs = ""
                niceTeamName = val[2]
                status = val[5]

                # update radioLog items that may have been amended
                self.parent.radioLog[self.amendRow][1] = val[1]
                self.parent.radioLog[self.amendRow][2] = niceTeamName
                self.parent.radioLog[self.amendRow][3] = self.messageField.text() + "\n[AMENDED " + time.strftime("%H%M") + "; WAS" + tmpTxt + ": '" + lastMsg + "']" + olderMsgs
                self.parent.radioLog[self.amendRow][5] = status

                # use to_from value "AMEND" and blank msg text to make sure team timer does not reset
                self.parent.newEntryProcessTeam(niceTeamName, status, "AMEND", "")

                # reapply the filter on team tables, in case callsign was changed
                for t in self.parent.tableViewList[1:]:
                    t.model().invalidateFilter()
            else:
                self.parent.newEntry(self.getValues())

            # make entries for attached callsigns
            # values array format: [time,to_from,team,message,locString,status,sec,fleet,dev]
            # 			LOG.debug("attached callsigns: "+str(self.attachedCallsignList))
            for attachedCallsign in self.attachedCallsignList:
                v = val[:]  # v is a fresh, independent copy of val for each iteration
                v[2] = getNiceTeamName(attachedCallsign)
                v[3] = "[ATTACHED FROM " + self.teamField.text().strip() + "] " + val[3]
                self.parent.newEntry(v)

            self.parent.totalEntryCount += 1
            if self.parent.totalEntryCount % 5 == 0:
                # rotate backup files after every 5 entries, but note the actual
                #  entry interval could be off during fast entries since the
                #  rotate script is called asynchronously (i.e. backgrounded)
                filesToBackup = [self.parent.firstWorkingDir + "\\" + self.parent.csvFileName, self.parent.firstWorkingDir + "\\" + self.parent.csvFileName.replace(".csv", "_clueLog.csv"), self.parent.firstWorkingDir + "\\" + self.parent.fsFileName]
                if self.parent.use2WD and self.parent.secondWorkingDir:
                    filesToBackup = filesToBackup + [
                        self.parent.secondWorkingDir + "\\" + self.parent.csvFileName,
                        self.parent.secondWorkingDir + "\\" + self.parent.csvFileName.replace(".csv", "_clueLog.csv"),
                        self.parent.secondWorkingDir + "\\" + self.parent.fsFileName,
                    ]
                self.parent.rotateCsvBackups(filesToBackup)
            LOG.debug("Accepted2")
        self.closeEvent(QEvent(QEvent.Close), True)

    ##		self.close()

    # 	def reject(self):
    # 		really=ICON_WARN(self,"Please Confirm","Cancel this entry?\nIt cannot be recovered.",
    # 			QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
    # 		if really==QMessageBox.Yes:
    # 			self.closeEvent(None)

    ##		self.timer.stop()
    ##
    ####	def closeEvent(self):
    ##		self.parent.newEntryWindow.tabWidget.removeTab(self.parent.newEntryWindow.tabWidget.indexOf(self))
    ##		NewEntryWidget.instances.remove(self)
    ##		self.close()

    ##	def closeEvent(self,event):
    ##		newEntryDialog.newEntryDialogUsedPositionList[self.position]=False
    ##		newEntryDialog.instances.remove(self)
    ##		self.timer.stop() # otherwise it keeps accepting even after closed!

    # 	def closeEvent(self,event,accepted=False):
    # 		# note, this type of messagebox is needed to show above all other dialogs for this application,
    # 		#  even the ones that have WindowStaysOnTopHint.  This works in Vista 32 home basic.
    # 		#  if it didn't show up on top, then, there would be no way to close the radiolog other than kill.
    # 		LOG.debug("closeEvent called: accepted="+str(accepted))
    # 		if not accepted:
    # 			really=QMessageBox(ICON_WARN,"Please Confirm","Close this Clue Report Form?\nIt cannot be recovered.",
    # 				QMessageBox.Yes|QMessageBox.Cancel,self,Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
    # 			if really.exec()==QMessageBox.Cancel:
    # 				event.ignore()
    # 				return
    #
    # 		clueDialog.indices[self.i]=False # free up the dialog box location for the next one
    # 		self.parent.clueDialogOpen=False
    # 		clueDialog.openDialogCount-=1
    # ##		NewEntryWidget.instances.remove(self)

    def closeEvent(self, event, accepted=False, force=False):
        # if the user hit cancel, make sure the user really wanted to cancel
        # fix #325: repeated cancel-confirm cycles are annoying; bypass the
        #  confirmation if the message is blank; note that any GPS data gets sent
        #  as soon as the dialog is opened (or as soon as the change callsign dialog
        #  is accepted), so, bypassing the confirmation in this manner will
        #  still preserve and process any incoming GPS coordinates
        if not accepted and not force and self.messageField.text() != "":
            msg = "Cancel this entry?\nIt cannot be recovered."
            if self.amendFlag:
                msg = "Cancel this amendment?\nOriginal message will be preserved."
            if not ask_user_to_confirm(msg, icon=ICON_WARN, parent=self):
                event.ignore()
                return
        # whether OK or Cancel, ignore the event if child dialog(s) are open,
        #  and raise the child window(s)
        if self.clueDialogOpen or self.subjectLocatedDialogOpen:
            # the 'child' dialogs are not technically children; use the NED's
            #  childDialogs attribute instead, which was populated in the __init__
            #  of each child dialog class
            for child in self.childDialogs:
                child.raise_()
            inform_user_about_issue("A Clue Report or Subject Located form is open that belongs to this entry.  Finish it first.", icon=ICON_WARN, title="Cannot close", parent=self)
            event.ignore()
            return
        else:
            self.timer.stop()
            # fix #333: stop mid-throb to avert runtime error
            #  but only if the throbTimer was actually started
            if self.throbTimer:
                self.throbTimer.stop()
            # if there is a pending GET request (locator), send it now with the
            #  specified callsign
            self.parent.sendPendingGet(self.teamField.text())
            ##		self.parent.newEntryWindow.tabWidget.removeTab(self.parent.newEntryWindow.tabWidget.indexOf(self))
            ##		self.parent.newEntryWindow.removeTab(self.parent.newEntryWindow.tabWidget.indexOf(self))
            self.parent.newEntryWindow.removeTab(self)
            NewEntryWidget.instances.remove(self)

    ##		else:
    ##			event.ignore()

    def focusChanged(self, oldFocus, newFocus):
        LOG.debug(f"oldFocus = {type(oldFocus)}")
        if oldFocus is self.teamField:
            LOG.debug(f"Team Field losing focus. Calling setStatusFromTeam()")
            self.setStatusFromTeam()

    def setStatusFromTeam(self):
        ##		self.timer.start(newEntryDialogTimeoutSeconds*1000) # reset the timeout
        extTeamName = getExtTeamName(self.teamField.text())
        if (extTeamName in teamStatusDict) and (teamStatusDict[extTeamName] != ""):
            prevStatus = teamStatusDict[extTeamName]
            # 			print("Team "+extTeamName+": previous status='"+prevStatus+"'")
            for button in self.statusButtonGroup.buttons():
                if button.text() == prevStatus:
                    button.setChecked(True)
        else:
            # 			print("unknown team, or existing team with no existing status")
            # must setExclusive(False) to allow unselecting all buttons,
            # then set it back to True afterwards
            self.statusButtonGroup.setExclusive(False)
            for button in self.statusButtonGroup.buttons():
                button.setChecked(False)
            self.statusButtonGroup.setExclusive(True)

    ##	def updateBannerText(self):
    ##		if self.amendFlag:
    ##			tmpTxt="AMENDED ENTRY"
    ##		else:
    ##			tmpTxt="New Entry"
    ##		self.setWindowTitle("Radio Log - "+tmpTxt+" - "+self.to_fromField.currentText()+" "+self.teamField.text())

    def teamFieldTextChanged(self):
        LOG.trace("teamFieldTextChanged")
        self.updateButtonsEnabled()
        # if typed callsign is only a three-or-fewer-digit number, prefix it with 'Team '
        #  otherwise do not prefix it
        cs = self.teamField.text()
        csraw = cs.replace("Team ", "")
        # 		LOG.debug("csraw: '"+csraw+"'")
        if re.match(r".*\D.*", csraw) or len(csraw) > 3:
            csout = csraw
        else:
            csout = "Team " + csraw
        # 		LOG.debug("csout: '"+csout+"'")
        self.teamField.setText(csout)

    def teamFieldEditingFinished(self):
        LOG.trace("teamFieldEditingFinished")
        cs = self.teamField.text()
        if re.match(r".*\D.*", cs):
            # change it to any case-insensitive-matching existing callsign
            for t in self.parent.allTeamsList:
                if t.upper() == cs.upper():
                    self.teamField.setText(t)
                    break
        if re.match(".*relay.*", cs, re.IGNORECASE):
            LOG.debug("relay callsign detected")
            # if the relay callsign is already in the callsign list, i.e. if
            #  they have previously called in, then assume they are relaying
            #  a message; if not, assume they are not yet relaying a message
            for t in self.parent.allTeamsList:
                if t.upper() == cs.upper():
                    self.relayedCheckBox.setChecked(True)
                    self.relayedByComboBox.setCurrentText(t)
                    break

    def setRelayedPrefix(self, relayedBy=None):
        if relayedBy is None:
            relayedBy = self.relayedByComboBox.currentText()
        # 		LOG.debug("setRelayedPrefix:"+relayedBy)
        if relayedBy == "":
            if self.relayed:
                prefix = "[RELAYED] "
            else:
                prefix = ""
        else:
            prefix = "[RELAYED by " + relayedBy + "] "
        mt = self.messageField.text()
        if mt.startswith("[RELAYED"):
            relayedEndIndex = mt.find("]")
            # 			LOG.debug("before relayed prefix removal:"+mt)
            mt = mt.replace(mt[: relayedEndIndex + 2], "")
        # 			LOG.debug("after relayed prefix removal:"+mt)
        mt = prefix + mt
        self.messageField.setText(mt)

    def getRelayedByItems(self):
        items = []
        for n in range(self.relayedByComboBox.count()):
            items.append(self.relayedByComboBox.itemText(n))
        return items

    def relayedCheckBoxStateChanged(self):
        # if this was a fleetsync call, move the incoming callsign to 'relayed by'
        #  and set focus to the callsign field to prompt for the callsign of the
        #  originating team/unit
        # if it was not a fleetsync call, leave the callsign alone and set 'relayed by'
        #  to blank, since it's likely that the radio operator may have typed the
        #  originating team/unit callsign in to the callsign field first, and then
        #  checked 'relayed' afterwards
        LOG.trace("relayedCheckBoxStateChanged; fleet=" + str(self.fleet) + "; dev=" + str(self.dev))
        self.relayed = self.relayedCheckBox.isChecked()
        self.relayedByLabel.setEnabled(self.relayed)
        self.relayedByComboBox.setEnabled(self.relayed)
        self.relayedByComboBox.clear()  # rebuild the list from scratch to avoid duplicates
        if self.relayed:  # do these steps regardless of whether it was a fleetsync call
            for team in self.parent.allTeamsList:
                if team != "dummy":
                    self.relayedByComboBox.addItem(team)
            # remove the current callsign from the list of 'relayed by' choices
            for n in range(self.relayedByComboBox.count()):
                if self.relayedByComboBox.itemText(n).lower() == self.teamField.text().lower():
                    self.relayedByComboBox.removeItem(n)
                    break
            self.relayedCheckBox.setText("Relayed")
            if self.relayedByTypedTemp is not None:
                self.relayedByComboBox.setCurrentText(self.relayedByTypedTemp)
        else:  # just unchecked the box, regadless of fleetsync
            text = self.relayedByComboBox.currentText()
            if text != "" and text not in self.getRelayedByItems():
                self.relayedByTypedTemp = text
            self.relayedByComboBox.setCurrentText("")
        if self.dev is not None:  # only do these steps if it was a fleetsync call
            if self.relayed:
                # store field values in case this was inadvertently checked
                self.callsignTemp = self.teamField.text()
                self.radioLocTemp = self.radioLocField.toPlainText()
                self.datumFormatTemp = self.datumFormatLabel.text()
                self.radioLocField.setText("")
                self.datumFormatLabel.setText("")
                # 			LOG.debug("relayed")
                self.relayedByComboBox.clear()
                cs = self.teamField.text()
                if self.relayedByTemp is not None:
                    self.relayedByComboBox.setCurrentText(self.relayedByTemp)
                elif cs != "":
                    self.relayedByComboBox.setCurrentText(cs)
                self.teamField.setText("")
                # need to 'burp' the focus to prevent two blinking cursors
                #  see http://stackoverflow.com/questions/42475602
                self.messageField.setFocus()
                self.teamField.setFocus()
            else:
                # 			LOG.debug("not relayed")
                # store field values in case this was inadvertently checked
                self.relayedByTemp = self.relayedByComboBox.currentText()
                self.relayedCheckBox.setText("Relayed?")
                if self.callsignTemp is not None:
                    self.teamField.setText(self.callsignTemp)
                else:
                    self.teamField.setText(self.relayedByComboBox.currentText())
                if self.radioLocTemp is not None:
                    self.radioLocField.setText(self.radioLocTemp)
                if self.datumFormatTemp is not None:
                    self.datumFormatLabel.setText(self.datumFormatTemp)
                self.relayedByComboBox.clear()
                self.messageField.setFocus()
        self.setRelayedPrefix()

    def relayedByComboBoxChanged(self):
        LOG.trace("relayedByComboBoxChanged")
        self.relayedBy = self.relayedByComboBox.currentText()
        self.setRelayedPrefix(self.relayedBy)
        self.messageField.setFocus()

    def messageTextChanged(self):  # gets called after every keystroke or button press, so, should be fast
        ##		self.timer.start(newEntryDialogTimeoutSeconds*1000) # reset the timeout
        message = self.messageField.text().lower()
        extTeamName = getExtTeamName(self.teamField.text())
        prevStatus = ""
        if extTeamName in teamStatusDict:
            prevStatus = teamStatusDict[extTeamName]
        newStatus = ""  # need to actively set it back to blank if neeeded, since this function is called on every text change
        # use an if/elif/else clause, which requires a search order; use the more final messages first
        # note, these hints can be trumped by clicking the status button AFTER typing

        # multiple things have to be in place to have a new status text here actually
        #  change the status of the new entry:
        # 1. button with matching text() must exist in NewEntryWidget and must
        #     be a member of statusButtonGroup (it can be behind another button
        #     so that it never gets clicked and is not visible, but, it must exist)
        # 2. the clicked() signal from that button must have a reciever of
        #     NewEntryWidget.quickTextAction()
        if "at ic" in message:
            newStatus = "At IC"
        elif "requesting transport" in message:
            newStatus = "Waiting for Transport"
        elif "enroute to ic" in message:
            newStatus = "In Transit"
        elif "starting assignment" in message:
            newStatus = "Working"
        elif "departing ic" in message:
            newStatus = "In Transit"
        elif "standby" in message:
            newStatus = "STANDBY"
        elif "hold position" in message:
            newStatus = "STANDBY"
        elif "requesting deputy" in message:
            newStatus = "STANDBY"
        elif "10-8" in message:
            newStatus = "Available"
        elif "10-97" in message:
            newStatus = "Working"
        elif "10-10" in message:
            newStatus = "Off Duty"
        elif prevStatus == "Available" and "evac" in message:
            newStatus = "In Transit"
        else:
            newStatus = prevStatus

        # 		LOG.debug("message:"+str(message))
        # 		LOG.debug("  previous status:"+str(prevStatus)+"  newStatus:"+str(newStatus))
        # attached callsigns (issue 306):
        # this takes place in two phases:
        # 1. determine the list of attached callsigns during message entry
        # 2. when the message is submitted, also create identical messages
        #     for each of the attached callsigns (and make sure their status
        #     changes to the same as the originating callsign)
        # also look for "with" or "w/" and if found, attach this message to the
        #  callsigns in the following token(s)
        # example: from transport 1: "enroute to IC with team4 and team5"
        #  means that this message and status should be copied to teams 4 and 5
        # if the attachment token is found ("with" or "w/") then treat all
        #  subsequent words as attached callsigns, with various possible delimiters (space, comma, 'and')
        #  and also provide for callsign shorthand; handle these cases:
        # team<number>
        # team<space><number>
        # <number>
        # t<number>
        # t<space><number>
        #  note that the cases with spaces require that we get rid of spaces
        #   before numbers if those spaces are preceded by a letter
        #  also replace 'team' or 't' with 'Team'

        self.attachedCallsignList = []
        # the following lines are commented out TMG 4-7-17 to prevent crashes when
        # amending attached-team messages; see issue#310; hopefully a better solution
        # can be found in the future

        # 		lowerMessage=message.lower()
        # 		if "with" in lowerMessage or "w/" in lowerMessage:
        # 			tailIndex=lowerMessage.find("with")+4
        # 			if tailIndex<4:
        # 				tailIndex=lowerMessage.find("w/")+2
        # 			if tailIndex>1:
        # 				tail=message[tailIndex:].strip()
        # 				#massage the tail to get it into a good format here
        # 				tail=re.sub(r'(\w)\s+(\d+)',r'\1\2',tail) # remove space after letters before numbers
        # 				tail=re.sub(r't(\d+)',r'team\1',tail) # change t# to team#
        # 				tail=re.sub(r'([\s,]+)(\d+)',r'\1team\2',tail) # insert 'team' before just-numbers
        # 				tail=re.sub(r'^(\d+)',r'team\1',tail) # and also at the start of the tail
        # 				tail=re.sub(r'team',r'Team',tail) # capitalize 'team'
        # 	# 			LOG.debug(" 'with' tail found:"+tail)
        # 				tailParse=re.split("[, ]+",tail)
        # 				# rebuild the attachedCallsignList from scratch on every keystroke;
        # 				#  trying to append to the list is problematic (i.e. when do we append?)
        # 				for token in tailParse:
        # 					if token!="and": # all parsed tokens other than "and" are callsigns to be attached
        # 						# keep the list as a local variable rather than object attribute,
        # 						#  since we want to rebuild the entire list on every keystroke
        # 						self.attachedCallsignList.append(token)
        # 		self.attachedField.setText(" ".join(self.attachedCallsignList))
        #
        # allow it to be set back to blank; must set exclusive to false and iterate over each button
        self.statusButtonGroup.setExclusive(False)
        for button in self.statusButtonGroup.buttons():
            # 			LOG.debug("checking button: "+button.text())
            if button.text() == newStatus:
                button.setChecked(True)
            else:
                button.setChecked(False)
        self.statusButtonGroup.setExclusive(True)
        self.messageField.deselect()

    def setCallsignFromComboBox(self, str):
        self.teamField.setText(str)
        self.teamField.setFocus()

    def setStatusFromButton(self):
        ##		self.timer.start(newEntryDialogTimeoutSeconds*1000) # reset the timeout
        clickedStatus = self.statusButtonGroup.checkedButton().text()
        extTeamName = getExtTeamName(self.teamField.text())
        teamStatusDict[extTeamName] = clickedStatus

    def updateTabLabel(self):
        i = self.parent.newEntryWindow.tabWidget.indexOf(self)
        self.parent.newEntryWindow.tabWidget.tabBar().tabButton(i, QTabBar.LeftSide).layout().itemAt(1).widget().setText(time.strftime("%H%M") + " " + self.to_fromField.currentText() + " " + self.teamField.text())

    ##		self.parent.newEntryWindow.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).setText(self.teamField.text())
    ##		self.parent.newEntryWindow.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).adjustSize()

    def getValues(self):
        time = self.timeField.text()
        to_from = self.to_fromField.currentText()
        team = self.teamField.text().strip()  # remove leading and trailing spaces
        message = self.messageField.text()
        if self.relayed:
            locString = ""
        else:
            locString = self.formattedLocString
        # 		location=self.radioLocField.text()
        status = ""
        if self.statusButtonGroup.checkedButton() != None:
            status = self.statusButtonGroup.checkedButton().text()
        return [time, to_from, team, message, locString, status, self.sec, self.fleet, self.dev, self.origLocString]

    def set_partial_team_name(self, from_to: int, text: str):
        LOG.debug(f"set_partial_team_name called with text = {text}")
        self.to_fromField.setCurrentIndex(from_to)
        # need to 'burp' the focus to prevent two blinking cursors
        #  see http://stackoverflow.com/questions/42475602
        self.messageField.setFocus()
        # all three of these lines are needed to override the default 'pseudo-selected'
        # behavior; see http://stackoverflow.com/questions/27856032
        self.teamField.setFocus()
        if text:
            self.teamField.setText(text + "  ")
            # self.teamField.setSelection(len(text),1)
