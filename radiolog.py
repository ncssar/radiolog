"""
RadioLog is a tool for documenting the activities that occur during a Search and Rescue operation.

This file, radiolog.py, is the starting code.

See requirements.txt for the required modules (pip install -r requirements.txt).
(See the comments in requirements.txt for additional information.)

Originally developed for Nevada County Sheriff's Search and Rescue.
Copyright (c) 2015-2018 Tom Grundy

http://github.com/ncssar/radiolog

Attribution, feedback, bug reports and feature requests are appreciated
"""

# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed WITHOUT ANY WARRANTY; without even the implied
# warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# See included file LICENSE.txt for full license terms, also available at
# http://opensource.org/licenses/gpl-3.0.html
#
# IMPORTANT: this file must be encoded as UTF-8, to preserve degree signs in the code
#
# REVISION HISTORY: See doc_technical\CHANGE_LOG.adoc


import argparse
import csv
import math
import os
import os.path
import re
import subprocess
import sys
import textwrap
import time
from pathlib import Path
from typing import Optional

import requests
import serial
import serial.tools.list_ports
from gwpycore import (ICON_ERROR, ICON_INFO, ICON_WARN,
                      WindowsBehaviorAdjuster, ask_user_to_confirm,
                      inform_user_about_issue, normalizeName, setup_logging)
from pyproj import Transformer
from PyQt5 import uic
from PyQt5.QtCore import (
    QAbstractTableModel, QCoreApplication, QEvent, QFile, QModelIndex, QObject,
    QSortFilterProxyModel, Qt, QTextStream, QTimer, QVariant)
from PyQt5.QtGui import QIcon, QKeyEvent, QKeySequence, QPixmap
from PyQt5.QtWidgets import (QAbstractItemView, QApplication, QDialog,
                             QFileDialog, QGridLayout, QHeaderView, QLabel,
                             QMenu, QProgressDialog, QTabBar, QTableView,
                             QWidget)

from app.command_line import parse_args
from app.config import load_config
from app.db.file_management import (determine_rotate_method,
                                    ensureLocalDirectoryExists,
                                    getFileNameBase, viable_2wd)
from app.logic.app_state import (CONFIG, SWITCHES, TIMEOUT_DISPLAY_LIST,
                                 continueSec, lastClueNumber, teamStatusDict)
from app.logic.exceptions import RadioLogError
from app.logic.teams import getExtTeamName, getNiceTeamName, getShortNiceTeamName
from app.printing.print_log import printLog
from app.ui.clue_dialogs import (clueDialog, clueLogDialog, clueTableModel,
                                 nonRadioClueDialog)
from app.ui.fs_filter_dialog import fsFilterDialog
from app.ui.help_dialog import HelpDialog
from app.ui.hotkey_pool import TeamHotKeys
from app.ui.initialize_keymap import initializeMainWindowActions
from app.ui.new_entry_dialog import NewEntryWidget, NewEntryWindow
from app.ui.op_period_dialog import opPeriodDialog
from app.ui.options_dialog import OptionsDialog
from app.ui.print_dialogs import PrintDialog, printClueLogDialog

# NOTE: SWITCHES is declared in app.logic.app_state (as an empty namespace)
SWITCHES = parse_args(sys.argv[1:])
# print(f"SWITCHES = {SWITCHES}")

# TODO Autodetect the screen resolution, but still allow a command line switch to override
if SWITCHES.minmode:
    # built to look decent at 800x600
    UiDialog = uic.loadUiType("app/ui/radiolog_min.ui")[0]
else:
    # normal version, for higher resolution
    UiDialog = uic.loadUiType("app/ui/radiolog.ui")[0]

# ConvertDialog = uic.loadUiType("app/ui/convertDialog.ui")[0]

statusStyleDict = {}
# even though tab labels are created with font-size:20px and the tab sizes and margins are created accordingly,
#  something after creation time is changing font-sizes to a smaller size.  So, just
#  hardcode them all here to force 20px always.
tabFontSize = "20px"
statusStyleDict["At IC"] = "font-size:" + tabFontSize + ";background:#00ff00;border:1px outset black;padding-left:0px;padding-right:0px"
statusStyleDict["In Transit"] = "font-size:" + tabFontSize + ";background:blue;color:white;border:1px outset black;padding-left:0px;padding-right:0px"
statusStyleDict["Working"] = "font-size:" + tabFontSize + ";background:none;border:1px outset black;padding-left:0px;padding-right:0px"
statusStyleDict["Off Duty"] = "font-size:" + tabFontSize + ";color:#aaaaaa;background:none;border:none;padding-left:0px;padding-right:0px"
# Waiting for Transport and Available should still flash even if not timed out, but they don't
#  prevent a timeout.  So, for this code, and alternating timer cycles (seconds):
# cycle 1: style as in the line specified for that status name
# cycle 2: if not timed out, style as "" (blank); if timed out, style as timeout as expected
statusStyleDict["Available"] = "font-size:" + tabFontSize + ";background:#00ffff;border:1px outset black;padding-left:0px;padding-right:0px;padding-top:-1px;padding-bottom:-1px"
statusStyleDict["Waiting for Transport"] = "font-size:" + tabFontSize + ";background:blue;color:white;border:1px outset black;padding-left:0px;padding-right:0px;padding-top:-1px;padding-bottom:-1px"
statusStyleDict["STANDBY"] = "font-size:" + tabFontSize + ";background:black;color:white;border:1px outset black;padding-left:0px;padding-right:0px;padding-top:-1px;padding-bottom:-1px"
statusStyleDict[""] = "font-size:" + tabFontSize + ";background:none;padding-left:1px;padding-right:1px"
statusStyleDict["TIMED_OUT_ORANGE"] = "font-size:" + tabFontSize + ";background:orange;border:1px outset black;padding-left:0px;padding-right:0px;padding-top:-1px;padding-bottom:-1px"
statusStyleDict["TIMED_OUT_RED"] = "font-size:" + tabFontSize + ";background:red;border:1px outset black;padding-left:0px;padding-right:0px;padding-top:-1px;padding-bottom:-1px"


teamFSFilterDict = {}
teamTimersDict = {}
teamCreatedTimeDict = {}

# TODO Move these settings to the config file
versionDepth = 5  # how many backup versions to keep; see rotateBackups


# log com port messages?
comLog = False

# newEntryDialogTimeoutSeconds=600
# choosing window location for newly opened dialog: just keeping a count of how many
# dialogs are open does not work, since an open dialog at a given position could
# still be completely covered by a newly opened dialog at that same position.
# Instead, create a list of valid fixed positions, then each newly opened dialog
# will just use the first available one in the list.  Update the list of which ones
# are used when each dialog is opened.
# openNewEntryDialogCount=0
# newEntryDialog_x0=100
# newEntryDialog_y0=100
# newEntryDialog_dx=30
# newEntryDialog_dy=30


# quickTextList=[
# ["DEPARTING IC",Qt.Key_F1],
# ["STARTING ASSIGNMENT",Qt.Key_F2],
# ["COMPLETED ASSIGNMENT",Qt.Key_F3],
# ["ARRIVING AT IC",Qt.Key_F4],
# "separator",
# ["RADIO CHECK: OK",Qt.Key_F5],
# ["WELFARE CHECK: OK",Qt.Key_F6],
# ["REQUESTING TRANSPORT",Qt.Key_F7],
# "separator",
# ["STANDBY",Qt.Key_F8],
# "separator",
# ["LOCATED A CLUE",Qt.Key_F9],
# "separator",
# ["SUBJECT LOCATED",Qt.Key_F10],
# "separator",
# ["REQUESTING DEPUTY",Qt.Key_F11]]

logfilepath: Optional[Path] = None
if not SWITCHES.nologfile:
    logfilepath = Path(SWITCHES.logfile)
LOG = setup_logging("main", loglevel=SWITCHES.loglevel, logfile=logfilepath, nocolor=SWITCHES.nocolor)

BG_GREEN = "background-color:#00bb00"
BG_RED = "background-color:#bb0000"
BG_DARK_GREEN = "background-color:#00ff00"
BG_GRAY = "background-color:#aaaaaa"
BG_BROWN = "background-color:#ff5050"
BG_LIGHT_GRAY = "background-color:lightgray"
BG_NONE = "background-color:none"
BG_WHITE = "background-color:white"


class MyWindow(QDialog, UiDialog):
    def __init__(self, parent):
        QDialog.__init__(self)

        issue = ensureLocalDirectoryExists()
        if issue:
            inform_user_about_issue(issue, icon=ICON_WARN, parent=self)

        self.setWindowFlags(self.windowFlags() | Qt.WindowMinMaxButtonsHint)
        self.parent = parent
        self.setupUi(self)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.loadFlag = False  # set this to true during load, to prevent save on each newEntry
        self.totalEntryCount = 0  # rotate backups after every 5 entries; see NewEntryWidget.accept

        self.teamHotkeysWidget.setVisible(False)  # disabled by default
        self.team_hot_keys = TeamHotKeys()
        self.homeDir = os.path.expanduser("~")

        # fix #342 (focus-follows-mouse causes freezes) - disable FFM here;
        self.windows_behavior_adjuster = WindowsBehaviorAdjuster()
        self.windows_behavior_adjuster.disableWindowTracking()

        self.incidentName = "New Incident"
        self.incidentNameNormalized = normalizeName(self.incidentName)
        self.opPeriod = 1
        self.incidentStartDate = time.strftime("%a %b %d, %Y")

        self.radioLog = [[time.strftime("%H%M"), "", "", "Radio Log Begins: " + self.incidentStartDate, "", "", time.time(), "", "", ""], ["", "", "", "", "", "", 1e10, "", "", ""]]  # 1e10 epoch seconds will keep the blank row at the bottom when sorted

        self.clueLog = []
        self.clueLog.append(["", self.radioLog[0][3], "", time.strftime("%H%M"), "", "", "", "", ""])

        self.lastFileName = ""  # to force error in restore, in the event the resource file doesn't specify the lastFileName
        # 		self.csvFileName=getFileNameBase(self.incidentNameNormalized)+".csv"
        # 		self.pdfFileName=getFileNameBase(self.incidentNameNormalized)+".pdf"
        self.updateFileNames()
        self.lastSavedFileName = "NONE"
        ##		self.fsFileName=self.getFileNameBase(self.incidentNameNormalized)+"_fleetsync.csv"

        # disable fsValidFleetList checking to allow arbitrary fleets; this
        #  idea is probably obsolete
        # 		self.fsValidFleetList=[100]
        self.fsLog = []
        # 		self.fsLog.append(['','','','',''])
        self.fsMuted = False
        self.noSend = SWITCHES.nosend
        self.fsMutedBlink = False
        self.fsFilterBlinkState = False
        self.getString = ""

        self.firstWorkingDir = os.getenv("HOMEPATH", "C:\\Users\\Default") + "\\Documents"
        if self.firstWorkingDir[1] != ":":
            self.firstWorkingDir = os.getenv("HOMEDRIVE", "C:") + self.firstWorkingDir
        # 		self.secondWorkingDir=os.getenv('HOMEPATH','C:\\Users\\Default')+"\\Documents\\sar"

        ##		# attempt to change to the second working dir and back again, to 'wake up'
        ##		#  any mount points, to hopefully avoid problems of second working dir
        ##		#  not always being written to, at all, for a given run of this program;
        ##		#  os.chdir dies gracefully if the specified dir does not exist
        ##		self.cwd=os.getcwd()
        ##		LOG.debug("t1")
        ##		os.chdir(self.secondWorkingDir)
        ##		LOG.debug("t2")
        ##		os.chdir(self.cwd)
        ##		LOG.debug("t3")

        self.optionsDialog = OptionsDialog(self)
        self.optionsDialog.accepted.connect(self.optionsAccepted)

        self.validDatumList = ["WGS84", "NAD27", "NAD27 CONUS"]
        self.timeoutDisplaySecList = [i[1] for i in TIMEOUT_DISPLAY_LIST]
        self.timeoutDisplayMinList = [int(i / 60) for i in self.timeoutDisplaySecList if i >= 60]

        # coordinate system name translation dictionary:
        #  key = ASCII name in the config file
        #  value = utf-8 name used in the rest of this code
        self.csDisplayDict = {}
        self.csDisplayDict["UTM 5x5"] = "UTM 5x5"
        self.csDisplayDict["UTM 7x7"] = "UTM 7x7"
        self.csDisplayDict["D.d"] = "D.d°"
        self.csDisplayDict["DM.m"] = "D° M.m'"
        self.csDisplayDict["DMS.s"] = "D° M' S.s\""

        self.sourceCRS = 0
        self.targetCRS = 0

        # config file (e.g. ./local/radiolog.cfg) stores the team standards;
        #  it should be created/modified by hand, and is read at radiolog startup,
        #  and is not modified by radiolog at any point
        # resource file / 'rc file' (e.g. ./radiolog_rc.txt) stores the search-specific
        #  options settings; it is read at radiolog startup, and is written
        #  whenever the options dialog is accepted

        # FIXME -- We are still calling the old method (readConfigFile) that loads the config settings (radiolog.cfg) into fields of MyWindow (self), because much of the existing code still looks there.
        # FIXME -- We are ALSO calling the new method (load_config) that loads similar config settings (radiolog.ini) into the CONFIG namespace (in app.logic.app_state).
        # FIXME -- (If radiolog.ini does not exist, then we call self.copy_oldstyle_config_to_new().)
        # FIXME -- Eventually, all of the code will look to the new INI file, and we can stop calling readConfigFile.
        # FIXME -- And then we won't need copy_oldstyle_config_to_new() anymore, either.
        self.configFileName = "local/radiolog.cfg"
        self.readConfigFile()  # defaults are set inside readConfigFile
        LOG.debug(f"SWITCHES.configfile = {SWITCHES.configfile}")
        if os.path.isfile(SWITCHES.configfile):
            load_config(filename=SWITCHES.configfile, config=CONFIG)
        else:
            self.copy_oldstyle_config_to_new()

        # set the default lookup name - this must be after readConfigFile
        #  since that function accepts the options form which updates the
        #  lookup filename based on the current incedent name and time
        self.fsFileName = "radiolog_fleetsync.csv"

        self.helpWindow = HelpDialog()
        self.helpWindow.stylize(statusStyleDict)

        self.printDialog = PrintDialog(self)
        self.printClueLogDialog = printClueLogDialog(self)

        self.radioLogNeedsPrint = False  # set to True with each new log entry; set to False when printed
        self.clueLogNeedsPrint = False

        self.fsFilterDialog = fsFilterDialog(self)
        self.fsFilterDialog.tableView.setColumnWidth(0, 50)
        self.fsFilterDialog.tableView.setColumnWidth(1, 75)
        self.fsBuildTooltip()

        self.addNonRadioClueButton.clicked.connect(self.addNonRadioClue)

        self.helpButton.clicked.connect(self.helpWindow.show)
        self.optionsButton.clicked.connect(self.optionsDialog.show)
        self.fsFilterButton.clicked.connect(self.fsFilterDialog.show)
        self.printButton.clicked.connect(self.printDialog.show)
        ##		self.printButton.clicked.connect(self.testConvertCoords)

        initializeMainWindowActions(self)
        self.helpWindow.set_hotkeys(self.act)
        self.use_phonetic = "Alpha" in self.act.fromTeam1.text()

        # FIXME The F1 and F2 keys are broken because the shortcuts defined directly in the
        # help and config buttons conflict with the ones in these actions.
        # We need to swap out the HBoxLayout for a QToolBar (which is an action based
        # container) so that we can use the actions rather than buttons.
        self.act.helpInfo.triggered.connect(self.helpWindow.show)
        self.act.optionsDialog.triggered.connect(self.optionsDialog.show)
        self.act.printDialog.triggered.connect(self.printDialog.show)
        self.act.openLog.triggered.connect(self.load)
        self.act.reloadFleetsync.triggered.connect(self.reloadFleetsync)
        self.act.restoreLastSaved.triggered.connect(self.restoreLastSaved)
        self.act.muteFleetsync.triggered.connect(self.fsCheckBox.toggle)
        self.act.filterFleetsync.triggered.connect(self.fsFilterDialog.show)
        self.act.toggleTeamHotkeys.triggered.connect(self.toggleTeamHotkeys)
        self.act.increaseFont.triggered.connect(self.increaseFont)
        self.act.decreaseFont.triggered.connect(self.decreaseFont)
        self.act.toTeam.triggered.connect(self.toTeam)
        self.act.toTeamsAll.triggered.connect(self.toTeamsAll)
        self.act.fromTeam.triggered.connect(self.fromTeam)
        self.act.fromTeam1.triggered.connect(self.fromTeam1)
        self.act.fromTeam2.triggered.connect(self.fromTeam2)
        self.act.fromTeam3.triggered.connect(self.fromTeam3)
        self.act.fromTeam4.triggered.connect(self.fromTeam4)
        self.act.fromTeam5.triggered.connect(self.fromTeam5)
        self.act.fromTeam6.triggered.connect(self.fromTeam6)
        self.act.fromTeam7.triggered.connect(self.fromTeam7)
        self.act.fromTeam8.triggered.connect(self.fromTeam8)
        self.act.fromTeam9.triggered.connect(self.fromTeam9)
        self.act.fromTeam10.triggered.connect(self.fromTeam10)
        self.act.fromSar.triggered.connect(self.fromSar)

        self.tabList = ["dummy"]
        self.tabGridLayoutList = ["dummy"]
        self.tableViewList = ["dummy"]
        self.proxyModelList = ["dummy"]
        self.teamNameList = ["dummy"]
        self.allTeamsList = ["dummy"]  # same as teamNameList but hidden tabs are not deleted from this list
        self.extTeamNameList = ["dummy"]
        self.fsLookup = []

        ##		self.newEntryDialogList=[]
        self.blinkToggle = 0
        self.fontSize = 10
        # font size is constrained to min and max for several items
        self.minLimitedFontSize = 8
        self.maxLimitedFontSize = 20
        self.x = 100
        self.y = 100
        self.w = 600
        self.h = 400
        self.clueLog_x = 200
        self.clueLog_y = 200
        self.clueLog_w = 1000
        self.clueLog_h = 400
        self.firstComPortAlive = False
        self.secondComPortAlive = False
        self.firstComPortFound = False
        self.secondComPortFound = False
        self.comPortScanInProgress = False
        self.comPortTryList = []
        ##		if SWITCHES.devmode:
        ##			self.comPortTryList=[serial.Serial("\\\\.\\CNCB0")] # DEVEL
        self.fsBuffer = ""
        self.entryHold = False
        self.currentEntryLastModAge = 0

        self.opPeriodDialog = opPeriodDialog(self)
        self.clueLogDialog = clueLogDialog(self)

        self.pushButton.clicked.connect(self.openNewEntry)
        self.opPeriodButton.clicked.connect(self.openOpPeriodDialog)
        self.clueLogButton.clicked.connect(self.clueLogDialog.show)  # never actually close this dialog

        self.splitter.setSizes([250, 150])  # any remainder is distributed based on this ratio
        self.splitter.splitterMoved.connect(self.tableView.scrollToBottom)

        self.tableModel = MyTableModel(self.radioLog, self)
        self.tableView.setModel(self.tableModel)
        self.tableView.setSelectionMode(QAbstractItemView.NoSelection)

        self.tableView.hideColumn(6)  # hide epoch seconds
        self.tableView.hideColumn(7)  # hide fleet
        self.tableView.hideColumn(8)  # hide device
        self.tableView.hideColumn(9)  # hide device
        self.tableView.resizeRowsToContents()

        self.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tableView.customContextMenuRequested.connect(self.tableContextMenu)

        # downside of the following line: slow, since it results in a resize call for each column,
        #  when we could defer and just do one resize at the end of all the resizes
        ##		self.tableView.horizontalHeader().sectionResized.connect(self.tableView.resizeRowsToContents)
        self.columnResizedFlag = False
        self.tableView.horizontalHeader().sectionResized.connect(self.setColumnResizedFlag)

        self.exitClicked = False
        # NOTE - the padding numbers for ::tab take a while to figure out in conjunction with
        #  the stylesheets of the label widgets of each tab in order to change status; don't
        #  change these numbers unless you want to spend a while on trial and error to get
        #  them looking good again!
        self.tabWidget.setStyleSheet(
            """
            QTabBar::tab {
                margin:0px;
                padding-left:0px;
                padding-right:0px;
                padding-bottom:8px;
                padding-top:0px;
                border-top-left-radius:4px;
                border-top-right-radius:4px;
                border:1px solid gray;
                font-size:20px;
            }
            QTabBar::tab:selected {
                background:white;
                border-bottom-color:white;
            }
            QTabBar::tab:!selected {
                margin-top:3px;
            }
            QTabBar::tab:disabled {
                width:20px;
                color:black;
                font-weight:bold;
                background:transparent;
                border:transparent;
                padding-bottom:3px;
            }
        """
        )

        # NOTE if you do this section before the model is assigned to the tableView,
        # python will crash every time!
        # see the QHeaderView.ResizeMode docs for descriptions of each resize mode value
        # note QHeaderView.setResizeMode is deprecated in 5.4, replaced with
        # .setSectionResizeMode but also has both global and column-index forms
        # NOTE also - do NOT set any to ResizeToContents - this slows things down a lot!
        #  only resize when needed!
        self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # automatically expand the 'message' column width to fill available space
        self.tableView.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)

        self.updateClock()

        self.fsLoadLookup(startupFlag=True)

        self.teamTimer = QTimer(self)
        self.teamTimer.timeout.connect(self.updateTeamTimers)
        self.teamTimer.timeout.connect(self.fsCheck)
        self.teamTimer.timeout.connect(self.updateClock)
        self.teamTimer.start(1000)

        self.fastTimer = QTimer(self)
        self.fastTimer.timeout.connect(self.resizeRowsToContentsIfNeeded)
        self.fastTimer.start(100)

        self.tabWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabWidget.customContextMenuRequested.connect(self.tabContextMenu)

        self.newEntryWindow = NewEntryWindow(self)  # create the window but don't show it until needed

        # load resource file; process default values and resource file values
        self.rcFileName = "radiolog_rc.txt"
        self.previousCleanShutdown = self.loadRcFile()
        showStartupOptions = True
        if not self.previousCleanShutdown:
            if ask_user_to_confirm("The previous Radio Log session may have shut down incorrectly.  Do you want to restore the last saved files (Radio Log, Clue Log, and FleetSync table)?", title="Restore last saved files?", icon=ICON_ERROR, parent=self):
                self.restore()
                showStartupOptions = False

        # make sure x/y/w/h from resource file will fit on the available display
        d = QApplication.desktop()
        if (self.x + self.w > d.width()) or (self.y + self.h > d.height()):
            LOG.warning("The resource file specifies a main window geometry that is bigger than (or not on) the available desktop. Using default sizes for this session.")
            self.x = 50
            self.y = 50
            self.w = d.availableGeometry(self).width() - 100
            self.h = d.availableGeometry(self).height() - 100
        if (self.clueLog_x + self.clueLog_w > d.width()) or (self.clueLog_y + self.clueLog_h > d.height()):
            LOG.warning("The resource file specifies a clue log window geometry that is bigger than (or not on) the available desktop. Using default sizes for this session.")
            self.clueLog_x = 75
            self.clueLog_y = 75
            self.clueLog_w = d.availableGeometry(self).width() - 100
            self.clueLog_h = d.availableGeometry(self).height() - 100
        self.setGeometry(int(self.x), int(self.y), int(self.w), int(self.h))
        self.clueLogDialog.setGeometry(int(self.clueLog_x), int(self.clueLog_y), int(self.clueLog_w), int(self.clueLog_h))
        self.fontsChanged()

        self.timeoutLabel.setText("TIMEOUT:\n" + TIMEOUT_DISPLAY_LIST[self.optionsDialog.timeoutField.value()][0])
        # pop up the options dialog to enter the incident name right away
        if showStartupOptions:
            QTimer.singleShot(1000, self.startupOptions)
        # save current resource file, to capture lastFileName without a clean shutdown
        self.saveRcFile()

    def readConfigFile(self):
        # TODO Use Python's built-in ConfigParser for this
        # specify defaults here
        self.fillableClueReportPdfFileName = "clueReportFillable.pdf"
        self.agencyName = "Search and Rescue"
        self.datum = "WGS84"
        self.coordFormatAscii = "UTM 5x5"
        self.coordFormat = self.csDisplayDict[self.coordFormatAscii]
        self.timeoutMinutes = "30"
        self.printLogoFileName = "radiolog_logo.jpg"
        self.firstWorkingDir = self.homeDir + "\\Documents"
        self.secondWorkingDir = None
        self.sarsoftServerName = "localhost"
        (self.rotateScript, self.rotateDelimiter) = determine_rotate_method()

        # 		self.tabGroups=[["NCSO","^1[tpsdel][0-9]+"],["CHP","^22s[0-9]+"],["Numbers","^Team [0-9]+"]]
        # the only default tab group should be number-only callsigns; everything
        #  else goes in a separate catch-all group; override this in radiolog.cfg
        defaultTabGroups = [["Numbers", "^Team [0-9]+"]]
        self.tabGroups = defaultTabGroups

        configFile = QFile(self.configFileName)
        if not configFile.open(QFile.ReadOnly | QFile.Text):
            issue = "Cannot read configuration file {0}; using default settings. {1}".format(self.configFileName, configFile.errorString())
            LOG.warning(issue)
            inform_user_about_issue(issue, icon=ICON_WARN, parent=self)
            self.timeoutRedSec = int(self.timeoutMinutes) * 60
            self.updateOptionsDialog()
            return
        inStr = QTextStream(configFile)
        line = inStr.readLine()
        if line != "[RadioLog]":
            issue = "Specified configuration file {0} is not a valid configuration file; using default settings.".format(self.configFileName)
            LOG.warning(issue)
            inform_user_about_issue(issue, icon=ICON_WARN, parent=self)
            configFile.close()
            self.timeoutRedSec = int(self.timeoutMinutes) * 60
            self.updateOptionsDialog()
            return

        while not inStr.atEnd():
            line = inStr.readLine()
            tokens = line.split("=")
            if tokens[0] == "agencyName":
                self.agencyName = tokens[1]
            elif tokens[0] == "datum":
                self.datum = tokens[1]
            elif tokens[0] == "coordFormat":
                self.coordFormatAscii = tokens[1]
            elif tokens[0] == "timeoutMinutes":
                self.timeoutMinutes = tokens[1]
            elif tokens[0] == "logo":
                self.printLogoFileName = tokens[1]
            elif tokens[0] == "clueReport":
                self.fillableClueReportPdfFileName = tokens[1]
            elif tokens[0] == "firstWorkingDir":
                self.firstWorkingDir = tokens[1]
            elif tokens[0] == "secondWorkingDir":
                self.secondWorkingDir = tokens[1]
            elif tokens[0] == "server":
                self.sarsoftServerName = tokens[1]
            elif tokens[0] == "rotateScript":
                self.rotateScript = tokens[1]
            elif tokens[0] == "rotateDelimiter":
                self.rotateDelimiter = tokens[1]
            elif tokens[0] == "tabGroups":
                self.tabGroups = eval(tokens[1])
        configFile.close()

        # validation and post-processing of each item
        configErr = ""
        self.printLogoFileName = "./local/" + self.printLogoFileName

        if self.datum not in self.validDatumList:
            configErr += "ERROR: invalid datum '" + self.datum + "'\n"
            configErr += "  Valid choices are: " + str(self.validDatumList) + "\n"
            configErr += "  Will use " + str(self.validDatumList[0]) + " for this session.\n\n"
            self.datum = self.validDatumList[0]
        # if specified datum is just NAD27, assume NAD27 CONUS
        if self.datum == "NAD27":
            self.datum = "NAD27 CONUS"

        if self.coordFormatAscii not in self.csDisplayDict:
            configErr += "ERROR: coordinate format '" + self.coordFormatAscii + "'\n"
            configErr += "  Supported coordinate format names are: " + str(list(self.csDisplayDict.keys())) + "\n"
            configErr += "  Will use " + list(self.csDisplayDict.keys())[0] + " for this session.\n\n"
            self.coordFormatAscii = list(self.csDisplayDict.keys())[0]

        # process any ~ characters
        self.firstWorkingDir = os.path.expanduser(self.firstWorkingDir)
        if self.secondWorkingDir:
            self.secondWorkingDir = os.path.expanduser(self.secondWorkingDir)

        if not os.path.isdir(self.firstWorkingDir):
            raise RadioLogError("Configuration error: The specified first working directory '{0}' does not exist.".format(self.firstWorkingDir))

        if self.use2WD and self.secondWorkingDir and not os.path.isdir(self.secondWorkingDir):
            configErr += "ERROR: second working directory '" + self.secondWorkingDir + "' does not exist.  Maybe it is not mounted yet; radiolog will try to write to it after every entry.\n\n"

        self.coordFormat = self.csDisplayDict[self.coordFormatAscii]
        self.datumFormatLabel.setText(self.datum + "\n" + self.coordFormat)

        if not self.timeoutMinutes.isdigit():
            configErr += "ERROR: timeout minutes value must be an integer.  Will use 30 minutes for this session.\n\n"
            self.timeoutMinutes = 30
        self.timeoutRedSec = int(self.timeoutMinutes) * 60
        if self.timeoutRedSec not in self.timeoutDisplaySecList:
            configErr += "ERROR: invalid timeout period (" + str(self.timeoutMinutes) + " minutes)\n"
            configErr += "  Valid choices:" + str(self.timeoutDisplayMinList) + "\nWill use 30 minutes for this session.\n\n"
            self.timeoutRedSec = 1800

        self.updateOptionsDialog()

        # if agencyName contains newline character(s), use it as-is for print;
        #  if not, textwrap with max line length that looks best on pdf reports
        self.agencyNameForPrint = self.agencyName
        if "\n" not in self.agencyName:
            self.agencyNameForPrint = "\n".join(textwrap.wrap(self.agencyName.upper(), width=int(len(self.agencyName) / 2 + 6)))

        if not os.path.isfile(self.fillableClueReportPdfFileName):
            configErr += "ERROR: specified fillable clue report pdf file '" + self.fillableClueReportPdfFileName + "' does not exist.  Clue report forms will NOT be generated for this session.\n\n"
            self.fillableClueReportPdfFileName = None

        if not os.path.isfile(self.printLogoFileName):
            configErr += "ERROR: specified logo file '" + self.printLogoFileName + "' does not exist.  No logo will be included on generated reports.\n\n"

        if not isinstance(self.tabGroups, list):
            configErr += "ERROR: specified tab group '" + str(self.tabGroups) + "' is not a list.  Using the default tabGroups group list.\n\n"
            self.tabGroups = defaultTabGroups

        if configErr:
            inform_user_about_issue("Error(s) encountered in config file " + self.configFileName + ":\n\n" + configErr, icon=ICON_WARN, title="Non-fatal Configuration Error(s)", parent=self)

        if SWITCHES.devmode:
            self.sarsoftServerName = "localhost"  # DEVEL

    def copy_oldstyle_config_to_new(self):
        CONFIG.agencyName = self.agencyName
        CONFIG.logo = Path(self.printLogoFileName)
        if self.fillableClueReportPdfFileName:
            CONFIG.clueReport = Path(self.fillableClueReportPdfFileName)
        CONFIG.firstWorkingDir = Path(self.firstWorkingDir)
        if self.secondWorkingDir:
            CONFIG.secondWorkingDir = Path(self.secondWorkingDir)
        CONFIG.tabGroups = self.tabGroups
        # CONFIG.coordFormat = self.coordFormat
        # CONFIG.datum = self.datum
        CONFIG.rotateDelimiter = self.rotateDelimiter
        CONFIG.rotateScript = self.rotateScript
        CONFIG.sarsoftServerName = self.sarsoftServerName
        CONFIG.timeoutMinutes = self.timeoutMinutes

    def getPrintParams(self) -> argparse.Namespace:
        """
        This is temporary. Ultimately, this all needs to move to config settings or app-state settigs.
        """
        printParams = argparse.Namespace()
        printParams.agencyNameForPrint = self.agencyNameForPrint
        printParams.allTeamsList = self.allTeamsList
        printParams.datum = self.datum
        printParams.incidentName = self.incidentName
        printParams.pdfFileName = self.pdfFileName
        printParams.printLogoFileName = self.printLogoFileName
        printParams.radioLog = self.radioLog
        printParams.radioLogNeedsPrint = self.radioLogNeedsPrint
        printParams.header_labels = self.tableModel.header_labels
        printParams.clue_log_header_labels = clueTableModel.header_labels
        printParams.clueLog = self.clueLog
        printParams.fillableClueReportPdfFileName = self.fillableClueReportPdfFileName
        return printParams

    def increaseFont(self):
        self.fontSize = self.fontSize + 2
        self.fontsChanged()

    def decreaseFont(self):
        if self.fontSize > 4:
            self.fontSize = self.fontSize - 2
            self.fontsChanged()

    def reloadFleetsync(self):
        self.fsLoadLookup()
        self.teamHotkeysWidget.setVisible(not self.teamHotkeysWidget.isVisible())

    def restoreLastSaved(self):
        if ask_user_to_confirm("Restore the last saved files (Radio Log, Clue Log, and FleetSync table)?", parent=self):
            self.restore()

    def toTeam(self):
        self.openNewEntry("t")

    def toTeamsAll(self):
        self.openNewEntry("a")

    def fromTeam(self):
        self.openNewEntry("f")

    def fromTeam1(self):
        self.openNewEntry("Alpha" if self.use_phonetic else "1")

    def fromTeam2(self):
        self.openNewEntry("Bravo" if self.use_phonetic else "2")

    def fromTeam3(self):
        self.openNewEntry("Charlie" if self.use_phonetic else "3")

    def fromTeam4(self):
        self.openNewEntry("Delta" if self.use_phonetic else "4")

    def fromTeam5(self):
        self.openNewEntry("Echo" if self.use_phonetic else "5")

    def fromTeam6(self):
        self.openNewEntry("Foxtrot" if self.use_phonetic else "6")

    def fromTeam7(self):
        self.openNewEntry("Golf" if self.use_phonetic else "7")

    def fromTeam8(self):
        self.openNewEntry("Hotel" if self.use_phonetic else "8")

    def fromTeam9(self):
        self.openNewEntry("India" if self.use_phonetic else "9")

    def fromTeam10(self):
        self.openNewEntry("Juliet" if self.use_phonetic else "10")

    def fromSar(self):
        self.openNewEntry("s")

    def rotateCsvBackups(self, filenames):
        if self.rotateScript and self.rotateDelimiter:
            cmd = self.rotateScript + " " + self.rotateDelimiter.join(filenames)
            LOG.info("Invoking backup rotation script: " + cmd)
            subprocess.Popen(cmd)
        else:
            LOG.warning("No backup rotation script and/or delimiter was specified; no rotation is being performed.")

    def updateOptionsDialog(self):
        LOG.debug("updating options dialog: datum=" + self.datum)
        self.optionsDialog.datumField.setCurrentIndex(self.optionsDialog.datumField.findText(self.datum))
        self.optionsDialog.formatField.setCurrentIndex(self.optionsDialog.formatField.findText(self.coordFormat))
        self.optionsDialog.timeoutField.setValue(self.timeoutDisplaySecList.index(int(self.timeoutRedSec)))
        self.optionsAccepted()  # at the very least, this sets timeoutOrangeSec

    def setColumnResizedFlag(self):
        self.columnResizedFlag = True

    def resizeRowsToContentsIfNeeded(self):
        if self.columnResizedFlag and not self.loadFlag:
            self.columnResizedFlag = False
            self.tableView.resizeRowsToContents()
            self.tableView.scrollToBottom()
            for n in self.tableViewList[1:]:
                n.resizeRowsToContents()

    def fsMuteBlink(self, state):
        if state == "on":
            self.incidentNameLabel.setText("FleetSync Muted")
            self.incidentNameLabel.setStyleSheet(BG_BROWN + ";color:white;font-size:" + str(self.limitedFontSize) + "pt;")
            self.fsCheckBox.setStyleSheet("border:3px outset red")
        else:
            if state == "noSend":
                self.incidentNameLabel.setText("FS Locators Muted")
                self.incidentNameLabel.setStyleSheet(BG_BROWN + ";color:white;font-size:" + str(self.limitedFontSize) + "pt;")
                self.fsCheckBox.setStyleSheet("border:3px outset red")
            else:
                self.incidentNameLabel.setText(self.incidentName)
                self.incidentNameLabel.setStyleSheet(BG_NONE + ";color:black;font-size:" + str(self.limitedFontSize) + "pt;")
                self.fsCheckBox.setStyleSheet("border:3px inset lightgray")

    def fsFilterBlink(self, state):
        if state == "on":
            self.fsFilterButton.setStyleSheet("QToolButton { " + BG_BROWN + ";border:2px outset lightgray; }")
        else:
            self.fsFilterButton.setStyleSheet("QToolButton { }")

    def fsFilterEdit(self, fleet, dev, state=True):
        # 		LOG.debug("editing filter for "+str(fleet)+" "+str(dev))
        for row in self.fsLog:
            # 			LOG.debug("row:"+str(row))
            if row[0] == fleet and row[1] == dev:
                # 				LOG.debug("found")
                row[3] = state
                self.fsBuildTooltip()
                self.fsFilterDialog.tableView.model().layoutChanged.emit()
                return

    def fsAnythingFiltered(self):
        for row in self.fsLog:
            if row[3] is True:
                return True
        return False

    def fsGetTeamFilterStatus(self, extTeamName):
        # 0 - no devices belonging to this callsign are filtered
        # 1 - some but not all devices belonging to this callsign are filtered
        # 2 - all devices belonging to this callsign are filtered
        total = 0
        filtered = 0
        for row in self.fsLog:
            if getExtTeamName(row[2]) == extTeamName:
                total += 1
                if row[3] is True:
                    filtered += 1
        if filtered == 0:
            return 0
        if filtered < total:
            return 1
        if filtered == total:
            return 2

    def fsGetTeamDevices(self, extTeamName):
        # return a list of two-element lists [fleet,dev]
        rval = []
        for row in self.fsLog:
            if getExtTeamName(row[2]) == extTeamName:
                rval.append([row[0], row[1]])
        return rval

    def fsFilteredCallDisplay(self, state="off", fleet=0, dev=0, callsign=""):
        if state == "on":
            self.incidentNameLabel.setText("Incoming FS call filtered/ignored:\n" + callsign + "   (" + str(fleet) + ":" + str(dev) + ")")
            self.incidentNameLabel.setStyleSheet(BG_BROWN + ";color:white;font-size:" + str(self.limitedFontSize / 2) + "pt")
        else:
            self.incidentNameLabel.setText(self.incidentName)
            self.incidentNameLabel.setStyleSheet(BG_NONE + ";color:black;font-size:" + str(self.limitedFontSize) + "pt")

    def fsCheckBoxCB(self):
        # 0 = unchecked / empty: mute fleetsync completely
        # 1 = partial check / square: listen for CID and location, but do not send locator requests
        # 2 = checked (normal behavior): listen for CID and location, and send locator requests
        self.fsMuted = self.fsCheckBox.checkState() == 0
        self.noSend = self.fsCheckBox.checkState() < 2
        # blinking is handled in fsCheck which is called once a second anyway;
        # make sure to set display back to normal if mute was just turned off
        #  since we don't know the previous blink state
        if self.fsMuted:
            LOG.info("FleetSync is now muted")
            self.fsMuteBlink("on")  # blink on immediately so user sees immediate response
        else:
            if self.noSend:
                LOG.info("Fleetsync is unmuted but locator requests will not be sent")
                self.fsMuteBlink("noSend")
            else:
                LOG.info("Fleetsync is unmuted and locator requests will be sent")
                self.fsMuteBlink("off")
                self.incidentNameLabel.setText(self.incidentName)
                self.incidentNameLabel.setStyleSheet(BG_NONE + ";color:black;font-size:" + str(self.limitedFontSize) + "pt;")

    # FleetSync - check for pending data
    # - check for pending data at regular interval (from timer)
    #     (it's important to check for ID-only lines, since handhelds with no
    #      GPS mic will not send $PKLSH but we still want to spawn a new entry
    #      dialog; and, $PKLSH isn't necessarily sent on BOT (Beginning of Transmission) anyway)
    #     (for 1 second interval, ID-only is always processed separately from $PKLSH;
    #     even for 2 second interval, sometimes ID is processed separately.
    #     So, if PKLSH is processed, add coords to any rececntly-spawned
    #     'from' new entry dialog for the same fleetsync id.)
    # - append any pending data to fsBuffer
    # - if a clean end of fleetsync transmission is included in this round of data,
    #    spawn a new entry window (unless one is already open with 'from'
    #    and the same fleetsync fleet and ID) with any geographic data
    #    from the current fsBuffer, then empty the fsBuffer

    # NOTE that the data coming in is bytes b'1234' but we want string; use bytes.decode('utf-8') to convert,
    #  after which /x02 will show up as a happy face and /x03 will show up as a heart on standard ASCII display.

    def fsCheck(self):
        if not (self.firstComPortFound and self.secondComPortFound):  # correct com ports not yet found; scan for waiting fleetsync data
            if not self.comPortScanInProgress:  # but not if this scan is already in progress (taking longer than 1 second)
                if comLog:
                    LOG.info("Two COM ports not yet found.  Scanning...")
                self.comPortScanInProgress = True
                # opening a port quickly, checking for waiting input, and closing on each iteration does not work; the
                #  com port must be open when the input begins, in order to catch it in the inWaiting internal buffer.
                # 1. go through each already-open com port to check for waiting data; if valid Fleetsync data is
                #     found, then we have the correct com port, abort the rest of the scan
                # 2. (only if no valid data was found in step 1) list com ports; open any new finds and close any
                #     stale ports (i.e. existed in the list in previous iterations but not in the list now)
                for comPortTry in self.comPortTryList:
                    if comLog:
                        LOG.debug("  Checking buffer for already-open port " + comPortTry.name)
                    try:
                        isWaiting = comPortTry.inWaiting()
                    except serial.serialutil.SerialException as err:
                        if "ClearCommError failed" in str(err):
                            LOG.debug("  COM port unplugged.  Scan continues...")
                            self.comPortTryList.remove(comPortTry)
                    except:
                        pass  # unicode decode errors may occur here for non-radio com devices
                    else:
                        if isWaiting:
                            LOG.debug("     DATA IS WAITING!!!")
                            tmpData = ""
                            try:
                                tmpData = comPortTry.read(comPortTry.inWaiting()).decode("utf-8")
                            except Exception as e:
                                # unicode decode errors may occur here also, apparently for glitch on hot plug
                                LOG.debug("      failure to decode COM port data:" + str(e))
                            if "\x02I" in tmpData:
                                LOG.debug("      VALID FLEETSYNC DATA!!!")
                                self.fsBuffer = self.fsBuffer + tmpData

                                if not self.firstComPortFound:
                                    self.firstComPort = comPortTry  # pass the actual open com port object, to keep it open
                                    self.firstComPortFound = True
                                else:
                                    self.secondComPort = comPortTry  # pass the actual open com port object, to keep it open
                                    self.secondComPortFound = True
                                self.comPortTryList.remove(comPortTry)  # and remove the good com port from the list of ports to try going forward
                            else:
                                LOG.debug("      but not valid fleetsync data.  Scan continues...")
                        else:
                            if comLog:
                                LOG.debug("     no data")
                for portIterable in serial.tools.list_ports.comports():
                    if portIterable[0] not in [x.name for x in self.comPortTryList]:
                        try:
                            self.comPortTryList.append(serial.Serial(portIterable[0]))
                        except:
                            pass
                        else:
                            LOG.debug("  Opened newly found port " + portIterable[0])
                            if self.firstComPortAlive:
                                self.secondComPortAlive = True
                            else:
                                self.firstComPortAlive = True
                self.comPortScanInProgress = False
        ##		else: # com port already found; read data normally
        # read data and process buffer even if both com ports aren't yet found, i.e. if only one is found

        self.firstComPortField.setStyleSheet(BG_GREEN if self.firstComPortAlive else BG_GRAY)
        self.secondComPortField.setStyleSheet(BG_GREEN if self.secondComPortAlive else BG_GRAY)

        # fixed issue 41: handle USB hot-unplug case, in which port scanning resumes;
        #  note that hot-plug takes 5 seconds or so to be recognized
        if self.firstComPortFound:
            # 			self.firstComPortField.setStyleSheet(BG_GREEN)
            waiting = 0
            try:
                waiting = self.firstComPort.inWaiting()
            except serial.serialutil.SerialException as err:
                if "ClearCommError failed" in str(err):
                    LOG.debug("first com port unplugged")
                    self.firstComPortFound = False
                    self.firstComPortAlive = False
                    self.firstComPortField.setStyleSheet(BG_RED)
            if waiting:
                self.firstComPortField.setStyleSheet(BG_DARK_GREEN)
                self.fsBuffer = self.fsBuffer + self.firstComPort.read(waiting).decode("utf-8")
        if self.secondComPortFound:
            # 			self.secondComPortField.setStyleSheet(BG_GREEN)
            waiting = 0
            try:
                waiting = self.secondComPort.inWaiting()
            except serial.serialutil.SerialException as err:
                if "ClearCommError failed" in str(err):
                    LOG.debug("second com port unplugged")
                    self.secondComPortFound = False
                    self.secondComPortAlive = False
                    self.secondComPortField.setStyleSheet(BG_RED)
            if waiting:
                self.secondComPortField.setStyleSheet(BG_DARK_GREEN)
                self.fsBuffer = self.fsBuffer + self.secondComPort.read(waiting).decode("utf-8")

        # don't process fsMuted before this point: we need to read the com ports
        #  even if they are muted, so that the com port buffers don't fill up
        #  while muted, which would result in buffer overrun or just all the
        #  queued up fs traffic being processed when fs is unmuted
        if self.fsMuted or self.noSend:
            if self.fsMuted:
                self.fsBuffer = ""  # make sure the buffer is clear, i.e. any incoming
                # fs traffic while muted should be read but disregarded
            if self.fsMuted or self.noSend:
                self.fsMutedBlink = not self.fsMutedBlink
            if self.fsMutedBlink:
                if self.fsMuted:
                    self.fsMuteBlink("on")
                else:
                    if self.noSend:
                        self.fsMuteBlink("noSend")
            else:
                self.fsMuteBlink("off")

        if self.fsAnythingFiltered():
            self.fsFilterBlinkState = not self.fsFilterBlinkState
            if self.fsFilterBlinkState:
                self.fsFilterBlink("on")
            else:
                self.fsFilterBlink("off")
        else:
            self.fsFilterBlink("off")

        if self.fsBuffer.endswith("\x03"):
            self.fsParse()
            self.fsBuffer = ""

    def fsParse(self):
        LOG.debug("PARSING")
        LOG.debug(self.fsBuffer)
        origLocString = ""
        formattedLocString = ""
        callsign = ""
        self.getString = ""
        sec = time.time()
        # the line delimeters are literal backslash then n, rather than standard \n
        for line in self.fsBuffer.split("\n"):
            LOG.debug(" line:" + line)
            if "$PKLSH" in line:
                lineParse = line.split(",")
                if len(lineParse) == 10:
                    [pklsh, nval, nstr, wval, wstr, utc, valid, fleet, dev, chksum] = lineParse
                    callsign = self.getCallsign(fleet, dev)
                    LOG.debug("$PKLSH detected containing CID: fleet=" + fleet + "  dev=" + dev + "  -->  callsign=" + callsign)
                    # unusual PKLSH lines seen from log files:
                    # $PKLSH,2913.1141,N,,,175302,A,100,2016,*7A - no data for west - this caused
                    #   parsing error "ValueError: invalid literal for int() with base 10: ''"
                    # $PKLSH,3851.3330,N,09447.9417,W,012212,V,100,1202,*23 - what's 'V'?
                    #   in standard NMEA sentences, status 'V' = 'warning'.  Dead GPS mic?
                    #   we should flag these to the user somehow; note, the coordinates are
                    #   for the Garmin factory in Olathe, KS
                    # so:
                    # - if valid=='V' set coord field to 'WARNING', do not attempt to parse, and carry on
                    # - if valid=='A' and coords are incomplete or otherwise invalid, set coord field
                    #    to 'INVALID', do not attempt to parse, and carry on
                    if valid == "A":  # only process if there is a GPS lock
                        # 				if valid!='Z':  # process regardless of GPS lock
                        locList = [nval, nstr, wval, wstr]
                        origLocString = "|".join(locList)  # don't use comma, that would conflict with CSV delimeter
                        validated = True
                        try:
                            float(nval)
                        except ValueError:
                            validated = False
                        try:
                            float(wval)
                        except ValueError:
                            validated = False
                        validated = validated and nstr in ["N", "S"] and wstr in ["W", "E"]
                        if validated:
                            LOG.debug("Valid location string:'" + origLocString + "'")
                            formattedLocString = self.convertCoords(locList, self.datum, self.coordFormat)
                            LOG.debug("Formatted location string:'" + formattedLocString + "'")
                            [lat, lon] = self.convertCoords(locList, targetDatum="WGS84", targetFormat="D.dList")
                            LOG.debug("WGS84 lat=" + str(lat) + "  lon=" + str(lon))
                            # sarsoft requires &id=FLEET:<fleet#>-<deviceID>
                            #  fleet# must match the locatorGroup fleet number in sarsoft
                            #  but deviceID can be any text; use the callsign to get useful names in sarsoft
                            if callsign.startswith("KW-"):
                                # did not find a good callsign; use the device number in the GET request
                                devTxt = dev
                            else:
                                # found a good callsign; use the callsign in the GET request
                                devTxt = callsign
                            self.getString = "http://" + self.sarsoftServerName + ":8080/rest/location/update/position?lat=" + str(lat) + "&lng=" + str(lon) + "&id=FLEET:" + fleet + "-"
                            # if callsign = "Radio ..." then leave the getString ending with hyphen for now, as a sign to defer
                            #  sending until accept of change callsign dialog, or closeEvent of NewEntryWidget, whichever comes first;
                            #  otherwise, append the callsign now, as a sign to send immediately
                            if not devTxt.startswith("Radio "):
                                self.getString = self.getString + devTxt
                        else:
                            LOG.error("INVALID location string parsed from $PKLSH: '" + origLocString + "'")
                            origLocString = "INVALID"
                            formattedLocString = "INVALID"
                    elif valid == "Z":
                        origLocString = "NO FIX"
                        formattedLocString = "NO FIX"
                    elif valid == "V":
                        LOG.warning("WARNING status character parsed from $PKLSH; check the GPS mic attached to that radio")
                        origLocString = "WARNING"
                        formattedLocString = "WARNING"
                    else:
                        origLocString = "UNDEFINED"
                        formattedLocString = "UNDEFINED"
                else:
                    LOG.error("Parsed line contained " + str(len(lineParse)) + " tokens instead of the expected 10; skipping.")
                    origLocString = "BAD DATA"
                    formattedLocString = "BAD DATA"
            elif "\x02I" in line:
                # caller ID lines look like " I110040021004002" (first character is \x02, may show as a space)
                # " I<n>" is a prefix, n is either 0 or 1 (not sure why)
                # the next three characters (100 above) are the fleet#
                # the next four characters (4002 above) are the device#
                # fleet and device# are repeated
                # apparently a delay elsewhere can result in an extra leading character here;
                #  so, find the exact characters rather than assuming character index
                i = line.index("\x02I")
                fleet = line[i + 3 : i + 6]
                dev = line[i + 6 : i + 10]
                callsign = self.getCallsign(fleet, dev)
                LOG.debug("CID detected (not in $PKLSH): fleet=" + fleet + "  dev=" + dev + "  callsign=" + callsign)
        # if any new entry dialogs are already open with 'from' and the
        #  current callsign, and that entry has been edited within the 'continue' time,
        #  update it with the current location if available;
        # otherwise, spawn a new entry dialog
        found = False
        for widget in NewEntryWidget.instances:
            ##			LOG.debug("checking against existing widget: to_from="+widget.to_fromField.currentText()" team="+widget.teamField.text()
            if widget.to_fromField.currentText() == "FROM" and widget.teamField.text() == callsign and widget.lastModAge < continueSec:
                ##				widget.timer.start(newEntryDialogTimeoutSeconds*1000) # reset the timeout
                found = True
                LOG.debug("  new entry widget is already open from this callsign within the 'continue time'; not opening a new one")
                prevLocString = widget.radioLocField.toPlainText()
                # if previous location string was blank, always overwrite;
                #  if previous location string was not blank, only overwrite if new location is valid
                if prevLocString == "" or (formattedLocString != "" and formattedLocString != "NO FIX"):
                    datumFormatString = "(" + self.datum + "  " + self.coordFormat + ")"
                    if widget.relayed:
                        LOG.debug("location strings not updated because the message is relayed")
                        widget.radioLocTemp = formattedLocString
                        widget.datumFormatTemp = datumFormatString
                    else:
                        LOG.debug("location strings updated because the message is not relayed")
                        widget.radioLocField.setText(formattedLocString)
                        widget.datumFormatLabel.setText(datumFormatString)
                        widget.formattedLocString = formattedLocString
                        widget.origLocString = origLocString
        self.fsLogUpdate(int(fleet), int(dev))
        # only open a new entry widget if the fleet/dev is not being filtered
        if not found:
            if self.fsIsFiltered(int(fleet), int(dev)):
                self.fsFilteredCallDisplay("on", fleet, dev, callsign)
                QTimer.singleShot(5000, self.fsFilteredCallDisplay)  # no arguments will clear the display
            else:
                self.openNewEntry("fs", callsign, formattedLocString, fleet, dev, origLocString)
        self.sendPendingGet()

    def sendPendingGet(self, suffix=""):
        # NOTE that requests.get can cause a blocking delay; so, do it AFTER spawning the newEntryDialog
        # if sarsoft is not running to handle this get request, Windows will complain with nested exceptions:
        # ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it
        # During handling of the above exception, another exception occurred:
        # requests.packages.urllib3.exceptions.ProtocolError: ('Connection aborted.', ConnectionRefusedError(10061, 'No connection could be made because the target machine actively refused it', None, 10061, None))
        # but we don't care about these; pass them silently

        # also, if it ends in hyphen, defer sending until accept of change callsign dialog, or closeEvent of newEntryDialog
        #  (see getString construction comments above)
        if not self.noSend:
            if self.getString != "":  # to avoid sending a GET string that is nothing but the callsign
                self.getString = self.getString + suffix
            if self.getString != "" and not self.getString.endswith("-"):
                LOG.debug("calling processEvents before sending GET request...")
                QCoreApplication.processEvents()
                try:
                    LOG.debug("Sending GET request:")
                    LOG.debug(self.getString)
                    # fire-and-forget: completely ignore the response, but, return immediately
                    r = requests.get(self.getString, timeout=0.0001)
                    LOG.debug("  request sent")
                    LOG.debug("  response: " + str(r))
                except Exception as e:
                    LOG.error("  exception during sending of GET request: " + str(e))
                self.getString = ""

    # for fsLog, a dictionary would probably be easier, but we have to use an array
    #  since we will be displaying in a QTableView
    # if callsign is specified, update the callsign but not the time;
    #  if callsign is not specified, udpate the time but not the callsign;
    #  if the entry does not yet exist, add it
    def fsLogUpdate(self, fleet, dev, callsign=False):
        # row structure: [fleet,dev,callsign,filtered,last_received]
        LOG.debug("fsLogUpdate called: fleet=" + str(fleet) + " dev=" + str(dev) + " callsign=" + (callsign or "<None>"))
        found = False
        t = time.strftime("%a %H:%M:%S")
        for row in self.fsLog:
            if row[0] == fleet and row[1] == dev:
                found = True
                if callsign:
                    row[2] = callsign
                else:
                    row[4] = t
        if not found:
            # always update callsign - it may have changed since creation
            self.fsLog.append([fleet, dev, self.getCallsign(fleet, dev), False, t])
        # 		LOG.debug(self.fsLog)
        # 		if self.fsFilterDialog.tableView:
        self.fsFilterDialog.tableView.model().layoutChanged.emit()
        self.fsBuildTeamFilterDict()

    def fsBuildTeamFilterDict(self):
        for extTeamName in teamFSFilterDict:
            teamFSFilterDict[extTeamName] = self.fsGetTeamFilterStatus(extTeamName)

    def fsBuildTooltip(self):
        filteredHtml = ""
        for row in self.fsLog:
            if row[3] is True:
                filteredHtml += "<tr><td>" + row[2] + "</td><td>" + str(row[0]) + "</td><td>" + str(row[1]) + "</td></tr>"
        if filteredHtml != "":
            tt = "Filtered devices:<br>(left-click to edit)<table border='1' cellpadding='3'><tr><td>Callsign</td><td>Fleet</td><td>ID</td></tr>" + filteredHtml + "</table>"
        else:
            tt = "No devices are currently being filtered.<br>(left-click to edit)"
        self.fsFilterButton.setToolTip(tt)

    def fsIsFiltered(self, fleet, dev):
        # 		LOG.debug("checking fsFilter: fleet="+str(fleet)+" dev="+str(dev))
        # disable fsValidFleetList checking to allow arbitrary fleets; this
        #  idea is probably obsolete
        # invalid fleets are always filtered, to prevent fleet-glitches (110-xxxx) from opening new entries
        # 		if int(fleet) not in self.fsValidFleetList:
        # 			LOG.debug("true1")
        # 			return True
        # if the fleet is valid, check for filtered device ID
        for row in self.fsLog:
            if row[0] == fleet and row[1] == dev and row[3] is True:
                # 				LOG.debug("  device is fitlered; returning True")
                return True
        # 		LOG.debug("not filtered; returning False")
        return False

    def fsLoadLookup(self, startupFlag=False, fsFileName=None, hideWarnings=False):
        LOG.trace("fsLoadLookup called: startupFlag=" + str(startupFlag) + "  fsFileName=" + str(fsFileName) + "  hideWarnings=" + str(hideWarnings))
        if not startupFlag and not fsFileName:  # don't ask for confirmation on startup or on restore
            if not ask_user_to_confirm("Are you sure you want to reload the default FleetSync lookup table?  This will overwrite any callsign changes you have made.", icon=ICON_WARN, parent=self):
                return
        fsEmptyFlag = False
        if len(self.fsLookup) == 0:
            fsEmptyFlag = True
        if not fsFileName:
            fsFileName = self.fsFileName
        try:
            LOG.trace("trying " + fsFileName)
            with open(fsFileName, "r") as fsFile:
                LOG.info("Loading FleetSync Lookup Table from file " + fsFileName)
                self.fsLookup = []
                csvReader = csv.reader(fsFile)
                for row in csvReader:
                    if not row[0].startswith("#"):
                        self.fsLookup.append(row)
                if not startupFlag:  # suppress message box on startup
                    inform_user_about_issue(f"FleetSync ID table has been re-loaded from file {fsFileName}.", icon=ICON_INFO, title="Information", parent=self, timeout=2000)
        except:
            if fsEmptyFlag:
                msg = (
                    "Cannot read FleetSync ID table file '"
                    + fsFileName
                    + "' and no FleetSync ID table has yet been loaded.  Callsigns for incoming FleetSync calls will be of the format 'KW-<fleet>-<device>'.\n\nThis warning will automatically close in a few seconds."
                )
            else:
                msg = "Cannot read FleetSync ID table file '" + fsFileName + "'!  Using existing settings.\n\nThis warning will automatically close in a few seconds."
            LOG.warning(msg)
            if not hideWarnings:
                inform_user_about_issue(msg, icon=ICON_WARN, parent=self, timeout=8000)

    # save to fsFileName in the working dir each time, but on startup, load from the default dir;
    #  would only need to load from the working dir if restoring
    def fsSaveLookup(self):
        fsName = self.firstWorkingDir + "\\" + self.csvFileName
        fsName = fsName.replace(".csv", "_fleetsync.csv")
        try:
            with open(fsName, "w", newline="") as fsFile:
                LOG.trace("Writing file " + fsName)
                csvWriter = csv.writer(fsFile)
                csvWriter.writerow(["## Radio Log FleetSync lookup table"])
                csvWriter.writerow(["## File written " + time.strftime("%a %b %d %Y %H:%M:%S")])
                csvWriter.writerow(["## Created during Incident Name: " + self.incidentName])
                for row in self.fsLookup:
                    csvWriter.writerow(row)
                csvWriter.writerow(["## end"])
        except:
            inform_user_about_issue("Cannot write FleetSync ID table file " + fsName + "!  Any modified FleetSync Callsign associations will be lost.", icon=ICON_WARN, parent=self)

    def getCallsign(self, fleet, dev):
        entry = [element for element in self.fsLookup if (element[0] == fleet and element[1] == dev)]
        if len(entry) != 1 or len(entry[0]) != 3:  # no match
            return "KW-" + str(fleet) + "-" + str(dev)
        else:
            return entry[0][2]

    def getFleetDev(self, callsign):
        entry = [element for element in self.fsLookup if (element[2] == callsign)]
        if len(entry) != 1:  # no match
            return False
        else:
            return [entry[0][0], entry[0][1]]

    def convertCoords(self, coords, targetDatum, targetFormat):
        easting = "0000000"
        northing = "0000000"
        LOG.debug("convertCoords called: targetDatum=" + targetDatum + " targetFormat=" + targetFormat + " coords=" + str(coords))
        # coords must be a parsed list of location data from fleetsync in NMEA format
        if isinstance(coords, list):
            latDeg = int(coords[0][0:2])  # first two numbers are degrees
            latMin = float(coords[0][2:])  # remainder is minutes
            lonDeg = int(coords[2][0:3])  # first three numbers are degrees
            lonMin = float(coords[2][3:])  # remainder is minutes
            # add decimal portion of degrees here, before changing sign for hemisphere
            latDd = latDeg + latMin / 60
            lonDd = lonDeg + lonMin / 60
            if coords[1] == "S":
                latDeg = -latDeg  # invert if needed
                ladDd = -latDd
            if coords[3] == "W":
                LOG.debug("inverting longitude")
                lonDeg = -lonDeg  # invert if needed
                lonDd = -lonDd
            ##			targetUTMZone=int(lonDeg/6)+30 # do the math: -179.99999deg -> -174deg = zone 1; -173.99999deg -> -168deg = zone 2, etc
            targetUTMZone = math.floor((lonDd + 180) / 6) + 1  # from http://stackoverflow.com/questions/9186496, since -120.0000deg should be zone 11, not 10
            LOG.debug("lonDeg=" + str(lonDeg) + " lonDd=" + str(lonDd) + " targetUTMZone=" + str(targetUTMZone))
        else:
            return "INVALID INPUT FORMAT - MUST BE A LIST"

        # relevant CRSes:
        #  4326 = WGS84 lat/lon
        #  4267 = NAD27 CONUS lat/lon
        #  32600+zone = WGS84 UTM (e.g. 32610 = UTM zone 10)
        #  26700+zone = NAD27 CONUS UTM (e.g. 26710 = UTM zone 10)

        # if target datum is WGS84 and target format is anything other than UTM, just do the math
        if targetDatum != "WGS84" or re.match("UTM", targetFormat):
            sourceCRS = 4326
            if targetDatum == "WGS84":
                targetCRS = 32600 + targetUTMZone
            elif targetDatum == "NAD27 CONUS":
                if re.match("UTM", targetFormat):
                    targetCRS = 26700 + targetUTMZone
                else:
                    targetCRS = 4267
            else:
                targetCRS = sourceCRS  # fallback to do a pass-thru transformation

            # the Transformer object is reusable; only need to recreate it if the CRSes have changed
            # see examples at
            # https://pyproj4.github.io/pyproj/stable/api/transformer.html#pyproj.transformer.Transformer.transform
            if sourceCRS != self.sourceCRS or targetCRS != self.targetCRS:
                self.sourceCRS = sourceCRS
                self.targetCRS = targetCRS
                self.transformer = Transformer.from_crs(sourceCRS, targetCRS)

            # ================ the actual transformation ==================
            t = self.transformer.transform(latDd, lonDd)
            # =============================================================

            if re.match("UTM", targetFormat):
                [easting, northing] = map(int, t)
            else:
                [lonDd, latDd] = t

        latDd = float(latDd)
        latDeg = int(latDd)
        latMin = float((latDd - float(latDeg)) * 60.0)
        latSec = float((latMin - int(latMin)) * 60.0)
        lonDd = float(lonDd)
        if lonDd < 0 and targetFormat != "D.dList":  # leave it negative for D.dList
            lonDd = -lonDd
            lonLetter = "W"
        else:
            lonLetter = "E"
        lon = int(lonDd)
        lonMin = float((abs(lonDd) - float(abs(lonDeg))) * 60.0)
        lonSec = float((abs(lonMin) - int(abs(lonMin))) * 60.0)
        LOG.debug("lonDd=" + str(lonDd))
        LOG.debug("lonDeg=" + str(lonDeg))

        # return the requested format
        # desired accuracy / digits of precision:
        # at 39 degrees north,
        # 0.00001 degree latitude = 1.11 meters
        # 0.001 minute latutude = 1.85 meters
        # 0.1 second latitude = 3.08 meters
        # (longitude lengths are about 78% as much as latitude, at 39 degrees north)
        if targetFormat == "D.dList":
            return [latDd, lonDd]
        if targetFormat == "D.d°":
            return "{:.6f}°N  {:.6f}°{}".format(latDd, lonDd, lonLetter)
        if targetFormat == "D° M.m'":
            return "{}° {:.4f}'N  {}° {:.4f}'{}".format(latDeg, latMin, abs(lonDeg), lonMin, lonLetter)
        if targetFormat == "D° M' S.s\"":
            return "{}° {}' {:.2f}\"N  {}° {}' {:.2f}\"{}".format(latDeg, int(latMin), latSec, abs(lonDeg), int(lonMin), lonSec, lonLetter)
        eStr = "{0:07d}".format(easting)
        nStr = "{0:07d}".format(northing)
        if targetFormat == "UTM 7x7":
            return "{} {}   {} {}".format(eStr[0:2], eStr[2:], nStr[0:2], nStr[2:])
        if targetFormat == "UTM 5x5":
            return "{}  {}".format(eStr[2:], nStr[2:])
        return "INVALID - UNKNOWN OUTPUT FORMAT REQUESTED"

    def startupOptions(self):
        self.optionsDialog.show()
        self.optionsDialog.raise_()
        self.optionsDialog.incidentField.selectAll()
        QTimer.singleShot(250, self.optionsDialog.incidentField.selectAll)
        QTimer.singleShot(500, self.optionsDialog.incidentField.deselect)
        QTimer.singleShot(750, self.optionsDialog.incidentField.selectAll)
        QTimer.singleShot(1000, self.optionsDialog.incidentField.deselect)
        QTimer.singleShot(1250, self.optionsDialog.incidentField.selectAll)
        QTimer.singleShot(1500, self.optionsDialog.incidentField.deselect)
        QTimer.singleShot(1750, self.optionsDialog.incidentField.selectAll)
        QTimer.singleShot(1800, self.optionsDialog.incidentField.setFocus)

    def fontsChanged(self):
        LOG.trace("1 - begin fontsChanged")
        self.limitedFontSize = self.fontSize
        if self.limitedFontSize > self.maxLimitedFontSize:
            self.limitedFontSize = self.maxLimitedFontSize
        if self.limitedFontSize < self.minLimitedFontSize:
            self.limitedFontSize = self.minLimitedFontSize
        # preserve the currently selected tab, since something in this function
        #  causes the rightmost tab to be selected
        i = self.tabWidget.currentIndex()
        self.tableView.setStyleSheet("font-size:" + str(self.fontSize) + "pt")
        for n in self.tableViewList[1:]:
            LOG.debug("n=" + str(n))
            n.setStyleSheet("font-size:" + str(self.fontSize) + "pt")
        # don't change tab font size unless you find a good way to dynamically
        # change tab size and margins as well
        ##		self.tabWidget.tabBar().setStyleSheet("font-size:"+str(self.fontSize)+"pt")
        LOG.trace("2")
        self.redrawTables()
        self.tabWidget.setCurrentIndex(i)
        self.incidentNameLabel.setStyleSheet("font-size:" + str(self.limitedFontSize) + "pt;")

        # NOTE that setStyleSheet is DESTRUCTIVE, not INCREMENTAL.  To set a new style
        #  without affecting previous style settings for the same identifier, you
        #  need to use getStyleSheet()+"....".  To avoid confusion, do as many settings
        #  as possible in one text block as below.

        # hardcode dialog button box pushbutton font size to 14pt since QTDesiger-generated code doesn't work
        self.parent.setStyleSheet(
            """
            QMessageBox,QDialogButtonBox QPushButton {
                font-size:14pt;
            }
            QToolTip {
                font-size:"""
            + str(self.fontSize * 2 / 3)
            + """pt;
                color:#555;
            }
            QMenu {
                font-size:"""
            + str(self.limitedFontSize * 3 / 4)
            + """pt;
            }
        """
        )
        LOG.trace("3 - end of fontsChanged")

    def redrawTables(self):
        # column sizing rules, in sequence:
        # TIME, T/F, STATUS: width is only a function of font size (not of contents)
        # TEAM, RADIO LOC.: resize to fit contents
        # MESSAGE: take all remaining space

        # benchmarks for 670 entries:
        # (removing the setSectionResizeMode for the horizontal header to resizeToContents
        #  does result in a speedup, since it's redundant with the code here)
        # full: autosize cols 2 and 4; hardcode cols 0,1,5; then resize rows: 5.5 sec
        # full minus autosize 2 and 4: 3 sec
        # full minus resize rows: 3.5 sec
        # full minus autosize 2 and 4, minus resize rows: 2 sec
        # full minus autosize 2 and 4, minus hardcode size 0,1,5, minus resize rows: < 0.5 sec

        # horizontalHeader().resizeSection is about the same speed as setColumnWidth
        #  but it's very important to make sure no other actions get called on resize!

        # no need to do layoutChanged.emit and scrollToBottom here; see end of load function
        ##		self.tableView.model().layoutChanged.emit()
        ##		self.tableView.scrollToBottom()
        self.loadFlag = True
        LOG.trace("1: start of redrawTables")
        for i in [2, 4]:  # hardcode results in significant speedup
            self.tableView.resizeColumnToContents(i)  # zero is the first column
        LOG.trace("2")
        self.tableView.setColumnWidth(0, self.fontSize * 5)  # wide enough for '2345'
        self.tableView.setColumnWidth(1, self.fontSize * 6)  # wide enough for 'FROM'
        self.tableView.setColumnWidth(5, self.fontSize * 10)  # wide enough for 'STATUS'
        LOG.trace("3")
        ##		self.tableView.resizeRowsToContents()
        LOG.trace("4")
        for n in self.tableViewList[1:]:
            LOG.debug(" n=" + str(n))
            for i in [2, 4]:  # hardcode results in significant speedup, but lag still scales with filtered table length
                print("    i=" + str(i))
                n.resizeColumnToContents(i)
            LOG.debug("    done with i")
            n.setColumnWidth(0, self.fontSize * 5)
            n.setColumnWidth(1, self.fontSize * 6)
            n.setColumnWidth(5, self.fontSize * 10)
            LOG.debug("    resizing rows to contents")
        ##			n.resizeRowsToContents()
        LOG.trace("5")
        self.tableView.scrollToBottom()
        LOG.trace("6")
        for i in range(1, self.tabWidget.count()):
            self.tabWidget.setCurrentIndex(i)
            self.tableViewList[i].scrollToBottom()
        LOG.trace("7: end of redrawTables")
        ##		self.resizeRowsToContentsIfNeeded()
        self.loadFlag = False

    def updateClock(self):
        self.clock.display(time.strftime("%H:%M"))

    def updateTeamTimers(self):
        # keep track of seconds since contact, rather than seconds remaining til timeout,
        #  since timeout setting may change but each team's counter should still count
        # 1. increment each number in teamTimersDict
        # 2. if any of them are more than the timeout setting, they have timed out: start flashing
        # 3. use this same timer to toggle the blink state of each style

        self.blinkToggle = 1 if self.blinkToggle == 0 else 0
        self.helpWindow.update_blinking(self.blinkToggle, statusStyleDict)

        for extTeamName in teamTimersDict:
            # if there is a NewEntryWidget currently open for this team, don't blink,
            #  but don't reset the timer.  Only reset the timer when the dialog is accepted.
            hold = False
            for widget in NewEntryWidget.instances:
                if widget.to_fromField.currentText() == "FROM" and getExtTeamName(widget.teamField.text()) == extTeamName:
                    hold = True
            i = self.extTeamNameList.index(extTeamName)
            status = teamStatusDict.get(extTeamName, "")
            fsFilter = teamFSFilterDict.get(extTeamName, 0)
            ##			LOG.debug("blinking "+extTeamName+": status="+status)
            # 			LOG.debug("fsFilter "+extTeamName+": "+str(fsFilter))
            secondsSinceContact = teamTimersDict.get(extTeamName, 0)
            if status in ["Waiting for Transport", "STANDBY", "Available"] or (secondsSinceContact >= self.timeoutOrangeSec):
                if self.blinkToggle == 0:
                    # blink 0: style is one of these:
                    # - style as normal per status
                    self.tabWidget.tabBar().tabButton(i, QTabBar.LeftSide).setStyleSheet(statusStyleDict[status])
                else:
                    # blink 1: style is one of these:
                    # - timeout orange
                    # - timeout red
                    # - no change (if status is anything but 'Waiting for transport' or 'STANDBY')
                    # - blank (black on white) (if status is 'Waiting for transport' or 'STANDBY', and not timed out)
                    if not hold and status not in ["At IC", "Off Duty"] and secondsSinceContact >= self.timeoutRedSec:
                        self.tabWidget.tabBar().tabButton(i, QTabBar.LeftSide).setStyleSheet(statusStyleDict["TIMED_OUT_RED"])
                    elif not hold and status not in ["At IC", "Off Duty"] and (secondsSinceContact >= self.timeoutOrangeSec and secondsSinceContact < self.timeoutRedSec):
                        self.tabWidget.tabBar().tabButton(i, QTabBar.LeftSide).setStyleSheet(statusStyleDict["TIMED_OUT_ORANGE"])
                    elif status == "Waiting for Transport" or status == "STANDBY" or status == "Available":
                        self.tabWidget.tabBar().tabButton(i, QTabBar.LeftSide).setStyleSheet(statusStyleDict[""])
            else:
                # not Waiting for Transport or Available, and not in orange/red time zone: draw the normal style
                self.tabWidget.tabBar().tabButton(i, QTabBar.LeftSide).setStyleSheet(statusStyleDict[status])

            # always check for fleetsync filtering, independent from team status
            if self.blinkToggle == 0:
                if fsFilter > 0:
                    f = self.tabWidget.tabBar().tabButton(i, QTabBar.LeftSide).font()
                    f.setStrikeOut(True)
                    self.tabWidget.tabBar().tabButton(i, QTabBar.LeftSide).setFont(f)
            if self.blinkToggle == 1:
                if fsFilter < 2:  # strikeout all the time if all devices for this callsign are filtered
                    f = self.tabWidget.tabBar().tabButton(i, QTabBar.LeftSide).font()
                    f.setStrikeOut(False)
                    self.tabWidget.tabBar().tabButton(i, QTabBar.LeftSide).setFont(f)
                else:
                    f = self.tabWidget.tabBar().tabButton(i, QTabBar.LeftSide).font()
                    f.setStrikeOut(True)
                    self.tabWidget.tabBar().tabButton(i, QTabBar.LeftSide).setFont(f)

            # once they have timed out, keep incrementing; but if the timer is '-1', they will never timeout
            if secondsSinceContact > -1:
                teamTimersDict[extTeamName] = secondsSinceContact + 1

    def keyPressEvent(self, event):
        if type(event) == QKeyEvent:
            # fix #336 (freeze / loss of focus when MyWindow grabs the keyPressEvent
            #  that was intended for NewEntryWidget but happened before NewEntryWidget
            #  was able to respond to it)
            # use the following fix for now: if the newEntryWindow is visible,
            #  ignore the envent completely; it would be nice to queue it until the
            #  NewEntryWidget can respond to it; but, what should the receiver of the
            #  queued event be, and, how should the timing of the queued event interact
            #  with other events and processes?
            #  See https://stackoverflow.com/questions/44148992; need to develop a full
            #  test case to proceed with that question
            if self.newEntryWindow.isVisible():
                LOG.warning("** keyPressEvent ambiguous timing; key press ignored: key=" + str(hex(event.key())))
                event.ignore()
            else:
                key = event.text().lower()  # hotkeys are case insensitive
                mod = event.modifiers()
                LOG.debug("  key:" + QKeySequence(event.key()).toString() + "  mod:" + str(mod))
                if self.teamHotkeysWidget.isVisible():
                    # these key handlers apply only if hotkeys are enabled:
                    teamForKey = self.team_hot_keys.getTeam(key)
                    if teamForKey:
                        self.openNewEntry(teamForKey)
                event.accept()
        else:
            event.ignore()

    def closeEvent(self, event):
        self.exitClicked = True

        # if radioLogNeedsPrint or clueLogNeedsPrint is True, bring up the print dialog
        if self.radioLogNeedsPrint or self.clueLogNeedsPrint:
            LOG.debug("needs print!")
            self.printDialog.exec_()
        else:
            LOG.debug("no print needed")
        # note, this type of messagebox is needed to show above all other dialogs for this application,
        #  even the ones that have WindowStaysOnTopHint.  This works in Vista 32 home basic.
        #  if it didn't show up on top, then, there would be no way to close the radiolog other than kill.
        if not ask_user_to_confirm("Exit the Radio Log program?", icon=ICON_WARN, parent=self):
            event.ignore()
            self.exitClicked = False
            return

        self.save(finalize=True)
        self.fsSaveLookup()
        self.saveRcFile(cleanShutdownFlag=True)

        self.teamTimer.stop()
        if self.firstComPortFound:
            self.firstComPort.close()
        if self.secondComPortFound:
            self.secondComPort.close()
        ##		self.optionsDialog.close()
        ##		self.helpWindow.close()
        ##		self.newEntryWindow.close()
        event.accept()

        qt_app.quit()  # needed to make sure all windows area closed

    def saveRcFile(self, cleanShutdownFlag=False):
        (x, y, w, h) = self.geometry().getRect()
        (cx, cy, cw, ch) = self.clueLogDialog.geometry().getRect()
        timeout = TIMEOUT_DISPLAY_LIST[self.optionsDialog.timeoutField.value()][0]
        rcFile = QFile(self.rcFileName)
        if not rcFile.open(QFile.WriteOnly | QFile.Text):
            inform_user_about_issue("Cannot write resource file " + self.rcFileName + "; proceeding, but, current settings will be lost. " + rcFile.errorString(), icon=ICON_WARN, parent=self)
            return
        out = QTextStream(rcFile)
        out << "[RadioLog]\n"
        # datum, coord format, and timeout are saved in the config file
        #  but also need to be able to auto-recover from .rc file
        # issue 322: use self.lastSavedFileName instead of self.csvFileName to
        #  make sure the initial rc file doesn't point to a file that does not yet exist
        out << "lastFileName=" << self.lastSavedFileName << "\n"
        out << "font-size=" << self.fontSize << "pt\n"
        out << "x=" << x << "\n"
        out << "y=" << y << "\n"
        out << "w=" << w << "\n"
        out << "h=" << h << "\n"
        out << "clueLog_x=" << cx << "\n"
        out << "clueLog_y=" << cy << "\n"
        out << "clueLog_w=" << cw << "\n"
        out << "clueLog_h=" << ch << "\n"
        out << "timeout=" << timeout << "\n"
        out << "datum=" << self.datum << "\n"
        out << "coordFormat=" << self.coordFormat << "\n"
        if cleanShutdownFlag:
            out << "cleanShutdown=True\n"
        rcFile.close()

    def loadRcFile(self):
        # this function gets called at startup (whether it's a clean fresh start
        #  or an auto-recover) but timeout, datum, and coordFormat should only
        #  be used if this is an auto-recover; otherwise those values should
        #  be taken from the config file.
        rcFile = QFile(self.rcFileName)
        if not rcFile.open(QFile.ReadOnly | QFile.Text):
            inform_user_about_issue("Cannot read resource file " + self.rcFileName + "; using default settings. " + rcFile.errorString(), icon=ICON_WARN, parent=self)
            return
        inStr = QTextStream(rcFile)
        line = inStr.readLine()
        if line != "[RadioLog]":
            inform_user_about_issue("Specified resource file " + self.rcFileName + " is not a valid resource file; using default settings.", icon=ICON_WARN, parent=self)
            rcFile.close()
            return
        cleanShutdownFlag = False
        self.lastFileName = "NONE"
        timeoutDisplay = "30 min"
        datum = None
        coordFormat = None
        while not inStr.atEnd():
            line = inStr.readLine()
            tokens = line.split("=")
            if tokens[0] == "x":
                self.x = int(tokens[1])
            elif tokens[0] == "y":
                self.y = int(tokens[1])
            elif tokens[0] == "w":
                self.w = int(tokens[1])
            elif tokens[0] == "h":
                self.h = int(tokens[1])
            elif tokens[0] == "font-size":
                self.fontSize = int(tokens[1].replace("pt", ""))
            elif tokens[0] == "clueLog_x":
                self.clueLog_x = int(tokens[1])
            elif tokens[0] == "clueLog_y":
                self.clueLog_y = int(tokens[1])
            elif tokens[0] == "clueLog_w":
                self.clueLog_w = int(tokens[1])
            elif tokens[0] == "clueLog_h":
                self.clueLog_h = int(tokens[1])
            elif tokens[0] == "lastFileName":
                self.lastFileName = tokens[1]
            elif tokens[0] == "timeout":
                timeoutDisplay = tokens[1]
            elif tokens[0] == "datum":
                datum = tokens[1]
            elif tokens[0] == "coordFormat":
                coordFormat = tokens[1]
            elif tokens[0] == "cleanShutdown" and tokens[1] == "True":
                cleanShutdownFlag = True
        # only apply datum, coordFormat, and timout if it's an auto-recover
        if not cleanShutdownFlag:
            if datum:
                self.datum = datum
            if coordFormat:
                self.coordFormat = coordFormat
            for n in range(len(TIMEOUT_DISPLAY_LIST)):
                pair = TIMEOUT_DISPLAY_LIST[n]
                if pair[0] == timeoutDisplay:
                    self.timeoutRedSec = pair[1]
                    break
        self.updateOptionsDialog()
        rcFile.close()
        return cleanShutdownFlag

    def save(self, finalize=False):
        csvFileNameList = [CONFIG.firstWorkingDir / self.csvFileName]
        if (path2wd := viable_2wd()) :
            csvFileNameList.append(path2wd / self.csvFileName)
        for fileName in csvFileNameList:
            LOG.trace(f"Writing {fileName}")
            with fileName.open("w", newline="") as csvFile:
                csvWriter = csv.writer(csvFile)
                csvWriter.writerow(["## Radio Log data file"])
                csvWriter.writerow(["## File written " + time.strftime("%a %b %d %Y %H:%M:%S")])
                csvWriter.writerow(["## Incident Name: " + self.incidentName])
                csvWriter.writerow(["## Datum: " + self.datum + "  Coordinate format: " + self.coordFormat])
                for row in self.radioLog:
                    row += [""] * (10 - len(row))  # pad the row up to 10 elements if needed, to avoid index errors elsewhere
                    if row[6] < 1e10:  # don't save the blank line
                        # replacing commas is not necessary: csvwriter puts strings in quotes,
                        #  and csvreader knows to not treat commas as delimeters if inside quotes
                        csvWriter.writerow(row)
                if finalize:
                    csvWriter.writerow(["## end"])
                if self.lastSavedFileName != self.csvFileName:  # this is the first save since startup, since restore, or since incident name change
                    self.lastSavedFileName = self.csvFileName
                    self.saveRcFile()
            LOG.trace(f"Done writing {fileName}")
        # now write the clue log to a separate csv file: same filename appended by '.clueLog'
        if len(self.clueLog) > 0:
            for fileName in csvFileNameList:
                fileName = str(fileName).replace(".csv", "_clueLog.csv")
                LOG.trace(f"Writing {fileName}")
                with open(fileName, "w", newline="") as csvFile:
                    csvWriter = csv.writer(csvFile)
                    csvWriter.writerow(["## Clue Log data file"])
                    csvWriter.writerow(["## File written " + time.strftime("%a %b %d %Y %H:%M:%S")])
                    csvWriter.writerow(["## Incident Name: " + self.incidentName])
                    csvWriter.writerow(["## Datum: " + self.datum + "  Coordinate format: " + self.coordFormat])
                    for row in self.clueLog:
                        csvWriter.writerow(row)
                    if finalize:
                        csvWriter.writerow(["## end"])
                LOG.trace(f"Done writing {fileName}")

    def load(self, fileName=None):
        # loading scheme:
        # always merge instead of overwrite; always use the loaded Begins line since it will be earlier by definition
        # maybe provide some way to force overwrite later, but, for now that can be done just by exiting and restarting
        if not fileName:
            fileDialog = QFileDialog()
            fileDialog.setOption(QFileDialog.DontUseNativeDialog)
            fileDialog.setProxyModel(CSVFileSortFilterProxyModel(self))
            fileDialog.setNameFilter("CSV Radio Log Data Files (*.csv)")
            fileDialog.setDirectory(self.firstWorkingDir)
            if fileDialog.exec_():
                fileName = fileDialog.selectedFiles()[0]
            else:  # user pressed cancel on the file browser dialog
                return
        # 			print("fileName="+fileName)
        # 			if not os.path.isfile(fileName): # prevent error if dialog is canceled
        # 				return
        if "_clueLog" in fileName or "_fleetsync" in fileName:
            inform_user_about_issue("Do not load a Clue Log or FleetSync file directly.  Load the parent radiolog.csv file directly, and the Clue Log and FleetSync files will automatically be loaded with it.", title="Invalid File Selected", parent=self)
            return
        progressBox = QProgressDialog("Loading, please wait...", "Abort", 0, 100)
        progressBox.setWindowModality(Qt.WindowModal)
        progressBox.setWindowTitle("Loading")
        progressBox.show()
        QCoreApplication.processEvents()
        self.teamTimer.start(10000)  # pause

        LOG.debug("Loading:" + fileName)
        # pass 1: count total entries for the progress box, and read incident name
        with open(fileName, "r") as csvFile:
            csvReader = csv.reader(csvFile)
            totalEntries = 0
            for row in csvReader:
                if row[0].startswith("## Incident Name:"):
                    self.incidentName = row[0][18:]
                    self.optionsDialog.incidentField.setText(self.incidentName)
                    LOG.debug("loaded incident name: '" + self.incidentName + "'")
                    self.incidentNameNormalized = normalizeName(self.incidentName)
                    LOG.debug("normalized loaded incident name: '" + self.incidentNameNormalized + "'")
                    self.incidentNameLabel.setText(self.incidentName)
                if not row[0].startswith("#"):  # prune comment lines
                    totalEntries = totalEntries + 1
            progressBox.setMaximum(totalEntries * 2)

        # pass 2: read and process the file
        with open(fileName, "r") as csvFile:
            csvReader = csv.reader(csvFile)
            loadedRadioLog = []
            i = 0
            for row in csvReader:
                if not row[0].startswith("#"):  # prune comment lines
                    row[6] = float(row[6])  # convert epoch seconds back to float, for sorting
                    row += [""] * (10 - len(row))  # pad the row up to 10 elements if needed, to avoid index errors elsewhere
                    loadedRadioLog.append(row)
                    i = i + 1
                    if row[3].startswith("Operational Period") and row[3].split()[3] == "Begins:":
                        self.opPeriod = int(row[3].split()[2])
                        self.printDialog.opPeriodComboBox.addItem(str(self.opPeriod))
                    progressBox.setValue(i)
            csvFile.close()

        # now add entries, sort, and prune any Begins lines after the first line
        # edit: don't prune Begins lines - those are needed to indicate start of operational periods
        # move loadFlag True then False closer in to the newEntry commands, to
        #  minimize opportunity for failed entries due to self.loadFlag being
        #  left at True, probably due to early return above (see #340)
        self.loadFlag = True
        for row in loadedRadioLog:
            self.newEntry(row)
            i = i + 1
            progressBox.setValue(i)
        self.loadFlag = False
        self.radioLog.sort(key=lambda entry: entry[6])  # sort by epoch seconds
        ##		self.radioLog[1:]=[x for x in self.radioLog[1:] if not x[3].startswith('Radio Log Begins:')]

        # take care of the newEntry cleanup functions that have been put off due to loadFlag

        # apparently, we need to emit layoutChanged and then scrollToBottom, before resizeColumnToContents,
        #  to make sure column width resizes to fit >all< contents (i.e 'Team 5678'). ??
        # they could be put inside redrawTables, but, there's no need to put them inside that
        #  function which is called from other places, unless another syptom shows up; so, leave
        #  them here for now.
        self.tableView.model().layoutChanged.emit()
        self.tableView.scrollToBottom()
        ##		self.tableView.resizeRowsToContents()
        ##		for i in range(self.tabWidget.count()):
        ##			self.tabWidget.setCurrentIndex(i)
        ##			self.tableViewList[i].scrollToBottom()
        ##			self.tableViewList[i].resizeRowsToContents()

        ##		self.tableView.model().layoutChanged.emit()

        # now load the clue log (same filename appended by .clueLog) if it exists
        clueLogFileName = fileName.replace(".csv", "_clueLog.csv")
        if os.path.isfile(clueLogFileName):
            with open(clueLogFileName, "r") as csvFile:
                csvReader = csv.reader(csvFile)
                ##				self.clueLog=[] # uncomment this line to overwrite instead of combine
                for row in csvReader:
                    if not row[0].startswith("#"):  # prune comment lines
                        self.clueLog.append(row)
                        if row[0] != "":
                            lastClueNumber = int(row[0])
                csvFile.close()

        self.clueLogDialog.tableView.model().layoutChanged.emit()
        # finished
        LOG.debug("Starting redrawTables")
        self.fontsChanged()
        ##		self.tableView.model().layoutChanged.emit()
        ##		QCoreApplication.processEvents()
        LOG.debug("Returned from redrawTables")
        progressBox.close()
        self.opPeriodButton.setText("OP " + str(self.opPeriod))
        self.teamTimer.start(1000)  # resume
        self.lastSavedFileName = "NONE"
        self.updateFileNames()  # note, no file will be saved until the next entry is made
        self.saveRcFile()

    def updateFileNames(self):
        # update the filenames based on current incident name and current date/time
        # normalize the name for purposes of filenames
        #  - get rid of all spaces -  no need to be able to reproduce the
        #    incident name's spaces from the filename
        self.incidentNameNormalized = normalizeName(self.incidentName)
        self.csvFileName = getFileNameBase(self.incidentNameNormalized) + ".csv"
        self.pdfFileName = getFileNameBase(self.incidentNameNormalized) + ".pdf"
        self.fsFileName = self.csvFileName.replace(".csv", "_fleetsync.csv")

    def optionsAccepted(self):
        self.incidentName = self.optionsDialog.incidentField.text()
        self.updateFileNames()
        # don't change the rc file at this point - wait until a log entry is actually saved
        self.incidentNameLabel.setText(self.incidentName)
        self.datum = self.optionsDialog.datumField.currentText()
        self.coordFormat = self.optionsDialog.formatField.currentText()
        # TMG 4-22-15: do not try to convert coords right now: it fails due to space in radioLoc i.e. "NO FIX"
        ##		for row in self.radioLog:
        ##			if row[9] and row[9]!='':
        ##				row[4]=self.convertCoords(row[9].split('|'),self.datum,self.coordFormat)
        ##		self.redrawTables()
        self.datumFormatLabel.setText(self.datum + "\n" + self.coordFormat)
        self.timeoutRedSec = TIMEOUT_DISPLAY_LIST[self.optionsDialog.timeoutField.value()][1]
        self.timeoutOrangeSec = self.timeoutRedSec - 300  # always go orange 5 minutes before red
        if self.timeoutOrangeSec < 0:
            self.timeoutOrangeSec = self.timeoutRedSec - 3  # or 3 seconds before for tiny values
        self.timeoutLabel.setText("TIMEOUT:\n" + TIMEOUT_DISPLAY_LIST[self.optionsDialog.timeoutField.value()][0])

    def openNewEntry(self, key=None, callsign=None, formattedLocString=None, fleet=None, dev=None, origLocString=None, amendFlag=False, amendRow=None):
        LOG.debug(
            "openNewEntry called:key="
            + str(key)
            + " callsign="
            + str(callsign)
            + " formattedLocString="
            + str(formattedLocString)
            + " fleet="
            + str(fleet)
            + " dev="
            + str(dev)
            + " origLocString="
            + str(origLocString)
            + " amendFlag="
            + str(amendFlag)
            + " amendRow="
            + str(amendRow)
        )
        if clueDialog.openDialogCount == 0:
            self.newEntryWindow.setWindowFlags(Qt.WindowTitleHint | Qt.WindowStaysOnTopHint)  # enable always on top
        else:
            self.newEntryWindow.setWindowFlags(Qt.WindowTitleHint)
        sec = time.time()  # epoch seconds, for sorting purposes; not displayed
        self.newEntryWidget = NewEntryWidget(self, sec, formattedLocString, fleet, dev, origLocString, amendFlag, amendRow)
        # focus rules and timeline:
        #  openNewEntry
        #    |-> newEntryWidget.__init__
        #    |     |-> addTab
        #    |           |-> focus to new messageField if existing holdSec has elapsed
        #    |-> process 'key' to further change focus as needed

        # note, this timeline points out that changing focus in the 'key' handler
        #  to a widget of the newEntryWidget only makes sense if addTab determined
        #  that the newEntryWidget should be the active stack item; otherwise we would
        #  just be setting focus to a field in one of the inactive/hidden stack items.
        #  This was the cause of bug #354.

        # - if spawned by fleetsync: let addTab determine focus
        # - if spawned from the keyboard: we can assume the newEntryWidget will
        #    be the active stack item, since you can't use the keyboard in the main
        #    GUI if there is an existing message in the stack, so, it's safe
        #    to set focus to a widget of the newEntryWidget here
        # - if spawned from a mouse click (Add Entry button, or team tab context menu)
        #    then the new entry should become the active entry ('cutting in line'),
        #    so it is also safe to set focus to a widget of the newEntryWidget here
        #     (future improvement: remember which stack item was active before this
        #      'cutting in line', and go back to it after the new entry is closed,
        #       if it still exists / has not been auto-cleaned)

        if key:
            if self.teamHotkeysWidget.isVisible() and len(key) == 1:
                self.newEntryWidget.to_fromField.setCurrentIndex(0)
                self.newEntryWidget.teamField.setText(self.team_hot_keys.getTeam(key))
                self.newEntryWidget.messageField.setFocus()
            else:
                if key == "fs":  # spawned by fleetsync: let addTab determine focus
                    pass
                elif key == "a":
                    self.newEntryWidget.set_partial_team_name(1, "All Teams")
                    self.newEntryWidget.messageField.setFocus()
                elif key == "t":
                    self.newEntryWidget.set_partial_team_name(1, "Team")
                elif key == "f" or key == "pop":
                    self.newEntryWidget.set_partial_team_name(0, "Team" if key == "f" else "")
                elif key == "s":
                    self.newEntryWidget.set_partial_team_name(0, "SAR")
                elif key == "tab":  # team tab context menu - activate right away
                    self.newEntryWidget.set_partial_team_name(1, "")
                else:  # some other keyboard key - assume it's the start of the team name
                    self.newEntryWidget.set_partial_team_name(0, "Team " + key)
        else:  # no key pressed; opened from the 'add entry' GUI button; activate right away
            self.newEntryWidget.set_partial_team_name(0, "")

        if callsign:
            extTeamName = getExtTeamName(callsign)
            self.newEntryWidget.teamField.setText(callsign)
            self.newEntryWidget.teamFieldEditingFinished()  # check for relay
            if callsign[0:3] == "KW-":
                self.newEntryWidget.teamField.setFocus()
                self.newEntryWidget.teamField.selectAll()
            if callsign[0:6] == "Radio " or callsign[0:3] == "KW-":
                LOG.debug("setting needsChangeCallsign")
                self.newEntryWidget.needsChangeCallsign = True
                # if it's the only item on the stack, open the change callsign
                #   dialog right now, since the normal event loop won't process
                #   needsChangeCallsign until the tab changes
                if self.newEntryWidget == self.newEntryWindow.tabWidget.currentWidget():
                    QTimer.singleShot(500, lambda: self.newEntryWidget.openChangeCallsignDialog())
                # note that changeCallsignDialog.accept is responsible for
                #  setting focus back to the messageField of the active message
                #  (not always the same as the new message)

        if formattedLocString:
            datumFormatString = "(" + self.datum + "  " + self.coordFormat + ")"
            if self.newEntryWidget.relayed:
                self.newEntryWidget.radioLocTemp = formattedLocString
                self.newEntryWidget.datumFormatTemp = datumFormatString
            else:
                self.newEntryWidget.radioLocField.setText(formattedLocString)
                self.newEntryWidget.datumFormatLabel.setText(datumFormatString)
        else:
            self.newEntryWidget.datumFormatLabel.setText("")

    def newEntry(self, values):
        # values array format: [time,to_from,team,message,locString,status,sec,fleet,dev]
        #  locString is also stored in the table in a column after dev, unmodified;
        #  the value in the 5th column is modified in place based on the datum and
        #  coordinate format; this is cleaner than formatting the coordinates in the
        #  QAbstractTableModel, because the hardcoded table values will show up in the
        #  saved file as expected.
        #  Only columns thru and including status are shown in the tables.
        LOG.debug("newEntry called with these values:")
        LOG.debug(values)
        niceTeamName = values[2]
        extTeamName = getExtTeamName(niceTeamName)
        status = values[5]
        if values[4] is None:
            values[4] = ""
        sec = values[6]  # epoch seconds of dialog open time, for sorting; not displayed
        # sorting is bad because layoutChanged should be emitted which is slow;
        #  since the only reason we really need to sort is to make sure that
        #  entries are saved and displayed in the order they began (not necessarily
        #  the same as the order they were accepted if multiple items are
        #  on the stack), just do that by hand here when determining where to insert
        #  the accepted entry into the radioLog list:
        # if new sec is greater than the sec of the last radioLog item, then append.
        # otherwise, decrement the index where the new row should be inserted,
        #  and try the test again until new sec is greater than the sec of the
        #  entry 'above'.
        # proper use of beginInsertRows and endInsertRows here makes sure the view(s)
        #  refresh automatically, allowing newEntryPost to be simplified,
        #  reducing lag by 90+%
        i = len(self.radioLog) - 1  # i = zero-based list index of the last element
        while i > -1 and sec < self.radioLog[i][6]:
            i = i - 1
        # 			LOG.debug("new entry sec="+str(sec)+"; prev entry sec="+str(self.radioLog[i+1][6])+"; decrementing: i="+str(i))
        # at this point, i is the index of the item AFTER which the new entry should be inserted,
        #  so, use i+1 for the actual insertion
        i = i + 1
        if not self.loadFlag:
            model = self.tableView.model()
            model.beginInsertRows(QModelIndex(), i, i)  # this is one-based
        # 		self.radioLog.append(values) # leave a blank entry at the end for aesthetics
        # myList.insert(i,val) means val will become myList[i] using a zero-based index
        #  i.e. val will be the (i+1)th element in the list
        self.radioLog.insert(i, values)
        # 		LOG.debug("inserting entry at index "+str(i))
        if not self.loadFlag:
            model.endInsertRows()
        ##		if not values[3].startswith("RADIO LOG SOFTWARE:"):
        ##			self.newEntryProcessTeam(niceTeamName,status,values[1],values[3])
        self.newEntryProcessTeam(niceTeamName, status, values[1], values[3])

    def newEntryProcessTeam(self, niceTeamName, status, to_from, msg):
        extTeamName = getExtTeamName(niceTeamName)
        # 393: if the new entry's extTeamName is a case-insensitive match for an
        #   existing extTeamName, use that already-existing extTeamName instead
        for existingExtTeamName in self.extTeamNameList:
            if extTeamName.lower() == existingExtTeamName.lower():
                extTeamName = existingExtTeamName
                break
        # skip entries with no team like 'radio log begins', or multiple entries like 'all'
        if niceTeamName != "" and not niceTeamName.lower() == "all" and not niceTeamName.lower().startswith("all "):
            # if it's a team that doesn't already have a tab, make a new tab
            if extTeamName not in self.extTeamNameList:
                self.newTeam(niceTeamName)
            i = self.extTeamNameList.index(extTeamName)
            teamStatusDict[extTeamName] = status
            if not extTeamName in teamFSFilterDict:
                teamFSFilterDict[extTeamName] = 0
            # credit to Berryblue031 for pointing out this way to style the tab widgets
            # http://www.qtcentre.org/threads/49025
            # NOTE the following line causes font-size to go back to system default;
            #  can't figure out why it doesn't inherit font-size from the existing
            #  styleSheet; so, each statusStyleDict entry must contain font-size explicitly
            self.tabWidget.tabBar().tabButton(i, QTabBar.LeftSide).setStyleSheet(statusStyleDict[status])
            # only reset the team timer if it is a 'FROM' message with non-blank message text
            #  (prevent reset on amend, where to_from can be "AMEND" and msg can be anything)
            if to_from == "FROM" and msg != "":
                teamTimersDict[extTeamName] = 0
            if status == "At IC":
                teamTimersDict[extTeamName] = -1  # no more timeouts will show up
        if not self.loadFlag:
            QTimer.singleShot(100, lambda: self.newEntryPost(extTeamName))

    def newEntryPost(self, extTeamName=None):
        # 		LOG.debug("1: called newEntryPost")
        self.radioLogNeedsPrint = True
        # don't do any sorting at all since layoutChanged during/after sort is
        #  a huge cause of lag; see notes in newEntry function
        # 		LOG.debug("3")
        # resize the bottom-most rows (up to 10 of them):
        #  this makes lag time independent of total row count for large tables,
        #  and reduces overall lag about 30% vs resizeRowsToContents (about 3 sec vs 4.5 sec for a 1300-row table)
        for n in range(len(self.radioLog) - 10, len(self.radioLog)):
            if n >= 0:
                self.tableView.resizeRowToContents(n + 1)
        # 		LOG.debug("4")
        self.tableView.scrollToBottom()
        # 		LOG.debug("5")
        for i in [2, 4]:  # hardcode results in significant speedup
            self.tableView.resizeColumnToContents(i)
        # 		LOG.debug("5.1")
        # note, the following clause results in a small lag for very large team count
        #  and large radioLog (about 0.1sec on TomZen for 180kB log file); probably
        #  not worth trying to optimize
        for n in self.tableViewList[1:]:
            for i in [2, 4]:  # hardcode results in significant speedup
                n.resizeColumnToContents(i)
        # 		LOG.debug("5.2")
        if extTeamName:
            # 			LOG.debug("5.2.1")
            if extTeamName == "ALL TEAMS":
                for i in range(1, len(self.extTeamNameList)):
                    self.tabWidget.setCurrentIndex(i)
                    self.tableViewList[i].resizeRowsToContents()
                    for n in range(len(self.radioLog) - 10, len(self.radioLog)):
                        if n >= 0:
                            self.tableViewList[i].resizeRowToContents(n + 1)
                    self.tableViewList[i].scrollToBottom()
            elif extTeamName != "z_00000":
                # 				LOG.debug("5.2.1.2")
                if extTeamName in self.extTeamNameList:
                    # 					LOG.debug("5.2.1.2.1")
                    i = self.extTeamNameList.index(extTeamName)
                    # 					LOG.debug("  a: i="+str(i))
                    self.tabWidget.setCurrentIndex(i)
                    # 					LOG.debug("  b")
                    self.tableViewList[i].resizeRowsToContents()
                    # 					LOG.debug("  c")
                    for n in range(len(self.radioLog) - 10, len(self.radioLog)):
                        if n >= 0:
                            self.tableViewList[i].resizeRowToContents(n + 1)
                    # 					LOG.debug("  d")
                    self.tableViewList[i].scrollToBottom()
        # 					LOG.debug("  e")
        # 		LOG.debug("6")
        self.save()

    ##		self.redrawTables()
    ##		QCoreApplication.processEvents()
    # 		LOG.debug("7: finished newEntryPost")

    def tableContextMenu(self, pos):
        row = self.tableView.rowAt(pos.y())
        rowData = self.radioLog[row]
        LOG.debug("row:" + str(row) + ":" + str(rowData))
        if row > 0 and rowData[1]:
            self.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
            self.tableView.selectRow(row)
            rowHasRadioLoc = False
            rowHasMsgCoords = False
            ##			if rowData[9] and rowData[9]!="":
            ##				rowHasRadioLoc=True
            ##			if re.search(r'[0-9]{4,}',rowData[3]): # a string of four or more digits in the message
            ##				rowHasMsgCoords=True
            menu = QMenu()
            amendAction = menu.addAction("Amend this entry")
            ##			convertAction=menu.addAction("Convert coordinates")
            ##			if not (rowHasRadioLoc or rowHasMsgCoords):
            ##				convertAction.setEnabled(False)
            action = menu.exec_(self.tableView.viewport().mapToGlobal(pos))
            self.tableView.clearSelection()
            self.tableView.setSelectionMode(QAbstractItemView.NoSelection)
            if action == amendAction:
                self.amendEntry(row)

    ##			if action==convertAction:
    ##				self.convertDialog=convertDialog(self,rowData,rowHasRadioLoc,rowHasMsgCoords)
    ##				self.convertDialog.show()

    def amendEntry(self, row):
        LOG.debug("Amending row " + str(row))
        amendDialog = self.openNewEntry(amendFlag=True, amendRow=row)

    def rebuildTabs(self):
        self.tabList = []
        self.tabGridLayoutList = []
        self.tableViewList = []

        bar = self.tabWidget.tabBar()
        while bar.count() > 0:
            bar.removeTab(0)
        for extTeamName in self.extTeamNameList:
            self.addTab(extTeamName)

    def newTeam(self, newTeamName):
        # not sure why newTeamName is False (bool) when called as a slot;
        # setting a default val for the arg has not effect, so just work with it
        if newTeamName == False:
            newTeamName = "Team0"

        # determine the correct index - keep team tabs in sequential order,
        # with non-"Team" callsigns alphabettically at the end
        # 1. append the new extended team name to extTeamNameList
        # 2. sort extTeamNameList (simple alphaumeric sort)
        # 3. find the index of the new extended team name in extTeamNameList
        # 4. add newTeamName to teamNameList at that index
        extTeamName = getExtTeamName(newTeamName)
        niceTeamName = getNiceTeamName(extTeamName)
        shortNiceTeamName = getShortNiceTeamName(niceTeamName)
        LOG.debug("new team: newTeamName=" + newTeamName + " extTeamName=" + extTeamName + " niceTeamName=" + niceTeamName + " shortNiceTeamName=" + shortNiceTeamName)
        self.extTeamNameList.append(extTeamName)
        LOG.debug("extTeamNameList before sort:" + str(self.extTeamNameList))
        # 		self.extTeamNameList.sort()

        self.rebuildGroupedTabDict()
        LOG.debug("extTeamNameList after sort:" + str(self.extTeamNameList))
        self.rebuildTabs()

        if not extTeamName.startswith("spacer"):
            # add to team name lists and dictionaries
            i = self.extTeamNameList.index(extTeamName)  # i is zero-based
            self.teamNameList.insert(i, niceTeamName)
            # 			LOG.debug("   niceTeamName="+str(niceTeamName)+"  allTeamsList before:"+str(self.allTeamsList)+"  count:"+str(self.allTeamsList.count(niceTeamName)))
            if self.allTeamsList.count(niceTeamName) == 0:
                self.allTeamsList.insert(i, niceTeamName)
                self.allTeamsList.sort()
            # 				LOG.debug("   allTeamsList after:"+str(self.allTeamsList))
            teamTimersDict[extTeamName] = 0
            teamCreatedTimeDict[extTeamName] = time.time()
            self.team_hot_keys.assignTeamHotkey(niceTeamName)

        self.team_hot_keys.rebuildTeamHotkeys(self.teamHotkeysHLayout, self.tabWidget)

    def addTab(self, extTeamName):
        niceTeamName = getNiceTeamName(extTeamName)
        shortNiceTeamName = getShortNiceTeamName(niceTeamName)
        # 		LOG.debug("new team: extTeamName="+extTeamName+" niceTeamName="+niceTeamName+" shortNiceTeamName="+shortNiceTeamName)
        i = self.extTeamNameList.index(extTeamName)  # i is zero-based
        self.tabList.insert(i, QWidget())
        self.tabGridLayoutList.insert(i, QGridLayout(self.tabList[i]))
        self.tableViewList.insert(i, QTableView(self.tabList[i]))
        self.tableViewList[i].verticalHeader().setVisible(False)
        self.tableViewList[i].setTextElideMode(Qt.ElideNone)
        self.tableViewList[i].setFocusPolicy(Qt.NoFocus)
        self.tableViewList[i].setSelectionMode(QAbstractItemView.NoSelection)
        self.tableViewList[i].setStyleSheet("font-size:" + str(self.fontSize) + "pt")
        self.tabGridLayoutList[i].addWidget(self.tableViewList[i], 0, 0, 1, 1)
        self.tabWidget.insertTab(i, self.tabList[i], "")
        label = QLabel(" " + shortNiceTeamName + " ")
        if len(shortNiceTeamName) < 2:
            label.setText("  " + shortNiceTeamName + "  ")  # extra spaces to make effective tab min width
        if extTeamName.startswith("spacer"):
            label.setText("")
        else:
            # 			LOG.debug("setting style for label "+extTeamName)
            label.setStyleSheet("font-size:18px;qproperty-alignment:AlignCenter")
        # 			label.setStyleSheet(statusStyleDict[""])
        # 		LOG.debug("setting tab button #"+str(i)+" to "+label.text())
        bar = self.tabWidget.tabBar()
        bar.setTabButton(i, QTabBar.LeftSide, label)
        # during rebuildTeamHotkeys, we need to read the name of currently displayed tabs.
        #  An apparent bug causes the tabButton (a label) to not have a text attrubite;
        #  so, use the whatsThis attribute instead.
        bar.setTabWhatsThis(i, niceTeamName)
        # 		LOG.debug("setting style for tab#"+str(i))
        bar.tabButton(i, QTabBar.LeftSide).setStyleSheet(statusStyleDict[""])
        # spacers should be disabled
        if extTeamName.startswith("spacer"):
            bar.setTabEnabled(i, False)

        # better to NOT modify the entered team name value, for data integrity;
        # instead, set the filter to only display rows where the human readable form
        # of the value in column 2 matches the human readable form of the tab name
        self.proxyModelList.insert(i, CustomSortFilterProxyModel(self))
        self.proxyModelList[i].setSourceModel(self.tableModel)
        self.proxyModelList[i].setFilterFixedString(extTeamName)
        self.tableViewList[i].setModel(self.proxyModelList[i])
        self.tableViewList[i].hideColumn(6)  # hide epoch seconds
        self.tableViewList[i].hideColumn(7)  # hide epoch seconds
        self.tableViewList[i].hideColumn(8)  # hide epoch seconds
        self.tableViewList[i].hideColumn(9)  # hide epoch seconds
        self.tableViewList[i].resizeRowsToContents()

        # NOTE if you do this section before the model is assigned to the tableView,
        # python will crash every time!
        # see the QHeaderView.ResizeMode docs for descriptions of each resize mode value
        # note QHeaderView.setResizeMode is deprecated in 5.4, replaced with
        # .setSectionResizeMode but also has both global and column-index forms
        self.tableViewList[i].horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # automatically expand the 'message' column width to fill available space
        self.tableViewList[i].horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)

    def rebuildGroupedTabDict(self):
        # sort the tabs list, inserting hidden uniquely-named spacer tabs between groups
        # grouping sequence and regular expressions are defined in the local config file
        #  with the 'tabGroups' variable, which is a list of regular expressions;
        #  any callsign that does not match any of the regular expressions will
        #  be placed in a catch-all group at the end.
        # Once a callsign has been assigned to a group, make sure to not assign it
        #  to any other groups.
        grouped = dict()
        for grp in self.tabGroups:
            grouped[grp[0]] = []
        grouped["other"] = []
        for etn in [x for x in self.extTeamNameList if not x.startswith("spacer")]:  # spacerless list
            g = "other"  # default to the 'other' group
            for grp in self.tabGroups:
                if re.match(grp[1].replace("^", "^z_0*").replace("Team ", "Team"), etn, re.IGNORECASE):
                    # account for leading 'z_' and any zeros introduced by getExtTeamName
                    g = grp[0]
                    break  # use only the first matching group
            grouped[g].append(etn)

        # sort alphanumerically within each group
        for grp in grouped:
            grouped[grp].sort()

        LOG.debug("grouped tabs:" + str(grouped))
        self.groupedTabDict = grouped

        # rebuild self.extTeamNameList, with groups and spacers in the correct order,
        #  since everything throughout the code keys off its sequence;
        #  note the spacer names need to be unique for later processing
        self.extTeamNameList = []
        spacerIndex = 1  # start with 1 so trailing 0 doesn't get deleted in getNiceTeamName
        for grp in self.tabGroups:
            # 			LOG.debug("group:"+str(grp)+":"+str(grouped[grp[0]]))
            for val in grouped[grp[0]]:
                # 				LOG.debug("appending:"+val)
                self.extTeamNameList.append(val)
            if len(grouped[grp[0]]) > 0:
                self.extTeamNameList.append("spacer" + str(spacerIndex))
                spacerIndex = spacerIndex + 1
        for val in grouped["other"]:
            if val != "dummy":
                # 				LOG.debug("appending other:"+val)
                self.extTeamNameList.append(val)

    def tabContextMenu(self, pos):
        menu = QMenu()
        LOG.debug("tab context menu requested: pos=" + str(pos))
        ##		menu.setStyleSheet("font-size:"+str(self.fontSize)+"pt")
        bar = self.tabWidget.tabBar()
        i = bar.tabAt(pos)  # returns -1 if not a valid tab
        LOG.debug("  i=" + str(i) + "  tabRect=" + str(bar.tabRect(i).bottomLeft()) + ":" + str(bar.tabRect(i).topRight()))
        extTeamName = self.extTeamNameList[i]
        niceTeamName = getNiceTeamName(extTeamName)
        LOG.debug("  extTeamName=" + str(extTeamName) + "  niceTeamName=" + str(niceTeamName))
        # 		if i>0:
        if i > -1 and not extTeamName.lower().startswith("spacer"):
            newEntryFromAction = menu.addAction("New Entry FROM " + str(niceTeamName))
            newEntryToAction = menu.addAction("New Entry TO " + str(niceTeamName))
            menu.addSeparator()
            printTeamLogAction = menu.addAction(QIcon(QPixmap(":/radiolog_ui/print_icon.png")), "Print " + str(niceTeamName) + " Log")
            menu.addSeparator()
            ##			relabelTeamTabAction=menu.addAction("Change Label / Assignment for "+str(niceTeamName))
            ##			menu.addSeparator()

            # add fleetsync submenu if there are any fleetsync devices for this callsign
            devices = self.fsGetTeamDevices(extTeamName)
            fsToggleAllAction = False  # initialize, so the action checker does not die
            if len(devices) > 0:
                fsMenu = menu.addMenu("FleetSync...")
                menu.addSeparator()
                if len(devices) > 1:
                    if teamFSFilterDict[extTeamName] == 2:
                        fsToggleAllAction = fsMenu.addAction("Unfilter all " + niceTeamName + " devices")
                    else:
                        fsToggleAllAction = fsMenu.addAction("Filter all " + niceTeamName + " devices")
                    fsMenu.addSeparator()
                    for device in devices:
                        key = str(device[0]) + ":" + str(device[1])
                        if self.fsIsFiltered(device[0], device[1]):
                            fsMenu.addAction("Unfilter calls from " + key).setData([device[0], device[1], False])
                        else:
                            fsMenu.addAction("Filter calls from " + key).setData([device[0], device[1], True])
                else:
                    key = str(devices[0][0]) + ":" + str(devices[0][1])
                    if teamFSFilterDict[extTeamName] == 2:
                        fsToggleAllAction = fsMenu.addAction("Unfilter calls from " + niceTeamName + " (" + key + ")")
                    else:
                        fsToggleAllAction = fsMenu.addAction("Filter calls from " + niceTeamName + " (" + key + ")")

            deleteTeamTabAction = menu.addAction("Hide tab for " + str(niceTeamName))
            action = menu.exec_(self.tabWidget.tabBar().mapToGlobal(pos))
            if action == newEntryFromAction:
                self.openNewEntry("tab", str(niceTeamName))
            if action == newEntryToAction:
                self.openNewEntry("tab", str(niceTeamName))
                self.newEntryWidget.to_fromField.setCurrentIndex(1)
            if action == printTeamLogAction:
                LOG.debug("printing team log for " + str(niceTeamName))
                printLog(self.opPeriod, self.getPrintParams(), str(niceTeamName))
                self.radioLogNeedsPrint = True  # since only one log has been printed; need to enhance this
            if action == deleteTeamTabAction:
                self.deleteTeamTab(niceTeamName)
            if action and action.data():  # only the single-device toggle actions will have data
                # 				LOG.debug("fsToggleOneAction called; data="+str(action.data()))
                d = action.data()
                self.fsFilterEdit(d[0], d[1], d[2])
                self.fsBuildTeamFilterDict()
            if action == fsToggleAllAction:
                newState = teamFSFilterDict[extTeamName] != 2  # if 2, unfilter all; else, filter all
                for device in self.fsGetTeamDevices(extTeamName):
                    self.fsFilterEdit(device[0], device[1], newState)
                self.fsBuildTeamFilterDict()

    ##			if action==relabelTeamTabAction:
    ##				label=QLabel(" abcdefg ")
    ##				label.setStyleSheet("font-size:20px;border:1px outset black;qproperty-alignment:AlignCenter")
    ##				self.tabWidget.tabBar().setTabButton(i,QTabBar.LeftSide,label)
    ####				self.tabWidget.tabBar().setTabText(i,"boo")
    ##				self.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).setStyleSheet("font-size:20px;border:1px outset black;qproperty-alignment:AlignCenter")

    def deleteTeamTab(self, teamName, ext=False):
        # optional arg 'ext' if called with extTeamName
        # must also modify related lists to keep everything in sync
        extTeamName = getExtTeamName(teamName)
        if ext:
            extTeamName = teamName
        niceTeamName = getNiceTeamName(extTeamName)
        # 		self.extTeamNameList.sort()
        LOG.debug("deleting team tab: teamName=" + str(teamName) + "  extTeamName=" + str(extTeamName) + "  niceTeamName=" + str(niceTeamName))
        LOG.debug("  teamNameList before deletion:" + str(self.teamNameList))
        LOG.debug("  extTeamNameList before deletion:" + str(self.extTeamNameList))
        if extTeamName in self.extTeamNameList:  # pass through if trying to delete a tab that doesn't exist / has already been deleted
            i = self.extTeamNameList.index(extTeamName)
            LOG.debug("  i=" + str(i))
            self.extTeamNameList.remove(extTeamName)
            if not teamName.lower().startswith("spacer"):
                self.teamNameList.remove(niceTeamName)
                del teamTimersDict[extTeamName]
                del teamCreatedTimeDict[extTeamName]
            del self.tabList[i]
            del self.tabGridLayoutList[i]
            del self.tableViewList[i]
            self.tabWidget.removeTab(i)
            try:
                del self.proxyModelList[i]
            except:
                LOG.debug("  ** sync error: proxyModelList current length = " + str(len(self.proxyModelList)) + "; requested to delete index " + str(i) + "; continuing...")
            else:
                LOG.debug("  deleted proxyModelList index " + str(i))

            self.team_hot_keys.freeHotkey(niceTeamName, self.tabWidget)
        self.team_hot_keys.rebuildTeamHotkeys(self.teamHotkeysHLayout, self.tabWidget)
        LOG.debug("  extTeamNameList after delete: " + str(self.extTeamNameList))
        # if there are two adjacent spacers, delete the second one
        for n in range(len(self.extTeamNameList) - 1):
            if self.extTeamNameList[n].lower().startswith("spacer"):
                if self.extTeamNameList[n + 1].lower().startswith("spacer"):
                    LOG.debug("  found back-to-back spacers at indices " + str(n) + " and " + str(n + 1))
                    self.deleteTeamTab(self.extTeamNameList[n + 1], True)

    def toggleTeamHotkeys(self):
        vis = self.teamHotkeysWidget.isVisible()
        if not vis:
            self.team_hot_keys.rebuildTeamHotkeys(self.teamHotkeysHLayout, self.tabWidget)
        self.teamHotkeysWidget.setVisible(not vis)

    def openOpPeriodDialog(self):
        self.opPeriodDialog = opPeriodDialog(self)
        self.opPeriodDialog.show()

    def addNonRadioClue(self):
        self.newNonRadioClueDialog = nonRadioClueDialog(self, time.strftime("%H%M"), lastClueNumber + 1)
        self.newNonRadioClueDialog.show()

    def restore(self):
        # use this function to reload the last saved files, based on lastFileName entry from resource file
        #  but, keep the new session's save filenames going forward
        if self.lastFileName == "NONE":
            inform_user_about_issue("Last saved filenames were not saved in the resource file.  Cannot automatically restore last saved files.  You will need to load the files directly [F4].", title="Cannot Restore", parent=-self)
            return
        fileToLoad = self.firstWorkingDir + "\\" + self.lastFileName
        if not os.path.isfile(fileToLoad):  # prevent error if dialog is canceled
            inform_user_about_issue("The file " + fileToLoad + " (specified in the resource file) does not exist.  You will need to load the files directly [F4].", title="Cannot Restore", parent=-self)
            return
        self.load(fileToLoad)  # loads the radio log and the clue log
        # hide warnings about missing fleetsync file, since it does not get saved until clean shutdown time
        self.fsLoadLookup(fsFileName=self.firstWorkingDir + "\\" + self.lastFileName.replace(".csv", "_fleetsync.csv"), hideWarnings=True)
        self.updateFileNames()
        self.fsSaveLookup()
        self.save()
        self.saveRcFile()


##class convertDialog(QDialog,Ui_convertDialog):
##	def __init__(self,parent,rowData,rowHasRadioLoc=False,rowHasMsgCoords=False):
##		QDialog.__init__(self)
##		self.Ui_convertDialog()
##		self.setupUi(self)
##		self.parent=parent
##		self.setWindowFlags(Qt.WindowStaysOnTopHint)
##		self.setAttribute(Qt.WA_DeleteOnClose)
##
##		metrix=QFontMetrics(self.msgField.font())
##		origText=rowData[0]+" "+rowData[1]+" "+rowData[2]+" : "+rowData[3]
##		clippedText=metrix.elidedText(origText,Qt.ElideRight,self.msgField.width())
##		self.msgField.setText(clippedText)
##
##		if not rowHasRadioLoc:
##			self.useRadioLocButton.setEnabled(False)
##			self.useCoordsInMessageButton.setChecked(True)
##		if not rowHasMsgCoords:
##			self.useCoordsInMessageButton.setEnabled(False)
##			self.useRadioLocButton.setChecked(True)
##
##		# initially set the target datum and format to the first choice that is not the same as the current log datum and format
##		datums=[self.datumComboBox.itemText(i) for i in range(self.datumComboBox.count())]
##		formats=[self.formatComboBox.itemText(i) for i in range(self.formatComboBox.count())]
##		self.datumComboBox.setCurrentText([datum for datum in datums if not datum==self.parent.datum][0])
##		self.formatComboBox.setCurrentText([coordFormat for coordFormat in formats if not coordFormat==self.parent.coordFormat][0])
##
##		if self.useRadioLocButton.isChecked():
##			self.origCoordsField.setText(rowData[9])
##		else:
##			self.origCoordsField.setText("")
##		self.origDatumFormatLabel.setText(self.parent.datum+"  "+self.parent.coordFormat)
##
##		self.goButton.clicked.connect(self.go)
##
####	def getCoordsFromString(self,string):
####		#1. parse into tokens, splitting on whitespace, comma, semicolon
####		#2. look for a pair of adjacent tokens that each have numbers in them
##
##	def go(self):
##		LOG.debug("CONVERTING")


class MyTableModel(QAbstractTableModel):
    header_labels = ["TIME", "T/F", "TEAM", "MESSAGE", "RADIO LOC.", "STATUS", "sec", "fleet", "dev", "origLoc"]

    def __init__(self, datain, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        # 		print("headerData:",section,",",orientation,",",role)
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header_labels[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)

    def rowCount(self, parent):
        return len(self.arraydata)

    def columnCount(self, parent):
        return len(self.arraydata[0])

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


class CustomSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        super(CustomSortFilterProxyModel, self).__init__(parent)

    # filterAcceptsRow - return True if row should be included in the model, False otherwise
    #
    # the value to test is the callsign (row[2])
    # the value to test against is the filterRegExp
    # for simple cases, this must be an exact match; but, we also want to accept
    # the row for 'all teams' or 'all'.  Future development: accept a list of teams
    def filterAcceptsRow(self, row, parent):
        target = self.filterRegExp().pattern()
        teamNameText = self.sourceModel().index(row, 2, parent).data()
        val = getExtTeamName(teamNameText)

        # for rows to all teams, only accept the row if the row's epoch time is earlier than the tab's creation time
        addAllFlag = False
        if teamNameText.lower() == "all" or teamNameText.lower().startswith("all "):
            if target in teamCreatedTimeDict:
                allEntryTime = self.sourceModel().index(row, 6, parent).data()
                if teamCreatedTimeDict[target] < allEntryTime:
                    addAllFlag = True
        ###		return(val==target or self.sourceModel().index(row,6,parent).data()==1e10)
        ##		return(val==target) # simple case: match the team name exactly
        return val == target or addAllFlag


# code for CSVFileSortFilterProxyModel partially taken from
#  https://github.com/ZhuangLab/storm-control/blob/master/steve/qtRegexFileDialog.py
class CSVFileSortFilterProxyModel(QSortFilterProxyModel):
    def __init__(self, parent=None):
        # 		print("initializing CSVFileSortFilterProxyModel")
        super(CSVFileSortFilterProxyModel, self).__init__(parent)

    # filterAcceptsRow - return True if row should be included in the model, False otherwise
    #
    # do not list files named *_fleetsync.csv or *_clueLog.csv
    #  do a case-insensitive comparison just in case
    def filterAcceptsRow(self, source_row, source_parent):
        # 		print("CSV filterAcceptsRow called")
        source_model = self.sourceModel()
        index0 = source_model.index(source_row, 0, source_parent)
        # Always show directories
        if source_model.isDir(index0):
            return True
        # filter files
        filename = source_model.fileName(index0).lower()
        # 		filename=self.sourceModel().index(row,0,parent).data().lower()
        # 		print("testing lowercased filename:"+filename)
        # never show non- .csv files
        if filename.count(".csv") < 1:
            return False
        if filename.count("_fleetsync") + filename.count("_cluelog") == 0:
            return True
        else:
            return False

    # use source model sort, otherwise date sort will be done alphamerically
    #  i.e. 9-1-2010 will be shown as more recent than 12-1-2018 since 9 > 1
    #  see https://stackoverflow.com/a/53797546/3577105
    def sort(self, column, order):
        self.sourceModel().sort(column, order)


class customEventFilter(QObject):
    def eventFilter(self, receiver, event):
        if event.type() == QEvent.ShortcutOverride and event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_Z:
            return True  # block the default processing of Ctrl+Z
        return super().eventFilter(receiver, event)


qt_app = QApplication(sys.argv)


def main():
    # This is supposed to be a quick fix for the scaling problem (https://github.com/ncssar/radiolog/issues/435)
    # but it acually makes things worse.
    # if hasattr(Qt, 'AA_EnableHighDpiScaling'):
    # 	QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    # if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
    # 	QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    LOG.diagnostic(f"Qt root directory (where qt.conf resides): {qt_app.applicationDirPath()}")
    eFilter = customEventFilter()
    qt_app.installEventFilter(eFilter)
    try:
        w = MyWindow(qt_app)
        w.show()
    except RadioLogError as e:
        msg = "ABORTING: {0}".format(e.message)
        LOG.critical(msg)
        inform_user_about_issue(msg, ICON_ERROR)
        sys.exit(-1)

    sys.exit(qt_app.exec_())


if __name__ == "__main__":
    main()
