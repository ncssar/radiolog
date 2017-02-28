# #############################################################################
#
#  radiolog.py - SAR Radio Log program, based on PyQt 5.4, Python 3.4.2
#
#   developed for Nevada County Sheriff's Search and Rescue
#    Copyright (c) 2015 Tom Grundy
#
#  http://ncssarradiologsoftware.sourceforge.net
#
#  Contact the author at nccaves@yahoo.com
#   Attribution, feedback, bug reports and feature requests are appreciated
#
#  REVISION HISTORY
#-----------------------------------------------------------------------------
#   DATE   |  AUTHOR  |  NOTES
#-----------------------------------------------------------------------------
#  2-22-15     TMG       First version installed and working on NCSSAR Computer 2
#  4-9-15      TMG       Feature-complete release candidate
#  4-10-15     TMG       enable reading from a second com port (two radios)
#  4-28-15     TMG       First release; initial commit to git
#  5-11-15     TMG       fix bug 10: don't clear team timer unless the message
#                         is 'FROM' with non-blank message text; change more
#                         app-wide stylesheet font sizes in fontsChanged, and
#                         change in children to override as needed
#  11-27-16    TMG       fix 307 (help window flashing colors are bouncing); also
#                         verified no ill effects in team tabs
#  12-1-16     TMG       fix 268 (throb crash on oldest item in non-empty stack)
#  12-1-16     TMG       add -nosend option to disable sending of GET requests,
#                         to avoid lag when network is not present
#  12-10-16    TMG       fix 267 (filename space handler) - remove spaces from
#                         incident name for purposes of filenames
#  12-10-16    TMG       fix 25 (print dialog button wording should change when
#                         called from main window exit button)
#  12-10-16    TMG       fix 306 (attached callsigns)
#   1-17-17    TMG       fix 41 (USB hot-plug / hot-unplug)
#   2-26-17    TMG       fix 311 (attached callsign bug)
#   2-27-17    TMG       fix 314 (NED focus / two-blinking-cursors)
#   2-27-17    TMG       fix 315 (ctrl-Z crash on empty list) for NED and for clue report
#   2-27-17    TMG       fix 312 (prevent orphaned clue/subject dialogs);
#                         fix 317 (crash on cancel of cancel for clue/subject dialogs);
#                         this involved changing dialog cancel buttons to just call
#                         close() instead of reject()
#   2-28-17    TMG       fix 316,318,320 (add dialog open/cancel radio log entries)
#                         and extend closeEvent functionality (above) to
#                         nonRadioClueDialog and changeCallsignDialog
# #############################################################################
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  See included file LICENSE.txt for full license terms, also
#  available at http://opensource.org/licenses/gpl-3.0.html
#
# ############################################################################
#
# Originally written and tested on Windows Vista Home Basic 32-bit;
#  should run for Windows Vista and higher
#
# Note, this file must be encoded as UTF-8, to preserve degree signs in the code
#
# ############################################################################
#
# key sequence behavior:
#
# when radio log form has focus:
#  <space> - open new entry dialog box: default values = from; first team in team combo box; time; focus goes to team field
#  <t> - open new entry dialog box: defaults = to; first team in team field; time; focus goes to team field
#  <f> - same as <space>
#  <any number> - open new entry dialog box: defaults = from; first team in team field whose first digit matches the typed number, or, new team# if none match; time
#
# when new entry dialog box has focus:
#
# known limitations:
#  cannot handle team names that have alpha characters after numeric characters (3b, 4a, etc)
#
# ############################################################################
#
#  message queue / stack rules:
#
#  when an incoming message happens during editing of an existing message:
#   1. add a stack entry on top of the stack and start flashing
#   2. if the current message has had no keystrokes / activity in the last n seconds,
#        leave it as is and move to the new entry
#   3. if the current message has had activity in the last n seconds, leave it open
#
#  when message is accepted:
#   1. go to next message upwards in the stack
#   2. if none, go the next message downwards in the stack
#   3. if none, close the dialog
#
#  every n seconds of inactivity:
#   1. accept the top message on the stack, and move to the next one
#
#  when any given message is set active:
#   1. stop flashing, if it was flashing
#
# ############################################################################
#
# external dependencies:
#  - installed GISInternals SDK including SDKShell.bat, cs2cs.exe, and grid shift files
#     (specify paths here using self.GISInternalsSDKRoot, sdkShellBat, cs2csExe variablies)
#     (download from http://www.gisinternals.com/release.php)
#
# core files of this project (until compiled/deployed):
#  - radiolog.py - this file, invoke with 'python radiolog.py' if not deployed
#  - radiolog_ui.py - pyuic5 compilation of radiolog.ui from QTDesigner
#  - newEntryDialog_ui.py - pyuic5 compilation of newEntryDialog.ui from QTDesigner
#  - options_ui.py - pyuic5 compilation of options.ui from QTDesigner
#  - help_ui.py - pyuic5 compilation of help.ui from QTDesigner
#  - radiolog_ui_qrc.py - pyrcc5 compilation of radiolog_ui.qrc from QTDesigner
#  - QTDesigner .ui and .qrc files as listed above
#
# ancillary files shipped with and/or referenced by this code:
#  - radiolog_logo.jpg - if the logo exists it is included in the printout
#  - radiolog_rc.txt - resource file, keeps track of last used window geometry and font size
#  - radiolog_fleetsync.csv - default CSV lookup table: fleet,device,callsign
#      (any fleet/device pairs that do not exist in that file will have callsign KW-<fleet>-<device>)
#
# files generated by this code:
#  NOTE: this program uses two working directories for redundancy.  The first one is
#    the current Windows user's Documents directory, and must be writable to avoid
#    a fatal error.  The second one will be written to on every new entry if it is available,
#    but will not cause any error if it is unavailable.  The second working directory
#    is specified below with the variable 'secondWorkingDir'.
#  - <incident_name>_<timestamp>.csv - CSV of entire radio log, written after each new entry
#  - <incident_name>_<timestamp>_fleetsync.csv - CSV FleetSync lookup table, written on each callsign change
#  - <incident_name>_<timestamp>_clueLog.csv - CSV clue log, written after each clue entry
#  - <incident_name>_<timestamp>_OP#.pdf - PDF of the radio log for specified operational period
#  - <incident_name>_<timestamp>_clueLog_OP#.pdf - PDF of the clue log for specified operational period
#  - <incident_name>_<timestamp>_clue##.fdf - FDF of clue report form (see calls to forge_fdf)
#  - <incident_name>_<timestamp>_clue##.fdf - PDF of clue report form
#    NOTE: upon change of incident name, previously saved files are not deleted, but
#      are kept in place as another backup.  Also, the previous log file is copied
#      as the new log file, so that file append on each new entry can continue
#      seamlessly.
#
# required non-core python modules:
#  - reportlab (for printing)
#  - pyserial (for com port / usb communication)
#  - requests (for forwarding locator information as a GET request for sarsoft)
#
# #############################################################################
#
# speed / performance notes
#
# once the table length gets about 500 rows or so, some delay is noticable:
#  - font resize (+/- keys)
#  - new entry form closed with 'OK' or Enter/Return, until the new entry appears in the table
#  - window resize
#  - print (delay per page)
#
# conclusions from benchmarking and speed tests on a table of around 1300 rows:
#  - the single biggest source of delay can be header resize modes:
#		...verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
#     will cause each row to resize whenever the contents change, which is probably
#     more often than you want, and will be called in a hidden / nested manner
#     inside other table view changes.  So, disable any lines like this, and only
#     resize when you really need to.  Removing this line reduced redraw time
#     on font change from 12 seconds to 3.  Also, it 'completely' eliminates
#     window resize delay.
#  - delay on entry form close is 'eliminated' / deferred by doing all the
#     redisplay work in a singleshot after the form is closed
#
# #############################################################################
# #############################################################################

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from help_ui import Ui_Help
from options_ui import Ui_optionsDialog
from newEntryWindow_ui import Ui_newEntryWindow
from newEntryWidget_ui import Ui_newEntryWidget
from clueDialog_ui import Ui_clueDialog
from clueLogDialog_ui import Ui_clueLogDialog
from printDialog_ui import Ui_printDialog
from changeCallsignDialog_ui import Ui_changeCallsignDialog
from opPeriodDialog_ui import Ui_opPeriodDialog
from printClueLogDialog_ui import Ui_printClueLogDialog
from nonRadioClueDialog_ui import Ui_nonRadioClueDialog
from convertDialog_ui import Ui_convertDialog
from subjectLocatedDialog_ui import Ui_subjectLocatedDialog

import functools
import sys
import time
import re
import serial
import serial.tools.list_ports
import csv
import os.path
import requests
import random
import subprocess
import win32api
import win32print
import shutil
import math
from reportlab.lib import colors,utils
from reportlab.lib.pagesizes import letter,landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.units import inch
from fdfgen import forge_fdf
from FingerTabs import *

# process command-line arguments
minMode=False
develMode=False
noSend=False
if len(sys.argv)>1:
	for arg in sys.argv[1:]:
		if arg.lower()=="-devel":
			develMode=True
			print("Development mode enabled.")
		if arg.lower()=="-min":
			minMode=True
			print("Minimum display size mode enabled.")
		if arg.lower()=="-nosend":
			noSend=True
			print("Will not send any GET requests for this session.")

if minMode:
	from radiolog_min_ui import Ui_Dialog # built to look decent at 800x600
else:
   from radiolog_ui import Ui_Dialog # normal version, for higher resolution

statusStyleDict={}
# even though tab labels are created with font-size:20px and the tab sizes and margins are created accordingly,
#  something after creation time is changing font-sizes to a smaller size.  So, just
#  hardcode them all here to force 20px always.
statusStyleDict["At IC"]="font-size:18px;background:#00ff00;border:1px outset black;padding-left:0px;padding-right:0px"
statusStyleDict["In Transit"]="font-size:18px;background:blue;color:white;border:1px outset black;padding-left:0px;padding-right:0px"
statusStyleDict["Working"]="font-size:18px;background:none;border:1px outset black;padding-left:0px;padding-right:0px"
# Waiting for Transport should still flash even if not timed out, but it doesn't
#  prevent a timeout.  So, for this code, and alternating timer cycles (seconds):
# cycle 1: style as in the following line
# cycle 2: if not timed out, style as "" (blank); if timed out, style as timeout as expected
statusStyleDict["Waiting for Transport"]="font-size:18px;background:blue;color:white;border:1px outset black;padding-left:0px;padding-right:0px;padding-top:-1px;padding-bottom:-1px"
statusStyleDict["STANDBY"]="font-size:18px;background:black;color:white;border:1px outset black;padding-left:0px;padding-right:0px;padding-top:-1px;padding-bottom:-1px"
statusStyleDict[""]="font-size:18px;background:none;padding-left:1px;padding-right:1px"
statusStyleDict["TIMED_OUT_ORANGE"]="font-size:18px;background:orange;border:1px outset black;padding-left:0px;padding-right:0px;padding-top:-1px;padding-bottom:-1px"
statusStyleDict["TIMED_OUT_RED"]="font-size:18px;background:red;border:1px outset black;padding-left:0px;padding-right:0px;padding-top:-1px;padding-bottom:-1px"

timeoutDisplayList=[["10 sec",10]]
for n in range (1,13):
	timeoutDisplayList.append([str(n*10)+" min",n*600])

teamStatusDict={}
teamTimersDict={}
teamCreatedTimeDict={}

versionDepth=5 # how many backup versions to keep; see rotateBackups

continueSec=20
holdSec=10

# log com port messages?
comLog=False

##newEntryDialogTimeoutSeconds=600
# choosing window location for newly opened dialog: just keeping a count of how many
# dialogs are open does not work, since an open dialog at a given position could
# still be completely covered by a newly opened dialog at that same position.
# Instead, create a list of valid fixed positions, then each newly opened dialog
# will just use the first available one in the list.  Update the list of which ones
# are used when each dialog is opened.
#openNewEntryDialogCount=0
##newEntryDialog_x0=100
##newEntryDialog_y0=100
##newEntryDialog_dx=30
##newEntryDialog_dy=30

lastClueNumber=0

##quickTextList=[
##	["DEPARTING IC",Qt.Key_F1],
##	["STARTING ASSIGNMENT",Qt.Key_F2],
##	["COMPLETED ASSIGNMENT",Qt.Key_F3],
##	["ARRIVING AT IC",Qt.Key_F4],
##	"separator",
##	["RADIO CHECK: OK",Qt.Key_F5],
##	["WELFARE CHECK: OK",Qt.Key_F6],
##	["REQUESTING TRANSPORT",Qt.Key_F7],
##	"separator",
##	["STANDBY",Qt.Key_F8],
##	"separator",
##	["LOCATED A CLUE",Qt.Key_F9],
##	"separator",
##	["SUBJECT LOCATED",Qt.Key_F10],
##	"separator",
##	["REQUESTING DEPUTY",Qt.Key_F11]]


def getExtTeamName(teamName):
	if teamName.lower().startswith("all ") or teamName.lower()=="all":
		return "ALL TEAMS"
	name=teamName.lower()
	name=name.replace(' ','')
	# find index of first number in the name; everything left of that is the 'prefix';
	# assume that everything after the prefix is a number
	firstNum=re.search("\d",name)
	firstNumIndex=-1 # assume there is no number at all
	if firstNum!=None:
		firstNumIndex=firstNum.start()
	if firstNumIndex>0:
		prefix=name[:firstNumIndex]
	else:
		prefix=""
#	print("FirstNumIndex:"+str(firstNumIndex)+" Prefix:'"+prefix+"'")
	# allow shorthand team names (t2) to still be inserted in the same sequence as
	# full team names (team2) so the tab list could be: team1 t2 team3
	# but other team names starting with t (tr1, transport1) would be added at the end
	if prefix=='t':
		prefix='team'
	# now force everything other than 'team' to be added alphabetically at the end,
	# by prefixing the prefix with 'z_' (the underscore makes it unique for easy pruning later)
	if prefix!='team':
		prefix="z_"+prefix
	if firstNum!=None:
		rest=name[firstNumIndex:].zfill(5)
	else:
		rest=teamName # preserve case if there are no numbers
##	rprint("prefix="+prefix+" rest="+rest+" name="+name)
	extTeamName=prefix+rest
#	print("Team Name:"+teamName+": extended team name:"+extTeamName)
	return extTeamName

def getNiceTeamName(extTeamName):
	# prune any leading 'z_' that may have been added for sorting purposes
	extTeamName=extTeamName.replace('z_','')
	# find index of first number in the name; everything left of that is the 'prefix';
	# assume that everything after the prefix is a number
	#  (left-zero-padded to 5 digits)
	firstNum=re.search("\d",extTeamName)
	firstNumIndex=-1 # assume there is no number at all
	if firstNum:
		firstNumIndex=firstNum.start()
	if firstNumIndex>0:
		prefix=extTeamName[:firstNumIndex]
#		name=prefix.capitalize()+" "+str(int(str(extTeamName[firstNumIndex:])))
		name=prefix.capitalize()+" "+str(extTeamName[firstNumIndex:]).lstrip('0')
	else:
		name=extTeamName
#	print("FirstNumIndex:"+str(firstNumIndex)+" Prefix:'"+prefix+"'")
#	print("Human Readable Name:'"+name+"'")
	return name

def getShortNiceTeamName(niceTeamName):
	# 1. remove spaces, then prune leading 'Team'
	shortNiceTeamName=niceTeamName.replace(' ','')
	shortNiceTeamName=shortNiceTeamName.replace('Team','')
	return shortNiceTeamName

def getFileNameBase(root):
	return root+"_"+time.strftime("%Y_%m_%d_%H%M%S")

logBuffer=""
logFileName=getFileNameBase("radiolog_log")+".txt"

def rprint(text):
	logText=str(int(time.time()))[-4:]+":"+str(text)
	print(logText)
	global logBuffer
	logBuffer+=logText+"\n"

# function to replace only the rightmost <occurrence> occurrences of <old> in <s> with <new>
# used by the undo function when adding new entry text
# credit to 'mg.' at http://stackoverflow.com/questions/2556108
def rreplace(s,old,new,occurrence):
	li=s.rsplit(old,occurrence)
	return new.join(li)

def writeLogBuffer():
	with open(logFileName,'a') as logFile:
		global logBuffer
		logFile.write(logBuffer)
		logFile.close()
		logBuffer=""

def rotateCsvBackups(fileName):
	rprint("Rotating backups for "+fileName)
	# iterate downwards through version depth (5 by default):
	# if the version exists, increment its version (if past max, delete it)
	# copy the current data file to backup version 1
	if not os.path.isfile(fileName):
		rprint(" No such file "+fileName+"; skipping rotateBackups")
		return
	for v in range(versionDepth,0,-1):
		rprint(" v="+str(v))
		if v==versionDepth:
			f=fileName.replace(".csv","_bak"+str(v)+".csv")
			if os.path.isfile(f):
				os.remove(f)
		else:
			src=fileName.replace(".csv","_bak"+str(v)+".csv")
			dst=fileName.replace(".csv","_bak"+str(v+1)+".csv")
			if os.path.isfile(src):
				os.rename(src,dst)
	shutil.copy(fileName,fileName.replace(".csv","_bak1.csv"))


class MyWindow(QDialog,Ui_Dialog):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.setWindowFlags(self.windowFlags()|Qt.WindowMinMaxButtonsHint)
		self.parent=parent
		self.ui=Ui_Dialog()
		self.ui.setupUi(self)
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.loadFlag=False # set this to true during load, to prevent save on each newEntry
		self.totalEntryCount=0 # rotate backups after every 5 entries; see newEntryWidget.accept

		self.incidentName="New Incident"
		self.incidentNameNormalized="NewIncident"
		self.opPeriod=1
		self.incidentStartDate=time.strftime("%a %b %d, %Y")

		self.radioLog=[[time.strftime("%H%M"),'','','Radio Log Begins: '+self.incidentStartDate,'','',time.time(),'','',''],
			['','','','','','',1e10,'','','']] # 1e10 epoch seconds will keep the blank row at the bottom when sorted

		self.clueLog=[]
		self.clueLog.append(['',self.radioLog[0][3],'',time.strftime("%H%M"),'','','','',''])

		self.lastFileName="" # to force error in restore, in the event the resource file doesn't specify the lastFileName
		self.csvFileName=getFileNameBase(self.incidentNameNormalized)+".csv"
		self.pdfFileName=getFileNameBase(self.incidentNameNormalized)+".pdf"
		self.fsFileName="radiolog_fleetsync.csv" # this is the default; modified filename is based on csvfilename at modify-time
##		self.fsFileName=self.getFileNameBase(self.incidentNameNormalized)+"_fleetsync.csv"

		self.fsValidFleetList=[100]
		self.fsFilteredDevList=[]
		self.getString=""

		self.firstWorkingDir=os.getenv('HOMEPATH','C:\\Users\\Default')+"\\Documents"
		if self.firstWorkingDir[1]!=":":
			self.firstWorkingDir=os.getenv('HOMEDRIVE','C:')+self.firstWorkingDir
		self.secondWorkingDir='Z:' # COMMON drive on the NCSSAR network
##		self.secondWorkingDir="C:\\Users\\Tom\\Documents\\sar"

##		# attempt to change to the second working dir and back again, to 'wake up'
##		#  any mount points, to hopefully avoid problems of second working dir
##		#  not always being written to, at all, for a given run of this program;
##		#  os.chdir dies gracefully if the specified dir does not exist
##		self.cwd=os.getcwd()
##		rprint("t1")
##		os.chdir(self.secondWorkingDir)
##		rprint("t2")
##		os.chdir(self.cwd)
##		rprint("t3")

		self.printLogoFileName="radiolog_logo.jpg"
		self.fillableClueReportPdfFileName="clueReportFillable.pdf"
		self.GISInternalsSDKRoot="C:\\GISInternals" # avoid spaces in the path - demons be here

		self.helpWindow=helpWindow()
		self.helpWindow.ui.hotkeysTableWidget.setColumnWidth(1,10)
		self.helpWindow.ui.hotkeysTableWidget.setColumnWidth(0,145)
		# note QHeaderView.setResizeMode is deprecated in 5.4, replaced with
		# .setSectionResizeMode but also has both global and column-index forms
		self.helpWindow.ui.hotkeysTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
		self.helpWindow.ui.hotkeysTableWidget.resizeRowsToContents()

		self.helpWindow.ui.colorLabel1.setStyleSheet(statusStyleDict["At IC"])
		self.helpWindow.ui.colorLabel2.setStyleSheet(statusStyleDict["In Transit"])
		self.helpWindow.ui.colorLabel3.setStyleSheet(statusStyleDict["Working"])
		self.helpWindow.ui.colorLabel4.setStyleSheet(statusStyleDict["Waiting for Transport"])
		self.helpWindow.ui.colorLabel5.setStyleSheet(statusStyleDict["TIMED_OUT_ORANGE"])
		self.helpWindow.ui.colorLabel6.setStyleSheet(statusStyleDict["TIMED_OUT_RED"])

		self.printDialog=printDialog(self)
		self.printClueLogDialog=printClueLogDialog(self)

		self.radioLogNeedsPrint=False # set to True with each new log entry; set to False when printed
		self.clueLogNeedsPrint=False

		self.optionsDialog=optionsDialog()
		self.optionsDialog.accepted.connect(self.optionsAccepted)

		self.ui.addNonRadioClueButton.clicked.connect(self.addNonRadioClue)

		self.ui.helpButton.clicked.connect(self.helpWindow.show)
		self.ui.optionsButton.clicked.connect(self.optionsDialog.show)
		self.ui.printButton.clicked.connect(self.printDialog.show)
##		self.ui.printButton.clicked.connect(self.testConvertCoords)

		self.sarsoftServerName="ncssar"
		if develMode:
			self.sarsoftServerName="localhost" # DEVEL

		self.ui.tabList=["dummy"]
		self.ui.tabGridLayoutList=["dummy"]
		self.ui.tableViewList=["dummy"]
		self.proxyModelList=["dummy"]
		self.teamNameList=["dummy"]
		self.allTeamsList=["dummy"] # same as teamNameList but hidden tabs are not deleted from this list
		self.extTeamNameList=["dummy"]
		self.fsLookup=[]
##		self.newEntryDialogList=[]
		self.blinkToggle=0
		self.fontSize=10
		self.timeoutRedSec=1800 # 30 minutes
		self.timeoutOrangeSec=1500 # 25 minutes
		self.datum="WGS84" # NCSSAR officially changed from NAD27 to WGS84 7-1-15
		self.coordFormat="UTM"
		self.x=100
		self.y=100
		self.w=600
		self.h=400
		self.clueLog_x=200
		self.clueLog_y=200
		self.clueLog_w=1000
		self.clueLog_h=400
		self.firstComPortAlive=False
		self.secondComPortAlive=False
		self.firstComPortFound=False
		self.secondComPortFound=False
		self.comPortScanInProgress=False
		self.comPortTryList=[]
##		if develMode:
##			self.comPortTryList=[serial.Serial("\\\\.\\CNCB0")] # DEVEL
		self.fsBuffer=""
		self.entryHold=False
		self.currentEntryLastModAge=0

		self.opPeriodDialog=opPeriodDialog(self)
		self.clueLogDialog=clueLogDialog(self)

		self.ui.pushButton.clicked.connect(self.openNewEntry)
		self.ui.opPeriodButton.clicked.connect(self.openOpPeriodDialog)
		self.ui.clueLogButton.clicked.connect(self.clueLogDialog.show) # never actually close this dialog

		self.ui.splitter.setSizes([250,150]) # any remainder is distributed based on this ratio
		self.ui.splitter.splitterMoved.connect(self.ui.tableView.scrollToBottom)

		self.tableModel = MyTableModel(self.radioLog, self)
		self.ui.tableView.setModel(self.tableModel)
		self.ui.tableView.setSelectionMode(QAbstractItemView.NoSelection)

		self.ui.tableView.hideColumn(6) # hide epoch seconds
		self.ui.tableView.hideColumn(7) # hide fleet
		self.ui.tableView.hideColumn(8) # hide device
		self.ui.tableView.hideColumn(9) # hide device
		self.ui.tableView.resizeRowsToContents()

		self.ui.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
		self.ui.tableView.customContextMenuRequested.connect(self.tableContextMenu)

		#downside of the following line: slow, since it results in a resize call for each column,
		#  when we could defer and just do one resize at the end of all the resizes
##		self.ui.tableView.horizontalHeader().sectionResized.connect(self.ui.tableView.resizeRowsToContents)
		self.columnResizedFlag=False
		self.ui.tableView.horizontalHeader().sectionResized.connect(self.setColumnResizedFlag)

		self.exitClicked=False
		# NOTE - the padding numbers for ::tab take a while to figure out in conjunction with
		#  the stylesheets of the label widgets of each tab in order to change status; don't
		#  change these numbers unless you want to spend a while on trial and error to get
		#  them looking good again!
		self.ui.tabWidget.setStyleSheet("""
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
				width:80px;
				color:black;
				font-weight:bold;
				background:transparent;
				border:transparent;
				padding-bottom:3px;
			}
		""")

		#NOTE if you do this section before the model is assigned to the tableView,
		# python will crash every time!
		# see the QHeaderView.ResizeMode docs for descriptions of each resize mode value
		# note QHeaderView.setResizeMode is deprecated in 5.4, replaced with
		# .setSectionResizeMode but also has both global and column-index forms
		# NOTE also - do NOT set any to ResizeToContents - this slows things down a lot!
		#  only resize when needed!
		self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
		# automatically expand the 'message' column width to fill available space
		self.ui.tableView.horizontalHeader().setSectionResizeMode(3,QHeaderView.Stretch)

		self.ui.datumFormatLabel.setText(self.datum+"\n"+self.coordFormat)
		self.updateClock()

		self.fsLoadLookup(startupFlag=True)

		self.teamTimer=QTimer(self)
		self.teamTimer.timeout.connect(self.updateTeamTimers)
		self.teamTimer.timeout.connect(self.fsCheck)
		self.teamTimer.timeout.connect(self.updateClock)
		self.teamTimer.start(1000)

		self.fastTimer=QTimer(self)
		self.fastTimer.timeout.connect(self.resizeRowsToContentsIfNeeded)
		self.fastTimer.start(100)

		self.logTimer=QTimer(self)
		self.logTimer.timeout.connect(writeLogBuffer)
		self.logTimer.start(5000)

		self.optionsDialog.ui.datumField.setCurrentIndex(self.optionsDialog.ui.datumField.findText(self.datum))
		self.optionsDialog.ui.formatField.setCurrentIndex(self.optionsDialog.ui.formatField.findText(self.coordFormat))
		self.timeoutDisplaySecList=[i[1] for i in timeoutDisplayList]
		self.optionsDialog.ui.timeoutField.setValue(self.timeoutDisplaySecList.index(int(self.timeoutRedSec)))

		self.ui.tabWidget.insertTab(0,QWidget(),'TEAMS:')
##		self.ui.tabWidget.setStyleSheet("font-size:12px")
		self.ui.tabWidget.setTabEnabled(0,False)

		self.ui.tabWidget.setContextMenuPolicy(Qt.CustomContextMenu)
		self.ui.tabWidget.customContextMenuRequested.connect(self.tabContextMenu)

		self.newEntryWindow=newEntryWindow(self) # create the window but don't show it until needed

		# load resource file; process default values and resource file values
		self.rcFileName="radiolog_rc.txt"
		self.previousCleanShutdown=self.loadRcFile()
		if not self.previousCleanShutdown:
			self.reallyRestore=QMessageBox.critical(self,"Restore last saved files?","The previous Radio Log session may have shut down incorrectly.  Do you want to restore the last saved files (Radio Log, Clue Log, and FleetSync table)?",
				QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
			if self.reallyRestore==QMessageBox.Yes:
				self.restore()

		# make sure x/y/w/h from resource file will fit on the available display
		d=QApplication.desktop()
		if (self.x+self.w > d.width()) or (self.y+self.h > d.height()):
			rprint("\nThe resource file specifies a main window geometry that is\n  bigger than (or not on) the available desktop.\n  Using default sizes for this session.\n\n")
			self.x=50
			self.y=50
			self.w=d.availableGeometry(self).width()-100
			self.h=d.availableGeometry(self).height()-100
		if (self.clueLog_x+self.clueLog_w > d.width()) or (self.clueLog_y+self.clueLog_h > d.height()):
			rprint("\nThe resource file specifies a clue log window geometry that is\n  bigger than (or not on) the available desktop.\n  Using default sizes for this session.\n\n")
			self.clueLog_x=75
			self.clueLog_y=75
			self.clueLog_w=d.availableGeometry(self).width()-100
			self.clueLog_h=d.availableGeometry(self).height()-100
		self.setGeometry(int(self.x),int(self.y),int(self.w),int(self.h))
		self.clueLogDialog.setGeometry(int(self.clueLog_x),int(self.clueLog_y),int(self.clueLog_w),int(self.clueLog_h))
		self.fontsChanged()

		self.ui.timeoutLabel.setText("TIMEOUT:\n"+timeoutDisplayList[self.optionsDialog.ui.timeoutField.value()][0])
		# pop up the options dialog to enter the incident name right away
		QTimer.singleShot(1000,self.startupOptions)
		# save current resource file, to capture lastFileName without a clean shutdown
		self.saveRcFile()

	def setColumnResizedFlag(self):
		self.columnResizedFlag=True

	def resizeRowsToContentsIfNeeded(self):
		if self.columnResizedFlag and not self.loadFlag:
			self.columnResizedFlag=False
			self.ui.tableView.resizeRowsToContents()
			self.ui.tableView.scrollToBottom()
			for n in self.ui.tableViewList[1:]:
				n.resizeRowsToContents()

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
		if not (self.firstComPortFound and self.secondComPortFound): # correct com ports not yet found; scan for waiting fleetsync data
			if not self.comPortScanInProgress: # but not if this scan is already in progress (taking longer than 1 second)
				if comLog:
					rprint("Two COM ports not yet found.  Scanning...")
				self.comPortScanInProgress=True
				# opening a port quickly, checking for waiting input, and closing on each iteration does not work; the
				#  com port must be open when the input begins, in order to catch it in the inWaiting internal buffer.
				# 1. go through each already-open com port to check for waiting data; if valid Fleetsync data is
				#     found, then we have the correct com port, abort the rest of the scan
				# 2. (only if no valid data was found in step 1) list com ports; open any new finds and close any
				#     stale ports (i.e. existed in the list in previous iterations but not in the list now)
				for comPortTry in self.comPortTryList:
					if comLog:
						rprint("  Checking buffer for already-open port "+comPortTry.name)
					try:
						isWaiting=comPortTry.inWaiting()
					except:
						pass
					else:
						if isWaiting:
							rprint("     DATA IS WAITING!!!")
							tmpData=comPortTry.read(comPortTry.inWaiting()).decode("utf-8")
							if '\x02I' in tmpData:
								rprint("      VALID FLEETSYNC DATA!!!")
								self.fsBuffer=self.fsBuffer+tmpData

								if not self.firstComPortFound:
									self.firstComPort=comPortTry # pass the actual open com port object, to keep it open
									self.firstComPortFound=True
								else:
									self.secondComPort=comPortTry # pass the actual open com port object, to keep it open
									self.secondComPortFound=True
								self.comPortTryList.remove(comPortTry) # and remove the good com port from the list of ports to try going forward
							else:
								rprint("      but not valid fleetsync data.  Scan continues...")
						else:
							if comLog:
								rprint("     no data")
				for portIterable in serial.tools.list_ports.comports():
					if portIterable[0] not in [x.name for x in self.comPortTryList]:
						try:
							self.comPortTryList.append(serial.Serial(portIterable[0]))
						except:
							pass
						else:
							rprint("  Opened newly found port "+portIterable[0])
							if self.firstComPortAlive:
								self.secondComPortAlive=True
							else:
								self.firstComPortAlive=True
				self.comPortScanInProgress=False
##		else: # com port already found; read data normally
		# read data and process buffer even if both com ports aren't yet found, i.e. if only one is found

		if self.firstComPortAlive:
			self.ui.firstComPortField.setStyleSheet("background-color:#00bb00")
		else:
			self.ui.firstComPortField.setStyleSheet("background-color:#aaaaaa")
		if self.secondComPortAlive:
			self.ui.secondComPortField.setStyleSheet("background-color:#00bb00")
		else:
			self.ui.secondComPortField.setStyleSheet("background-color:#aaaaaa")
			
		# fixed issue 41: handle USB hot-unplug case, in which port scanning resumes;
		#  note that hot-plug takes 5 seconds or so to be recognized
		if self.firstComPortFound:
# 			self.ui.firstComPortField.setStyleSheet("background-color:#00bb00")
			waiting=0
			try:
				waiting=self.firstComPort.inWaiting()
			except serial.serialutil.SerialException as err:
				if str(err)=="call to ClearCommError failed":
					rprint("first com port unplugged")
					self.firstComPortFound=False
					self.firstComPortAlive=False
					self.ui.firstComPortField.setStyleSheet("background-color:#bb0000")
			if waiting:
				self.ui.firstComPortField.setStyleSheet("background-color:#00ff00")
				self.fsBuffer=self.fsBuffer+self.firstComPort.read(waiting).decode('utf-8')
		if self.secondComPortFound:
# 			self.ui.secondComPortField.setStyleSheet("background-color:#00bb00")
			waiting=0
			try:
				waiting=self.secondComPort.inWaiting()
			except serial.serialutil.SerialException as err:
				if str(err)=="call to ClearCommError failed":
					rprint("second com port unplugged")
					self.secondComPortFound=False
					self.secondComPortAlive=False
					self.ui.secondComPortField.setStyleSheet("background-color:#bb0000")
			if waiting:
				self.ui.secondComPortField.setStyleSheet("background-color:#00ff00")
				self.fsBuffer=self.fsBuffer+self.secondComPort.read(waiting).decode('utf-8')

		if self.fsBuffer.endswith("\x03"):
			self.fsParse()
			self.fsBuffer=""

	def fsParse(self):
		rprint("PARSING")
		rprint(self.fsBuffer)
		origLocString=''
		formattedLocString=''
		callsign=''
		self.getString=''
		sec=time.time()
		# the line delimeters are literal backslash then n, rather than standard \n
		for line in self.fsBuffer.split('\n'):
			rprint(" line:"+line)
			if '$PKLSH' in line:
				[pklsh,nval,nstr,wval,wstr,utc,valid,fleet,dev,chksum]=line.split(',')
				callsign=self.getCallsign(fleet,dev)
				if valid=='A':  # only process if there is a GPS lock
#				if valid!='Z':  # process regardless of GPS lock
					locList=[nval,nstr,wval,wstr]
					origLocString='|'.join(locList) # don't use comma, that would conflict with CSV delimeter
					rprint("Valid location string:'"+origLocString+"'")
					formattedLocString=self.convertCoords(locList,self.datum,self.coordFormat)
					rprint("Formatted location string:'"+formattedLocString+"'")
					[lat,lon]=self.convertCoords(locList,targetDatum="WGS84",targetFormat="D.dList")
					rprint("WGS84 lat="+str(lat)+"  lon="+str(lon))
					# sarsoft requires &id=FLEET:<fleet#>-<deviceID>
					#  fleet# must match the locatorGroup fleet number in sarsoft
					#  but deviceID can be any text; use the callsign to get useful names in sarsoft
					if callsign.startswith("KW-"):
                   # did not find a good callsign; use the device number in the GET request
						devTxt=dev
					else:
						# found a good callsign; use the callsign in the GET request
						devTxt=callsign
					self.getString="http://"+self.sarsoftServerName+":8080/rest/location/update/position?lat="+str(lat)+"&lng="+str(lon)+"&id=FLEET:"+fleet+"-"
					# if callsign = "Radio ..." then leave the getString ending with hyphen for now, as a sign to defer
					#  sending until accept of change callsign dialog, or closeEvent of newEntryWidget, whichever comes first;
					#  otherwise, append the callsign now, as a sign to send immediately
					if not devTxt.startswith("Radio "):
						self.getString=self.getString+devTxt
				else:
					origLocString='NO FIX'
					formattedLocString='NO FIX'
			elif '\x02I' in line:
				fleet=line[3:6]
				dev=line[6:10]
				callsign=self.getCallsign(fleet,dev)
		# if any new entry dialogs are already open with 'from' and the
		#  current callsign, and that entry has been edited within the 'continue' time,
		#  update it with the current location if available;
		# otherwise, spawn a new entry dialog
		found=False
		for widget in newEntryWidget.instances:
##			rprint("checking against existing widget: to_from="+widget.ui.to_fromField.currentText()" team="+widget.ui.teamField.text()
			if widget.ui.to_fromField.currentText()=="FROM" and widget.ui.teamField.text()==callsign and widget.lastModAge<continueSec:
##				widget.timer.start(newEntryDialogTimeoutSeconds*1000) # reset the timeout
				found=True
##				if origLocString!='' and origLocString!='NO FIX':  # don't overwrite location if earlier transmission had a good lock
				prevLocString=widget.ui.radioLocField.text()
				# if previous location string was blank, always overwrite;
				#  if previous location string was not blank, only overwrite if new location is valid
				if prevLocString=='' or (formattedLocString!='' and formattedLocString!='NO FIX'):
					widget.ui.radioLocField.setText(formattedLocString)
					widget.ui.datumFormatLabel.setText("("+self.datum+"  "+self.coordFormat+")")
					widget.formattedLocString=formattedLocString
					widget.origLocString=origLocString
		# only open a new entry widget if the fleet/dev is not being filtered
		if not found and not self.fsIsFiltered(fleet,dev):
			self.openNewEntry(None,callsign,formattedLocString,fleet,dev,origLocString)
		self.sendPendingGet()

	def sendPendingGet(self,suffix=""):
		# NOTE that requests.get can cause a blocking delay; so, do it AFTER spawning the newEntryDialog
		# if sarsoft is not running to handle this get request, Windows will complain with nested exceptions:
		# ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it
		# During handling of the above exception, another exception occurred:
		# requests.packages.urllib3.exceptions.ProtocolError: ('Connection aborted.', ConnectionRefusedError(10061, 'No connection could be made because the target machine actively refused it', None, 10061, None))
		# but we don't care about these; pass them silently

		# also, if it ends in hyphen, defer sending until accept of change callsign dialog, or closeEvent of newEntryDialog
		#  (see getString construction comments above)
		if not noSend:
			if self.getString!='': # to avoid sending a GET string that is nothing but the callsign
				self.getString=self.getString+suffix
			if self.getString!='' and not self.getString.endswith("-"):
				QCoreApplication.processEvents()
				try:
					rprint("Sending GET request:")
					rprint(self.getString)
					requests.get(self.getString)
				except:
					pass
				self.getString=''

	def fsIsFiltered(self,fleet,dev):
		rprint("fleet="+fleet+" dev="+dev)
		# invalid fleets are always filtered, to prevent fleet-glitches (110-xxxx) from opening new entries
		if int(fleet) not in self.fsValidFleetList:
			rprint("true1")
			return True
		# if the fleet is valid, check for filtered device ID
		if int(dev) in self.fsFilteredDevList:
			rprint("true2")
			return True
		rprint("false1")
		return False

	def fsLoadLookup(self,startupFlag=False,fsFileName=None):
		if not startupFlag and not fsFileName: # don't ask for confirmation on startup or on restore
			really=QMessageBox.warning(self,'Please Confirm','Are you sure you want to reload the default FleetSync lookup table?  This will overwrite any callsign changes you have made.',
				QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
			if really==QMessageBox.No:
				return
		fsEmptyFlag=False
		if len(self.fsLookup)==0:
			fsEmptyFlag=True
		if not fsFileName:
			fsFileName=self.fsFileName
		try:
			rprint("Loading FleetSync Lookup Table from file "+fsFileName)
			with open(fsFileName,'r') as fsFile:
				self.fsLookup=[]
				csvReader=csv.reader(fsFile)
				for row in csvReader:
					if not row[0].startswith("#"):
						self.fsLookup.append(row)
				if not startupFlag: # suppress message box on startup
					self.fsMsgBox=QMessageBox(QMessageBox.Information,"Information","FleetSync ID table has been re-loaded from file "+self.fsFileName+".")
					self.fsMsgBox.show()
					QCoreApplication.processEvents()
					QTimer.singleShot(2000,self.fsMsgBox.close)
		except:
			if fsEmptyFlag:
				QMessageBox.warning(self,"Warning","Cannot read FleetSync ID table file "+fsFileName+" and no FleetSync ID table has yet been loaded.  Callsigns for incoming FleetSync calls will be of the format 'KW-<fleet>-<device>'.")
			else:
				QMessageBox.warning(self,"Warning","Cannot read FleetSync ID table file "+fsFileName+"!  Using existing settings.")

	# save to fsFileName in the working dir each time, but on startup, load from the default dir;
	#  would only need to load from the working dir if restoring
	def fsSaveLookup(self):
		fsName=self.firstWorkingDir+"\\"+self.csvFileName
		fsName=fsName.replace(".csv","_fleetsync.csv")
		try:
			with open(fsName,'w',newline='') as fsFile:
				rprint("Writing file "+fsName)
				csvWriter=csv.writer(fsFile)
				csvWriter.writerow(["## Radio Log FleetSync lookup table"])
				csvWriter.writerow(["## File written "+time.strftime("%a %b %d %Y %H:%M:%S")])
				csvWriter.writerow(["## Created during Incident Name: "+self.incidentName])
				for row in self.fsLookup:
					csvWriter.writerow(row)
				csvWriter.writerow(["## end"])
		except:
			QMessageBox.warning(self,"Warning","Cannot write FleetSync ID table file "+fsName+"!  Any modified FleetSync Callsign associations will be lost.")

	def getCallsign(self,fleet,dev):
		entry=[element for element in self.fsLookup if (element[0]==fleet and element[1]==dev)]
		if len(entry)!=1 or len(entry[0])!=3: # no match
			return "KW-"+str(fleet)+"-"+str(dev)
		else:
			return entry[0][2]

	def getFleetDev(self,callsign):
		entry=[element for element in self.fsLookup if (element[2]==callsign)]
		if len(entry)!=1: # no match
			return False
		else:
			return [entry[0][0],entry[0][1]]

	def testConvertCoords(self):
		coordsTestList=[
			['3918.9200','N','11955.2100','W'],
			['3918.9200','N','12055.2100','W'],
			['3918.9200','N','12155.2100','W'],
			['3918.9200','N','11959.9900','W'],
			['3918.9200','N','12000.0000','W'],
			['3918.9200','N','12000.0100','W'],
			['3830.0000','N','12130.0000','W'],
			['3830.0000','N','12115.0000','W'],
			['3830.0000','N','12100.0000','W'],
			['3830.0000','N','12045.0000','W'],
			['3830.0000','N','12030.0000','W'],
			['3830.0000','N','12015.0000','W'],
			['3830.0000','N','12000.0000','W'],
			['3830.0000','N','11945.0000','W'],
			['3830.0000','N','11930.0000','W'],
			['3830.0000','N','11915.0000','W'],
			['3830.0000','N','11900.0000','W'],
			['3845.0000','N','12130.0000','W'],
			['3845.0000','N','12115.0000','W'],
			['3845.0000','N','12100.0000','W'],
			['3845.0000','N','12045.0000','W'],
			['3845.0000','N','12030.0000','W'],
			['3845.0000','N','12015.0000','W'],
			['3845.0000','N','12000.0000','W'],
			['3845.0000','N','11945.0000','W'],
			['3845.0000','N','11930.0000','W'],
			['3845.0000','N','11915.0000','W'],
			['3845.0000','N','11900.0000','W'],
			['3900.0000','N','12130.0000','W'],
			['3900.0000','N','12115.0000','W'],
			['3900.0000','N','12100.0000','W'],
			['3900.0000','N','12045.0000','W'],
			['3900.0000','N','12030.0000','W'],
			['3900.0000','N','12015.0000','W'],
			['3900.0000','N','12000.0000','W'],
			['3900.0000','N','11945.0000','W'],
			['3900.0000','N','11930.0000','W'],
			['3900.0000','N','11915.0000','W'],
			['3900.0000','N','11900.0000','W'],
			['3915.0000','N','12130.0000','W'],
			['3915.0000','N','12115.0000','W'],
			['3915.0000','N','12100.0000','W'],
			['3915.0000','N','12045.0000','W'],
			['3915.0000','N','12030.0000','W'],
			['3915.0000','N','12015.0000','W'],
			['3915.0000','N','12000.0000','W'],
			['3915.0000','N','11945.0000','W'],
			['3915.0000','N','11930.0000','W'],
			['3915.0000','N','11915.0000','W'],
			['3915.0000','N','11900.0000','W'],
			['3930.0000','N','12130.0000','W'],
			['3930.0000','N','12115.0000','W'],
			['3930.0000','N','12100.0000','W'],
			['3930.0000','N','12045.0000','W'],
			['3930.0000','N','12030.0000','W'],
			['3930.0000','N','12015.0000','W'],
			['3930.0000','N','12000.0000','W'],
			['3930.0000','N','11945.0000','W'],
			['3930.0000','N','11930.0000','W'],
			['3930.0000','N','11915.0000','W'],
			['3930.0000','N','11900.0000','W'],
			['3945.0000','N','12130.0000','W'],
			['3945.0000','N','12115.0000','W'],
			['3945.0000','N','12100.0000','W'],
			['3945.0000','N','12045.0000','W'],
			['3945.0000','N','12030.0000','W'],
			['3945.0000','N','12015.0000','W'],
			['3945.0000','N','12000.0000','W'],
			['3945.0000','N','11945.0000','W'],
			['3945.0000','N','11930.0000','W'],
			['3945.0000','N','11915.0000','W'],
			['3945.0000','N','11900.0000','W'],
			['4000.0000','N','12130.0000','W'],
			['4000.0000','N','12115.0000','W'],
			['4000.0000','N','12100.0000','W'],
			['4000.0000','N','12045.0000','W'],
			['4000.0000','N','12030.0000','W'],
			['4000.0000','N','12015.0000','W'],
			['4000.0000','N','12000.0000','W'],
			['4000.0000','N','11945.0000','W'],
			['4000.0000','N','11930.0000','W'],
			['4000.0000','N','11915.0000','W'],
			['4000.0000','N','11900.0000','W']]

		for coords in coordsTestList:
			rval=self.convertCoords(coords,self.datum,self.coordFormat)
			rprint("testConvertCoords:"+str(coords)+" --> "+rval)

	def convertCoords(self,coords,targetDatum,targetFormat):
		easting="0000000"
		northing="0000000"
		rprint("convertCoords called: targetDatum="+targetDatum+" targetFormat="+targetFormat+" coords="+str(coords))
		# coords must be a parsed list of location data from fleetsync in NMEA format;
		# reformat the coords argument to the format needed by cs2cs
		if isinstance(coords,list):
			latDeg=int(coords[0][0:2]) # first two numbers are degrees
			latMin=float(coords[0][2:]) # remainder is minutes
			lonDeg=int(coords[2][0:3]) # first three numbers are degrees
			lonMin=float(coords[2][3:]) # remainder is minutes
			# add decimal portion of degrees here, before changing sign for hemisphere
			latDd=latDeg+latMin/60
			lonDd=lonDeg+lonMin/60
			if coords[1]=="S":
				latDeg=-latDeg # invert if needed
				ladDd=-latDd
			if coords[3]=="W":
				rprint("inverting longitude")
				lonDeg=-lonDeg # invert if needed
				lonDd=-lonDd
##			targetUTMZone=int(lonDeg/6)+30 # do the math: -179.99999deg -> -174deg = zone 1; -173.99999deg -> -168deg = zone 2, etc
			targetUTMZone=math.floor((lonDd+180)/6)+1 # from http://stackoverflow.com/questions/9186496, since -120.0000deg should be zone 11, not 10
			rprint("lonDeg="+str(lonDeg)+" lonDd="+str(lonDd)+" targetUTMZone="+str(targetUTMZone))
			#cs2cs wants longitude first: -121d1' 39d15' works, but 39d15' -121d1' gives an error
			latlon_cs2cs="{}d{}' {}d{}'".format(lonDeg,lonMin,latDeg,latMin)
			rprint("Formatted coordinates:"+latlon_cs2cs)
		else:
			return("INVALID INPUT FORMAT - MUST BE A LIST")

		# if target datum is WGS84 and target format is anything other than UTM, just do the math,
		# it's quicker than calling cs2cs; otherwise, call cs2cs
		if targetDatum!="WGS84" or targetFormat=="UTM":
			sdkShellBat=self.GISInternalsSDKRoot+"\\SDKShell.bat setenv" # must do 'setenv' as argument, otherwise command will terminate; see SDKShell.bat
			cs2csExe=self.GISInternalsSDKRoot+"\\bin\\proj\\apps\\cs2cs.exe"

			if targetDatum=="WGS84" and targetFormat=="UTM":
				targetProj4="+init=EPSG:326{0:02d}".format(targetUTMZone) # EPSG:32610 = WGS84 UTM zone 10N, 32611 = zone 11, etc
			elif targetDatum=="NAD27 CONUS":
				if targetFormat=="UTM":
					targetProj4="+init=EPSG:267{0:02d}".format(targetUTMZone) # EPSG:26710 = NAD27 UTM zone 10N, 26711 = zone 11, etc
				else:
					targetProj4="+proj=latlong +init=EPSG:4267"
			else:
				targetProj4="+proj=latlong +init=EPSG:4326" # fallback to WGS84 latlong

			cs2csArgs="+proj=latlong +init=EPSG:4326 +to "+targetProj4 # assume source is WGS84 latlong

			cmd=sdkShellBat+" & "+cs2csExe+" -f \"%.6f\" "+cs2csArgs # format is not needed for UTM but is needed to return decimal degrees
			rprint(cmd)

			cs2cs=subprocess.check_output(cmd,universal_newlines=True,stderr=subprocess.STDOUT,input=latlon_cs2cs+'\n',timeout=5)
			for line in cs2cs.split("\n"):
				line=line.lstrip()
				rprint("LINE:"+line)
				if line!='' and line[1].isdigit(): # check the second character, in case the first is '-' (negative degrees)
					rprint("Found it:"+line)
					if targetFormat=="UTM":
						[easting,northing,junk]=line.split()
						easting=str(int(float(easting))).zfill(7)
						northing=str(int(float(northing))).zfill(7)
					else:
						[lonDd,latDd,junk]=line.split()

		latDd=float(latDd)
		latDeg=int(latDd)
		latMin=float((latDd-float(latDeg))*60.0)
		latSec=float((latMin-int(latMin))*60.0)
		lonDd=float(lonDd)
		if lonDd<0 and targetFormat!="D.dList": # leave it negative for D.dList
			lonDd=-lonDd
			lonLetter="W"
		else:
			lonLetter="E"
		lon=int(lonDd)
		lonMin=float((lonDd-float(lonDeg))*60.0)
		lonSec=float((lonMin-int(lonMin))*60.0)

		# return the requested format
		# desired accuracy / digits of precision:
		# at 39 degrees north,
		# 0.00001 degree latitude = 1.11 meters
		# 0.001 minute latutude = 1.85 meters
		# 0.1 second latitude = 3.08 meters
		# (longitude lengths are about 78% as much as latitude, at 39 degrees north)
		if targetFormat=="D.dList":
			return [latDd,lonDd]
		if targetFormat=="D.d°":
			return "{:.5f}°N, {:.5f}°{}".format(latDd,lonDd,lonLetter)
		if targetFormat=="D° M.m'":
			return "{}° {:.3f}'N, {}° {:.3f}'{}".format(latDeg,latMin,lonDeg,lonMin,lonLetter)
		if targetFormat=="D° M' S.s\"":
			return "{}° {}' {:.1f}\"N, {}° {}' {:.1f}\"{}".format(latDeg,int(latMin),latSec,lonDeg,int(lonMin),lonSec,lonLetter)
		if targetFormat=="UTM":
			return "{}  {}".format(easting[2:],northing[2:])
		return "INVALID - UNKNOWN OUTPUT FORMAT REQUESTED"

	def printLogHeaderFooter(self,canvas,doc,opPeriod="",teams=False):
		formNameText="Radio Log"
		if teams:
			formNameText="Team Radio Logs"
		canvas.saveState()
		styles = getSampleStyleSheet()
		self.img=None
		if os.path.isfile(self.printLogoFileName):
			imgReader=utils.ImageReader(self.printLogoFileName)
			imgW,imgH=imgReader.getSize()
			imgAspect=imgH/float(imgW)
			self.img=Image(self.printLogoFileName,width=0.54*inch/float(imgAspect),height=0.54*inch)
			headerTable=[
					[self.img,"NEVADA COUNTY SHERIFF'S\nSEARCH AND RESCUE","Incident: "+self.incidentName,formNameText+" - Page "+str(canvas.getPageNumber())],
					["","","Operational Period: "+str(opPeriod),"Printed: "+time.strftime("%a %b %d, %Y  %H:%M")]]
			t=Table(headerTable,colWidths=[x*inch for x in [0.8,4.2,2.5,2.5]],rowHeights=[x*inch for x in [0.3,0.3]])
			t.setStyle(TableStyle([('FONT',(1,0),(1,1),'Helvetica-Bold'),
										  ('FONT',(2,0),(3,0),'Helvetica-Bold'),
			                       ('FONTSIZE',(1,0),(1,1),18),
										  ('SPAN',(0,0),(0,1)),
										  ('SPAN',(1,0),(1,1)),
										  ('LEADING',(1,0),(1,1),20),
										  ('TOPADDING',(1,0),(1,0),0),
										  ('BOTTOMPADDING',(1,1),(1,1),4),
         	                    ('VALIGN',(0,0),(-1,-1),"MIDDLE"),
            	                 ('ALIGN',(1,0),(1,-1),"CENTER"),
										  ('ALIGN',(0,0),(0,1),"CENTER"),
										  ('BOX',(0,0),(-1,-1),2,colors.black),
										  ('BOX',(2,0),(-1,-1),2,colors.black),
										  ('INNERGRID',(2,0),(3,1),0.5,colors.black)]))
		else:
			headerTable=[
					[self.img,"NEVADA COUNTY SHERIFF'S\nSEARCH AND RESCUE","Incident: "+self.incidentName,formNameText+" - Page "+str(canvas.getPageNumber())],
					["","","Operational Period: ","Printed: "+time.strftime("%a %b %d, %Y  %H:%M")]]
			t=Table(headerTable,colWidths=[x*inch for x in [0.0,5,2.5,2.5]],rowHeights=[x*inch for x in [0.3,0.3]])
			t.setStyle(TableStyle([('FONT',(1,0),(1,1),'Helvetica-Bold'),
			                       ('FONT',(2,0),(3,0),'Helvetica-Bold'),
			                       ('FONTSIZE',(1,0),(1,1),18),
										  ('SPAN',(0,0),(0,1)),
										  ('SPAN',(1,0),(1,1)),
										  ('LEADING',(1,0),(1,1),20),
         	                    ('VALIGN',(1,0),(-1,-1),"MIDDLE"),
            	                 ('ALIGN',(1,0),(1,-1),"CENTER"),
										  ('BOX',(0,0),(-1,-1),2,colors.black),
										  ('BOX',(2,0),(-1,-1),2,colors.black),
										  ('INNERGRID',(2,0),(3,1),0.5,colors.black)]))
		w,h=t.wrapOn(canvas,doc.width,doc.height)
		self.msgBox.setInformativeText("Generating page "+str(canvas.getPageNumber()))
		QCoreApplication.processEvents()
		rprint("Page number:"+str(canvas.getPageNumber()))
		rprint("Height:"+str(h))
		rprint("Pagesize:"+str(doc.pagesize))
		t.drawOn(canvas,doc.leftMargin,doc.pagesize[1]-h-0.5*inch) # enforce a 0.5 inch top margin regardless of paper size
##		canvas.grid([x*inch for x in [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11]],[y*inch for y in [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5]])
		canvas.restoreState()

	# optonal argument 'teams': if True, generate one pdf of all individual team logs;
	#  so, this function should be called once to generate the overall log pdf, and
	#  again with teams=True to generate team logs pdf
	def printLog(self,opPeriod,teams=False):
		opPeriod=int(opPeriod)
		pdfName=self.firstWorkingDir+"\\"+self.pdfFileName
		if teams:
			pdfName=pdfName.replace('.pdf','_teams.pdf')
		pdfName=pdfName.replace('.pdf','_OP'+str(opPeriod)+'.pdf')
		rprint("generating radio log pdf: "+pdfName)
		try:
			f=open(pdfName,"wb")
		except:
			QMessageBox.critical(self,"Error","PDF could not be generated.  Maybe the file is currently being viewed by another program?  If so, please close that viewer and try again.  As a last resort, the auto-saved CSV file can be printed from Excel or as a plain text file.")
			return
		else:
			f.close()
		if teams:
			msgAdder=" for individual teams"
		else:
			msgAdder=""
		self.msgBox=QMessageBox(QMessageBox.Information,"Printing","Generating PDF"+msgAdder+"; will send to default printer automatically; please wait...",QMessageBox.Abort)
		self.msgBox.setInformativeText("Initializing...")
		# note the topMargin is based on what looks good; you would think that a 0.6 table plus a 0.5 hard
		# margin (see t.drawOn above) would require a 1.1 margin here, but, not so.
		doc = SimpleDocTemplate(pdfName, pagesize=landscape(letter),leftMargin=0.5*inch,rightMargin=0.5*inch,topMargin=1.03*inch,bottomMargin=0.5*inch) # or pagesize=letter
		self.msgBox.show()
		QCoreApplication.processEvents()
		elements=[]
		teamFilterList=[""] # by default, print print all entries; if teams=True, add a filter for each team
		if teams:
			teamFilterList=[]
			for team in self.allTeamsList:
				if team!="dummy":
					teamFilterList.append(team)
		rprint("teamFilterList="+str(teamFilterList))
		for team in teamFilterList:
			radioLogPrint=[]
			styles = getSampleStyleSheet()
			radioLogPrint.append(MyTableModel.header_labels[0:6])
##			if teams and opPeriod==1: # if request op period = 1, include 'Radio Log Begins' in all team tables
##				radioLogPrint.append(self.radioLog[0])
			entryOpPeriod=1 # update this number when 'Operational Period <x> Begins' lines are found
##			hits=False # flag to indicate whether this team has any entries in the requested op period; if not, don't make a table for this team
			for row in self.radioLog:
				opStartRow=False
##				rprint("message:"+row[3]+":"+str(row[3].split()))
				if row[3].startswith("Radio Log Begins:"):
					opStartRow=True
				if row[3].startswith("Operational Period") and row[3].split()[3] == "Begins:":
					opStartRow=True
					entryOpPeriod=int(row[3].split()[2])
##				rprint("desired op period="+str(opPeriod)+"; this entry op period="+str(entryOpPeriod))
				if entryOpPeriod == opPeriod:
##					rprint("hit")
					if team=="" or team.lower()==row[2].lower() or opStartRow: # filter by team name if argument was specified
						radioLogPrint.append([row[0],row[1],row[2],Paragraph(row[3],styles['Normal']),Paragraph(row[4],styles['Normal']),Paragraph(row[5],styles['Normal'])])
##						hits=True
			if not teams:
				radioLogPrint[1][4]=self.datum
			rprint("length:"+str(len(radioLogPrint)))
			if not teams or len(radioLogPrint)>2: # don't make a table for teams that have no entries during the requested op period
				t=Table(radioLogPrint,repeatRows=1,colWidths=[x*inch for x in [0.5,0.6,1.25,5.5,1.25,0.9]])
				t.setStyle(TableStyle([('FONT',(0,0),(-1,-1),'Helvetica'),
					                    ('FONT',(0,0),(-1,1),'Helvetica-Bold'),
					                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
			      	                 ('BOX', (0,0), (-1,-1), 2, colors.black),
			         	              ('BOX', (0,0), (5,0), 2, colors.black)]))
				elements.append(t)
				if teams and team!=teamFilterList[-1]: # don't add a spacer after the last team - it could cause another page!
					elements.append(Spacer(0,0.25*inch))
		doc.build(elements,onFirstPage=functools.partial(self.printLogHeaderFooter,opPeriod=opPeriod,teams=teams),onLaterPages=functools.partial(self.printLogHeaderFooter,opPeriod=opPeriod,teams=teams))
		self.msgBox.setInformativeText("Finalizing and Printing...")
		QTimer.singleShot(5000,self.msgBox.close)
		win32api.ShellExecute(0,"print",pdfName,'/d:"%s"' % win32print.GetDefaultPrinter(),".",0)
		self.radioLogNeedsPrint=False
		if os.path.isdir(self.secondWorkingDir):
			rprint("copying radio log pdf"+msgAdder+" to "+self.secondWorkingDir)
			shutil.copy(pdfName,self.secondWorkingDir)

	def printTeamLogs(self,opPeriod):
		self.printLog(opPeriod,teams=True)

	def printClueLogHeaderFooter(self,canvas,doc,opPeriod=""):
		canvas.saveState()
		styles = getSampleStyleSheet()
		self.img=None
		if os.path.isfile(self.printLogoFileName):
			imgReader=utils.ImageReader(self.printLogoFileName)
			imgW,imgH=imgReader.getSize()
			imgAspect=imgH/float(imgW)
			self.img=Image(self.printLogoFileName,width=0.54*inch/float(imgAspect),height=0.54*inch)
			headerTable=[
					[self.img,"NEVADA COUNTY SHERIFF'S\nSEARCH AND RESCUE","Incident: "+self.incidentName,"Clue Log - Page "+str(canvas.getPageNumber())],
					["","","Operational Period: "+str(opPeriod),"Printed: "+time.strftime("%a %b %d, %Y  %H:%M")]]
			t=Table(headerTable,colWidths=[x*inch for x in [0.8,4.2,2.5,2.5]],rowHeights=[x*inch for x in [0.3,0.3]])
			t.setStyle(TableStyle([('FONT',(1,0),(1,1),'Helvetica-Bold'),
			                       ('FONTSIZE',(1,0),(1,1),18),
										  ('SPAN',(0,0),(0,1)),
										  ('SPAN',(1,0),(1,1)),
										  ('LEADING',(1,0),(1,1),20),
										  ('TOPADDING',(1,0),(1,0),0),
										  ('BOTTOMPADDING',(1,1),(1,1),4),
         	                    ('VALIGN',(0,0),(-1,-1),"MIDDLE"),
            	                 ('ALIGN',(1,0),(1,-1),"CENTER"),
										  ('ALIGN',(0,0),(0,1),"CENTER"),
										  ('BOX',(0,0),(-1,-1),2,colors.black),
										  ('BOX',(2,0),(-1,-1),2,colors.black),
										  ('INNERGRID',(2,0),(3,1),0.5,colors.black)]))
		else:
			headerTable=[
					[self.img,"NEVADA COUNTY SHERIFF'S\nSEARCH AND RESCUE","Incident: "+self.incidentName,"Clue Log - Page "+str(canvas.getPageNumber())],
					["","","Operational Period: "+str(opPeriod),"Printed: "+time.strftime("%a %b %d, %Y  %H:%M")]]
			t=Table(headerTable,colWidths=[x*inch for x in [0.0,5,2.5,2.5]],rowHeights=[x*inch for x in [0.3,0.3]])
			t.setStyle(TableStyle([('FONT',(1,0),(1,1),'Helvetica-Bold'),
			                       ('FONTSIZE',(1,0),(1,1),18),
										  ('SPAN',(0,0),(0,1)),
										  ('SPAN',(1,0),(1,1)),
										  ('LEADING',(1,0),(1,1),20),
         	                    ('VALIGN',(1,0),(-1,-1),"MIDDLE"),
            	                 ('ALIGN',(1,0),(1,-1),"CENTER"),
										  ('BOX',(0,0),(-1,-1),2,colors.black),
										  ('BOX',(2,0),(-1,-1),2,colors.black),
										  ('INNERGRID',(2,0),(3,1),0.5,colors.black)]))
		w,h=t.wrapOn(canvas,doc.width,doc.height)
		self.msgBox.setInformativeText("Generating page "+str(canvas.getPageNumber()))
		QCoreApplication.processEvents()
		rprint("Page number:"+str(canvas.getPageNumber()))
		rprint("Height:"+str(h))
		rprint("Pagesize:"+str(doc.pagesize))
		t.drawOn(canvas,doc.leftMargin,doc.pagesize[1]-h-0.5*inch) # enforce a 0.5 inch top margin regardless of paper size
##		canvas.grid([x*inch for x in [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11]],[y*inch for y in [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5]])
		canvas.restoreState()

	def printClueLog(self,opPeriod):
##      header_labels=['#','DESCRIPTION','TEAM','TIME','DATE','O.P.','LOCATION','INSTRUCTIONS','RADIO LOC.']
		opPeriod=int(opPeriod)
		clueLogPdfFileName=self.firstWorkingDir+"\\"+self.pdfFileName.replace(".pdf","_clueLog_OP"+str(opPeriod)+".pdf")
		rprint("generating clue log pdf: "+clueLogPdfFileName)
		try:
			f=open(clueLogPdfFileName,"wb")
		except:
			QMessageBox.critical(self,"Error","PDF could not be generated.  Maybe the file is currently being viewed by another program?  If so, please close that viewer and try again.  As a last resort, the auto-saved CSV file can be printed from Excel or as a plain text file.")
			return
		else:
			f.close()
		self.msgBox=QMessageBox(QMessageBox.Information,"Printing","Generating PDF; will send to default printer automatically; please wait...",QMessageBox.Abort)
		self.msgBox.setInformativeText("Initializing...")
		# note the topMargin is based on what looks good; you would think that a 0.6 table plus a 0.5 hard
		# margin (see t.drawOn above) would require a 1.1 margin here, but, not so.
		doc = SimpleDocTemplate(clueLogPdfFileName, pagesize=landscape(letter),leftMargin=0.5*inch,rightMargin=0.5*inch,topMargin=1.03*inch,bottomMargin=0.5*inch) # or pagesize=letter
		self.msgBox.show()
		QCoreApplication.processEvents()
		elements=[]
		styles = getSampleStyleSheet()
		clueLogPrint=[]
		clueLogPrint.append(clueTableModel.header_labels[0:5]+clueTableModel.header_labels[6:8]) # omit operational period
		for row in self.clueLog:
			rprint("clue: opPeriod="+str(opPeriod)+"; row="+str(row))
			if (str(row[5])==str(opPeriod) or row[1].startswith("Operational Period "+str(opPeriod)+" Begins:") or (opPeriod==1 and row[1].startswith("Radio Log Begins:"))):
				clueLogPrint.append([row[0],Paragraph(row[1],styles['Normal']),row[2],row[3],row[4],Paragraph(row[6],styles['Normal']),Paragraph(row[7],styles['Normal'])])
		clueLogPrint[1][5]=self.datum
		if len(clueLogPrint)>2:
##			t=Table(clueLogPrint,repeatRows=1,colWidths=[x*inch for x in [0.6,3.75,.9,0.5,1.25,3]])
			t=Table(clueLogPrint,repeatRows=1,colWidths=[x*inch for x in [0.3,3.75,0.9,0.5,0.8,1.25,2.5]])
			t.setStyle(TableStyle([('FONT',(0,0),(-1,-1),'Helvetica'),
				                    ('FONT',(0,0),(-1,1),'Helvetica-Bold'),
				                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
			                       ('BOX', (0,0), (-1,-1), 2, colors.black),
			                       ('BOX', (0,0), (6,0), 2, colors.black)]))
			elements.append(t)
			doc.build(elements,onFirstPage=functools.partial(self.printClueLogHeaderFooter,opPeriod=opPeriod),onLaterPages=functools.partial(self.printClueLogHeaderFooter,opPeriod=opPeriod))
			self.msgBox.setInformativeText("Finalizing and Printing...")
			QTimer.singleShot(5000,self.msgBox.close)
			win32api.ShellExecute(0,"print",clueLogPdfFileName,'/d:"%s"' % win32print.GetDefaultPrinter(),".",0)
			if os.path.isdir(self.secondWorkingDir):
				rprint("copying clue log pdf to "+self.secondWorkingDir)
				shutil.copy(clueLogPdfFileName,self.secondWorkingDir)
		else:
			self.msgBox.close()
			self.msgBox=QMessageBox(QMessageBox.Information,"Printing","No clues were logged during Operational Period "+str(opPeriod)+"; no clue log will be printed.",QMessageBox.Ok)
			QTimer.singleShot(500,self.msgBox.show)
		self.clueLogNeedsPrint=False

	def printClueReport(self,clueData):
##		header_labels=['#','DESCRIPTION','TEAM','TIME','DATE','O.P.','LOCATION','INSTRUCTIONS','RADIO LOC.']
		# do not use ui object here, since this could be called later, when the clueDialog is not open
		cluePdfName=self.firstWorkingDir+"\\"+self.pdfFileName.replace(".pdf","_clue"+str(clueData[0]).zfill(2)+".pdf")
		rprint("generating clue report pdf: "+cluePdfName)
		clueFdfName=cluePdfName.replace(".pdf",".fdf")

		self.msgBox=QMessageBox(QMessageBox.Information,"Printing Clue #"+clueData[0],"Generating PDF; will send to default printer automatically; please wait...",QMessageBox.Abort)
		self.msgBox.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.msgBox.show()
		self.msgBox.raise_()
		QTimer.singleShot(5000,self.msgBox.close)

		instructions=clueData[7].lower()
		# initialize all checkboxes to OFF
		instructionsCollect=False
		instructionsMarkAndLeave=False
		instructionsDisregard=False
		instructionsOther=False
		# look for keywords in the instructions text
		if "collect" in instructions:
			instructionsCollect=True
		if "mark & leave" in instructions:
			instructionsMarkAndLeave=True
		if "disregard" in instructions:
			instructionsDisregard=True
		# now see if there are any instructions other than the standard ones above; if so, print them in 'other'
		instructions=re.sub(r'collect','',instructions)
		instructions=re.sub(r'mark & leave','',instructions)
		instructions=re.sub(r'disregard','',instructions)
		instructions=re.sub(r'^[; ]+','',instructions) # only get rid of semicolons and spaces before the first word
		instructions=re.sub(r' ; ','',instructions) # also get rid of remaining ' ; ' i.e. when first word is not a keyword
		instructions=re.sub(r'; *$','',instructions) # also get rid of trailing ';' i.e. when last word is a keyword
		if instructions != "":
			instructionsOther=True
		instructionsOtherText=instructions

		locText=clueData[6]
		if clueData[8]!="":
			locText=locText+"\n(Radio GPS = "+clueData[8]+")"
		fields=[('incidentNameField',self.incidentName),
              ('dateField',time.strftime("%x")),
              ('operationalPeriodField',clueData[5]),
				  ('clueNumberField',clueData[0]),
				  ('dateTimeField',clueData[4]+"   "+clueData[3]),
				  ('teamField',clueData[2]),
				  ('descriptionField',clueData[1]),
				  ('locationField',locText),
				  ('instructionsCollectField',instructionsCollect),
				  ('instructionsDisregardField',instructionsDisregard),
				  ('instructionsMarkAndLeaveField',instructionsMarkAndLeave),
				  ('instructionsOtherField',instructionsOther),
				  ('instructionsOtherTextField',instructionsOtherText)]
		fdf=forge_fdf("",fields,[],[],[])
		fdf_file=open(clueFdfName,"wb")
		fdf_file.write(fdf)
		fdf_file.close()

		pdftk_cmd='pdftk "'+self.fillableClueReportPdfFileName+'" fill_form "'+clueFdfName+'" output "'+cluePdfName+'" flatten'
		rprint("Calling pdftk with the following command:")
		rprint(pdftk_cmd)
		os.system(pdftk_cmd)

		win32api.ShellExecute(0,"print",cluePdfName,'/d:"%s"' % win32print.GetDefaultPrinter(),".",0)
		if os.path.isdir(self.secondWorkingDir):
			rprint("copying clue report pdf to "+self.secondWorkingDir)
			shutil.copy(clueFdfName,self.secondWorkingDir)
			shutil.copy(cluePdfName,self.secondWorkingDir)


	def startupOptions(self):
		self.optionsDialog.show()
		self.optionsDialog.raise_()
		self.optionsDialog.ui.incidentField.selectAll()
		QTimer.singleShot(250,self.optionsDialog.ui.incidentField.selectAll)
		QTimer.singleShot(500,self.optionsDialog.ui.incidentField.deselect)
		QTimer.singleShot(750,self.optionsDialog.ui.incidentField.selectAll)
		QTimer.singleShot(1000,self.optionsDialog.ui.incidentField.deselect)
		QTimer.singleShot(1250,self.optionsDialog.ui.incidentField.selectAll)
		QTimer.singleShot(1500,self.optionsDialog.ui.incidentField.deselect)
		QTimer.singleShot(1750,self.optionsDialog.ui.incidentField.selectAll)
		QTimer.singleShot(1800,self.optionsDialog.ui.incidentField.setFocus)

	def fontsChanged(self):
		rprint("1 - begin fontsChanged")
		# preserve the currently selected tab, since something in this function
		#  causes the rightmost tab to be selected
		i=self.ui.tabWidget.currentIndex()
		self.ui.tableView.setStyleSheet("font-size:"+str(self.fontSize)+"pt")
		for n in self.ui.tableViewList[1:]:
			rprint("n="+str(n))
			n.setStyleSheet("font-size:"+str(self.fontSize)+"pt")
		# don't change tab font size unless you find a good way to dynamically
		# change tab size and margins as well
##		self.ui.tabWidget.tabBar().setStyleSheet("font-size:"+str(self.fontSize)+"pt")
		rprint("2")
		self.redrawTables()
		self.ui.tabWidget.setCurrentIndex(i)
		rprint("3 - end of fontsChanged")
		# changin QLabel size application-wide is too impactful; investigate later
		self.ui.incidentNameLabel.setStyleSheet("font-size:"+str(self.fontSize)+"pt;")
		self.parent.setStyleSheet("QMessageBox,QPushButton,QMenu { font-size:"+str(self.fontSize)+"pt; }")

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
##		self.ui.tableView.model().layoutChanged.emit()
##		self.ui.tableView.scrollToBottom()
		self.loadFlag=True
		rprint("1: start of redrawTables")
		for i in [2,4]: # hardcode results in significant speedup
			self.ui.tableView.resizeColumnToContents(i) # zero is the first column
		rprint("2")
		self.ui.tableView.setColumnWidth(0,self.fontSize*5) # wide enough for '2345'
		self.ui.tableView.setColumnWidth(1,self.fontSize*6) # wide enough for 'FROM'
		self.ui.tableView.setColumnWidth(5,self.fontSize*10) # wide enough for 'STATUS'
		rprint("3")
##		self.ui.tableView.resizeRowsToContents()
		rprint("4")
		for n in self.ui.tableViewList[1:]:
			rprint(" n="+str(n))
			for i in [2,4]: # hardcode results in significant speedup, but lag still scales with filtered table length
				print("    i="+str(i))
				n.resizeColumnToContents(i)
			rprint("    done with i")
			n.setColumnWidth(0,self.fontSize*5)
			n.setColumnWidth(1,self.fontSize*6)
			n.setColumnWidth(5,self.fontSize*10)
			rprint("    resizing rows to contents")
##			n.resizeRowsToContents()
		rprint("5")
		self.ui.tableView.scrollToBottom()
		rprint("6")
		for i in range(1,self.ui.tabWidget.count()):
			self.ui.tabWidget.setCurrentIndex(i)
			self.ui.tableViewList[i].scrollToBottom()
		rprint("7: end of redrawTables")
##		self.resizeRowsToContentsIfNeeded()
		self.loadFlag=False

	def updateClock(self):
		self.ui.clock.display(time.strftime("%H:%M"))

	def updateTeamTimers(self):
		# keep track of seconds since contact, rather than seconds remaining til timeout,
		#  since timeout setting may change but each team's counter should still count
		# 1. increment each number in teamTimersDict
		# 2. if any of them are more than the timeout setting, they have timed out: start flashing
		# 3. use this same timer to toggle the blink state of each style

		if self.blinkToggle==0:
			self.blinkToggle=1
			# now make sure the help window color code bars blink too
			self.helpWindow.ui.colorLabel4.setStyleSheet(statusStyleDict[""])
			self.helpWindow.ui.colorLabel5.setStyleSheet(statusStyleDict["TIMED_OUT_ORANGE"])
			self.helpWindow.ui.colorLabel6.setStyleSheet(statusStyleDict["TIMED_OUT_RED"])
			self.helpWindow.ui.colorLabel7.setStyleSheet(statusStyleDict[""])
		else:
			self.blinkToggle=0
			# now make sure the help window color code bars blink too
			self.helpWindow.ui.colorLabel4.setStyleSheet(statusStyleDict["Waiting for Transport"])
			self.helpWindow.ui.colorLabel5.setStyleSheet(statusStyleDict[""])
			self.helpWindow.ui.colorLabel6.setStyleSheet(statusStyleDict[""])
			self.helpWindow.ui.colorLabel7.setStyleSheet(statusStyleDict["STANDBY"])

		for extTeamName in teamTimersDict:
			# if there is a newEntryWidget currently open for this team, don't blink,
			#  but don't reset the timer.  Only reset the timer when the dialog is accepted.
			hold=False
			for widget in newEntryWidget.instances:
				if widget.ui.to_fromField.currentText()=="FROM" and getExtTeamName(widget.ui.teamField.text())==extTeamName:
					hold=True
			i=self.extTeamNameList.index(extTeamName)
			status=teamStatusDict[extTeamName]
##			rprint("blinking "+extTeamName+": status="+status)
			secondsSinceContact=teamTimersDict[extTeamName]
			if status=="Waiting for Transport" or status=="STANDBY" or (secondsSinceContact>=self.timeoutOrangeSec):
				if self.blinkToggle==0:
					# blink 0: style is one of these:
					# - style as normal per status
					self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).setStyleSheet(statusStyleDict[status])
				else:
					# blink 1: style is one of these:
					# - timeout orange
					# - timeout red
					# - no change (if status is anything but 'Waiting for transport' or 'STANDBY')
					# - blank (black on white) (if status is 'Waiting for transport' or 'STANDBY', and not timed out)
					if not hold and status!="At IC" and secondsSinceContact>=self.timeoutRedSec:
						self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).setStyleSheet(statusStyleDict["TIMED_OUT_RED"])
					elif not hold and status!="At IC" and (secondsSinceContact>=self.timeoutOrangeSec and secondsSinceContact<self.timeoutRedSec):
						self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).setStyleSheet(statusStyleDict["TIMED_OUT_ORANGE"])
					elif status=="Waiting for Transport"or status=="STANDBY":
						self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).setStyleSheet(statusStyleDict[""])
			else:
				# not Waiting for transport, and not in orange/red time zone: draw the normal style
				self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).setStyleSheet(statusStyleDict[status])

			# once they have timed out, keep incrementing; but if the timer is '-1', they will never timeout
			if secondsSinceContact>-1:
				teamTimersDict[extTeamName]=secondsSinceContact+1

	def keyPressEvent(self,event):
		if type(event)==QKeyEvent:
			key=event.text().lower() # hotkeys are case insensitive
			if re.match("\d",key):
				self.openNewEntry(key)
			elif key=='t' or event.key()==Qt.Key_Right:
				self.openNewEntry('t')
			elif key=='f' or event.key()==Qt.Key_Left:
				self.openNewEntry('f')
			elif key=='a':
				self.openNewEntry('a')
			elif key=='s':
				self.openNewEntry('s')
			elif key=='=' or key=='+':
				self.fontSize=self.fontSize+2
				self.fontsChanged()
			elif key=='-' or key=='_':
				if self.fontSize>4:
					self.fontSize=self.fontSize-2
					self.fontsChanged()
			elif event.key()==Qt.Key_F3:
				self.printDialog.show()
			elif event.key()==Qt.Key_F4:
				self.load()
			elif event.key()==Qt.Key_F5:
				self.fsLoadLookup()
			elif event.key()==Qt.Key_F6:
				if QMessageBox.question(self,"Please Confirm","Restore the last saved files (Radio Log, Clue Log, and FleetSync table)?",
						QMessageBox.Yes|QMessageBox.Cancel,QMessageBox.Cancel)==QMessageBox.Yes:
					self.restore()
			elif event.key()==Qt.Key_Space or event.key()==Qt.Key_Enter or event.key()==Qt.Key_Return:
				self.openNewEntry('pop')
			event.accept()
		else:
			event.ignore()

	def closeEvent(self,event):
		self.exitClicked=True
		
		# if radioLogNeedsPrint or clueLogNeedsPrint is True, bring up the print dialog
		if self.radioLogNeedsPrint or self.clueLogNeedsPrint:
			rprint("needs print!")
			self.printDialog.exec()
		else:
			rprint("no print needed")
		# note, this type of messagebox is needed to show above all other dialogs for this application,
		#  even the ones that have WindowStaysOnTopHint.  This works in Vista 32 home basic.
		#  if it didn't show up on top, then, there would be no way to close the radiolog other than kill.
		really=QMessageBox(QMessageBox.Warning,"Please Confirm","Exit the Radio Log program?",
			QMessageBox.Yes|QMessageBox.Cancel,self,Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
		if really.exec()==QMessageBox.Cancel:
			event.ignore()
			self.exitClicked=False
			return

		self.save(finalize=True)
		self.fsSaveLookup()
		self.saveRcFile(cleanShutdownFlag=True)
		writeLogBuffer()

		self.teamTimer.stop()
		if self.firstComPortFound:
			self.firstComPort.close()
		if self.secondComPortFound:
			self.secondComPort.close()
##		self.optionsDialog.close()
##		self.helpWindow.close()
##		self.newEntryWindow.close()
		event.accept()
		qApp.quit() # needed to make sure all windows area closed

	def saveRcFile(self,cleanShutdownFlag=False):
		(x,y,w,h)=self.geometry().getRect()
		(cx,cy,cw,ch)=self.clueLogDialog.geometry().getRect()
		rcFile=QFile(self.rcFileName)
		if not rcFile.open(QFile.WriteOnly|QFile.Text):
			QMessageBox.warning(self,"Error","Cannot write resource file! "+rcFile.errorString())
			return
		out=QTextStream(rcFile)
		out << "[RadioLog]\n"
		# do not save timeout,datum,coord format in the resource file - keep them at the hardcoded defaults
		# future improvement: read defaults from radiolog_defaults.txt (necessary for different teams)
#		out << "timeout-seconds=" << self.timeoutRedSec << "\n"
#		out << "datum=" << self.datum << "\n"
#		out << "coordinate-format=" << self.coordFormat << "\n"
		out << "lastFileName=" << self.csvFileName << "\n"
		out << "font-size=" << self.fontSize << "pt\n"
		out << "x=" << x << "\n"
		out << "y=" << y << "\n"
		out << "w=" << w << "\n"
		out << "h=" << h << "\n"
		out << "clueLog_x=" << cx << "\n"
		out << "clueLog_y=" << cy << "\n"
		out << "clueLog_w=" << cw << "\n"
		out << "clueLog_h=" << ch << "\n"
		if cleanShutdownFlag:
			out << "cleanShutdown=True\n"
		rcFile.close()

	def loadRcFile(self):
		rcFile=QFile(self.rcFileName)
		if not rcFile.open(QFile.ReadOnly|QFile.Text):
			QMessageBox.warning(self,"Error","Cannot read resource file!  Using default settings. "+rcFile.errorString())
			return
		inStr=QTextStream(rcFile)
		line=inStr.readLine()
		if line!="[RadioLog]":
			QMessageBox.warning(self,"Error","Not a valid resource file!  Using default settings.")
			rcFile.close()
			return
		cleanShutdownFlag=False
		while not inStr.atEnd():
			line=inStr.readLine()
			tokens=line.split("=")
			if tokens[0]=="x":
				self.x=int(tokens[1])
			elif tokens[0]=="y":
				self.y=int(tokens[1])
			elif tokens[0]=="w":
				self.w=int(tokens[1])
			elif tokens[0]=="h":
				self.h=int(tokens[1])
			elif tokens[0]=="font-size":
				self.fontSize=int(tokens[1].replace('pt',''))
			elif tokens[0]=="clueLog_x":
				self.clueLog_x=int(tokens[1])
			elif tokens[0]=="clueLog_y":
				self.clueLog_y=int(tokens[1])
			elif tokens[0]=="clueLog_w":
				self.clueLog_w=int(tokens[1])
			elif tokens[0]=="clueLog_h":
				self.clueLog_h=int(tokens[1])
			elif tokens[0]=="lastFileName":
				self.lastFileName=tokens[1]
			elif tokens[0]=="cleanShutdown" and tokens[1]=="True":
				cleanShutdownFlag=True

		# do not save timeout,datum,coord format in the resource file - keep them at the hardcoded defaults
		# future improvement: read defaults from radiolog_defaults.txt (necessary for different teams)
#			elif tokens[0]=="timeout-seconds":
#				self.timeoutRedSec=tokens[1]
#			elif tokens[0]=="datum":
#				self.datum=tokens[1]
#			elif tokens[0]=="coordinate-format":
#				self.coordFormat=tokens[1]
		rcFile.close()
		return cleanShutdownFlag

	def save(self,finalize=False):
		csvFileNameList=[self.firstWorkingDir+"\\"+self.csvFileName]
		if os.path.isdir(self.secondWorkingDir):
			csvFileNameList.append(self.secondWorkingDir+"\\"+self.csvFileName)
		for fileName in csvFileNameList:
			with open(fileName,'w',newline='') as csvFile:
				csvWriter=csv.writer(csvFile)
				csvWriter.writerow(["## Radio Log data file"])
				csvWriter.writerow(["## File written "+time.strftime("%a %b %d %Y %H:%M:%S")])
				csvWriter.writerow(["## Incident Name: "+self.incidentName])
				csvWriter.writerow(["## Datum: "+self.datum+"  Coordinate format: "+self.coordFormat])
				for row in self.radioLog:
					row += [''] * (10-len(row)) # pad the row up to 10 elements if needed, to avoid index errors elsewhere
					if row[6]<1e10: # don't save the blank line
						# replacing commas is not necessary: csvwriter puts strings in quotes,
						#  and csvreader knows to not treat commas as delimeters if inside quotes
						csvWriter.writerow(row)
				if finalize:
					csvWriter.writerow(["## end"])
		# now write the clue log to a separate csv file: same filename appended by '.clueLog'
		if len(self.clueLog)>0:
			for fileName in csvFileNameList:
				fileName=fileName.replace(".csv","_clueLog.csv")
				with open(fileName,'w',newline='') as csvFile:
					csvWriter=csv.writer(csvFile)
					csvWriter.writerow(["## Clue Log data file"])
					csvWriter.writerow(["## File written "+time.strftime("%a %b %d %Y %H:%M:%S")])
					csvWriter.writerow(["## Incident Name: "+self.incidentName])
					csvWriter.writerow(["## Datum: "+self.datum+"  Coordinate format: "+self.coordFormat])
					for row in self.clueLog:
						csvWriter.writerow(row)
					if finalize:
						csvWriter.writerow(["## end"])

	def load(self,fileName=None):
		# loading scheme:
		# always merge instead of overwrite; always use the loaded Begins line since it will be earlier by definition
		# maybe provide some way to force overwrite later, but, for now that can be done just by exiting and restarting
		self.loadFlag=True
		if not fileName:
			fileName=QFileDialog.getOpenFileName(caption="Load Existing Radio Log",filter="RadioLog CSV files (*.csv)")[0]
			if not os.path.isfile(fileName): # prevent error if dialog is canceled
				return
		if "_clueLog" in fileName or "_fleetsync" in fileName:
			QMessageBox(QMessageBox.Critical,"Invalid File Selected","Do not load a Clue Log or FleetSync file directly.  Load the parent radiolog.csv file directly, and the Clue Log and FleetSync files will automatically be loaded with it.",QMessageBox.Ok).exec()
			return
		progressBox=QProgressDialog("Loading, please wait...","Abort",0,100)
		progressBox.setWindowModality(Qt.WindowModal)
		progressBox.setWindowTitle("Loading")
		progressBox.show()
		QCoreApplication.processEvents()
		self.teamTimer.start(10000) # pause

		rprint("Loading:"+fileName)
		# pass 1: count total entries for the progress box, and read incident name
		with open(fileName,'r') as csvFile:
			csvReader=csv.reader(csvFile)
			totalEntries=0
			for row in csvReader:
				if row[0].startswith("## Incident Name:"):
					self.incidentName=row[0][17:]
					self.incidentNameNormalized=self.incidentName.replace(" ","")
					self.ui.incidentNameLabel.setText(self.incidentName)
				if not row[0].startswith('#'): # prune comment lines
					totalEntries=totalEntries+1
			progressBox.setMaximum(totalEntries*2)

		# pass 2: read and process the file
		with open(fileName,'r') as csvFile:
			csvReader=csv.reader(csvFile)
			loadedRadioLog=[]
			i=0
			for row in csvReader:
				if not row[0].startswith('#'): # prune comment lines
					row[6]=float(row[6]) # convert epoch seconds back to float, for sorting
					row += [''] * (10-len(row)) # pad the row up to 10 elements if needed, to avoid index errors elsewhere
					loadedRadioLog.append(row)
					i=i+1
					if row[3].startswith("Operational Period") and row[3].split()[3]=="Begins:":
						self.opPeriod=int(row[3].split()[2])
						self.printDialog.ui.opPeriodComboBox.addItem(str(self.opPeriod))
					progressBox.setValue(i)
			csvFile.close()

		# now add entries, sort, and prune any Begins lines after the first line
		# edit: don't prune Begins lines - those are needed to indicate start of operational periods
		for row in loadedRadioLog:
			self.newEntry(row)
			i=i+1
			progressBox.setValue(i)
		self.radioLog.sort(key=lambda entry: entry[6]) # sort by epoch seconds
##		self.radioLog[1:]=[x for x in self.radioLog[1:] if not x[3].startswith('Radio Log Begins:')]

		# take care of the newEntry cleanup functions that have been put off due to loadFlag
		rprint("trace1")

# apparently, we need to emit layoutChanged and then scrollToBottom, before resizeColumnToContents,
#  to make sure column width resizes to fit >all< contents (i.e 'Team 5678'). ??
# they could be put inside redrawTables, but, there's no need to put them inside that
#  function which is called from other places, unless another syptom shows up; so, leave
#  them here for now.
		self.ui.tableView.model().layoutChanged.emit()
		self.ui.tableView.scrollToBottom()
##		self.ui.tableView.resizeRowsToContents()
##		for i in range(self.ui.tabWidget.count()):
##			self.ui.tabWidget.setCurrentIndex(i)
##			self.ui.tableViewList[i].scrollToBottom()
##			self.ui.tableViewList[i].resizeRowsToContents()

##		self.ui.tableView.model().layoutChanged.emit()

		# now load the clue log (same filename appended by .clueLog) if it exists
		clueLogFileName=fileName.replace(".csv","_clueLog.csv")
		global lastClueNumber
		if os.path.isfile(clueLogFileName):
			with open(clueLogFileName,'r') as csvFile:
				csvReader=csv.reader(csvFile)
##				self.clueLog=[] # uncomment this line to overwrite instead of combine
				for row in csvReader:
					if not row[0].startswith('#'): # prune comment lines
						self.clueLog.append(row)
						if row[0]!="":
							lastClueNumber=int(row[0])
				csvFile.close()

		self.clueLogDialog.ui.tableView.model().layoutChanged.emit()
		# finished
		rprint("Starting redrawTables")
		self.fontsChanged()
##		self.ui.tableView.model().layoutChanged.emit()
##		QCoreApplication.processEvents()
		rprint("Returned from redrawTables")
		progressBox.close()
		self.ui.opPeriodButton.setText("OP "+str(self.opPeriod))
		self.teamTimer.start(1000) #resume
		self.loadFlag=False

	def optionsAccepted(self):
		self.incidentName=self.optionsDialog.ui.incidentField.text()
		# normalize the name for purposes of filenames
		#  - get rid of all spaces -  no need to be able to reproduce the
		#    incident name's spaces from the filename
		self.incidentNameNormalized=self.incidentName.replace(" ","")
		self.csvFileName=getFileNameBase(self.incidentNameNormalized)+".csv"
		self.pdfFileName=getFileNameBase(self.incidentNameNormalized)+".pdf"
		self.fsFileName=self.csvFileName.replace('.csv','_fleetsync.csv')

		self.ui.incidentNameLabel.setText(self.incidentName)
		self.datum=self.optionsDialog.ui.datumField.currentText()
		self.coordFormat=self.optionsDialog.ui.formatField.currentText()
		# TMG 4-22-15: do not try to convert coords right now: it fails due to space in radioLoc i.e. "NO FIX"
##		for row in self.radioLog:
##			if row[9] and row[9]!='':
##				row[4]=self.convertCoords(row[9].split('|'),self.datum,self.coordFormat)
##		self.redrawTables()
		self.ui.datumFormatLabel.setText(self.datum+"\n"+self.coordFormat)
		self.timeoutRedSec=timeoutDisplayList[self.optionsDialog.ui.timeoutField.value()][1]
		self.timeoutOrangeSec=self.timeoutRedSec-300 # always go orange 5 minutes before red
		if self.timeoutOrangeSec<0:
			self.timeoutOrangeSec=self.timeoutRedSec-3 # or 3 seconds before for tiny values
		self.ui.timeoutLabel.setText("TIMEOUT:\n"+timeoutDisplayList[self.optionsDialog.ui.timeoutField.value()][0])

	def openNewEntry(self,key=None,callsign=None,formattedLocString=None,fleet=None,dev=None,origLocString=None,amendFlag=False,amendRow=None):
		if clueDialog.openDialogCount==0:
			self.newEntryWindow.setWindowFlags(Qt.WindowTitleHint|Qt.WindowStaysOnTopHint) # enable always on top
		else:
			self.newEntryWindow.setWindowFlags(Qt.WindowTitleHint)
		sec=time.time() # epoch seconds, for sorting purposes; not displayed
		self.newEntryWidget=newEntryWidget(self,sec,formattedLocString,fleet,dev,origLocString,amendFlag,amendRow)
		if key:
			if key=='a':
				self.newEntryWidget.ui.to_fromField.setCurrentIndex(1)
				# all three of these lines are needed to override the default 'pseudo-selected'
				# behavior; see http://stackoverflow.com/questions/27856032
				self.newEntryWidget.ui.teamField.setFocus()
				self.newEntryWidget.ui.teamField.setText("All Teams ")
				self.newEntryWidget.ui.messageField.setFocus()
##				self.newEntryWidget.ui.teamField.setSelection(9,1)
			elif key=='t':
				self.newEntryWidget.ui.to_fromField.setCurrentIndex(1)
				# need to 'burp' the focus to prevent two blinking cursors
				#  see http://stackoverflow.com/questions/42475602
				self.newEntryWidget.ui.messageField.setFocus()
				# all three of these lines are needed to override the default 'pseudo-selected'
				# behavior; see http://stackoverflow.com/questions/27856032
				self.newEntryWidget.ui.teamField.setFocus()
				self.newEntryWidget.ui.teamField.setText("Team  ")
				self.newEntryWidget.ui.teamField.setSelection(5,1)
			elif key=='f' or key=='pop':
				self.newEntryWidget.ui.to_fromField.setCurrentIndex(0)
				# need to 'burp' the focus to prevent two blinking cursors
				#  see http://stackoverflow.com/questions/42475602
				self.newEntryWidget.ui.messageField.setFocus()
				self.newEntryWidget.ui.teamField.setFocus()
				self.newEntryWidget.ui.teamField.setText("Team  ")
				self.newEntryWidget.ui.teamField.setSelection(5,1)
			elif key=='s':
				self.newEntryWidget.ui.to_fromField.setCurrentIndex(0)
				# need to 'burp' the focus to prevent two blinking cursors
				#  see http://stackoverflow.com/questions/42475602
				self.newEntryWidget.ui.messageField.setFocus()
				self.newEntryWidget.ui.teamField.setFocus()
				self.newEntryWidget.ui.teamField.setText("SAR  ")
				self.newEntryWidget.ui.teamField.setSelection(4,1)
			elif key=='tab':
				self.newEntryWidget.ui.to_fromField.setCurrentIndex(0)
				self.newEntryWidget.ui.messageField.setFocus()
			else:
				self.newEntryWidget.ui.to_fromField.setCurrentIndex(0)
				# need to 'burp' the focus to prevent two blinking cursors
				#  see http://stackoverflow.com/questions/42475602
				self.newEntryWidget.ui.messageField.setFocus()
				self.newEntryWidget.ui.teamField.setFocus()
				self.newEntryWidget.ui.teamField.setText("Team "+key+" ")
				self.newEntryWidget.ui.teamField.setSelection(6,1)
		else: # no key pressed; opened from the 'add entry' GUI button
			# need to 'burp' the focus to prevent two blinking cursors
			#  see http://stackoverflow.com/questions/42475602
			self.newEntryWidget.ui.messageField.setFocus()
			self.newEntryWidget.ui.teamField.setFocus()

		if callsign:
			extTeamName=getExtTeamName(callsign)
			self.newEntryWidget.ui.teamField.setText(callsign)
			if callsign[0:3]=='KW-':
				self.newEntryWidget.ui.teamField.setFocus()
				self.newEntryWidget.ui.teamField.selectAll()
			if callsign[0:6]=="Radio " or callsign[0:3]=="KW-":
##				self.newEntryWidget.openChangeCallsignDialog()
				QTimer.singleShot(500,lambda:self.newEntryWidget.openChangeCallsignDialog())
			# change this to only take focus if the new tab is active; otherwise, leave the focus alone
##			else:
##				self.newEntryWidget.ui.messageField.setFocus() # ready to type the message
			self.newEntryWidget.ui.messageField.setFocus()

		if formattedLocString:
			self.newEntryWidget.ui.radioLocField.setText(formattedLocString)
			self.newEntryWidget.ui.datumFormatLabel.setText("("+self.datum+"  "+self.coordFormat+")")
		else:
			self.newEntryWidget.ui.datumFormatLabel.setText("")

	def newEntry(self,values):
		# values array format: [time,to_from,team,message,locString,status,sec,fleet,dev]
		#  locString is also stored in the table in a column after dev, unmodified;
		#  the value in the 5th column is modified in place based on the datum and
		#  coordinate format; this is cleaner than formatting the coordinates in the
		#  QAbstractTableModel, because the hardcoded table values will show up in the
		#  saved file as expected.
		#  Only columns thru and including status are shown in the tables.
		rprint("newEntry called with these values:")
		rprint(values)
		niceTeamName=values[2]
		status=values[5]
		if values[4]==None:
			values[4]=''
		sec=values[6] # epoch seconds of dialog open time, for sorting; not displayed
		extTeamName=getExtTeamName(niceTeamName)
		self.radioLog.append(values) # leave a blank entry at the end for aesthetics
##		if not values[3].startswith("RADIO LOG SOFTWARE:"):
##			self.newEntryProcessTeam(niceTeamName,status,values[1],values[3])
		self.newEntryProcessTeam(niceTeamName,status,values[1],values[3])

	def newEntryProcessTeam(self,niceTeamName,status,to_from,msg):
		extTeamName=getExtTeamName(niceTeamName)
      # skip entries with no team like 'radio log begins', or multiple entries like 'all'
		if niceTeamName!='' and not niceTeamName.lower()=="all" and not niceTeamName.lower().startswith("all"):
			# if it's a team that doesn't already have a tab, make a new tab
			if extTeamName not in self.extTeamNameList:
				self.newTeam(niceTeamName)
			i=self.extTeamNameList.index(extTeamName)
			teamStatusDict[extTeamName]=status
			# credit to Berryblue031 for pointing out this way to style the tab widgets
			# http://www.qtcentre.org/threads/49025
			# NOTE the following line causes font-size to go back to system default;
			#  can't figure out why it doesn't inherit font-size from the existing
			#  styleSheet; so, each statusStyleDict entry must contain font-size explicitly
			self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).setStyleSheet(statusStyleDict[status])
			# only reset the team timer if it is a 'FROM' message with non-blank message text
			#  (prevent reset on amend, where to_from can be "AMEND" and msg can be anything)
			if to_from=="FROM" and msg != "":
				teamTimersDict[extTeamName]=0
			if status=="At IC":
				teamTimersDict[extTeamName]=-1 # no more timeouts will show up
		if not self.loadFlag:
			QTimer.singleShot(100,lambda:self.newEntryPost(extTeamName))

	def newEntryPost(self,extTeamName=None):
##		rprint("1: called newEntryPost")
		self.radioLogNeedsPrint=True
		self.radioLog.sort(key=lambda entry: entry[6]) # sort by epoch seconds - in case dialogs are accepted out of order
##		rprint("2") # layoutChanged.emit() is a key source of delay!  about 2 seconds on a 670 row table
		# putting this line in a singleShot would allow the main table to get updated much
		#  more quickly, but, the team table would not be updated until later and the new entry
		#  row height would be incorrect due to the data not being available for resizeRowsToContents
		# could maybe address part of that by setting verticalHeader.setDefaultSectionSize at font change time?
		self.ui.tableView.model().layoutChanged.emit() # note this must happen AFTER the sort!
##		rprint("3")
		# resize the bottom-most rows (up to 10 of them):
		#  this makes lag time independent of total row count for large tables,
		#  and reduces overall lag about 30% vs resizeRowsToContents (about 3 sec vs 4.5 sec for a 1300-row table)
		for n in range(len(self.radioLog)-10,len(self.radioLog)):
			if n>=0:
				self.ui.tableView.resizeRowToContents(n+1)
##		rprint("4")
		self.ui.tableView.scrollToBottom()
##		rprint("5")
		for i in [2,4]: # hardcode results in significant speedup
			self.ui.tableView.resizeColumnToContents(i)
		for n in self.ui.tableViewList[1:]:
			for i in [2,4]: # hardcode results in significant speedup
				n.resizeColumnToContents(i)
		if extTeamName:
			if extTeamName=="ALL TEAMS":
				for i in range(1,len(self.extTeamNameList)):
					self.ui.tabWidget.setCurrentIndex(i)
					self.ui.tableViewList[i].resizeRowsToContents()
					for n in range(len(self.radioLog)-10,len(self.radioLog)):
						if n>=0:
							self.ui.tableViewList[i].resizeRowToContents(n+1)
					self.ui.tableViewList[i].scrollToBottom()
			elif extTeamName!="z_00000":
				if extTeamName in self.extTeamNameList:
					i=self.extTeamNameList.index(extTeamName)
					self.ui.tabWidget.setCurrentIndex(i)
					self.ui.tableViewList[i].resizeRowsToContents()
					for n in range(len(self.radioLog)-10,len(self.radioLog)):
						if n>=0:
							self.ui.tableViewList[i].resizeRowToContents(n+1)
					self.ui.tableViewList[i].scrollToBottom()

##		rprint("6")
		self.save()
##		self.redrawTables()
##		QCoreApplication.processEvents()
##		rprint("7: finished newEntryPost")

	def tableContextMenu(self,pos):
		row=self.ui.tableView.rowAt(pos.y())
		rowData=self.radioLog[row]
		rprint("row:"+str(row)+":"+str(rowData))
		if row>0 and rowData[1]:
			self.ui.tableView.setSelectionMode(QAbstractItemView.SingleSelection)
			self.ui.tableView.selectRow(row)
			rowHasRadioLoc=False
			rowHasMsgCoords=False
##			if rowData[9] and rowData[9]!="":
##				rowHasRadioLoc=True
##			if re.search(r'[0-9]{4,}',rowData[3]): # a string of four or more digits in the message
##				rowHasMsgCoords=True
			menu=QMenu()
			amendAction=menu.addAction("Amend this entry")
##			convertAction=menu.addAction("Convert coordinates")
##			if not (rowHasRadioLoc or rowHasMsgCoords):
##				convertAction.setEnabled(False)
			action=menu.exec_(self.ui.tableView.viewport().mapToGlobal(pos))
			self.ui.tableView.clearSelection()
			self.ui.tableView.setSelectionMode(QAbstractItemView.NoSelection)
			if action==amendAction:
				self.amendEntry(row)
##			if action==convertAction:
##				self.convertDialog=convertDialog(self,rowData,rowHasRadioLoc,rowHasMsgCoords)
##				self.convertDialog.show()

	def amendEntry(self,row):
		rprint("Amending row "+str(row))
		amendDialog=self.openNewEntry(amendFlag=True,amendRow=row)

	def newTeam(self,newTeamName):
		# not sure why newTeamName is False (bool) when called as a slot;
		# setting a default val for the arg has not effect, so just work with it
		if newTeamName==False:
			newTeamName="Team0"

		# determine the correct index - keep team tabs in sequential order,
		# with non-"Team" callsigns alphabettically at the end
		# 1. append the new extended team name to extTeamNameList
		# 2. sort extTeamNameList (simple alphaumeric sort)
		# 3. find the index of the new extended team name in extTeamNameList
		# 4. add newTeamName to teamNameList at that index
		extTeamName=getExtTeamName(newTeamName)
		niceTeamName=getNiceTeamName(extTeamName)
		shortNiceTeamName=getShortNiceTeamName(niceTeamName)
		rprint("new team: newTeamName="+newTeamName+" extTeamName="+extTeamName+" niceTeamName="+niceTeamName+" shortNiceTeamName="+shortNiceTeamName)
		self.extTeamNameList.append(extTeamName)
		self.extTeamNameList.sort()
		i=self.extTeamNameList.index(extTeamName)
		self.teamNameList.insert(i,niceTeamName)
		if self.allTeamsList.count(niceTeamName)==0:
			self.allTeamsList.insert(i,niceTeamName)
			self.allTeamsList.sort()
		teamTimersDict[extTeamName]=0
		teamCreatedTimeDict[extTeamName]=time.time()

		self.ui.tabList.insert(i,QWidget())
		self.ui.tabGridLayoutList.insert(i,QGridLayout(self.ui.tabList[i]))
		self.ui.tableViewList.insert(i,QTableView(self.ui.tabList[i]))
		self.ui.tableViewList[i].verticalHeader().setVisible(False)
		self.ui.tableViewList[i].setTextElideMode(Qt.ElideNone)
		self.ui.tableViewList[i].setFocusPolicy(Qt.NoFocus)
		self.ui.tableViewList[i].setSelectionMode(QAbstractItemView.NoSelection)
		self.ui.tableViewList[i].setStyleSheet("font-size:"+str(self.fontSize)+"pt")
		self.ui.tabGridLayoutList[i].addWidget(self.ui.tableViewList[i],0,0,1,1)
		self.ui.tabWidget.insertTab(i,self.ui.tabList[i],'')
		noSpaceNiceTeamName=niceTeamName.replace(' ','')
		label=QLabel(" "+shortNiceTeamName+" ")
		label.setStyleSheet("font-size:20px;border:1px outset black;qproperty-alignment:AlignCenter")
		self.ui.tabWidget.tabBar().setTabButton(i,QTabBar.LeftSide,label)
		self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).setStyleSheet("font-size:20px;border:1px outset black;qproperty-alignment:AlignCenter")

##		deleteTeamTabAction=QAction("Delete Tab",None)
##		deleteTeamTabAction.triggered.connect(self.deletePrint)
##		self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).setContextMenuPolicy(Qt.ActionsContextMenu)
##		self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).addAction(deleteTeamTabAction)
##		deleteTeamTabAction.triggered.connect(lambda:self.deleteTeamTab(newTeamName))



		# better to NOT modify the entered team name value, for data integrity;
		# instead, set the filter to only display rows where the human readable form
		# of the value in column 2 matches the human readable form of the tab name
		self.proxyModelList.insert(i,CustomSortFilterProxyModel(self))
		self.proxyModelList[i].setSourceModel(self.tableModel)
		self.proxyModelList[i].setFilterFixedString(getExtTeamName(newTeamName))
		self.ui.tableViewList[i].setModel(self.proxyModelList[i])
		self.ui.tableViewList[i].hideColumn(6) # hide epoch seconds
		self.ui.tableViewList[i].hideColumn(7) # hide epoch seconds
		self.ui.tableViewList[i].hideColumn(8) # hide epoch seconds
		self.ui.tableViewList[i].hideColumn(9) # hide epoch seconds
		self.ui.tableViewList[i].resizeRowsToContents()

		#NOTE if you do this section before the model is assigned to the tableView,
		# python will crash every time!
		# see the QHeaderView.ResizeMode docs for descriptions of each resize mode value
		# note QHeaderView.setResizeMode is deprecated in 5.4, replaced with
		# .setSectionResizeMode but also has both global and column-index forms
		self.ui.tableViewList[i].horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
		# automatically expand the 'message' column width to fill available space
		self.ui.tableViewList[i].horizontalHeader().setSectionResizeMode(3,QHeaderView.Stretch)
##		self.redrawTables()
##		self.fontsChanged()

##	def deletePrint(self):
##		rprint("deleting")

	def tabContextMenu(self,pos):
		menu=QMenu()
##		menu.setStyleSheet("font-size:"+str(self.fontSize)+"pt")
		i=self.ui.tabWidget.tabBar().tabAt(pos)
		niceTeamName=getNiceTeamName(self.extTeamNameList[i])
		if i>0:
			newEntryFromAction=menu.addAction("New Entry FROM "+str(niceTeamName))
			newEntryToAction=menu.addAction("New Entry TO "+str(niceTeamName))
			menu.addSeparator()
##			relabelTeamTabAction=menu.addAction("Change Label / Assignment for "+str(niceTeamName))
##			menu.addSeparator()
			deleteTeamTabAction=menu.addAction("Hide tab for "+str(niceTeamName))
			action=menu.exec_(self.ui.tabWidget.tabBar().mapToGlobal(pos))
			if action==newEntryFromAction:
				self.openNewEntry('tab',str(niceTeamName))
			if action==newEntryToAction:
				self.openNewEntry('tab',str(niceTeamName))
				self.newEntryWidget.ui.to_fromField.setCurrentIndex(1)
			if action==deleteTeamTabAction:
				self.deleteTeamTab(niceTeamName)
##			if action==relabelTeamTabAction:
##				label=QLabel(" abcdefg ")
##				label.setStyleSheet("font-size:20px;border:1px outset black;qproperty-alignment:AlignCenter")
##				self.ui.tabWidget.tabBar().setTabButton(i,QTabBar.LeftSide,label)
####				self.ui.tabWidget.tabBar().setTabText(i,"boo")
##				self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).setStyleSheet("font-size:20px;border:1px outset black;qproperty-alignment:AlignCenter")

	def deleteTeamTab(self,teamName):
		# must also modify related lists to keep everything in sync
		extTeamName=getExtTeamName(teamName)
		niceTeamName=getNiceTeamName(extTeamName)
		shortNiceTeamName=getShortNiceTeamName(niceTeamName)
		self.extTeamNameList.sort()
		if extTeamName in self.extTeamNameList: # pass through if trying to delete a tab that doesn't exist / has already been deleted
			i=self.extTeamNameList.index(extTeamName)
			self.extTeamNameList.remove(extTeamName)
			self.teamNameList.remove(niceTeamName)
			del teamTimersDict[extTeamName]
			del teamCreatedTimeDict[extTeamName]
			del self.ui.tabList[i]
			del self.ui.tabGridLayoutList[i]
			del self.ui.tableViewList[i]
			self.ui.tabWidget.removeTab(i)
			del self.proxyModelList[i]

	def openOpPeriodDialog(self):
		self.opPeriodDialog=opPeriodDialog(self)
		self.opPeriodDialog.show()

	def addNonRadioClue(self):
		self.newNonRadioClueDialog=nonRadioClueDialog(self,time.strftime("%H%M"),lastClueNumber+1)
		self.newNonRadioClueDialog.show()

	def restore(self):
		# use this function to reload the last saved files, based on lastFileName entry from resource file
		#  but, keep the new session's save filenames going forward
		if self.lastFileName=="":
			QMessageBox(QMessageBox.Critical,"Cannot Restore","Last saved filenames were not saved in the resource file.  Cannot automatically restore last saved files.  You will need to load the files directly [F4].",QMessageBox.Ok).exec()
			return
		self.load(self.firstWorkingDir+"\\"+self.lastFileName) # loads the radio log and the clue log
		self.fsLoadLookup(fsFileName=self.firstWorkingDir+"\\"+self.lastFileName.replace(".csv","_fleetsync.csv"))
		self.fsSaveLookup()
		self.save()
		self.saveRcFile()


class helpWindow(QDialog,Ui_Help):
	def __init__(self, *args):
		QDialog.__init__(self)
		self.ui=Ui_Help()
		self.ui.setupUi(self)
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
##		self.setAttribute(Qt.WA_DeleteOnClose)


class optionsDialog(QDialog,Ui_optionsDialog):
	def __init__(self, *args):
		QDialog.__init__(self)
		self.ui=Ui_optionsDialog()
		self.ui.setupUi(self)
		self.ui.buttonBox.setStyleSheet("font-size:16pt;")
		self.ui.timeoutField.valueChanged.connect(self.displayTimeout)
		self.displayTimeout()
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
##		self.setAttribute(Qt.WA_DeleteOnClose)
		self.ui.datumField.setEnabled(False) # since convert menu is not working yet, TMG 4-8-15
		self.ui.formatField.setEnabled(False) # since convert menu is not working yet, TMG 4-8-15

	def showEvent(self,event):
		# clear focus from all fields, otherwise previously edited field gets focus on next show,
		# which could lead to accidental editing
		self.ui.incidentField.clearFocus()
		self.ui.datumField.clearFocus()
		self.ui.formatField.clearFocus()
		self.ui.timeoutField.clearFocus()

	def displayTimeout(self):
		self.ui.timeoutLabel.setText("Timeout: "+timeoutDisplayList[self.ui.timeoutField.value()][0])


class printDialog(QDialog,Ui_printDialog):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.parent=parent
		self.ui=Ui_printDialog()
		self.ui.setupUi(self)
		self.ui.OKButton.setStyleSheet("font-size:14pt;")
		self.ui.CancelButton.setStyleSheet("font-size:14pt;")
		self.ui.opPeriodComboBox.addItem("1")
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)

	def showEvent(self,event):
		rprint("show event called")
		rprint("teamNameList:"+str(self.parent.teamNameList))
		rprint("allTeamsList:"+str(self.parent.allTeamsList))
		if self.parent.exitClicked:
			self.ui.OKButton.setText("Print")
			self.ui.CancelButton.setText("Exit without printing")
		else:
			self.ui.OKButton.setText("OK")
			self.ui.CancelButton.setText("Cancel")
		if len(self.parent.clueLog)>0:
			self.ui.clueLogField.setChecked(True)
			self.ui.clueLogField.setEnabled(True)
		else:
			self.ui.clueLogField.setChecked(False)
			self.ui.clueLogField.setEnabled(False)
		self.ui.opPeriodComboBox.setCurrentIndex(self.ui.opPeriodComboBox.count()-1)

	def accept(self):
		opPeriod=self.ui.opPeriodComboBox.currentText()
		if self.ui.radioLogField.isChecked():
			rprint("PRINT radio log")
			self.parent.printLog(opPeriod)
		if self.ui.teamRadioLogsField.isChecked():
			rprint("PRINT team radio logs")
			self.parent.printTeamLogs(opPeriod)
		if self.ui.clueLogField.isChecked():
			rprint("PRINT clue log")
			self.parent.printClueLog(opPeriod)
		super(printDialog,self).accept()


# newEntryWindow is the window that has a QTabWidget;
#  each tab's widget (except the first and last which are just labels) is a newEntryWidget
# the name newEntryWindow is to distinguish it from the previous newEntryDialog
#  which had one instance (one dialog box) created per new entry
class newEntryWindow(QDialog,Ui_newEntryWindow):
##	def __init__(self,parent,sec,formattedLocString='',fleet='',dev='',origLocString='',amendFlag=False,amendRow=None):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.ui=Ui_newEntryWindow()
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
		self.parent=parent
		self.tabWidth=175
		self.tabHeight=25
		self.ui.setupUi(self)
		self.ui.tabWidget.setTabBar(FingerTabBarWidget(width=self.tabWidth,height=self.tabHeight))
		self.ui.tabWidget.setTabPosition(QTabWidget.West)
##		self.i=0 # unique persistent tab index; increments with each newly added tab; values are never re-used

		self.ui.tabWidget.insertTab(0,QWidget(),'NEWEST')
		self.ui.tabWidget.setTabEnabled(0,False)
		self.ui.tabWidget.insertTab(1,QWidget(),'OLDEST')
		self.ui.tabWidget.setTabEnabled(1,False)

		self.ui.tabWidget.currentChanged.connect(self.tabChanged)
##		self.ui.tabWidget.currentChanged.connect(self.throb)
##		self.ui.tabWidget.currentChanged.connect(self.activeTabMessageFieldFocus)

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
		self.ui.tabWidget.setStyleSheet("""
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
		""")

		self.timer=QTimer(self)
		self.timer.start(1000)
		self.timer.timeout.connect(self.autoCleanup)

	# prevent 'esc' from closing the newEntryWindow
	def keyPressEvent(self,event):
		if event.key()!=Qt.Key_Escape:
			QDialog.keyPressEvent(self,event)

	def tabChanged(self,throb=True):
##	def throb(self):
		tabCount=self.ui.tabWidget.count()
		currentIndex=self.ui.tabWidget.currentIndex()
		rprint("tabCount="+str(tabCount)+" currentIndex="+str(currentIndex))
		if tabCount>2: # skip all this if 'NEWEST' and 'OLDEST' are the only tabs remaining
			if (tabCount-currentIndex)>1: # don't try to throb the 'OLDEST' label - it has no throb method
				if throb:
					self.ui.tabWidget.widget(currentIndex).throb()

##	def activeTabMessageFieldFocus(self):
##		currentIndex=self.ui.tabWidget.currentIndex()
				self.ui.tabWidget.widget(currentIndex).ui.messageField.setFocus()

##	def updateTabColors(self):

##		if tabCount<4:
##			self.ui.tabWidget.tabBar().setHidden(True)
##			self.ui.tabWidget.resize(initialTabWidgetWidth+20,initialTabWidgetHeight+20)
##		else:
##			self.ui.tabWidget.tabBar().setHidden(False)
##			self.ui.tabWidget.resize(initialTabWidgetWidth+self.tabWidth+20,initialTabWidgetHeight+20)
##		self.adjustSize()
##		currentIndex=self.ui.tabWidget.currentIndex()

##			# code to set tab colors based on sequence
##			for i in range(1,currentIndex):
##				self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).layout().itemAt(1).widget().setStyleSheet(statusStyleDict["TIMED_OUT_RED"])
##			for i in range(currentIndex+1,tabCount-1):
##				self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).layout().itemAt(1).widget().setStyleSheet(statusStyleDict["TIMED_OUT_ORANGE"])
##			try:
##				self.ui.tabWidget.tabBar().tabButton(currentIndex,QTabBar.LeftSide).layout().itemAt(1).widget().setStyleSheet("")
##			except: # the line above has no meaning if the currentIndex is gone and there are no items left
##				pass

	def addTab(self,labelText,widget=None): # always adds at index=1 (index 0 = "NEWEST") i.e. the top of the stack
##		self.i+=1
##		self.ui.tabWidget.insertTab(1,newEntryTabWidget(self,self.i),tabText)
		if widget:
##			widget=newEntryWidget(self.parent) # newEntryWidget constructor calls this function
##			widget=QWidget()
##			self.ui.tabWidget.insertTab(1,widget,labelText)


			self.ui.tabWidget.insertTab(1,widget,"")

			label=QLabel(labelText)
			font = QFont()
			font.setFamily("Segoe UI")
			font.setPointSize(9)
			label.setFont(font)
			spacer=QWidget()
			topWidget=QWidget()
##			label.setStyleSheet("border:1px outset black")
##			spacer.setStyleSheet("border:1px outset black")

##			label.setAlignment(Qt.AlignVCenter)
##			label.setIndent(20)
##			label.setMidLineWidth(20)
##			label.frameRect().moveBottom(20)

##			subWidget=QWidget()
			layout=QHBoxLayout()
			layout.addWidget(spacer)
			layout.addWidget(label)
			layout.setSpacing(0) # to make the rest of the sizing more predictable

			label.setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
			label.setGeometry(QRect(0,0,self.tabWidth-8,self.tabHeight-8))
			spacer.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding)
			spacer.setMinimumSize(8,4)
			layout.setContentsMargins(0,0,0,0)
			topWidget.setLayout(layout)
			topWidget.setSizePolicy(QSizePolicy.Fixed,QSizePolicy.Expanding)
			topWidget.setGeometry(QRect(4,0,self.tabWidth,self.tabHeight-8))
##			label.setGeometry(QRect(16,4,self.tabWidth-3,self.tabHeight-8))

##			self.ui.tabWidget.tabBar().setTabButton(1,QTabBar.LeftSide,label)
##			self.ui.tabWidget.tabBar().tabButton(1,QTabBar.LeftSide).move(1,1)

			self.ui.tabWidget.tabBar().setTabButton(1,QTabBar.LeftSide,topWidget)

##			self.ui.tabWidget.tabBar().tabButton(1,QTabBar.LeftSide).setSizePolicy(QSizePolicy.Expanding,QSizePolicy.Expanding)
##			# if any existing entry widget is still within the hold time, don't change the active tab
##			hold=False
##			for entry in newEntryWidget.instances:
##				if entry.lastModAge<holdSec:
##					hold=True
			# if the current active widget has had no activity within the hold time, then
			#  make this new entry the active tab; otherwise leave it alone
##			currentIndex=self.ui.tabWidget.currentIndex()
##			if self.ui.tabWidget.widget(currentIndex).lastModAge>holdSec or self.ui.tabWidget.count()==3:
			if self.parent.currentEntryLastModAge>holdSec or self.ui.tabWidget.count()==3:
				self.ui.tabWidget.setCurrentIndex(1)
				widget.ui.messageField.setFocus()
##			if not self.parent.entryHold:
##			if not hold:
##				self.ui.tabWidget.setCurrentIndex(1)
##				self.parent.entryHold=True

##			self.ui.tabWidget.setStyleSheet("QTabWidget::tab {background-color:lightgray;}")
		else:
			self.parent.openNewEntry()
		self.tabChanged(throb=False)

##	def clearHold(self):
##		self.entryHold=False
##
##	def clearContinue(self):
##		self.entryContinue=False

	def removeTab(self,caller):
		# determine the current index of the tab that owns the widget that called this function
		i=self.ui.tabWidget.indexOf(caller)
		# determine the number of tabs BEFORE removal of the tab in question
		count=self.ui.tabWidget.count()
		rprint("removeTab: count="+str(count)+" i="+str(i))
		# remove that tab
		self.ui.tabWidget.removeTab(i)
		# activate the next tab upwards in the stack, if there is one
		if i>1:
			self.ui.tabWidget.setCurrentIndex(i-1)
		# otherwise, activate the tab at the bottom of the stack, if there is one
		elif i<count-3: # count-1 no longer exists; count-2="OLDEST"; count-3=bottom item of the stack
			self.ui.tabWidget.setCurrentIndex(count-3)

		self.tabChanged(throb=False)

		if count<4: # lower the window if the stack is empty
			rprint("lowering: count="+str(count))
			self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint) # disable always on top
			self.lower()

##	def autoCleanupStateChanged(self):
##		if self.ui.autoCleanupCheckBox.isChecked():
##			self.ui.cleanupNowButton.setEnabled(False)
##		else:
##			self.ui.cleanupNowButton.setEnabled(True)

	# cleanup rules:
	# if subject dialog or clue dialog is open, do not increment the tab's idle timer
	# if there is any text in the tab's message field, or if the cleanup checkbox is False, ignore the idle timer or set it to zero on every timer count (never auto-close the tab)
	def autoCleanup(self): # this function is called every second by the timer
		if self.ui.autoCleanupCheckBox.isChecked():
			for tab in newEntryWidget.instances:
# 				rprint("lastModAge:"+str(tab.lastModAge))
				# note the pause happens in newEntryWidget.updateTimer()
				if tab.ui.messageField.text()=="" and tab.lastModAge>60:
					tab.closeEvent(QEvent(QEvent.Close),accepted=False,force=True)
##			if not tab.clueDialogOpen and not tab.subjectLocatedDialogOpen and tab.ui.messageField.text()=="" and time.time()-tab.sec>60:


##class newEntryWidget(QWidget,Ui_newEntryWidget):
####	def __init__(self,parent,i):
##	def __init__(self,parent):
##		QWidget.__init__(self)
##		self.parent=parent
####		self.i=i # unique permanent index of this tab
##		self.ui=Ui_newEntryWidget()
##		self.ui.setupUi(self)
##
##	def accept(self):
##		# 1. process the new entry
##		# 2. remove this tab from the stack
##		# 3. determine what tab to move to next
##		#   - move up if there was anything above this tab
##		#   - otherwise, move down (to bottom?) if there was anything below this tab
##		#   - otherwise (if this was the only tab), close (or minimize?) this dialog
##		print(self.ui.messageField.text())
##		self.parent.removeTab(self)
##
####		super(newEntryTabWidget,self).accept()
##
##	def reject(self):
##		pass
####		super(newEntryTabWidget,self).reject()






##class newEntryWidget(QDialog,Ui_newEntryDialog):
class newEntryWidget(QWidget,Ui_newEntryWidget):
	instances=[]
##	newEntryDialogPositionList=[]
##	newEntryDialogUsedPositionList=[]
##	for n in range(50):
##		newEntryDialogPositionList.append([newEntryDialog_x0+n*newEntryDialog_dx,newEntryDialog_y0+n*newEntryDialog_dy])
##		newEntryDialogUsedPositionList.append(False)
##	def __init__(self,parent,position,sec,formattedLocString='',fleet='',dev='',origLocString='',amendFlag=False,amendRow=None):
	def __init__(self,parent,sec=0,formattedLocString='',fleet='',dev='',origLocString='',amendFlag=False,amendRow=None):
		QDialog.__init__(self)

		self.ui=Ui_newEntryWidget()

		self.amendFlag=amendFlag
		self.amendRow=amendRow
		self.attachedCallsignList=[]
##		self.position=position # dialog x,y to show at
		self.sec=sec
		self.formattedLocString=formattedLocString
		self.origLocString=origLocString
		self.fleet=fleet
		self.dev=dev
		self.parent=parent
		if amendFlag:
			row=parent.radioLog[amendRow]
			self.sec=row[0]
			self.formattedLocString=row[4]
##		newEntryDialog.newEntryDialogUsedPositionList[self.position]=True
		newEntryWidget.instances.append(self)
		self.ui.setupUi(self)

		# blank-out the label under the callsign field if this was a manually / hotkey
		#  generated newEntryWidget; the label only applies to fleetsync-spawned entries
		if not fleet:
			self.ui.label_2.setText("")

		self.setStyleSheet("QPushButton { font-size:9pt; }")
		self.ui.buttonBox.setStyleSheet("font-size:12pt;")
		self.setAttribute(Qt.WA_DeleteOnClose) # so that closeEvent gets called when closed by GUI
		self.palette=QPalette()
		self.setAutoFillBackground(True)
		self.clueDialogOpen=False # only allow one clue dialog at a time per newEntryWidget
		self.subjectLocatedDialogOpen=False

##		# close and accept the dialog as a new entry if message is no user input for 30 seconds

##		QTimer.singleShot(100,lambda:self.changeBackgroundColor(0))

		rprint("newEntryWidget created")
		self.quickTextAddedStack=[]

		self.childDialogs=[] # keep track of exactly which clueDialog or
		  # subjectLocatedDialogs are 'owned' by this NED, for use in closeEvent
		  
##		self.ui.messageField.setToolTip("<table><tr><td>a<td>b<tr><td>c<td>d</table>")
		if amendFlag:
			self.ui.timeField.setText(row[0])
			self.ui.teamField.setText(row[2])
			if row[0]=="TO":
				self.ui.to_fromField.setCurrentIndex(1)
			oldMsg=row[3]
			amendIndex=oldMsg.find('\n[AMENDED')
			if amendIndex>-1:
				self.ui.messageField.setText(row[3][:amendIndex])
			else:
				self.ui.messageField.setText(row[3])
			self.ui.label.setText("AMENDED Message:")
		else:
			self.ui.timeField.setText(time.strftime("%H%M"))
		self.ui.teamField.textChanged.connect(self.setStatusFromTeam)
		self.ui.teamField.textChanged.connect(self.updateTabLabel)
		self.ui.to_fromField.currentIndexChanged.connect(self.updateTabLabel)
		self.ui.messageField.textChanged.connect(self.messageTextChanged)
		self.ui.statusButtonGroup.buttonClicked.connect(self.setStatusFromButton)

		self.ui.teamField.textChanged.connect(self.resetLastModAge)
		self.ui.messageField.textChanged.connect(self.resetLastModAge)
		self.ui.radioLocField.textChanged.connect(self.resetLastModAge)
		self.ui.statusButtonGroup.buttonClicked.connect(self.resetLastModAge)

		self.lastModAge=0

		# add this newEntryWidget as a new tab in the newEntryWindow.ui.tabWidget
		self.parent.newEntryWindow.addTab(time.strftime("%H%M"),self)
		# do not raise the window if there is an active clue report form
      # or an active changeCallsignDialog
		rprint("clueLog.openDialogCount="+str(clueDialog.openDialogCount))
		rprint("changeCallsignDialog.openDialogCount="+str(changeCallsignDialog.openDialogCount))
		rprint("subjectLocatedDialog.openDialogCount="+str(subjectLocatedDialog.openDialogCount))
		rprint("showing")
		self.parent.newEntryWindow.show()
		self.parent.newEntryWindow.setFocus()
		if clueDialog.openDialogCount==0 and subjectLocatedDialog.openDialogCount==0 and changeCallsignDialog.openDialogCount==0:
			rprint("raising")
			self.parent.newEntryWindow.raise_()
		# the following line is needed to get fix the apparent Qt bug (?) that causes
		#  the messageField text to all be selected when a new message comes in
		#  during the continue period.
		self.parent.newEntryWindow.ui.tabWidget.currentWidget().ui.messageField.deselect()

		self.timer=QTimer(self)
		self.timer.start(1000)
		self.timer.timeout.connect(self.updateTimer)

##		# unless an entry is currently being edited, activate the newly added tab
##		if newEntryWidgetHold:
##			blink 1
##		else:
##			self.parent.newEntryWindow.ui.tabWidget.setCurrentIndex(1)

		# update the tab label to include callsign
##		self.ui.teamField.textC
##		rprint("ctrl+z keyBindings:"+str(QKeySequence("Ctrl+Z")))

##		# install actions for messageField
##		for entry in quickTextList:
##			if entry != "separator":
##				rprint("adding:"+entry[0]+" "+str(entry[1]))
##				# calling the slot with arguments: lambda evaluates at the time the action is called, so, won't work here;
##				#  functools.partial evaluates at addAction time so will do what we want.a
##				action=QAction(entry[0],None)
##				action.setShortcutContext(Qt.WidgetShortcut)
##				action.setShortcut(entry[1])
##				self.ui.messageField.addAction(action)
##				action.triggered.connect(functools.partial(self.quickTextAction,entry[0]))
##
##		self.ui.messageField.setContextMenuPolicy(Qt.CustomContextMenu)
##		self.ui.messageField.customContextMenuRequested.connect(self.messageContextMenu)
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
####				self.ui.messageField.addAction(action)
##
####		act2=menu.addAction("STUFF",functools.partial(self.quickTextAction,"STUFF"),"Ctrl+F")
####		self.addAction(act2)
####		f1Action=menu.addAction("DEPARTING IC",self.dummySlot,Qt.Key_F1)
####		f2Action=menu.addAction("BEGINNING ASSIGNMENT")
####		f3Action=menu.addAction("COMPLETED ASSIGNMENT")
####		f4Action=menu.addAction("ARRIVING AT IC")
####		action=menu.exec_(self.ui.messageField.mapToGlobal(pos))
##		menu.exec_(self.ui.messageField.mapToGlobal(pos))
####		if action:
####			self.ui.messageField.setText(action.text())

##	def quickTextAction(self,quickText):
##		rprint("quickText:"+quickText)

##	def changeEvent(self,event):
##		self.throb(0)

	def throb(self,n=0):
		# this function calls itself recursivly 25 times to throb the background blue->white
		self.palette.setColor(QPalette.Background,QColor(n*10,n*10,255))
		self.setPalette(self.palette)
		if n<25:
			QTimer.singleShot(15,lambda:self.throb(n+1))
		else:
			self.palette.setColor(QPalette.Background,QColor(255,255,255))
			self.setPalette(self.palette)

	def updateTimer(self):
		# pause all timers if there are any clue or subject or changeCallsign dialogs open
		if clueDialog.openDialogCount==0 and subjectLocatedDialog.openDialogCount==0 and changeCallsignDialog.openDialogCount==0:
			self.lastModAge+=1
		self.parent.currentEntryLastModAge=self.lastModAge
##		if self.lastModAge>holdSec:
##			if self.entryHold: # each entry widget has its own lastModAge and its last entryHold
##				rprint("releasing entry hold for self")
##				self.parent.entryHold=False

	def resetLastModAge(self):
		rprint("resetting last mod age for "+self.ui.teamField.text())
		self.lastModAge=-1
		self.parent.currentEntryLastModAge=self.lastModAge

	def quickTextAction(self):
		quickText=self.sender().text()
		quickText=re.sub(r' +\[.*$','',quickText) # prune one or more spaces followed by open bracket, thru end
		existingText=self.ui.messageField.text()
		if existingText=="":
			self.quickTextAddedStack.append(quickText)
			self.ui.messageField.setText(quickText)
		else:
			textToAdd="; "+quickText
			self.quickTextAddedStack.append(textToAdd)
			self.ui.messageField.setText(existingText+textToAdd)
		self.ui.messageField.setFocus()

	def quickTextUndo(self):
		rprint("ctrl+z keyBindings:"+str(QKeySequence("Ctrl+Z")))
		if len(self.quickTextAddedStack):
			textToRemove=self.quickTextAddedStack.pop()
			existingText=self.ui.messageField.text()
			self.ui.messageField.setText(rreplace(existingText,textToRemove,'',1))
			self.ui.messageField.setFocus()

	def quickTextClueAction(self): # do not push clues on the quick text stack, to make sure they can't be undone
		rprint(str(self.clueDialogOpen))
		if not self.clueDialogOpen: # only allow one open clue diolog at a time per radio log entry; see init and clueDialog init and closeEvent
			self.newClueDialog=clueDialog(self,self.ui.timeField.text(),self.ui.teamField.text(),self.ui.radioLocField.text(),lastClueNumber+1)
			self.newClueDialog.show()

	def quickTextSubjectLocatedAction(self):
		self.subjectLocatedDialog=subjectLocatedDialog(self,self.ui.timeField.text(),self.ui.teamField.text(),self.ui.radioLocField.text())
		self.subjectLocatedDialog.show()

	# if Enter or Return is pressed while in the teamField, jump to messageField
	#  as if the user pressed the tab key
	def keyPressEvent(self,event):
		key=event.key()
		if key==Qt.Key_Enter or key==Qt.Key_Return:
			if self.ui.teamField.hasFocus():
				self.ui.messageField.setFocus()
			elif self.ui.messageField.hasFocus():
				self.accept()
			else:
				super().keyPressEvent(event) # pass the event as normal
		else:
			super().keyPressEvent(event) # pass the event as normal

	def openChangeCallsignDialog(self):
		# problem: changeCallsignDialog does not stay on top of newEntryWindow!
		# only open the dialog if the newEntryWidget was created from an incoming fleetSync ID
		#  (it has no meaning for hotkey-opened newEntryWidgets)
		rprint("FLEET:'"+str(self.fleet)+"'")
		if self.fleet:
			self.changeCallsignDialog=changeCallsignDialog(self,self.ui.teamField.text(),self.fleet,self.dev)
			self.changeCallsignDialog.exec() # required to make it stay on top

	def accept(self):
		if not self.clueDialogOpen and not self.subjectLocatedDialogOpen:
			# getValues return value: [time,to_from,team,message,self.formattedLocString,status,self.sec,self.fleet,self.dev,self.origLocString]
			rprint("Accepted")
			val=self.getValues()
			if self.amendFlag:
				prevToFrom=self.parent.radioLog[self.amendRow][1]
				newToFrom=self.ui.to_fromField.currentText()
				prevTeam=self.parent.radioLog[self.amendRow][2]
				newTeam=self.ui.teamField.text()
	##			if self.parent.radioLog[self.amendRow][1]!=self.ui.to_fromField.currentText() or self.parent.radioLog[self.amendRow][2]!=self.ui.teamField.text():
				if prevToFrom!=newToFrom or prevTeam!=newTeam:
					tmpTxt=" "+self.parent.radioLog[self.amendRow][1]+" "+self.parent.radioLog[self.amendRow][2]
					# if the old team tab is now empty, remove it
					if prevTeam!=newTeam:
						prevEntryCount=len([entry for entry in self.parent.radioLog if entry[2]==prevTeam])
						rprint("number of entries for the previous team:"+str(prevEntryCount))
						if prevEntryCount==1:
							prevExtTeamName=getExtTeamName(prevTeam)
							self.parent.deleteTeamTab(prevExtTeamName)
				else:
					tmpTxt=""
				# oldMsg = entire message value before the amendment is accepted; may have previous amendments
				# lastMsg = only the last message, i.e. oldMsg minus any previous amendments
				oldMsg=self.parent.radioLog[self.amendRow][3]
				amendIndex=oldMsg.find('\n[AMENDED')
				if amendIndex>-1:
					lastMsg=oldMsg[:amendIndex]
					olderMsgs=oldMsg[amendIndex:]
				else:
					lastMsg=oldMsg
					olderMsgs=''
				niceTeamName=val[2]
				status=val[5]
	
				# update radioLog items that may have been amended
				self.parent.radioLog[self.amendRow][1]=val[1]
				self.parent.radioLog[self.amendRow][2]=niceTeamName
				self.parent.radioLog[self.amendRow][3]=self.ui.messageField.text()+"\n[AMENDED "+time.strftime('%H%M')+"; WAS"+tmpTxt+": '"+lastMsg+"']"+olderMsgs
				self.parent.radioLog[self.amendRow][5]=status
	
				# use to_from value "AMEND" and blank msg text to make sure team timer does not reset
				self.parent.newEntryProcessTeam(niceTeamName,status,"AMEND","")
			else:
				self.parent.newEntry(self.getValues())
	
			# make entries for attached callsigns
			# values array format: [time,to_from,team,message,locString,status,sec,fleet,dev]
			rprint("attached callsigns: "+str(self.attachedCallsignList))
			for attachedCallsign in self.attachedCallsignList:
				v=val[:] # v is a fresh, independent copy of val for each iteration
				v[2]=getNiceTeamName(attachedCallsign)
				v[3]="[ATTACHED FROM "+self.ui.teamField.text().strip()+"] "+val[3]
				self.parent.newEntry(v)
	
			self.parent.totalEntryCount+=1
			if self.parent.totalEntryCount%5==0: # rotate backup files after every 5 entries
				rotateCsvBackups(self.parent.firstWorkingDir+"\\"+self.parent.csvFileName)
				rotateCsvBackups(self.parent.firstWorkingDir+"\\"+self.parent.csvFileName.replace(".csv","_clueLog.csv"))
				rotateCsvBackups(self.parent.firstWorkingDir+"\\"+self.parent.fsFileName)
				rotateCsvBackups(self.parent.secondWorkingDir+"\\"+self.parent.csvFileName)
				rotateCsvBackups(self.parent.secondWorkingDir+"\\"+self.parent.csvFileName.replace(".csv","_clueLog.csv"))
				rotateCsvBackups(self.parent.secondWorkingDir+"\\"+self.parent.fsFileName)
	
			rprint("Accepted2")
		
		self.closeEvent(QEvent(QEvent.Close),True)
##		self.close()

# 	def reject(self):
# 		really=QMessageBox.warning(self,"Please Confirm","Cancel this entry?\nIt cannot be recovered.",
# 			QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
# 		if really==QMessageBox.Yes:
# 			self.closeEvent(None)

##		self.timer.stop()
##
####	def closeEvent(self):
##		self.parent.newEntryWindow.ui.tabWidget.removeTab(self.parent.newEntryWindow.ui.tabWidget.indexOf(self))
##		newEntryWidget.instances.remove(self)
##		self.close()

##	def closeEvent(self,event):
##		newEntryDialog.newEntryDialogUsedPositionList[self.position]=False
##		newEntryDialog.instances.remove(self)
##		self.timer.stop() # otherwise it keeps accepting even after closed!

	
	
	
# 	def closeEvent(self,event,accepted=False):
# 		# note, this type of messagebox is needed to show above all other dialogs for this application,
# 		#  even the ones that have WindowStaysOnTopHint.  This works in Vista 32 home basic.
# 		#  if it didn't show up on top, then, there would be no way to close the radiolog other than kill.
# 		rprint("closeEvent called: accepted="+str(accepted))
# 		if not accepted:
# 			really=QMessageBox(QMessageBox.Warning,"Please Confirm","Close this Clue Report Form?\nIt cannot be recovered.",
# 				QMessageBox.Yes|QMessageBox.Cancel,self,Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
# 			if really.exec()==QMessageBox.Cancel:
# 				event.ignore()
# 				return
# 
# 		clueDialog.indices[self.i]=False # free up the dialog box location for the next one
# 		self.parent.clueDialogOpen=False
# 		clueDialog.openDialogCount-=1
# ##		newEntryWidget.instances.remove(self)






	def closeEvent(self,event,accepted=False,force=False):
		# if the user hit cancel, make sure the user really wanted to cancel
		if not accepted and not force:
			really=QMessageBox.warning(self,"Please Confirm","Cancel this entry?\nIt cannot be recovered.",
				QMessageBox.Yes|QMessageBox.No,QMessageBox.No)
			if really==QMessageBox.No:
				event.ignore()
				return
		# whether OK or Cancel, ignore the event if child dialog(s) are open,
		#  and raise the child window(s)
		if self.clueDialogOpen or self.subjectLocatedDialogOpen:
			QMessageBox.warning(self,"Cannot close","A Clue Report or Subject Located form is open that belongs to this entry.  Finish it first.")
			# the 'child' dialogs are not technically children; use the NED's
			#  childDialogs attribute instead, which was populated in the __init__
			#  of each child dialog class
			for child in self.childDialogs:
				child.raise_()
			event.ignore()
			return
		else:
			self.timer.stop()
			# if there is a pending GET request (locator), send it now with the
			#  specified callsign
			self.parent.sendPendingGet(self.ui.teamField.text())
	##		self.parent.newEntryWindow.ui.tabWidget.removeTab(self.parent.newEntryWindow.ui.tabWidget.indexOf(self))
	##		self.parent.newEntryWindow.removeTab(self.parent.newEntryWindow.ui.tabWidget.indexOf(self))
			self.parent.newEntryWindow.removeTab(self)
			newEntryWidget.instances.remove(self)
			rprint("closed")
##		else:
##			event.ignore()

	def setStatusFromTeam(self):
##		self.timer.start(newEntryDialogTimeoutSeconds*1000) # reset the timeout
		extTeamName=getExtTeamName(self.ui.teamField.text())
		if (extTeamName in teamStatusDict) and (teamStatusDict[extTeamName]!=''):
			prevStatus=teamStatusDict[extTeamName]
#			print("Team "+extTeamName+": previous status='"+prevStatus+"'")
			for button in self.ui.statusButtonGroup.buttons():
				if button.text()==prevStatus:
					button.setChecked(True)
		else:
#			print("unknown team, or existing team with no existing status")
			# must setExclusive(False) to allow unselecting all buttons,
			# then set it back to True afterwards
			self.ui.statusButtonGroup.setExclusive(False)
			for button in self.ui.statusButtonGroup.buttons():
				button.setChecked(False)
			self.ui.statusButtonGroup.setExclusive(True)

##	def updateBannerText(self):
##		if self.amendFlag:
##			tmpTxt="AMENDED ENTRY"
##		else:
##			tmpTxt="New Entry"
##		self.setWindowTitle("Radio Log - "+tmpTxt+" - "+self.ui.to_fromField.currentText()+" "+self.ui.teamField.text())

	def messageTextChanged(self): # gets called after every keystroke or button press, so, should be fast
##		self.timer.start(newEntryDialogTimeoutSeconds*1000) # reset the timeout
		message=self.ui.messageField.text().lower()
		extTeamName=getExtTeamName(self.ui.teamField.text())
		prevStatus=""
		if extTeamName in teamStatusDict:
			prevStatus=teamStatusDict[extTeamName]
		newStatus="" #  need to actively set it back to blank if neeeded, since this function is called on every text change
		# use an if/elif/else clause, which requires a search order; use the more final messages first
		# note, these hints can be trumped by clicking the status button AFTER typing
		if "at ic" in message:
			newStatus="At IC"
		elif "requesting transport" in message:
			newStatus="Waiting for Transport"
		elif "enroute to ic" in message:
			newStatus="In Transit"
		elif "starting assignment" in message:
			newStatus="Working"
		elif "departing ic" in message:
			newStatus="In Transit"
		elif "standby" in message:
			newStatus="STANDBY"
		elif "hold position" in message:
			newStatus="STANDBY"
		elif "requesting deputy" in message:
			newStatus="STANDBY"
		else:
			newStatus=prevStatus
		
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
		self.attachedCallsignList=[]
		lowerMessage=message.lower()
		if "with" in lowerMessage or "w/" in lowerMessage:
			tailIndex=lowerMessage.find("with")+4
			if tailIndex<4:
				tailIndex=lowerMessage.find("w/")+2
			if tailIndex>1:
				tail=message[tailIndex:].strip()
				#massage the tail to get it into a good format here
				tail=re.sub(r'(\w)\s+(\d+)',r'\1\2',tail) # remove space after letters before numbers
				tail=re.sub(r't(\d+)',r'team\1',tail) # change t# to team#
				tail=re.sub(r'([\s,]+)(\d+)',r'\1team\2',tail) # insert 'team' before just-numbers
				tail=re.sub(r'^(\d+)',r'team\1',tail) # and also at the start of the tail
				tail=re.sub(r'team',r'Team',tail) # capitalize 'team'
	# 			rprint(" 'with' tail found:"+tail)
				tailParse=re.split("[, ]+",tail)
				# rebuild the attachedCallsignList from scratch on every keystroke;
				#  trying to append to the list is problematic (i.e. when do we append?)
				for token in tailParse:
					if token!="and": # all parsed tokens other than "and" are callsigns to be attached
						# keep the list as a local variable rather than object attribute,
						#  since we want to rebuild the entire list on every keystroke
						self.attachedCallsignList.append(token)
		self.ui.attachedField.setText(" ".join(self.attachedCallsignList))
			
		# allow it to be set back to blank; must set exclusive to false and iterate over each button
		self.ui.statusButtonGroup.setExclusive(False)
		for button in self.ui.statusButtonGroup.buttons():
			if button.text()==newStatus:
				button.setChecked(True)
			else:
				button.setChecked(False)
		self.ui.statusButtonGroup.setExclusive(True)

	def setStatusFromButton(self):
##		self.timer.start(newEntryDialogTimeoutSeconds*1000) # reset the timeout
		clickedStatus=self.ui.statusButtonGroup.checkedButton().text()
		extTeamName=getExtTeamName(self.ui.teamField.text())
		teamStatusDict[extTeamName]=clickedStatus

	def updateTabLabel(self):
		i=self.parent.newEntryWindow.ui.tabWidget.indexOf(self)
		self.parent.newEntryWindow.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).layout().itemAt(1).widget().setText(time.strftime("%H%M")+" "+self.ui.to_fromField.currentText()+" "+self.ui.teamField.text())
##		self.parent.newEntryWindow.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).setText(self.ui.teamField.text())
##		self.parent.newEntryWindow.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).adjustSize()

	def getValues(self):
		time=self.ui.timeField.text()
		to_from=self.ui.to_fromField.currentText()
		team=self.ui.teamField.text().strip() # remove leading and trailing spaces
		message=self.ui.messageField.text()
#		location=self.ui.radioLocField.text()
		status=''
		if self.ui.statusButtonGroup.checkedButton()!=None:
			status=self.ui.statusButtonGroup.checkedButton().text()
		return [time,to_from,team,message,self.formattedLocString,status,self.sec,self.fleet,self.dev,self.origLocString]


class clueDialog(QDialog,Ui_clueDialog):
##	instances=[]
	openDialogCount=0
	indices=[False]*20 # allow up to 20 clue dialogs open at the same time
	dx=20
	dy=20
	x0=200
	y0=200
	def __init__(self,parent,t,callsign,radioLoc,newClueNumber):
		QDialog.__init__(self)
		self.ui=Ui_clueDialog()
		self.ui.setupUi(self)
		self.setStyleSheet("QPushButton { font-size:9pt; }")
		self.ui.buttonBox.setStyleSheet("font-size:12pt;")
		self.ui.timeField.setText(t)
		self.ui.dateField.setText(time.strftime("%x"))
		self.ui.callsignField.setText(callsign)
		self.ui.radioLocField.setText(radioLoc)
		self.ui.clueNumberField.setText(str(newClueNumber))
		self.clueQuickTextAddedStack=[]
		self.parent=parent
		self.parent.childDialogs.append(self)
##		self.parent.timer.stop() # do not timeout the new entry dialog if it has a child clueDialog open!
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
##		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.ui.descriptionField.setFocus()
##		self.i=0 # dialog box location index; set at runtime, so we know which index to free on close
##		clueDialog.instances.append(self)
		[x,y,i]=self.pickXYI()
		self.move(x,y)
		self.i=i # save the index so we can clear it on close
		# save the clue number at init time, so that any new clueDialog opened before this one
		#  is saved will have an incremented clue number.  May need to get fancier in terms
		#  of releasing clue numbers on reject, but, don't worry about it for now - that's why
		#  the clue number field is editable.
		global lastClueNumber
		lastClueNumber=newClueNumber
		self.parent.clueDialogOpen=True
		clueDialog.openDialogCount+=1
		self.values=self.parent.getValues()
		self.values[3]="RADIO LOG SOFTWARE: 'LOCATED A CLUE' button pressed; radio operator is gathering details"
##		self.values[3]="RADIO LOG SOFTWARE: 'LOCATED A CLUE' button pressed for '"+self.values[2]+"'; radio operator is gathering details"
##		self.values[2]='' # this message is not actually from a team
		self.parent.parent.newEntry(self.values)

	def pickXYI(self):
		for index in range(len(clueDialog.indices)):
			if clueDialog.indices[index]==False:
				clueDialog.indices[index]=True
				return [index*clueDialog.dx+clueDialog.x0,index*clueDialog.dy+clueDialog.y0,index]

	# treat Enter or Return like Tab: cycle through fields similar to tab sequence, and accept after last field
	def keyPressEvent(self,event):
		key=event.key()
		if key==Qt.Key_Enter or key==Qt.Key_Return:
			if self.ui.descriptionField.hasFocus():
				self.ui.locationField.setFocus()
			elif self.ui.locationField.hasFocus(): # make sure this is elif, not if - otherwise it just cascades!
				self.ui.instructionsField.setFocus()
			elif self.ui.instructionsField.hasFocus():
				self.accept()
			else:
				super().keyPressEvent(event) # pass the event as normal
		else:
			super().keyPressEvent(event) # pass the event as normal

	def accept(self):
##		self.parent.timer.start(newEntryDialogTimeoutSeconds*1000) # reset the timeout
		number=self.ui.clueNumberField.text()
		description=self.ui.descriptionField.toPlainText()
		location=self.ui.locationField.text()
		instructions=self.ui.instructionsField.text()
		team=self.ui.callsignField.text()
		clueDate=self.ui.dateField.text()
		clueTime=self.ui.timeField.text()
		radioLoc=self.ui.radioLocField.text()

		# validation: description, location, instructions fields must all be non-blank
		vText=""
		if description=="":
			vText+="\n'Description' cannot be blank."
		if location=="":
			vText+="\n'Location' cannot be blank."
		if instructions=="":
			vText+="\n'Instructions' cannot be blank."
		rprint("vText:"+vText)
		if vText!="":
			self.clueMsgBox=QMessageBox(QMessageBox.Critical,"Error","Please complete the form and try again:\n"+vText,
				QMessageBox.Ok,self,Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			self.clueMsgBox.show()
			return

		self.parent.clueLogNeedsPrint=True
		textToAdd=''
		existingText=self.parent.ui.messageField.text()
		if existingText!='':
			textToAdd='; '
		textToAdd+="CLUE#"+number+": "+description+"; LOCATION: "+location+"; INSTRUCTIONS: "+instructions
		self.parent.ui.messageField.setText(existingText+textToAdd)
		# previously, lastClueNumber was saved here - on accept; we need to save it on init instead, so that
		#  multiple concurrent clueDialogs will not have the same clue number!
		# header_labels=['CLUE#','DESCRIPTION','TEAM','TIME','DATE','OP','LOCATION','INSTRUCTIONS','RADIO LOC.']
		clueData=[number,description,team,clueTime,clueDate,self.parent.parent.opPeriod,location,instructions,radioLoc]
		self.parent.parent.clueLog.append(clueData)
		if self.ui.clueReportPrintCheckBox.isChecked():
			self.parent.parent.printClueReport(clueData)
		rprint("accepted - calling close")
		self.parent.parent.clueLogDialog.ui.tableView.model().layoutChanged.emit()
		self.closeEvent(QEvent(QEvent.Close),True)
##		pixmap=QPixmap(":/radiolog_ui/print_icon.png")
##		self.parent.parent.clueLogDialog.ui.tableView.model().setHeaderData(0,Qt.Vertical,pixmap,Qt.DecorationRole)
##		self.parent.parent.clueLogDialog.ui.tableView.model().setHeaderData(1,Qt.Vertical,pixmap,Qt.DecorationRole)
##		self.parent.parent.clueLogDialog.ui.tableView.model().headerDataChanged.emit(Qt.Vertical,0,1)
##		# don't try self.close() here - it can cause the dialog to never close!  Instead use super().accept()
		super(clueDialog,self).accept()

	def closeEvent(self,event,accepted=False):
		# note, this type of messagebox is needed to show above all other dialogs for this application,
		#  even the ones that have WindowStaysOnTopHint.  This works in Vista 32 home basic.
		#  if it didn't show up on top, then, there would be no way to close the radiolog other than kill.
		if not accepted:
			really=QMessageBox(QMessageBox.Warning,"Please Confirm","Close this Clue Report Form?\nIt cannot be recovered.",
				QMessageBox.Yes|QMessageBox.Cancel,self,Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			if really.exec()==QMessageBox.Cancel:
				event.ignore()
				return	
			self.values=self.parent.getValues()
			self.values[3]="RADIO LOG SOFTWARE: radio operator has canceled the 'LOCATED A CLUE' form"
			self.parent.parent.newEntry(self.values)
		
		clueDialog.indices[self.i]=False # free up the dialog box location for the next one
		self.parent.clueDialogOpen=False
		clueDialog.openDialogCount-=1
		self.parent.childDialogs.remove(self)
		event.accept()
##		newEntryWidget.instances.remove(self)

	def clueQuickTextAction(self):
		quickText=self.sender().text()
		quickText=re.sub(r' +\[.*$','',quickText) # prune one or more spaces followed by open bracket, thru end
		quickText=re.sub(r'&&','&',quickText) # double-ampersand is needed in Qt designer for a literal ampersand
		existingText=self.ui.instructionsField.text()
		if existingText=="":
			self.clueQuickTextAddedStack.append(quickText)
			self.ui.instructionsField.setText(quickText)
		else:
			textToAdd="; "+quickText
			self.clueQuickTextAddedStack.append(textToAdd)
			self.ui.instructionsField.setText(existingText+textToAdd)
		self.ui.instructionsField.setFocus()

	def clueQuickTextUndo(self):
		rprint("ctrl+z keyBindings:"+str(QKeySequence("Ctrl+Z")))
		if len(self.clueQuickTextAddedStack):
			textToRemove=self.clueQuickTextAddedStack.pop()
			existingText=self.ui.instructionsField.text()
			self.ui.instructionsField.setText(rreplace(existingText,textToRemove,'',1))
			self.ui.instructionsField.setFocus()


class nonRadioClueDialog(QDialog,Ui_nonRadioClueDialog):
	def __init__(self,parent,t,newClueNumber):
		QDialog.__init__(self)
		self.ui=Ui_nonRadioClueDialog()
		self.ui.setupUi(self)
		self.ui.buttonBox.setStyleSheet("font-size:16pt;")
		self.ui.timeField.setText(t)
		self.ui.dateField.setText(time.strftime("%x"))
		self.ui.clueNumberField.setText(str(newClueNumber))
		self.parent=parent
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		self.setAttribute(Qt.WA_DeleteOnClose)
		# values format for adding a new entry:
		#  [time,to_from,team,message,self.formattedLocString,status,self.sec,self.fleet,self.dev,self.origLocString]
		self.values=["" for n in range(10)]
		self.values[0]=t
		self.values[3]="RADIO LOG SOFTWARE: 'ADD NON-RADIO CLUE' button pressed; radio operator is gathering details"
		self.values[6]=time.time()
		self.parent.newEntry(self.values)
		
	def accept(self):
		self.parent.clueLogNeedsPrint=True
		number=self.ui.clueNumberField.text()
		description=self.ui.descriptionField.toPlainText()
		location=self.ui.locationField.text()
		instructions=self.ui.instructionsField.text()
		team=self.ui.callsignField.text()
		clueDate=self.ui.dateField.text()
		clueTime=self.ui.timeField.text()
		radioLoc=''
		textToAdd=''
		global lastClueNumber
		lastClueNumber=int(self.ui.clueNumberField.text())
		# header_labels=['CLUE#','DESCRIPTION','TEAM','TIME','DATE','OP','LOCATION','INSTRUCTIONS','RADIO LOC.']
		clueData=[number,description,team,clueTime,clueDate,self.parent.opPeriod,location,instructions,radioLoc]
		self.parent.clueLog.append(clueData)
		
		# add a radio log entry too
		self.values=["" for n in range(10)]
		self.values[0]=self.ui.timeField.text()
		self.values[3]="CLUE#"+number+"(NON-RADIO): "+description+"; REPORTED BY: "+team+"; see clue report and clue log for details"
		self.values[6]=time.time()
		self.parent.newEntry(self.values)
		
		if self.ui.clueReportPrintCheckBox.isChecked():
			self.parent.printClueReport(clueData)
		rprint("accepted - calling close")
##		# don't try self.close() here - it can cause the dialog to never close!  Instead use super().accept()
		self.parent.clueLogDialog.ui.tableView.model().layoutChanged.emit()
		super(nonRadioClueDialog,self).accept()

	def closeEvent(self,event,accepted=False):
		# note, this type of messagebox is needed to show above all other dialogs for this application,
		#  even the ones that have WindowStaysOnTopHint.  This works in Vista 32 home basic.
		#  if it didn't show up on top, then, there would be no way to close the radiolog other than kill.
		if not accepted:
			really=QMessageBox(QMessageBox.Warning,"Please Confirm","Close this Clue Report Form?\nIt cannot be recovered.",
				QMessageBox.Yes|QMessageBox.Cancel,self,Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			if really.exec()==QMessageBox.Cancel:
				event.ignore()
				return
			self.values=["" for n in range(10)]
			self.values[0]=self.ui.timeField.text()
			self.values[3]="RADIO LOG SOFTWARE: radio operator has canceled the 'NON-RADIO CLUE' form"
			self.values[6]=time.time()
			self.parent.newEntry(self.values)
# 	def reject(self):
# ##		self.parent.timer.start(newEntryDialogTimeoutSeconds*1000) # reset the timeout
# 		rprint("rejected - calling close")
# 		# don't try self.close() here - it can cause the dialog to never close!  Instead use super().reject()
# 		self.closeEvent(None)
# 		super(nonRadioClueDialog,self).reject()


class clueLogDialog(QDialog,Ui_clueLogDialog):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.ui=Ui_clueLogDialog()
		self.ui.setupUi(self)
		self.parent=parent
		self.tableModel = clueTableModel(parent.clueLog, self)
		self.ui.tableView.setStyleSheet("font-size:"+str(parent.fontSize)+"pt")
		self.ui.tableView.setModel(self.tableModel)

		self.ui.tableView.verticalHeader().setVisible(True)
		self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
		self.ui.tableView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

		# automatically expand the 'description' and 'instructions' column widths to fill available space and wrap if needed
		self.ui.tableView.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)
		self.ui.tableView.horizontalHeader().setSectionResizeMode(7,QHeaderView.Stretch)

		self.ui.tableView.verticalHeader().sectionClicked.connect(self.headerClicked)
		self.ui.addNonRadioClueButton.clicked.connect(self.parent.addNonRadioClue)
		self.ui.printButton.clicked.connect(self.parent.printClueLogDialog.show)

		self.ui.tableView.setSelectionMode(QAbstractItemView.NoSelection)
		self.ui.tableView.setFocusPolicy(Qt.NoFocus)

	def showEvent(self,event):
		self.ui.tableView.resizeRowsToContents()
		self.ui.tableView.scrollToBottom()

	def resizeEvent(self,event):
		self.ui.tableView.resizeRowsToContents()
		self.ui.tableView.scrollToBottom()

	def headerClicked(self,section):
		clueData=self.parent.clueLog[section]
		clueNum=clueData[0]
		if clueNum!="": # pass through if clicking a non-clue row
			if QMessageBox.question(self,"Confirm - Print Clue Report","Print Clue Report for Clue #"+str(clueNum)+"?",QMessageBox.Yes|QMessageBox.Cancel)==QMessageBox.Yes:
				self.parent.printClueReport(clueData)


class subjectLocatedDialog(QDialog,Ui_subjectLocatedDialog):
	openDialogCount=0
	def __init__(self,parent,t,callsign,radioLoc):
		QDialog.__init__(self)
		self.ui=Ui_subjectLocatedDialog()
		self.ui.setupUi(self)
		self.ui.timeField.setText(t)
		self.ui.dateField.setText(time.strftime("%x"))
		self.ui.callsignField.setText(callsign)
		self.ui.radioLocField.setText(radioLoc)
		self.parent=parent
		self.parent.subjectLocatedDialogOpen=True
		self.parent.childDialogs.append(self)
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.ui.locationField.setFocus()
		self.values=self.parent.getValues()
		self.values[3]="RADIO LOG SOFTWARE: 'SUBJECT LOCATED' button pressed; radio operator is gathering details"
		self.parent.parent.newEntry(self.values)
		subjectLocatedDialog.openDialogCount+=1

	def accept(self):
		location=self.ui.locationField.text()
		condition=self.ui.conditionField.toPlainText()
		resources=self.ui.resourcesField.toPlainText()
		other=self.ui.otherField.toPlainText()
		team=self.ui.callsignField.text()
		subjDate=self.ui.dateField.text()
		subjTime=self.ui.timeField.text()
		radioLoc=self.ui.radioLocField.text()

		# validation: description, location, instructions fields must all be non-blank
		vText=""
		if location=="":
			vText+="\n'Location' cannot be blank."
		if condition=="":
			vText+="\n'Condition' cannot be blank."
		if resources=="":
			vText+="\n'Resources Needed' cannot be blank."
		rprint("vText:"+vText)
		if vText!="":
			self.clueMsgBox=QMessageBox(QMessageBox.Critical,"Error","Please complete the form and try again:\n"+vText,
				QMessageBox.Ok,self,Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			self.clueMsgBox.show()
			return

		textToAdd=''
		existingText=self.parent.ui.messageField.text()
		if existingText!='':
			textToAdd='; '
		textToAdd+="SUBJECT LOCATED: LOCATION: "+location+"; CONDITION: "+condition+"; RESOURCES NEEDED: "+resources
		if other!='':
			textToAdd+="; "+other
		self.parent.ui.messageField.setText(existingText+textToAdd)
		self.closeEvent(QEvent(QEvent.Close),True)
		super(subjectLocatedDialog,self).accept()

# 	def reject(self):
# 		rprint("rejected - calling close")
# 		# don't try self.close() here - it can cause the dialog to never close!  Instead use super().reject()
# 		self.closeEvent(None)
# 		self.values=self.parent.getValues()
# 		self.values[3]="RADIO LOG SOFTWARE: radio operator has canceled the 'SUBJECT LOCATED' form"
# 		self.parent.parent.newEntry(self.values)
# 		super(subjectLocatedDialog,self).reject()

	def closeEvent(self,event,accepted=False):
		# note, this type of messagebox is needed to show above all other dialogs for this application,
		#  even the ones that have WindowStaysOnTopHint.  This works in Vista 32 home basic.
		#  if it didn't show up on top, then, there would be no way to close the radiolog other than kill.
		if not accepted:
			really=QMessageBox(QMessageBox.Warning,"Please Confirm","Close this Subject Located form?\nIt cannot be recovered.",
				QMessageBox.Yes|QMessageBox.Cancel,self,Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			if really.exec()==QMessageBox.Cancel:
				event.ignore()
				return
			self.values=self.parent.getValues()
			self.values[3]="RADIO LOG SOFTWARE: radio operator has canceled the 'SUBJECT LOCATED' form"
			self.parent.parent.newEntry(self.values)
		self.parent.subjectLocatedDialogOpen=False
		subjectLocatedDialog.openDialogCount-=1
		self.parent.childDialogs.remove(self)


class printClueLogDialog(QDialog,Ui_printClueLogDialog):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.ui=Ui_printClueLogDialog()
		self.ui.setupUi(self)
		self.parent=parent
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)

	def showEvent(self,event):
		itemsToAdd=sorted(list(set([str(clue[5]) for clue in self.parent.clueLog if str(clue[5])!=""])))
		self.ui.opPeriodComboBox.clear()
		self.ui.opPeriodComboBox.addItems(itemsToAdd)

	def accept(self):
		opPeriod=self.ui.opPeriodComboBox.currentText()
		self.parent.printClueLog(opPeriod)
		super(printClueLogDialog,self).accept()

# actions to be performed when changing the operational period:
# - bring up print dialog for current OP if checked (and wait until it is closed)
# - delete team tabs for 'At IC' teams if checked
# - change the OP variable
# - change the OP button text
# - add radio log entry (and clue log entry) 'Operational Period # Begins: <date>'
# - add new op period to list of available op periods in print dialog

# other parts of the flow that are dependent on operational period:
# - print tools use the 'Operational Period # Begins:' entry to filter rows to print
# - clue dialog and clue log
# - filenames:
#  - radio log .csv, clue log .csv - do NOT include op period in filename, since
#        one file per incident includes all op periods
#  - generated radio log and clue log pdf - DO include op period in filename,
#        since each pdf only covers one op period

class opPeriodDialog(QDialog,Ui_opPeriodDialog):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.ui=Ui_opPeriodDialog()
		self.ui.setupUi(self)
		self.parent=parent
		self.ui.currentOpPeriodField.setText(str(parent.opPeriod))
		self.ui.newOpPeriodField.setText(str(parent.opPeriod+1))
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)

	def accept(self):
		if self.ui.printCheckBox.isChecked():
			self.parent.printDialog.exec() # instead of show(), to pause execution until the print dialog is closed

		if self.ui.deleteTabsCheckBox.isChecked():
			for extTeamName in teamStatusDict:
				status=teamStatusDict[extTeamName]
				if status == "At IC":
					self.parent.deleteTeamTab(getNiceTeamName(extTeamName))

		self.parent.opPeriod=int(self.ui.newOpPeriodField.text())
		self.parent.ui.opPeriodButton.setText("OP "+str(self.parent.opPeriod))
		opText="Operational Period "+str(self.parent.opPeriod)+" Begins: "+time.strftime("%a %b %d, %Y")
		self.parent.newEntry([time.strftime("%H%M"),"","",opText,"","",time.time(),"",""])
##      clueData=[number,description,team,clueTime,clueDate,self.parent.parent.opPeriod,location,instructions,radioLoc]
		self.parent.clueLog.append(['',opText,'',time.strftime("%H%M"),'','','','',''])
		self.parent.printDialog.ui.opPeriodComboBox.addItem(self.ui.newOpPeriodField.text())
		super(opPeriodDialog,self).accept()


class changeCallsignDialog(QDialog,Ui_changeCallsignDialog):
	openDialogCount=0
	def __init__(self,parent,callsign,fleet,device):
		QDialog.__init__(self)
		self.ui=Ui_changeCallsignDialog()
		self.ui.setupUi(self)
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.parent=parent
		self.currentCallsign=callsign

		self.ui.fleetField.setText(fleet)
		self.ui.deviceField.setText(device)
		self.ui.currentCallsignField.setText(callsign)
		self.ui.newCallsignField.setFocus()
		self.ui.newCallsignField.setText("Team  ")
		self.ui.newCallsignField.setSelection(5,1)
		changeCallsignDialog.openDialogCount+=1

	def accept(self):
		found=False
		# change existing device entry if found, otherwise add a new entry
		for n in range(len(self.parent.parent.fsLookup)):
			entry=self.parent.parent.fsLookup[n]
			if entry[0]==self.ui.fleetField.text() and entry[1]==self.ui.deviceField.text():
				found=True
				self.parent.parent.fsLookup[n][2]=self.ui.newCallsignField.text()
		if not found:
			self.parent.parent.fsLookup.append([self.ui.fleetField.text(),self.ui.deviceField.text(),self.ui.newCallsignField.text()])
		# set the current radio log entry teamField also
		self.parent.ui.teamField.setText(self.ui.newCallsignField.text())
		# save the updated table (filename is set at the same times that csvFilename is set)
		self.parent.parent.fsSaveLookup()
		# finally, pass the 'accept' signal on up the tree as usual
		changeCallsignDialog.openDialogCount-=1
		self.parent.parent.sendPendingGet(self.ui.newCallsignField.text())
		self.parent.ui.messageField.setFocus()
		super(changeCallsignDialog,self).accept()


##class convertDialog(QDialog,Ui_convertDialog):
##	def __init__(self,parent,rowData,rowHasRadioLoc=False,rowHasMsgCoords=False):
##		QDialog.__init__(self)
##		self.ui=Ui_convertDialog()
##		self.ui.setupUi(self)
##		self.parent=parent
##		self.setWindowFlags(Qt.WindowStaysOnTopHint)
##		self.setAttribute(Qt.WA_DeleteOnClose)
##
##		metrix=QFontMetrics(self.ui.msgField.font())
##		origText=rowData[0]+" "+rowData[1]+" "+rowData[2]+" : "+rowData[3]
##		clippedText=metrix.elidedText(origText,Qt.ElideRight,self.ui.msgField.width())
##		self.ui.msgField.setText(clippedText)
##
##		if not rowHasRadioLoc:
##			self.ui.useRadioLocButton.setEnabled(False)
##			self.ui.useCoordsInMessageButton.setChecked(True)
##		if not rowHasMsgCoords:
##			self.ui.useCoordsInMessageButton.setEnabled(False)
##			self.ui.useRadioLocButton.setChecked(True)
##
##		# initially set the target datum and format to the first choice that is not the same as the current log datum and format
##		datums=[self.ui.datumComboBox.itemText(i) for i in range(self.ui.datumComboBox.count())]
##		formats=[self.ui.formatComboBox.itemText(i) for i in range(self.ui.formatComboBox.count())]
##		self.ui.datumComboBox.setCurrentText([datum for datum in datums if not datum==self.parent.datum][0])
##		self.ui.formatComboBox.setCurrentText([coordFormat for coordFormat in formats if not coordFormat==self.parent.coordFormat][0])
##
##		if self.ui.useRadioLocButton.isChecked():
##			self.ui.origCoordsField.setText(rowData[9])
##		else:
##			self.ui.origCoordsField.setText("")
##		self.ui.origDatumFormatLabel.setText(self.parent.datum+"  "+self.parent.coordFormat)
##
##		self.ui.goButton.clicked.connect(self.go)
##
####	def getCoordsFromString(self,string):
####		#1. parse into tokens, splitting on whitespace, comma, semicolon
####		#2. look for a pair of adjacent tokens that each have numbers in them
##
##	def go(self):
##		rprint("CONVERTING")


class clueTableModel(QAbstractTableModel):
	header_labels=['#','DESCRIPTION','TEAM','TIME','DATE','O.P.','LOCATION','INSTRUCTIONS','RADIO LOC.']
	def __init__(self,datain,parent=None,*args):
		QAbstractTableModel.__init__(self,parent,*args)
		self.arraydata=datain
		self.printIconPixmap=QPixmap(20,20)
		self.printIconPixmap.load(":/radiolog_ui/print_icon.png")
##		self.setEditTriggers(QAbstractItemView.NoEditTriggers)


	def headerData(self,section,orientation,role=Qt.DisplayRole):
		if orientation==Qt.Vertical:
			if role==Qt.DecorationRole and self.arraydata[section][0]!="":
				#icon and button won't display correctly in this use case; just make the entire header item clickable
				return self.printIconPixmap
			if role==Qt.DisplayRole:
				return ""
		if role==Qt.DisplayRole and orientation==Qt.Horizontal:
			return self.header_labels[section]
		return QAbstractTableModel.headerData(self,section,orientation,role)

	def rowCount(self, parent):
		return len(self.arraydata)

	def columnCount(self, parent):
		if len(self.arraydata)>0:
			return len(self.arraydata[0])
		else:
			return len(clueTableModel.header_labels)

	def data(self, index, role):
		if not index.isValid():
			return QVariant()
		elif role != Qt.DisplayRole:
			return QVariant()
		try:
			rval=QVariant(self.arraydata[index.row()][index.column()])
		except:
			row=index.row()
			col=index.column()
			rprint("Row="+str(row)+" Col="+str(col))
			rprint("arraydata:")
			rprint(self.arraydata)
		else:
			return rval

	def dataChangedAll(self):
		self.dataChanged.emit(self.createIndex(0,0),self.createIndex(self.rowCount(self)-1,self.columnCount(self)-1))


class MyTableModel(QAbstractTableModel):
	header_labels=['TIME','T/F','TEAM','MESSAGE','RADIO LOC.','STATUS','sec','fleet','dev','origLoc']
	def __init__(self, datain, parent=None, *args):
		QAbstractTableModel.__init__(self, parent, *args)
		self.arraydata=datain

	def headerData(self,section,orientation,role=Qt.DisplayRole):
#		print("headerData:",section,",",orientation,",",role)
		if role==Qt.DisplayRole and orientation==Qt.Horizontal:
			return self.header_labels[section]
		return QAbstractTableModel.headerData(self,section,orientation,role)

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
			rval=QVariant(self.arraydata[index.row()][index.column()])
		except:
			row=index.row()
			col=index.column()
			rprint("Row="+str(row)+" Col="+str(col))
			rprint("arraydata:")
			rprint(self.arraydata)
		else:
			return rval

	def dataChangedAll(self):
		self.dataChanged.emit(self.createIndex(0,0),self.createIndex(self.rowCount(self)-1,self.columnCount(self)-1))


class CustomSortFilterProxyModel(QSortFilterProxyModel):
	def __init__(self,parent=None):
		super(CustomSortFilterProxyModel,self).__init__(parent)

	# filterAcceptsRow - return True if row should be included in the model, False otherwise
	#
	# the value to test is the callsign (row[2])
	# the value to test against is the filterRegExp
	# for simple cases, this must be an exact match; but, we also want to accept
	# the row for 'all teams' or 'all'.  Future development: accept a list of teams
	def filterAcceptsRow(self,row,parent):
		target=self.filterRegExp().pattern()
		teamNameText=self.sourceModel().index(row,2,parent).data()
		val=getExtTeamName(teamNameText)

		# for rows to all teams, only accept the row if the row's epoch time is earlier than the tab's creation time
		addAllFlag=False
		if teamNameText.lower()=="all" or teamNameText.lower().startswith("all "):
			if target in teamCreatedTimeDict:
				allEntryTime=self.sourceModel().index(row,6,parent).data()
				if teamCreatedTimeDict[target]<allEntryTime:
					addAllFlag=True
###		return(val==target or self.sourceModel().index(row,6,parent).data()==1e10)
##		return(val==target) # simple case: match the team name exactly
		return(val==target or addAllFlag)


class customEventFilter(QObject):
	def eventFilter(self,receiver,event):
		if(event.type()==QEvent.ShortcutOverride and
			event.modifiers()==Qt.ControlModifier and
			event.key()==Qt.Key_Z):
			return True # block the default processing of Ctrl+Z
		return super(customEventFilter,self).eventFilter(receiver,event)


def main():
	app = QApplication(sys.argv)
	eFilter=customEventFilter()
	app.installEventFilter(eFilter)
	w = MyWindow(app)
	w.show()
	sys.exit(app.exec_())

if __name__ == "__main__":
	main()
