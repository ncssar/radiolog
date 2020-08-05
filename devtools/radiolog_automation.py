import sys, re, time

from pywinauto import backend
import pywinauto

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

PHONETIC_LIST = ["Alpha","Bravo","Charlie","Delta","Echo","Foxtrot","Golf","Hotel","India","Juliet","Kilo","Lima","Mike","November","Oscar","Papa","Quebec","Romeo","Sierra","Tango","Uniform","Victor","Whiskey","Xray","Yankee","Zulu"]
PHONETIC_DICT = {"A": "Alpha","B": "Bravo","C": "Charlie","D": "Delta","E": "Echo","F": "Foxtrot","G": "Golf","H": "Hotel","I": "India","J": "Juliet","K": "Kilo","L": "Lima","M": "Mike","N": "November","O": "Oscar","P": "Papa","Q": "Quebec","R": "Romeo","S": "Sierra","T": "Tango","U": "Uniform","V": "Victor","W": "Whiskey","X": "Xray","Y": "Yankee","Z": "Zulu"}

GRID_HEIGHT = 15
CELL_WIDTH = 250
CELL_HEIGHT = 26
VERTICAL_SPACING = CELL_HEIGHT+5
HORIZONTAL_SPACING = CELL_WIDTH+10

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

##########################################################################

class InspectorWindow(QWidget):
	def __init__(self, *args):
		QWidget.__init__(self, *args)

		self.paces = Automator(self)

		self.current_grid_col = 0
		self.current_grid_row = 0

		self.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
		self.setWindowTitle("RadioLog Automation")
		self.setMinimumSize(HORIZONTAL_SPACING+10, GRID_HEIGHT * VERTICAL_SPACING + 10)
		self.central_widget = QWidget(self)

		self.chkPhonetic = self.add_checkbox("Use Phonetic Team Names",
			tip="Use team names like Team Alpha, Team Bravo, ... (instead of Team 1, Team 2, ...)")

		self.btnDeployTeams = self.add_action_button("Deploy 3 Teams", callback=self.paces.deployTeams,
			tip="Add several entries to the log (radio checks, and team departing) -- using Team 1, Team 2, ...")

		self.btnTeamClue = self.add_action_button("Add a Team-Found Clue", callback=self.paces.teamClue,
			tip="Add an entry that Team 3 found a clue")

		self.btnNonRadioClue = self.add_action_button("Add a Non-Radio Clue", callback=self.paces.nonRadioClue,
			tip="Add an entry that a Ranger found a clue")

		self.btnSubjectLocated = self.add_action_button("Subject Located", callback=self.paces.subjectLocatedAction)

		self.btnOpPeriodAction = self.add_action_button("Bump Operational Period", callback=self.paces.opPeriodAction,
			tip="Invoke the form that bumps to a new operational period")

		self.btnClueLogAction = self.add_action_button("Open Clue Log Window", callback=self.paces.clueLogAction)

		self.btnHelpAction = self.add_action_button("Open the Help Window", callback=self.paces.helpAction)

		self.btnOptionsAction = self.add_action_button("Options Window", callback=self.paces.optionsAction,
			tip="Open the options window (e.g. Incident name)")

		self.btnFsFilterAction = self.add_action_button("FS Filtering", callback=self.paces.fsFilterAction,
			tip="Invoke filtering of the FS data")

		self.btnPrintAction = self.add_action_button("Open the Print Dialog", callback=self.paces.printAction)

		self.move_to_next_cell()

		self.btnExit = self.add_action_button("Exit Wihtout Printing", callback=self.paces.exitWihtoutPrinting)


	def add_checkbox(self, name, tip=""):
		normalized_name = re.sub(r"[^A-Za-z0-9]+","",name)
		# print(normalized_name)
		chk = QCheckBox(self.central_widget)
		chk.setText(name)
		chk.setGeometry(QRect(self.current_grid_col * HORIZONTAL_SPACING + 10, self.current_grid_row * VERTICAL_SPACING + 10, CELL_WIDTH, CELL_HEIGHT))
		chk.setMouseTracking(False)
		chk.setObjectName("chk" + normalized_name)
		chk.setToolTip(tip if tip else name)
		self.move_to_next_cell()
		return chk

	def add_action_button(self, name, callback, tip=""):
		normalized_name = re.sub(r"[^A-Za-z0-9]+","",name)
		# print(normalized_name)
		btn = QPushButton(self.central_widget)
		btn.setText(name)
		btn.setGeometry(QRect(self.current_grid_col * HORIZONTAL_SPACING + 10, self.current_grid_row * VERTICAL_SPACING + 10, CELL_WIDTH, CELL_HEIGHT))
		btn.setMouseTracking(False)
		btn.setObjectName("btn" + normalized_name)
		btn.pressed.connect(callback)
		btn.setToolTip(tip if tip else name)
		self.move_to_next_cell()
		return btn

	def move_to_next_cell(self):
		self.current_grid_row += 1
		if self.current_grid_row >= GRID_HEIGHT:
			self.current_grid_col += 1
			self.current_grid_row = 0
			self.resize_to_grid()

	def resize_to_grid(self):
		self.resize((self.current_grid_col+1)*HORIZONTAL_SPACING + 10, GRID_HEIGHT * VERTICAL_SPACING + 10)



##########################################################################

NEW_ENTRY_PREFIX = "newEntryWindow.tabWidget.qt_tabwidget_stackedwidget.newEntryWidget"

class Automator():
	def __init__(self, parent) -> None:
		self.parent = parent
		try:
			print("[TRACE] starting Automator")
			self.radiolog = pywinauto.application.Application(backend="uia").connect(title_re="Radio Log", class_name="MyWindow")
			print(f"All top-level windows: {self.radiolog.windows()}")
			#print(f"Top window: {self.radiolog.top_window().print_control_identifiers()}")
			#print(f"Active window: {self.radiolog.active()}")
		except Exception as e:
			print(type(e).__name__)
			print(e)
			print("\nERROR: RadioLog must be running already.\n")
			sys.exit(1)


	def _team_name(self,team_no):
		if self.parent.chkPhonetic.isChecked():
			return PHONETIC_LIST[team_no-1]
		else:
			return "Team "+str(team_no)


	def _discover_elements(self, control):
		try:
			control.print_control_identifiers()
		except pywinauto.findbestmatch.MatchError as e:
			print(f"Can't find ["+e.tofind+"]. Candidates are: "+';'.join(sorted(e.items)))


	def deployTeams(self):
		r = self.radiolog
		r.RadioLog.type_keys("f")
		dlg = r.NewEntry
		dlg.child_window(auto_id=NEW_ENTRY_PREFIX + ".teamField", control_type="Edit").set_edit_text(self._team_name(1))
		dlg.child_window(auto_id=NEW_ENTRY_PREFIX + ".messageField", control_type="Edit").set_edit_text("Radio check: OK")
		dlg.type_keys("{ENTER}")

		r.RadioLog.type_keys("f")
		dlg = r.NewEntry
		dlg.child_window(auto_id=NEW_ENTRY_PREFIX + ".teamField", control_type="Edit").set_edit_text(self._team_name(2))
		dlg.child_window(auto_id=NEW_ENTRY_PREFIX + ".messageField", control_type="Edit").set_edit_text("Radio check: OK")
		dlg.type_keys("{ENTER}")

		r.RadioLog.type_keys("f")
		dlg = r.NewEntry
		dlg.child_window(auto_id=NEW_ENTRY_PREFIX + ".teamField", control_type="Edit").set_edit_text(self._team_name(1))
		dlg.child_window(auto_id=NEW_ENTRY_PREFIX + ".messageField", control_type="Edit").set_edit_text("Departing IC")
		dlg.type_keys("{ENTER}")

		r.RadioLog.type_keys("f")
		dlg = r.NewEntry
		dlg.child_window(auto_id=NEW_ENTRY_PREFIX + ".teamField", control_type="Edit").set_edit_text(self._team_name(3))
		dlg.child_window(auto_id=NEW_ENTRY_PREFIX + ".messageField", control_type="Edit").set_edit_text("Radio check: OK")
		dlg.type_keys("{ENTER}")

		r.RadioLog.type_keys("f")
		dlg = r.NewEntry
		dlg.child_window(auto_id=NEW_ENTRY_PREFIX + ".teamField", control_type="Edit").set_edit_text(self._team_name(3))
		dlg.child_window(auto_id=NEW_ENTRY_PREFIX + ".messageField", control_type="Edit").set_edit_text("Departing IC")
		dlg.type_keys("{ENTER}")


	def teamClue(self):
		r = self.radiolog
		r.RadioLog.type_keys("f")
		# In case the "magic naming" on the next line doesn't work, here's the long way: dlg = r.child_window(title="Radio Log - New Entry", auto_id="newEntryWindow", control_type="Window")
		dlg1 = r.NewEntry
		dlg1.child_window(auto_id=NEW_ENTRY_PREFIX + ".teamField", control_type="Edit").set_edit_text(self._team_name(3))
		dlg1.type_keys("{F10}")  # [F10] LOCATED A CLUE

		dlg = r.ClueReport
		# dlg.print_control_identifiers()
		dlg.child_window(auto_id="clueDialog.descriptionField", control_type="Edit").set_edit_text("Candy Wrapper")
		dlg.child_window(auto_id="clueDialog.locationField", control_type="Edit").set_edit_text("12345 E 98765 N")
		# dlg.child_window(auto_id="clueDialog.instructionsField", control_type="Edit").set_edit_text("Mark & leave")
		dlg.type_keys("{F2}")    # [F2] MARK & LEAVE

		# We DO NOT want to print a report! So, let's uncheck this.
		dlg.child_window(auto_id="clueDialog.clueReportPrintCheckBox", control_type="CheckBox").click()
		dlg.OK.click() # same as dlg.type_keys("{ENTER}")


	def nonRadioClue(self):
		r = self.radiolog
		r.RadioLog.NonRadioClue.click()
		# dlg = r.child_window(title="Clue Report", auto_id="nonRadioClueDialog", control_type="Window")
		dlg = r.ClueReport

		dlg.child_window(auto_id="nonRadioClueDialog.groupBox.callsignField", control_type="Edit").type_keys("Ranger")
		dlg.child_window(auto_id="nonRadioClueDialog.descriptionField", control_type="Edit").set_edit_text("Water bottle (Sparklets)")

		# We DO NOT want to print a report! So, let's uncheck this.
		dlg.child_window(auto_id="nonRadioClueDialog.clueReportPrintCheckBox", control_type="CheckBox").click()
		dlg.OK.click() # same as dlg.type_keys("{ENTER}")


	def opPeriodAction(self):
		r = self.radiolog
		r.RadioLog.child_window(auto_id="Dialog.opPeriodButton", control_type="Button").click()  # Invoke the form that bumps to a new operational period
		# dlg = r.child_window(title="Change Operational Period", auto_id="opPeriodDialog", control_type="Window")
		dlg = r.ChangeOperationalPeriod
		self._discover_elements(dlg)


	def subjectLocatedAction(self):
		r = self.radiolog
		r.RadioLog.type_keys("f")
		# In case the "magic naming" on the next line doesn't work, here's the long way: dlg = r.child_window(title="Radio Log - New Entry", auto_id="newEntryWindow", control_type="Window")
		dlg1 = r.NewEntry
		dlg1.child_window(auto_id=NEW_ENTRY_PREFIX + ".teamField", control_type="Edit").set_edit_text(self._team_name(3))
		# dlg1.child_window(auto_id="Dialog.subjectLocatedButton", control_type="Button").click()
		dlg1.type_keys("{F11}")  # [F11] SUBJECT LOCATED
		# dlg = r.child_window(title="Subject Located", auto_id="subjectLocatedDialog", control_type="Window")
		dlg = r.SubjectLocated
		dlg.child_window(auto_id="subjectLocatedDialog.locationField", control_type="Edit").set_edit_text("12345 E 67890 N")
		dlg.child_window(auto_id="subjectLocatedDialog.conditionField", control_type="Edit").set_edit_text("Broken leg; heat exaustion; 2nd degree sunburn")
		dlg.child_window(auto_id="subjectLocatedDialog.resourcesField", control_type="Edit").set_edit_text("Stokes; burn cream")
		dlg.child_window(auto_id="subjectLocatedDialog.otherField", control_type="Edit").set_edit_text("Will meet EMS at Waypoint 7")
		# dlg.child_window(title="OK", control_type="Button").click()


	def clueLogAction(self):
		r = self.radiolog
		r.RadioLog.child_window(auto_id="Dialog.clueLogButton", control_type="Button").click()  # Open the clue log window
		# dlg = r.child_window(title="Clue Log", auto_id="clueLogDialog", control_type="Window")
		dlg = r.ClueLog
		self._discover_elements(dlg)


	def fsFilterAction(self):
		r = self.radiolog
		r.RadioLog.child_window(auto_id="Dialog.fsFilterButton", control_type="Button").click()  # Invoke filtering of the FS data
		# dlg = r.child_window(title="Radio Log - FleetSync Filter Setup", auto_id="fsFilterDialog", control_type="Window")
		dlg = r.RadioLogFleetSyncFilterSetup
		self._discover_elements(dlg)


	def printAction(self):
		r = self.radiolog
		r.RadioLog.child_window(auto_id="Dialog.printButton", control_type="Button").click()  # Open the print dialog
		# dlg = r.child_window(title="Print", auto_id="printDialog", control_type="Window")
		dlg = r.Print
		dlg.print_control_identifiers()



	def optionsAction(self):
		r = self.radiolog
		r.RadioLog.child_window(auto_id="Dialog.optionsButton", control_type="Button").click()  # Open the options window (e.g. Incident name)
		# dlg = r.child_window(title="Options", auto_id="optionsDialog", control_type="Window")
		dlg = r.Options
		self._discover_elements(dlg)


	def helpAction(self):
		r = self.radiolog
		r.RadioLog.child_window(auto_id="Dialog.helpButton", control_type="Button").click()  # Open the help window
		# dlg = r.child_window(title="Help", auto_id="Help", control_type="Window")
		# dlg = r.child_window(title="Help", auto_id="helpWindow", control_type="Window")
		dlg = r.Help
		self._discover_elements(dlg)


	def exitWihtoutPrinting(self):
		r = self.radiolog
		r.RadioLog.close()
		dlg = r.Exit
		self._discover_elements(dlg)

if __name__ == "__main__":
	main()


