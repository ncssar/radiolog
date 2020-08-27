import logging

from gwpycore import AppActions
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QHeaderView

LOG = logging.getLogger("main")


HelpDialogSpec = uic.loadUiType("app/ui/help.ui")[0]

HELP_FONT = QFont("Segoe UI", 9)
HELP_FONT_STRIKEOUT = QFont("Segoe UI", 9)
HELP_FONT_STRIKEOUT.setStrikeOut(True)


class HelpDialog(QDialog, HelpDialogSpec):
    def __init__(self, *args):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
        self.setFixedSize(self.size())

    def stylize(self, statusStyleDict):
        self.hotkeysTableWidget.setColumnWidth(1, 10)
        self.hotkeysTableWidget.setColumnWidth(0, 145)
        # note QHeaderView.setResizeMode is deprecated in 5.4, replaced with
        # .setSectionResizeMode but also has both global and column-index forms
        self.hotkeysTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.hotkeysTableWidget.resizeRowsToContents()

        self.colorLabel1.setStyleSheet(statusStyleDict["At IC"])
        self.colorLabel2.setStyleSheet(statusStyleDict["In Transit"])
        self.colorLabel3.setStyleSheet(statusStyleDict["Working"])
        self.colorLabel4.setStyleSheet(statusStyleDict["Waiting for Transport"])
        self.colorLabel5.setStyleSheet(statusStyleDict["TIMED_OUT_ORANGE"])
        self.colorLabel6.setStyleSheet(statusStyleDict["TIMED_OUT_RED"])

        self.fsSomeFilteredLabel.setFont(HELP_FONT)
        self.fsAllFilteredLabel.setFont(HELP_FONT_STRIKEOUT)
        self.fsSomeFilteredLabel.setStyleSheet(statusStyleDict["Working"])
        self.fsAllFilteredLabel.setStyleSheet(statusStyleDict["Working"])

    def update_blinking(self, blinkToggle, statusStyleDict):

        if blinkToggle == 1:
            self.colorLabel4.setStyleSheet(statusStyleDict[""])
            self.colorLabel5.setStyleSheet(statusStyleDict["TIMED_OUT_ORANGE"])
            self.colorLabel6.setStyleSheet(statusStyleDict["TIMED_OUT_RED"])
            self.colorLabel7.setStyleSheet(statusStyleDict[""])
            self.fsSomeFilteredLabel.setFont(HELP_FONT_STRIKEOUT)
        else:
            self.colorLabel4.setStyleSheet(statusStyleDict["Waiting for Transport"])
            self.colorLabel5.setStyleSheet(statusStyleDict[""])
            self.colorLabel6.setStyleSheet(statusStyleDict[""])
            self.colorLabel7.setStyleSheet(statusStyleDict["STANDBY"])
            self.fsSomeFilteredLabel.setFont(HELP_FONT)

    def set_hotkeys(self, act: AppActions):
        # FIXME Still need to actually place these hotkey description in the help window
        # FIXME These all currently only fetch the primary shortcut
        LOG.debug(f"helpInfo = {act.getActionInfo('helpInfo')}")
        LOG.debug(f"optionsDialog = {act.getActionInfo('optionsDialog')}")
        LOG.debug(f"printDialog = {act.getActionInfo('printDialog')}")
        LOG.debug(f"openLog = {act.getActionInfo('openLog')}")
        LOG.debug(f"reloadFleetsync = {act.getActionInfo('reloadFleetsync')}")
        LOG.debug(f"restoreLastSaved = {act.getActionInfo('restoreLastSaved')}")
        LOG.debug(f"muteFleetsync = {act.getActionInfo('muteFleetsync')}")
        LOG.debug(f"filterFleetsync = {act.getActionInfo('filterFleetsync')}")
        LOG.debug(f"toggleTeamHotkeys = {act.getActionInfo('toggleTeamHotkeys')}")
        LOG.debug(f"increaseFont = {act.getActionInfo('increaseFont')}")
        LOG.debug(f"decreaseFont = {act.getActionInfo('decreaseFont')}")
        LOG.debug(f"toTeam = {act.getActionInfo('toTeam')}")
        LOG.debug(f"toTeamsAll = {act.getActionInfo('toTeamsAll')}")
        LOG.debug(f"fromTeam = {act.getActionInfo('fromTeam')}")
        LOG.debug(f"fromTeam1 = {act.getActionInfo('fromTeam1')}")
        LOG.debug(f"fromTeam2 = {act.getActionInfo('fromTeam2')}")
        LOG.debug(f"fromTeam3 = {act.getActionInfo('fromTeam3')}")
        LOG.debug(f"fromTeam4 = {act.getActionInfo('fromTeam4')}")
        LOG.debug(f"fromTeam5 = {act.getActionInfo('fromTeam5')}")
        LOG.debug(f"fromTeam6 = {act.getActionInfo('fromTeam6')}")
        LOG.debug(f"fromTeam7 = {act.getActionInfo('fromTeam7')}")
        LOG.debug(f"fromTeam8 = {act.getActionInfo('fromTeam8')}")
        LOG.debug(f"fromTeam9 = {act.getActionInfo('fromTeam9')}")
        LOG.debug(f"fromTeam10 = {act.getActionInfo('fromTeam10')}")
