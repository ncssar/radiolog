from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QDialog, QHeaderView

HelpDialog = uic.loadUiType("app/ui/help.ui")[0]

HELP_FONT = QFont("Segoe UI", 9)
HELP_FONT_STRIKEOUT = QFont("Segoe UI",9)
HELP_FONT_STRIKEOUT.setStrikeOut(True)

class HelpWindow(QDialog, HelpDialog):
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


