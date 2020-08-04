import sys, re

from pywinauto import backend
from pywinauto.application import Application as pwaApp

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


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

        self.rlog = Automator()

        self.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.setWindowTitle("RadioLog Automation")
        self.setMinimumSize(350,500)

        self.central_widget = QWidget(self)

        self.btnDeployNumeric = self.add_action_button(
            name="Deploy 3 Teams (Numeric)", parent=self.central_widget, x=10, y=10, callback=self.rlog.deployNumeric,
            tip="Add several entries to the log (radio checks, and team departing) -- using Team 1, Team 2, ...")

        self.btnDeployAlpha = self.add_action_button(
            name="Deploy 3 Teams (Phonetic)", parent=self.central_widget, x=10, y=30, callback=self.rlog.deployAlpha,
            tip="Add several new simple entries to the log (radio checks, and team departing) -- using Team Alpha, Team Bravo, ...")

        self.btnTeamClue = self.add_action_button(
            name="Add a Team-Found Clue", parent=self.central_widget, x=10, y=50, callback=self.rlog.teamClue,
            tip="Add an entry that Team 1 found a clue")

        self.btnTeamClue = self.add_action_button(
            name="Add a Non-Radio Clue", parent=self.central_widget, x=10, y=50, callback=self.rlog.nonRadioClue,
            tip="Add an entry that a second source found a clue")


    def add_action_button(self, name, parent, x, y, callback, tip):
        normalized_name = re.sub(r"[^A-Za-z0-9]+","",name)
        btn = QPushButton(parent)
        btn.setText(name)
        btn.setGeometry(QRect(x, y, 300, 22))
        btn.setMouseTracking(False)
        btn.setObjectName("btn" + normalized_name)
        btn.pressed.connect(callback)
        btn.setToolTip(tip)
        return btn

class Automator():
    def __init__(self) -> None:
        self.radiolog = pwaApp(backend="uia").connect(title_re="Radio Log", class_name="MyWindow")
        """
        {SCROLLLOCK}, {VK_SPACE}, {VK_LSHIFT}, {VK_PAUSE}, {VK_MODECHANGE},
        {BACK}, {VK_HOME}, {F23}, {F22}, {F21}, {F20}, {VK_HANGEUL}, {VK_KANJI},
        {VK_RIGHT}, {BS}, {HOME}, {VK_F4}, {VK_ACCEPT}, {VK_F18}, {VK_SNAPSHOT},
        {VK_PA1}, {VK_NONAME}, {VK_LCONTROL}, {ZOOM}, {VK_ATTN}, {VK_F10}, {VK_F22},
        {VK_F23}, {VK_F20}, {VK_F21}, {VK_SCROLL}, {TAB}, {VK_F11}, {VK_END},
        {LEFT}, {VK_UP}, {NUMLOCK}, {VK_APPS}, {PGUP}, {VK_F8}, {VK_CONTROL},
        {VK_LEFT}, {PRTSC}, {VK_NUMPAD4}, {CAPSLOCK}, {VK_CONVERT}, {VK_PROCESSKEY},
        {ENTER}, {VK_SEPARATOR}, {VK_RWIN}, {VK_LMENU}, {VK_NEXT}, {F1}, {F2},
        {F3}, {F4}, {F5}, {F6}, {F7}, {F8}, {F9}, {VK_ADD}, {VK_RCONTROL},
        {VK_RETURN}, {BREAK}, {VK_NUMPAD9}, {VK_NUMPAD8}, {RWIN}, {VK_KANA},
        {PGDN}, {VK_NUMPAD3}, {DEL}, {VK_NUMPAD1}, {VK_NUMPAD0}, {VK_NUMPAD7},
        {VK_NUMPAD6}, {VK_NUMPAD5}, {DELETE}, {VK_PRIOR}, {VK_SUBTRACT}, {HELP},
        {VK_PRINT}, {VK_BACK}, {CAP}, {VK_RBUTTON}, {VK_RSHIFT}, {VK_LWIN}, {DOWN},
        {VK_HELP}, {VK_NONCONVERT}, {BACKSPACE}, {VK_SELECT}, {VK_TAB}, {VK_HANJA},
        {VK_NUMPAD2}, {INSERT}, {VK_F9}, {VK_DECIMAL}, {VK_FINAL}, {VK_EXSEL},
        {RMENU}, {VK_F3}, {VK_F2}, {VK_F1}, {VK_F7}, {VK_F6}, {VK_F5}, {VK_CRSEL},
        {VK_SHIFT}, {VK_EREOF}, {VK_CANCEL}, {VK_DELETE}, {VK_HANGUL}, {VK_MBUTTON},
        {VK_NUMLOCK}, {VK_CLEAR}, {END}, {VK_MENU}, {SPACE}, {BKSP}, {VK_INSERT},
        {F18}, {F19}, {ESC}, {VK_MULTIPLY}, {F12}, {F13}, {F10}, {F11}, {F16},
        {F17}, {F14}, {F15}, {F24}, {RIGHT}, {VK_F24}, {VK_CAPITAL}, {VK_LBUTTON},
        {VK_OEM_CLEAR}, {VK_ESCAPE}, {UP}, {VK_DIVIDE}, {INS}, {VK_JUNJA},
        {VK_F19}, {VK_EXECUTE}, {VK_PLAY}, {VK_RMENU}, {VK_F13}, {VK_F12}, {LWIN},
        {VK_DOWN}, {VK_F17}, {VK_F16}, {VK_F15}, {VK_F14}

        Aliases:
        ~: {ENTER}
        +: {VK_SHIFT}
        ^: {VK_CONTROL}
        %: {VK_MENU} a.k.a. Alt key

        """

    def deployNumeric(self):
        print("Clicked deployNumeric")
        rlog = self.radiolog
        rlog.RadioLog.type_keys("1")
        rlog.NewEntry.type_keys("{TAB}Radio check: OK~")

        rlog.RadioLog.type_keys("2")
        rlog.NewEntry.type_keys("{TAB}Radio check: OK~")

        rlog.RadioLog.type_keys("1")
        rlog.NewEntry.type_keys("{TAB}Departing IC~")

        rlog.RadioLog.type_keys("3")
        rlog.NewEntry.type_keys("{TAB}Radio check: OK~")

        rlog.RadioLog.type_keys("3")
        rlog.NewEntry.type_keys("{TAB}Departing IC~")

        return

    def deployAlpha(self):
        print("Clicked deployAlpha")
        rlog = self.radiolog

    def teamClue(self):
        print("Clicked teamClue")
        rlog = self.radiolog
        rlog.RadioLog.type_keys("1")
        dlg = rlog.NewEntry
        dlg.print_control_identifiers()
        dlg.type_keys("{F10}")
        dlg.type_keys("Candy wrapper{TAB}")
        dlg.type_keys("12345 E 98765 N{TAB}")
        dlg.type_keys("Mark & leave")
        dlg.OK.click()
        return

    def nonRadioClue(self):
        print("Clicked nonRadioClue")
        rlog = self.radiolog
        rlog.RadioLog.NonRadioClue.click()
        dlg = rlog.ClueReport
        # dlg.print_control_identifiers()
        dlg.child_window(auto_id="nonRadioClueDialog.groupBox.callsignField", control_type="Edit").type_keys("Ranger")
        dlg.child_window(auto_id="nonRadioClueDialog.descriptionField", control_type="Edit").set_edit_text("Water bottle (Sparklets)")
        dlg.child_window(title="Print a Clue Report Form as soon as this clue is saved", auto_id="nonRadioClueDialog.clueReportPrintCheckBox", control_type="CheckBox").click()
        return

if __name__ == "__main__":
    main()


"""


rlog.RadioLog {
	mainform = Radio Log ahk_class Qt5150QWindowIcon
	WinWait, %mainform%
	IfWinNotActive, %mainform%,, WinActivate, %mainform%
	return
}

Wait4EntryForm() {
	entryform = Radio Log - New Entry ahk_class Qt5150QWindowIcon
	WinWait, %entryform%
	IfWinNotActive, %entryform%,, WinActivate, %entryform%
	return
}

rlog.ClueEntry {
	clueform = Clue Report ahk_class Qt5150QWindowIcon
	WinWait, %clueform%
	IfWinNotActive, %clueform%,, WinActivate, %clueform%
	return
}







"""
