﻿# #############################################################################
#
#  radiolog.py - SAR Radio Log program, based on PyQt 5.4, Python 3.4.2
#
#   developed for Nevada County Sheriff's Search and Rescue
#    Copyright (c) 2015-2018 Tom Grundy
#
#  http://github.com/ncssar/radiolog
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
#    4-7-17    TMG       stopgap for 310 - disable attached callsign handling for now
#   4-11-17    TMG       fix 322 (restore crashes - file not found) - give a message
#                         and return gracefully if the file specified in the rc file
#                         does not exist, and, take steps to make sure the correct
#                         filename is saved to the rc file at the correct times
#   4-15-17    TMG       fix 323 (load dialog should only show non-fleetsync and
#                         non-clueLog .csv files)
#   4-26-17    TMG       fix 326 (zero-left-padded tabs when callsigns are digits-only)
#   4-29-17    TMG       fix 34 (fleetsync mute)
#   5-2-17     TMG       fix 325 (cancel-confirm bypass if message is blank)
#   5-13-17    TMG       fix 338 (esc key in clue/subject dialogs closes w/out confirm):
#                          add keyPressEvents to ignore the esc key; note that the
#                          Qt docs say that .reject() is called by the esc key but
#                          that has other repercussions in this case; also serves
#                          as interim fix for #337 (crash due to the above) until
#                          a strong parent-child dialog relationship can be established
#                          (see http://stackoverflow.com/questions/43956587)
#   5-13-17    TMG       fix #333 (crash on throb after widget has been closed)
#   5-13-17    TMG       further fix on #333: don't try to stop the timer if it
#                          does not exist, i.e. if not currently mid-throb; caused
#                          similar crash to #333 during auto-cleanup of delayed stack
#   5-19-17    TMG       move loadFlag settings closer to core load functionality
#                          to at least partially address #340
#   5-21-17    TMG       fix #257, fix #260: 90+% lag reduction: do not do any sorting;
#                         instead, calculate the correct index to insert a new row
#                         during newEntry, and use beginInsertRows and endInsertRows
#                         instead of layoutChanged; see notes in newEntry function
#   6-15-17    TMG       fix #336 by simply ignoring keyPressEvents that happen
#                         before newEntryWidget is responsive, and get fielded by
#                         MyWindows instead; would be nice to find a better long-term
#                         solution; see https://stackoverflow.com/questions/44148992
#                         and see notes inline below
#   7-1-17     TMG       fix #342 (focus-follows-mouse freeze); 'fix' #332 (freeze
#                         due to modal dialogs displayed underneath other windows)
#                         by doing full audit and recode and test of all QMessageBox calls
#   7-1-17     TMG       fix #343 (crash on print clue log when there are no clues):
#                         show an error message when the print button is clicked if
#                         there are no operational periods that have clues, and only
#                         populate the print clue log operational period cyclic field
#                         with op periods that do have clues
#   7-3-17     TMG       fix #341 (add checkbox for fleetsync mute)
#   9-24-17    TMG       fix #346 (slash in incident name kills everything) using
#                         normName function; get rid of leading space in loaded
#                         incident name due to incorrect index (17 instead of 18);
#                         fix #349 (save filename not updated after load)
#   9-24-17    TMG       fix #350 (do not try to read fleetsync file on restore) by
#                         adding hideWarnings argument to fsLoadLookup
#   9-24-17    TMG       fix #345 (get rid of 'printing' message dialog) by commenting
#                         out all print dialog lines which also fixes # 33 and #263;
#                         time will tell if this is sufficient, or if we need to
#                         bring back some less-invasive and less-confusing notification,
#                         like a line in the main dialog or such
#   11-5-17    TMG       fix #32 (add fleetsync device filtering) - affects several
#                         parts of the code and several files
#   11-15-17   TMG       fix #354 (stolen focus / hold time failure); fix #355 (space bar error);
#                         add focus rules and timeline documentation; change hold time
#                         to 20 sec (based on observations during class); set focus
#                         to the active stack item's message field on changeCallsignDialog close
#   11-23-17   TMG       address #31 (css / font size issues) - not yet checked against
#                         dispatch computer - only tested on home computer
#   11-23-17   TMG       fix #356 (change callsign dialog should not pop up until
#                         its new entry widget is active (i.e. the active stack item)
#     5-1-18   TMG       fix #357 (freeze after print, introduced by fix # 345)
#    5-28-18   TMG       fix #360 (remove leading zeros from team tab names)
#     6-9-18   TMG		 allow configuration by different teams using optional local/radiolog.cfg
#                          (merged config branch to master)
#    7-22-18   TMG       add team hotkeys (fix #370); change return/enter/space to open
#                          a new entry dialog with blank callsign (i.e. LEO callsigns);
#                          toggle team hotkeys vs normal hotkeys using F12
#    7-22-18   TMG       fix #373 (esc closes NED in same manner as cancel button)
#    7-22-18   TMG       fix #360 again (leading zeros still showed up in tab
#                          context menus, therefore in callsign field of NED created
#                          from tab context menus)
#     8-2-18   TMG       space bar event does not reach the main window after the
#                          first team tab gets created, so disable it for now -
#                          must use enter or return to open a NED with no callsign (#370)
#     8-3-18   TMG       fix #372 (combobox / cyclic callsign selection)
#     8-5-18   TMG       fix #371 (amend callsign of existing message)
#    8-29-18   TMG       fix #375 (crash during new entry for new team)
#     9-9-18   TMG       fix #379 (subject located form - field type error; confirmed
#                           that all other calls to toPlainText are for valid fields)
#     9-9-18   TMG       add a very short timeout to the requests.get locator update call to 
#                           eliminate lag while completely ignoring the response
#                           ('fire-and-forget'); would have to use a thread-based module
#                           if the response were important; works well on home computer,
#                           hopefully this fixes #378
#    9-17-18   TMG       fix and improve team hotkey selection and recycling
#    9-17-18   TMG       change some dictionary lookups to use get() with a default,
#                           to avoid possible KeyErrors
#    9-17-18   TMG       catch any sync errors during deletion of proxyModelList entries
#                           (which happens during team tab deletion)
#    9-17-18   TMG       disallow blank callsign for new entry
#    9-23-18   TMG       cleanup config file defaults handling
#    10-3-18   TMG       fix #364: eliminate backup rotation lag by running it
#                          in the background (external powershell script on Windows
#                          systems; custom script can be specified in config file;
#                          currently there is no default backup rotation script for
#                          non-Windows systems)
#   10-26-18   TMG       fix #380 (fleetsync CID parsing issue); add more CID parsing
#                          and callsign-change messages
#   11-17-18   TMG       overhaul logging: use the logging module, making sure
#                          to show uncaught exceptions on the screen and in the
#                          log file
#   11-17-18   TMG       fix #382 (disable locator requests from GUI);
#                          fix #383 (disable second working dir from GUI)
#   11-17-18   TMG       fix #381 (auto-accept entry on clue report or subj located accept);
#                          fix #339 (don't increment clue# if clue form is canceled)
#   11-18-18   TMG       fix #358 and make FS location parsing more robust
#   11-18-18   TMG       fix #351 (don't show options at startup after restore)
#   12-12-18   TMG       fix #384 (bad data causes unpack error)
#   12-14-18   TMG       fix #385 (print team log from team tab context menu)
#   12-15-18   TMG       fix #387 (file browser sort by date)
#   12-15-18   TMG       simplify code for #387 fix above; also filter out _clueLog_bak
#                         and _fleetSync_bak files from file browser
#   12-16-18   TMG       fix #388 (team log print variant team names)
#    4-11-19   TMG       fix #392 (get rid of leading 'Team ' when appropriate);
#                         fix #393 (preserve case of new callsigns);
#                         fix #394 (show actual tie in log messages)
#     5-3-19   TMG       fix #329 (team tab bar grouping) - default groups are just
#                         numbered teams, vs everything else; can specify a more
#                         elaborate set of group names and regular expressions
#                         in the config file (tabGroups)
#     5-4-19   TMG       enhance #393: if typed callsign is a case-insensitive
#                         match with an existing callsign, use the existing callsign;
#                         fix #397 ('Available' status - also added 'Off Duty' status
#                         which does not time out and has no background and gray text;
#                         '10-8' changes to 'Available', '10-97' changes to 'Working',
#                         '10-10' changes to 'Off Duty')
#     2-8-20   TMG       re-fix #41: repair hot-unplug handling for current pyserial
#    2-10-20   TMG       fix #396: create default local dir and config file if needed
#    5-28-20   TMG       fix #412: relayed message features
#    6-15-20   TMG       fix #415: restore timeout on auto-recover (in rc file);
#                          fix #404: show http request response in log;
#                          address #413: multiple crashes - add more logging; 
#                          improve relay features to be more intuitive
#
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

import functools
import sys
import logging
import time
import re
import serial
import serial.tools.list_ports
import csv
import os.path
import os
import glob
import requests
import subprocess
import win32api
import win32gui
import win32print
import win32con
import shutil
import math
import textwrap
from reportlab.lib import colors,utils
from reportlab.lib.pagesizes import letter,landscape,portrait
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.units import inch
from PyPDF2 import PdfFileReader,PdfFileWriter
from FingerTabs import *
from pygeodesy import Datums,ellipsoidalBase,dms

__version__ = "3.0.1"

# process command-line arguments
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

from ui.radiolog_ui import Ui_Dialog # normal version, for higher resolution

statusStyleDict={}
# even though tab labels are created with font-size:20px and the tab sizes and margins are created accordingly,
#  something after creation time is changing font-sizes to a smaller size.  So, just
#  hardcode them all here to force 20px always.
tabFontSize="20px"
statusStyleDict["At IC"]="font-size:"+tabFontSize+";background:#00ff00;border:1px outset black;padding-left:0px;padding-right:0px"
statusStyleDict["In Transit"]="font-size:"+tabFontSize+";background:blue;color:white;border:1px outset black;padding-left:0px;padding-right:0px"
statusStyleDict["Working"]="font-size:"+tabFontSize+";background:none;border:1px outset black;padding-left:0px;padding-right:0px"
statusStyleDict["Off Duty"]="font-size:"+tabFontSize+";color:#aaaaaa;background:none;border:none;padding-left:0px;padding-right:0px"
# Waiting for Transport and Available should still flash even if not timed out, but they don't
#  prevent a timeout.  So, for this code, and alternating timer cycles (seconds):
# cycle 1: style as in the line specified for that status name
# cycle 2: if not timed out, style as "" (blank); if timed out, style as timeout as expected
statusStyleDict["Available"]="font-size:"+tabFontSize+";background:#00ffff;border:1px outset black;padding-left:0px;padding-right:0px;padding-top:-1px;padding-bottom:-1px"
statusStyleDict["Waiting for Transport"]="font-size:"+tabFontSize+";background:blue;color:white;border:1px outset black;padding-left:0px;padding-right:0px;padding-top:-1px;padding-bottom:-1px"
statusStyleDict["STANDBY"]="font-size:"+tabFontSize+";background:black;color:white;border:1px outset black;padding-left:0px;padding-right:0px;padding-top:-1px;padding-bottom:-1px"
statusStyleDict[""]="font-size:"+tabFontSize+";background:none;padding-left:1px;padding-right:1px"
statusStyleDict["TIMED_OUT_ORANGE"]="font-size:"+tabFontSize+";background:orange;border:1px outset black;padding-left:0px;padding-right:0px;padding-top:-1px;padding-bottom:-1px"
statusStyleDict["TIMED_OUT_RED"]="font-size:"+tabFontSize+";background:red;border:1px outset black;padding-left:0px;padding-right:0px;padding-top:-1px;padding-bottom:-1px"

timeoutDisplayList=[["10 sec",10]]
for n in range (1,13):
	timeoutDisplayList.append([str(n*10)+" min",n*600])

teamStatusDict={}
teamFSFilterDict={}
teamTimersDict={}
teamCreatedTimeDict={}

versionDepth=5 # how many backup versions to keep; see rotateBackups

continueSec=20
holdSec=20

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
	# fix #459 (and other places in the code): remove all leading and trailing spaces, and change all chains of spaces to one space
	name=re.sub(r' +',r' ',teamName).strip()
	name=name.replace(' ','') # remove spaces to shorten the name
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
	if prefix.lower()=='t':
		prefix='team'
	# now force everything other than 'team' to be added alphabetically at the end,
	# by prefixing the prefix with 'z_' (the underscore makes it unique for easy pruning later)
	# if prefix!='team':
	# 	prefix="z_"+prefix

	# #503 - extTeamName should always start with 'z_' then a capital letter
	prefix='z_'+prefix.capitalize()

	if firstNum!=None:
		rest=name[firstNumIndex:].zfill(5)
	else:
		rest=teamName # preserve case if there are no numbers
##	rprint("prefix="+prefix+" rest="+rest+" name="+name)
	extTeamName=prefix+rest
# 	rprint("Team Name:"+teamName+": extended team name:"+extTeamName)
	return extTeamName

def getNiceTeamName(extTeamName):
	# prune any leading 'z_' that may have been added for sorting purposes
	extTeamName=extTeamName.replace('z_','')
	# find index of first number in the name; everything left of that is the 'prefix';
	# assume that everything after the prefix is a number
	#  (left-zero-padded to 5 digits)
	firstNum=re.search("\d",extTeamName)
	firstNumIndex=-1 # assume there is no number at all
	prefix=""
	if firstNum:
		firstNumIndex=firstNum.start()
	if firstNumIndex>0:
		prefix=extTeamName[:firstNumIndex]
#		name=prefix.capitalize()+" "+str(int(str(extTeamName[firstNumIndex:])))
		name=prefix.capitalize()+" "+str(extTeamName[firstNumIndex:]).lstrip('0')
	else:
		name=extTeamName
	# finally, remove any leading zeros (necessary for non-'Team' callsigns)
	name=name.lstrip('0')
# 	rprint("getNiceTeamName("+extTeamName+")")
# 	rprint("FirstNumIndex:"+str(firstNumIndex)+" Prefix:'"+prefix+"'")
# 	rprint("Human Readable Name:'"+name+"'")
	return name

def getShortNiceTeamName(niceTeamName):
	# 1. remove spaces, then prune leading 'Team'
	shortNiceTeamName=niceTeamName.replace(' ','')
	shortNiceTeamName=shortNiceTeamName.replace('Team','')
	# 2. remove any leading zeros since this is only used for the tab label
	shortNiceTeamName=shortNiceTeamName.lstrip('0')
	return shortNiceTeamName

def getFileNameBase(root):
	return root+"_"+time.strftime("%Y_%m_%d_%H%M%S")

###### LOGGING CODE BEGIN ######

# do not pass ERRORs to stdout - they already show up on the screen from stderr
class LoggingFilter(logging.Filter):
	def filter(self,record):
		return record.levelno < logging.ERROR

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logFileLeafName=getFileNameBase('radiolog_log')+'.txt'

def setLogHandlers(dir=None):
	# remove all existing handlers before adding the new ones
	for h in logger.handlers[:]:
		logger.removeHandler(h)
	# add a filehandler if dir is specified
	if dir:
		# logFileName=os.path.join(dir,getFileNameBase("radiolog_log")+".txt")
		logFileName=os.path.join(dir,logFileLeafName)
		fh=logging.FileHandler(logFileName)
		fh.setLevel(logging.INFO)
		logger.addHandler(fh)
	ch=logging.StreamHandler(stream=sys.stdout)
	ch.setLevel(logging.INFO)
	ch.addFilter(LoggingFilter())
	logger.addHandler(ch)

setLogHandlers()

# redirect stderr to stdout here by overriding excepthook
# from https://stackoverflow.com/a/16993115/3577105
# and https://www.programcreek.com/python/example/1013/sys.excepthook
def handle_exception(exc_type, exc_value, exc_traceback):
	if not issubclass(exc_type, KeyboardInterrupt):
		logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
	sys.__excepthook__(exc_type, exc_value, exc_traceback)
	# interesting that the program no longer exits after uncaught exceptions
	#  if this function replaces __excepthook__.  Probably a good thing but
	#  it would be nice to undertstand why.
	return
# note: 'sys.excepthook = handle_exception' must be done inside main()

def rprint(text):
	logText=time.strftime("%H%M%S")+":"+str(text)
	logger.info(logText)

###### LOGGING CODE END ######

# #471: rebuild any modified Qt .ui and .qrc files at runtime
#   (copied from plans_console repo - could be made into a shared module at some point)

qtDesignerSubDir='designer' # subdir containing Qt Designer source files (*.ui)
qtUiPySubDir='ui' # target subdir for compiled ui files (*_ui.py)
qtQrcSubDir='.' # subdir containing Qt qrc resource files (*.qrc)
qtRcPySubDir='.' # target subdir for compiled resource files

installDir=os.path.dirname(os.path.realpath(__file__))
qtDesignerDir=os.path.join(installDir,qtDesignerSubDir)
qtUiPyDir=os.path.join(installDir,qtUiPySubDir)
qtQrcDir=os.path.join(installDir,qtQrcSubDir)
qtRcPyDir=os.path.join(installDir,qtRcPySubDir)

# rebuild all _ui.py files from .ui files in the same directory as this script as needed
#   NOTE - this will overwrite any edits in _ui.py files
for ui in glob.glob(os.path.join(qtDesignerDir,'*.ui')):
	uipy=os.path.join(qtUiPyDir,os.path.basename(ui).replace('.ui','_ui.py'))
	if not (os.path.isfile(uipy) and os.path.getmtime(uipy) > os.path.getmtime(ui)):
		cmd='pyuic5 -o '+uipy+' '+ui
		rprint('Building GUI file from '+os.path.basename(ui)+':')
		rprint('  '+cmd)
		os.system(cmd)

# rebuild all _rc.py files from .qrc files in the same directory as this script as needed
#   NOTE - this will overwrite any edits in _rc.py files
for qrc in glob.glob(os.path.join(qtQrcDir,'*.qrc')):
	rcpy=os.path.join(qtRcPyDir,os.path.basename(qrc).replace('.qrc','_rc.py'))
	if not (os.path.isfile(rcpy) and os.path.getmtime(rcpy) > os.path.getmtime(qrc)):
		cmd='pyrcc5 -o '+rcpy+' '+qrc
		rprint('Building Qt Resource file from '+os.path.basename(qrc)+':')
		rprint('  '+cmd)
		os.system(cmd)

from ui.help_ui import Ui_Help
from ui.options_ui import Ui_optionsDialog
from ui.fsSendDialog_ui import Ui_fsSendDialog
from ui.fsSendMessageDialog_ui import Ui_fsSendMessageDialog
from ui.newEntryWindow_ui import Ui_newEntryWindow
from ui.newEntryWidget_ui import Ui_newEntryWidget
from ui.clueDialog_ui import Ui_clueDialog
from ui.clueLogDialog_ui import Ui_clueLogDialog
from ui.printDialog_ui import Ui_printDialog
from ui.changeCallsignDialog_ui import Ui_changeCallsignDialog
from ui.fsFilterDialog_ui import Ui_fsFilterDialog
from ui.opPeriodDialog_ui import Ui_opPeriodDialog
from ui.printClueLogDialog_ui import Ui_printClueLogDialog
from ui.nonRadioClueDialog_ui import Ui_nonRadioClueDialog
from ui.subjectLocatedDialog_ui import Ui_subjectLocatedDialog
from ui.continuedIncidentDialog_ui import Ui_continuedIncidentDialog
from ui.loadDialog_ui import Ui_loadDialog

# function to replace only the rightmost <occurrence> occurrences of <old> in <s> with <new>
# used by the undo function when adding new entry text
# credit to 'mg.' at http://stackoverflow.com/questions/2556108
def rreplace(s,old,new,occurrence):
	li=s.rsplit(old,occurrence)
	return new.join(li)
	
def normName(name):
	return re.sub("[^A-Za-z0-9_]+","_",name)
  
class MyWindow(QDialog,Ui_Dialog):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.newWorkingDir=False # is this the first time using a newly created working dir?  (if so, suppress some warnings)
		msg='RadioLog '+str(__version__)
		self.firstWorkingDir=os.path.join(os.getenv('HOMEPATH','C:\\Users\\Default'),'RadioLog')
		if self.firstWorkingDir[1]!=':':
			self.firstWorkingDir=os.path.join(os.getenv('HOMEDRIVE','C:'),self.firstWorkingDir)
		if not os.path.isdir(self.firstWorkingDir):
			try:
				os.makedirs(self.firstWorkingDir)
				msg+='\nWorking directory "'+self.firstWorkingDir+'" was not found; creating it now.'
				self.newWorkingDir=True
			except:
				err='FATAL ERROR: working directory "'+self.firstWorkingDir+'" was not found and could not be created.  ABORTING.'
				msg+=err
				self.configErrMsgBox=QMessageBox(QMessageBox.Critical,"Fatal Configuration Error",err,
								QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
				self.configErrMsgBox.exec_()
				print(msg)
				sys.exit(-1)
		else:
			msg+='\nWorking directory found at "'+self.firstWorkingDir+'".'

		# create sessionDir immediately, since this is where logging output will be saved
		self.sessionDir=os.path.join(self.firstWorkingDir,'NewSession_'+time.strftime('%Y_%m_%d_%H%M%S'))
		try:
			os.mkdir(self.sessionDir)
			msg+='\nInitial session directory created at "'+self.sessionDir+'".'
		except:
			err='FATAL ERROR: initial session directory "'+self.sessionDir+'" could not be created.  ABORTING.'
			msg+=err
			self.configErrMsgBox=QMessageBox(QMessageBox.Critical,"Fatal Configuration Error",err,
							QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			self.configErrMsgBox.exec_()
			print(msg)
			sys.exit(-1)
		
		# if everything was created successfully, set the log file location and start logging
		if os.path.isdir(self.sessionDir):
			setLogHandlers(self.sessionDir)
			rprint(msg)
		else:
			err='FATAL ERROR: initial session directory "'+self.sessionDir+'" was not created.  ABORTING.'
			msg+=err
			self.configErrMsgBox=QMessageBox(QMessageBox.Critical,"Fatal Configuration Error",err,
							QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			self.configErrMsgBox.exec_()
			print(msg)
			sys.exit(-1)

		self.configDir=os.path.join(self.firstWorkingDir,'config')
		self.configDefaultDir=os.path.join(installDir,'config_default')

#####  BEGIN config dir migration code #522

		# create the config dir if it doesn't already exist, and populate it
		#  with files from config_default
		if not os.path.isdir(self.configDir):
			msg='Local configuration directory was not found.  It looks like this is the first time running RadioLog '+str(__version__)+' on this computer.\n\n'
			msg+='You can import the local configuration files from a previous version.\n\nIf you skip this step, RadioLog will use the defaults, '
			msg+='but any important local settings will be lost, including:\n\n  - local server IP address (for GPS locators)\n  - second working directory (for other tools like Plans Console)\n  - agency name and logo (for generated PDFs)\n\n'
			msg+='This is a one-time offer.  This question will not show up again when you install newer versions.  Importing now will apply the imported settings immediately.  If you choose to use the defaults for now, you can always copy the configuration files into place by hand later.'
			box=QMessageBox(QMessageBox.Question,'Import configuration files',msg,
					QMessageBox.Yes|QMessageBox.No,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			box.button(QMessageBox.Yes).setText('Yes - Browse for directory')
			box.button(QMessageBox.No).setText('No - use defaults')
			srcDir=None
			if box.exec_()==QMessageBox.Yes:
				ok=False
				notValidSrcDir=False
				while not ok:
					msg=''
					if notValidSrcDir:
						msg='The specified directory '+notValidSrcDir+' does not contain radiolog.cfg.  Try again, or click Cancel to stop trying to find a previous configuration directory and use the defaults instead.\n\n'
					msg+='The file browser will be shown next.  Select a directory that contains one or more of these files:\n\n'
					msg+='  - radiolog.cfg [required]\n  - radiolog_logo.jpg\n  - radiolog_fleetsync.csv'
					msg+='\n\nIn previous versions, the configuration directory name was "local".'
					box=QMessageBox(QMessageBox.Information,'Import configuration files',msg,
							QMessageBox.Ok|QMessageBox.Cancel,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
					if box.exec_()==QMessageBox.Ok:
						# srcDir=QFileDialog.getExistingDirectory(box,'Choose previous configuration directory','C:\\')
						fd=QFileDialog(self,'Choose previous configuration directory','C:\\')
						fd.setFileMode(QFileDialog.Directory)
						if fd.exec_():
							srcDir=fd.selectedFiles()[0]
							contents=os.listdir(srcDir)
							if 'radiolog.cfg' in contents:
								ok=True
							else:
								notValidSrcDir=srcDir
								srcDir=None
					else:
						break
			if not srcDir:
				srcDir=self.configDefaultDir
			msg='About to copy configuration directory from\n\n"'+srcDir+'"\n\nto\n\n"'+self.configDir+'"\n\nAfter the copy operation, you may want to edit the copied files in that directory to suit your needs.'
			rprint(msg)
			box=QMessageBox(QMessageBox.Information,'Copying configuration directory',msg,
					QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			box.exec_()
			shutil.copytree(srcDir,self.configDir)
		self.configFileName=os.path.join(self.configDir,'radiolog.cfg')
		self.configFileDefaultName=os.path.join(self.configDefaultDir,'radiolog.cfg')
		if not os.path.isfile(self.configFileName):
			msg='config directory was found but did not contain radiolog.cfg; about to copy from default config directory '+self.configDefaultDir+'; this could disable important features like GPS locators, the second working directory, and more.'
			rprint(msg)
			box=QMessageBox(QMessageBox.Information,'Copying radiolog.cfg',msg,
					QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			box.exec_()
			shutil.copyfile(self.configFileDefaultName,self.configFileName)

#####  END config dir migration code #522

		self.setWindowFlags(self.windowFlags()|Qt.WindowMinMaxButtonsHint)
		self.parent=parent
		self.ui=Ui_Dialog()
		self.ui.setupUi(self)
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.loadFlag=False # set this to true during load, to prevent save on each newEntry
		self.totalEntryCount=0 # rotate backups after every 5 entries; see newEntryWidget.accept
		
		self.ui.teamHotkeysWidget.setVisible(False) # disabled by default		
		self.hotkeyDict={}
		self.nextAvailHotkeyIndex=0
		self.hotkeyPool=["1","2","3","4","5","6","7","8","9","0","q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m"]
		self.homeDir=os.path.expanduser("~")
		
		# coordinate system name translation dictionary:
		#  key = ASCII name in the config file
		#  value = utf-8 name used in the rest of this code
		self.csDisplayDict={}
		self.csDisplayDict["UTM 5x5"]="UTM 5x5"
		self.csDisplayDict["UTM 7x7"]="UTM 7x7"
		self.csDisplayDict["D.d"]="D.d°"
		self.csDisplayDict["DM.m"]="D° M.m'"
		self.csDisplayDict["DMS.s"]="D° M' S.s\""

		self.validDatumList=["WGS84","NAD27","NAD27 CONUS"]

		self.timeoutDisplaySecList=[i[1] for i in timeoutDisplayList]
		self.timeoutDisplayMinList=[int(i/60) for i in self.timeoutDisplaySecList if i>=60]
		
		# fix #342 (focus-follows-mouse causes freezes) - disable FFM here;
		#  restore to initial setting on shutdown (note this would leave it
		#  disabled after unclean shutdown)
		self.initialWindowTracking=False
		try:
			self.initialWindowTracking=win32gui.SystemParametersInfo(win32con.SPI_GETACTIVEWINDOWTRACKING)
		except:
			pass
		if self.initialWindowTracking:
			rprint("Window Tracking was initially enabled.  Disabling it for radiolog; will re-enable on exit.")
			win32gui.SystemParametersInfo(win32con.SPI_SETACTIVEWINDOWTRACKING,False)

# 		self.secondWorkingDir=os.getenv('HOMEPATH','C:\\Users\\Default')+"\\Documents\\sar"

		self.incidentName="New Incident"
		self.incidentNameNormalized=normName(self.incidentName)
		self.opPeriod=1
		self.incidentStartDate=time.strftime("%a %b %d, %Y")
		self.isContinuedIncident=False

		self.optionsDialog=optionsDialog(self)
		self.optionsDialog.accepted.connect(self.optionsAccepted)
		
		# config file (e.g. <firstWorkingDir>/config/radiolog.cfg) stores the team standards;
		#  it should be created/modified by hand, and is read at radiolog startup,
		#  and is not modified by radiolog at any point
		# resource file / 'rc file' (e.g. <firstWorkingDir>/radiolog_rc.txt) stores the search-specific
		#  options settings; it is read at radiolog startup, and is written
		#  whenever the options dialog is accepted
		self.readConfigFile() # defaults are set inside readConfigFile

		self.printDialog=printDialog(self)
		self.printClueLogDialog=printClueLogDialog(self)

		# #483: Check for recent radiolog sessions on this computer.  If any sessions are found from the previous 4 days,
		#  ask the operator if this new session is intended to be a continuation of one of those previous incidents.
		#  If so:
		#    - set the incident name to the same as that in the selected previous radiolog csv file;
		#    - set the OP number to one more than the latest OP# in the previous csv
		#       (with a reminder that OP# can be changed by hand by clicking the OP button);
		#    - set the next clue number to one more than the latest clue number in the previous CSV
		#       (with a reminder that clue# can be changed in the clue dialog the next time it is raised)

		self.checkForContinuedIncident()

		if self.isContinuedIncident:
			rlInitText='Radio Log Begins - Continued incident "'+self.incidentName+'": Operational Period '+str(self.opPeriod)+' Begins: '
		else:
			rlInitText='Radio Log Begins: '
		rlInitText+=self.incidentStartDate
		if lastClueNumber>0:
			rlInitText+=' (Last clue number: '+str(lastClueNumber)+')'
		self.radioLog=[[time.strftime("%H%M"),'','',rlInitText,'','',time.time(),'','',''],
			['','','','','','',1e10,'','','']] # 1e10 epoch seconds will keep the blank row at the bottom when sorted
		rprint('Initial entry: '+rlInitText)

		self.clueLog=[]
		self.clueLog.append(['',self.radioLog[0][3],'',time.strftime("%H%M"),'','','','',''])

		self.lastFileName="" # to force error in restore, in the event the resource file doesn't specify the lastFileName
# 		self.csvFileName=getFileNameBase(self.incidentNameNormalized)+".csv"
# 		self.pdfFileName=getFileNameBase(self.incidentNameNormalized)+".pdf"
		self.updateFileNames()
		self.lastSavedFileName="NONE"
##		self.fsFileName=self.getFileNameBase(self.incidentNameNormalized)+"_fleetsync.csv"

		# disable fsValidFleetList checking to allow arbitrary fleets; this
		#  idea is probably obsolete
# 		self.fsValidFleetList=[100]
		self.fsLog=[]
# 		self.fsLog.append(['','','','',''])
		self.fsMuted=False
		self.noSend=noSend
		self.fsMutedBlink=False
		self.fsFilterBlinkState=False
		self.enableSendText=True
		self.enablePollGPS=True
		self.getString=""

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
		
		self.fsSendDialog=fsSendDialog(self)
		self.fsSendList=[[]]
		self.fsResponseMessage=''

		self.sourceCRS=0
		self.targetCRS=0
		
		# set the default lookup name - this must be after readConfigFile
		#  since that function accepts the options form which updates the
		#  lookup filename based on the current incedent name and time
		# self.fsFileName=os.path.join(self.firstWorkingDir,'config','radiolog_fleetsync.csv')
		self.fsFileName='radiolog_fleetsync.csv'
		
		self.helpFont1=QFont()
		self.helpFont1.setFamily("Segoe UI")
		self.helpFont1.setPointSize(9)
		self.helpFont1.setStrikeOut(False)

		self.helpFont2=QFont()
		self.helpFont2.setFamily("Segoe UI")
		self.helpFont2.setPointSize(9)
		self.helpFont2.setStrikeOut(True)

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

		self.helpWindow.ui.fsSomeFilteredLabel.setFont(self.helpFont1)
		self.helpWindow.ui.fsAllFilteredLabel.setFont(self.helpFont2)		
		self.helpWindow.ui.fsSomeFilteredLabel.setStyleSheet(statusStyleDict["Working"])
		self.helpWindow.ui.fsAllFilteredLabel.setStyleSheet(statusStyleDict["Working"])

		self.radioLogNeedsPrint=False # set to True with each new log entry; set to False when printed
		self.clueLogNeedsPrint=False

		self.fsFilterDialog=fsFilterDialog(self)
		self.fsFilterDialog.ui.tableView.setColumnWidth(0,50)
		self.fsFilterDialog.ui.tableView.setColumnWidth(1,75)
		self.fsBuildTooltip()
		self.fsLatestComPort=None
		self.fsShowChannelWarning=True
		
		self.ui.addNonRadioClueButton.clicked.connect(self.addNonRadioClue)

		self.ui.helpButton.clicked.connect(self.helpWindow.show)
		self.ui.optionsButton.clicked.connect(self.optionsDialog.show)
		self.ui.fsFilterButton.clicked.connect(self.fsFilterDialog.show)
		self.ui.printButton.clicked.connect(self.printDialog.show)
##		self.ui.printButton.clicked.connect(self.testConvertCoords)

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
		# font size is constrained to min and max for several items
		self.minLimitedFontSize=8
		self.maxLimitedFontSize=20
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
		self.firstComPort=None
		self.secondComPort=None
		self.comPortScanInProgress=False
		self.comPortTryList=[]
##		if develMode:
##			self.comPortTryList=[serial.Serial("\\\\.\\CNCB0")] # DEVEL
		self.fsBuffer=""
		self.entryHold=False
		self.currentEntryLastModAge=0
		self.fsAwaitingResponse=None # used as a flag: [fleet,device,text,elapsed]
		self.fsAwaitingResponseTimeout=8 # give up after this many seconds

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
				width:20px;
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

# 		self.ui.tabWidget.insertTab(0,QWidget(),'TEAMS:')
# ##		self.ui.tabWidget.setStyleSheet("font-size:12px")
# 		self.ui.tabWidget.setTabEnabled(0,False)
		
# 		self.ui.teamHotkeysHLayout.insertWidget(0,QLabel("HOTKEYS:"))

		self.ui.tabWidget.setContextMenuPolicy(Qt.CustomContextMenu)
		self.ui.tabWidget.customContextMenuRequested.connect(self.tabContextMenu)

		self.newEntryWindow=newEntryWindow(self) # create the window but don't show it until needed

		# load resource file; process default values and resource file values
		self.rcFileName=os.path.join(self.firstWorkingDir,'radiolog_rc.txt')
		self.previousCleanShutdown=self.loadRcFile()
		showStartupOptions=True
		if self.isContinuedIncident:
			showStartupOptions=False
		if not self.previousCleanShutdown and not self.newWorkingDir:
			self.reallyRestore=QMessageBox(QMessageBox.Critical,"Restore last saved files?","The previous Radio Log session may have shut down incorrectly.  Do you want to restore the last saved files (Radio Log, Clue Log, and FleetSync table)?",
										QMessageBox.Yes|QMessageBox.No,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			self.reallyRestore.show()
			self.reallyRestore.raise_()
			if self.reallyRestore.exec_()==QMessageBox.Yes:
				self.restore()
				showStartupOptions=False
			
		# make sure x/y/w/h from resource file will fit on the available display
		d=QApplication.desktop()
		if (self.x+self.w > d.width()) or (self.y+self.h > d.height()):
			rprint("The resource file specifies a main window geometry that is bigger than (or not on) the available desktop.  Using default sizes for this session.")
			self.x=50
			self.y=50
			self.w=d.availableGeometry(self).width()-100
			self.h=d.availableGeometry(self).height()-100
		if (self.clueLog_x+self.clueLog_w > d.width()) or (self.clueLog_y+self.clueLog_h > d.height()):
			rprint("The resource file specifies a clue log window geometry that is bigger than (or not on) the available desktop.  Using default sizes for this session.")
			self.clueLog_x=75
			self.clueLog_y=75
			self.clueLog_w=d.availableGeometry(self).width()-100
			self.clueLog_h=d.availableGeometry(self).height()-100
		self.setGeometry(int(self.x),int(self.y),int(self.w),int(self.h))
		self.clueLogDialog.setGeometry(int(self.clueLog_x),int(self.clueLog_y),int(self.clueLog_w),int(self.clueLog_h))
		self.fontsChanged()

		self.ui.timeoutLabel.setText("TIMEOUT:\n"+timeoutDisplayList[self.optionsDialog.ui.timeoutField.value()][0])
		# pop up the options dialog to enter the incident name right away
		if showStartupOptions:
			QTimer.singleShot(1000,self.startupOptions)
		# save current resource file, to capture lastFileName without a clean shutdown
		self.saveRcFile()

	def getSessions(self,sort='chronological',reverse=False):
		csvFiles=glob.glob(self.firstWorkingDir+'/*/*.csv') # files nested in session dirs
		# backwards compatibility: also list csv files saved flat in the working dir
		csvFiles+=glob.glob(self.firstWorkingDir+'/*.csv')

		# backwards compatibility: look in the old working directory too
		#  copied code from radiolog.py before #522 dir structure overhaul;
		#  could consider removing this in the future, since it grabs all .csv
		#  files from ~\Documents
		oldWD=os.getenv('HOMEPATH','C:\\Users\\Default')+"\\Documents"
		if oldWD[1]!=":":
			oldWD=os.getenv('HOMEDRIVE','C:')+oldWD

		csvFiles+=glob.glob(oldWD+'/*.csv')

		# remove _fleetsync and _clueLog files
		csvFiles=[f for f in csvFiles if '_clueLog' not in f and '_fleetsync' not in f and self.isRadioLogDataFile(f)]
		rprint('Found '+str(len(csvFiles))+' .csv files (excluding _clueLog.csv and _fleetsync.csv files)')
		if sort=='chronological':
			sortedCsvFiles=sorted(csvFiles,key=os.path.getmtime,reverse=reverse)
		elif sort=='alphabetical':
			sortedCsvFiles=sorted(csvFiles,reverse=reverse)
		else:
			soretdCsvFiles=csvFiles
		rval=[]
		now=time.time()
		for f in sortedCsvFiles:
			mtime=os.path.getmtime(f)
			age=now-mtime
			ageStr=''
			if age<3600:
				ageStr='< 1 hour'
			elif age<86400:
				ageStr='< 1 day'
			else:
				ageDays=int(age/86400)
				ageStr=str(ageDays)+' day'
				if ageDays>1:
					ageStr+='s'
			if ageStr:
				ageStr+=' ago'
			filenameBase=f[:-4] # do this rather than splitext, to preserve entire path name
			incidentName=None
			lastOP='1' # if no entries indicate change in OP#, then initial OP is 1 by default
			lastClue='--'
			with open(f,'r') as radioLog:
				lines=radioLog.readlines()
				# don't show files that have less than two entries
				if len(lines)<7:
					rprint('  not listing empty csv '+f)
					continue
				for line in lines:
					if not incidentName and '## Incident Name:' in line:
						incidentName=': '.join(line.split(': ')[1:]).rstrip() # provide for spaces and ': ' in incident name
					# last clue# could be determined by an actual clue in the previous OP, but
					#  should carry forward the last clue number from an earlier OP if no clues
					#  were found in the most recent OP
					if 'Radio Log Begins - Continued incident' in line and '(Last clue number:' in line:
						lastClue=re.findall('(Last clue number: [0-9]+)',line)[-1].split()[3]
					if 'CLUE#' in line and 'LOCATION:' in line and 'INSTRUCTIONS:' in line:
						lastClue=re.findall('CLUE#[0-9]+:',line)[-1].split('#')[1][:-1]
					if 'Operational Period ' in line:
						lastOP=re.findall('Operational Period [0-9]+ Begins:',line)[-1].split()[2]
			rval.append([incidentName,lastOP or 1,lastClue or 0,ageStr,filenameBase,mtime])
		return rval

	# Build a nested list of radiolog session data from any sessions in the last n days;
	#  each list element is [incident_name,last_op#,last_clue#,filename_base]
	#  then let the user choose from these, or choose to start a new incident
	# - only show the most recent OP of each incident, i.e. don't show both OP2 and OP1
	# - add a note that the user can change OP and next clue# afterwards from the GUI
	def checkForContinuedIncident(self):
		continuedIncidentWindowDays=self.continuedIncidentWindowDays
		continuedIncidentWindowSec=continuedIncidentWindowDays*24*60*60
		now=time.time()
		opd={} # dictionary of most recent OP#'s per incident name
		choices=[]
		for session in self.getSessions(reverse=True):
			[incidentName,lastOP,lastClue,ageStr,filenameBase,mtime]=session
			rprint('session:'+str(session))
			if now-mtime<continuedIncidentWindowSec:
				if type(lastOP)==str and lastOP.isdigit() and int(lastOP)>int(opd.get(incidentName,0)):
					choices.append(session)
					opd[incidentName]=lastOP
				else:
					rprint('  not listing '+incidentName+' OP '+lastOP+' ('+filenameBase+') since OP '+str(opd.get(incidentName,0))+' is already listed')
			else:
				break
		if choices:
			rprint('radiolog sessions from the last '+str(continuedIncidentWindowDays)+' days:')
			rprint(' (hiding empty sessions; only showing the most recent session of continued incidents)')
			for choice in choices:
				rprint(choice[4])
			cd=continuedIncidentDialog(self)
			cd.ui.theTable.setRowCount(len(choices))
			row=0
			for choice in choices:
				q0=QTableWidgetItem(choice[0])
				q1=QTableWidgetItem(choice[1])
				q2=QTableWidgetItem(choice[2])
				q3=QTableWidgetItem(choice[3])
				# q0.setToolTip(choice[4])
				# q1.setToolTip(choice[4])
				# q2.setToolTip(choice[4])
				q3.setToolTip(choice[4])
				cd.ui.theTable.setItem(row,0,q0)
				cd.ui.theTable.setItem(row,1,q1)
				cd.ui.theTable.setItem(row,2,q2)
				cd.ui.theTable.setItem(row,3,q3)
				row+=1
			cd.show()
			cd.raise_()
			cd.exec_()
		else:
			rprint('no csv files from the last '+str(continuedIncidentWindowDays)+' days.')
	
	def isRadioLogDataFile(self,filename):
		# rprint('checking '+filename)
		if filename.endswith('.csv') and os.path.isfile(filename):
			with open(filename,'r') as f:
				if '## Radio Log data file' in f.readline():
					return True
		return False

	def readConfigFile(self):
		# specify defaults here
		self.clueReportPdfFileName='clueReport.pdf'
		self.agencyName="Search and Rescue"
		self.datum="WGS84"
		self.coordFormatAscii="UTM 5x5"
		self.coordFormat=self.csDisplayDict[self.coordFormatAscii]
		self.timeoutMinutes="30"
		self.printLogoFileName="radiolog_logo.jpg" # relative to config dir
		# self.firstWorkingDir=self.homeDir+"\\Documents"
		self.secondWorkingDir=None
		self.sarsoftServerName="localhost"
		self.rotateScript=None
		self.rotateDelimiter=None
		# 		self.tabGroups=[["NCSO","^1[tpsdel][0-9]+"],["CHP","^22s[0-9]+"],["Numbers","^Team [0-9]+"]]
		# the only default tab group should be number-only callsigns; everything
		#  else goes in a separate catch-all group; override this in radiolog.cfg
		defaultTabGroups=[["Numbers","^Team [0-9]+"]]
		self.tabGroups=defaultTabGroups
		self.continuedIncidentWindowDays="4"
		
		if os.name=="nt":
			rprint("Operating system is Windows.")
			if shutil.which("powershell.exe"):
				rprint("PowerShell.exe is in the path.")
				self.rotateScript="powershell.exe -ExecutionPolicy Bypass .\\rotateCsvBackups.ps1 -filenames "
				self.rotateDelimiter=","
			else:
				rprint("PowerShell.exe is not in the path; poweshell-based backup rotation script cannot be used.")
		else:
			rprint("Operating system is not Windows.  Powershell-based backup rotation script cannot be used.")

		configFile=QFile(self.configFileName)
		if not configFile.open(QFile.ReadOnly|QFile.Text):
			warn=QMessageBox(QMessageBox.Warning,"Error","Cannot read configuration file " + self.configFileName + "; using default settings. "+configFile.errorString(),
							QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			warn.show()
			warn.raise_()
			warn.exec_()
			self.timeoutRedSec=int(self.timeoutMinutes)*60
			self.updateOptionsDialog()
			return
		inStr=QTextStream(configFile)
		line=inStr.readLine()
		if line!="[RadioLog]":
			warn=QMessageBox(QMessageBox.Warning,"Error","Specified configuration file " + self.configFileName + " is not a valid configuration file; using default settings.",
							QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			warn.show()
			warn.raise_()
			warn.exec_()
			configFile.close()
			self.timeoutRedSec=int(self.timeoutMinutes)*60
			self.updateOptionsDialog()
			return
		
		while not inStr.atEnd():
			line=inStr.readLine()
			tokens=line.split("=")
			if tokens[0]=="agencyName":
				self.agencyName=tokens[1]
			elif tokens[0]=="datum":
				self.datum=tokens[1]
			elif tokens[0]=="coordFormat":
				self.coordFormatAscii=tokens[1]
			elif tokens[0]=="timeoutMinutes":
				self.timeoutMinutes=tokens[1]
			elif tokens[0]=="logo":
				self.printLogoFileName=tokens[1]
			elif tokens[0]=="firstWorkingDir":
				self.firstWorkingDir=tokens[1]
			elif tokens[0]=="secondWorkingDir":
				self.secondWorkingDir=tokens[1]
			elif tokens[0]=="server":
				self.sarsoftServerName=tokens[1]
			elif tokens[0]=="rotateScript":
				self.rotateScript=tokens[1]
			elif tokens[0]=="rotateDelimiter":
				self.rotateDelimiter=tokens[1]
			elif tokens[0]=="tabGroups":
				self.tabGroups=eval(tokens[1])
			elif tokens[0]=="continuedIncidentWindowDays":
				self.continuedIncidentWindowDays=tokens[1]
		configFile.close()
		
		# validation and post-processing of each item
		configErr=""
		self.printLogoFileName=os.path.join(self.configDir,self.printLogoFileName)
		
		if self.datum not in self.validDatumList:
			configErr+="ERROR: invalid datum '"+self.datum+"'\n"
			configErr+="  Valid choices are: "+str(self.validDatumList)+"\n"
			configErr+="  Will use "+str(self.validDatumList[0])+" for this session.\n\n"
			self.datum=self.validDatumList[0]
		# if specified datum is just NAD27, assume NAD27 CONUS
		if self.datum=="NAD27":
			self.datum="NAD27 CONUS"

		if self.coordFormatAscii not in self.csDisplayDict:
			configErr+="ERROR: coordinate format '"+self.coordFormatAscii+"'\n"
			configErr+="  Supported coordinate format names are: "+str(list(self.csDisplayDict.keys()))+"\n"
			configErr+="  Will use "+list(self.csDisplayDict.keys())[0]+" for this session.\n\n"
			self.coordFormatAscii=list(self.csDisplayDict.keys())[0]
		
		# process any ~ characters
		self.firstWorkingDir=os.path.expanduser(self.firstWorkingDir)
		if self.secondWorkingDir:				
			self.secondWorkingDir=os.path.expanduser(self.secondWorkingDir)				

		if not os.path.isdir(self.firstWorkingDir):
			configErr="FATAL ERROR: first working directory '"+self.firstWorkingDir+"' does not exist.  ABORTING."
			self.configErrMsgBox=QMessageBox(QMessageBox.Critical,"Fatal Configuration Error",configErr,
 							QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			self.configErrMsgBox.exec_()
			sys.exit(-1)
			
		if self.use2WD and self.secondWorkingDir and not os.path.isdir(self.secondWorkingDir):
			configErr+="ERROR: second working directory '"+self.secondWorkingDir+"' does not exist.  Maybe it is not mounted yet; radiolog will try to write to it after every entry.\n\n"
		
		self.coordFormat=self.csDisplayDict[self.coordFormatAscii]
		self.ui.datumFormatLabel.setText(self.datum+"\n"+self.coordFormat)
	
		if not self.timeoutMinutes.isdigit():
			configErr+="ERROR: timeout minutes value must be an integer.  Will use 30 minutes for this session.\n\n"
			self.timeoutMinutes=30
		self.timeoutRedSec=int(self.timeoutMinutes)*60
		if not self.timeoutRedSec in self.timeoutDisplaySecList:
			configErr+="ERROR: invalid timeout period ("+str(self.timeoutMinutes)+" minutes)\n"
			configErr+="  Valid choices:"+str(self.timeoutDisplayMinList)+"\nWill use 30 minutes for this session.\n\n"
			self.timeoutRedSec=1800
		
		self.updateOptionsDialog()
		
		# if agencyName contains newline character(s), use it as-is for print;
		#  if not, textwrap with max line length that looks best on pdf reports
		self.agencyNameForPrint=self.agencyName
		if not "\n" in self.agencyName:
			self.agencyNameForPrint="\n".join(textwrap.wrap(self.agencyName.upper(),width=len(self.agencyName)/2+6))
		
		if not os.path.isfile(self.printLogoFileName):
			configErr+="ERROR: specified logo file '"+self.printLogoFileName+"' does not exist.  No logo will be included on generated reports.\n\n"
		
		if not isinstance(self.tabGroups,list):
			configErr+="ERROR: specified tab group '"+str(self.tabGroups)+"' is not a list.  Using the default tabGroups group list.\n\n"
			self.tabGroups=defaultTabGroups

		if not self.continuedIncidentWindowDays.isdigit():
			configErr+="ERROR: continuedIncidentWindowDays value must be an integer.  Will use 4 days for this session.\n\n"
			self.continuedIncidentWindowDays=4
		else:
			self.continuedIncidentWindowDays=int(self.continuedIncidentWindowDays)
			 
		if configErr:
			self.configErrMsgBox=QMessageBox(QMessageBox.Warning,"Non-fatal Configuration Error(s)","Error(s) encountered in config file "+self.configFileName+":\n\n"+configErr,
 							QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			self.configErrMsgBox.exec_()

		if develMode:
			self.sarsoftServerName="localhost" # DEVEL

	def rotateCsvBackups(self,filenames):
		if self.rotateScript and self.rotateDelimiter:
			# #442: wrap each filename in quotes, to allow spaces in filenames
			#  from https://stackoverflow.com/a/12007707
			#  wrapping in one or two sets of double quotes still doesn't work
			#   since the quotes are stripped by powershell; wrapping in three
			#   double quotes does work:
			quotedFilenames=[f'"""{filename}"""' for filename in filenames]
			cmd=self.rotateScript+' '+self.rotateDelimiter.join(quotedFilenames)
			rprint("Invoking backup rotation script: "+cmd)
			subprocess.Popen(cmd)
		else:
			rprint("No backup rotation script and/or delimiter was specified; no rotation is being performed.")
		
	def updateOptionsDialog(self):
		rprint("updating options dialog: datum="+self.datum)
		self.optionsDialog.ui.datumField.setCurrentIndex(self.optionsDialog.ui.datumField.findText(self.datum))
		self.optionsDialog.ui.formatField.setCurrentIndex(self.optionsDialog.ui.formatField.findText(self.coordFormat))
		self.optionsDialog.ui.timeoutField.setValue(self.timeoutDisplaySecList.index(int(self.timeoutRedSec)))
		self.optionsAccepted() # at the very least, this sets timeoutOrangeSec

	def setColumnResizedFlag(self):
		self.columnResizedFlag=True

	def resizeRowsToContentsIfNeeded(self):
		if self.columnResizedFlag and not self.loadFlag:
			self.columnResizedFlag=False
			self.ui.tableView.resizeRowsToContents()
			self.ui.tableView.scrollToBottom()
			for n in self.ui.tableViewList[1:]:
				n.resizeRowsToContents()
		
	def fsMuteBlink(self,state):
		if state=="on":
			self.ui.incidentNameLabel.setText("FleetSync Muted")
			self.ui.incidentNameLabel.setStyleSheet("background-color:#ff5050;color:white;font-size:"+str(self.limitedFontSize)+"pt;")
			self.ui.fsCheckBox.setStyleSheet("border:3px outset red")
		else:
			if state=="noSend":
				self.ui.incidentNameLabel.setText("FS Locators Muted")
				self.ui.incidentNameLabel.setStyleSheet("background-color:#ff5050;color:white;font-size:"+str(self.limitedFontSize)+"pt;")
				self.ui.fsCheckBox.setStyleSheet("border:3px outset red")
			else:
				self.ui.incidentNameLabel.setText(self.incidentName)
				self.ui.incidentNameLabel.setStyleSheet("background-color:none;color:black;font-size:"+str(self.limitedFontSize)+"pt;")
				self.ui.fsCheckBox.setStyleSheet("border:3px inset lightgray")
	
	def fsFilterBlink(self,state):
		if state=="on":
			self.ui.fsFilterButton.setStyleSheet("QToolButton { background-color:#ff5050;border:2px outset lightgray; }")
		else:
			self.ui.fsFilterButton.setStyleSheet("QToolButton { }")
			
	def fsFilterEdit(self,fleet,dev,state=True):
# 		rprint("editing filter for "+str(fleet)+" "+str(dev))
		for row in self.fsLog:
# 			rprint("row:"+str(row))
			if row[0]==fleet and row[1]==dev:
# 				rprint("found")
				row[3]=state
				self.fsBuildTooltip()
				self.fsFilterDialog.ui.tableView.model().layoutChanged.emit()
				return
	
	def fsAnythingFiltered(self):
		for row in self.fsLog:
			if row[3]==True:
				return True
		return False
	
	def fsGetTeamFilterStatus(self,extTeamName):
		# 0 - no devices belonging to this callsign are filtered
		# 1 - some but not all devices belonging to this callsign are filtered
		# 2 - all devices belonging to this callsign are filtered
		total=0
		filtered=0
		for row in self.fsLog:
			if getExtTeamName(row[2])==extTeamName:
				total+=1
				if row[3]==True:
					filtered+=1
		if filtered==0:
			return 0
		if filtered<total:
			return 1
		if filtered==total:
			return 2
	
	def fsGetTeamDevices(self,extTeamName):
		# return a list of two-element lists [fleet,dev]
		# rprint('fsGetTeamDevices called for extTeamName='+extTeamName)
		# rprint('self.fsLog='+str(self.fsLog))
		rval=[]
		for row in self.fsLog:
			if getExtTeamName(row[2])==extTeamName:
				rval.append([row[0],row[1]])
		# rprint('returning '+str(rval))
		return rval
		
	def fsFilteredCallDisplay(self,state="off",fleet=0,dev=0,callsign=''):
		if state=="on":
			self.ui.incidentNameLabel.setText("Incoming FS call filtered/ignored:\n"+callsign+"   ("+str(fleet)+":"+str(dev)+")")
			self.ui.incidentNameLabel.setStyleSheet("background-color:#ff5050;color:white;font-size:"+str(self.limitedFontSize/2)+"pt")
		else:
			self.ui.incidentNameLabel.setText(self.incidentName)
			self.ui.incidentNameLabel.setStyleSheet("background-color:none;color:black;font-size:"+str(self.limitedFontSize)+"pt")
				
	def fsCheckBoxCB(self):
		# 0 = unchecked / empty: mute fleetsync completely
		# 1 = partial check / square: listen for CID and location, but do not send locator requests
		# 2 = checked (normal behavior): listen for CID and location, and send locator requests
		self.fsMuted=self.ui.fsCheckBox.checkState()==0
		self.noSend=self.ui.fsCheckBox.checkState()<2
		# blinking is handled in fsCheck which is called once a second anyway;
		# make sure to set display back to normal if mute was just turned off
		#  since we don't know the previous blink state
		if self.fsMuted:
			rprint("FleetSync is now muted")
			self.fsMuteBlink("on") # blink on immediately so user sees immediate response
		else:
			if self.noSend:
				rprint("Fleetsync is unmuted but locator requests will not be sent")
				self.fsMuteBlink("noSend")
			else:
				rprint("Fleetsync is unmuted and locator requests will be sent")
				self.fsMuteBlink("off")
				self.ui.incidentNameLabel.setText(self.incidentName)
				self.ui.incidentNameLabel.setStyleSheet("background-color:none;color:black;font-size:"+str(self.limitedFontSize)+"pt;")
			
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
		if self.fsAwaitingResponse:
			if self.fsAwaitingResponse[3]>=self.fsAwaitingResponseTimeout:
				rprint('Fleetsync timed out awaiting response')
				self.fsFailedFlag=True
				try:
					self.fsTimedOut=True
					self.fsAwaitingResponseMessageBox.close()
				except:
					pass
				# rprint('q1: fsThereWillBeAnotherTry='+str(self.fsThereWillBeAnotherTry))
				if not self.fsThereWillBeAnotherTry:
					# values format for adding a new entry:
					#  [time,to_from,team,message,self.formattedLocString,status,self.sec,self.fleet,self.dev,self.origLocString]
					values=["" for n in range(10)]
					values[0]=time.strftime("%H%M")
					values[6]=time.time()
					[f,dev]=self.fsAwaitingResponse[0:2]
					callsignText=self.getCallsign(f,dev)
					values[2]=str(callsignText)
					if callsignText:
						callsignText='('+callsignText+')'
					else:
						callsignText='(no callsign)'
					if self.fsAwaitingResponse[2]=='Location request sent':
						values[3]='FLEETSYNC: No response received for location request from '+str(f)+':'+str(dev)+' '+callsignText
					elif self.fsAwaitingResponse[2]=='Text message sent':
						msg=self.fsAwaitingResponse[4]
						values[1]='TO'
						values[3]='FLEETSYNC: Text message sent to '+str(f)+':'+str(dev)+' '+callsignText+' but delivery was NOT confirmed: "'+msg+'"'
					else:
						values[3]='FLEETSYNC: Timeout after unknown command type "'+self.fsAwaitingResponse[2]+'"'
					self.newEntry(values)
					msg='FleetSync did not respond within the expected timeframe.'
					if self.fsAwaitingResponse[2]=='Location request sent':
						msg+='\n\nThis could happen after a location request for one of several reasons:\n  - The radio in question was off\n  - The radio in question was on, but not set to this channel\n  - The radio in question was on and set to this channel, but had no GPS fix'
					self.fsAwaitingResponse=None # clear the flag
					if len(self.fsSendList)==1:
						box=QMessageBox(QMessageBox.Critical,'FleetSync timeout',msg,
							QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
						box.open()
						box.raise_()
						box.exec_()
					else:
						self.fsResponseMessage+='\n\n'+str(f)+':'+str(dev)+' '+callsignText+':'+msg
			else:
				self.fsAwaitingResponse[3]+=1
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
					except serial.serialutil.SerialException as err:
						if "ClearCommError failed" in str(err):
							rprint("  COM port unplugged.  Scan continues...")
							self.comPortTryList.remove(comPortTry)
					except:
						pass # unicode decode errors may occur here for non-radio com devices
					else:
						if isWaiting:
							rprint("     DATA IS WAITING!!!")
							tmpData=comPortTry.read(comPortTry.inWaiting()).decode("utf-8")
							if '\x02I' in tmpData or tmpData=='\x020\x03' or tmpData=='\x021\x03' or tmpData.startswith('\x02$PKL'):
								rprint("      VALID FLEETSYNC DATA!!!")
								self.fsBuffer=self.fsBuffer+tmpData

								if not self.firstComPortFound:
									self.firstComPort=comPortTry # pass the actual open com port object, to keep it open
									self.firstComPortFound=True
									self.fsLatestComPort=self.firstComPort
								else:
									self.secondComPort=comPortTry # pass the actual open com port object, to keep it open
									self.secondComPortFound=True
									self.fsLatestComPort=self.secondComPort
								self.comPortTryList.remove(comPortTry) # and remove the good com port from the list of ports to try going forward
							else:
								rprint("      but not valid fleetsync data.  Scan continues...")
								rprint(str(tmpData))
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
				if "ClearCommError failed" in str(err):
					rprint("first COM port unplugged")
					self.firstComPortFound=False
					self.firstComPortAlive=False
					self.ui.firstComPortField.setStyleSheet("background-color:#bb0000")
			if waiting:
				self.ui.firstComPortField.setStyleSheet("background-color:#00ff00")
				self.fsBuffer=self.fsBuffer+self.firstComPort.read(waiting).decode('utf-8')
				self.fsLatestComPort=self.firstComPort
		if self.secondComPortFound:
# 			self.ui.secondComPortField.setStyleSheet("background-color:#00bb00")
			waiting=0
			try:
				waiting=self.secondComPort.inWaiting()
			except serial.serialutil.SerialException as err:
				if "ClearCommError failed" in str(err):
					rprint("second COM port unplugged")
					self.secondComPortFound=False
					self.secondComPortAlive=False
					self.ui.secondComPortField.setStyleSheet("background-color:#bb0000")
			if waiting:
				self.ui.secondComPortField.setStyleSheet("background-color:#00ff00")
				self.fsBuffer=self.fsBuffer+self.secondComPort.read(waiting).decode('utf-8')
				self.fsLatestComPort=self.secondComPort

		# don't process fsMuted before this point: we need to read the com ports
		#  even if they are muted, so that the com port buffers don't fill up
		#  while muted, which would result in buffer overrun or just all the
		#  queued up fs traffic being processed when fs is unmuted
		if self.fsMuted or self.noSend:
			if self.fsMuted:
				self.fsBuffer="" # make sure the buffer is clear, i.e. any incoming
			 		# fs traffic while muted should be read but disregarded
			if (self.fsMuted or self.noSend):
				self.fsMutedBlink=not self.fsMutedBlink
			if self.fsMutedBlink:
				if self.fsMuted:
					self.fsMuteBlink("on")
				else:
					if self.noSend:
						self.fsMuteBlink("noSend")
			else:
				self.fsMuteBlink("off")
				
		if self.fsAnythingFiltered():
			self.fsFilterBlinkState=not self.fsFilterBlinkState
			if self.fsFilterBlinkState:
				self.fsFilterBlink("on")
			else:
				self.fsFilterBlink("off")
		else:
			self.fsFilterBlink("off")
		
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
		fleet=None
		dev=None
		# the line delimeters are literal backslash then n, rather than standard \n
		for line in self.fsBuffer.split('\n'):
			rprint(" line:"+line)
			if line=='\x020\x03':
				# success response code - happens in these cases:
				# - positive acknowledge received after text sent to individual device
				# - broadcast text sent (target radios will not try to respond to broadcast)
				# - positive acknowledge received after location poll, regardless of response from portable radio;
				#     if target radio has a GPS lock, either current (A status) or stale (V status), 
				#     the next lines will include $PKLSH etc.  In this case, there is no action to take;
				#     just move on to the next line.
				if self.fsAwaitingResponse and self.fsAwaitingResponse[2]=='Text message sent':
					[f,dev]=self.fsAwaitingResponse[0:2]
					msg=self.fsAwaitingResponse[4]
					self.fsAwaitingResponse=None # clear the flag before closing the messagebox
					try:
						self.fsAwaitingResponseMessageBox.close()
					except:
						pass
					recipient=''
					suffix=''
					# values format for adding a new entry:
					#  [time,to_from,team,message,self.formattedLocString,status,self.sec,self.fleet,self.dev,self.origLocString]
					values=["" for n in range(10)]
					values[0]=time.strftime("%H%M")
					values[1]='TO'
					if int(f)==0 and int(dev)==0:
						recipient='all devices'
						values[2]='ALL'
					else:
						callsignText=self.getCallsign(f,dev)
						values[2]=str(callsignText)
						if callsignText:
							callsignText='('+callsignText+')'
						else:
							callsignText='(no callsign)'
						recipient=str(f)+':'+str(dev)+' '+callsignText
						suffix=' and delivery was confirmed'
					values[3]='FLEETSYNC: Text message sent to '+recipient+suffix+': "'+msg+'"'
					values[6]=time.time()
					self.newEntry(values)
					rprint('FLEETSYNC: Text message sent to '+recipient+suffix)
					return
			if line=='\x021\x03': # failure response
				if self.fsAwaitingResponse:
					# rprint('q2: fsThereWillBeAnotherTry='+str(self.fsThereWillBeAnotherTry))
					if not self.fsThereWillBeAnotherTry:
						# values format for adding a new entry:
						#  [time,to_from,team,message,self.formattedLocString,status,self.sec,self.fleet,self.dev,self.origLocString]
						values=["" for n in range(10)]
						values[0]=time.strftime("%H%M")
						[f,dev]=self.fsAwaitingResponse[0:2]
						callsignText=self.getCallsign(f,dev)
						values[2]=str(callsignText)
						if callsignText:
							callsignText='('+callsignText+')'
						else:
							callsignText='(no callsign)'
						recipient=str(f)+':'+str(dev)+' '+callsignText
						values[3]='FLEETSYNC: NO RESPONSE from '+recipient
						values[6]=time.time()
						self.newEntry(values)
						self.fsFailedFlag=True
						try:
							self.fsAwaitingResponseMessageBox.close()
						except:
							pass
						self.fsAwaitingResponse=None # clear the flag
						rprint('FLEETSYNC: NO RESPONSE from '+recipient)
						return
			if '$PKLSH' in line:
				lineParse=line.split(',')
				if len(lineParse)==10:
					[pklsh,nval,nstr,wval,wstr,utc,valid,fleet,dev,chksum]=lineParse
					callsign=self.getCallsign(fleet,dev)
					rprint("$PKLSH detected containing CID: fleet="+fleet+"  dev="+dev+"  -->  callsign="+callsign)
					# OLD RADIOS (2180):
					# unusual PKLSH lines seen from log files:
					# $PKLSH,2913.1141,N,,,175302,A,100,2016,*7A - no data for west - this caused
					#   parsing error "ValueError: invalid literal for int() with base 10: ''"
					# $PKLSH,3851.3330,N,09447.9417,W,012212,V,100,1202,*23 - what's 'V'?
					#   in standard NMEA sentences, status 'V' = 'warning'.  Dead GPS mic?
					#   we should flag these to the user somehow; note, the coordinates are
					#   for the Garmin factory in Olathe, KS
					# - if valid=='V' set coord field to 'WARNING', do not attempt to parse, and carry on
					# - if valid=='A' and coords are incomplete or otherwise invalid, set coord field
					#    to 'INVALID', do not attempt to parse, and carry on
					# 
					# NEW RADIOS (NX5200):
					# $PKLSH can contain status 'V' if it had a GPS lock before but does not currently,
					#   in which case the real coodinates of the last known lock will be included.
					#   If this happens, we do want to see the coordinates in the entry body, but we do not want
					#   to update the sartopo locator.
					# - iv valid=='V', append the formatted string with an asterisk, but do not update the locator
					# - if valid=='A' - as with old radios
					# so:
					# if valid=='A':  # only process if there is a GPS lock
					if valid!='Z':  # process regardless of GPS lock
						locList=[nval,nstr,wval,wstr]
						origLocString='|'.join(locList) # don't use comma, that would conflict with CSV delimeter
						validated=True
						try:
							float(nval)
						except ValueError:
							validated=False
						try:
							float(wval)
						except ValueError:
							validated=False
						validated=validated and nstr in ['N','S'] and wstr in ['W','E']
						if validated:
							rprint("Valid location string:'"+origLocString+"'")
							formattedLocString=self.convertCoords(locList,self.datum,self.coordFormat)
							rprint("Formatted location string:'"+formattedLocString+"'")
							[lat,lon]=self.convertCoords(locList,targetDatum="WGS84",targetFormat="D.dList")
							rprint("WGS84 lat="+str(lat)+"  lon="+str(lon))
							if valid=='A': # don't update the locator if valid=='V'
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
							# was this a response to a location request for this device?
							if self.fsAwaitingResponse and [int(fleet),int(dev)]==[int(x) for x in self.fsAwaitingResponse[0:2]]:
								try:
									self.fsAwaitingResponseMessageBox.close()
								except:
									pass
								# values format for adding a new entry:
								#  [time,to_from,team,message,self.formattedLocString,status,self.sec,self.fleet,self.dev,self.origLocString]
								values=["" for n in range(10)]
								values[0]=time.strftime("%H%M")
								values[1]='FROM'
								values[4]=formattedLocString
								if valid=='A':
									prefix='SUCCESSFUL RESPONSE'
								elif valid=='V':
									prefix='RESPONSE WITH WARNING CODE (probably indicates a stale GPS lock)'
									values[4]='*'+values[4]+'*'
								else:
									prefix='UNKNOWN RESPONSE CODE "'+str(valid)+'"'
									values[4]='!'+values[4]+'!'
								callsignText=self.getCallsign(fleet,dev)
								values[2]=callsignText or ''
								if callsignText:
									callsignText='('+callsignText+')'
								else:
									callsignText='(no callsign)'
								values[3]='FLEETSYNC LOCATION REQUEST: '+prefix+' from device '+str(fleet)+':'+str(dev)+' '+callsignText
								values[6]=time.time()
								self.newEntry(values)
								rprint(values[3])
								t=self.fsAwaitingResponse[2]
								self.fsAwaitingResponse=None # clear the flag
								self.fsAwaitingResponseMessageBox=QMessageBox(QMessageBox.Information,t,values[3]+':\n\n'+formattedLocString+'\n\nNew entry created with response coordinates.',
												QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
								self.fsAwaitingResponseMessageBox.show()
								self.fsAwaitingResponseMessageBox.raise_()
								self.fsAwaitingResponseMessageBox.exec_()
								return # done processing this FS traffic - don't spawn a new entry dialog
						else:
							rprint("INVALID location string parsed from $PKLSH: '"+origLocString+"'")
							origLocString='INVALID'
							formattedLocString='INVALID'
					elif valid=='Z':
						origLocString='NO FIX'
						formattedLocString='NO FIX'
					elif valid=='V':
						rprint("WARNING status character parsed from $PKLSH; check the GPS mic attached to that radio")
						origLocString='WARNING'
						formattedLocString='WARNING'
					else:
						origLocString='UNDEFINED'
						formattedLocString='UNDEFINED'
				else:
					rprint("Parsed line contained "+str(len(lineParse))+" tokens instead of the expected 10; skipping.")
					origLocString='BAD DATA'
					formattedLocString='BAD DATA'
			elif '\x02I' in line:
				# caller ID lines look like " I110040021004002" (first character is \x02, may show as a space)
				# " I<n>" is a prefix, n is either 0 or 1 (not sure why)
				# the next three characters (100 above) are the fleet#
				# the next four characters (4002 above) are the device#
				# fleet and device# are repeated
				# apparently a delay elsewhere can result in an extra leading character here;
				#  so, find the exact characters rather than assuming character index
				i=line.index('\x02I')
				fleet=line[i+3:i+6]
				dev=line[i+6:i+10]
				callsign=self.getCallsign(fleet,dev)
				rprint("CID detected (not in $PKLSH): fleet="+fleet+"  dev="+dev+"  callsign="+callsign)
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
				rprint("  new entry widget is already open from this callsign within the 'continue time'; not opening a new one")
				prevLocString=widget.ui.radioLocField.toPlainText()
				# if previous location string was blank, always overwrite;
				#  if previous location string was not blank, only overwrite if new location is valid
				if prevLocString=='' or (formattedLocString!='' and formattedLocString!='NO FIX'):
					datumFormatString="("+self.datum+"  "+self.coordFormat+")"
					if widget.relayed:
						rprint("location strings not updated because the message is relayed")
						widget.radioLocTemp=formattedLocString
						widget.datumFormatTemp=datumFormatString
					else:
						rprint("location strings updated because the message is not relayed")
						widget.ui.radioLocField.setText(formattedLocString)
						widget.ui.datumFormatLabel.setText(datumFormatString)
						widget.formattedLocString=formattedLocString
						widget.origLocString=origLocString
				# #509: populate radio location field in any child dialogs that have that field (clue or subject located)
				for child in widget.childDialogs:
					rprint('  new entry widget for '+str(callsign)+' has a child dialog; attempting to update radio location in that dialog')
					try:
						# need to account for widgets that have .toPlainText() method (in clueDialog)
						#  and widgets that have .text() method (in subjectLocatedDialog)
						try:
							prevLocString=child.ui.radioLocField.toPlainText()
						except:
							prevLocString=child.ui.radioLocField.text()
						#  only populate with the radio location of the first call - don't keep updating with subsequent calls
						#  (could be changed in the future if needed - basically, should the report include the radio coords of
						#   the first call of the report, or of the last call of a continued conversation before the report is saved?)
						if prevLocString=='' and formattedLocString!='' and formattedLocString!='NO FIX':
							child.ui.radioLocField.setText(formattedLocString)
					except:
						pass
		if fleet and dev:
			self.fsLogUpdate(int(fleet),int(dev))
			# only open a new entry widget if the fleet/dev is not being filtered
			if not found:
				if self.fsIsFiltered(int(fleet),int(dev)):
					self.fsFilteredCallDisplay("on",fleet,dev,callsign)
					QTimer.singleShot(5000,self.fsFilteredCallDisplay) # no arguments will clear the display
				else:
					self.openNewEntry('fs',callsign,formattedLocString,fleet,dev,origLocString)
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
		if not self.noSend:
			if self.getString!='': # to avoid sending a GET string that is nothing but the callsign
				self.getString=self.getString+suffix
			if self.getString!='' and not self.getString.endswith("-"):
				rprint("calling processEvents before sending GET request...")
				QCoreApplication.processEvents()
				try:
					rprint("Sending GET request:")
					rprint(self.getString)
					# fire-and-forget: completely ignore the response, but, return immediately
					r=requests.get(self.getString,timeout=0.0001)
					rprint("  request sent")
					rprint("  response: "+str(r))
				except Exception as e:
					rprint("  exception during sending of GET request: "+str(e))
				self.getString=''
				
	# for fsLog, a dictionary would probably be easier, but we have to use an array
	#  since we will be displaying in a QTableView
	# if callsign is specified, update the callsign but not the time;
	#  if callsign is not specified, udpate the time but not the callsign;
	#  if the entry does not yet exist, add it
	def fsLogUpdate(self,fleet,dev,callsign=False):
		# row structure: [fleet,dev,callsign,filtered,last_received,com port]
		rprint("fsLogUpdate called: fleet="+str(fleet)+" dev="+str(dev)+" callsign="+(callsign or "<None>")+"  COM port="+self.fsLatestComPort.name)
		found=False
		t=time.strftime("%a %H:%M:%S")
		com=str(self.fsLatestComPort.name)
		for row in self.fsLog:
			if row[0]==fleet and row[1]==dev:
				found=True
				if callsign:
					row[2]=callsign
				else:
					row[4]=t
				row[5]=com
		if not found:
			# always update callsign - it may have changed since creation
			self.fsLog.append([fleet,dev,self.getCallsign(fleet,dev),False,t,com])
# 		rprint(self.fsLog)
# 		if self.fsFilterDialog.ui.tableView:
		self.fsFilterDialog.ui.tableView.model().layoutChanged.emit()
		self.fsBuildTeamFilterDict()
	
	def fsGetLatestComPort(self,fleet,device):
		rprint('fsLog:'+str(self.fsLog))
		log=[x for x in self.fsLog if x[0:2]==[int(fleet),int(device)]]
		if len(log)==1:
			comPortName=log[0][5]
		elif len(log)>1:
			rprint('WARNING: there are multiple fsLog entries for '+str(fleet)+':'+str(device))
			comPortName=log[0][5]
		else:
			rprint('WARNING: '+str(fleet)+':'+str(device)+' has no fsLog entry so it probably has not been heard from yet')
			comPortName=None
		# rprint('returning '+str(comPortName))
		if self.firstComPort and self.firstComPort.name==comPortName:
			return self.firstComPort
		elif self.secondComPort and self.secondComPort.name:
			return self.secondComPort

	def fsBuildTeamFilterDict(self):
		for extTeamName in teamFSFilterDict:
			teamFSFilterDict[extTeamName]=self.fsGetTeamFilterStatus(extTeamName)
					
	def fsBuildTooltip(self):
		filteredHtml=""
		for row in self.fsLog:
			if row[3]==True:
				filteredHtml+="<tr><td>"+row[2]+"</td><td>"+str(row[0])+"</td><td>"+str(row[1])+"</td></tr>"
		if filteredHtml != "":
			tt="Filtered devices:<br>(left-click to edit)<table border='1' cellpadding='3'><tr><td>Callsign</td><td>Fleet</td><td>ID</td></tr>"+filteredHtml+"</table>"
		else:
			tt="No devices are currently being filtered.<br>(left-click to edit)"
		self.ui.fsFilterButton.setToolTip(tt)

	def fsIsFiltered(self,fleet,dev):
# 		rprint("checking fsFilter: fleet="+str(fleet)+" dev="+str(dev))
		# disable fsValidFleetList checking to allow arbitrary fleets; this
		#  idea is probably obsolete
		# invalid fleets are always filtered, to prevent fleet-glitches (110-xxxx) from opening new entries
# 		if int(fleet) not in self.fsValidFleetList:
# 			rprint("true1")
# 			return True
		# if the fleet is valid, check for filtered device ID
		for row in self.fsLog:
			if row[0]==fleet and row[1]==dev and row[3]==True:
# 				rprint("  device is fitlered; returning True")
				return True
# 		rprint("not filtered; returning False")
		return False

	def fsLoadLookup(self,startupFlag=False,fsFileName=None,hideWarnings=False):
		rprint("fsLoadLookup called: startupFlag="+str(startupFlag)+"  fsFileName="+str(fsFileName)+"  hideWarnings="+str(hideWarnings))
		if not startupFlag and not fsFileName: # don't ask for confirmation on startup or on restore
			really=QMessageBox(QMessageBox.Warning,'Please Confirm','Are you sure you want to reload the default FleetSync lookup table?  This will overwrite any callsign changes you have made.',
				QMessageBox.Yes|QMessageBox.No,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			really.setDefaultButton(QMessageBox.No)
			really.show()
			really.raise_()
			if really.exec_()==QMessageBox.No:
				return
		fsEmptyFlag=False
		if len(self.fsLookup)==0:
			fsEmptyFlag=True
		if not fsFileName:
			fsFileName=self.fsFileName
		if os.path.isfile(fsFileName):
			fsFullPath=fsFileName
		else:
			if startupFlag:
				fsDir=self.configDir
			else:
				fsDir=self.sessionDir
			# rprint('t1: fsDir='+fsDir+'  fsFileName='+fsFileName)
			fsFullPath=os.path.join(fsDir,fsFileName)
		try:
			rprint("  trying "+fsFullPath)
			with open(fsFullPath,'r') as fsFile:
				rprint("Loading FleetSync Lookup Table from file "+fsFullPath)
				self.fsLookup=[]
				csvReader=csv.reader(fsFile)
				for row in csvReader:
					if row and not row[0].startswith("#"): # allow blank lines and comment lines
						self.fsLookup.append(row)
				if not startupFlag: # suppress message box on startup
					self.fsMsgBox=QMessageBox(QMessageBox.Information,"Information","FleetSync ID table has been re-loaded from file "+fsFullPath+".",
											QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
					self.fsMsgBox.show()
					QCoreApplication.processEvents()
					QTimer.singleShot(2000,self.fsMsgBox.close)
		except:
			if not hideWarnings:
				if fsEmptyFlag:
					warn=QMessageBox(QMessageBox.Warning,"Warning","Cannot read FleetSync ID table file '"+fsFullPath+"' and no FleetSync ID table has yet been loaded.  Callsigns for incoming FleetSync calls will be of the format 'KW-<fleet>-<device>'.\n\nThis warning will automatically close in a few seconds.",
									QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
				else:
					warn=QMessageBox(QMessageBox.Warning,"Warning","Cannot read FleetSync ID table file '"+fsFullPath+"'!  Using existing settings.\n\nThis warning will automatically close in a few seconds.",
									QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
				warn.show()
				warn.raise_()
				QTimer.singleShot(8000,warn.close)
				warn.exec_()

	# save to fsFileName in the working dir each time, but on startup, load from the default dir;
	#  would only need to load from the working dir if restoring
	def fsSaveLookup(self):
		fsFullPath=os.path.join(self.sessionDir,self.fsFileName)
		try:
			with open(fsFullPath,'w',newline='') as fsFile:
				rprint("Writing file "+fsFullPath)
				csvWriter=csv.writer(fsFile)
				csvWriter.writerow(["## Radio Log FleetSync lookup table"])
				csvWriter.writerow(["## File written "+time.strftime("%a %b %d %Y %H:%M:%S")])
				csvWriter.writerow(["## Created during Incident Name: "+self.incidentName])
				for row in self.fsLookup:
					csvWriter.writerow(row)
				csvWriter.writerow(["## end"])
		except:
			warn=QMessageBox(QMessageBox.Warning,"Warning","Cannot write FleetSync ID table file "+fsFullPath+"!  Any modified FleetSync Callsign associations will be lost.",
							QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			warn.show()
			warn.raise_()
			warn.exec_()

	def getCallsign(self,fleet,dev):
		entry=[element for element in self.fsLookup if (str(element[0])==str(fleet) and str(element[1])==str(dev))]
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

	# convertCoords
	#   coords - 4-element list of strings
	#      [LatString,NS,LonString,EW]  ex. ['3912.2949', 'N', '12104.5526', 'W']
	#      LatString - in the format that Kenwood produces: DDMM.mmmm
	#          (3912.2949 = 39deg 12.2949min)
	#      NS - North or South hemisphere
	#      LonString - in the format that Kenwood produces: DDMM.mmmm
	#      EW - Eeast or West hemisphere
	#          (W along with a positive LonString means the lon value is actually negative)
	#          12034.5678 W  --> -120deg 34.5678min
	#   targetDatum - 'WGS84' or 'NAD27' or 'NAD27 CONUS' (the last two are synonyms in this usage)
	def convertCoords(self,coords,targetDatum,targetFormat):
		rprint("convertCoords called: targetDatum="+targetDatum+" targetFormat="+targetFormat+" coords="+str(coords))
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
				latDd=-latDd
			if coords[3]=="W":
				lonDeg=-lonDeg # invert if needed
				lonDd=-lonDd
			# UTM Zone calculation no longer needed since pygeodesy does it internally - left here as a comment for reference
			# targetUTMZone=math.floor((lonDd+180)/6)+1 # from http://stackoverflow.com/questions/9186496, since -120.0000deg should be zone 11, not 10
		else:
			return("INVALID INPUT FORMAT - MUST BE A LIST")

		# 1. create a LLEB object from the input coordinate pair
		g=ellipsoidalBase.LatLonEllipsoidalBase(latDd,lonDd,datum=Datums.WGS84)

		# 2. convert/reproject datum if needed
		if 'NAD27' in targetDatum:
			g=g.toDatum(Datums.NAD27)

		# 3. return the requested format
		# desired accuracy / digits of precision - these match caltopo, except for seconds
		# at 39 degrees north,
		# 0.00001 degree latitude = 1.11 meters
		# 0.001 minute latutude = 1.85 meters
		# 0.1 second latitude = 3.08 meters
		# (longitude lengths are about 78% as much as latitude, at 39 degrees north)
		if targetFormat=="D.dList":
			return [g.lat,g.lon]
		if targetFormat=="D.d°":
			return g.toStr(dms.F_D,joined='  ',prec=-5)
		if targetFormat=="D° M.m'":
			return g.toStr(dms.F_DM,joined='  ',prec=-3,s_D="° ",s_M="'")
		if targetFormat=="D° M' S.s\"":
			return g.toStr(dms.F_DMS,joined='  ',prec=-1,s_D="° ",s_M="' ",s_S='"')
		if 'UTM' in targetFormat:
			g=g.toUtm() # fewer formatting options exist for utm objects; build the strings from components below
			eStr="{0:07d}".format(round(g.easting))
			nStr="{0:07d}".format(round(g.northing))
			zone=g.zone # utm zone
			band=g.band # latitude band
			if 'FULL' in targetFormat.upper():
				if 'SHORT' in targetFormat.upper():
					return "{}{} {} {}".format(zone,band,eStr,nStr)
				else:
					return "{}{} {} {}   {} {}".format(zone,band,eStr[0:2],eStr[2:],nStr[0:2],nStr[2:])
			if '7x7' in targetFormat:
				if 'SHORT' in targetFormat.upper():
					return "{} {}".format(eStr,nStr)
				else:
					return "{} {}   {} {}".format(eStr[0:2],eStr[2:],nStr[0:2],nStr[2:])
			if targetFormat=="UTM 5x5":
				return "{}  {}".format(eStr[2:],nStr[2:])
		return "INVALID - UNKNOWN OUTPUT FORMAT REQUESTED"

	def printLogHeaderFooter(self,canvas,doc,opPeriod="",teams=False):
		formNameText="Radio Log"
		if teams:
			if isinstance(teams,str):
				formNameText="Team: "+teams
			else:
				formNameText="Team Radio Logs"
		canvas.saveState()
		styles = getSampleStyleSheet()
		self.img=None
		if os.path.isfile(self.printLogoFileName):
			rprint("valid logo file "+self.printLogoFileName)
			imgReader=utils.ImageReader(self.printLogoFileName)
			imgW,imgH=imgReader.getSize()
			imgAspect=imgH/float(imgW)
			self.img=Image(self.printLogoFileName,width=0.54*inch/float(imgAspect),height=0.54*inch)
			headerTable=[
					[self.img,self.agencyNameForPrint,"Incident: "+self.incidentName,formNameText+" - Page "+str(canvas.getPageNumber())],
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
					[self.img,self.agencyNameForPrint,"Incident: "+self.incidentName,formNameText+" - Page "+str(canvas.getPageNumber())],
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
# 		self.logMsgBox.setInformativeText("Generating page "+str(canvas.getPageNumber()))
		QCoreApplication.processEvents()
		rprint("Page number:"+str(canvas.getPageNumber()))
		rprint("Height:"+str(h))
		rprint("Pagesize:"+str(doc.pagesize))
		t.drawOn(canvas,doc.leftMargin,doc.pagesize[1]-h-0.5*inch) # enforce a 0.5 inch top margin regardless of paper size
##		canvas.grid([x*inch for x in [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11]],[y*inch for y in [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5]])
		rprint("done drawing printLogHeaderFooter canvas")
		canvas.restoreState()
		rprint("end of printLogHeaderFooter")

	# optonal argument 'teams': if True, generate one pdf of all individual team logs;
	#  so, this function should be called once to generate the overall log pdf, and
	#  again with teams=True to generate team logs pdf
	# if 'teams' is an array of team names, just print those team log(s)
	def printLog(self,opPeriod,teams=False):
		opPeriod=int(opPeriod)
		pdfName=self.firstWorkingDir+"\\"+self.pdfFileName
		teamFilterList=[""] # by default, print print all entries; if teams=True, add a filter for each team
		msgAdder=""
		if teams:
			if isinstance(teams,list):
				# recursively call this function for each team in list of teams
				for team in teams:
					self.printLog(opPeriod,team)
			elif isinstance(teams,str):
				pdfName=pdfName.replace('.pdf','_'+teams.replace(' ','_').replace('.','_')+'.pdf')
				msgAdder=" for "+teams
				teamFilterList=[teams]
			else:
				pdfName=pdfName.replace('.pdf','_teams.pdf')
				msgAdder=" for individual teams"
				teamFilterList=[]
				for team in self.allTeamsList:
					if team!="dummy":
						teamFilterList.append(team)
		rprint("teamFilterList="+str(teamFilterList))
		pdfName=pdfName.replace('.pdf','_OP'+str(opPeriod)+'.pdf')
		rprint("generating radio log pdf: "+pdfName)
		try:
			f=open(pdfName,"wb")
		except:
			self.printLogErrMsgBox=QMessageBox(QMessageBox.Critical,"Error","PDF could not be generated:\n\n"+pdfName+"\n\nMaybe the file is currently being viewed by another program?  If so, please close that viewer and try again.  As a last resort, the auto-saved CSV file can be printed from Excel or as a plain text file.",
				QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			self.printLogErrMsgBox.show()
			self.printLogErrMsgBox.raise_()
			self.printLogErrMsgBox.exec_()
			return
		else:
			f.close()
# 		self.logMsgBox=QMessageBox(QMessageBox.Information,"Printing","Generating PDF"+msgAdder+"; will send to default printer automatically; please wait...",
# 							QMessageBox.Abort,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
# 		self.logMsgBox.setInformativeText("Initializing...")
		# note the topMargin is based on what looks good; you would think that a 0.6 table plus a 0.5 hard
		# margin (see t.drawOn above) would require a 1.1 margin here, but, not so.
		doc = SimpleDocTemplate(pdfName, pagesize=landscape(letter),leftMargin=0.5*inch,rightMargin=0.5*inch,topMargin=1.03*inch,bottomMargin=0.5*inch) # or pagesize=letter
# 		self.logMsgBox.show()
# 		QTimer.singleShot(5000,self.logMsgBox.close)
		QCoreApplication.processEvents()
		elements=[]
		for team in teamFilterList:
			extTeamNameLower=getExtTeamName(team).lower()
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
				# #523: handled continued incidents
				if row[3].startswith('Radio Log Begins - Continued incident'):
					opStartRow=True
					entryOpPeriod=int(row[3].split(': Operational Period ')[1].split()[0])
##				rprint("desired op period="+str(opPeriod)+"; this entry op period="+str(entryOpPeriod))
				if entryOpPeriod == opPeriod:
					if team=="" or extTeamNameLower==getExtTeamName(row[2]).lower() or opStartRow: # filter by team name if argument was specified
						radioLogPrint.append([row[0],row[1],row[2],Paragraph(row[3],styles['Normal']),Paragraph(row[4],styles['Normal']),Paragraph(row[5],styles['Normal'])])
##						hits=True
			if not teams:
				# #523: avoid exception	
				try:
					radioLogPrint[1][4]=self.datum
				except:
					rprint('Nothing to print for specified operational period '+str(opPeriod))
					return
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
# 		self.logMsgBox.setInformativeText("Finalizing and Printing...")
		win32api.ShellExecute(0,"print",pdfName,'/d:"%s"' % win32print.GetDefaultPrinter(),".",0)
		self.radioLogNeedsPrint=False

		if self.use2WD and self.secondWorkingDir and os.path.isdir(self.secondWorkingDir):
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
					[self.img,self.agencyNameForPrint,"Incident: "+self.incidentName,"Clue Log - Page "+str(canvas.getPageNumber())],
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
					[self.img,self.agencyNameForPrint,"Incident: "+self.incidentName,"Clue Log - Page "+str(canvas.getPageNumber())],
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
# 		self.clueLogMsgBox.setInformativeText("Generating page "+str(canvas.getPageNumber()))
		QCoreApplication.processEvents()
		rprint("Page number:"+str(canvas.getPageNumber()))
		rprint("Height:"+str(h))
		rprint("Pagesize:"+str(doc.pagesize))
		t.drawOn(canvas,doc.leftMargin,doc.pagesize[1]-h-0.5*inch) # enforce a 0.5 inch top margin regardless of paper size
		rprint("done drawing printClueLogHeaderFooter canvas")
##		canvas.grid([x*inch for x in [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11]],[y*inch for y in [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5]])
		canvas.restoreState()
		rprint("end of printClueLogHeaderFooter")

	def printClueLog(self,opPeriod):
##      header_labels=['#','DESCRIPTION','TEAM','TIME','DATE','O.P.','LOCATION','INSTRUCTIONS','RADIO LOC.']
		opPeriod=int(opPeriod)
		clueLogPdfFileName=self.firstWorkingDir+"\\"+self.pdfFileName.replace(".pdf","_clueLog_OP"+str(opPeriod)+".pdf")
		rprint("generating clue log pdf: "+clueLogPdfFileName)
		try:
			f=open(clueLogPdfFileName,"wb")
		except:
			self.printClueLogErrMsgBox=QMessageBox(QMessageBox.Critical,"Error","PDF could not be generated:\n\n"+clueLogPdfFileName+"\n\nMaybe the file is currently being viewed by another program?  If so, please close that viewer and try again.  As a last resort, the auto-saved CSV file can be printed from Excel or as a plain text file.",
				QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			self.printClueLogErrMsgBox.show()
			self.printClueLogErrMsgBox.raise_()
			QTimer.singleShot(10000,self.printClueLogErrMsgBox.close)
			self.printClueLogErrMsgBox.exec_()
			return
		else:
			f.close()
# 		self.clueLogMsgBox=QMessageBox(QMessageBox.Information,"Printing","Generating PDF; will send to default printer automatically; please wait...",
# 							QMessageBox.Abort,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
# 		self.clueLogMsgBox.setInformativeText("Initializing...")
		# note the topMargin is based on what looks good; you would think that a 0.6 table plus a 0.5 hard
		# margin (see t.drawOn above) would require a 1.1 margin here, but, not so.
		doc = SimpleDocTemplate(clueLogPdfFileName, pagesize=landscape(letter),leftMargin=0.5*inch,rightMargin=0.5*inch,topMargin=1.03*inch,bottomMargin=0.5*inch) # or pagesize=letter
# 		self.clueLogMsgBox.show()
# 		QTimer.singleShot(5000,self.clueLogMsgBox.close)
		QCoreApplication.processEvents()
		elements=[]
		styles = getSampleStyleSheet()
		clueLogPrint=[]
		clueLogPrint.append(clueTableModel.header_labels[0:5]+clueTableModel.header_labels[6:8]) # omit operational period
		for row in self.clueLog:
			rprint("clue: opPeriod="+str(opPeriod)+"; row="+str(row))
			if (str(row[5])==str(opPeriod) or row[1].startswith("Operational Period "+str(opPeriod)+" Begins:") or (opPeriod==1 and row[1].startswith("Radio Log Begins:"))):
				clueLogPrint.append([row[0],Paragraph(row[1],styles['Normal']),row[2],row[3],row[4],Paragraph(row[6],styles['Normal']),Paragraph(row[7],styles['Normal'])])
		# #523: avoid exception	
		try:
			clueLogPrint[1][5]=self.datum
		except:
			rprint('Nothing to print for specified operational period '+str(opPeriod))
			return
		if len(clueLogPrint)>2:
##			t=Table(clueLogPrint,repeatRows=1,colWidths=[x*inch for x in [0.6,3.75,.9,0.5,1.25,3]])
			t=Table(clueLogPrint,repeatRows=1,colWidths=[x*inch for x in [0.3,3.75,0.9,0.5,0.8,1.25,2.5]])
			t.setStyle(TableStyle([('F/generating clue llONT',(0,0),(-1,-1),'Helvetica'),
				                    ('FONT',(0,0),(-1,1),'Helvetica-Bold'),
				                    ('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
			                       ('BOX', (0,0), (-1,-1), 2, colors.black),
			                       ('BOX', (0,0), (6,0), 2, colors.black)]))
			elements.append(t)
			doc.build(elements,onFirstPage=functools.partial(self.printClueLogHeaderFooter,opPeriod=opPeriod),onLaterPages=functools.partial(self.printClueLogHeaderFooter,opPeriod=opPeriod))
# 			self.clueLogMsgBox.setInformativeText("Finalizing and Printing...")
			win32api.ShellExecute(0,"print",clueLogPdfFileName,'/d:"%s"' % win32print.GetDefaultPrinter(),".",0)
			if self.use2WD and self.secondWorkingDir and os.path.isdir(self.secondWorkingDir):
				rprint("copying clue log pdf to "+self.secondWorkingDir)
				shutil.copy(clueLogPdfFileName,self.secondWorkingDir)
# 		else:
# 			self.clueLogMsgBox.setText("No clues were logged during Operational Period "+str(opPeriod)+"; no clue log will be printed.")
# 			self.clueLogMsgBox.setInformativeText("")
# 			self.clueLogMsgBox.setStandardButtons(QMessageBox.Ok)
# 			self.msgBox.close()
# 			self.msgBox=QMessageBox(QMessageBox.Information,"Printing","No clues were logged during Operational Period "+str(opPeriod)+"; no clue log will be printed.",QMessageBox.Ok)
# 			QTimer.singleShot(500,self.msgBox.show)
		self.clueLogNeedsPrint=False

	# fillable pdf works well with pdftk external dependency, but is problematic in pure python
	#  see https://stackoverflow.com/questions/72625568
	# so, use reportlab instead
	def printClueReport(self,clueData):
		cluePdfName=self.firstWorkingDir+"\\"+self.pdfFileName.replace(".pdf","_clue"+str(clueData[0]).zfill(2)+".pdf")
		rprint("generating clue report pdf: "+cluePdfName)
		
		try:
			f=open(cluePdfName,"wb")
		except:
			self.printClueErrMsgBox=QMessageBox(QMessageBox.Critical,"Error","PDF could not be generated:\n\n"+cluePdfName+"\n\nMaybe the file is currently being viewed by another program?  If so, please close that viewer and try again.",
				QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			self.printClueErrMsgBox.show()
			self.printClueErrMsgBox.raise_()
			QTimer.singleShot(10000,self.printClueErrMsgBox.close)
			self.printClueErrMsgBox.exec_()
			return
		else:
			f.close()

		cluePdfOverlayName=cluePdfName.replace('.pdf','_overlay.pdf')
		doc = SimpleDocTemplate(cluePdfOverlayName, pagesize=portrait(letter),leftMargin=0.84*inch,rightMargin=0.67*inch,topMargin=0.68*inch,bottomMargin=0.5*inch) # or pagesize=letter
		QCoreApplication.processEvents()
		tableWidthInches=6.92 # determined from the template pdf, used to draw overlay pdf fields below
		elements=[]
		styles = getSampleStyleSheet()

		img=''
		if os.path.isfile(self.printLogoFileName):
			imgReader=utils.ImageReader(self.printLogoFileName)
			imgW,imgH=imgReader.getSize()
			imgAspect=imgH/float(imgW)
			img=Image(self.printLogoFileName,width=0.54*inch/float(imgAspect),height=0.54*inch)

		instructions=clueData[7].lower()
		# initialize all checkboxes to OFF
		instructionsCollect=''
		instructionsMarkAndLeave=''
		instructionsDisregard=''
		instructionsOther=''
		# look for keywords in the instructions text
		if "collect" in instructions:
			instructionsCollect='X'
		if "mark & leave" in instructions:
			instructionsMarkAndLeave='X'
		if "disregard" in instructions:
			instructionsDisregard='X'
		# now see if there are any instructions other than the standard ones above; if so, print them in 'other'
		instructions=re.sub(r'collect','',instructions)
		instructions=re.sub(r'mark & leave','',instructions)
		instructions=re.sub(r'disregard','',instructions)
		instructions=re.sub(r'^[; ]+','',instructions) # only get rid of semicolons and spaces before the first word
		instructions=re.sub(r' ; ','',instructions) # also get rid of remaining ' ; ' i.e. when first word is not a keyword
		instructions=re.sub(r'; *$','',instructions) # also get rid of trailing ';' i.e. when last word is a keyword
		if instructions != "":
			instructionsOther='X'
		instructionsOtherText=re.sub(';+',';',instructions) # reduce multi-semicolon chains from above
# 		locText=clueData[6]
		if clueData[8]!="":
# 			locText=locText+"\n(Radio GPS = "+clueData[8]+")"
			radioLocText="(Radio GPS: "+re.sub(r"\n","  x  ",clueData[8])+")"
		else:
			radioLocText=""

		# define the fields and locations of the overlay pdf; similar to fillable pdf but with more control
		# clueTableDicts - list of dictionaries, with each dictionary corresponding to a new reportlab table
		#  data - list of lists, each sublist corresponding to one row of the reportlab table
		#  heights - list of row heights (in inches) - the length of this list must equal the length of 'data';
		#    can also be a single number, in which case each row will have the same specified height
		#  widths - list of column widths - the length of theis list must equal the length of each element of 'data'
		#    if sum of values adds up to page width in inches, then units are assumed to be in inches;
		#    otherwise, units are assumed to be equal parts of total page width
		clueTableDicts=[
			{ # title bar row
				'data':[[img,self.agencyNameForPrint,img]],
				'heights':0.68,
				'widths':[1,3,1],
				'hvalign':['center','middle'],
				'fontName':'Helvetica-Bold',
				'fontSize':18
			},
			{ # incident name / date / operational period
				'data':[['',self.incidentName,time.strftime('%x'),str(clueData[5])]],
				'heights':0.43,
				'widths':[67,108,85,79], # measured mm on screen (not sure of zoom)
				'hvalign':['center','bottom']
			},
			{ # clue number / date/time located / team that located the clue
				'data':[[str(clueData[0]),clueData[4]+'   '+clueData[3],clueData[2]]],
				'heights':0.39,
				'widths':[67,141,131],
				'hvalign':['center','bottom']
			},
			{ # gap - Name of Individual That Located Clue, plus gap before description text
				'data':[['']],
				'heights':0.54,
				'widths':[1]
			},
			{ # description of clue
				'data':[['',clueData[1]]],
				'heights':0.87,
				'widths':[1,40], # left indent
				'hvalign':['left','top']
			},
			{ # radio location
				'data':[['',radioLocText]],
				'heights':0.22,
				'widths':[1,4],
				'hvalign':['left','middle']
			},
			{ # location description
				'data':[['',clueData[6]]],
				'heights':0.63,
				'widths':[1,40], # left indent
				'hvalign':['left','top']
			},
			{ # gap - 'To investigations' and gap before checkboxes
				'data':[['']],
				'heights':1,
				'widths':[1]
			},
			{ # Instructions checkboxes - to keep it to a single table, each row is [gap,checkbox,gap,othertext]
				'data':[
					['',instructionsCollect,'',''],
					['',instructionsMarkAndLeave,'',''],
					['',instructionsDisregard,'',''],
					['',instructionsOther,'',instructionsOtherText]
				],
				'heights':0.19,
				'widths':[1.35,1,3,30]
				# note: if a cell width is less than required for a single character (plus padding),
				#  the pdf generation process will throw an exception:
				# AttributeError: 'Paragraph' object has no attribute 'blPara'
				#  should probably catch this at the call to doc.build, by making the narrowest
				#  field wider and trying again.  For helvetica-bold 18pt, a width of 0.15 is too
				#  narrow and causes the error (1 part in 46) but 0.19 is OK (1 part in 36).
			}
		]
		def ParagraphOrNot(d,style):
			if isinstance(d,(str,int,float)):
				# rprint('   paragraph')
				return Paragraph(d,style)
			else:
				# rprint('   NOT paragraph')
				return d

		for td in clueTableDicts:
			# rprint('--- new table ---')
			# rprint('-- raw table data --')
			# try:
			# 	rprint(json.dumps(td,indent=3))
			# except:
				# rprint(str(td))

			# using Normal paragraph style enables word wrap within table cells https://stackoverflow.com/a/10244769/3577105
			style=ParagraphStyle('theStyle',parent=styles['Normal'])
			# style.backColor='#dddddd' # helpful for layout development and debug
			# style.borderPadding=(5,0,5,0)
			if 'fontName' in td.keys():
				style.fontName=td['fontName']
			if 'fontSize' in td.keys():
				style.fontSize=td['fontSize']
			else:
				style.fontSize=12
			style.leading=style.fontSize*1.15 # rule of thumb: 20% larger than font size

			# vertical alignment must be specified in the Table style;
			# horizontal alignment must be specified in the Paragraph style
			if 'hvalign' in td.keys():
				[h,v]=td['hvalign']
				if h=='center':
					style.alignment=1

			data=[[ParagraphOrNot(d,style) for d in row] for row in td['data']]
			# data=td['data']
			# rprint('data:'+str(data))
			widths=td['widths']
			wsum=sum(td['widths'])
			# if width units are not inches, treat them as proportional units
			if sum(td['widths'])!=tableWidthInches:
				widths=[(w/wsum)*tableWidthInches for w in widths]
			# rprint('widths='+str(widths))
			heights=td['heights']
			if isinstance(heights,(int,float)):
				heightsList=[heights for x in range(len(data))]
				heights=heightsList
			# rprint('heights='+str(heights))
			t=Table(data,colWidths=[x*inch for x in widths],rowHeights=[x*inch for x in heights])
			styleList=[
				# ('BOX',(0,0),(-1,-1),1,colors.red), # helpful for layout development and debug
				# ('INNERGRID',(0,0),(-1,-1),0.5,colors.red) # helpful for layout development and debug
			]
			# vertical alignment must be specified in the Table style;
			# horizontal alignment within paragraphs must be specified in the Paragraph style
			#  but should be applied in the Table style also, in case the data is not a Paragraph
			if 'hvalign' in td.keys():
				[h,v]=td['hvalign']
				if isinstance(v,str): # apply it to the entire table
					styleList.append(('VALIGN',(0,0),(-1,-1),v.upper()))
				if isinstance(h,str): # apply it to the entire table
					styleList.append(('ALIGN',(0,0),(-1,-1),h.upper()))
			t.setStyle(TableStyle(styleList))
			# rprint('setting table style:'+str(styleList))
			elements.append(t)
		doc.build(elements)

		# overlaying on the template https://gist.github.com/vsajip/8166dc0935ee7807c5bd4daa22a20937
		templatePDF=PdfFileReader(self.clueReportPdfFileName,'rb')
		templatePage=templatePDF.getPage(0)
		overlayPDF=PdfFileReader(cluePdfOverlayName,'rb')
		templatePage.mergePage(overlayPDF.getPage(0))
		outputPDF=PdfFileWriter()
		outputPDF.addPage(templatePage)
		with open(cluePdfName,'wb') as out_pdf:
			outputPDF.write(out_pdf)

		win32api.ShellExecute(0,"print",cluePdfName,'/d:"%s"' % win32print.GetDefaultPrinter(),".",0)
		if self.use2WD and self.secondWorkingDir and os.path.isdir(self.secondWorkingDir):
			rprint("copying clue report pdf to "+self.secondWorkingDir)
			shutil.copy(cluePdfName,self.secondWorkingDir)

		try:
			os.remove(cluePdfOverlayName)
		except:
			pass

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
		# rprint("1 - begin fontsChanged")
		self.limitedFontSize=self.fontSize
		if self.limitedFontSize>self.maxLimitedFontSize:
			self.limitedFontSize=self.maxLimitedFontSize
		if self.limitedFontSize<self.minLimitedFontSize:
			self.limitedFontSize=self.minLimitedFontSize
		# preserve the currently selected tab, since something in this function
		#  causes the rightmost tab to be selected
		i=self.ui.tabWidget.currentIndex()
		self.ui.tableView.setStyleSheet("font-size:"+str(self.fontSize)+"pt")
		for n in self.ui.tableViewList[1:]:
			# rprint("n="+str(n))
			n.setStyleSheet("font-size:"+str(self.fontSize)+"pt")
		# don't change tab font size unless you find a good way to dynamically
		# change tab size and margins as well
##		self.ui.tabWidget.tabBar().setStyleSheet("font-size:"+str(self.fontSize)+"pt")
		# rprint("2")
		self.redrawTables()
		self.ui.tabWidget.setCurrentIndex(i)
		self.ui.incidentNameLabel.setStyleSheet("font-size:"+str(self.limitedFontSize)+"pt;")

		# NOTE that setStyleSheet is DESTRUCTIVE, not INCREMENTAL.  To set a new style
		#  without affecting previous style settings for the same identifier, you
		#  need to use getStyleSheet()+"....".  To avoid confusion, do as many settings
		#  as possible in one text block as below.
		
		# hardcode dialog button box pushbutton font size to 14pt since QTDesiger-generated code doesn't work
		self.parent.setStyleSheet("""
			QMessageBox,QDialogButtonBox QPushButton {
				font-size:14pt;
			}
			QToolTip {
				font-size:"""+str(self.fontSize*2/3)+"""pt;
				color:#555;
			}
			QMenu {
				font-size:"""+str(self.limitedFontSize*3/4)+"""pt;
			}
		""")
		# rprint("3 - end of fontsChanged")

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
		# rprint("1: start of redrawTables")
		for i in [2,4]: # hardcode results in significant speedup
			self.ui.tableView.resizeColumnToContents(i) # zero is the first column
		# rprint("2")
		self.ui.tableView.setColumnWidth(0,self.fontSize*5) # wide enough for '2345'
		self.ui.tableView.setColumnWidth(1,self.fontSize*6) # wide enough for 'FROM'
		self.ui.tableView.setColumnWidth(5,self.fontSize*10) # wide enough for 'STATUS'
		# rprint("3")
##		self.ui.tableView.resizeRowsToContents()
		# rprint("4")
		for n in self.ui.tableViewList[1:]:
			# rprint(" n="+str(n))
			for i in [2,4]: # hardcode results in significant speedup, but lag still scales with filtered table length
				# rprint("    i="+str(i))
				n.resizeColumnToContents(i)
			# rprint("    done with i")
			n.setColumnWidth(0,self.fontSize*5)
			n.setColumnWidth(1,self.fontSize*6)
			n.setColumnWidth(5,self.fontSize*10)
			# rprint("    resizing rows to contents")
##			n.resizeRowsToContents()
		# rprint("5")
		self.ui.tableView.scrollToBottom()
		# rprint("6")
		for i in range(1,self.ui.tabWidget.count()):
			self.ui.tabWidget.setCurrentIndex(i)
			self.ui.tableViewList[i].scrollToBottom()
		# rprint("7: end of redrawTables")
##		self.resizeRowsToContentsIfNeeded()
		self.loadFlag=False

	def updateClock(self):
		self.ui.clock.display(time.strftime("%H:%M"))

	def updateTeamTimers(self):
		# rprint('timers:'+str(teamTimersDict))
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
			self.helpWindow.ui.fsSomeFilteredLabel.setFont(self.helpFont2)
		else:
			self.blinkToggle=0
			# now make sure the help window color code bars blink too
			self.helpWindow.ui.colorLabel4.setStyleSheet(statusStyleDict["Waiting for Transport"])
			self.helpWindow.ui.colorLabel5.setStyleSheet(statusStyleDict[""])
			self.helpWindow.ui.colorLabel6.setStyleSheet(statusStyleDict[""])
			self.helpWindow.ui.colorLabel7.setStyleSheet(statusStyleDict["STANDBY"])
			self.helpWindow.ui.fsSomeFilteredLabel.setFont(self.helpFont1)

		for extTeamName in teamTimersDict:
			# if there is a newEntryWidget currently open for this team, don't blink,
			#  but don't reset the timer.  Only reset the timer when the dialog is accepted.
			hold=False
			for widget in newEntryWidget.instances:
				if widget.ui.to_fromField.currentText()=="FROM" and getExtTeamName(widget.ui.teamField.text())==extTeamName:
					hold=True
			i=self.extTeamNameList.index(extTeamName)
			status=teamStatusDict.get(extTeamName,"")
			fsFilter=teamFSFilterDict.get(extTeamName,0)
##			rprint("blinking "+extTeamName+": status="+status)
# 			rprint("fsFilter "+extTeamName+": "+str(fsFilter))
			secondsSinceContact=teamTimersDict.get(extTeamName,0)
			if status in ["Waiting for Transport","STANDBY","Available"] or (secondsSinceContact>=self.timeoutOrangeSec):
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
					if not hold and status not in ["At IC","Off Duty"] and secondsSinceContact>=self.timeoutRedSec:
						self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).setStyleSheet(statusStyleDict["TIMED_OUT_RED"])
					elif not hold and status not in ["At IC","Off Duty"] and (secondsSinceContact>=self.timeoutOrangeSec and secondsSinceContact<self.timeoutRedSec):
						self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).setStyleSheet(statusStyleDict["TIMED_OUT_ORANGE"])
					elif status=="Waiting for Transport" or status=="STANDBY" or status=="Available":
						self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).setStyleSheet(statusStyleDict[""])
			else:
				# not Waiting for Transport or Available, and not in orange/red time zone: draw the normal style
				self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).setStyleSheet(statusStyleDict[status])
				
			# always check for fleetsync filtering, independent from team status
			if self.blinkToggle==0:
				if fsFilter>0:
					f=self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).font()
					f.setStrikeOut(True)
					self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).setFont(f)
			if self.blinkToggle==1:
				if fsFilter<2: # strikeout all the time if all devices for this callsign are filtered
					f=self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).font()
					f.setStrikeOut(False)
					self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).setFont(f)
				else:
					f=self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).font()
					f.setStrikeOut(True)
					self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).setFont(f)
					
			# once they have timed out, keep incrementing; but if the timer is '-1', they will never timeout
			if secondsSinceContact>-1:
				teamTimersDict[extTeamName]=secondsSinceContact+1

	def keyPressEvent(self,event):
		if type(event)==QKeyEvent:
		# fix #336 (freeze / loss of focus when MyWindow grabs the keyPressEvent
		#  that was intended for newEntryWidget but happened before newEntryWidget
		#  was able to respond to it)
		# use the following fix for now: if the newEntryWindow is visible,
		#  ignore the envent completely; it would be nice to queue it until the
		#  newEntryWidget can respond to it; but, what should the receiver of the
		#  queued event be, and, how should the timing of the queued event interact
		#  with other events and processes?
		#  See https://stackoverflow.com/questions/44148992; need to develop a full
		#  test case to proceed with that question
			if self.newEntryWindow.isVisible():
				rprint("** keyPressEvent ambiguous timing; key press ignored: key="+str(hex(event.key())))
				event.ignore()
			else:
				key=event.text().lower() # hotkeys are case insensitive
				mod=event.modifiers()
# 				rprint("  key:"+QKeySequence(event.key()).toString()+"  mod:"+str(mod))
				if self.ui.teamHotkeysWidget.isVisible():
					# these key handlers apply only if hotkeys are enabled:
					if key in self.hotkeyDict.keys():
						self.openNewEntry(key)
				else:
					# these key handlers apply only if hotkeys are disabled:
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
				# these key handlers apply regardless of hotkeys enabled state:
				if key=='=' or key=='+':
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
					self.ui.teamHotkeysWidget.setVisible(not self.ui.teamHotkeysWidget.isVisible())
				elif event.key()==Qt.Key_F6:
					q=QMessageBox(QMessageBox.Question,"Please Confirm","Restore the last saved files (Radio Log, Clue Log, and FleetSync table)?",
							QMessageBox.Yes|QMessageBox.No,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
					q.setDefaultButton(QMessageBox.No)
					q.show()
					q.raise_()
					if q.exec_()==QMessageBox.Yes:
						self.restore()
				elif event.key()==Qt.Key_F7:
					self.ui.fsCheckBox.toggle()
				elif event.key()==Qt.Key_F8:
					self.fsFilterDialog.show()
				elif event.key()==Qt.Key_F12:
					self.toggleTeamHotkeys()
				elif event.key()==Qt.Key_Enter or event.key()==Qt.Key_Return:
					self.openNewEntry('pop')
				event.accept()
		else:
			event.ignore()

	def closeEvent(self,event):
		self.exitClicked=True
		
		# if radioLogNeedsPrint or clueLogNeedsPrint is True, bring up the print dialog
		if self.radioLogNeedsPrint or self.clueLogNeedsPrint:
			rprint("needs print!")
			self.printDialog.exec_()
		else:
			rprint("no print needed")
		# note, this type of messagebox is needed to show above all other dialogs for this application,
		#  even the ones that have WindowStaysOnTopHint.  This works in Vista 32 home basic.
		#  if it didn't show up on top, then, there would be no way to close the radiolog other than kill.
		really=QMessageBox(QMessageBox.Warning,"Please Confirm","Exit the Radio Log program?",
			QMessageBox.Yes|QMessageBox.No,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
		really.setDefaultButton(QMessageBox.No)
		really.show()
		really.raise_()
		if really.exec_()==QMessageBox.No:
			event.ignore()
			self.exitClicked=False
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
		
		if self.initialWindowTracking:
			rprint("restoring initial window tracking behavior ("+str(self.initialWindowTracking)+")")
			win32gui.SystemParametersInfo(win32con.SPI_SETACTIVEWINDOWTRACKING,self.initialWindowTracking)

		qApp.quit() # needed to make sure all windows area closed

	def saveRcFile(self,cleanShutdownFlag=False):
		(x,y,w,h)=self.geometry().getRect()
		(cx,cy,cw,ch)=self.clueLogDialog.geometry().getRect()
		timeout=timeoutDisplayList[self.optionsDialog.ui.timeoutField.value()][0]
		rcFile=QFile(self.rcFileName)
		if not rcFile.open(QFile.WriteOnly|QFile.Text):
			warn=QMessageBox(QMessageBox.Warning,"Error","Cannot write resource file " + self.rcFileName + "; proceeding, but, current settings will be lost. "+rcFile.errorString(),
							QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			warn.show()
			warn.raise_()
			warn.exec_()
			return
		out=QTextStream(rcFile)
		out << "[RadioLog]\n"
		# datum, coord format, and timeout are saved in the config file
		#  but also need to be able to auto-recover from .rc file
		# issue 322: use self.lastSavedFileName instead of self.csvFileName to
		#  make sure the initial rc file doesn't point to a file that does not yet exist
		out << "lastFileName=" << os.path.join(self.sessionDir,self.lastSavedFileName) << "\n"
		out << "font-size=" << self.fontSize << "pt\n"
		out << "x=" << x << "\n"
		out << "y=" << y << "\n"
		out << "w=" << w << "\n"
		out << "h=" << h << "\n"
		out << "clueLog_x=" << cx << "\n"
		out << "clueLog_y=" << cy << "\n"
		out << "clueLog_w=" << cw << "\n"
		out << "clueLog_h=" << ch << "\n"
		out << "timeout="<< timeout << "\n"
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
		rcFile=QFile(self.rcFileName)
		if not rcFile.open(QFile.ReadOnly|QFile.Text):
			if not self.newWorkingDir: # don't show the warning, but still return, if this is the first run in a new working dir
				warn=QMessageBox(QMessageBox.Warning,"Error","Cannot read resource file " + self.rcFileName + "; using default settings. "+rcFile.errorString(),
							QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
				warn.show()
				warn.raise_()
				warn.exec_()
			return
		inStr=QTextStream(rcFile)
		line=inStr.readLine()
		if line!="[RadioLog]":
			warn=QMessageBox(QMessageBox.Warning,"Error","Specified resource file " + self.rcFileName + " is not a valid resource file; using default settings.",
							QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			warn.show()
			warn.raise_()
			warn.exec_()
			rcFile.close()
			return
		cleanShutdownFlag=False
		self.lastFileName="NONE"
		timeoutDisplay='30 min'
		datum=None
		coordFormat=None
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
			elif tokens[0]=="timeout":
				timeoutDisplay=tokens[1]
			elif tokens[0]=="datum":
				datum=tokens[1]
			elif tokens[0]=="coordFormat":
				coordFormat=tokens[1]
			elif tokens[0]=="cleanShutdown" and tokens[1]=="True":
				cleanShutdownFlag=True
		# only apply datum, coordFormat, and timout if it's an auto-recover
		if not cleanShutdownFlag:
			if datum:
				self.datum=datum
			if coordFormat:
				self.coordFormat=coordFormat
			for n in range(len(timeoutDisplayList)):
				pair=timeoutDisplayList[n]
				if pair[0]==timeoutDisplay:
					self.timeoutRedSec=pair[1]
					break
		self.updateOptionsDialog()
		rcFile.close()
		return cleanShutdownFlag

	def save(self,finalize=False):
		csvFileNameList=[os.path.join(self.sessionDir,self.csvFileName)]
		if self.use2WD and self.secondWorkingDir and os.path.isdir(self.secondWorkingDir):
			csvFileNameList.append(os.path.join(self.secondWorkingDir,self.csvFileName)) # save flat in second working dir
		for fileName in csvFileNameList:
			rprint("  writing "+fileName)
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
				if self.lastSavedFileName!=self.csvFileName: # this is the first save since startup, since restore, or since incident name change
					self.lastSavedFileName=self.csvFileName
					self.saveRcFile()
			rprint("  done writing "+fileName)
		# now write the clue log to a separate csv file: same filename appended by '.clueLog'
		if len(self.clueLog)>0:
			for fileName in csvFileNameList:
				fileName=fileName.replace(".csv","_clueLog.csv")
				rprint("  writing "+fileName)
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
				rprint("  done writing "+fileName)

	def load(self,fileName=None):
		# loading scheme:
		# always merge instead of overwrite; always use the loaded Begins line since it will be earlier by definition
		# maybe provide some way to force overwrite later, but, for now that can be done just by exiting and restarting
# 		if not fileName:
# 			fileDialog=QFileDialog()
# 			fileDialog.setOption(QFileDialog.DontUseNativeDialog)
# 			fileDialog.setProxyModel(CSVFileSortFilterProxyModel(self))
# 			fileDialog.setNameFilter("CSV Radio Log Data Files (*.csv)")
# 			fileDialog.setDirectory(self.firstWorkingDir)
# 			if fileDialog.exec_():
# 				fileName=fileDialog.selectedFiles()[0]
# 			else: # user pressed cancel on the file browser dialog
# 				return
# # 			print("fileName="+fileName)
# # 			if not os.path.isfile(fileName): # prevent error if dialog is canceled
# # 				return
# 		if "_clueLog" in fileName or "_fleetsync" in fileName:
# 			crit=QMessageBox(QMessageBox.Critical,"Invalid File Selected","Do not load a Clue Log or FleetSync file directly.  Load the parent radiolog.csv file directly, and the Clue Log and FleetSync files will automatically be loaded with it.",
# 							QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
# 			crit.show()
# 			crit.raise_()
# 			crit.exec_() # make sure it's modal
# 			return


		if not fileName:
			sessions=self.getSessions(reverse=True)
			if not sessions:
				rprint('There are no available sessions to load.')
				return
			ld=loadDialog(self)
			ld.ui.theTable.setRowCount(len(sessions))
			row=0
			for [incidentName,lastOP,lastClue,ageStr,filenameBase,mtime] in sessions:
				q0=QTableWidgetItem(incidentName)
				q1=QTableWidgetItem(lastOP)
				q2=QTableWidgetItem(lastClue)
				q3=QTableWidgetItem(time.strftime("%m/%d/%Y %H:%M:%S",time.localtime(mtime)))
				q0.setToolTip(filenameBase)
				q1.setToolTip(filenameBase)
				q2.setToolTip(filenameBase)
				q3.setToolTip(filenameBase)
				ld.ui.theTable.setItem(row,0,q0)
				ld.ui.theTable.setItem(row,1,q1)
				ld.ui.theTable.setItem(row,2,q2)
				ld.ui.theTable.setItem(row,3,q3)
				row+=1
			ld.show()
			ld.raise_()
			rval=ld.exec_()

		else: # entry point when session is selected from load dialog
			rprint("Loading: "+fileName)
			progressBox=QProgressDialog("Loading, please wait...","Abort",0,100)
			progressBox.setWindowModality(Qt.WindowModal)
			progressBox.setWindowTitle("Loading")
			progressBox.show()
			QCoreApplication.processEvents()
			self.teamTimer.start(10000) # pause
			# pass 1: count total entries for the progress box, and read incident name
			with open(fileName,'r') as csvFile:
				csvReader=csv.reader(csvFile)
				totalEntries=0
				for row in csvReader:
					if row[0].startswith("## Incident Name:"):
						self.incidentName=row[0][18:]
						self.optionsDialog.ui.incidentField.setText(self.incidentName)
						rprint("loaded incident name: '"+self.incidentName+"'")
						self.incidentNameNormalized=normName(self.incidentName)
						rprint("normalized loaded incident name: '"+self.incidentNameNormalized+"'")
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
						newOp=None
						if row[3].startswith("Operational Period") and row[3].split()[3]=="Begins:":
							newOp=int(row[3].split()[2])
						if row[3].startswith('Radio Log Begins - Continued incident'):
							newOp=int(row[3].split(': Operational Period ')[1].split()[0])
						if newOp:
							self.opPeriod=newOp
							self.printDialog.ui.opPeriodComboBox.addItem(str(self.opPeriod))
							rprint('Setting OP to '+str(self.opPeriod)+' based on loaded entry "'+row[3]+'".')
						progressBox.setValue(i)
				csvFile.close()

			# now add entries, sort, and prune any Begins lines after the first line
			# edit: don't prune Begins lines - those are needed to indicate start of operational periods
			# move loadFlag True then False closer in to the newEntry commands, to
			#  minimize opportunity for failed entries due to self.loadFlag being
			#  left at True, probably due to early return above (see #340)
			self.loadFlag=True
			for row in loadedRadioLog:
				self.newEntry(row)
				i=i+1
				progressBox.setValue(i)
			self.loadFlag=False
			self.radioLog.sort(key=lambda entry: entry[6]) # sort by epoch seconds
##		self.radioLog[1:]=[x for x in self.radioLog[1:] if not x[3].startswith('Radio Log Begins:')]

		# take care of the newEntry cleanup functions that have been put off due to loadFlag

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
							elif '(Last clue number: ' in row[1]:
								lastClueNumber=int(row[1].split('(Last clue number: ')[1].replace(')',''))
					csvFile.close()

			self.clueLogDialog.ui.tableView.model().layoutChanged.emit()
			# finished
			# rprint("Starting redrawTables")
			self.fontsChanged()
	##		self.ui.tableView.model().layoutChanged.emit()
	##		QCoreApplication.processEvents()
			# rprint("Returned from redrawTables")
			progressBox.close()
			self.ui.opPeriodButton.setText("OP "+str(self.opPeriod))
			self.teamTimer.start(1000) #resume
			self.lastSavedFileName="NONE"
			self.updateFileNames() # note, no file will be saved until the next entry is made
			self.saveRcFile()

	def updateFileNames(self):
		# update the filenames based on current incident name and current date/time
		# normalize the name for purposes of filenames
		#  - get rid of all spaces -  no need to be able to reproduce the
		#    incident name's spaces from the filename
		self.incidentNameNormalized=normName(self.incidentName)
		sessionDirAttempt=os.path.join(self.firstWorkingDir,self.incidentNameNormalized)+'_'+time.strftime('%Y_%m_%d_%H%M%S')
		if sessionDirAttempt is not self.sessionDir:
			if not os.path.isdir(sessionDirAttempt):
				setLogHandlers() # open log file handler prevents dir rename; close it now
				try:
					os.rename(self.sessionDir,sessionDirAttempt)
				except Exception as e:
					err='ERROR: session directory could not be renamed from\n\n'+self.sessionDir+'\n\nto\n\n'+sessionDirAttempt+'.\n\nUsing existing session directory.\n\n'+repr(e)
					setLogHandlers(self.sessionDir) # resume log file in new location, regardless of rename outcome
					rprint(err.replace('\n',' '))
					self.errMsgBox=QMessageBox(QMessageBox.Critical,"Session Directory Error",err,
									QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
					self.errMsgBox.exec_()
				else:
					self.sessionDir=sessionDirAttempt
					setLogHandlers(self.sessionDir) # resume log file in new location, regardless of rename outcome
					rprint('Renamed session directory to "'+self.sessionDir+'"')
		self.csvFileName=getFileNameBase(self.incidentNameNormalized)+".csv"
		self.pdfFileName=getFileNameBase(self.incidentNameNormalized)+".pdf"
		self.fsFileName=self.csvFileName.replace('.csv','_fleetsync.csv')

	def optionsAccepted(self):
		tmp=self.optionsDialog.ui.incidentField.text()
		if self.incidentName is not tmp:
			rprint('Incident name changed to "'+tmp+'".') # note that this gets called from code as well as GUI
			self.incidentName=self.optionsDialog.ui.incidentField.text()
			self.updateFileNames()
			# don't change the rc file at this point - wait until a log entry is actually saved
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

	def openNewEntry(self,key=None,callsign=None,formattedLocString=None,fleet=None,dev=None,origLocString=None,amendFlag=False,amendRow=None,isMostRecentForCallsign=False):
		rprint("openNewEntry called:key="+str(key)+" callsign="+str(callsign)+" formattedLocString="+str(formattedLocString)+" fleet="+str(fleet)+" dev="+str(dev)+" origLocString="+str(origLocString)+" amendFlag="+str(amendFlag)+" amendRow="+str(amendRow)+" isMostRecentForCallsign="+str(isMostRecentForCallsign))
		if clueDialog.openDialogCount==0:
			self.newEntryWindow.setWindowFlags(Qt.WindowTitleHint|Qt.WindowStaysOnTopHint) # enable always on top
		else:
			self.newEntryWindow.setWindowFlags(Qt.WindowTitleHint)
		sec=time.time() # epoch seconds, for sorting purposes; not displayed
		self.newEntryWidget=newEntryWidget(self,sec,formattedLocString,fleet,dev,origLocString,amendFlag,amendRow,isMostRecentForCallsign)
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
			if self.ui.teamHotkeysWidget.isVisible() and len(key)==1:
				self.newEntryWidget.ui.to_fromField.setCurrentIndex(0)
				self.newEntryWidget.ui.teamField.setText(self.hotkeyDict[key])
				self.newEntryWidget.ui.messageField.setFocus()
			else:
				if key=='fs': # spawned by fleetsync: let addTab determine focus
					pass
				elif key=='a':
					self.newEntryWidget.ui.to_fromField.setCurrentIndex(1)
					# all three of these lines are needed to override the default 'pseudo-selected'
					# behavior; see http://stackoverflow.com/questions/27856032
					self.newEntryWidget.ui.teamField.setFocus()
					self.newEntryWidget.ui.teamField.setText("All Teams ")
					self.newEntryWidget.ui.messageField.setFocus()
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
					if key=='f':
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
				elif key=='tab': # team tab context menu - activate right away
					self.newEntryWindow.ui.tabWidget.setCurrentIndex(1)
					self.newEntryWidget.ui.to_fromField.setCurrentIndex(0)
					self.newEntryWidget.ui.messageField.setFocus()
				else: # some other keyboard key - assume it's the start of the team name
					self.newEntryWidget.ui.to_fromField.setCurrentIndex(0)
					# need to 'burp' the focus to prevent two blinking cursors
					#  see http://stackoverflow.com/questions/42475602
					self.newEntryWidget.ui.messageField.setFocus()
					self.newEntryWidget.ui.teamField.setFocus()
					self.newEntryWidget.ui.teamField.setText("Team "+key)
					self.newEntryWidget.ui.teamField.setSelection(6,1)
		else: # no key pressed; opened from the 'add entry' GUI button; activate right away
			# need to 'burp' the focus to prevent two blinking cursors
			#  see http://stackoverflow.com/questions/42475602
			self.newEntryWindow.ui.tabWidget.setCurrentIndex(1)
			self.newEntryWidget.ui.messageField.setFocus()
			self.newEntryWidget.ui.teamField.setFocus()

		if callsign:
			extTeamName=getExtTeamName(callsign)
			self.newEntryWidget.ui.teamField.setText(callsign)
			self.newEntryWidget.teamFieldEditingFinished() # check for relay
			if callsign[0:3]=='KW-':
				self.newEntryWidget.ui.teamField.setFocus()
				self.newEntryWidget.ui.teamField.selectAll()
			if callsign[0:6]=="Radio " or callsign[0:3]=="KW-":
				rprint("setting needsChangeCallsign")
				self.newEntryWidget.needsChangeCallsign=True
				# if it's the only item on the stack, open the change callsign
				#   dialog right now, since the normal event loop won't process
				#   needsChangeCallsign until the tab changes
				if self.newEntryWidget==self.newEntryWindow.ui.tabWidget.currentWidget():
					QTimer.singleShot(500,lambda:self.newEntryWidget.openChangeCallsignDialog())
				# note that changeCallsignDialog.accept is responsible for
				#  setting focus back to the messageField of the active message
				#  (not always the same as the new message)

		if formattedLocString:
			datumFormatString="("+self.datum+"  "+self.coordFormat+")"
			if self.newEntryWidget.relayed:
				self.newEntryWidget.radioLocTemp=formattedLocString
				self.newEntryWidget.datumFormatTemp=datumFormatString
			else:
				self.newEntryWidget.ui.radioLocField.setText(formattedLocString)
				self.newEntryWidget.ui.datumFormatLabel.setText(datumFormatString)
		else:
			self.newEntryWidget.ui.datumFormatLabel.setText("")
	
	def newEntry(self,values,amend=False):
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
		extTeamName=getExtTeamName(niceTeamName)
		status=values[5]
		if values[4]==None:
			values[4]=''
		sec=values[6] # epoch seconds of dialog open time, for sorting; not displayed
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
		i=len(self.radioLog)-1 # i = zero-based list index of the last element
		while i>-1 and isinstance(sec,float) and sec<self.radioLog[i][6]:
			i=i-1
# 			rprint("new entry sec="+str(sec)+"; prev entry sec="+str(self.radioLog[i+1][6])+"; decrementing: i="+str(i))
		# at this point, i is the index of the item AFTER which the new entry should be inserted,
		#  so, use i+1 for the actual insertion
		i=i+1
		if not self.loadFlag:
			model=self.ui.tableView.model()
			model.beginInsertRows(QModelIndex(),i,i) # this is one-based
# 		self.radioLog.append(values) # leave a blank entry at the end for aesthetics
		# myList.insert(i,val) means val will become myList[i] using a zero-based index
		#  i.e. val will be the (i+1)th element in the list 
		self.radioLog.insert(i,values)
# 		rprint("inserting entry at index "+str(i))
		if not self.loadFlag:
			model.endInsertRows()
##		if not values[3].startswith("RADIO LOG SOFTWARE:"):
##			self.newEntryProcessTeam(niceTeamName,status,values[1],values[3])
		self.newEntryProcessTeam(niceTeamName,status,values[1],values[3],amend)

	def newEntryProcessTeam(self,niceTeamName,status,to_from,msg,amend=False):
		# rprint('t1: niceTeamName={} status={} to_from={} msg={} amend={}'.format(niceTeamName,status,to_from,msg,amend))
		extTeamName=getExtTeamName(niceTeamName)
		# 393: if the new entry's extTeamName is a case-insensitive match for an
		#   existing extTeamName, use that already-existing extTeamName instead
		for existingExtTeamName in self.extTeamNameList:
			if extTeamName.lower()==existingExtTeamName.lower():
				extTeamName=existingExtTeamName
				break
      # skip entries with no team like 'radio log begins', or multiple entries like 'all'
		if niceTeamName!='' and not niceTeamName.lower()=="all" and not niceTeamName.lower().startswith("all "):
			# if it's a team that doesn't already have a tab, make a new tab
			if extTeamName not in self.extTeamNameList:
				self.newTeam(niceTeamName)
			i=self.extTeamNameList.index(extTeamName)
			teamStatusDict[extTeamName]=status
			if not extTeamName in teamFSFilterDict:
				teamFSFilterDict[extTeamName]=0
			# credit to Berryblue031 for pointing out this way to style the tab widgets
			# http://www.qtcentre.org/threads/49025
			# NOTE the following line causes font-size to go back to system default;
			#  can't figure out why it doesn't inherit font-size from the existing
			#  styleSheet; so, each statusStyleDict entry must contain font-size explicitly
			self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).setStyleSheet(statusStyleDict[status])
			# only reset the team timer if it is a 'FROM' message with non-blank message text
			#  (prevent reset on amend, where to_from can be "AMEND" and msg can be anything)
			# if this was an amendment, set team timer based on the team's most recent 'FROM' entry
			if amend:
				rprint('t2')
				found=False
				for n in range(len(self.radioLog)-1,-1,-1):
					entry=self.radioLog[n]
					rprint(' t3:'+str(n)+':'+str(entry))
					if getExtTeamName(entry[2]).lower()==extTeamName.lower() and entry[1]=='FROM':
						rprint('  t4:match: now='+str(int(time.time())))
						rprint('  setting teamTimersDict to '+str(time.time()-entry[6]))
						teamTimersDict[extTeamName]=int(time.time()-entry[6])
						found=True
						break
				# if there are 'from' entries for the callsign, use the oldest 'to' entry for the callsign
				if not found:
					for entry in self.radioLog:
						rprint(' t3b:'+str(entry))
						if getExtTeamName(entry[2]).lower()==extTeamName.lower():
							rprint('t4b:"TO" match: now='+str(int(time.time())))
							teamTimersDict[extTeamName]=int(time.time()-entry[6])
							found=True
							break
				# this code should never be reached: what does it mean if there are no TO or FROM entries after amend?
				if not found:
					rprint('WARNING after amend: team timer may be undetermined because no entries (either TO or FROM) were found for '+str(niceTeamName))
			elif to_from=="FROM" and msg != "":
				teamTimersDict[extTeamName]=0
			# finally, disable timeouts as long as status is AT IC
			if status=="At IC":
				teamTimersDict[extTeamName]=-1 # no more timeouts will show up
		if not self.loadFlag:
			QTimer.singleShot(100,lambda:self.newEntryPost(extTeamName))

	def newEntryPost(self,extTeamName=None):
# 		rprint("1: called newEntryPost")
		self.radioLogNeedsPrint=True
		# don't do any sorting at all since layoutChanged during/after sort is
		#  a huge cause of lag; see notes in newEntry function
# 		rprint("3")
		# resize the bottom-most rows (up to 10 of them):
		#  this makes lag time independent of total row count for large tables,
		#  and reduces overall lag about 30% vs resizeRowsToContents (about 3 sec vs 4.5 sec for a 1300-row table)
		for n in range(len(self.radioLog)-10,len(self.radioLog)):
			if n>=0:
				self.ui.tableView.resizeRowToContents(n+1)
# 		rprint("4")
		self.ui.tableView.scrollToBottom()
# 		rprint("5")
		for i in [2,4]: # hardcode results in significant speedup
			self.ui.tableView.resizeColumnToContents(i)
# 		rprint("5.1")
		# note, the following clause results in a small lag for very large team count
		#  and large radioLog (about 0.1sec on TomZen for 180kB log file); probably
		#  not worth trying to optimize
		for n in self.ui.tableViewList[1:]:
			for i in [2,4]: # hardcode results in significant speedup
				n.resizeColumnToContents(i)
# 		rprint("5.2")
		if extTeamName:
# 			rprint("5.2.1")
			if extTeamName=="ALL TEAMS":
				for i in range(1,len(self.extTeamNameList)):
					self.ui.tabWidget.setCurrentIndex(i)
					self.ui.tableViewList[i].resizeRowsToContents()
					for n in range(len(self.radioLog)-10,len(self.radioLog)):
						if n>=0:
							self.ui.tableViewList[i].resizeRowToContents(n+1)
					self.ui.tableViewList[i].scrollToBottom()
			elif extTeamName!="z_00000":
# 				rprint("5.2.1.2")
				if extTeamName in self.extTeamNameList:
# 					rprint("5.2.1.2.1")
					i=self.extTeamNameList.index(extTeamName)
# 					rprint("  a: i="+str(i))
					self.ui.tabWidget.setCurrentIndex(i)
# 					rprint("  b")
					self.ui.tableViewList[i].resizeRowsToContents()
# 					rprint("  c")
					for n in range(len(self.radioLog)-10,len(self.radioLog)):
						if n>=0:
							self.ui.tableViewList[i].resizeRowToContents(n+1)
# 					rprint("  d")
					self.ui.tableViewList[i].scrollToBottom()
# 					rprint("  e")
# 		rprint("6")
		self.save()
##		self.redrawTables()
##		QCoreApplication.processEvents()
# 		rprint("7: finished newEntryPost")

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

	def amendEntry(self,row): # row argument is zero-based
		rprint("Amending row "+str(row))
		rprint('radioLog len = '+str(len(self.radioLog)))
		rprint(str(self.radioLog))
		# #508 - determine if the row being amended is the most recent row regarding the same callsign
		#    row argument is zero-based, and radiolog always has a dummy row at the end
		team=self.radioLog[row][2]
		extTeamName=getExtTeamName(team)
		found=False
		for n in range(row+1,len(self.radioLog)):
			entry=self.radioLog[n]
			rprint(' t3:'+str(n)+':'+str(entry))
			if getExtTeamName(entry[2]).lower()==extTeamName.lower():
				found=True
				break
		if found:
			rprint('found a newer entry for '+team+' than the one being amended')
		else:
			rprint('did not find a newer entry for '+team+' than the one being amended')
		isMostRecent=not found
		amendDialog=self.openNewEntry(amendFlag=True,amendRow=row,isMostRecentForCallsign=isMostRecent)

	def rebuildTabs(self):
# 		groupDict=self.rebuildGroupedTabDict()
# 		tabs=[]
# 		for group in groupDict:
# 			tabs.extend(groupDict[group])
# 			tabs.append("")
# 		rprint("Final tabs list:"+str(tabs))
# 		bar=self.ui.tabWidget.tabBar()
# 		for i in range(len(tabs)):
# 			bar.insertTab(i,tabs[i])
# 			if tabs[i]=="":
# 				bar.setTabEnabled(i,False)
# 		rprint("extTeamNameList before sort:"+str(self.extTeamNameList))
# # 		self.extTeamNameList.sort()
# 		self.rebuildGroupedTabDict()
# 		rprint("extTeamNameList after sort:"+str(self.extTeamNameList))
		self.ui.tabList=[]
		self.ui.tabGridLayoutList=[]
		self.ui.tableViewList=[]
# 		self.proxyModelList=["dummy"]
# 		self.teamNameList=["dummy"]
# 		self.allTeamsList=[] # same as teamNameList but hidden tabs are not deleted from this list
		
		bar=self.ui.tabWidget.tabBar()
		while bar.count()>0:
# 			print("count:"+str(bar.count()))
			bar.removeTab(0)
		for extTeamName in self.extTeamNameList:
			self.addTab(extTeamName)
# 		self.rebuildTeamHotkeys()
	
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
		rprint("extTeamNameList before sort:"+str(self.extTeamNameList))
# 		self.extTeamNameList.sort()
		
		self.rebuildGroupedTabDict()
		rprint("extTeamNameList after sort:"+str(self.extTeamNameList))
		self.rebuildTabs()
		
		if not extTeamName.startswith("spacer"):
			# add to team name lists and dictionaries
			i=self.extTeamNameList.index(extTeamName) # i is zero-based
			self.teamNameList.insert(i,niceTeamName)
# 			rprint("   niceTeamName="+str(niceTeamName)+"  allTeamsList before:"+str(self.allTeamsList)+"  count:"+str(self.allTeamsList.count(niceTeamName)))
			if self.allTeamsList.count(niceTeamName)==0:
				self.allTeamsList.insert(i,niceTeamName)
				self.allTeamsList.sort()
# 				rprint("   allTeamsList after:"+str(self.allTeamsList))
			teamTimersDict[extTeamName]=0
			teamCreatedTimeDict[extTeamName]=time.time()
			# assign team hotkey
			hotkey=self.getNextAvailHotkey()
			rprint("next available hotkey:"+str(hotkey))
			if hotkey:
				self.hotkeyDict[hotkey]=niceTeamName
			else:
				rprint("Team hotkey pool has been used up.  Not setting any hotkeyDict entry for "+niceTeamName)
				
		self.rebuildTeamHotkeys()

		"""		
		i=self.extTeamNameList.index(extTeamName) # i is zero-based
		if len(self.extTeamNameList)>>i+1:
			if self.extTeamNameList[i+1]=="":
				rprint("  spacer needed after this new team")
		if i>>0:
			if self.extTeamNameList[i-1]=="":
				rprint("  spacer needed before this new team")
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
		label=QLabel(" "+shortNiceTeamName+" ")
		label.setStyleSheet("font-size:20px;border:1px outset black;qproperty-alignment:AlignCenter")
		rprint("setting tab button #"+str(i)+" to "+label.text())
		bar=self.ui.tabWidget.tabBar()
		bar.setTabButton(i,QTabBar.LeftSide,label)
		# during rebuildTeamHotkeys, we need to read the name of currently displayed tabs.
		#  An apparent bug causes the tabButton (a label) to not have a text attrubite;
		#  so, use the whatsThis attribute instead.
		bar.setTabWhatsThis(i,niceTeamName)
		bar.tabButton(i,QTabBar.LeftSide).setStyleSheet("font-size:20px;border:1px outset black;qproperty-alignment:AlignHCenter")
		# spacers should be disabled
		if extTeamName=="":
			bar.setTabEnabled(i,False)
		# hotkeyDict: key=hotkey  val=niceTeamName
		# hotkeyRDict: key=niceTeamName  val=hotkey
		
		hotkey=self.getNextAvailHotkey()
		if hotkey:
			self.hotkeyDict[hotkey]=niceTeamName
		else:
			rprint("Team hotkey pool has been used up.  Not setting any hotkeyDict entry for "+niceTeamName)
		
		self.rebuildTeamHotkeys()
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
		self.proxyModelList[i].setFilterFixedString(extTeamName)
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


# 		self.rebuildTabs()
			
##	def deletePrint(self):
##		rprint("deleting")

		"""

	def addTab(self,extTeamName):
		niceTeamName=getNiceTeamName(extTeamName)
		shortNiceTeamName=getShortNiceTeamName(niceTeamName)
# 		rprint("new team: extTeamName="+extTeamName+" niceTeamName="+niceTeamName+" shortNiceTeamName="+shortNiceTeamName)
		i=self.extTeamNameList.index(extTeamName) # i is zero-based
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
		label=QLabel(" "+shortNiceTeamName+" ")
		if len(shortNiceTeamName)<2:
			label.setText("  "+shortNiceTeamName+"  ") # extra spaces to make effective tab min width
		if extTeamName.startswith("spacer"):
			label.setText("")
		else:
# 			rprint("setting style for label "+extTeamName)
			label.setStyleSheet("font-size:18px;qproperty-alignment:AlignCenter")
# 			label.setStyleSheet(statusStyleDict[""])
# 		rprint("setting tab button #"+str(i)+" to "+label.text())
		bar=self.ui.tabWidget.tabBar()
		bar.setTabButton(i,QTabBar.LeftSide,label)
		# during rebuildTeamHotkeys, we need to read the name of currently displayed tabs.
		#  An apparent bug causes the tabButton (a label) to not have a text attrubite;
		#  so, use the whatsThis attribute instead.
		bar.setTabWhatsThis(i,niceTeamName)
# 		rprint("setting style for tab#"+str(i))
# 		bar.tabButton(i,QTabBar.LeftSide).setStyleSheet("font-size:18px;qproperty-alignment:AlignHCenter")
		bar.tabButton(i,QTabBar.LeftSide).setStyleSheet(statusStyleDict[""])
# 		if not extTeamName.startswith("spacer"):
# 			label.setStyleSheet("font-size:40px;border:1px outset green;qproperty-alignment:AlignHCenter")
		# spacers should be disabled
		if extTeamName.startswith("spacer"):
			bar.setTabEnabled(i,False)

# 		if not extTeamName.startswith("spacer"):
# 			hotkey=self.getNextAvailHotkey()
# 			rprint("next available hotkey:"+str(hotkey))
# 			if hotkey:
# 				self.hotkeyDict[hotkey]=niceTeamName
# 			else:
# 				rprint("Team hotkey pool has been used up.  Not setting any hotkeyDict entry for "+niceTeamName)
# 		self.rebuildTeamHotkeys()
		
		# better to NOT modify the entered team name value, for data integrity;
		# instead, set the filter to only display rows where the human readable form
		# of the value in column 2 matches the human readable form of the tab name
		self.proxyModelList.insert(i,CustomSortFilterProxyModel(self))
		self.proxyModelList[i].setSourceModel(self.tableModel)
		self.proxyModelList[i].setFilterFixedString(extTeamName)
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
		
	def rebuildGroupedTabDict(self):
		# sort the tabs list, inserting hidden uniquely-named spacer tabs between groups
		# grouping sequence and regular expressions are defined in the local config file
		#  with the 'tabGroups' variable, which is a list of regular expressions;
		#  any callsign that does not match any of the regular expressions will
		#  be placed in a catch-all group at the end.
		# Once a callsign has been assigned to a group, make sure to not assign it
		#  to any other groups.
		grouped=dict()
		for grp in self.tabGroups:
			grouped[grp[0]]=[]
		grouped["other"]=[]
		for etn in [x for x in self.extTeamNameList if not x.startswith("spacer")]: # spacerless list
			g="other" # default to the 'other' group
			for grp in self.tabGroups:
				if re.match(grp[1].replace("^","^z_0*").replace("Team ","Team"),etn,re.IGNORECASE):
					# account for leading 'z_' and any zeros introduced by getExtTeamName
					g=grp[0]
					break # use only the first matching group
			grouped[g].append(etn)
			
		# sort alphanumerically within each group
		for grp in grouped:
			grouped[grp].sort()
			
		rprint("grouped tabs:"+str(grouped))
		self.groupedTabDict=grouped
		
		# rebuild self.extTeamNameList, with groups and spacers in the correct order,
		#  since everything throughout the code keys off its sequence;
		#  note the spacer names need to be unique for later processing
		self.extTeamNameList=[]
		spacerIndex=1 # start with 1 so trailing 0 doesn't get deleted in getNiceTeamName
		for grp in self.tabGroups:
# 			rprint("group:"+str(grp)+":"+str(grouped[grp[0]]))
			for val in grouped[grp[0]]:
# 				rprint("appending:"+val)
				self.extTeamNameList.append(val)
			if len(grouped[grp[0]])>0:
				self.extTeamNameList.append("spacer"+str(spacerIndex))
				spacerIndex=spacerIndex+1
		for val in grouped["other"]:
			if val!="dummy":
# 				rprint("appending other:"+val)
				self.extTeamNameList.append(val)
			
	def tabContextMenu(self,pos):
		menu=QMenu()
		rprint("tab context menu requested: pos="+str(pos))
##		menu.setStyleSheet("font-size:"+str(self.fontSize)+"pt")
		bar=self.ui.tabWidget.tabBar()
		i=bar.tabAt(pos) # returns -1 if not a valid tab
		rprint("  i="+str(i)+"  tabRect="+str(bar.tabRect(i).bottomLeft())+":"+str(bar.tabRect(i).topRight()))
		extTeamName=self.extTeamNameList[i]
		niceTeamName=getNiceTeamName(extTeamName)
		rprint("  extTeamName="+str(extTeamName)+"  niceTeamName="+str(niceTeamName))
# 		if i>0:
		if i>-1 and not extTeamName.lower().startswith("spacer"):
			newEntryFromAction=menu.addAction("New Entry FROM "+str(niceTeamName))
			newEntryToAction=menu.addAction("New Entry TO "+str(niceTeamName))
			menu.addSeparator()
			printTeamLogAction=menu.addAction(QIcon(QPixmap(":/radiolog_ui/icons/print_icon.png")),"Print "+str(niceTeamName)+" Log")
			menu.addSeparator()
##			relabelTeamTabAction=menu.addAction("Change Label / Assignment for "+str(niceTeamName))
##			menu.addSeparator()

		# add fleetsync submenu if there are any fleetsync devices for this callsign
			devices=self.fsGetTeamDevices(extTeamName)
			fsToggleAllAction=False # initialize, so the action checker does not die
			fsSendTextToAllAction=False # initialize, so the action checker does not die
			if len(devices)>0:
				fsMenu=menu.addMenu("FleetSync...")
				menu.addSeparator()
				if self.enableSendText:
					if len(devices)>1:
						fsSendTextToAllAction=fsMenu.addAction("Send text message to all "+niceTeamName+" devices")
						fsMenu.addSeparator()
					for device in devices:
						key=str(device[0])+":"+str(device[1])
						fsMenu.addAction("Send text message to "+key).setData([device[0],device[1],'SendText'])
					fsMenu.addSeparator()
				if self.enablePollGPS:
					for device in devices:
						key=str(device[0])+":"+str(device[1])
						fsMenu.addAction("Request location from "+key).setData([device[0],device[1],'PollGPS'])
					fsMenu.addSeparator()
				if len(devices)>1:
					if teamFSFilterDict[extTeamName]==2:
						fsToggleAllAction=fsMenu.addAction("Unfilter all "+niceTeamName+" devices")
					else:
						fsToggleAllAction=fsMenu.addAction("Filter all "+niceTeamName+" devices")
					fsMenu.addSeparator()
					for device in devices:
						key=str(device[0])+":"+str(device[1])
						if self.fsIsFiltered(device[0],device[1]):
							fsMenu.addAction("Unfilter calls from "+key).setData([device[0],device[1],'unfilter'])
						else:
							fsMenu.addAction("Filter calls from "+key).setData([device[0],device[1],'filter'])
				else:
					key=str(devices[0][0])+":"+str(devices[0][1])
					if teamFSFilterDict[extTeamName]==2:
						fsToggleAllAction=fsMenu.addAction("Unfilter calls from "+niceTeamName+" ("+key+")")
					else:
						fsToggleAllAction=fsMenu.addAction("Filter calls from "+niceTeamName+" ("+key+")")
			deleteTeamTabAction=menu.addAction("Hide tab for "+str(niceTeamName))

			# action handlers
			action=menu.exec_(self.ui.tabWidget.tabBar().mapToGlobal(pos))
			if action==newEntryFromAction:
				self.openNewEntry('tab',str(niceTeamName))
			elif action==newEntryToAction:
				self.openNewEntry('tab',str(niceTeamName))
				self.newEntryWidget.ui.to_fromField.setCurrentIndex(1)
			elif action==printTeamLogAction:
				rprint("printing team log for "+str(niceTeamName))
				self.printLog(self.opPeriod,str(niceTeamName))
				self.radioLogNeedsPrint=True # since only one log has been printed; need to enhance this
			elif action==deleteTeamTabAction:
				self.deleteTeamTab(niceTeamName)
			elif action and action.data(): # only the single-device toggle/text/poll actions will have data
				d=action.data()
				if 'filter' in d[2].lower():
					self.fsFilterEdit(d[0],d[1],d[2].lower()=='filter')
					self.fsBuildTeamFilterDict()
				elif d[2]=='SendText':
					callsignText=self.getCallsign(d[0],d[1])
					if callsignText:
						callsignText='('+callsignText+')'
					else:
						callsignText='(no callsign)'
					box=fsSendMessageDialog(self,[[d[0],d[1],callsignText]])
					box.show()
					box.raise_()
					box.exec_()
				elif d[2]=='PollGPS':
					self.pollGPS(d[0],d[1])
				else:
					rprint('unknown context menu action:'+str(d))
			elif action==fsToggleAllAction:
				newState=teamFSFilterDict[extTeamName]!=2 # if 2, unfilter all; else, filter all
				for device in self.fsGetTeamDevices(extTeamName):
					self.fsFilterEdit(device[0],device[1],newState)
				self.fsBuildTeamFilterDict()
			elif action==fsSendTextToAllAction:
				theList=[]
				for device in self.fsGetTeamDevices(extTeamName):
					callsignText=self.getCallsign(device[0],device[1])
					if callsignText:
						callsignText='('+callsignText+')'
					else:
						callsignText='(no callsign)'
					theList.append([device[0],device[1],callsignText])
				box=fsSendMessageDialog(self,theList)
				box.show()
				box.raise_()
				box.exec_()
				

##			if action==relabelTeamTabAction:
##				label=QLabel(" abcdefg ")
##				label.setStyleSheet("font-size:20px;border:1px outset black;qproperty-alignment:AlignCenter")
##				self.ui.tabWidget.tabBar().setTabButton(i,QTabBar.LeftSide,label)
####				self.ui.tabWidget.tabBar().setTabText(i,"boo")
##				self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).setStyleSheet("font-size:20px;border:1px outset black;qproperty-alignment:AlignCenter")

	# sendText and pollGPS:
	# self.firstComPort and secondComPort are not defined until valid FS data has been read from that port.
	#  Even if we expand the definition of 'valid' data, we want to be able to send to a port regardless of
	#  whether any data has yet been read from that port. May want to revise that to help with the send functions.

	# How do we decide which COM port to send to?  There's no perfect solution, but, let's go with this plan:
	# Q1: is self.firstComPort alive?
	#   YES1: Q2: is self.secondComPort alive?
	#     YES2: Q3: does self.fsLog have an entry for the device in question?
	#       YES3: send to the com port specified for that device in self.fsLog
	#                i.e. the com port on which that device was most recently heard from
	#                 (if failed, send to the other port; if that also fails, show failure message)
	#       NO3: send to the com port that has the most recent entry (for any device) in self.fsLog
	#                 (if failed, send to the other port; if that also fails, show failure message)
	#     NO2: send to firstComPort (if failed, show failure message - there is no second port to try)
	#   NO1: cannot send - show a message box and return False
	# 

	# def fsSendData(self,d,portList=None):
	# 	portList=portList or [self.firstComPort]
	# 	rprint('trying to send - portList='+str(portList))
	# 	if portList and len(portList)>0:
	# 		for port in portList:
	# 			rprint('Sending FleetSync data to '+str(port.name)+'...')
	# 			port.write(d.encode())
	# 	else:
	# 		rprint('Cannot send FleetSync data - no open ports were found.')

	# can be called recursively by omitting arguments after d
	# def fsSendData(self,d,fleet=None,device=None,port=None):
	# 	# port=port or self.firstComPort
	# 	if fleet and device:
	# 		if int(fleet)==0 and int(device)==0: # it's a broadcast - send to both com ports in sequence
	# 			self.firstComPort.write(d.encode())
	# 			if self.secondComPort:
	# 				time.sleep(3) # yes, we do want a blocking sleep
	# 				self.secondComPort.write(d.encode())
	# 			return True
	# 		else:
	# 			firstPortToTry=self.fsGetLatestComPort(fleet,device)
	# 			secondPortToTry=None
	# 			if firstPortToTry==self.firstComPort and self.secondComPort:
	# 				secondPortToTry=self.secondComPort
	# 			elif firstPortToTry==self.secondComPort and self.firstComPort:
	# 				secondPortToTry=self.firstComPort
	# 			firstPortToTry.write(d.encode())
	# 			self.fsAwaitingResponse=[fleet,device,'Text message sent',0,d]
	# 			[f,dev,t]=self.fsAwaitingResponse[0:3]
	# 			self.fsAwaitingResponseMessageBox=QMessageBox(QMessageBox.Information,t,t+' to '+str(fleet)+':'+str(device)+'; awaiting response up to '+str(self.fsAwaitingResponseTimeout)+' seconds...',
	# 							QMessageBox.Abort,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
	# 			self.fsAwaitingResponseMessageBox.show()
	# 			self.fsAwaitingResponseMessageBox.raise_()
	# 			self.fsAwaitingResponseMessageBox.exec_()
	# 			if self.fsFailedFlag: # timed out, or, got a '1' response
	# 				rprint('failed; need to send again')
	# 				if secondPortToTry:
	# 					self.fsAwaitingResponseMessageBox.setText('No response after sending from preferred radio.  Sending from alternate radio; awaiting response up to '+str(self.fsAwaitingResponseTimeout)+' seconds...')
	# 					secondPortToTry.write(d.encode())
	# 					self.fsAwaitingResponse[3]=0 # reset the timer
	# 			else:
	# 				rprint('apparently successful')
	# 			self.fsAwaitingResponse=None # clear the flag - this will happen after the messagebox is closed (due to valid response, or timeout in fsCheck, or Abort clicked)






	# 	else: # this must be the recursive call where we actually send the data	
	# 		success=False
	# 		if port:
	# 			rprint('Sending FleetSync data to '+str(port.name)+'...')
	# 			port.write(d.encode())
	# 			return True
	# 		else:
	# 			msg='Cannot send FleetSync data - no valid FleetSync COM ports were found.  Keying the mic on a portable radio will trigger COM port recognition.'
	# 			rprint(msg)
	# 			box=QMessageBox(QMessageBox.Critical,'FleetSync error',msg,
	# 				QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
	# 			box.open()
	# 			box.raise_()
	# 			box.exec_()
	# 			return False


	# Serial data format for sendText and pollGPS functions was discovered by using RADtext 
	#    https://radtext.morganized.com/radtext
	#  along with a virtual COM port bridge, and a COM port terminal emulator to watch the traffic

	# sendText - outgoing serial port data format:
	#
	# <start><length_code><fleet><device><msg><sequence><end>
	#
	# <start> - 02 hex (ascii smiley face)
	# <length_code> - indicates max possible message length, though the plain text message is not padded to that length
	#   46 hex (ascii F) - corresponds to 'S' (Short - 48 characters)
	#   47 hex (ascii G) - corresponds to both 'L' (Long - 1024 characters) and 'X' (Extra-long - 4096 characters)
	#   if you send COM port data with message body longer than that limit, the mobile will not transmit
	# <fleet> - plain-text three-digit fleet ID (000 for broadcast)
	# <device> - plain-text four-digit device ID (0000 for broadcast)
	# <msg> - plain-text message
	# UNUSED: <sequence> - plain-text two-digit decimal sequence identifier - increments with each send - probably not relevant
	#   NOTE: sequnce is generated by radtext, but, it shows up as part of the message body on the
	#          receiving device, which is probably not useful.  Interesting point that we could
	#          add timestamp or such to the message body if needed, but, this is not a separate token.
	# <end> - 03 hex (ascii heart)
	#
	# examples:
	# broadcast 'test' (short):  02 46 30 30 30 30 30 30 30 74 65 73 74 32 39 03   F0000000test28  (sequence=28)
	# 100:1002 'test' (short):  02 46 31 30 30 31 30 30 32 74 65 73 74 33 31 03   F1001002test31  (sequence=31)

	def sendText(self,fleetOrListOrAll,device=None,message=None):
		self.fsTimedOut=False
		self.fsResponseMessage=''
		broadcast=False
		self.fsSendList=[[]]
		self.fsFailedFlag=False
		if isinstance(fleetOrListOrAll,list):
			self.fsSendList=fleetOrListOrAll
		elif fleetOrListOrAll=='ALL':
			broadcast=True
		else:
			self.fsSendList=[[fleetOrListOrAll,device]]
		if message:
			if self.fsShowChannelWarning:
				m='WARNING: You are about to send FleetSync data burst noise on one or both mobile radios.\n\nMake sure that neither radio is set to any law or fire channel, or any other channel where FleetSync data bursts would cause problems.'
				box=QMessageBox(QMessageBox.Warning,'FleetSync Channel Warning',m,
								QMessageBox.Ok|QMessageBox.Cancel,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
				box.show()
				box.raise_()
				box.exec_()
				if box.clickedButton().text()=='Cancel':
					return
			timestamp=time.strftime("%b%d %H:%M") # this uses 11 chars plus space, leaving 36 usable for short message
			# timestamp=time.strftime('%m/%d/%y %H:%M') # this uses 14 chars plus space
			rprint('message:'+str(message))
			if broadcast:
				# portable radios will not attempt to send acknowledgement for broadcast
				rprint('broadcasting text message to all devices')
				d='\x02\x460000000'+timestamp+' '+message+'\x03'
				rprint('com data: '+str(d))
				suffix=' using one mobile radio'
				self.firstComPort.write(d.encode())
				if self.secondComPort:
					time.sleep(3) # yes, we do want a blocking sleep
					suffix=' using two mobile radios'
					self.secondComPort.write(d.encode())
				# values format for adding a new entry:
				#  [time,to_from,team,message,self.formattedLocString,status,self.sec,self.fleet,self.dev,self.origLocString]
				values=["" for n in range(10)]
				values[0]=time.strftime("%H%M")
				values[3]='TEXT MESSAGE SENT TO ALL DEVICES'+suffix+': "'+str(message)+'"'
				values[6]=time.time()
				self.newEntry(values)
			else:
				# recipient portable will send acknowledgement when fleet and device ase specified
				for [fleet,device] in self.fsSendList:
					# values format for adding a new entry:
					#  [time,to_from,team,message,self.formattedLocString,status,self.sec,self.fleet,self.dev,self.origLocString]
					values=["" for n in range(10)]
					callsignText=self.getCallsign(fleet,device)
					values[2]=str(callsignText)
					if callsignText:
						callsignText='('+callsignText+')'
					else:
						callsignText='(no callsign)'
					rprint('sending text message to fleet='+str(fleet)+' device='+str(device)+' '+callsignText)
					d='\x02\x46'+str(fleet)+str(device)+timestamp+' '+message+'\x03'
					rprint('com data: '+str(d))
					fsFirstPortToTry=self.fsGetLatestComPort(fleet,device) or self.firstComPort
					if fsFirstPortToTry==self.firstComPort:
						self.fsSecondPortToTry=self.secondComPort # could be None; inst var so fsCheck can see it
					else:
						self.fsSecondPortToTry=self.firstComPort # could be None; inst var so fsCheck can see it
					self.fsThereWillBeAnotherTry=False
					if self.fsSecondPortToTry:
						self.fsThereWillBeAnotherTry=True
					# rprint('1: fsThereWillBeAnotherTry='+str(self.fsThereWillBeAnotherTry))
					fsFirstPortToTry.write(d.encode())
					# if self.fsSendData(d,fsFirstPortToTry):
					self.fsAwaitingResponse=[fleet,device,'Text message sent',0,message]
					[f,dev,t]=self.fsAwaitingResponse[0:3]
					self.fsAwaitingResponseMessageBox=QMessageBox(QMessageBox.NoIcon,t,t+' to '+str(f)+':'+str(dev)+' on preferred COM port; awaiting response up to '+str(self.fsAwaitingResponseTimeout)+' seconds...',
									QMessageBox.Abort,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
					self.fsAwaitingResponseMessageBox.show()
					self.fsAwaitingResponseMessageBox.raise_()
					self.fsAwaitingResponseMessageBox.exec_()
					# add a log entry when Abort is pressed
					if self.fsAwaitingResponse and not self.fsTimedOut:
						values[0]=time.strftime("%H%M")
						values[1]='TO'
						values[3]='FLEETSYNC: Text message sent to '+str(f)+':'+str(dev)+' '+callsignText+' but radiolog operator clicked Abort before delivery could be confirmed: "'+str(message)+'"'
						values[6]=time.time()
						self.newEntry(values)
						self.fsResponseMessage+='\n\n'+str(f)+':'+str(dev)+' '+callsignText+': radiolog operator clicked Abort before delivery could be confirmed'
					if self.fsFailedFlag: # timed out, or, got a '1' response
						if self.fsSecondPortToTry:
							rprint('failed on preferred COM port; sending on alternate COM port')
							self.fsTimedOut=False
							self.fsFailedFlag=False # clear the flag
							self.fsSecondPortToTry.write(d.encode())
							self.fsThereWillBeAnotherTry=False
							# rprint('2: fsThereWillBeAnotherTry='+str(self.fsThereWillBeAnotherTry))
							self.fsAwaitingResponse[3]=0 # reset the timer
							self.fsAwaitingResponseMessageBox=QMessageBox(QMessageBox.NoIcon,t,t+' to '+str(f)+':'+str(dev)+' on alternate COM port; awaiting response up to '+str(self.fsAwaitingResponseTimeout)+' seconds...',
											QMessageBox.Abort,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
							self.fsAwaitingResponseMessageBox.show()
							self.fsAwaitingResponseMessageBox.raise_()
							self.fsAwaitingResponseMessageBox.exec_()
							# add a log entry when Abort is pressed
							if self.fsAwaitingResponse and not self.fsTimedOut:
								values[0]=time.strftime("%H%M")
								values[1]='TO'
								values[3]='FLEETSYNC: Text message sent to '+str(f)+':'+str(dev)+' '+callsignText+' but radiolog operator clicked Abort before delivery could be confirmed: "'+str(message)+'"'
								values[6]=time.time()
								self.newEntry(values)
								self.fsResponseMessage+='\n\n'+str(f)+':'+str(dev)+' '+callsignText+': radiolog operator clicked Abort before delivery could be confirmed'
							if self.fsFailedFlag: # timed out, or, got a '1' response
								rprint('failed on alternate COM port: message delivery not confirmed')
							else:
								rprint('apparently successful on alternate COM port')
								self.fsResponseMessage+='\n\n'+str(f)+':'+str(dev)+' '+callsignText+': delivery confirmed'
						else:
							rprint('failed on preferred COM port; no alternate COM port available')
					else:
						rprint('apparently successful on preferred COM port')
						self.fsResponseMessage+='\n\n'+str(f)+':'+str(dev)+' '+callsignText+': delivery confirmed'
					self.fsAwaitingResponse=None # clear the flag - this will happen after the messagebox is closed (due to valid response, or timeout in fsCheck, or Abort clicked)
				if self.fsResponseMessage:
					box=QMessageBox(QMessageBox.Information,'FleetSync Response Summary','FleetSync response summary:'+self.fsResponseMessage,
						QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
					box.open()
					box.raise_()
					box.exec_()


	# pollGPS - outgoing serial port data format:
	#
	# <start><poll_code><fleet><device><sequence><end>
	#
	# <start> - 02 hex (ascii smiley face)
	# <poll_code> - 52 33 hex (ascii R3)
	# <fleet> - plain-text three-digit fleet ID (000 for broadcast)
	# <device> - plain-text four-digit device ID (0000 for broadcast)
	# UNUSED - see sendText notes - <sequence> - plain-text two-digit decimal sequence identifier - increments with each send - probably not relevant
	# <end> - 03 hex (ascii heart)

	# examples:
	# poll 100:1001:  02 52 33 31 30 30 31 30 30 31 32 35 03   R3100100120  (sequence=20)
	# poll 100:1002:  02 52 33 31 30 30 31 30 30 32 32 37 03   R3100100221  (sequence=21)
	
	def pollGPS(self,fleet,device):
		if self.fsShowChannelWarning:
			m='WARNING: You are about to send FleetSync data burst noise on one or both mobile radios.\n\nMake sure that neither radio is set to any law or fire channel, or any other channel where FleetSync data bursts would cause problems.'
			box=QMessageBox(QMessageBox.Warning,'FleetSync Channel Warning',m,
							QMessageBox.Ok|QMessageBox.Cancel,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			box.show()
			box.raise_()
			box.exec_()
			if box.clickedButton().text()=='Cancel':
				return
		rprint('polling GPS for fleet='+str(fleet)+' device='+str(device))
		d='\x02\x52\x33'+str(fleet)+str(device)+'\x03'
		rprint('com data: '+str(d))
		self.fsTimedOut=False
		self.fsFailedFlag=False
		fsFirstPortToTry=self.fsGetLatestComPort(fleet,device) or self.firstComPort
		if fsFirstPortToTry==self.firstComPort:
			self.fsSecondPortToTry=self.secondComPort # could be None; inst var so fsCheck can see it
		else:
			self.fsSecondPortToTry=self.firstComPort # could be None; inst var so fsCheck can see it
		self.fsThereWillBeAnotherTry=False
		if self.fsSecondPortToTry:
			self.fsThereWillBeAnotherTry=True
		# rprint('3: fsThereWillBeAnotherTry='+str(self.fsThereWillBeAnotherTry))
		fsFirstPortToTry.write(d.encode())
		self.fsAwaitingResponse=[fleet,device,'Location request sent',0]
		[f,dev,t]=self.fsAwaitingResponse[0:3]
		self.fsAwaitingResponseMessageBox=QMessageBox(QMessageBox.NoIcon,t,t+' to '+str(f)+':'+str(dev)+' on preferred COM port; awaiting response up to '+str(self.fsAwaitingResponseTimeout)+' seconds...',
						QMessageBox.Abort,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
		self.fsAwaitingResponseMessageBox.show()
		self.fsAwaitingResponseMessageBox.raise_()
		self.fsAwaitingResponseMessageBox.exec_()
		# add a log entry when Abort is pressed
		if self.fsAwaitingResponse and not self.fsTimedOut:
			# values format for adding a new entry:
			#  [time,to_from,team,message,self.formattedLocString,status,self.sec,self.fleet,self.dev,self.origLocString]
			values=["" for n in range(10)]
			values[0]=time.strftime("%H%M")
			callsignText=self.getCallsign(f,dev)
			values[2]=str(callsignText)
			if callsignText:
				callsignText='('+callsignText+')'
			else:
				callsignText='(no callsign)'
			values[3]='FLEETSYNC: GPS location request set to '+str(f)+':'+str(dev)+' '+callsignText+' but radiolog operator clicked Abort before response was received'
			values[6]=time.time()
			self.newEntry(values)
		if self.fsFailedFlag: # timed out, or, got a '1' response
			if self.fsSecondPortToTry:
				rprint('failed on preferred COM port; sending on alternate COM port')
				self.fsTimedOut=False
				self.fsFailedFlag=False # clear the flag
				self.fsThereWillBeAnotherTry=False
				# rprint('5: fsThereWillBeAnotherTry='+str(self.fsThereWillBeAnotherTry))
				self.fsSecondPortToTry.write(d.encode())
				self.fsAwaitingResponse[3]=0 # reset the timer
				self.fsAwaitingResponseMessageBox=QMessageBox(QMessageBox.NoIcon,t,t+' to '+str(f)+':'+str(dev)+' on alternate COM port; awaiting response up to '+str(self.fsAwaitingResponseTimeout)+' seconds...',
								QMessageBox.Abort,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
				self.fsAwaitingResponseMessageBox.show()
				self.fsAwaitingResponseMessageBox.raise_()
				self.fsAwaitingResponseMessageBox.exec_()
				# add a log entry when Abort is pressed
				if self.fsAwaitingResponse and not self.fsTimedOut:
					# values format for adding a new entry:
					#  [time,to_from,team,message,self.formattedLocString,status,self.sec,self.fleet,self.dev,self.origLocString]
					values=["" for n in range(10)]
					values[0]=time.strftime("%H%M")
					callsignText=self.getCallsign(f,dev)
					values[2]=str(callsignText)
					if callsignText:
						callsignText='('+callsignText+')'
					else:
						callsignText='(no callsign)'
					values[3]='FLEETSYNC: GPS location request set to '+str(f)+':'+str(dev)+' '+callsignText+' but radiolog operator clicked Abort before response was received'
					values[6]=time.time()
					self.newEntry(values)
				if self.fsFailedFlag: # timed out, or, got a '1' response
					rprint('failed on alternate COM port: message delivery not confirmed')
				else:
					rprint('apparently successful on alternate COM port')
			else:
				rprint('failed on preferred COM port; no alternate COM port available')
		else:
			rprint('apparently successful on preferred COM port')
		self.fsAwaitingResponse=None # clear the flag - this will happen after the messagebox is closed (due to valid response, or timeout in fsCheck, or Abort clicked)

	def deleteTeamTab(self,teamName,ext=False):
		# optional arg 'ext' if called with extTeamName
		# must also modify related lists to keep everything in sync
		extTeamName=getExtTeamName(teamName)
		if ext:
			extTeamName=teamName
		niceTeamName=getNiceTeamName(extTeamName)
		# 406: apply the same fix as #393:
		# if the new entry's extTeamName is a case-insensitive match for an
		#   existing extTeamName, use that already-existing extTeamName instead
		for existingExtTeamName in self.extTeamNameList:
			if extTeamName.lower()==existingExtTeamName.lower():
				extTeamName=existingExtTeamName
				break
# 		self.extTeamNameList.sort()
		rprint("deleting team tab: teamName="+str(teamName)+"  extTeamName="+str(extTeamName)+"  niceTeamName="+str(niceTeamName))
		rprint("  teamNameList before deletion:"+str(self.teamNameList))
		rprint("  extTeamNameList before deletion:"+str(self.extTeamNameList))
		if extTeamName in self.extTeamNameList: # pass through if trying to delete a tab that doesn't exist / has already been deleted
			i=self.extTeamNameList.index(extTeamName)
			rprint("  i="+str(i))
			self.extTeamNameList.remove(extTeamName)
			if not teamName.lower().startswith("spacer"):
				self.teamNameList.remove(niceTeamName)
				del teamTimersDict[extTeamName]
				del teamCreatedTimeDict[extTeamName]
			del self.ui.tabList[i]
			del self.ui.tabGridLayoutList[i]
			del self.ui.tableViewList[i]
			self.ui.tabWidget.removeTab(i)
			try:
				del self.proxyModelList[i]
			except:
				rprint("  ** sync error: proxyModelList current length = "+str(len(self.proxyModelList))+"; requested to delete index "+str(i)+"; continuing...")
			else:
				rprint("  deleted proxyModelList index "+str(i))
			# free the hotkey, and reassign it to the first (if any) displayed callsign that has no hotkey
			hotkeyRDict={v:k for k,v in self.hotkeyDict.items()}
			if niceTeamName in hotkeyRDict:
				hotkey=hotkeyRDict[niceTeamName]
				rprint("Freeing hotkey '"+hotkey+"' which was used for callsign '"+niceTeamName+"'")
				del self.hotkeyDict[hotkey]
				bar=self.ui.tabWidget.tabBar()
				taken=False
				for i in range(1,bar.count()):
					if not taken:
						callsign=bar.tabWhatsThis(i)
						rprint("checking tab#"+str(i)+":"+callsign)
						if callsign not in hotkeyRDict and not callsign.lower().startswith("spacer"):
							rprint("  does not have a hotkey; using the freed hotkey '"+hotkey+"'")
							self.hotkeyDict[hotkey]=callsign
							taken=True
		self.rebuildTeamHotkeys()
		rprint("  extTeamNameList after delete: "+str(self.extTeamNameList))
		# if there are two adjacent spacers, delete the second one
		for n in range(len(self.extTeamNameList)-1):
			if self.extTeamNameList[n].lower().startswith("spacer"):
				if self.extTeamNameList[n+1].lower().startswith("spacer"):
					rprint("  found back-to-back spacers at indices "+str(n)+" and "+str(n+1))
					self.deleteTeamTab(self.extTeamNameList[n+1],True)

	def getNextAvailHotkey(self):
		# iterate through hotkey pool until finding one that is not taken
		for hotkey in self.hotkeyPool:
			if hotkey not in self.hotkeyDict:
				return hotkey
		return None # no available hotkeys

	def rebuildTeamHotkeys(self):
		# delete all child widgets
		while self.ui.teamHotkeysHLayout.count():
			child=self.ui.teamHotkeysHLayout.takeAt(0)
			if child.widget():
				child.widget().deleteLater()
						
		bar=self.ui.tabWidget.tabBar()
# 		label=QLabel("HOTKEYS:")
# 		label.setFixedWidth(bar.tabRect(0).width())
# 		self.ui.teamHotkeysHLayout.addWidget(label)
# 		icon = QIcon()
# 		icon.addPixmap(QPixmap(":/radiolog_ui/blank-computer-key.png"), QIcon.Normal, QIcon.Off)
# 		p=QPalette();
# 		p.setBrush(self.backgroundRole(),QBrush(QPixmap(":/radiolog_ui/blank-computer-key.png").scaled(30,30)))
		hotkeyRDict={v:k for k,v in self.hotkeyDict.items()}
# 		rprint("tab count="+str(bar.count()))
		for i in range(0,bar.count()):
			#  An apparent bug causes the tabButton (a label) to not have a text attrubite;
			#  so, use the whatsThis attribute instead.
			callsign=bar.tabWhatsThis(i)
			hotkey=hotkeyRDict.get(callsign,"")
			l=QLabel(hotkey)
			l.setFixedWidth(bar.tabRect(i).width())
# 			l.setStyleSheet("border:0px solid black;margin:0px;font-style:italic;font-size:14px;border-image:url(:/radiolog_ui/blank-computer-key.png) 0 0 30 30;")
			l.setStyleSheet("border:0px solid black;margin:0px;font-style:italic;font-size:14px;background-image:url(:/radiolog_ui/icons/blank-computer-key.png) 0 0 30 30;")
			l.setAlignment(Qt.AlignCenter)
# 			l.setPalette(p)
# 			w.setPixmap(QPixmap(":/radiolog_ui/blank-computer-key.png").scaled(30,30))
# 			l.setIconSize(QSize(30, 30))
			self.ui.teamHotkeysHLayout.addWidget(l)
		self.ui.teamHotkeysHLayout.addStretch()
		# #488: make sure standard hotkeys are re-enabled when last team tab is hidden
		if bar.count()<2:
			self.ui.teamHotkeysWidget.setVisible(False)
		
	def toggleTeamHotkeys(self):
		# #488: don't try to toggle team hotkeys when count is 0 or 1
		#  (the dummy tab will still exist after the only team tab has been hidden)
		#  (should also disable team hotkeys when all team tabs have been hidden)
		if self.ui.tabWidget.tabBar().count()<2:
			return
		vis=self.ui.teamHotkeysWidget.isVisible()
		if not vis:
			self.rebuildTeamHotkeys()
		self.ui.teamHotkeysWidget.setVisible(not vis)

	def openOpPeriodDialog(self):
		self.opPeriodDialog=opPeriodDialog(self)
		self.opPeriodDialog.show()

	def addNonRadioClue(self):
		self.newNonRadioClueDialog=nonRadioClueDialog(self,time.strftime("%H%M"),lastClueNumber+1)
		self.newNonRadioClueDialog.show()

	def restore(self):
		# use this function to reload the last saved files, based on lastFileName entry from resource file
		#  but, keep the new session's save filenames going forward
		if self.lastFileName=="NONE":
			self.crit1=QMessageBox(QMessageBox.Critical,"Cannot Restore","Last saved filenames were not saved in the resource file.  Cannot automatically restore last saved files.  You will need to load the files directly [F4].",
							QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			self.crit1.show()
			self.crit1.raise_()
			self.crit1.exec_()
			return
		# fileToLoad=self.firstWorkingDir+"\\"+self.lastFileName
		# fileToLoad=os.path.join(self.firstWorkingDir,self.lastFileName)
		fileToLoad=self.lastFileName # full filename with dir is saved in rc file
		# allSessionDirs=[os.path.join(self.firstWorkingDir,d) for d in os.listdir(self.firstWorkingDir) if os.path.isdir(os.path.join(self.firstWorkingDir,d))]
		# lastSessionDir=max(allSessionDirs,key=os.path.getmtime)
		if not os.path.isfile(fileToLoad): # prevent error if dialog is canceled
			self.crit2=QMessageBox(QMessageBox.Critical,"Cannot Restore","The file "+fileToLoad+" (specified in the resource file) does not exist.  You will need to load the files directly [F4].",
							QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			self.crit2.show()
			self.crit2.raise_()
			self.crit2.exec_()
			return
		rprint('Restoring previous session after unclean shutdown:')
		self.load(fileToLoad) # loads the radio log and the clue log
		# hide warnings about missing fleetsync file, since it does not get saved until clean shutdown time
		self.fsLoadLookup(fsFileName=fileToLoad.replace('.csv','_fleetsync.csv'),hideWarnings=True)
		self.updateFileNames()
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
		self.setFixedSize(self.size())
		

class optionsDialog(QDialog,Ui_optionsDialog):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.parent=parent
		self.ui=Ui_optionsDialog()
		self.ui.setupUi(self)
		self.ui.timeoutField.valueChanged.connect(self.displayTimeout)
		self.displayTimeout()
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
##		self.setAttribute(Qt.WA_DeleteOnClose)
		self.ui.datumField.setEnabled(False) # since convert menu is not working yet, TMG 4-8-15
		self.ui.formatField.setEnabled(False) # since convert menu is not working yet, TMG 4-8-15
		self.setFixedSize(self.size())
		self.secondWorkingDirCB()

	def showEvent(self,event):
		# clear focus from all fields, otherwise previously edited field gets focus on next show,
		# which could lead to accidental editing
		self.ui.incidentField.clearFocus()
		self.ui.datumField.clearFocus()
		self.ui.formatField.clearFocus()
		self.ui.timeoutField.clearFocus()
		self.ui.secondWorkingDirCheckBox.clearFocus()

	def displayTimeout(self):
		self.ui.timeoutLabel.setText("Timeout: "+timeoutDisplayList[self.ui.timeoutField.value()][0])
	
	def secondWorkingDirCB(self):
		self.parent.use2WD=self.ui.secondWorkingDirCheckBox.isChecked()

	def fsSendCB(self):
		self.parent.fsSendDialog.show()

	def accept(self):
		# only save the rc file when the options dialog is accepted interactively;
		#  saving from self.optionsAccepted causes errors because that function
		#  is called during init, before the values are ready to save
		self.parent.saveRcFile()
		super(optionsDialog,self).accept()

class printDialog(QDialog,Ui_printDialog):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.parent=parent
		self.ui=Ui_printDialog()
		self.ui.setupUi(self)
		self.ui.opPeriodComboBox.addItem(str(self.parent.opPeriod))
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		self.setFixedSize(self.size())

	def showEvent(self,event):
		rprint("show event called")
		rprint("teamNameList:"+str(self.parent.teamNameList))
		rprint("allTeamsList:"+str(self.parent.allTeamsList))
		if self.parent.exitClicked:
			self.ui.buttonBox.button(QDialogButtonBox.Ok).setText("Print")
			self.ui.buttonBox.button(QDialogButtonBox.Cancel).setText("Exit without printing")
		else:
			self.ui.buttonBox.button(QDialogButtonBox.Ok).setText("Ok")
			self.ui.buttonBox.button(QDialogButtonBox.Cancel).setText("Cancel")
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
# 			rprint("  printDialog.accept.clueLog.trace1")
			self.parent.printClueLog(opPeriod)
# 			rprint("  printDialog.accept.clueLog.trace2")
# 		rprint("  printDialog.accept.end.trace1")
		super(printDialog,self).accept()
# 		rprint("  printDialog.accept.end.trace2")

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
# 		rprint("tabCount="+str(tabCount)+" currentIndex="+str(currentIndex))
		if tabCount>2: # skip all this if 'NEWEST' and 'OLDEST' are the only tabs remaining
			if (tabCount-currentIndex)>1: # don't try to throb the 'OLDEST' label - it has no throb method
				currentWidget=self.ui.tabWidget.widget(currentIndex)
				if currentWidget.needsChangeCallsign:
					QTimer.singleShot(500,lambda:currentWidget.openChangeCallsignDialog())
				if throb:
					currentWidget.throb()

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
		else: # this should be fallback dead code since addTab is always called with a widget:
			self.parent.openNewEntry()

##	def clearHold(self):
##		self.entryHold=False
##
##	def clearContinue(self):
##		self.entryContinue=False

	def removeTab(self,caller):
		# rprint('removeTab called: caller='+str(caller))
		# determine the current index of the tab that owns the widget that called this function
		i=self.ui.tabWidget.indexOf(caller)
		# determine the number of tabs BEFORE removal of the tab in question
		count=self.ui.tabWidget.count()
		# rprint('  tab count before removal:'+str(count))
# 		rprint("removeTab: count="+str(count)+" i="+str(i))
		# remove that tab
		self.ui.tabWidget.removeTab(i)
		# activate the next tab upwards in the stack, if there is one
		if i>1:
			self.ui.tabWidget.setCurrentIndex(i-1)
		# otherwise, activate the tab at the bottom of the stack, if there is one
		elif i<count-3: # count-1 no longer exists; count-2="OLDEST"; count-3=bottom item of the stack
			self.ui.tabWidget.setCurrentIndex(count-3)

		if count<4: # hide the window (don't just lower - #504) if the stack is empty
			# rprint("lowering: count="+str(count))
			self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint) # disable always on top
			self.hide()

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
				# rprint("lastModAge:"+str(tab.lastModAge))
				# note the pause happens in newEntryWidget.updateTimer()
				if tab.ui.messageField.text()=="" and tab.lastModAge>60:
					rprint('  closing unused new entry widget for '+str(tab.ui.teamField.text())+' due to inactivity')
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
	def __init__(self,parent,sec=0,formattedLocString='',fleet='',dev='',origLocString='',amendFlag=False,amendRow=None,isMostRecentForCallsign=False):
		QDialog.__init__(self)

		self.ui=Ui_newEntryWidget()

		self.throbTimer=None
		self.amendFlag=amendFlag
		self.amendRow=amendRow
		self.attachedCallsignList=[]
##		self.position=position # dialog x,y to show at
		self.sec=sec
		self.formattedLocString=formattedLocString
		self.origLocString=origLocString
		self.fleet=fleet
		self.needsChangeCallsign=False # can be set to True by openNewEntry
		self.dev=dev
		self.parent=parent
		self.isMostRecentForCallsign=isMostRecentForCallsign
		if amendFlag:
			row=parent.radioLog[amendRow]
			self.sec=row[6]
			self.formattedLocString=row[4]
##		newEntryDialog.newEntryDialogUsedPositionList[self.position]=True
		newEntryWidget.instances.append(self)
		self.ui.setupUi(self)

		# blank-out the label under the callsign field if this was a manually / hotkey
		#  generated newEntryWidget; the label only applies to fleetsync-spawned entries
		if not fleet:
			self.ui.label_2.setText("")

		self.setAttribute(Qt.WA_DeleteOnClose) # so that closeEvent gets called when closed by GUI
		self.palette=QPalette()
		self.setAutoFillBackground(True)
		self.clueDialogOpen=False # only allow one clue dialog at a time per newEntryWidget
		self.subjectLocatedDialogOpen=False

# 		rprint(" new entry widget opened.  allteamslist:"+str(self.parent.allTeamsList))
		if len(self.parent.allTeamsList)<2:
			self.ui.teamComboBox.setEnabled(False)
		else:
			self.ui.teamComboBox.clear()
			for team in self.parent.allTeamsList:
				if team!='dummy':
					self.ui.teamComboBox.addItem(team)
		
##		# close and accept the dialog as a new entry if message is no user input for 30 seconds

##		QTimer.singleShot(100,lambda:self.changeBackgroundColor(0))

# 		rprint("newEntryWidget created")
		self.quickTextAddedStack=[]

		self.childDialogs=[] # keep track of exactly which clueDialog or
		  # subjectLocatedDialogs are 'owned' by this NED, for use in closeEvent
		  
##		self.ui.messageField.setToolTip("<table><tr><td>a<td>b<tr><td>c<td>d</table>")
		if amendFlag:
			self.ui.timeField.setText(row[0])
			self.ui.teamField.setText(row[2])
			if row[1]=="TO":
				self.ui.to_fromField.setCurrentIndex(1)
			oldMsg=row[3]
			amendIndex=oldMsg.find('\n[AMENDED')
			if amendIndex>-1:
				self.ui.messageField.setText(row[3][:amendIndex])
			else:
				self.ui.messageField.setText(row[3])
			self.ui.label.setText("AMENDED Message:")
			if not self.isMostRecentForCallsign:
				# #508 - it would be nice to show a warning when a status button is clicked,
				#   but that has some complexity - easier to just disable the group box,
				#   though we can't then catch a button click in that area to show a warning
				#   without installing an event filter https://stackoverflow.com/questions/8467527
				self.ui.statusGroupBox.setEnabled(False)
		else:
			self.ui.timeField.setText(time.strftime("%H%M"))

		# #508 - keep track of status changes while typing
		self.tmpNewStatus=None

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
# 		rprint("clueLog.openDialogCount="+str(clueDialog.openDialogCount))
# 		rprint("changeCallsignDialog.openDialogCount="+str(changeCallsignDialog.openDialogCount))
# 		rprint("subjectLocatedDialog.openDialogCount="+str(subjectLocatedDialog.openDialogCount))
# 		rprint("showing")
		if not self.parent.newEntryWindow.isVisible():
			self.parent.newEntryWindow.show()
# 		self.parent.newEntryWindow.setFocus()
		if clueDialog.openDialogCount==0 and subjectLocatedDialog.openDialogCount==0 and changeCallsignDialog.openDialogCount==0:
# 			rprint("raising")
			self.parent.newEntryWindow.raise_()
		# the following line is needed to get fix the apparent Qt bug (?) that causes
		#  the messageField text to all be selected when a new message comes in
		#  during the continue period.
		self.parent.newEntryWindow.ui.tabWidget.currentWidget().ui.messageField.deselect()

		self.timer=QTimer(self)
		self.timer.start(1000)
		self.timer.timeout.connect(self.updateTimer)
		
		self.relayed=None
		# store field values in case relayed checkbox is toggled accidentally
		self.relayedByTypedTemp=None
		self.relayedByTemp=None
		self.callsignTemp=None
		self.radioLocTemp=None
		self.datumFormatTemp=None
		
		self.ui.relayedByComboBox.lineEdit().editingFinished.connect(self.relayedByComboBoxChanged)

		# #502 - if amending, call setStatusFromTeam - otherwise it is only called by typing in the callsign field
		if self.amendFlag:
			self.setStatusFromTeam()

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
# 		rprint("throb:n="+str(n))
		self.palette.setColor(QPalette.Background,QColor(n*10,n*10,255))
		self.setPalette(self.palette)
		if n<25:
			#fix #333: make throbTimer a normal timer and then call throbTimer.setSingleShot,
			# so we can just stop it using .stop() when the widget is closed
			# to avert 'wrapped C/C++ object .. has been deleted'
# 			self.throbTimer=QTimer.singleShot(15,lambda:self.throb(n+1))
			self.throbTimer=QTimer()
			self.throbTimer.timeout.connect(lambda:self.throb(n+1))
			self.throbTimer.setSingleShot(True)
			self.throbTimer.start(15)
		else:
# 			rprint("throb complete")
			self.throbTimer=None
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
# 		rprint("resetting last mod age for "+self.ui.teamField.text())
		self.lastModAge=-1
		self.parent.currentEntryLastModAge=self.lastModAge

	def quickTextAction(self):
		quickText=self.sender().text()
# 		rprint("  quickTextAction called: text="+str(quickText))
		quickText=re.sub(r' +\[.*$','',quickText) # prune one or more spaces followed by open bracket, thru end
		existingText=self.ui.messageField.text()
		if existingText=="":
			textToAdd=quickText
		elif existingText.endswith("]"):
			textToAdd=" "+quickText
		elif existingText.endswith("] "):
			textToAdd=quickText
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
			self.newClueDialog=clueDialog(self,self.ui.timeField.text(),self.ui.teamField.text(),self.ui.radioLocField.toPlainText(),lastClueNumber+1)
			self.newClueDialog.show()

	def quickTextSubjectLocatedAction(self):
		self.subjectLocatedDialog=subjectLocatedDialog(self,self.ui.timeField.text(),self.ui.teamField.text(),self.ui.radioLocField.toPlainText())
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
		elif key==Qt.Key_Escape:
			# need to force focus away from callsignField so that
			#  callsignLostFocus gets called, to keep callsign and tab name in sync,
			#  otherwise this will cause a crash (hitting the cancel button does
			#  not cause a crash because the button takes focus before closing)
			self.ui.messageField.setFocus()
			self.close()
		else:
			super().keyPressEvent(event) # pass the event as normal

	def openChangeCallsignDialog(self):
		# problem: changeCallsignDialog does not stay on top of newEntryWindow!
		# only open the dialog if the newEntryWidget was created from an incoming fleetSync ID
		#  (it has no meaning for hotkey-opened newEntryWidgets)
		self.needsChangeCallsign=False
		if self.fleet:
			self.changeCallsignDialog=changeCallsignDialog(self,self.ui.teamField.text(),self.fleet,self.dev)
			self.changeCallsignDialog.exec_() # required to make it stay on top

	def accept(self):
		if not self.clueDialogOpen and not self.subjectLocatedDialogOpen:
			# getValues return value: [time,to_from,team,message,self.formattedLocString,status,self.sec,self.fleet,self.dev,self.origLocString]
			rprint("Accepted")
			val=self.getValues()
			
			# validation: callsign field must be non-blank
			vText=""
			if val[2]=="":
				vText+="\nCallsign cannot be blank."
			rprint("vText:"+vText)
			if vText!="":
				self.entryMsgBox=QMessageBox(QMessageBox.Critical,"Error","Please complete the form and try again:\n"+vText,
					QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
				self.entryMsgBox.show()
				self.entryMsgBox.raise_()
				self.entryMsgBox.exec_()
				return
				
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
				self.parent.newEntryProcessTeam(niceTeamName,status,"AMEND","",self.amendFlag)
				
				# reapply the filter on team tables, in case callsign was changed
				for t in self.parent.ui.tableViewList[1:]:
					t.model().invalidateFilter()
			else:
				self.parent.newEntry(self.getValues(),self.amendFlag)
	
			# make entries for attached callsigns
			# values array format: [time,to_from,team,message,locString,status,sec,fleet,dev]
# 			rprint("attached callsigns: "+str(self.attachedCallsignList))
			for attachedCallsign in self.attachedCallsignList:
				v=val[:] # v is a fresh, independent copy of val for each iteration
				v[2]=getNiceTeamName(attachedCallsign)
				v[3]="[ATTACHED FROM "+self.ui.teamField.text().strip()+"] "+val[3]
				self.parent.newEntry(v,self.amendFlag)
	
			self.parent.totalEntryCount+=1
			if self.parent.totalEntryCount%5==0:
				# rotate backup files after every 5 entries, but note the actual
				#  entry interval could be off during fast entries since the
				#  rotate script is called asynchronously (i.e. backgrounded)
				filesToBackup=[
						os.path.join(self.parent.sessionDir,self.parent.csvFileName),
						os.path.join(self.parent.sessionDir,self.parent.csvFileName.replace(".csv","_clueLog.csv")),
						os.path.join(self.parent.sessionDir,self.parent.fsFileName)]
				if self.parent.use2WD and self.parent.secondWorkingDir:
					filesToBackup=filesToBackup+[
							os.path.join(self.parent.secondWorkingDir,self.parent.csvFileName),
							os.path.join(self.parent.secondWorkingDir,self.parent.csvFileName.replace(".csv","_clueLog.csv")),
							os.path.join(self.parent.secondWorkingDir,self.parent.fsFileName)]
				self.parent.rotateCsvBackups(filesToBackup)	
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
		# fix #325: repeated cancel-confirm cycles are annoying; bypass the
		#  confirmation if the message is blank; note that any GPS data gets sent
		#  as soon as the dialog is opened (or as soon as the change callsign dialog
		#  is accepted), so, bypassing the confirmation in this manner will
		#  still preserve and process any incoming GPS coordinates
		if not accepted and not force and self.ui.messageField.text()!="":
			msg="Cancel this entry?\nIt cannot be recovered."
			if self.amendFlag:
				msg="Cancel this amendment?\nOriginal message will be preserved."
			self.really1=QMessageBox(QMessageBox.Warning,"Please Confirm",msg,
				QMessageBox.Yes|QMessageBox.No,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			self.really1.setDefaultButton(QMessageBox.No)
			self.really1.show()
			self.really1.raise_()
			if self.really1.exec_()==QMessageBox.No:
				event.ignore()
				return
		# whether OK or Cancel, ignore the event if child dialog(s) are open,
		#  and raise the child window(s)
		if self.clueDialogOpen or self.subjectLocatedDialogOpen:
			warn=QMessageBox(QMessageBox.Warning,"Cannot close","A Clue Report or Subject Located form is open that belongs to this entry.  Finish it first.",
							QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			# the 'child' dialogs are not technically children; use the NED's
			#  childDialogs attribute instead, which was populated in the __init__
			#  of each child dialog class
			for child in self.childDialogs:
				child.raise_()
			warn.show()
			warn.raise_()
			warn.exec_() # make sure it's modal
			event.ignore()
			return
		else:
			# rprint('newEntryWidget.closeEvent t3')
			self.timer.stop()
			# fix #333: stop mid-throb to avert runtime error
			#  but only if the throbTimer was actually started
			if self.throbTimer:
				self.throbTimer.stop()
			# if there is a pending GET request (locator), send it now with the
			#  specified callsign
			self.parent.sendPendingGet(self.ui.teamField.text())
	##		self.parent.newEntryWindow.ui.tabWidget.removeTab(self.parent.newEntryWindow.ui.tabWidget.indexOf(self))
	##		self.parent.newEntryWindow.removeTab(self.parent.newEntryWindow.ui.tabWidget.indexOf(self))
			self.parent.newEntryWindow.removeTab(self)
			newEntryWidget.instances.remove(self)
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

	def teamFieldTextChanged(self):
		pass # no longer needed due to better post-edit checking 

	def teamFieldEditingFinished(self):
		cs=re.sub(r' +',r' ',self.ui.teamField.text()).strip() # remove leading and trailing spaces, and reduce chains of spaces to single space
		# rprint('teamFieldEditingFinished: cs="'+cs+'"')
		if not cs in self.parent.allTeamsList: # if not already an exact case-sensitive match for an existing callsign:
			if re.match(".*\D.*",cs): # if there are any characters that are not numbers
				# change it to any case-insensitive-matching existing callsign
				for t in self.parent.allTeamsList:
					if t.upper()==cs.upper() or t.upper()==cs.upper().replace('T','TEAM'):
						self.ui.teamField.setText(t)
						break
			else: # only numbers - see if 'Team ' followed by that number (case-insensitive) is an existing callsign
				found=False
				for t in self.parent.allTeamsList:
					if t.upper()=='TEAM '+cs:
						self.ui.teamField.setText(t)
						found=True
						break
				if not found:
					self.ui.teamField.setText('Team '+cs)
		if re.match(".*relay.*",cs,re.IGNORECASE):
			rprint("relay callsign detected")
			# if the relay callsign is already in the callsign list, i.e. if
			#  they have previously called in, then assume they are relaying
			#  a message; if not, assume they are not yet relaying a message
			for t in self.parent.allTeamsList:
				if t.upper()==cs.upper():
					self.ui.relayedCheckBox.setChecked(True)
					self.ui.relayedByComboBox.setCurrentText(t)
					break

	def setRelayedPrefix(self,relayedBy=None):
		if relayedBy is None:
			relayedBy=self.ui.relayedByComboBox.currentText()
# 		rprint("setRelayedPrefix:"+relayedBy)
		if relayedBy=="":
			if self.relayed:
				prefix="[RELAYED] "
			else:
				prefix=""
		else:
			prefix="[RELAYED by "+relayedBy+"] "
		mt=self.ui.messageField.text()
		if mt.startswith("[RELAYED"):
			relayedEndIndex=mt.find("]")
# 			rprint("before relayed prefix removal:"+mt)
			mt=mt.replace(mt[:relayedEndIndex+2],"")
# 			rprint("after relayed prefix removal:"+mt)
		mt=prefix+mt
		self.ui.messageField.setText(mt)			
	
	def getRelayedByItems(self):
		items=[]
		for n in range(self.ui.relayedByComboBox.count()):
			items.append(self.ui.relayedByComboBox.itemText(n))
		return items
		
	def relayedCheckBoxStateChanged(self):
		# if this was a fleetsync call, move the incoming callsign to 'relayed by'
		#  and set focus to the callsign field to prompt for the callsign of the
		#  originating team/unit
		# if it was not a fleetsync call, leave the callsign alone and set 'relayed by'
		#  to blank, since it's likely that the radio operator may have typed the
		#  originating team/unit callsign in to the callsign field first, and then
		#  checked 'relayed' afterwards
		rprint("relayedCheckBoxStateChanged; fleet="+str(self.fleet)+"; dev="+str(self.dev))
		self.relayed=self.ui.relayedCheckBox.isChecked()
		self.ui.relayedByLabel.setEnabled(self.relayed)
		self.ui.relayedByComboBox.setEnabled(self.relayed)
		self.ui.relayedByComboBox.clear() # rebuild the list from scratch to avoid duplicates
		if self.relayed: # do these steps regardless of whether it was a fleetsync call
			for team in self.parent.allTeamsList:
				if team!='dummy':
					self.ui.relayedByComboBox.addItem(team)
			# remove the current callsign from the list of 'relayed by' choices
			for n in range(self.ui.relayedByComboBox.count()):
				if self.ui.relayedByComboBox.itemText(n).lower()==self.ui.teamField.text().lower():
					self.ui.relayedByComboBox.removeItem(n)
					break	
			self.ui.relayedCheckBox.setText("Relayed")
			if self.relayedByTypedTemp is not None:
				self.ui.relayedByComboBox.setCurrentText(self.relayedByTypedTemp)
		else: # just unchecked the box, regadless of fleetsync
			text=self.ui.relayedByComboBox.currentText()
			if text!="" and text not in self.getRelayedByItems():
				self.relayedByTypedTemp=text
			self.ui.relayedByComboBox.setCurrentText("")
		if self.dev is not None: # only do these steps if it was a fleetsync call
			if self.relayed:
				# store field values in case this was inadvertently checked
				self.callsignTemp=self.ui.teamField.text()
				self.radioLocTemp=self.ui.radioLocField.toPlainText()
				self.datumFormatTemp=self.ui.datumFormatLabel.text()
				self.ui.radioLocField.setText("")
				self.ui.datumFormatLabel.setText("")
	# 			rprint("relayed")
				self.ui.relayedByComboBox.clear()
				cs=self.ui.teamField.text()
				if self.relayedByTemp is not None:
					self.ui.relayedByComboBox.setCurrentText(self.relayedByTemp)
				elif cs!="":
					self.ui.relayedByComboBox.setCurrentText(cs)
				self.ui.teamField.setText("")
				# need to 'burp' the focus to prevent two blinking cursors
				#  see http://stackoverflow.com/questions/42475602
				self.ui.messageField.setFocus()
				self.ui.teamField.setFocus()
			else:
	# 			rprint("not relayed")
				# store field values in case this was inadvertently checked
				self.relayedByTemp=self.ui.relayedByComboBox.currentText()
				self.ui.relayedCheckBox.setText("Relayed?")
				if self.callsignTemp is not None:
					self.ui.teamField.setText(self.callsignTemp)
				else:
					self.ui.teamField.setText(self.ui.relayedByComboBox.currentText())
				if self.radioLocTemp is not None:
					self.ui.radioLocField.setText(self.radioLocTemp)
				if self.datumFormatTemp is not None:
					self.ui.datumFormatLabel.setText(self.datumFormatTemp)
				self.ui.relayedByComboBox.clear()
				self.ui.messageField.setFocus()
		self.setRelayedPrefix()
	
	def relayedByComboBoxChanged(self):
		rprint("relayedByComboBoxChanged")
		self.relayedBy=self.ui.relayedByComboBox.currentText()
		self.setRelayedPrefix(self.relayedBy)
		self.ui.messageField.setFocus()
			
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
		
		# multiple things have to be in place to have a new status text here actually
		#  change the status of the new entry:
		# 1. button with matching text() must exist in newEntryWidget and must
		#     be a member of statusButtonGroup (it can be behind another button
		#     so that it never gets clicked and is not visible, but, it must exist)
		# 2. the clicked() signal from that button must have a reciever of
		#     newEntryWidget.quickTextAction()
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
		elif "10-8" in message:
			newStatus="Available"
		elif "10-97" in message:
			newStatus="Working"
		elif "10-10" in message:
			newStatus="Off Duty"
		elif prevStatus=="Available" and "evac" in message:
			newStatus="In Transit"
		else:
			newStatus=prevStatus
		
# 		rprint("message:"+str(message))
# 		rprint("  previous status:"+str(prevStatus)+"  newStatus:"+str(newStatus))
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
# 	# 			rprint(" 'with' tail found:"+tail)
# 				tailParse=re.split("[, ]+",tail)
# 				# rebuild the attachedCallsignList from scratch on every keystroke;
# 				#  trying to append to the list is problematic (i.e. when do we append?)
# 				for token in tailParse:
# 					if token!="and": # all parsed tokens other than "and" are callsigns to be attached
# 						# keep the list as a local variable rather than object attribute,
# 						#  since we want to rebuild the entire list on every keystroke
# 						self.attachedCallsignList.append(token)
# 		self.ui.attachedField.setText(" ".join(self.attachedCallsignList))
# 		
		# #508 - initialize tmpNewStatus based on the text of the message being amended, not based on the team's current status
		if not self.tmpNewStatus:
			self.tmpNewStatus=prevStatus	
		if newStatus!=prevStatus:
			# rprint('newStatus='+newStatus+'  prevStatus='+prevStatus+'  tmpNewStatus='+str(self.tmpNewStatus))
			# #508 - disable status change based on text, and show a warning, if this is an amendment
			#  for an older (not the most recent) message for the callsign
			if (not self.amendFlag) or self.isMostRecentForCallsign:
				# allow it to be set back to blank; must set exclusive to false and iterate over each button
				self.ui.statusButtonGroup.setExclusive(False)
				for button in self.ui.statusButtonGroup.buttons():
		# 			rprint("checking button: "+button.text())
					if button.text()==newStatus:
						button.setChecked(True)
					else:
						button.setChecked(False)
				self.ui.statusButtonGroup.setExclusive(True)
			else:
				# #508 - don't show a warning on every keystroke - just once per relevant text change
				if newStatus!=self.tmpNewStatus:
					self.warnNoStatusChange()
					# rprint('setting tmpNewStatus to '+newStatus)
					self.tmpNewStatus=newStatus
		self.ui.messageField.deselect()

	def warnNoStatusChange(self):
		box=QMessageBox(QMessageBox.Warning,"Warning","For safety reasons, changing the status from an older message (not the most recent message for this callsign) is disabled.\n\nTo change the status right now, you would need to create a new entry, or amend the most recent entry for this callsign.",
			QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
		box.show()
		box.raise_()
		box.exec_()

	def setCallsignFromComboBox(self,str):
		self.ui.teamField.setText(str)
		self.ui.teamField.setFocus()
		
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
		# fix #459 (and other places in the code): remove all leading and trailing spaces, and change all chains of spaces to one space
		team=re.sub(r' +',r' ',self.ui.teamField.text()).strip()
		message=self.ui.messageField.text()
		if self.relayed:
			locString=""
		else:
			locString=self.formattedLocString
#		location=self.ui.radioLocField.text()
		status=''
		if self.ui.statusButtonGroup.checkedButton()!=None:
			status=self.ui.statusButtonGroup.checkedButton().text()
		return [time,to_from,team,message,locString,status,self.sec,self.fleet,self.dev,self.origLocString]


class clueDialog(QDialog,Ui_clueDialog):
##	instances=[]
	openDialogCount=0
	indices=[False]*20 # allow up to 20 clue dialogs open at the same time
	dx=20
	dy=20
	x0=200
	y0=200
	# max length values determined by trial and error with a generated PDF
	descriptionMaxLength=270
	locationMaxLength=200
	def __init__(self,parent,t,callsign,radioLoc,newClueNumber):
		QDialog.__init__(self)
		self.ui=Ui_clueDialog()
		self.ui.setupUi(self)
		self.ui.timeField.setText(t)
		self.ui.dateField.setText(time.strftime("%x"))
		self.ui.callsignField.setText(callsign)
		self.ui.radioLocField.setText(re.sub(' +','\n',radioLoc))
		self.ui.clueNumberField.setText(str(newClueNumber))
		self.clueQuickTextAddedStack=[]
		self.parent=parent
		self.parent.childDialogs.append(self)
##		self.parent.timer.stop() # do not timeout the new entry dialog if it has a child clueDialog open!
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
##		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setAttribute(Qt.WA_DeleteOnClose)

		# set max length to prevent text overrun in generated pdf
		# based on https://stackoverflow.com/a/46550977/3577105
		self.ui.descriptionField.textChanged.connect(self.descriptionTextChanged)
		# for locationField, we could use maxLength or setValidator since it's a QLineEdit, but that lacks audio and visual feedback
		self.ui.locationField.textChanged.connect(self.locationTextChanged)

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
		amendText=''
		amendText2=''
		if self.parent.amendFlag:
			amendText=' during amendment of previous message'
			amendText2=', which will appear with that amended message when completed'
		self.values[3]="RADIO LOG SOFTWARE: 'LOCATED A CLUE' button pressed"+amendText+"; radio operator is gathering details"+amendText2
##		self.values[3]="RADIO LOG SOFTWARE: 'LOCATED A CLUE' button pressed for '"+self.values[2]+"'; radio operator is gathering details"
##		self.values[2]='' # this message is not actually from a team
		self.parent.parent.newEntry(self.values)
		self.setFixedSize(self.size())
		self.descriptionTooLongHasBeenShown=False
		self.locationTooLongHasBeenShown=False

	def descriptionTextChanged(self):
		text=self.ui.descriptionField.toPlainText()
		if len(text)>clueDialog.descriptionMaxLength:
			self.ui.descriptionField.setPlainText(text[:clueDialog.descriptionMaxLength])
			cursor=self.ui.descriptionField.textCursor()
			cursor.setPosition(clueDialog.descriptionMaxLength)
			self.ui.descriptionField.setTextCursor(cursor)
			if not self.descriptionTooLongHasBeenShown: # only show the message box once per clue
				box=QMessageBox(QMessageBox.Warning,"Warning","You've reached the maximum clue description length.  Consider changing the description to 'see attached' then adding additional notes by hand after the clue form is printed.",
					QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
				box.show()
				box.raise_()
				box.exec_()
				self.descriptionTooLongHasBeenShown=True
			else:
				QApplication.beep()

	def locationTextChanged(self):
		text=self.ui.locationField.text()
		if len(text)>clueDialog.locationMaxLength:
			self.ui.locationField.setText(text[:clueDialog.locationMaxLength])
			self.ui.locationField.setCursorPosition(clueDialog.locationMaxLength)
			if not self.locationTooLongHasBeenShown: # only show the message box once per clue
				box=QMessageBox(QMessageBox.Warning,"Warning","You've reached the maximum clue location length.  Consider changing the location to 'see attached' then adding additional notes by hand after the clue form is printed.",
					QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
				box.show()
				box.raise_()
				box.exec_()
				self.locationTooLongHasBeenShown=True
			else:
				QApplication.beep()

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
			# fix issue #338: prevent 'esc' from closing the newEntryWindow
			if event.key()!=Qt.Key_Escape:
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
		radioLoc=self.ui.radioLocField.toPlainText()

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
				QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			self.clueMsgBox.show()
			self.clueMsgBox.raise_()
			self.clueMsgBox.exec_()
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
				QMessageBox.Yes|QMessageBox.No,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			if really.exec_()==QMessageBox.No:
				event.ignore()
				return
			if clueDialog.openDialogCount==1:
				global lastClueNumber
				lastClueNumber=lastClueNumber-1 # only release the clue# if no other clue forms are open
			self.values=self.parent.getValues()
			amendText=''
			if self.parent.amendFlag:
				amendText=' during amendment of previous message'
			self.values[3]="RADIO LOG SOFTWARE: radio operator has canceled the 'LOCATED A CLUE' form"+amendText
			self.parent.parent.newEntry(self.values)
		
		clueDialog.indices[self.i]=False # free up the dialog box location for the next one
		self.parent.clueDialogOpen=False
		clueDialog.openDialogCount-=1
		self.parent.childDialogs.remove(self)
		event.accept()
		if accepted:
			self.parent.accept()
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
		self.setFixedSize(self.size())
		
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
				QMessageBox.Yes|QMessageBox.No,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			really.setDefaultButton(QMessageBox.No)
			if really.exec_()==QMessageBox.No:
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
		self.ui.tableView.setModel(self.tableModel)

		self.ui.tableView.verticalHeader().setVisible(True)
		self.ui.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
		self.ui.tableView.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

		# automatically expand the 'description' and 'instructions' column widths to fill available space and wrap if needed
		self.ui.tableView.horizontalHeader().setSectionResizeMode(1,QHeaderView.Stretch)
		self.ui.tableView.horizontalHeader().setSectionResizeMode(7,QHeaderView.Stretch)

		self.ui.tableView.verticalHeader().sectionClicked.connect(self.headerClicked)
		self.ui.addNonRadioClueButton.clicked.connect(self.parent.addNonRadioClue)
		self.ui.printButton.clicked.connect(self.printClueLogCB)

		self.ui.tableView.setSelectionMode(QAbstractItemView.NoSelection)
		self.ui.tableView.setFocusPolicy(Qt.NoFocus)

	def showEvent(self,event):
		self.ui.tableView.resizeRowsToContents()
		self.ui.tableView.scrollToBottom()
		self.ui.tableView.setStyleSheet("font-size:"+str(self.parent.limitedFontSize)+"pt")

	def resizeEvent(self,event):
		self.ui.tableView.resizeRowsToContents()
		self.ui.tableView.scrollToBottom()

	def headerClicked(self,section):
		clueData=self.parent.clueLog[section]
		clueNum=clueData[0]
		if clueNum!="": # pass through if clicking a non-clue row
			q=QMessageBox(QMessageBox.Question,"Confirm - Print Clue Report","Print Clue Report for Clue #"+str(clueNum)+"?",
						QMessageBox.Yes|QMessageBox.Cancel,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			q.show()
			q.raise_()
			if q.exec_()==QMessageBox.Yes:
				self.parent.printClueReport(clueData)
				
	def printClueLogCB(self):
		self.parent.opsWithClues=sorted(list(set([str(clue[5]) for clue in self.parent.clueLog if str(clue[5])!=""])))
		if len(self.parent.opsWithClues)==0:
			crit=QMessageBox(QMessageBox.Critical,"No Clues to Print","There are no clues to print.",QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			crit.show()
			crit.raise_()
			crit.exec_()
		else:
			self.parent.printClueLogDialog.show()


class subjectLocatedDialog(QDialog,Ui_subjectLocatedDialog):
	openDialogCount=0
	def __init__(self,parent,t,callsign,radioLoc):
		QDialog.__init__(self)
		self.ui=Ui_subjectLocatedDialog()
		self.ui.setupUi(self)
		self.ui.timeField.setText(t)
		self.ui.dateField.setText(time.strftime("%x"))
		self.ui.callsignField.setText(callsign)
		self.ui.radioLocField.setText(re.sub(' +','\n',radioLoc))
		self.parent=parent
		self.parent.subjectLocatedDialogOpen=True
		self.parent.childDialogs.append(self)
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.ui.locationField.setFocus()
		self.values=self.parent.getValues()
		amendText=''
		amendText2=''
		if self.parent.amendFlag:
			amendText=' during amendment of previous message'
			amendText2=', which will appear with that amended message when completed'
		self.values[3]="RADIO LOG SOFTWARE: 'SUBJECT LOCATED' button pressed"+amendText+"; radio operator is gathering details"+amendText2
		self.parent.parent.newEntry(self.values)
		subjectLocatedDialog.openDialogCount+=1
		self.setFixedSize(self.size())

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
			self.subjectMsgBox=QMessageBox(QMessageBox.Critical,"Error","Please complete the form and try again:\n"+vText,
				QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			self.subjectMsgBox.show()
			self.subjectMsgBox.raise_()
			self.subjectMsgBox.exec_()
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
				QMessageBox.Yes|QMessageBox.No,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			if really.exec_()==QMessageBox.No:
				event.ignore()
				return
			self.values=self.parent.getValues()
			amendText=''
			if self.parent.amendFlag:
				amendText=' during amendment of previous message'
			self.values[3]="RADIO LOG SOFTWARE: radio operator has canceled the 'SUBJECT LOCATED' form"+amendText
			self.parent.parent.newEntry(self.values)
		self.parent.subjectLocatedDialogOpen=False
		subjectLocatedDialog.openDialogCount-=1
		self.parent.childDialogs.remove(self)
		if accepted:
			self.parent.accept()

	# fix issue #338: prevent 'esc' from closing the newEntryWindow
	def keyPressEvent(self,event):
		if event.key()!=Qt.Key_Escape:
			super().keyPressEvent(event) # pass the event as normal

class printClueLogDialog(QDialog,Ui_printClueLogDialog):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.ui=Ui_printClueLogDialog()
		self.ui.setupUi(self)
		self.parent=parent
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)

	def showEvent(self,event):
		itemsToAdd=self.parent.opsWithClues
		if len(itemsToAdd)==0:
			itemsToAdd=['--']
		self.ui.opPeriodComboBox.clear()
		self.ui.opPeriodComboBox.addItems(itemsToAdd)

	def accept(self):
		opPeriod=self.ui.opPeriodComboBox.currentText()
		rprint("  printClueLogDialog.accept.trace1")
		if opPeriod=='--':
			crit=QMessageBox(QMessageBox.Critical,"No Clues to Print","There are no clues to print.",QMessageBox.Ok,self.parent,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			crit.show()
			crit.raise_()
			crit.exec_()
			self.reject()
		else:
			self.parent.printClueLog(opPeriod)
			rprint("  printClueLogDialog.accept.trace2")
			super(printClueLogDialog,self).accept()
			rprint("  printClueLogDialog.accept.trace3")

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
		self.setFixedSize(self.size())

	def accept(self):
		if self.ui.printCheckBox.isChecked():
			self.parent.printDialog.exec_() # instead of show(), to pause execution until the print dialog is closed

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

# allow different justifications for different columns of qtableview
# from https://stackoverflow.com/a/52644764
from PyQt5 import QtCore,QtWidgets
class alignCenterDelegate(QtWidgets.QStyledItemDelegate):
	def initStyleOption(self,option,index):
		super(alignCenterDelegate,self).initStyleOption(option,index)
		option.displayAlignment=QtCore.Qt.AlignCenter

class continuedIncidentDialog(QDialog,Ui_continuedIncidentDialog):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.ui=Ui_continuedIncidentDialog()
		self.ui.setupUi(self)
		self.parent=parent
		self.incidentNameCandidate=''
		self.lastOPCandidate=0
		self.lastClueCandidate=0
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		ciwd=self.parent.continuedIncidentWindowDays
		if ciwd==1:
			dayText='day'
		else:
			dayText=str(ciwd)+' days'
		self.ui.instructionsLabel.setText('If so, select a row from the following list of radiolog sessions that were run on this computer within the last '+dayText+', then click YES.')
		self.ui.theTable.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
		# automatically expand the 'Incident name' column width to fill available space
		self.ui.theTable.horizontalHeader().setSectionResizeMode(0,QHeaderView.Stretch)
		centerDelegate=alignCenterDelegate(self.ui.theTable)
		self.ui.theTable.setItemDelegateForColumn(1,centerDelegate)
		self.ui.theTable.setItemDelegateForColumn(2,centerDelegate)
		self.ui.theTable.setItemDelegateForColumn(3,centerDelegate)
		# clearFocus doesn't remove the focus rectangle from the top-left cell unless
		#  there is a half second delay (singleshot) before callig it, but changing
		#  the focus to something else does remove the focus rectangle immediately
		self.ui.noButton.setFocus()
		# self.setFixedSize(self.size())

	def accept(self): # YES is clicked
		self.parent.isContinuedIncident=True
		self.parent.incidentName=self.incidentNameCandidate
		self.parent.optionsDialog.ui.incidentField.setText(self.parent.incidentName)
		global lastClueNumber
		lastClueNumber=self.lastClueCandidate
		self.parent.opPeriod=self.lastOPCandidate+1
		self.parent.ui.opPeriodButton.setText("OP "+str(self.parent.opPeriod))
		# radiolog entry and clue log entry are made by init code based on values set here
		self.parent.printDialog.ui.opPeriodComboBox.setItemText(0,str(self.parent.opPeriod))
		self.changed=False
		super(continuedIncidentDialog,self).accept()

	def reject(self): # NO is clicked
		super(continuedIncidentDialog,self).reject()

	# toggle selection behavior is actually a bit tricky;
	#  the next three functions correspond to the same-named signals
	#  and work together to keep track of whether the clicked cell
	#  was already selected; other signals don't fire in the needed sequence
	def cellClicked(self,row,col):
		# rprint('row clicked:'+str(row))
		# rprint('  selected row:'+str(self.ui.theTable.selectedIndexes()[0].row()))
		if self.changed:
			self.ui.yesButton.setEnabled(True)
			self.incidentNameCandidate=self.ui.theTable.item(row,0).text()
			self.lastOPCandidate=self.ui.theTable.item(row,1).text()
			if self.lastOPCandidate.isnumeric():
				self.lastOPCandidate=int(self.lastOPCandidate)
			else:
				self.lastOPCandidate=1
			self.lastClueCandidate=self.ui.theTable.item(row,2).text()
			if self.lastClueCandidate.isnumeric():
				self.lastClueCandidate=int(self.lastClueCandidate)
			else:
				self.lastClueCandidate=0
			self.ui.yesButton.setText('YES: Start a new OP of "'+self.incidentNameCandidate+'"\n(OP = '+str(self.lastOPCandidate+1)+'; next clue# = '+str(self.lastClueCandidate+1)+')')
			self.ui.yesButton.setDefault(True)
			self.changed=False
		else:
			self.ui.theTable.clearSelection()
			self.ui.noButton.setDefault(True)
			self.ui.yesButton.setEnabled(False)
			self.ui.theTable.clearFocus() # to remove the focus rectangle

	def currentCellChanged(self,r1,c1,r2,c2):
		# rprint('r1={} c1={}   r2={} c2={}'.format(r1,c1,r2,c2))
		self.changed=True

	def clicked(self,i):
		# rprint('clicked row: '+str(i.row()))
		si=self.ui.theTable.selectedIndexes()
		if not si: # clicked when already unselected; select it again
			# rprint('  no row selected when clicked event called')
			self.changed=True
		# else:
			# rprint('  selected row:'+str(self.ui.theTable.selectedIndexes()[0].row()))

class loadDialog(QDialog,Ui_loadDialog):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.ui=Ui_loadDialog()
		self.ui.setupUi(self)
		self.parent=parent
		self.setAttribute(Qt.WA_DeleteOnClose)
		# self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		self.ui.theTable.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
		# automatically expand the 'Incident name' column width to fill available space
		self.ui.theTable.horizontalHeader().setSectionResizeMode(0,QHeaderView.Stretch)
		self.ui.theTable.horizontalHeader().setSectionResizeMode(3,QHeaderView.Stretch)
		centerDelegate=alignCenterDelegate(self.ui.theTable)
		self.ui.theTable.setItemDelegateForColumn(1,centerDelegate)
		self.ui.theTable.setItemDelegateForColumn(2,centerDelegate)
		self.ui.theTable.setItemDelegateForColumn(3,centerDelegate)
		# clearFocus doesn't remove the focus rectangle from the top-left cell unless
		#  there is a half second delay (singleshot) before callig it, but changing
		#  the focus to something else does remove the focus rectangle immediately
		self.ui.buttonBox.setFocus()
		self.filenameBase=None
		self.setFixedSize(self.size())

	def accept(self):
		if self.filenameBase:
			self.parent.load(self.filenameBase+'.csv')
			super(loadDialog,self).accept()

	def reject(self):
		super(loadDialog,self).reject()

	def cellClicked(self,row,col):
		self.filenameBase=self.ui.theTable.item(row,col).toolTip()

	def useBrowserClicked(self,*args):
		fileDialog=QFileDialog()
		fileDialog.setOption(QFileDialog.DontUseNativeDialog)
		fileDialog.setProxyModel(CSVFileSortFilterProxyModel(self))
		fileDialog.setNameFilter("CSV Radio Log Data Files (*.csv)")
		fileDialog.setDirectory(self.parent.firstWorkingDir)
		if fileDialog.exec_():
			self.parent.load(fileDialog.selectedFiles()[0])
			self.close()

# fleetsync filtering scheme:
# - maintain a table of all known (received) fleetsync device IDs.  This table is empty at startup.
#   columns: fleet, id, callsign, last time, filtered
#      callsign may be blank
#      filtered is true/false
# - for each incoming FS transmission, add/update the entry for that device, regardless of whether it is filtered.
# - allow the filtered value to be changed from various places
#   - fitler dialog - allow click in table cell to toggle
#   - team tab right-click menu - should this affect all callsigns belonging to that team?
#   - change callsign dialog - show filtered status and allow click to toggle
# - show filtered status in various places
#   - team tab - one symbology for all devices filtered, another for some devices filtered
#   - main UI filter button - flash a color if anything is filtered (or if FS is muted??)
#   - table cell in filter dialog - maybe show rows in groups - filtered first?  or sort by filtered?
 
class fsFilterDialog(QDialog,Ui_fsFilterDialog):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.ui=Ui_fsFilterDialog()
		self.ui.setupUi(self)
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		self.parent=parent
		self.tableModel = fsTableModel(parent.fsLog, self)
		self.ui.tableView.setModel(self.tableModel)
		self.ui.tableView.setSelectionMode(QAbstractItemView.NoSelection)
		self.ui.tableView.clicked.connect(self.tableClicked)
		self.ui.tableView.horizontalHeader().setSectionResizeMode(2,QHeaderView.Stretch)
		self.setFixedSize(self.size())
		self.ui.tableView.setStyleSheet("font-size:12pt")
		
	def tableClicked(self,index):
		if index.column()==3:
			self.parent.fsLog[index.row()][index.column()] = not self.parent.fsLog[index.row()][index.column()]
			self.ui.tableView.model().layoutChanged.emit()
			self.parent.fsBuildTeamFilterDict()
			self.parent.fsBuildTooltip()
			
	def closeEvent(self,event):
		rprint("closing fsFilterDialog")


class fsSendDialog(QDialog,Ui_fsSendDialog):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.ui=Ui_fsSendDialog()
		self.ui.setupUi(self)
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		self.parent=parent
		# need to connect apply signal by hand https://stackoverflow.com/a/35444005
		btn=self.ui.buttonBox.button(QDialogButtonBox.Apply)
		btn.clicked.connect(self.apply)
		self.ui.fleetField.setValidator(QRegExpValidator(QRegExp('[1-9][0-9][0-9]'),self.ui.fleetField))
		# 36 character max length - see sendText notes
		self.ui.messageField.setValidator(QRegExpValidator(QRegExp('.{1,36}'),self.ui.messageField))
		self.functionChanged() # to set device validator

	def functionChanged(self):
		sendText=self.ui.sendTextRadioButton.isChecked()
		self.ui.sendToAllCheckbox.setEnabled(sendText)
		self.ui.messageField.setEnabled(sendText)
		# if sending, a comma-or-space-delimited list of device IDs can be specified;
		# if polling GPS, only one device ID can be specified
		if sendText:
			self.ui.deviceLabel.setText('Device ID(s)')
			self.ui.deviceField.setValidator(QRegExpValidator(QRegExp('^([1-9][0-9][0-9][0-9][, ]?)*$'),self.ui.deviceField))
		else:
			self.ui.sendToAllCheckbox.setChecked(False) # this should automatically enable fleet/device fields
			self.ui.deviceField.setText('') # easier than overriding fixup() in a custom validator
			self.ui.deviceLabel.setText('Device ID')
			self.ui.deviceField.setValidator(QRegExpValidator(QRegExp('[1-9][0-9][0-9][0-9]'),self.ui.deviceField))

	def sendAllCheckboxChanged(self):
		sendAll=self.ui.sendToAllCheckbox.isChecked()
		self.ui.fleetField.setEnabled(not sendAll)
		self.ui.deviceField.setEnabled(not sendAll)

	def apply(self):
		if not self.parent.firstComPort:
			msg='Cannot send FleetSync data - no valid FleetSync COM ports were found.  Keying the mic on a portable radio will trigger COM port recognition.'
			rprint(msg)
			box=QMessageBox(QMessageBox.Critical,'FleetSync error',msg,
				QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			box.open()
			box.raise_()
			box.exec_()
			return

		# validate fields
		# valid=(fleet.isnumeric() and int(fleet)>99 and int(fleet)<1000) # three digit integer
		# valid=valid and (device.isnumeric() and int(fleet)>99 and int(fleet)<1000) # three digit integer
		valid=True
		fleet=self.ui.fleetField.text()
		device=self.ui.deviceField.text()
		msg=self.ui.messageField.text()
		invalidMsg='The form had error(s).  Please correct and try again:'
		sendText=self.ui.sendTextRadioButton.isChecked()
		sendAll=self.ui.sendToAllCheckbox.isChecked()
		if not sendAll:
			if not self.ui.fleetField.hasAcceptableInput():
				invalidMsg+='\n - Fleet ID must be a three-digit integer'
				valid=False
			if not self.ui.deviceField.hasAcceptableInput():
				if sendText:
					invalidMsg+='\n - Device ID(s) must be a four-digit integer, or a comma-separated or space-separated list of four-digit integers'
				else:
					invalidMsg+='\n - Device ID must be a four-digit integer'
				valid=False
		if sendText:
			if not msg or msg.isspace():
				invalidMsg+='\n - Message cannot be blank'
				valid=False
		if not valid:
			box=QMessageBox(QMessageBox.Critical,"Form errors",invalidMsg,
										QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			box.show()
			box.raise_()
			box.exec_()
			return

		# validation completed
		if sendText:
			if sendAll:
				self.parent.sendText('ALL',message=msg)
			else:
				deviceParse=re.split('[ ,]+',device)
				if len(deviceParse)==1:
					self.parent.sendText(fleet,device,msg)
				elif len(deviceParse)>1:
					self.parent.sendText([[fleet,d] for d in deviceParse],message=msg)
				else:
					rprint('ERROR: the form validated, but apparently in error: must specify a device ID or list of device IDs (separated by comma or space)')
		else:
			self.parent.pollGPS(fleet,device)


class fsSendMessageDialog(QDialog,Ui_fsSendMessageDialog):
	def __init__(self,parent,fdcList): # fdcList is a list of [fleet,dev,callsignText] lists
		QDialog.__init__(self)
		self.ui=Ui_fsSendMessageDialog()
		self.ui.setupUi(self)
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		self.parent=parent
		self.fdcList=fdcList
		# 36 character max length - see sendText notes
		self.ui.messageField.setValidator(QRegExpValidator(QRegExp('.{1,36}'),self.ui.messageField))
		if len(fdcList)==1:
			[fleet,device,callsignText]=fdcList[0]
			self.ui.theLabel.setText('Message for '+str(fleet)+':'+str(device)+' '+str(callsignText)+':')
		else:
			label='Message for multiple radios:'
			for fdc in fdcList:
				[fleet,device,callsignText]=fdc
				label+='\n  '+str(fleet)+':'+str(device)+' '+str(callsignText)
			self.ui.theLabel.setText(label)

	def accept(self):
		msg=self.ui.messageField.text()
		if not msg or msg.isspace():
			box=QMessageBox(QMessageBox.Critical,"Form error",'Message cannot be blank; please try again.',
										QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			box.show()
			box.raise_()
			box.exec_()
			return
		self.parent.sendText([fdc[0:2] for fdc in self.fdcList],message=msg)
		super(fsSendMessageDialog,self).accept()


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
		self.fleet=int(fleet)
		self.device=int(device)
		
		rprint("openChangeCallsignDialog called.  fleet="+str(self.fleet)+"  dev="+str(self.device))

		self.ui.fleetField.setText(fleet)
		self.ui.deviceField.setText(device)
		self.ui.currentCallsignField.setText(callsign)
		self.ui.newCallsignField.setFocus()
		self.ui.newCallsignField.setText("Team  ")
		self.ui.newCallsignField.setSelection(5,1)
		self.ui.fsFilterButton.clicked.connect(self.fsFilterConfirm)
		changeCallsignDialog.openDialogCount+=1
		self.setFixedSize(self.size())

	def fsFilterConfirm(self):
		really=QMessageBox(QMessageBox.Warning,"Please Confirm","Filter (ignore) future incoming messages\n  from this FleetSync device?",
			QMessageBox.Yes|QMessageBox.No,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
		if really.exec_()==QMessageBox.No:
			self.close()
			return
		self.parent.parent.fsFilterEdit(self.fleet,self.device,True)
		self.close()
		# also close the related new entry dialog if its message field is blank, in the same manner as autoCleanup
		if self.parent.ui.messageField.text()=="":
			self.parent.closeEvent(QEvent(QEvent.Close),accepted=False,force=True)
		
	def accept(self):
		found=False
		fleet=self.ui.fleetField.text()
		dev=self.ui.deviceField.text()
		# fix #459 (and other places in the code): remove all leading and trailing spaces, and change all chains of spaces to one space
		newCallsign=re.sub(r' +',r' ',self.ui.newCallsignField.text()).strip()
		# change existing device entry if found, otherwise add a new entry
		for n in range(len(self.parent.parent.fsLookup)):
			entry=self.parent.parent.fsLookup[n]
			if entry[0]==fleet and entry[1]==dev:
				found=True
				self.parent.parent.fsLookup[n][2]=newCallsign
		if not found:
			self.parent.parent.fsLookup.append([fleet,dev,newCallsign])
		# set the current radio log entry teamField also
		self.parent.ui.teamField.setText(newCallsign)
		# save the updated table (filename is set at the same times that csvFilename is set)
		self.parent.parent.fsSaveLookup()
		# change the callsign in fsLog
		self.parent.parent.fsLogUpdate(int(fleet),int(dev),newCallsign)
		# finally, pass the 'accept' signal on up the tree as usual
		changeCallsignDialog.openDialogCount-=1
		self.parent.parent.sendPendingGet(newCallsign)
		# set the focus to the messageField of the active stack item - not always
		#  the same as the new entry, as determined by addTab
		self.parent.parent.newEntryWindow.ui.tabWidget.currentWidget().ui.messageField.setFocus()
		super(changeCallsignDialog,self).accept()
		rprint("New callsign pairing created: fleet="+fleet+"  dev="+dev+"  callsign="+newCallsign)


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
		self.printIconPixmap.load(":/radiolog_ui/icons/print_icon.png")
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


class fsTableModel(QAbstractTableModel):
	header_labels=['Fleet','Device','Callsign','Filtered?','Last Received']
	def __init__(self, datain, parent=None, *args):
		QAbstractTableModel.__init__(self, parent, *args)
		self.arraydata=datain
		self.filteredIcon=QIcon(QPixmap(":/radiolog_ui/icons/fs_redcircleslash.png"))
		self.unfilteredIcon=QIcon(QPixmap(":/radiolog_ui/icons/fs_greencheckbox.png"))
		
	def headerData(self,section,orientation,role=Qt.DisplayRole):
#		print("headerData:",section,",",orientation,",",role)
		if role==Qt.DisplayRole and orientation==Qt.Horizontal:
			return self.header_labels[section]
		return QAbstractTableModel.headerData(self,section,orientation,role)

	def rowCount(self, parent):
		return len(self.arraydata)

	def columnCount(self, parent):
		return len(self.header_labels)

	# NOTE that it is generally not wise to tweak the display from within the model;
	#  a delegate is the propoer place for that; however, since this model
	#  only has one display, we can modify it here using the DisplayRole which
	#  will not modify the behavior of functions that query the fsLog directly.
	def data(self, index, role):
		if not index.isValid():
			return QVariant()
		elif role == Qt.DecorationRole and index.column()==3:
			if self.arraydata[index.row()][index.column()]==True:
# 			return QColor(128,128,255)
				return self.filteredIcon
			else:
				return self.unfilteredIcon
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
			if index.column()==3:
				if rval==True:
					rval="Filtered"
				if rval==False:
					rval="Unfiltered"
			return rval
		

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
		return(val.lower()==target.lower() or addAllFlag) # #453: perform case-insensitive match


# code for CSVFileSortFilterProxyModel partially taken from
#  https://github.com/ZhuangLab/storm-control/blob/master/steve/qtRegexFileDialog.py
class CSVFileSortFilterProxyModel(QSortFilterProxyModel):
	def __init__(self,parent=None):
# 		print("initializing CSVFileSortFilterProxyModel")
		super(CSVFileSortFilterProxyModel,self).__init__(parent)

	# filterAcceptsRow - return True if row should be included in the model, False otherwise
	#
	# do not list files named *_fleetsync.csv or *_clueLog.csv
	#  do a case-insensitive comparison just in case
	def filterAcceptsRow(self,source_row,source_parent):
# 		print("CSV filterAcceptsRow called")
		source_model=self.sourceModel()
		index0=source_model.index(source_row,0,source_parent)
		# Always show directories
		if source_model.isDir(index0):
			return True
		# filter files
		filename=source_model.fileName(index0).lower()
# 		filename=self.sourceModel().index(row,0,parent).data().lower()
# 		print("testing lowercased filename:"+filename)
		# never show non- .csv files
		if filename.count(".csv")<1:
			return False
		if filename.count("_fleetsync")+filename.count("_cluelog")==0:
			return True
		else:
			return False

	# use source model sort, otherwise date sort will be done alphamerically
	#  i.e. 9-1-2010 will be shown as more recent than 12-1-2018 since 9 > 1 
	#  see https://stackoverflow.com/a/53797546/3577105
	def sort(self, column, order):
		self.sourceModel().sort(column, order)
	
 
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
	sys.excepthook = handle_exception
	main()
