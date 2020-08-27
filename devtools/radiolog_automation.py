import re
import sys
import time

from gwpycore import SimpleControlPanel
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from pywinauto import backend

sys.coinit_flags = 2
import pywinauto

PHONETIC_LIST = [
    "Alpha",
    "Bravo",
    "Charlie",
    "Delta",
    "Echo",
    "Foxtrot",
    "Golf",
    "Hotel",
    "India",
    "Juliet",
    "Kilo",
    "Lima",
    "Mike",
    "November",
    "Oscar",
    "Papa",
    "Quebec",
    "Romeo",
    "Sierra",
    "Tango",
    "Uniform",
    "Victor",
    "Whiskey",
    "Xray",
    "Yankee",
    "Zulu",
]
PHONETIC_DICT = {
    "A": "Alpha",
    "B": "Bravo",
    "C": "Charlie",
    "D": "Delta",
    "E": "Echo",
    "F": "Foxtrot",
    "G": "Golf",
    "H": "Hotel",
    "I": "India",
    "J": "Juliet",
    "K": "Kilo",
    "L": "Lima",
    "M": "Mike",
    "N": "November",
    "O": "Oscar",
    "P": "Papa",
    "Q": "Quebec",
    "R": "Romeo",
    "S": "Sierra",
    "T": "Tango",
    "U": "Uniform",
    "V": "Victor",
    "W": "Whiskey",
    "X": "Xray",
    "Y": "Yankee",
    "Z": "Zulu",
}


def main():
    """
    This script puts RadioLog through its paces.
    1. Start Radiolog running, if not already.
    2. Start this tool (in another terminal window)
    3. Choose between numeric or phonetic team names
    4. Click a button to invoke the corresponding action
    """
    qt_app = QApplication(sys.argv)
    global cp, auto_app, radiolog
    cp = TestingControlPanel()
    auto_app = pywinauto.application.Application()
    try:
        radiolog = pywinauto.application.Application(backend="uia").connect(title_re="Radio Log", class_name="MyWindow")
    except Exception as e:
        print(type(e).__name__)
        print(e)
        print("\nERROR: RadioLog must be running already.\n")
        sys.exit(1)
    cp.show()
    sys.exit(qt_app.exec_())


class TestingControlPanel(SimpleControlPanel):
    def __init__(self):
        SimpleControlPanel.__init__(self, title="RadioLog Automation", grid_height=8)

        self.chkPhonetic = self.add_checkbox("Use Phonetic Team Names", tip="Use team names like Team Alpha, Team Bravo, ... (instead of Team 1, Team 2, ...)")

        self.btnDeployTeams = self.add_action_button("Deploy 3 Teams", callback=deployTeams, tip="Add several entries to the log (radio checks, and team departing) -- using Team 1, Team 2, ...")

        self.btnTeamClue = self.add_action_button("Add a Team-Found Clue", callback=teamClue, tip="Add an entry that Team 3 found a clue")

        self.btnNonRadioClue = self.add_action_button("Add a Non-Radio Clue", callback=nonRadioClue, tip="Add an entry that a Ranger found a clue")

        self.btnSubjectLocated = self.add_action_button("Subject Located", callback=subjectLocatedAction)

        self.btnOpPeriodAction = self.add_action_button("Bump Operational Period", callback=opPeriodAction, tip="Invoke the form that bumps to a new operational period")

        self.btnClueLogAction = self.add_action_button("Open Clue Log Window", callback=clueLogAction)

        self.btnHelpAction = self.add_action_button("Open the Help Window", callback=helpAction)

        self.btnOptionsAction = self.add_action_button("Options Window", callback=optionsAction, tip="Open the options window (e.g. Incident name)")

        self.btnFsFilterAction = self.add_action_button("FS Filtering", callback=fsFilterAction, tip="Invoke filtering of the FS data")

        self.btnPrintAction = self.add_action_button("Open the Print Dialog", callback=printAction)

        self.move_to_next_cell()  # add a spacer

        self.btnExit = self.add_action_button("Exit Wihtout Printing", callback=exitWihtoutPrinting)


NEW_ENTRY_PREFIX = "newEntryWindow.tabWidget.qt_tabwidget_stackedwidget.newEntryWidget"


def _team_name(team_no):
    if cp.chkPhonetic.isChecked():
        return PHONETIC_LIST[team_no - 1]
    else:
        return "Team " + str(team_no)


def _discover_elements(control):
    try:
        control.print_control_identifiers()
    except pywinauto.findbestmatch.MatchError as e:
        print(f"Can't find [" + e.tofind + "]. Candidates are: " + ";".join(sorted(e.items)))


def deployTeams():
    radiolog.RadioLog.type_keys("f")
    dlg = radiolog.NewEntry
    dlg.child_window(auto_id=NEW_ENTRY_PREFIX + ".teamField", control_type="Edit").set_edit_text(_team_name(1))
    dlg.child_window(auto_id=NEW_ENTRY_PREFIX + ".messageField", control_type="Edit").set_edit_text("Radio check: OK")
    dlg.type_keys("{ENTER}")

    radiolog.RadioLog.type_keys("f")
    dlg = radiolog.NewEntry
    dlg.child_window(auto_id=NEW_ENTRY_PREFIX + ".teamField", control_type="Edit").set_edit_text(_team_name(2))
    dlg.child_window(auto_id=NEW_ENTRY_PREFIX + ".messageField", control_type="Edit").set_edit_text("Radio check: OK")
    dlg.type_keys("{ENTER}")

    radiolog.RadioLog.type_keys("f")
    dlg = radiolog.NewEntry
    dlg.child_window(auto_id=NEW_ENTRY_PREFIX + ".teamField", control_type="Edit").set_edit_text(_team_name(1))
    dlg.child_window(auto_id=NEW_ENTRY_PREFIX + ".messageField", control_type="Edit").set_edit_text("Departing IC")
    dlg.type_keys("{ENTER}")

    radiolog.RadioLog.type_keys("f")
    dlg = radiolog.NewEntry
    dlg.child_window(auto_id=NEW_ENTRY_PREFIX + ".teamField", control_type="Edit").set_edit_text(_team_name(3))
    dlg.child_window(auto_id=NEW_ENTRY_PREFIX + ".messageField", control_type="Edit").set_edit_text("Radio check: OK")
    dlg.type_keys("{ENTER}")

    radiolog.RadioLog.type_keys("f")
    dlg = radiolog.NewEntry
    dlg.child_window(auto_id=NEW_ENTRY_PREFIX + ".teamField", control_type="Edit").set_edit_text(_team_name(3))
    dlg.child_window(auto_id=NEW_ENTRY_PREFIX + ".messageField", control_type="Edit").set_edit_text("Departing IC")
    dlg.type_keys("{ENTER}")


def teamClue():
    radiolog.RadioLog.type_keys("f")
    # In case the "magic naming" on the next line doesn't work, here's the long way: dlg = radiolog.child_window(title="Radio Log - New Entry", auto_id="newEntryWindow", control_type="Window")
    dlg1 = radiolog.NewEntry
    dlg1.child_window(auto_id=NEW_ENTRY_PREFIX + ".teamField", control_type="Edit").set_edit_text(_team_name(3))
    dlg1.type_keys("{F10}")  # [F10] LOCATED A CLUE

    dlg = radiolog.ClueReport
    # dlg.print_control_identifiers()
    dlg.child_window(auto_id="clueDialog.descriptionField", control_type="Edit").set_edit_text("Candy Wrapper")
    dlg.child_window(auto_id="clueDialog.locationField", control_type="Edit").set_edit_text("12345 E 98765 N")
    # dlg.child_window(auto_id="clueDialog.instructionsField", control_type="Edit").set_edit_text("Mark & leave")
    dlg.type_keys("{F2}")  # [F2] MARK & LEAVE

    # We DO NOT want to print a report! So, let's uncheck this.
    dlg.child_window(auto_id="clueDialog.clueReportPrintCheckBox", control_type="CheckBox").click()
    dlg.OK.click()  # same as dlg.type_keys("{ENTER}")


def nonRadioClue():
    radiolog.RadioLog.NonRadioClue.click()
    # dlg = radiolog.child_window(title="Clue Report", auto_id="nonRadioClueDialog", control_type="Window")
    dlg = radiolog.ClueReport

    dlg.child_window(auto_id="nonRadioClueDialog.groupBox.callsignField", control_type="Edit").type_keys("Ranger")
    dlg.child_window(auto_id="nonRadioClueDialog.descriptionField", control_type="Edit").set_edit_text("Water bottle (Sparklets)")

    # We DO NOT want to print a report! So, let's uncheck this.
    dlg.child_window(auto_id="nonRadioClueDialog.clueReportPrintCheckBox", control_type="CheckBox").click()
    dlg.OK.click()  # same as dlg.type_keys("{ENTER}")


def opPeriodAction():
    radiolog.RadioLog.child_window(auto_id="Dialog.opPeriodButton", control_type="Button").click()  # Invoke the form that bumps to a new operational period
    # dlg = radiolog.child_window(title="Change Operational Period", auto_id="opPeriodDialog", control_type="Window")
    dlg = radiolog.ChangeOperationalPeriod


def subjectLocatedAction():
    radiolog.RadioLog.type_keys("f")
    # In case the "magic naming" on the next line doesn't work, here's the long way: dlg = radiolog.child_window(title="Radio Log - New Entry", auto_id="newEntryWindow", control_type="Window")
    dlg1 = radiolog.NewEntry
    dlg1.child_window(auto_id=NEW_ENTRY_PREFIX + ".teamField", control_type="Edit").set_edit_text(_team_name(3))
    # dlg1.child_window(auto_id="Dialog.subjectLocatedButton", control_type="Button").click()
    dlg1.type_keys("{F11}")  # [F11] SUBJECT LOCATED
    # dlg = radiolog.child_window(title="Subject Located", auto_id="subjectLocatedDialog", control_type="Window")
    dlg = radiolog.SubjectLocated
    dlg.child_window(auto_id="subjectLocatedDialog.locationField", control_type="Edit").set_edit_text("12345 E 67890 N")
    dlg.child_window(auto_id="subjectLocatedDialog.conditionField", control_type="Edit").set_edit_text("Broken leg; heat exaustion; 2nd degree sunburn")
    dlg.child_window(auto_id="subjectLocatedDialog.resourcesField", control_type="Edit").set_edit_text("Stokes; burn cream")
    dlg.child_window(auto_id="subjectLocatedDialog.otherField", control_type="Edit").set_edit_text("Will meet EMS at Waypoint 7")
    # dlg.child_window(title="OK", control_type="Button").click()


def clueLogAction():
    radiolog.RadioLog.child_window(auto_id="Dialog.clueLogButton", control_type="Button").click()  # Open the clue log window
    # dlg = radiolog.child_window(title="Clue Log", auto_id="clueLogDialog", control_type="Window")
    dlg = radiolog.ClueLog
    # _discover_elements(dlg)


def fsFilterAction():
    radiolog.RadioLog.child_window(auto_id="Dialog.fsFilterButton", control_type="Button").click()  # Invoke filtering of the FS data
    # dlg = radiolog.child_window(title="Radio Log - FleetSync Filter Setup", auto_id="fsFilterDialog", control_type="Window")
    dlg = radiolog.RadioLogFleetSyncFilterSetup
    # _discover_elements(dlg)


def printAction():
    radiolog.RadioLog.child_window(auto_id="Dialog.printButton", control_type="Button").click()  # Open the print dialog
    # dlg = radiolog.child_window(title="Print", auto_id="printDialog", control_type="Window")
    dlg = radiolog.Print
    dlg.print_control_identifiers()


def optionsAction():
    radiolog.RadioLog.child_window(auto_id="Dialog.optionsButton", control_type="Button").click()  # Open the options window (e.g. Incident name)
    # dlg = radiolog.child_window(title="Options", auto_id="optionsDialog", control_type="Window")
    dlg = radiolog.Options
    # _discover_elements(dlg)


def helpAction():
    radiolog.RadioLog.child_window(auto_id="Dialog.helpButton", control_type="Button").click()  # Open the help window
    # dlg = radiolog.child_window(title="Help", auto_id="Help", control_type="Window")
    # dlg = radiolog.child_window(title="Help", auto_id="helpWindow", control_type="Window")
    dlg = radiolog.Help
    # _discover_elements(dlg)


def exitWihtoutPrinting():
    radiolog.RadioLog.close()
    dlg = radiolog.Exit
    sys.exit(0)


if __name__ == "__main__":
    main()
