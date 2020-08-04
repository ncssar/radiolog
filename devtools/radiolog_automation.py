import sys, re

from pywinauto import backend
from pywinauto.application import Application as pwaApp

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

PHONETIC_LIST = ["Alpha","Bravo","Charlie","Delta","Echo","Foxtrot","Golf","Hotel","India","Juliet","Kilo","Lima","Mike","November","Oscar","Papa","Quebec","Romeo","Sierra","Tango","Uniform","Victor","Whiskey","Xray","Yankee","Zulu"]
PHONETIC_DICT = {"A": "Alpha","B": "Bravo","C": "Charlie","D": "Delta","E": "Echo","F": "Foxtrot","G": "Golf","H": "Hotel","I": "India","J": "Juliet","K": "Kilo","L": "Lima","M": "Mike","N": "November","O": "Oscar","P": "Papa","Q": "Quebec","R": "Romeo","S": "Sierra","T": "Tango","U": "Uniform","V": "Victor","W": "Whiskey","X": "Xray","Y": "Yankee","Z": "Zulu"}

BUTTON_WIDTH = 250
BUTTON_HEIGHT = 24
VERTICAL_SPACING = BUTTON_HEIGHT+5
HORIZONTAL_SPACING = BUTTON_WIDTH+10

def main():
	"""
	This script puts RadioLog through its paces.
	1. Start Radiolog running, if not already.
	2. Click a button to invoke the corresponding action
	"""
	app = QApplication(sys.argv)
	w = InspectorWindow()
	w.show()
	sys.exit(app.exec_())


class InspectorWindow(QWidget):
	def __init__(self, *args):
		QWidget.__init__(self, *args)

		self.paces = Automator(self)

		self.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
		self.setWindowTitle("RadioLog Automation")
		self.setMinimumSize(350,500)

		self.central_widget = QWidget(self)

		col = 0
		slot = 0
		self.chkPhonetic = self.add_checkbox("Use phonetic team names", parent=self.central_widget, horiz=col, vert=slot,
			tip="Use team names like Team Alpha, Team Bravo, ... (instead of Team 1, Team 2, ...)")

		slot += 1
		self.btnDeployTeams = self.add_action_button(
			name="Deploy 3 Teams", parent=self.central_widget, horiz=col, vert=slot, callback=self.paces.deployTeams,
			tip="Add several entries to the log (radio checks, and team departing) -- using Team 1, Team 2, ...")

		slot += 1
		self.btnTeamClue = self.add_action_button(
			name="Add a Team-Found Clue", parent=self.central_widget, horiz=col, vert=slot, callback=self.paces.teamClue,
			tip="Add an entry that Team 1 found a clue")

		slot += 1
		self.btnNonRadioClue = self.add_action_button(
			name="Add a Non-Radio Clue", parent=self.central_widget, horiz=col, vert=slot, callback=self.paces.nonRadioClue,
			tip="Add an entry that a second source found a clue")

		slot += 1
		self.btnOpPeriodAction = self.add_action_button(
			name="", parent=self.central_widget, horiz=col, vert=slot, callback=self.paces.opPeriodAction,
			tip="Invoke the form that bumps to a new operational period")

		slot += 1
		self.btnClueLogAction = self.add_action_button(
			name="", parent=self.central_widget, horiz=col, vert=slot, callback=self.paces.clueLogAction,
			tip="Open the clue log window")

		slot += 1
		self.btnHelpAction = self.add_action_button(
			name="", parent=self.central_widget, horiz=col, vert=slot, callback=self.paces.helpAction,
			tip="Open the help window")

		slot += 1
		self.btnOptionsAction = self.add_action_button(
			name="", parent=self.central_widget, horiz=col, vert=slot, callback=self.paces.optionsAction,
			tip="Open the options window (e.g. Incident name)")

		slot += 1
		self.btnFsFilterAction = self.add_action_button(
			name="", parent=self.central_widget, horiz=col, vert=slot, callback=self.paces.fsFilterAction,
			tip="Invoke filtering of the FS data")

		slot += 1
		self.btnPrintAction = self.add_action_button(
			name="", parent=self.central_widget, horiz=col, vert=slot, callback=self.paces.printAction,
			tip="Open the print dialog")



		slot += 2
		self.btnExit = self.add_action_button(
			name="Exit Wihtout Printing", parent=self.central_widget, horiz=col, vert=slot, callback=self.paces.exitWihtoutPrinting,
			tip="Exit wihtout printing")


	def add_checkbox(self, name, parent, horiz, vert, tip):
		normalized_name = re.sub(r"[^A-Za-z0-9]+","",name)
		chk = QCheckBox(parent)
		chk.setText(name)
		chk.setGeometry(QRect(horiz * HORIZONTAL_SPACING + 10, vert * VERTICAL_SPACING + 10, BUTTON_WIDTH, BUTTON_HEIGHT))
		chk.setMouseTracking(False)
		chk.setObjectName("chk" + normalized_name)
		chk.setToolTip(tip)
		return chk

	def add_action_button(self, name, parent, horiz, vert, callback, tip):
		normalized_name = re.sub(r"[^A-Za-z0-9]+","",name)
		btn = QPushButton(parent)
		btn.setText(name)
		btn.setGeometry(QRect(horiz * HORIZONTAL_SPACING + 10, vert * VERTICAL_SPACING + 10, BUTTON_WIDTH, BUTTON_HEIGHT))
		btn.setMouseTracking(False)
		btn.setObjectName("btn" + normalized_name)
		btn.pressed.connect(callback)
		btn.setToolTip(tip)
		return btn

NEW_ENTRY = "newEntryWindow.tabWidget.qt_tabwidget_stackedwidget.newEntryWidget"
CLUE_ENTRY = "clueDialog"
NON_RADIO_CLUE = "nonRadioClueDialog"



class Automator():
	def __init__(self, parent) -> None:
		self.parent = parent
		try:
			self.radiolog = pwaApp(backend="uia").connect(title_re="Radio Log", class_name="MyWindow")
		except:
			print("\nERROR: RadioLog must be running already.\n")
			sys.exit(1)

	def _target(self, dlg, prefix, control_id, control_type):
		return dlg.child_window(auto_id=prefix + "." + control_id, control_type=control_type)

	def _team_name(self,team_no):
		if self.parent.chkPhonetic.isChecked():
			return PHONETIC_LIST[team_no-1]
		else:
			return "Team "+str(team_no)


	def deployTeams(self):
		r = self.radiolog
		r.RadioLog.type_keys("f")
		dlg = r.NewEntry
		self._target(dlg, NEW_ENTRY, "teamField", "Edit").set_edit_text(self._team_name(1))
		self._target(dlg, NEW_ENTRY, "messageField", "Edit").set_edit_text("Radio check: OK")
		dlg.type_keys("{ENTER}")

		r.RadioLog.type_keys("f")
		dlg = r.NewEntry
		self._target(dlg, NEW_ENTRY, "teamField", "Edit").set_edit_text(self._team_name(2))
		self._target(dlg, NEW_ENTRY, "messageField", "Edit").set_edit_text("Radio check: OK")
		dlg.type_keys("{ENTER}")

		r.RadioLog.type_keys("f")
		dlg = r.NewEntry
		self._target(dlg, NEW_ENTRY, "teamField", "Edit").set_edit_text(self._team_name(1))
		self._target(dlg, NEW_ENTRY, "messageField", "Edit").set_edit_text("Departing IC")
		dlg.type_keys("{ENTER}")

		r.RadioLog.type_keys("f")
		dlg = r.NewEntry
		self._target(dlg, NEW_ENTRY, "teamField", "Edit").set_edit_text(self._team_name(3))
		self._target(dlg, NEW_ENTRY, "messageField", "Edit").set_edit_text("Radio check: OK")
		dlg.type_keys("{ENTER}")

		r.RadioLog.type_keys("f")
		dlg = r.NewEntry
		self._target(dlg, NEW_ENTRY, "teamField", "Edit").set_edit_text(self._team_name(3))
		self._target(dlg, NEW_ENTRY, "messageField", "Edit").set_edit_text("Departing IC")
		dlg.type_keys("{ENTER}")


	def teamClue(self):
		r = self.radiolog
		r.RadioLog.type_keys("f")
		dlg1 = r.NewEntry
		self._target(dlg1, NEW_ENTRY, "teamField", "Edit").set_edit_text(self._team_name(3))
		dlg1.type_keys("{F10}")  # [F10] LOCATED A CLUE

		dlg = r.ClueReport
		# dlg.print_control_identifiers()
		self._target(dlg, CLUE_ENTRY, "descriptionField", "Edit").set_edit_text("Candy Wrapper")
		self._target(dlg, CLUE_ENTRY, "locationField", "Edit").set_edit_text("12345 E 98765 N")
		# self._target(dlg, CLUE_ENTRY, "instructionsField", "Edit").set_edit_text("Mark & leave")
		dlg.type_keys("{F2}")    # [F2] MARK & LEAVE

		# We DO NOT want to print a report! So, let's uncheck this.
		self._target(dlg, CLUE_ENTRY, "clueReportPrintCheckBox", "CheckBox").click()
		dlg.OK.click() # same as dlg.type_keys("{ENTER}")


	def nonRadioClue(self):
		r = self.radiolog
		r.RadioLog.NonRadioClue.click()

		dlg = r.ClueReport

		self._target(dlg, NON_RADIO_CLUE, "groupBox.callsignField", "Edit").type_keys("Ranger")
		self._target(dlg, NON_RADIO_CLUE, "descriptionField", "Edit").set_edit_text("Water bottle (Sparklets)")

		# We DO NOT want to print a report! So, let's uncheck this.
		self._target(dlg, NON_RADIO_CLUE, "clueReportPrintCheckBox", "CheckBox").click()
		dlg.OK.click() # same as dlg.type_keys("{ENTER}")

	def opPeriodAction(self):
		r = self.radiolog
		self._target(r, "Dialog", "opPeriodButton", "Button").click()  # Invoke the form that bumps to a new operational period
		dlg = r.ClueReport
		dlg.print_control_identifiers()

	def clueLogAction(self):
		r = self.radiolog
		self._target(r, "Dialog", "clueLogButton", "Button").click()  # Open the clue log window
		dlg = r.ClueLog
		dlg.print_control_identifiers()

	def helpAction(self):
		r = self.radiolog
		self._target(r, "Dialog", "helpButton", "Button").click()  # Open the help window
		dlg = r.Help
		dlg.print_control_identifiers()

	def optionsAction(self):
		r = self.radiolog
		self._target(r, "Dialog", "optionsButton", "Button").click()  # Open the options window (e.g. Incident name)
		dlg = r.Options
		dlg.print_control_identifiers()

	def fsFilterAction(self):
		r = self.radiolog
		self._target(r, "Dialog", "fsFilterButton", "Button").click()  # Invoke filtering of the FS data
		dlg = r.Filter
		dlg.print_control_identifiers()

	def printAction(self):
		r = self.radiolog
		self._target(r, "Dialog", "printButton", "Button").click()  # Open the print dialog
		dlg = r.Print
		dlg.print_control_identifiers()




	def exitWihtoutPrinting(self):
		r = self.radiolog
		r.RadioLog.print_control_identifiers()

if __name__ == "__main__":
	main()


