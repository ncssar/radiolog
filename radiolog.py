# #############################################################################
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
import json
import threading
import webbrowser
import queue
from reportlab.lib import colors,utils
from reportlab.lib.pagesizes import letter,landscape,portrait
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image, Spacer
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.units import inch
from PyPDF2 import PdfReader,PdfWriter
from FingerTabs import *
from pygeodesy import Datums,ellipsoidalBase,dms
from difflib import SequenceMatcher
from caltopo_python import CaltopoSession
from pyqtspinner import WaitingSpinner

__version__ = "3.14.0"

# json dump, shortened to n lines
def jd(j):
    nLines=5
    try:
        lines=json.dumps(j,indent=3).splitlines()
        str='\n'.join(lines[:nLines])
        if len(lines)>nLines:
            str+='  ...'
        logging.info(str)
    except Exception as e:
        logging.info(f'exception while printing json "{j}": {e}')

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

# Foreground, Background, Bold, Italic - used by teamTabsPopup but could maybe be used
#  to replace statusStyleDict as a speedup versus style sheets
statusAppearanceDict={
	# 'default':{
	# 	'foreground':Qt.black,
	# 	'background':None,
	# 	'italic':False,
	# 	'blink':False
	# },
	'At IC':{
		'foreground':None,
		'background':Qt.green,
		'bgHidden':QColor('#afa'),
		'blink':False
	},
	'In Transit':{
		'foreground':Qt.white,
		'background':Qt.blue,
		'bgHidden':QColor('#aaf'),
		'blink':False
	},
	'Waiting for Transport':{
		'foreground':Qt.white,
		'background':Qt.blue,
		'bgHidden':QColor('#aaf'),
		'blink':True
	},
	'STANDBY':{
		'foreground':Qt.white,
		'background':Qt.black,
		'bgHidden':QColor('#ddd'),
		'blink':True
	},
	'TIMED_OUT_ORANGE':{
		'foreground':Qt.black,
		'background':QColor(255,128,0),
		'bgHidden':QColor('#fb3'),
		'blink':False
	},
	'TIMED_OUT_RED':{
		'foreground':Qt.black,
		'background':Qt.red,
		'bgHidden':QColor('#faa'),
		'blink':False
	}
}

timeoutDisplayList=[["10 sec",10]]
for n in range (1,13):
	timeoutDisplayList.append([str(n*10)+" min",n*600])

teamStatusDict={}
teamFSFilterDict={}
teamTimersDict={}
teamCreatedTimeDict={}

versionDepth=5 # how many backup versions to keep; see rotateBackups

#752 - change continueSec to a config file option, default=20
# continueSec=20
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

# lastClueNumber=0

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

phonetics=[
	'Alpha','Bravo','Charlie','Delta','Echo','Foxtrot','Golf','Hotel',
	'India','Juliet','Kilo','Lima','Mike','November','Oscar','Papa',
	'Quebec','Romeo','Sierra','Tango','Uniform','Victor','X-ray','Yankee','Zulu',
	'Adam','Boy','Charles','David','Edward','Frank','George','Henry',
	'Ida','John','King','Lincoln','Mary','Nora','Ocean','Paul','Queen',
	'Robert','Sam','Tom','Union','Victor','William','Xray','Young','Zebra'
]
lowerPhonetics=[x.lower() for x in phonetics]

capsList=['SAR'] # can be overridden using config file

def preserveCapsIfNeeded(w):
	# use global variable capsList
	if w.upper() in capsList:
		return w.upper()
	else:
		return w

# 728 - capitalize() will lowecase all letters except th first;
#  to preserve the case of the rest of the word after the first letter,
#  see https://stackoverflow.com/a/31767666/3577105
def capFirst(word):
	return word[:1].upper()+word[1:]

def getExtTeamName(teamName):
	# logging.info('getExtTeamName called with argument "'+str(teamName)+'"')
	if teamName.lower().startswith("all ") or teamName.lower()=="all":
		return "ALL TEAMS"
	#702 - change camelCaseWords to camel Case Words
	#  insert a space before every Uppercase letter that is preceded by a lowercase letter
	teamName=re.sub(r'([a-z])([A-Z])',r'\1 \2',teamName)
	# logging.info(' t1: teamName='+str(teamName))
	# capitalize each word, in case teamName is e.g. 'Team bravo'
	#  https://stackoverflow.com/a/1549644/3577105
	# teamName=' '.join(w.capitalize() for w in teamName.split())
	# 728 - preserve case of letters after the first letter in each word
	teamName=' '.join(capFirst(w) for w in teamName.split())
	# logging.info(' t2: teamName='+str(teamName))
	# fix #459 (and other places in the code): remove all leading and trailing spaces, and change all chains of spaces to one space
	name=re.sub(r' +',r' ',teamName).strip()
	name=name.replace(' ','') # remove spaces to shorten the name
	# find index of first number in the name; everything left of that is the 'prefix';
	# assume that everything after the prefix is a number
	firstNum=re.search(r'\d',name)
	firstNumIndex=-1 # assume there is no number at all
	if firstNum!=None:
		firstNumIndex=firstNum.start()
	if firstNumIndex>0:
		prefix=name[:firstNumIndex]
	else:
		prefix=""
	#589: always prepend 'Team' here if name is all digits or is in the list of known names
	if name.isdigit() or name.lower() in lowerPhonetics:
		prefix='team'
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
	# #452 - preserve caps if needed after capitalize but before prepending with 'z_'
	prefix=prefix.capitalize()
	prefix=preserveCapsIfNeeded(prefix)
	prefix='z_'+prefix

	if firstNum!=None:
		rest=name[firstNumIndex:].zfill(5)
	else:
		rest=name # preserve case if there are no numbers
##	logging.info("prefix="+prefix+" rest="+rest+" name="+name)
	extTeamName=prefix+rest
	# logging.info("Team Name:"+teamName+": extended team name:"+extTeamName)
	# logging.info('  --> extTeamName="'+str(extTeamName)+'"')
	return extTeamName

def getNiceTeamName(extTeamName):
	# logging.info('getNiceTeamName called for '+str(extTeamName))
	# prune any leading 'z_' that may have been added for sorting purposes
	extTeamName=extTeamName.replace('z_','')
	# 751 - preserve verbatim uppercase team name if it starts with KW- (case-insensitive comparison)
	if extTeamName.lower().startswith('kw-'):
		return extTeamName.upper()
	# find index of first number in the name; everything left of that is the 'prefix';
	# assume that everything after the prefix is a number
	#  (left-zero-padded to 5 digits)
	# if there is no number, split after the word 'team' if it exists
	firstNum=re.search(r'\d',extTeamName)
	splitIndex=-1 # assume there is no number at all
	prefix=""
	if firstNum:
		splitIndex=firstNum.start()
	elif extTeamName.lower().startswith('team'):
		splitIndex=4
	if splitIndex>0:
		prefix=extTeamName[:splitIndex]
#		name=prefix.capitalize()+" "+str(int(str(extTeamName[firstNumIndex:])))
		# #452 - preserve caps if needed after capitalize but before appending tail
		prefix=prefix.capitalize()
		prefix=preserveCapsIfNeeded(prefix)
		name=prefix+" "+str(extTeamName[splitIndex:]).lstrip('0')
	else:
		name=extTeamName
	# finally, remove any leading zeros (necessary for non-'Team' callsigns)
	name=name.lstrip('0')
# 	logging.info("getNiceTeamName("+extTeamName+")")
# 	logging.info("FirstNumIndex:"+str(firstNumIndex)+" Prefix:'"+prefix+"'")
	# logging.info("Human Readable Name:'"+name+"'")
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

def getClueNamesShorthand(clueNames):
	# build a list of numbers mapped from clueNames: use the number if clueName is numeric, or 0 if non-numeric
	numbers=[]
	notNumbers=[]
	for clueName in clueNames:
		if isinstance(clueName,str) and clueName.isdigit():
			numbers.append(int(clueName))
		else:
			notNumbers.append(clueName)
	
	# from Google AI Overview
	# Ensure sorted order and unique elements
	numbers = sorted(list(set(numbers)))
	ranges = []
	start = numbers[0]
	
	for i in range(1, len(numbers)):
		# Check if the current number is consecutive to the previous one
		if numbers[i] != numbers[i-1] + 1:
			# If not, the current range has ended
			ranges.append((start, numbers[i-1]))
			start = numbers[i]
			
	# Append the last range after the loop finishes
	ranges.append((start, numbers[-1]))

	# convert ranges to shorthand
	# e.g. ranges=[(1, 2), (5, 5), (7, 10), (13, 15), (42, 45)]
	# shorthand=[str(first)+' thru '+str(last) for (first,last) in ranges]
	shorthandList=[]
	for (first,last) in ranges:
		if first==last:
			shorthandList.append(f'{first}')
		elif last-first==1:
			shorthandList+=[str(first),str(last)]
		else:
			# shorthandList.append(f'{first} thru {last}')
			shorthandList.append(f'{first}-{last}')
	shorthandList+=notNumbers
	return ' '.join(shorthandList)
	
# callback called from both clueDialog and nonRadioClueDialog
def clueNumberChanged(dialog,mainWindow):
	# global usedClueNames
	# global lastClueNumber
	# logging.info(f'changed t1: old="{dialog.clueName}" field="{dialog.ui.clueNumberField.text()}"')
	newVal=dialog.ui.clueNumberField.text().rstrip()
	if newVal!=dialog.clueName:
		if not newVal or any(item.lower()==newVal.lower() for item in mainWindow.usedClueNames): # case insensitive list search, so 20a is disallowed if 20A exists
			head='Clue Number Already Used'
			msg=f'"{newVal}" is already used.  Enter a different clue number, or use the default.'
			if not newVal:
				head='Blank Clue Number is Not Allowed'
				msg='Clue number must be specified.'
			box=QMessageBox(QMessageBox.Critical,head,msg,QMessageBox.Close,dialog,
				Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			box.open()
			box.raise_()
			box.exec_()
			# set the field text back to the initial value; that will trigger this function again so make sure it falls through gracefully
			dialog.ui.clueNumberField.setText(dialog.clueName)
			dialog.ui.clueNumberField.setFocus()
		else: # new value is unique
			# remove dialog.clueName from usedClueNames, which was set at init and is the previous value of this field
			mainWindow.usedClueNames.remove(dialog.clueName)
			# add an automated entry
			dialog.values=["" for n in range(10)]
			dialog.values[0]=time.strftime("%H%M")
			prefix=''
			logging.info(f'calling classname: {dialog.__class__.__name__}')
			if 'nonRadio' in dialog.__class__.__name__:
				prefix='NON-RADIO '
			dialog.values[3]="RADIO LOG SOFTWARE: "+prefix+"CLUE NUMBER CHANGED FROM "+dialog.clueName+" to "+newVal
			dialog.values[6]=time.time()
			mainWindow.newEntry(dialog.values)
			# then update dialog.clueName and usedClueNames
			dialog.clueName=newVal
			mainWindow.usedClueNames.append(dialog.clueName)
	# logging.info(f'changed t2: newVal="{newVal}";  field text="{dialog.ui.clueNumberField.text()}"')
	if dialog.ui.clueNumberField.text() not in [dialog.clueName,newVal]: # clueName: if it was just set to the initial value; newVal: if trailing space was trimmed
		# logging.info('changed t3')
		dialog.ui.clueNumberField.setText(newVal)
	# logging.info('changed t4')


###### LOGGING CODE BEGIN ######

# do not pass ERRORs to stdout - they already show up on the screen from stderr
class LoggingFilter(logging.Filter):
	def filter(self,record):
		# only show thread name if other than main thread
		if record.threadName=='MainThread':
			record.threadName=''
		# return record.levelno < logging.ERROR
		return True # print all levels
	
# only print module name if it is other than radiolog
class LoggingFormatter(logging.Formatter):
	def format(self,record):
		s=super().format(record)
		if record.module=='radiolog':
			s=s.replace('[radiolog:','[')
		return s

logFileLeafName=getFileNameBase('radiolog_log')+'.txt'

def setLogHandlers(dir=None):
	sh=logging.StreamHandler(sys.stdout)
	sh.setLevel(logging.INFO)
	sh.addFilter(LoggingFilter())
	sh.setFormatter(LoggingFormatter('%(asctime)s [%(module)s:%(lineno)d:%(levelname)s:%(threadName)s] %(message)s','%H%M%S'))
	handlers=[sh]
	# add a filehandler if dir is specified
	if dir:
		logFileName=os.path.join(dir,logFileLeafName)
		fh=logging.FileHandler(logFileName)
		fh.setLevel(logging.INFO)
		fh.addFilter(LoggingFilter())
		fh.setFormatter(LoggingFormatter('%(asctime)s [%(module)s:%(lineno)d:%(levelname)s:%(threadName)s] %(message)s','%H%M%S'))
		handlers=[sh,fh]
	# redo logging.basicConfig here, to overwrite setup from any imported modules
	logging.basicConfig(
		level=logging.INFO,
		datefmt='%H%M%S',
		format='%(asctime)s [%(module)s:%(lineno)d:%(levelname)s:%(threadName)s] %(message)s',
		handlers=handlers,
		force=True
	)

setLogHandlers()

# redirect stderr to stdout here by overriding excepthook
# from https://stackoverflow.com/a/16993115/3577105
# and https://www.programcreek.com/python/example/1013/sys.excepthook
def handle_exception(exc_type, exc_value, exc_traceback):
	if not issubclass(exc_type, KeyboardInterrupt):
		logging.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
	sys.__excepthook__(exc_type, exc_value, exc_traceback)
	# interesting that the program no longer exits after uncaught exceptions
	#  if this function replaces __excepthook__.  Probably a good thing but
	#  it would be nice to undertstand why.
	return
# note: 'sys.excepthook = handle_exception' must be done inside main()

# get rid of rprint - replace all occurrances with logging.info - mainly to preserve line numbers
# def rprint(text):
# 	logging.info(text)

###### LOGGING CODE END ######

# #471: rebuild any modified Qt .ui and .qrc files at runtime
#   (copied from plans_console repo - could be made into a shared module at some point)

qtDesignerSubDir='designer' # subdir containing Qt Designer source files (*.ui)
qtUiPySubDir='ui' # target subdir for compiled ui files (*_ui.py)
qtQrcSubDir='.' # subdir containing Qt qrc resource files (*.qrc)
qtRcPySubDir='.' # target subdir for compiled resource files
iconsSubDir='icons'

installDir=os.path.dirname(os.path.realpath(__file__))
qtDesignerDir=os.path.join(installDir,qtDesignerSubDir)
qtUiPyDir=os.path.join(installDir,qtUiPySubDir)
qtQrcDir=os.path.join(installDir,qtQrcSubDir)
qtRcPyDir=os.path.join(installDir,qtRcPySubDir)
iconsDir=os.path.join(installDir,iconsSubDir)

# rebuild all _ui.py files from .ui files in the same directory as this script as needed
#   NOTE - this will overwrite any edits in _ui.py files
for ui in glob.glob(os.path.join(qtDesignerDir,'*.ui')):
	uipy=os.path.join(qtUiPyDir,os.path.basename(ui).replace('.ui','_ui.py'))
	if not (os.path.isfile(uipy) and os.path.getmtime(uipy) > os.path.getmtime(ui)):
		cmd='pyuic5 -o '+uipy+' '+ui
		logging.info('Building GUI file from '+os.path.basename(ui)+':')
		logging.info('  '+cmd)
		os.system(cmd)

# rebuild all _rc.py files from .qrc files in the same directory as this script as needed
#   NOTE - this will overwrite any edits in _rc.py files
for qrc in glob.glob(os.path.join(qtQrcDir,'*.qrc')):
	rcpy=os.path.join(qtRcPyDir,os.path.basename(qrc).replace('.qrc','_rc.py'))
	if not (os.path.isfile(rcpy) and os.path.getmtime(rcpy) > os.path.getmtime(qrc)):
		cmd='pyrcc5 -o '+rcpy+' '+qrc
		logging.info('Building Qt Resource file from '+os.path.basename(qrc)+':')
		logging.info('  '+cmd)
		os.system(cmd)

# define simple-subclasses here so they can be used during import of pyuic5-compiled _ui.py files
class CustomPlainTextEdit(QPlainTextEdit):
	def __init__(self,parent,*args,**kwargs):
		self.parent=parent
		QPlainTextEdit.__init__(self,parent)
	
	def focusOutEvent(self,e):
		self.parent.customFocusOutEvent(self)
		super(CustomPlainTextEdit,self).focusOutEvent(e)


# custom QComboBox - click on the lineEdit opens the popup, like a non-editable QComboBox
#  from google search AI overview
class CustomComboBox(QComboBox):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.setEditable(True)
		self.lineEdit().setReadOnly(True)

		# Install an event filter on the QLineEdit to capture mouse clicks
		self.lineEdit().installEventFilter(self)

	def eventFilter(self, obj, event):
		# Filter for the specific QLineEdit and mouse press events
		if obj == self.lineEdit() and event.type() == QtCore.QEvent.Type.MouseButtonPress:
			self.showPopup()
			return True  # Event is handled
		return super().eventFilter(obj, event)
	

class CustomLineEdit(QLineEdit):
	def __init__(self,parent,*args,**kwargs):
		self.parent=parent
		QLineEdit.__init__(self,parent)
	
	def focusOutEvent(self,e):
		self.parent.customFocusOutEvent(self)
		super(CustomLineEdit,self).focusOutEvent(e)

	def focusInEvent(self,e):
		self.parent.customFocusInEvent(self)
		super(CustomLineEdit,self).focusInEvent(e)


from ui.help_ui import Ui_Help
from ui.options_ui import Ui_optionsDialog
from ui.fsSendDialog_ui import Ui_fsSendDialog
from ui.fsSendMessageDialog_ui import Ui_fsSendMessageDialog
from ui.newEntryWindow_ui import Ui_newEntryWindow
from ui.newEntryWidget_ui import Ui_newEntryWidget
from ui.clueDialog_ui import Ui_clueDialog
from ui.clueLogDialog_ui import Ui_clueLogDialog
from ui.printDialog_ui import Ui_printDialog
from ui.fsFilterDialog_ui import Ui_fsFilterDialog
from ui.opPeriodDialog_ui import Ui_opPeriodDialog
from ui.printClueLogDialog_ui import Ui_printClueLogDialog
from ui.nonRadioClueDialog_ui import Ui_nonRadioClueDialog
from ui.subjectLocatedDialog_ui import Ui_subjectLocatedDialog
from ui.continuedIncidentDialog_ui import Ui_continuedIncidentDialog
from ui.loadDialog_ui import Ui_loadDialog
from ui.loginDialog_ui import Ui_loginDialog
from ui.teamTabsPopup_ui import Ui_teamTabsPopup
from ui.findDialog_ui import Ui_findDialog
from ui.teamNotesDialog_ui import Ui_teamNotesDialog

# function to replace only the rightmost <occurrence> occurrences of <old> in <s> with <new>
# used by the undo function when adding new entry text
# credit to 'mg.' at http://stackoverflow.com/questions/2556108
def rreplace(s,old,new,occurrence):
	li=s.rsplit(old,occurrence)
	return new.join(li)
	
def normName(name):
	return re.sub("[^A-Za-z0-9_]+","_",name)

def buildObjSS(objectName,style):
	return '#'+objectName+' { '+style+' }'

#529 - specify a hardcoded global stylesheet to be applied to every dialog class;
#  setting the top level style sheet when there is a lot of data can cause big delay:
#  setting the top level stylesheet resulted in 10 second delay for ~300 entries
#  when called during fontsChanged, but doing so now once during init of each class
#  is instant; make sure to do the same in init of each custom GUI class, since some
#  dialogs don't have a parent
globalStyleSheet="""
			QMessageBox,QDialogButtonBox QPushButton {
				font-size:14pt;
			}
		"""

caltopoColors={
	'openedWritable':'#00dd00',
	'openedReadOnly':'#ff9933',
	'mapless':'#bbddbb',
	'disabled':'#aaaaaa',
	'disconnected':'#ee0000'
}

caltopoIndicatorToolTip="""
	<style>
		table {
			border-collapse: collapse;
			width: 100%;
		}
		th, td {
			border: 1px solid black;
			padding: 5px;
			text-align: left;
		}
		th {
			background-color: #f2f2f2;
		}
	</style>
	<table>
		<thead>
			<tr>
				<th>Color</th>
				<th>CalTopo Link Indicator Meaning</th>
			</tr>
		</thead>
		<tbody>
			<tr>
				<td style="background-color: """+caltopoColors['disabled']+""";">&nbsp;&nbsp;&nbsp;</td>
				<td>Disabled</td>
			</tr>
			<tr>
				<td style="background-color: """+caltopoColors['mapless']+""";">&nbsp;&nbsp;&nbsp;</td>
				<td>Connected to caltopo server, no open map</td>
			</tr>
			<tr>
				<td style="background-color: """+caltopoColors['openedWritable']+""";">&nbsp;&nbsp;&nbsp;</td>
				<td>Connected to a writable map or bookmark</td>
			</tr>
			<tr>
				<td style="background-color: """+caltopoColors['openedReadOnly']+""";">&nbsp;&nbsp;&nbsp;</td>
				<td>Connected to a read-only map or bookmark</td>
			</tr>
			<tr>
				<td style="background-color: """+caltopoColors['disconnected']+""";">&nbsp;&nbsp;&nbsp;</td>
				<td>Unexpected disconnect (will automatically reconnect)</td>
			</tr>
		</tbody>
	</table>"""

# CustomEncoder enables json.dumps for dicts with lists of callables
#  (to avoid "TypeError: Object of type function is not JSON serializable")
#  usage: json.dumps(callable_list, cls=CustomEncoder)
class CustomEncoder(json.JSONEncoder):
	def default(self, obj):
		if callable(obj):
			return f"Callable: {obj.__name__ if hasattr(obj, '__name__') else str(obj)}"
		return json.JSONEncoder.default(self, obj)
	

class MyWindow(QDialog,Ui_Dialog):

	# inter-thread signals (GUI must only be modified by main-thread code to avoid crashes!)
	_sig_caltopoDisconnected=pyqtSignal()
	_sig_caltopoReconnected=pyqtSignal()
	_sig_caltopoReconnectedFromCreateCTS=pyqtSignal()
	_sig_caltopoReconnectedFromOpenMap=pyqtSignal()
	_sig_caltopoMapClosed=pyqtSignal()
	# _sig_caltopoCreateCTSCB=pyqtSignal(bool)

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
			logging.info(msg)
		else:
			err='FATAL ERROR: initial session directory "'+self.sessionDir+'" was not created.  ABORTING.'
			msg+=err
			self.configErrMsgBox=QMessageBox(QMessageBox.Critical,"Fatal Configuration Error",err,
							QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			self.configErrMsgBox.exec_()
			print(msg)
			sys.exit(-1)

		self.configDir=os.path.join(self.firstWorkingDir,'.config')
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
			logging.info(msg)
			box=QMessageBox(QMessageBox.Information,'Copying configuration directory',msg,
					QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			box.exec_()
			shutil.copytree(srcDir,self.configDir)
		self.configFileName=os.path.join(self.configDir,'radiolog.cfg')
		self.configFileDefaultName=os.path.join(self.configDefaultDir,'radiolog.cfg')
		if not os.path.isfile(self.configFileName):
			msg='config directory was found but did not contain radiolog.cfg; about to copy from default config directory '+self.configDefaultDir+'; this could disable important features like GPS locators, the second working directory, and more.'
			logging.info(msg)
			box=QMessageBox(QMessageBox.Information,'Copying radiolog.cfg',msg,
					QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			box.exec_()
			shutil.copyfile(self.configFileDefaultName,self.configFileName)

#####  END config dir migration code #522

		self.setWindowFlags(self.windowFlags()|Qt.WindowMinMaxButtonsHint)
		self.parent=parent
		self.ui=Ui_Dialog()
		self.ui.setupUi(self)
		self.setStyleSheet(globalStyleSheet)
		# #520 - show version number in main window banner
		versionText='RadioLog '+str(__version__)
		# determine if this is being run from a pyinstaller executable, or from 'python radiolog.py'
		# https://stackoverflow.com/a/35514032
		if '.py' in sys.argv[0]:
			versionText+='dev'
		self.setWindowTitle(versionText)
		logging.info(versionText)
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.loadFlag=False # set this to true during load, to prevent save on each newEntry
		self.totalEntryCount=0 # rotate backups after every 5 entries; see newEntryWidget.accept
		
		# set the team table palette - copied from main table compiled _ui.py
		self.teamTablePalette = QPalette()
		brush = QBrush(QColor(0, 120, 215))
		brush.setStyle(QtCore.Qt.SolidPattern)
		self.teamTablePalette.setBrush(QPalette.Active, QPalette.Highlight, brush)
		brush = QBrush(QColor(85, 170, 255))
		brush.setStyle(QtCore.Qt.SolidPattern)
		self.teamTablePalette.setBrush(QPalette.Inactive, QPalette.Highlight, brush)
		brush = QBrush(QColor(0, 120, 215))
		brush.setStyle(QtCore.Qt.SolidPattern)
		self.teamTablePalette.setBrush(QPalette.Disabled, QPalette.Highlight, brush)
		   
		self.ui.teamHotkeysWidget.setVisible(False) # disabled by default
		# self.ui.teamHotkeysWidget.setStyleSheet('left:50') # same as QTabWidget::tab-bar
		self.hotkeyDict={}
		self.nextAvailHotkeyIndex=0
		self.hotkeyPool=["1","2","3","4","5","6","7","8","9","0","q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x","c","v","b","n","m"]
		self.homeDir=os.path.expanduser("~")
		
		self.hiddenTeamTabsList=[]
		# to make the sidebar a child of the mainwindow, a second argument is passed to
		#  QWidget.__init__ in the sidebar's class __init__ function
		self.sidebar=teamTabsPopup(self)
		self.sidebar.move(-self.sidebar.width(),0)
		self.sidebar.show()
		self.sidebar.raise_()
		self.sidebar.leaveEvent=self.sidebarShowHide
		self.sidebarAnimation=QPropertyAnimation(self.sidebar,b'pos')
		self.sidebarAnimation.setDuration(150)
		self.sidebarIsVisible=False # .isVisible would always return True; it's just slid left when 'hidden'
		self.ui.teamTabsMoreButton=QtWidgets.QPushButton(self.ui.frame)
		self.ui.teamTabsMoreButton.enterEvent=self.sidebarShowHide
		self.ui.teamTabsMoreButton.setVisible(False)
		self.ui.teamTabsMoreButton.setGeometry(1,1,30,35)
		from PyQt5 import QtGui
		self.teamTabsMoreButtonIcon = QIcon()
		self.blankIcon=QIcon()
		self.teamTabsMoreButtonIcon.addPixmap(QPixmap(":/radiolog_ui/icons/3dots.png"), QIcon.Normal, QIcon.Off)
		self.ui.teamTabsMoreButton.setIcon(self.teamTabsMoreButtonIcon)
		self.ui.teamTabsMoreButton.setIconSize(QtCore.QSize(20, 20))
		self.teamTabsMoreButtonIsBlinking=False
		self.CCD1List=['KW-'] # if needed, KW- is appended to CCD1List after loading from config file

		self.findDialog=findDialog(self)
				# messageFieldTopLeft=self.mapToGlobal(self.ui.messageField.pos())
		# tvp=self.mapToGlobal(self.ui.tableView.pos())
		# tvp=self.ui.tableView.mapToGlobal(QPoint(0,0))
		# tvp=self.ui.tableView.parentWidget().mapToGlobal(self.ui.tableView.pos())
		# tvw=self.ui.tableView.width()
		# logging.info('tableView x='+str(tvp.x())+' y='+str(tvp.y())+' w='+str(tvw))
		# self.findDialog.move(tvp.x()+tvw-200,tvp.y())
		# self.findDialog.show()
		# self.findDialog.raise_()
		# self.findDialog.leaveEvent=self.findDialogShowHide
		# self.findDialogAnimation=QPropertyAnimation(self.findDialog,b'pos')
		# self.findDialogAnimation=QPropertyAnimation(self.findDialog.ui.findField,b'geometry')
		# self.findDialogAnimation.setDuration(150)
		# self.findDialogIsVisible=False # .isVisible would always return True; it's just slid left when 'hidden'

		self.menuFont=QFont()
		self.menuFont.setPointSize(14)
		self.toolTipFontSize=14

		self.callsignCompletionWordList=['Relay','Transport']
		for x in phonetics:
			self.callsignCompletionWordList.append(x)
			self.callsignCompletionWordList.append('Team '+x)

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
			logging.info("Window Tracking was initially enabled.  Disabling it for radiolog; will re-enable on exit.")
			win32gui.SystemParametersInfo(win32con.SPI_SETACTIVEWINDOWTRACKING,False)

# 		self.secondWorkingDir=os.getenv('HOMEPATH','C:\\Users\\Default')+"\\Documents\\sar"

		self.incidentName="New Incident"
		self.incidentNameNormalized=normName(self.incidentName)
		self.opPeriod=1
		self.incidentStartDate=time.strftime("%a %b %d, %Y")
		self.isContinuedIncident=False
		self.useOperatorLogin=True # can be disabled in config
		self.operatorLastName='?'
		self.operatorFirstName='?'
		self.operatorId='???'

		self.cts=None
		self.caltopoURL=''
		self.caltopoLink=0
		self.caltopoLinkPrev=0
		self.caltopoOpenMapButtonPrevText=''
		self.caltopoGroupFieldsPrevEnabled=False
		self.radioMarkerDict={}
		self.caltopoMapListDicts=[]
		self.caltopoOpenMapIsWritable=False
		self.caltopoBadResponse=None
		self.radioMarkerFID=None
		self.radioMarkerFolderHasBeenRequested=False

		self.optionsDialog=optionsDialog(self)
		self.optionsDialog.accepted.connect(self.optionsAccepted)
		
		self.printFailMessageBoxShown=False
		
		self.fontSize=10
		self.x=100
		self.y=100
		self.w=600
		self.h=400
		self.clueLog_x=200
		self.clueLog_y=200
		self.clueLog_w=1000
		self.clueLog_h=400
		
		self.useNewEntryWindowHiddenPopup=True # can be disabled in config

		# config file (e.g. <firstWorkingDir>/.config/radiolog.cfg) stores the team standards;
		#  it should be created/modified by hand, and is read at radiolog startup,
		#  and is not modified by radiolog at any point
		# resource file / 'rc file' (e.g. <firstWorkingDir>/radiolog_rc.txt) stores the search-specific
		#  options settings; it is read at radiolog startup, and is written
		#  whenever the options dialog is accepted
		self.readConfigFile() # defaults are set inside readConfigFile

		# logging.info('useOperatorLogin after readConfigFile:'+str(self.useOperatorLogin))

		self.printDialog=printDialog(self)
		self.printClueLogDialog=printClueLogDialog(self)

		# load resource file; process default values and resource file values
		self.lastFileName="" # to force error in restore, in the event the resource file doesn't specify the lastFileName
		self.rcFileName=os.path.join(self.firstWorkingDir,'radiolog_rc.txt')
		self.previousCleanShutdown=self.loadRcFile()
		showStartupOptions=True
		restoreFlag=False
		if not self.previousCleanShutdown and not self.newWorkingDir:
			self.reallyRestore=QMessageBox(QMessageBox.Critical,"Restore last saved files?","The previous Radio Log session may have shut down incorrectly.  Do you want to restore the last saved files (Radio Log, Clue Log, and FleetSync table)?",
										QMessageBox.Yes|QMessageBox.No,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			self.reallyRestore.show()
			self.reallyRestore.raise_()
			if self.reallyRestore.exec_()==QMessageBox.Yes:
				restoreFlag=True
				showStartupOptions=False

		# self.nonEmptyTabGroupCount=0
		self.nonEmptyTabGroups=[]

		self.usedClueNames=[]
		# #483: Check for recent radiolog sessions on this computer.  If any sessions are found from the previous 4 days,
		#  ask the operator if this new session is intended to be a continuation of one of those previous incidents.
		#  If so:
		#    - set the incident name to the same as that in the selected previous radiolog csv file;
		#    - set the OP number to one more than the latest OP# in the previous csv
		#       (with a reminder that OP# can be changed by hand by clicking the OP button);
		#    - set the next clue number to one more than the latest clue number in the previous CSV
		#       (with a reminder that clue# can be changed in the clue dialog the next time it is raised)

		if not restoreFlag:
			self.checkForContinuedIncident()

		if self.isContinuedIncident:
			showStartupOptions=False
			rlInitText='Radio Log Begins - Continued incident "'+self.incidentName+'": Operational Period '+str(self.opPeriod)+' Begins: '
		elif restoreFlag:
			rlInitText='Restored after crash: '
		else:
			rlInitText='Radio Log Begins: '
		rlInitText+=self.incidentStartDate

		clueCount=len(self.usedClueNames)
		suffix=''
		if clueCount==0 and not restoreFlag: # don't add 'no clues' wording: it's confusing on restore, since it shows up as the most recent entry
			usedCluesText='(No clues so far for this incident)'
		else:
			if clueCount>1:
				suffix='s'
			# clueNamesText=' '.join(self.usedClueNames)
			clueNamesText=getClueNamesShorthand(self.usedClueNames)
			usedCluesText='('+str(clueCount)+' clue'+suffix+' so far for this incident: '+clueNamesText+')'
		rlInitText+=' '+usedCluesText
		self.radioLog=[[time.strftime("%H%M"),'','',rlInitText,'','',time.time(),'','','',''],
			['','','','','','',1e10,'','','','']] # 1e10 epoch seconds will keep the blank row at the bottom when sorted
		logging.info('Initial entry: '+rlInitText)

		self.clueLog=[]
		self.clueLog.append(['',self.radioLog[0][3],'',time.strftime("%H%M"),'','','','','',''])

# 		self.csvFileName=getFileNameBase(self.incidentNameNormalized)+".csv"
# 		self.pdfFileName=getFileNameBase(self.incidentNameNormalized)+".pdf"
		self.updateFileNames()
		self.lastSavedFileName="NONE"
##		self.fsFileName=self.getFileNameBase(self.incidentNameNormalized)+"_fleetsync.csv"

		# disable fsValidFleetList checking to allow arbitrary fleets; this
		#  idea is probably obsolete
# 		self.fsValidFleetList=[100]
		self.fsLog=[]
		self.fsFullLog=[]
# 		self.fsLog.append(['','','','',''])
		self.latestBumpDict={}
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
##		logging.info("t1")
##		os.chdir(self.secondWorkingDir)
##		logging.info("t2")
##		os.chdir(self.cwd)
##		logging.info("t3")
		
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
		self.fsLogFileName='radiolog_fsLog.csv'

		self.operatorsFileName='radiolog_operators.json'
		self.teamNotesFileName='team_notes.json'
		
		# 662 added for debugging - copy the operator file into the run dir on startup and on shutdown
		#  (#724: only if the file exists!)
		if os.path.isfile(os.path.join(self.configDir,self.operatorsFileName)):
			shutil.copy(os.path.join(self.configDir,self.operatorsFileName),os.path.join(self.sessionDir,'operators_at_startup.json'))

		# self.operatorsDict: dictionary with one key ('operators') whose value is a list of dictionaries
		#  Why not just a list of dictionaries?  Why wrap in a single-item dictionary?
		#  -> for ease of file I/O with json.dump and json.load - see loadOperators and saveOperators
		self.operatorsDict={'operators':[]}
		
		self.teamNotesDict={}

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
		self.fsFilterDialog.ui.tableView.setColumnWidth(6,60)
		self.fsBuildTooltip()
		self.fsLatestComPort=None
		self.fsShowChannelWarning=True
		
		self.teamNotesDialog=teamNotesDialog(self)

		if self.useOperatorLogin:
			self.loginDialog=loginDialog(self)
			self.ui.loginWidget.clicked.connect(self.loginDialog.toggleShow) # note this is a custom class with custom signal
		else:
			self.ui.loginWidget.setVisible(False)

		self.ui.addNonRadioClueButton.clicked.connect(self.addNonRadioClue)

		self.ui.helpButton.clicked.connect(self.helpWindow.toggleShow)
		self.ui.optionsButton.clicked.connect(self.optionsDialog.toggleShow)
		self.ui.fsFilterButton.clicked.connect(self.fsFilterDialog.toggleShow)
		self.ui.printButton.clicked.connect(self.printDialog.toggleShow)
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
		# font size is constrained to min and max for several items
		self.minLimitedFontSize=8
		self.maxLimitedFontSize=20
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
		self.ui.opPeriodButton.clicked.connect(self.opPeriodDialog.toggleShow)
		self.ui.clueLogButton.clicked.connect(self.clueLogDialog.toggleRaise) # never actually close this dialog

		self.ui.splitter.setSizes([250,150]) # any remainder is distributed based on this ratio
		self.ui.splitter.splitterMoved.connect(self.ui.tableView.scrollToBottom)

		self.tableModel = MyTableModel(self.radioLog, self)
		self.ui.tableView.setModel(self.tableModel)
		self.ui.tableView.setSelectionMode(QAbstractItemView.SingleSelection)

		self.ui.tableView.hideColumn(6) # hide epoch seconds
		self.ui.tableView.hideColumn(7) # hide fleet
		self.ui.tableView.hideColumn(8) # hide device
		self.ui.tableView.hideColumn(9) # hide device
		if not self.useOperatorLogin:
			self.ui.tableView.hideColumn(10) # hide operator
		self.ui.tableView.resizeRowsToContents()

		self.sel=''
		
		self.ui.tableView.setContextMenuPolicy(Qt.CustomContextMenu)
		# self.ui.tableView.customContextMenuRequested.connect(self.tableContextMenu)

		#downside of the following line: slow, since it results in a resize call for each column,
		#  when we could defer and just do one resize at the end of all the resizes
##		self.ui.tableView.horizontalHeader().sectionResized.connect(self.ui.tableView.resizeRowsToContents)
		self.columnResizedFlag=False
		self.ui.tableView.horizontalHeader().sectionResized.connect(self.setColumnResizedFlag)
		self.ui.tableView.horizontalHeader().setMinimumSectionSize(10) # allow tiny column for operator initials

		self.nonRadioClueDialogIsOpen=False
		self.exitClicked=False
		# NOTE - the padding numbers for ::tab take a while to figure out in conjunction with
		#  the stylesheets of the label widgets of each tab in order to change status; don't
		#  change these numbers unless you want to spend a while on trial and error to get
		#  them looking good again!
			# QTabWidget::tab-bar[shifted=true] {
			# 	left:20px;
			# }
			# QTabWidget::tab-bar[shifted=false] {
			# 	left:0px;
			# }
		# the tab bar left margin can vary when the tab scrolls side to side,
		#  for large team count.  It is biggest initially, before it has been scrolled
		#  or if the team count is low enough that all tabs fit; it is smallest when
		#  the bar has been scrolled to the right; and it is somewhere in the middle
		#  when scrolled back all the way left again.  We need to make sure the left
		#  margin is large enough so that the first team tab is not clipped by an
		#  opaque teamTabsMoreButton, by trial-and-error of the tab-bar 'left' value.
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
				border: 3px outset blue;
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
			QTabWidget::tab-bar {
				left: 22px;
			}
		""")
		self.tabWidgetStyleSheetBase=self.ui.tabWidget.styleSheet()

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

		self.fsSaveLookup()

		self.teamTimer=QTimer(self)
		self.teamTimer.timeout.connect(self.updateTeamTimers)
		self.teamTimer.timeout.connect(self.fsCheck)
		self.teamTimer.timeout.connect(self.updateClock)
		self.teamTimer.start(1000)

		self.slowTimer=QTimer(self)
		self.slowTimer.timeout.connect(self.checkForResize)
		self.slowTimer.start(5000)

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
		# self.NEWFlags=Qt.WindowTitleHint|Qt.WindowStaysOnTopHint
		# self.newEntryWindow.setWindowFlags(self.NEWFlags)
		self.newEntryWindow.setWindowFlags(Qt.WindowTitleHint)

		self.newEntryWindowHiddenPopup=QMessageBox(QMessageBox.NoIcon,'Pending entry','A new entry / clue report / subject-located report is pending, but its window lost focus and may be hidden.\n\nYou can leave this reminder window open, and move it out of the way if needed, while you work in whatever window took focus.',
					QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
		self.newEntryWindowHiddenPopup.button(QMessageBox.Ok).setText('Raise Pending Window')
		self.newEntryWindowHiddenPopup.setModal(False)
		self.newEntryWindowHiddenPopup.buttonClicked.connect(self.newEntryWindowHiddenPopupClicked)
		# it took some googling and experimentation to find the set of window flags that would accomplish these goals
		# - stays on top
		# - has no close X icon at the top right (setting ~Qt.WindowCloseButtonHint didn't seem to work, even with CustomizeWindowHint)
		# - still shows a banner so that the window can be grabbed and moved if needed
		# the same flags don't do the trick inside the QMessageBox constructor for whatever reason
		self.newEntryWindowHiddenPopup.setWindowFlags(Qt.Dialog|Qt.CustomizeWindowHint|Qt.WindowTitleHint|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)

		# make sure x/y/w/h from resource file will fit on the available display
		d=QApplication.desktop()
		if (self.x+self.w > d.width()) or (self.y+self.h > d.height()):
			logging.info("The resource file specifies a main window geometry that is bigger than (or not on) the available desktop.  Using default sizes for this session.")
			self.x=50
			self.y=50
			self.w=d.availableGeometry(self).width()-100
			self.h=d.availableGeometry(self).height()-100
		if (self.clueLog_x+self.clueLog_w > d.width()) or (self.clueLog_y+self.clueLog_h > d.height()):
			logging.info("The resource file specifies a clue log window geometry that is bigger than (or not on) the available desktop.  Using default sizes for this session.")
			self.clueLog_x=75
			self.clueLog_y=75
			self.clueLog_w=d.availableGeometry(self).width()-100
			self.clueLog_h=d.availableGeometry(self).height()-100
		self.setGeometry(int(self.x),int(self.y),int(self.w),int(self.h))
		self.clueLogDialog.setGeometry(int(self.clueLog_x),int(self.clueLog_y),int(self.clueLog_w),int(self.clueLog_h))
		self.fontsChanged()

		#734 move restore to just after fontsChanged, which defines font size variables
		if restoreFlag:
			self.restore()

		self.previousActiveWindowName='None'

		self.ui.timeoutLabel.setText("TIMEOUT:\n"+timeoutDisplayList[self.optionsDialog.ui.timeoutField.value()][0])
		# pop up the options dialog to enter the incident name right away;
		#  if useOperatorLogin is also True, startupOptions will open loginDialog
		#  after the options dialog is closed
		if showStartupOptions:
			QTimer.singleShot(1000,self.startupOptions)
		elif self.useOperatorLogin: # this clause will run for continued incidents
			QTimer.singleShot(1000,self.showLoginDialog)
		# save current resource file, to capture lastFileName without a clean shutdown
		self.saveRcFile()
		self.showTeamTabsMoreButtonIfNeeded()

		# connect inter-thread signals to main-thread slots
		self._sig_caltopoDisconnected.connect(self.caltopoDisconnectedCallback_mainThread)
		self._sig_caltopoReconnected.connect(self.caltopoReconnectedCallback_mainThread)
		self._sig_caltopoReconnectedFromCreateCTS.connect(self.caltopoReconnectedFromCreateCTS_mainThread)
		self._sig_caltopoReconnectedFromOpenMap.connect(self.caltopoReconnectedFromOpenMap_mainThread)
		self._sig_caltopoMapClosed.connect(self.caltopoMapClosedCallback_mainThread)
		# self._sig_caltopoCreateCTSCB.connect(self.caltopoCreateCTSCB_mainThread)

		# # thread/queue/signal mechanism for radio markers, similar to the mechanism more requests in caltopo_python
		# # thread-safe queue to hold marker requests
		# self.radioMarkerQueue=queue.Queue()

		# thread-safe event to tell _radioMarkerWorker to start working through radioMarkerQueue
		self.radioMarkerEvent=threading.Event()

		# the actual radio marker thread
		self.radioMarkerThread=threading.Thread(target=self._radioMarkerWorker,args=(self.radioMarkerEvent,),daemon=True,name='radioMarkerThread')
		self.radioMarkerThread.start()
		self.radioMarkerDictLock=threading.Lock()
		
		self.cts=None
		# self.setupCaltopo()
		self.ui.caltopoLinkIndicator.setToolTip(caltopoIndicatorToolTip)

		# createCTS and openMap need to be done in QThreads so they don't block the waitingspinner
		self.createCTSThread=caltopoCreateCTSThread(self)
		self.createCTSThread.finished.connect(self.createCTSCB)

		self.openMapThread=caltopoOpenMapThread(self)
		self.openMapThread.finished.connect(self.openMapCB)

	def clearSelectionAllTables(self):
		self.ui.tableView.setCurrentIndex(QModelIndex())
		self.ui.tableView.clearFocus() # to get rid of dotted focus box around cell 0,0
		for teamTable in self.ui.tableViewList:
			if not isinstance(teamTable,str): # 'dummy' is the default initial entry
				teamTable.setCurrentIndex(QModelIndex())
				teamTable.clearFocus()

	def getSessions(self,sort='chronological',reverse=False,omitCurrentSession=False,fromCsvFile=None,maxFilesToCheck=999):
		if fromCsvFile:
			sortedCsvFiles=[fromCsvFile]
		else:
			logging.info('gs0')
			csvFiles=glob.glob(self.firstWorkingDir+'/*/*.csv') # files nested in session dirs
			logging.info('gs1')
			# backwards compatibility: also list csv files saved flat in the working dir
			csvFiles+=glob.glob(self.firstWorkingDir+'/*.csv')
			logging.info('gs2')

			# backwards compatibility: look in the old working directory too
			#  copied code from radiolog.py before #522 dir structure overhaul;
			#  could consider removing this in the future, since it grabs all .csv
			#  files from ~\Documents
			oldWD=os.path.join(os.getenv('HOMEPATH','C:\\Users\\Default'),'Documents')
			if oldWD[1]!=":":
				oldWD=os.getenv('HOMEDRIVE','C:')+oldWD

			logging.info('gs3')
			csvFiles+=glob.glob(oldWD+'/*.csv')
			logging.info('gs4')

			csvFiles=[f for f in csvFiles if '_clueLog' not in f and '_fleetsync' not in f and '_bak' not in f and '_fsLog' not in f] # only show 'base' radiolog csv files
			# logging.info(f'csvFiles:{csvFiles}')
			logging.info('gs5')

			csvFiles.sort(key=os.path.getmtime,reverse=reverse)

			logging.info('gs5p1')

			suffix=''
			if len(csvFiles)>maxFilesToCheck:
				suffix=f'  Only checking the {maxFilesToCheck} most recent ones.'
			logging.info(f'Found {len(csvFiles)} .csv files (excluding _clueLog, _fleetsync, _bak, and _fsLog csv files).{suffix}')

			logging.info('gs5p2')

			# only use the (up-to) N most recent files from here on out; this should reduce startup time (i.e. when the file system was asleep)
			csvFilesTmp=[]
			for f in csvFiles:
				if len(csvFilesTmp)<maxFilesToCheck and self.isRadioLogDataFile(f): # isRadioLogDataFile can be expensive, so short-circuit it if needed
					csvFilesTmp.append(f)
			csvFiles=csvFilesTmp

			# csvFiles=[self.isRadioLogDataFile(f) for f in csvFiles] # isRadioLogDataFile returns the first valid filename in the search path, or False if none are valid
			logging.info('gs6')
			csvFiles=[f for f in csvFiles if f] # get rid of 'False' return values from isRadioLogDataFile
			logging.info('gs7')

			#552 remove current session from the list
			if omitCurrentSession:
				csvFiles=[f for f in csvFiles if self.csvFileName not in f]
			logging.info('gs8')

			if sort=='chronological':
				sortedCsvFiles=sorted(csvFiles,key=os.path.getmtime,reverse=reverse)
			elif sort=='alphabetical':
				sortedCsvFiles=sorted(csvFiles,reverse=reverse)
			else:
				sortedCsvFiles=csvFiles
			logging.info('gs9')
		rval=[]
		now=time.time()
		for f in sortedCsvFiles:
			logging.info(f'processing file {f}...')
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
			if '_bak' in f:
				filenameBase=f[:-9]
			incidentName=None
			lastOP=1 # if no entries indicate change in OP#, then initial OP is 1 by default
			clueNames=[]
			lastClue='--'
			clueLogFileName=f.replace('.csv','_clueLog.csv')
			if os.path.isfile(clueLogFileName):
				with open(clueLogFileName,'r') as csvFile:
					csvReader=csv.reader(csvFile)
	##				self.clueLog=[] # uncomment this line to overwrite instead of combine
					for row in csvReader:
						# logging.info(f'row:{row}')
						if not incidentName and '## Incident Name:' in row[0]:
							incidentName=': '.join(row[0].split(': ')[1:]).rstrip() # provide for spaces and ': ' in incident name
						if not row[0].startswith('#'): # ignore comment lines
							# self.clueLog.append(row)
							clueName=''
							if row[0]!="":
								clueName=row[0]
							elif 'Operational Period ' in row[1]:
								logging.info(f't1: row[1]={row[1]}')
								try:
									lastOP=int(re.findall('Operational Period [0-9]+ Begins:',row[1])[-1].split()[2])
								except Exception as e:
									logging.info(str(e)+'\nlastOP could not be parsed as an integer from text "'+row[1]+'"; assuming OP 1')
								try:
									# clueNames=row[1].split('(Last clue number: ')[1].replace(')','')
									clueNames=re.findall('clues? so far for this incident: (.*?)\\)',row[1])[0].split()
								except Exception as e:
									# logging.info(str(e)+'\nLast clue number was not included in Operational Period clue log entry; not recording any previous clues')
									logging.info(str(e)+'\nUsed clue name(s) not included in Operational Period clue log entry; not recording any previous clues')
							if clueName:
								clueNames.append(clueName)
					csvFile.close()
					outList=[]
					if clueNames:
						logging.info(f'pre-parsed clue names list: {clueNames}')
					for clueName in clueNames:
						if '-' in clueName: # numeric range
							(first,last)=clueName.split('-')
							print(f'clueName={clueName}  first={first}  last={last}')
							outList+=[str(x) for x in range(int(first),int(last)+1)]
						else: # signle numeric or non-numeric
							outList.append(clueName)
					clueNames=list(dict.fromkeys(outList)) # quickest way to remove duplicates while preserving order
					if clueNames:
						logging.info(f'parsed clue names list: {clueNames}')
			else:
				logging.info(f'clue log file {clueLogFileName} not found or could not be opened')
			sessionDict=({
				'incidentName':incidentName,
				'lastOP':lastOP,
				'usedClueNames':clueNames,
				'ageStr':ageStr,
				'filenameBase':filenameBase,
				'mtime':mtime})
			# logging.info('session:'+json.dumps(sessionDict,indent=3))
			rval.append(sessionDict)
			# rval.append([incidentName,lastOP or 1,lastClue or 0,ageStr,filenameBase,mtime,clueNames])
		logging.info('gs10')
		if fromCsvFile:
			return rval[0] # there should only be one item - return it as a dict rather than list of dicts
		else:
			return rval # return the whole list of dicts

	# Build a nested list of radiolog session data from any sessions in the last n days;
	#  each list element is [incident_name,last_op#,last_clue#,filename_base]
	#  then let the user choose from these, or choose to start a new incident
	# - only show the most recent OP of each incident, i.e. don't show both OP2 and OP1;
	#    but do show multiple sessions of the same OP# if it's the greatest OP#
	#    which might have happened due to operator error
	# - add a note that the user can change OP and next clue# afterwards from the GUI
	def checkForContinuedIncident(self):
		continuedIncidentWindowDays=self.continuedIncidentWindowDays
		continuedIncidentWindowSec=continuedIncidentWindowDays*24*60*60
		now=time.time()
		opd={} # dictionary of most recent OP#'s per incident name
		choices=[]
		for session in self.getSessions(reverse=True,maxFilesToCheck=20): # limit the number of sessions (should be the number of files) to save time
			# [incidentName,lastOP,lastClue,ageStr,filenameBase,mtime,clueNames]=session
			# logging.info('session:'+json.dumps(session,indent=3))
			incidentName=session['incidentName']
			filenameBase=session['filenameBase']
			if now-session['mtime']<continuedIncidentWindowSec:
				lastOP=session['lastOP']
				if lastOP>=opd.get(incidentName,0):
					choices.append(session)
					opd[incidentName]=lastOP
				else:
					logging.info(f'  not listing {incidentName} OP {lastOP} ({filenameBase}) since OP {opd.get(incidentName,0)} is already listed')
			else:
				break
		if choices:
			logging.info('radiolog sessions from the last '+str(continuedIncidentWindowDays)+' days:')
			logging.info(' (hiding empty sessions; only showing the most recent session of continued incidents)')
			for choice in choices:
				logging.info(choice['filenameBase'])
			cd=continuedIncidentDialog(self)
			cd.ui.theTable.setRowCount(len(choices))
			row=0
			for choice in choices:
				# highestClueNumStr=str(choice['highestClueNumber'])
				highestClueNumStr=str(self.getLastClueNumber(choice['usedClueNames']))
				if highestClueNumStr=='0':
					highestClueNumStr='--'
				q0=QTableWidgetItem(choice['incidentName'])
				q1=QTableWidgetItem(str(choice['lastOP']))
				q2=QTableWidgetItem(highestClueNumStr)
				q3=QTableWidgetItem(choice['ageStr'])
				q0.setData(Qt.UserRole,choice) # store the entire dictionary in UserRole of col 0
				# q0.setToolTip(choice[4])
				# q1.setToolTip(choice[4])
				# q2.setToolTip(choice[4])
				q3.setToolTip(choice['filenameBase'])
				# store the full list of used clue names in the UserRole of the lastClue cell
				# q2.setData(Qt.UserRole,choice['usedClueNames'])
				cd.ui.theTable.setItem(row,0,q0)
				cd.ui.theTable.setItem(row,1,q1)
				cd.ui.theTable.setItem(row,2,q2)
				cd.ui.theTable.setItem(row,3,q3)
				row+=1
			cd.show()
			cd.raise_()
			cd.exec_()
		else:
			logging.info('no csv files from the last '+str(continuedIncidentWindowDays)+' days.')
	
	def isRadioLogDataFile(self,filename):
		# logging.info('checking '+filename)
		# since this check is used to build the list of previous sessions, return True
		#  if there is a valid _bak csv, even if the primary is corrupted
		filenameList=[filename]
		for n in range(1,6):
			filenameList.append(filename.replace('.csv','_bak'+str(n)+'.csv'))
		for filename in filenameList:
			# if filename.endswith('.csv') and os.path.isfile(filename): # this line is not needed
			try: # in case the file is corrupted or not found
				with open(filename,'r') as f:
					if '## Radio Log data file' in f.readline():
						return filename # return whichever filename was valid
			except:
				pass
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
		self.continueSec="20"
		self.fsBypassSequenceChecks=False
		self.caltopoIntegrationDefault=False
		self.caltopoAccountName="NONE"
		self.caltopoDefaultTeamAccount=None
		self.caltopoMapMarkersDefault=False
		self.caltopoWebBrowserDefault=False
		
		if os.name=="nt":
			logging.info("Operating system is Windows.")
			if shutil.which("powershell.exe"):
				logging.info("PowerShell.exe is in the path.")
				#601 - use absolute path
				#643: use an argument list rather than a single string;
				# as long as -File is in the argument list immediately before the script name,
				# spaces in the script name and in arguments will be handled correctly;
				# see comments at the end of https://stackoverflow.com/a/44250252/3577105
				self.rotateScript=''
				self.rotateCmdArgs=['powershell.exe','-ExecutionPolicy','Bypass','-File',installDir+'\\rotateCsvBackups.ps1','-filenames']
			else:
				logging.info("PowerShell.exe is not in the path; poweshell-based backup rotation script cannot be used.")
		else:
			logging.info("Operating system is not Windows.  Powershell-based backup rotation script cannot be used.")

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
				self.rotateCmdArgs=[self.rotateScript]
			elif tokens[0]=="rotateDelimiter":
				self.rotateDelimiter=tokens[1]
			elif tokens[0]=="tabGroups":
				self.tabGroups=eval(tokens[1])
			elif tokens[0]=="continuedIncidentWindowDays":
				self.continuedIncidentWindowDays=tokens[1]
			elif tokens[0]=='useOperatorLogin':
				try:
					self.useOperatorLogin=eval(tokens[1])
				except:
					pass
			elif tokens[0]=='capsList':
				global capsList
				capsList=eval(tokens[1])
			elif tokens[0]=='CCD1List':
				self.CCD1List=eval(tokens[1])
				# KW- should always be a part of CCD1List
				if 'KW-' not in self.CCD1List:
					self.CCD1List.append('KW-')
			elif tokens[0]=='continueSec':
				self.continueSec=tokens[1]
			elif tokens[0]=='fsBypassSequenceChecks':
				self.fsBypassSequenceChecks=tokens[1]
			elif tokens[0]=='caltopoIntegrationDefault':
				self.caltopoIntegrationDefault=tokens[1]
			elif tokens[0]=='caltopoAccountName':
				self.caltopoAccountName=tokens[1]
			elif tokens[0]=='caltopoDefaultTeamAccount':
				self.caltopoDefaultTeamAccount=tokens[1]
			elif tokens[0]=='caltopoMapMarkersDefault':
				self.caltopoMapMarkersDefault=tokens[1]
			elif tokens[0]=='caltopoWebBrowserDefault':
				self.caltopoWebBrowserDefault=tokens[1]
					
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
		
		if not self.continueSec.isdigit():
			configErr+="ERROR: continueSec value must be an integer.  Will use 20 seconds for this session.\n\n"
		self.continueSec=int(self.continueSec)

		if self.fsBypassSequenceChecks and self.fsBypassSequenceChecks not in ['True','False']:
			configErr+='ERROR: fsBypassSequenceChecks value must be True or False.  Will set to False by default.'
			self.fsBypassSequenceChecks='False'
		if type(self.fsBypassSequenceChecks)==str:
			self.fsBypassSequenceChecks=eval(self.fsBypassSequenceChecks)
		if self.fsBypassSequenceChecks:
			logging.info('FleetSync / NEXEDGE sequence checks will be bypassed for this session; every part of every incoming message will raise a new entry popup if needed.')

		if self.caltopoIntegrationDefault and self.caltopoIntegrationDefault not in ['True','False']:
			configErr+='ERROR: caltopoIntegrationDefault value must be True or False.  Will set to False by default.'
			self.caltopoIntegrationDefault='False'
		if type(self.caltopoIntegrationDefault)==str:
			self.caltopoIntegrationDefault=eval(self.caltopoIntegrationDefault)
			
		if self.caltopoMapMarkersDefault and self.caltopoMapMarkersDefault not in ['True','False']:
			configErr+='ERROR: caltopoMapMarkersDefault value must be True or False.  Will set to False by default.'
			self.caltopoMapMarkersDefault='False'
		if type(self.caltopoMapMarkersDefault)==str:
			self.caltopoMapMarkersDefault=eval(self.caltopoMapMarkersDefault)
			
		if self.caltopoWebBrowserDefault and self.caltopoWebBrowserDefault not in ['True','False']:
			configErr+='ERROR: caltopoWebBrowserDefault value must be True or False.  Will set to False by default.'
			self.caltopoWebBrowserDefault='False'
		if type(self.caltopoWebBrowserDefault)==str:
			self.caltopoWebBrowserDefault=eval(self.caltopoWebBrowserDefault)

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
		# if self.rotateScript and self.rotateDelimiter:
			# #442: wrap each filename in quotes, to allow spaces in filenames
			#  from https://stackoverflow.com/a/12007707
			#  wrapping in one or two sets of double quotes still doesn't work
			#   since the quotes are stripped by powershell; wrapping in three
			#   double quotes does work:
			# quotedFilenames=[f'"""{filename}"""' for filename in filenames]
			# cmd=self.rotateScript+' '+self.rotateDelimiter.join(quotedFilenames)
		if self.rotateCmdArgs and isinstance(self.rotateCmdArgs,list) and self.rotateCmdArgs[0]:
			#643: use an argument list rather than a single string;
			# as long as -File is in the argument list immediately before the script name,
			# spaces in the script name and in arguments will be handled correctly;
			# see comments at the end of https://stackoverflow.com/a/44250252/3577105;
			# (this elimiates the need to wrap things in three sets of double quotes per #442)
			cmd=self.rotateCmdArgs+filenames
			logging.info("Invoking backup rotation script (with arguments): "+str(cmd))
			# #650, #651 - fail gracefully, so that the caller can proceed as normal
			try:
				subprocess.Popen(cmd)
			except Exception as e:
				logging.info("  Backup rotation script failed with this exception; proceeding:"+str(e))
		else:
			logging.info("No backup rotation script was specified; no rotation is being performed.")
		
	def updateOptionsDialog(self):
		# logging.info("updating options dialog: datum="+self.datum)
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
			
	def fsFilterEdit(self,fleetOrBlank,devOrUid,state=True):
# 		logging.info("editing filter for "+str(fleet)+" "+str(dev))
		for row in self.fsLog:
# 			logging.info("row:"+str(row))
			if row[0]==fleetOrBlank and row[1]==devOrUid:
# 				logging.info("found")
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
		# logging.info('fsGetTeamDevices called for extTeamName='+extTeamName)
		# logging.info('self.fsLog='+str(self.fsLog))
		rval=[]
		for row in self.fsLog:
			if getExtTeamName(row[2])==extTeamName:
				rval.append([row[0],row[1]])
		# logging.info('returning '+str(rval))
		return rval
		
	def fsFilteredCallDisplay(self,state='off',fleetOrBlank='',devOrUid='',callsign=''):
		if fleetOrBlank: # fleetsync
			typeStr='FleetSync'
			idStr=fleetOrBlank+':'+devOrUid
		else: #nexedge
			typeStr='NEXEDGE'
			idStr=devOrUid
		if state=='on':
			self.ui.incidentNameLabel.setText(typeStr+' filtered:\n'+callsign+'   ('+idStr+')')
			self.ui.incidentNameLabel.setStyleSheet('background-color:#ff5050;color:white;font-size:'+str(int(self.limitedFontSize*3/4))+'pt')
		elif state=='bump':
			self.ui.incidentNameLabel.setText('Mic bump filtered:\n'+callsign+'   ('+idStr+')')
			self.ui.incidentNameLabel.setStyleSheet('background-color:#5050ff;color:white;font-size:'+str(int(self.limitedFontSize*3/4))+'pt')
		else:
			self.ui.incidentNameLabel.setText(self.incidentName)
			self.ui.incidentNameLabel.setStyleSheet('background-color:none;color:black;font-size:'+str(self.limitedFontSize)+'pt')
				
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
			logging.info("FleetSync is now muted")
			self.fsMuteBlink("on") # blink on immediately so user sees immediate response
		else:
			if self.noSend:
				logging.info("Fleetsync is unmuted but locator requests will not be sent")
				self.fsMuteBlink("noSend")
			else:
				logging.info("Fleetsync is unmuted and locator requests will be sent")
				self.fsMuteBlink("off")
				self.ui.incidentNameLabel.setText(self.incidentName)
				self.ui.incidentNameLabel.setStyleSheet("background-color:none;color:black;font-size:"+str(self.limitedFontSize)+"pt;")
			
	# FleetSync / NEXEDGE - check for pending data
	# - check for pending data at regular interval (from timer)
	#     (it's important to check for ID-only lines, since handhelds with no
	#      GPS mic will not send $PKLSH / $PKNSH but we still want to spawn a new entry
	#      dialog; and, $PKLSH / $PKNSH isn't necessarily sent on BOT (Beginning of Transmission) anyway)
	#     (for 1 second interval, ID-only is always processed separately from $PKLSH/ $PKNSH;
	#     even for 2 second interval, sometimes ID is processed separately.
	#     So, if $PKLSH / $PKNSH is processed, add coords to any rececntly-spawned
	#     'from' new entry dialog for the same fleetsync / nexedge id.)
	# - append any pending data to fsBuffer
	# - if a clean end of transmission packet is included in this round of data,
	#    spawn a new entry window (unless one is already open with 'from'
	#    and the same fleetsync / nexedge ID) with any geographic data
	#    from the current fsBuffer, then empty the fsBuffer

	# NOTE that the data coming in is bytes b'1234' but we want string; use bytes.decode('utf-8') to convert,
	#  after which /x02 (a.k.a. STX a.k.a. Start of Text) will show up as a happy face 
	#  and /x03 (a.k.a. ETX a.k.a. End of Text) will show up as a heart on standard ASCII display.

	def fsCheck(self):
		if self.fsAwaitingResponse:
			if self.fsAwaitingResponse[3]>=self.fsAwaitingResponseTimeout:
				logging.info('Timed out awaiting FleetSync or NEXEDGE response')
				self.fsFailedFlag=True
				try:
					self.fsTimedOut=True
					self.fsAwaitingResponseMessageBox.close()
				except:
					pass
				# logging.info('q1: fsThereWillBeAnotherTry='+str(self.fsThereWillBeAnotherTry))
				if not self.fsThereWillBeAnotherTry:
					# values format for adding a new entry:
					#  [time,to_from,team,message,self.formattedLocString,status,self.sec,self.fleet,self.dev,self.origLocString]
					values=["" for n in range(10)]
					values[0]=time.strftime("%H%M")
					values[6]=time.time()
					[f,dev]=self.fsAwaitingResponse[0:2]
					if f: # fleetsync
						callsignText=self.getCallsign(f,dev)
						h='FLEETSYNC'
						idStr=f+':'+dev
					else: # nexedge
						uid=dev
						callsignText=self.getCallsign(uid)
						h='NEXEDGE'
						idStr=uid
					values[2]=str(callsignText)
					if callsignText:
						callsignText='('+callsignText+')'
					else:
						callsignText='(no callsign)'
					if self.fsAwaitingResponse[2]=='Location request sent':
						values[3]=h+': No response received for location request from '+idStr+' '+callsignText
					elif self.fsAwaitingResponse[2]=='Text message sent':
						msg=self.fsAwaitingResponse[4]
						values[1]='TO'
						values[3]=h+': Text message sent to '+idStr+' '+callsignText+' but delivery was NOT confirmed: "'+msg+'"'
					else:
						values[3]=h+': Timeout after unknown command type "'+self.fsAwaitingResponse[2]+'"'

					self.newEntry(values)
					msg='No '+h+' response: unable to confirm that the message was received by the target device(s).'
					if self.fsAwaitingResponse[2]=='Location request sent':
						msg+='\n\nThis could happen after a location request for one of several reasons:\n  - The radio in question was off\n  - The radio in question was on, but not set to this channel\n  - The radio in question was on and set to this channel, but had no GPS fix'
					self.fsAwaitingResponse=None # clear the flag
					if len(self.fsSendList)==1:
						box=QMessageBox(QMessageBox.Critical,h+' timeout',msg,
							QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
						box.open()
						box.raise_()
						box.exec_()
					else:
						self.fsResponseMessage+='\n\n'+idStr+' '+callsignText+': '+msg
			else:
				remaining=self.fsAwaitingResponseTimeout-self.fsAwaitingResponse[3]
				suffix=''
				if remaining!=1:
					suffix='s'
				msg=re.sub('[0-9]+ more seconds',str(remaining)+' more second'+suffix,self.fsAwaitingResponseMessageBox.text())
				self.fsAwaitingResponseMessageBox.setText(msg)
				self.fsAwaitingResponse[3]+=1
		if not (self.firstComPortFound and self.secondComPortFound): # correct com ports not yet found; scan for waiting fleetsync data
			if not self.comPortScanInProgress: # but not if this scan is already in progress (taking longer than 1 second)
				if comLog:
					logging.info("Two COM ports not yet found.  Scanning...")
				self.comPortScanInProgress=True
				# opening a port quickly, checking for waiting input, and closing on each iteration does not work; the
				#  com port must be open when the input begins, in order to catch it in the inWaiting internal buffer.
				# 1. go through each already-open com port to check for waiting data; if valid Fleetsync data is
				#     found, then we have the correct com port, abort the rest of the scan
				# 2. (only if no valid data was found in step 1) list com ports; open any new finds and close any
				#     stale ports (i.e. existed in the list in previous iterations but not in the list now)
				for comPortTry in self.comPortTryList:
					if comLog:
						logging.info("  Checking buffer for already-open port "+comPortTry.name)
					try:
						isWaiting=comPortTry.inWaiting()
					except serial.serialutil.SerialException as err:
						if "ClearCommError failed" in str(err):
							logging.info("  COM port unplugged.  Scan continues...")
							self.comPortTryList.remove(comPortTry)
					except:
						pass # unicode decode errors may occur here for non-radio com devices
					else:
						if isWaiting:
							logging.info("     DATA IS WAITING!!!")
							valid=False
							tmpData=comPortTry.read(comPortTry.inWaiting()).decode("utf-8")
							if '\x02I' in tmpData or tmpData=='\x020\x03' or tmpData=='\x021\x03' or tmpData.startswith('\x02$PKL'):
								logging.info("      VALID FLEETSYNC DATA!!!")
								valid=True
							elif '\x02gI' in tmpData:
								logging.info('      VALID NEXEDGE DATA!!!')
								valid=True
								# NEXEDGE format (e.g. for ID 03001; NXDN has no concept of fleet:device - just 5-decimal-digit unit ID, max=65536 (4 hex characters))
								# BOT CID: ☻gI1U03001U03001♥
								# EOT CID: ☻gI0U03001U03001♥
								#   ☻gI - preamble (\x02gI)
								#   BOT/EOT - BOT=1, EOT=0
								#   U##### - U followed by unit ID (5 decimal digits)
								#   repeat U#####
								#   ♥ - postamble (\x03)
								# GPS: same as with fleetsync, but PKNSH instead of PKLSH; arrives immediately after BOT CID rather than EOT CID
							else:
								logging.info("      but not valid FleetSync or NEXEDGE data.  Scan continues...")
								logging.info(str(tmpData))
							if valid:
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
							if comLog:
								logging.info("     no data")
				for portIterable in serial.tools.list_ports.comports():
					if portIterable[0] not in [x.name for x in self.comPortTryList]:
						try:
							self.comPortTryList.append(serial.Serial(portIterable[0]))
						except:
							pass
						else:
							logging.info("  Opened newly found port "+portIterable[0])
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
					logging.info("first COM port unplugged")
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
					logging.info("second COM port unplugged")
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
		logging.info("PARSING")
		logging.info(self.fsBuffer)
		origLocString=''
		formattedLocString=''
		callsign=''
		self.getString=''
		sec=time.time()
		fleet=None
		dev=None
		uid=None
		seq=[]
		prevSeq=[]
		# the line delimeters are literal backslash then n, rather than standard \n
		for line in self.fsBuffer.split('\n'):
			logging.info(" line:"+line)
			# initialize valid/lat/lon/devTxt for use during mic bump handling
			valid=''
			lat=''
			lon=''
			devTxt=''
			if line=='\x020\x03':
				# success response code - happens in these cases:
				# - positive acknowledge received after text sent to individual device
				# - broadcast text sent (target radios will not try to respond to broadcast)
				# - positive acknowledge received after location poll, regardless of response from portable radio;
				#     if target radio has a GPS lock, either current (A status) or stale (V status), 
				#     the next lines will include $PKLSH etc.  In this case, there is no action to take;
				#     just move on to the next line.
				if self.fsAwaitingResponse and self.fsAwaitingResponse[2]=='Text message sent':
					[fleet,dev]=self.fsAwaitingResponse[0:2]
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
					if int(dev)==0:
						recipient='all devices'
						values[2]='ALL'
					else:
						if fleet: # fleetsync
							callsignText=self.getCallsign(fleet,dev)
							idStr=fleet+':'+dev
							h='FLEETSYNC'
						else: # nexedge
							uid=dev
							callsignText=self.getCallsign(uid)
							idStr=uid
							h='NEXEDGE'
						values[2]=str(callsignText)
						if callsignText:
							callsignText='('+callsignText+')'
						else:
							callsignText='(no callsign)'
						recipient=idStr+' '+callsignText
						suffix=' and delivery was confirmed'
					values[3]=h+': Text message sent to '+recipient+suffix+': "'+msg+'"'
					values[6]=time.time()
					self.newEntry(values)
					logging.info(h+': Text message sent to '+recipient+suffix)
					return
			if line=='\x021\x03': # failure response
				if self.fsAwaitingResponse:
					# logging.info('q2: fsThereWillBeAnotherTry='+str(self.fsThereWillBeAnotherTry))
					if not self.fsThereWillBeAnotherTry:
						# values format for adding a new entry:
						#  [time,to_from,team,message,self.formattedLocString,status,self.sec,self.fleet,self.dev,self.origLocString]
						values=["" for n in range(10)]
						values[0]=time.strftime("%H%M")
						[fleet,dev]=self.fsAwaitingResponse[0:2]
						if fleet: # fleetsync
							callsignText=self.getCallsign(fleet,dev)
							idStr=fleet+':'+dev
							h='FLEETSYNC'
						else: # nexedge
							uid=dev
							callsignText=self.getCallsign(uid)
							idStr=uid
							h='NEXEDGE'
						values[2]=str(callsignText)
						if callsignText:
							callsignText='('+callsignText+')'
						else:
							callsignText='(no callsign)'
						recipient=idStr+' '+callsignText
						values[3]=h+': NO RESPONSE from '+recipient
						values[6]=time.time()
						self.newEntry(values)
						self.fsFailedFlag=True
						try:
							self.fsAwaitingResponseMessageBox.close()
						except:
							pass
						self.fsAwaitingResponse=None # clear the flag
						logging.info(h+': NO RESPONSE from '+recipient)
						return
			if '$PKLSH' in line or '$PKNSH' in line: # handle fleetsync and nexedge in this 'if' clause
				seq.append('GPS')
				lineParse=line.split(',')
				header=lineParse[0] # $PKLSH or $PKNSH, possibly following CID STX thru ETX
				gpsAfterMicBump=False # flag that allows the radio marker to be sent, but doesn't spawn a new entry
				# logging.info('header:'+header+'  tokens:'+str(len(lineParse)))
				# if CID packet(s) came before $PKLSH on the same line, that's OK since they don't have any commas
				if '$PKLSH' in header: # fleetsync
					if len(lineParse)==10:
						[header,nval,nstr,wval,wstr,utc,valid,fleet,dev,chksum]=lineParse
						uid=''
						callsign=self.getCallsign(fleet,dev)
						idStr=fleet+':'+dev
						h='FLEETSYNC'
						logging.info("$PKLSH (FleetSync) detected containing CID: fleet="+fleet+"  dev="+dev+"  -->  callsign="+callsign)
						# 744 - if there was a filtered mic bump from this device within the last two seconds,
						#  and the current line doesn't contain a FS or NXDN CID prefix (BOT or EOT), then skip this GPS-only line completely
						latestMicBump=self.latestBumpDict.get(str(fleet)+':'+str(dev),0)
						if time.time()-latestMicBump<2 and not '\x02I' in line and not '\x02gI' in line:
							logging.info('latest filtered mic bump for this device:'+str(latestMicBump)+'  ('+str(time.time()-latestMicBump)+' seconds ago)')
							logging.info(' this was within the last two seconds, and this line has no CID data; will send radio marker data, but otherwise skipping this GPS-only line, as part of the same mic bump')
							gpsAfterMicBump=True
							# return
					else:
						logging.info("Parsed $PKLSH line contained "+str(len(lineParse))+" tokens instead of the expected 10 tokens; skipping.")
						origLocString='BAD DATA'
						formattedLocString='BAD DATA'
						continue
				elif '$PKNSH' in header: # nexedge
					if len(lineParse)==9:
						[header,nval,nstr,wval,wstr,utc,valid,uid,chksum]=lineParse
						fleet=''
						dev=''
						uid=uid[1:] # get rid of the leading 'U'
						callsign=self.getCallsign(uid)
						idStr=uid
						h='NEXEDGE'
						logging.info("$PKNSH (NEXEDGE) detected containing CID: Unit ID = "+uid+"  -->  callsign="+callsign)
					else:
						logging.info("Parsed $PKNSH line contained "+str(len(lineParse))+" tokens instead of the expected 9 tokens; skipping.")
						origLocString='BAD DATA'
						formattedLocString='BAD DATA'
						continue

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
				#   to update the caltopo locator.
				# - iv valid=='V', append the formatted string with an asterisk, but do not update the locator
				# - if valid=='A' - as with old radios
				# so:
				# if valid=='A':  # only process if there is a GPS lock
				#
				# $PKNSH (NEXEDGE equivalent of $PKLSH) - has one less comma-delimited token than $PKLSH
				#  U01001 = unit ID 01001
				# $PKNSH,3916.1154,N,12101.6008,W,123456,A,U01001,*4C

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
						logging.info("Valid location string:'"+origLocString+"'")
						formattedLocString=self.convertCoords(locList,self.datum,self.coordFormat)
						logging.info("Formatted location string:'"+formattedLocString+"'")
						[lat,lon]=self.convertCoords(locList,targetDatum="WGS84",targetFormat="D.dList")
						logging.info("WGS84 lat="+str(lat)+"  lon="+str(lon))
						if valid=='A': # don't update the locator if valid=='V'
							# sarsoft requires &id=FLEET:<fleet#>-<deviceID>
							#  fleet# must match the locatorGroup fleet number in sarsoft
							#  but deviceID can be any text; use the callsign to get useful names in sarsoft
							if callsign.startswith("KW-"):
								# did not find a good callsign; use the device number in the GET request
								devTxt=dev or uid
							else:
								# found a good callsign; use the callsign in the GET request
								devTxt=callsign
							# for sending locator updates, assume fleet 100 for now - this may be dead code soon - see #598
							self.getString="http://"+self.sarsoftServerName+":8080/rest/location/update/position?lat="+str(lat)+"&lng="+str(lon)+"&id=FLEET:"+(fleet or '100')+"-"
							# if callsign = "Radio ..." then leave the getString ending with hyphen for now, as a sign to defer
							#  sending until accept of change callsign dialog, or closeEvent of newEntryWidget, whichever comes first;
							#  otherwise, append the callsign now, as a sign to send immediately

							# TODO: change this hardcode to deal with other default device names - see #635
							if not devTxt.startswith("Radio "):
								self.getString=self.getString+devTxt
							# if self.optionsDialog.ui.caltopoRadioMarkersCheckBox.isChecked() and self.cts:
							self.sendRadioMarker(fleet,dev,uid,devTxt,lat,lon,bump=gpsAfterMicBump) # always send or queue
							if gpsAfterMicBump:
								return # deferred return from above to here, so that the radio marker can still be sent

						# was this a response to a location request for this device?
						if self.fsAwaitingResponse and [fleet,dev]==[x for x in self.fsAwaitingResponse[0:2]]:
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
							# callsignText=self.getCallsign(fleet,dev)
							values[2]=callsign or ''
							if callsign:
								callsignText='('+callsign+')'
							else:
								callsignText='(no callsign)'
							values[3]=h+' LOCATION REQUEST: '+prefix+' from device '+idStr+' '+callsignText
							values[6]=time.time()
							self.newEntry(values)
							logging.info(values[3])
							t=self.fsAwaitingResponse[2]
							self.fsAwaitingResponse=None # clear the flag
							self.fsAwaitingResponseMessageBox=QMessageBox(QMessageBox.Information,t,values[3]+':\n\n'+formattedLocString+'\n\nNew entry created with response coordinates.',
											QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
							self.fsAwaitingResponseMessageBox.show()
							self.fsAwaitingResponseMessageBox.raise_()
							self.fsAwaitingResponseMessageBox.exec_()
							return # done processing this traffic - don't spawn a new entry dialog
					else:
						logging.info('INVALID location string parsed from '+header+': "'+origLocString+'"')
						origLocString='INVALID'
						formattedLocString='INVALID'
				elif valid=='Z':
					origLocString='NO FIX'
					formattedLocString='NO FIX'
				elif valid=='V':
					logging.info('WARNING status character parsed from '+header+'; check the GPS mic attached to that radio')
					origLocString='WARNING'
					formattedLocString='WARNING'
				else:
					origLocString='UNDEFINED'
					formattedLocString='UNDEFINED'
			if '\x02I' in line: # fleetsync CID - 'if' rather than 'elif' means that self.getString is available to send to sartopo
				# caller ID lines look like " I110040021004002" (first character is \x02, may show as a space)
				# " I<n>" is a prefix, n is either 1 (BOT) or 0 (EOT)
				# the next three characters (100 above) are the fleet#
				# the next four characters (4002 above) are the device#
				# fleet and device# are repeated
				# apparently a delay elsewhere can result in an extra leading character here;
				#  so, find the exact characters rather than assuming character index

				# 1. parse line into unique complete packets,
				#   where 'packet' is defined here as an unbroken string of 6 to 19 digits between '\x02I[1=BOT or 0=EOT]' and '\x03'
				#   normally, there is only one packet per parsed buffered line;
				#    for a mic bump, a BOT packet will be immediately followed by an EOT packet - though the EOT may not show
				#    up until the subsequent buffered line (the subsequent fsParse call);
				#    even for a mic bump, the second packet is identical to the first, so set() will only have one member;
				#    if set length != 1 then we know there's garbled data and there's nothing else we can do here
				if('\x02I1') in line:
					seq.append('BOT')
				if('\x02I0') in line:
					seq.append('EOT')
				packetSet=set(re.findall('\x02I[0-1]([0-9]{6,19})\x03',line))
				# logging.info('FleetSync packetSet: '+str(list(packetSet)))
				if len(packetSet)>1:
					logging.info('FLEETSYNC ERROR: data appears garbled; there are two complete but non-identical CID packets.  Skipping this message.')
					return
				if len(packetSet)==0:
					logging.info('FLEETSYNC ERROR: data appears garbled; no complete CID packets were found in the incoming data.  Skipping this message.')
					return
				packet=packetSet.pop()
				count=line.count(packet)
				# logging.info('packet:'+str(packet))
				# logging.info('packet count on this line: '+str(count))
				
				# 2. within a well-defined packed, the 7-digit fid (fleet&ID) should begin at index 0 (first character)
				fid=packet[0:7] # returns indices 0 thru 6 = 7 digits
				# it's not clear whether this must-repeat-within-packet requirement is universal for all users;
				#  keep the code handy but commented out for now, if a need arises to become more strict about
				#  filtering garbled data.  For now, limiting this to complete-packets-only may be sufficient
				# if packet[8:15]!=fid:
				# 	logging.info('FLEETSYNC ERROR: Fleet&ID 7-digit sequence is not repeated within the packet.  Skipping this message.')
				# 	return
				fleet=fid[0:3]
				dev=fid[3:7]
				callsign=self.getCallsign(fleet,dev)

				# passive mic bump filter: if BOT and EOT packets are in the same line, return without opening a new dialog
				if count>1:
					logging.info(' Mic bump filtered from '+callsign+' (FleetSync)')
					self.fsFilteredCallDisplay() # blank for a tenth of a second in case of repeated bumps
					QTimer.singleShot(200,lambda:self.fsFilteredCallDisplay('bump',fleet,dev,callsign))
					QTimer.singleShot(5000,self.fsFilteredCallDisplay) # no arguments will clear the display
					self.fsLogUpdate(fleet=fleet,dev=dev,bump=True,seq=seq,result='bump')
					self.sendPendingGet() # while getString will be non-empty if this bump had GPS, it may still have the default callsign
					if valid=='A':
						self.sendRadioMarker(fleet,dev,None,devTxt,lat,lon,bump=True)
					return
					
				logging.info("FleetSync CID detected (not in $PKLSH): fleet="+fleet+"  dev="+dev+"  callsign="+callsign)

			elif '\x02gI' in line: # NEXEDGE CID - similar to above
				if('\x02gI1') in line:
					seq.append('BOT')
				if('\x02gI0') in line:
					seq.append('EOT')
				match=re.findall(r'\x02gI[0-1](U\d{5}U\d{5})\x03',line)
				# logging.info('match:'+str(match))
				packetSet=set(match)
				# logging.info('NXDN packetSet: '+str(list(packetSet)))
				if len(packetSet)>1:
					logging.info('NEXEDGE ERROR: data appears garbled; there are two complete but non-identical CID packets.  Skipping this message.')
					return
				if len(packetSet)==0:
					logging.info('NEXEDGE ERROR: data appears garbled; no complete CID packets were found in the incoming data.  Skipping this message.')
					return
				packet=packetSet.pop()
				count=line.count(packet)
				# logging.info('packet:'+str(packet))
				# logging.info('packet count on this line: '+str(count))
				uid=packet[1:6] # 'U' not included - this is a 5-character string of integers
				callsign=self.getCallsign(uid)

				# passive mic bump filter: if BOT and EOT packets are in the same line, return without opening a new dialog
				if count>1:
					logging.info(' Mic bump filtered from '+callsign+' (NEXEDGE)')
					self.fsFilteredCallDisplay() # blank for a tenth of a second in case of repeated bumps
					QTimer.singleShot(200,lambda:self.fsFilteredCallDisplay('bump',None,uid,callsign))
					QTimer.singleShot(5000,self.fsFilteredCallDisplay) # no arguments will clear the display
					self.fsLogUpdate(uid=uid,bump=True,seq=seq,result='bump')
					self.sendPendingGet() # while getString will be non-empty if this bump had GPS, it may still have the default callsign
					if valid=='A':
						self.sendRadioMarker(None,None,uid,devTxt,lat,lon,bump=True)
					return
				
				logging.info('NEXEDGE CID detected (not in $PKNSH): id='+uid+'  callsign='+callsign)

		#722 - BOT/EOT/GPS-based rules to reduce excessive new entry widgets
		if self.fsBypassSequenceChecks:
			attemptNEW=True
		else:
			if fleet:
				prevSeq=self.fsGetPrevSeq(fleet,dev)
			elif uid:
				prevSeq=self.fsGetPrevSeq(uid)
			logging.info('prevSeq:'+str(prevSeq))
			attemptNEW=False
			if 'BOT' in seq:
				attemptNEW=True
			elif 'EOT' in seq: # BOT+EOT will not land here - it would be filtered as a mic bump
				if 'BOT' not in prevSeq: # maybe a previous BOT was garbled or lost, so try now
					attemptNEW=True
				if 'BOT' in prevSeq and 'EOT' in prevSeq: # previous was a bump; maybe BOT since then was garbled or lost, so try now
					attemptNEW=True
			elif 'GPS' in seq: # EOT+GPS will not land here, since it was caught above
				if 'BOT' not in prevSeq and 'EOT' not in prevSeq:
					attemptNEW=True
		# if any new entry dialogs are already open with 'from' and the
		#  current callsign, and that entry has been edited within the 'continue' time,
		#  update it with the current location if available;
		# otherwise, spawn a new entry dialog
		found=False
		widget=None
		logging.info(f'checking for existing open new entry tabs: fleet={fleet} dev={dev} callsign="{callsign}" continueSec={self.continueSec}')
		for widget in newEntryWidget.instances:
			logging.info(f'checking against existing widget: fleet={widget.fleet} dev={widget.dev} to_from={widget.ui.to_fromField.currentText()} team="{widget.ui.teamField.text()}" lastModAge={widget.lastModAge}')
			# #452 - do a case-insensitive and spaces-removed comparison, in case Sar 1 and SAR 1 both exist, or trans 1 and Trans 1 and TRANS1, etc.
			#742 - don't open a new entry if the existing new entry widget has a child clue or subject dialog open
			# if widget.ui.to_fromField.currentText()=="FROM" and widget.ui.teamField.text().lower().replace(' ','')==callsign.lower().replace(' ','') and widget.lastModAge<continueSec:
			if widget.ui.to_fromField.currentText()=="FROM" and (widget.ui.teamField.text().lower().replace(' ','')==callsign.lower().replace(' ','') or (widget.fleet==fleet and widget.dev==dev)):
				if widget.lastModAge<self.continueSec:
					logging.info("  new entry widget is already open from this device or callsign within the 'continue time'")
					found='continue'
				elif widget.childDialogs:
					logging.info('  new entry widget is already open that has child dialog/s (clue or subject located)')
					found='child'
				if found:
##				widget.timer.start(newEntryDialogTimeoutSeconds*1000) # reset the timeout
				# found=True
				# logging.info("  new entry widget is already open from this callsign within the 'continue time'; not opening a new one")
					prevLocString=widget.ui.radioLocField.toPlainText()
					# if previous location string was blank, always overwrite;
					#  if previous location string was not blank, only overwrite if new location is valid
					# logging.info('t1: prevLocString='+str(prevLocString)+'  formattedLocString='+str(formattedLocString))
					# 753 - fix the logic that determines whether update should be attempted
					if formattedLocString!='' and formattedLocString not in ['BAD DATA','NO FIX','WARNING','UNDEFINED','INVALID']:
						datumFormatString="("+self.datum+"  "+self.coordFormat+")"
						if widget.relayed:
							logging.info("location strings not updated because the message is relayed")
							widget.radioLocTemp=formattedLocString
							widget.datumFormatTemp=datumFormatString
						else:
							logging.info("location strings updated because the message is not relayed")
							widget.ui.radioLocField.setText(formattedLocString)
							widget.ui.datumFormatLabel.setText(datumFormatString)
							widget.formattedLocString=formattedLocString
							widget.origLocString=origLocString
					# #509: populate radio location field in any child dialogs that have that field (clue or subject located)
					for child in widget.childDialogs:
						logging.info('  new entry widget for '+str(callsign)+' has a child dialog; attempting to update radio location in that dialog')
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
							# 753 - confirmed the decision to only keep the first valid location; clean up the logic
							if prevLocString=='' and formattedLocString!='' and formattedLocString not in ['BAD DATA','NO FIX','WARNING','UNDEFINED','INVALID']:
								child.ui.radioLocField.setText(formattedLocString)
						except:
							pass
					break # to preserve 'widget' variable for use below
		#750 reset team timer here, regardless of whether a new entry is opened
		#  but only if the the team's timer already exists, to prevent error in updateTeamTimers
		extTeamName=getExtTeamName(callsign)
		if extTeamName in teamTimersDict:
			teamTimersDict[extTeamName]=0
		if fleet and dev:
			fsResult=found # False or 'continue' or 'child'
			resultSuffix=''
			# only open a new entry widget if none is alredy open within the continue time, 
			#  and the fleet/dev is not being filtered
			if not found:
				if self.fsIsFiltered(fleet,dev):
					fsResult='filtered'
					self.fsFilteredCallDisplay("on",fleet,dev,callsign)
					QTimer.singleShot(5000,self.fsFilteredCallDisplay) # no arguments will clear the display
				else:
					if attemptNEW:
						fsResult='newEntry'
						logging.info('no other new entry tab was found for this callsign; inside fsParse: calling openNewEntry')
						resultSuffix=self.openNewEntry('fs',callsign,formattedLocString,fleet,dev,origLocString)
						widget=self.newEntryWidget # the widget created by openNewEntry
					else:
						logging.info('no other entry was found, but due to sequence checking, no new entry will be created')
						fsResult='skipped'
			if not attemptNEW: # since the above 'skipped' setting only happens if no match is found
				fsResult='skipped'
			self.fsLogUpdate(fleet=fleet,dev=dev,seq=seq,result=fsResult+resultSuffix)
			self.sendPendingGet()
		elif uid:
			nxResult=found # False or 'continue' or 'child' or 'skipped'
			resultSuffix=''
			# only open a new entry widget if none is alredy open within the continue time, 
			#  and the fleet/dev is not being filtered
			if not found:
				if self.fsIsFiltered('',uid):
					nxResult='filtered'
					self.fsFilteredCallDisplay('on','',uid,callsign)
					QTimer.singleShot(5000,self.fsFilteredCallDisplay) # no arguments will clear the display
				else:
					if attemptNEW:
						nxResult='newEntry'
						resultSuffix=self.openNewEntry('nex',callsign,formattedLocString,None,uid,origLocString)
						widget=self.newEntryWidget # the widget created by openNewEntry
					else:
						logging.info('no other entry was found, but due to sequence checking, no new entry will be created')
						nxResult='skipped'
			if not attemptNEW: # since the above 'skipped' setting only happens if no match is found
				nxResult='skipped'
			self.fsLogUpdate(uid=uid,seq=seq,result=nxResult+resultSuffix)
			self.sendPendingGet()

		# 683 - activate the widget if needed here, rather than in addTab which only happens for new tabs
		# logging.info('checking to see if widget should be activated: widget='+str(widget)+'  currentEntryLastModAge='+str(self.currentEntryLastModAge)+'  tab count='+str(self.newEntryWindow.ui.tabWidget.count()))
		#748 - only attempt this clause if widget is defined (i.e. if there was a find, or, the last widget in the list)
		if widget and (self.currentEntryLastModAge>holdSec or self.newEntryWindow.ui.tabWidget.count()==3):
			# logging.info('  activating New Entry Widget: '+widget.ui.teamField.text())
			self.newEntryWindow.ui.tabWidget.setCurrentWidget(widget)
			if not widget.ui.teamField.hasFocus(): # if teamField has focus i.e. is being changed, keep focus there
				widget.ui.messageField.setFocus()
		# #722 - end of 'if attemptNEW' clause
		# else:
		# 	if fleet:
		# 		self.fsLogUpdate(fleet=fleet,dev=dev,seq=seq,result='skipped')
		# 	elif uid:
		# 		self.fsLogUpdate(uid=uid,seq=seq,result='skipped')


	def sendPendingGet(self,suffix=""):
		logging.info('sendPendingGet called; locator-style requests disabled for this version; maintained for any future use of LiveTracks')
		# # NOTE that requests.get can cause a blocking delay; so, do it AFTER spawning the newEntryDialog
		# # if sarsoft is not running to handle this get request, Windows will complain with nested exceptions:
		# # ConnectionRefusedError: [WinError 10061] No connection could be made because the target machine actively refused it
		# # During handling of the above exception, another exception occurred:
		# # requests.packages.urllib3.exceptions.ProtocolError: ('Connection aborted.', ConnectionRefusedError(10061, 'No connection could be made because the target machine actively refused it', None, 10061, None))
		# # but we don't care about these; pass them silently

		# # also, if it ends in hyphen, defer sending until accept of change callsign dialog, or closeEvent of newEntryDialog
		# #  (see getString construction comments above)
		# if not self.noSend:
		# 	if self.getString!='': # to avoid sending a GET string that is nothing but the callsign
		# 		self.getString=self.getString+suffix
		# 	if self.getString!='' and not self.getString.endswith("-"):
		# 		logging.info("calling processEvents before sending GET request...")
		# 		QCoreApplication.processEvents()
		# 		try:
		# 			logging.info("Sending GET request:")
		# 			logging.info(self.getString)
		# 			# fire-and-forget: completely ignore the response, but, return immediately
		# 			r=requests.get(self.getString,timeout=0.0001)
		# 			logging.info("  request sent")
		# 			logging.info("  response: "+str(r))
		# 		except Exception as e:
		# 			logging.info("  exception during sending of GET request: "+str(e))
		# 		self.getString=''
				
	def getRadioMarkerLabelForCallsign(self,callsign):
		return callsign.replace('Team ','T')
	
	# def radioMarkerDeferredHook(self,d):
	# 	# # modify the queued entry now before the request is sent
	# 	# logging.info('deferred hook called with this queued entry dict:')
	# 	# logging.info(json.dumps(d,indent=3,cls=CustomEncoder))
	# 	# # 1. determine devStr (fleet:device, or uid for NXDN) from the dict
	# 	# # j=json.loads(d['json'])
	# 	# # jdc
	# 	# deviceStr=d['callbacks'][1][1]['deviceStr'] # assumes the first arg to the second callback is a dict
	# 	# # 2. call addRadioMarker again to enqueue a new request which will
	# 	# #     now have the correct ID of the dame device's existing marker
	# 	# self.sendRadioMarker(fleet,dev,uid,callsign,lat,lon)
	# 	# # 3. cancel the current request
	# 	# return 'CANCEL'
	# 	pass

	def sendRadioMarker(self,fleet,dev,uid,callsign,lat=None,lon=None,timeStr=None,label=None,bump=False):
		# - always update radioMarkerDict right away, in the main thread
		# - if there is an open writable map - even if unexpectedly disconnected - set the event now to start processing
		#   (if map is opened at a later time, optionsDialog.caltopoOpenMapButtonClicked sets the event)
		# - when the marker request comes back (in a callback), update radioMarkerDict's marker ID if needed (it could be None for a while)

		if uid:
			deviceStr=str(uid)
		else:
			deviceStr=str(fleet)+':'+str(dev)
		label=label or self.getRadioMarkerLabelForCallsign(callsign)
		d=self.radioMarkerDict.get(deviceStr,None)
		existingId=None
		latestTimeString=timeStr or time.strftime('%H:%M:%S %b%d')
		if bump:
			latestTimeString+=' bump'
		with self.radioMarkerDictLock:
			if d:
				logging.info('am1a: radioMarkerDict entry found: d["'+str(deviceStr)+'"]='+str(d))
				existingId=d.get('caltopoId',None)
				if lat: # latitude specified: it's a new call: update lat, lon, latestTimeString, label; set lastId to None
					d['latestTimeString']=latestTimeString
					d['lat']=lat
					d['lon']=lon
					d['lastId']=None # flag to tell _radioMarkerWorker to update this device's marker
					d['label']=label
				else: # latitude not specified: it's not a new call - must be callsign change from already-open NED
					lat=d.get('lat',None)
					lon=d.get('lon',None)
					latestTimeString=d.get('latestTimeString','')
					logging.info('  label update only (--> '+str(label)+'); using previous lat,lon='+str(lat)+','+str(lon)+' and preserving time string '+str(latestTimeString))
					d['lastId']=None # flag to tell _radioMarkerWorker to update this device's marker
					d['label']=label # set here, in case cts doesn't exist yet
			else:
				logging.info('am1b: no radioMarkerDict entry found for deviceStr='+str(deviceStr))
				# add placeholder radioMarkerDict entry now, to allow updating while disconnected
				self.radioMarkerDict[deviceStr]={
					'caltopoId': None, # only set caltopoId if this is the first successful request
					'lastId': None,  # changed on every request: '' = fail on last attempt, real ID = success on last attempt
					'label': label,
					'latestTimeString': latestTimeString,
					'lat': lat,
					'lon': lon,
					# 'folderId': None, # changed once the folder has been created
					'history':[]
				}
				if not lat or not lon:
					# no lat or lon, and also no radioMarkerDict entry:
					#  this is the case for label-change requests while disconnected,
					#  for a device whose marker creation request also happened while disconnected,
					#  therefore no radioMarkerDict entry was ever created during _handleResponse;
					#  will need to determine existingId later, when the queued request is
					#  pulled from the queue and processed.
					logging.info('  lat or lon not specified in current or previous request; skipping')

			# update the history, in case it's ever needed to audit or show on caltopo
			self.radioMarkerDict[deviceStr]['history']+=[[latestTimeString,label,lat,lon]]
		
		# # always enqueue right away
		# #  the only data we need to enqueue is deviceStr; radioMarkerDict holds all the details
		# self.radioMarkerQueue.put(deviceStr)

		# radioMarkerQueueEntry={
		# 	'fleet':fleet,
		# 	'dev':dev,
		# 	'uid':uid,
		# 	'callsign':callsign,
		# 	'lat':lat,
		# 	'lon':lon,
		# 	'timeStr':timeStr,
		# 	'label':label
		# }
		# self.radioMarkerQueue.put(radioMarkerQueueEntry)
		# if a writable map is open, emit the event now to start processing the queue
		if self.cts and self.caltopoLink in [-1,2] and self.caltopoOpenMapIsWritable:  # -1 = unexpected disconnect; 2 = connected to open map
			self.radioMarkerEvent.set()

		# logging.info(f'sendRadioMarker called: fleet={fleet} dev={dev} uid={uid} callsign={callsign} lat={lat} lon={lon} timeStr={timeStr} label={label}')
		# if self.caltopoOpenMapIsWritable:
		# 	with self.pendingRadioMarkerArgsLock:
		# 		self.pendingRadioMarkerArgs=(fleet,dev,uid,callsign)
		# 		self.pendingRadioMarkerKwArgs={
		# 				'lat':lat,
		# 				'lon':lon,
		# 				'timeStr':timeStr,
		# 				'label':label
		# 			}
		# 	self.radioMarkerEvent.set()
		# else:
		# 	logging.info(' the current caltopo map is not writable; not sending marker request')

		# self.sendRadioMarkerThread=threading.Thread(
		# 		target=self._sendRadioMarkerWorker,
		# 		args=(fleet,dev,uid,callsign),
		# 		kwargs={
		# 			'lat':lat,
		# 			'lon':lon,
		# 			'timeStr':timeStr,
		# 			'label':label
		# 		},
		# 		daemon=True)

	def _radioMarkerWorker(self,event):
		# when triggered by the event, iterate over all entries in radioMarkerDict (one entry per device)
		#  and take the appropriate action on each entry:
		#  - if caltopoId is None, the marker hasn't yet been created: call addMarker; otherwise:
		#  - if lastId is equal to (non-empty)caltopoId, it's already up to date - no action needed; otherwise:
		#  - call editMarker to update lat, lon, label
		#
		# In the event that a second incoming call for a device happens before a prior response is received for that
		#  same device (if disconnected or just a slow connection) there's no problem: a second edit request is fine,
		#  and a second addMarker request will be cleaned up in handleRadioMarkerResponse by deleting the earlier marker
		#
		# Note: we need to use a thread lock when editing radioMarkerDict since it's also edited in the main thread
		# 
		# if there is an open writable map, make or update the radio marker;
		#   if unexpectedly disconnected, caltopo_python will take care of queueing it
		# only try to send the latest history entry, in case several were created
		#  before the map was opened or while disconnected
		# using 'return' inside this function would actually end the thread;
		#   instead, use 'continue' to go back to the 'while' line
		while True:
			logging.info('_radioMarkerWorker: waiting for event...')
			event.wait()
			logging.info('  _radioMarkerWorker: event received, processing begins...')
			event.clear()
			# #811 - refresh now, in case anything was deleted since the last regular sync;
			#  to get the tightest correllation i.e. the most confidence that the cache is up to date,
			#  we would need to refresh immediately before each call to getOrCreateRadioMarkerFID,
			#  but just one refresh per event should be plenty.  This wil be a blocking refresh, but this is already
			#  inside radioMarkerThread so it shouldn't affect main thread performance.
			self.cts._refresh(forceImmediate=True) # in case anything was deleted since the last regular sync
			with self.radioMarkerDictLock:
				for (deviceStr,d) in self.radioMarkerDict.items(): # as long as we only read radioMarkerDict, there should be no need for a lock
					# (caltopoId,lastId,label,latestTimeString,lat,lon,folderId)=(d.get(key,None) for key in ['caltopoId','lastId','label','latestTimeString','lat','lon','folderId'])
					(caltopoId,lastId,label,latestTimeString,lat,lon)=(d.get(key,None) for key in ['caltopoId','lastId','label','latestTimeString','lat','lon'])
					if lastId is None and lat is not None: # only process devices with coordinates whose lastId has been cleared by sendRadioMarker
						# qe=self.radioMarkerQueue.get() # pop an item from the queue for processing; don't move past this iteration until marker request is sent to a writable map
						try:
							# if not self.pendingRadioMarkerArgs:
							# 	logging.info('WARNING: radioMarkerEvent received, but argument variables are empty; continuing')
							# 	continue
							# (fleet,dev,uid,callsign)=self.pendingRadioMarkerArgs
							# lat=self.pendingRadioMarkerKwArgs['lat']
							# lon=self.pendingRadioMarkerKwArgs['lon']
							# timeStr=self.pendingRadioMarkerKwArgs['timeStr']
							# label=self.pendingRadioMarkerKwArgs['label']
							# with self.pendingRadioMarkerArgsLock:
							# 	self.pendingRadioMarkerArgs=None
							# 	self.pendingRadioMarkerKwArgs=None
							logging.info(f'processing marker: caltopoId={caltopoId} lastId={lastId} label={label} latestTimeString={latestTimeString} lat={lat} lon={lon}')
							# mimic the old 'Locator Group' behavior:
							# - create a 'Radios' folder on the first call to this function; place markers in that folder
							# - if a marker for the callsign already exists, move it (and update the time)
							# - if a marker for the callsign does not yet exist, add one (with updated time)
							# - one marker per device (as opposed to one marker per callsign)
							#  - there could be multiple markers (multiple devices) with the same callsign

							# questions:
							# - should radio markers be deleted at any point?
							# - should radio marker colors be changed, as a function of team status, or time since last call?

							# self.radioMarkerDict - keys are device strings ('<fleet>:<device>' or '<NXDN UID>'),
							#	values are dicts with the following keys:
							#  - caltopoID - caltopo feature ID of this device's caltopo marker, if any
							#  - label
							#  - latestTimeString
							#  - lat
							#  - lon
							#  - history - list of lists, each one being a call from that device (oldest first): [timeStr,label,lat,lon]

							# self.radioMarkerDict entries must have all the info needed for createCTS to add deferred markers,
							#  i.e. if incoming GPS data was stored before the CTS session was created, or during lost connection

							# if uid:
							# 	deviceStr=str(uid)
							# else:
							# 	deviceStr=str(fleet)+':'+str(dev)
							# d=self.radioMarkerDict.get(deviceStr,None) # should already be populated by this time
						# 'caltopoId': None, # only set caltopoId if this is the first successful request
						# 'lastId': None,  # changed on every request: '' = fail on last attempt, real ID = success on last attempt
						# 'label': label,
						# 'latestTimeString': latestTimeString,
						# 'lat': lat,
						# 'lon': lon,
						# 'history':[]
							# (caltopoId,lastId,label,latestTimeString,lat,lon,history)=(d.get(key,None) for key in ['caltopoId','lastId','label','latestTimeString','lat','lon','history'])
							# existingId=d.get('existingId',None)
							# logging.info(f'deviceStr={deviceStr}  existingId={existingId}')
							id='' # initialize here so that entry can be saved before cts exists
							existingId=caltopoId # preserve caltopoID if already set
							# label=self.getRadioMarkerLabelForCallsign(callsign)
							r=False
							if self.cts and self.caltopoLink in [-1,2]: # -1 = unexpected disconnect; 2 = connected to open map
								self.radioMarkerFID=self.getOrCreateRadioMarkerFID()
								# since this is in a separate thread, we can do a wait loop until the folder ID is not None
								# while self.caltopoLink==2 and self.radioMarkerFID is None:

								# this sleep causes the GUI to freeze.  Can't figure out why.  Google AI overview seems to think
								#  the GIL may not be getting released correctly, but even if that's true, there's no way to
								#  directly control it.  So: find another way to wait until the folder exists before adding markers.
								# while self.radioMarkerFID is None: # this could be waiting a LONG time e.g. if disconnected
								# 	logging.info('  waiting for radioMarkerFID...')
								# 	time.sleep(1)

								# removal of radioMarkerQueue - and simple reliance on just looking in radioMarkerDict -
								#  means that we don't need to wait inside this loop for radioMarkerFID to exist - we can
								#  just exit the loop using 'continue'; simply don't create any markers until the Radios folder exists
								if not self.radioMarkerFID:
									logging.warning('Radios folder does not exist yet; not creating any radio markers for now...')
									continue
								try:
									# logging.info('  addMarker:  label='+str(label)+'  folderId='+str(self.radioMarkerFID))
									logging.info(f'  addMarker:  label={label}')
									# radioMarkerFID will probably still be None if the Radios folder was created in the previous lines,
									#  since that request is in a different thread and radioMarkerFID isn't set until its callback is triggered.
									# options:
									#  - wait to call addMarker until radioMarkerFID is not None
									#      NOTE: to avoid main thread delay, this would require putting sendRadioMarker in a separate thread,
									#       which would probably be a good idea anyway to ensure radiolog usage is not delayed by caltopo integration
									#  - for any markers created woth fid=None, edit them later to set the fid
									#  - add an argument to add<Class> calls in caltopo_python that would wait to build the request until a certain flag is set
									#  - place the entire addMarker call in the callback of the addFolder call
									callbacks=[[self.handleRadioMarkerResponse,[],{
										'deviceStr':deviceStr,
										# 'lat':lat,
										# 'lon':lon,
										# 'label':label,
										# 'latestTimeString':latestTimeString,
										'id':'.result.id', # will be equal to existingId on subsequent updates
										# 'existingId':existingId, # will be None on first call from a device
										# 'radioMarkerFID':self.radioMarkerFID # record radioMarkerFID at enqueue-time
									}]]
									description=latestTimeString+'  ['+deviceStr+']'
									color='#ff0000'
									if latestTimeString.endswith(' bump'):
										description=latestTimeString[:-5]+'  ['+deviceStr+'] b'
										color='#888888'
									if existingId: # update an existing marker
										r=self.cts.editFeature(
												id=existingId,
												title=label,
												folderId=self.radioMarkerFID, # in case a marker was moved to a different folder
												# className='Marker',
												geometry={'coordinates':[lon,lat,0,0]},
												properties={'description':description,'marker-color':color},
												callbacks=callbacks)
									else: # create a new marker
										r=self.cts.addMarker(lat,lon,label,description,
							   					color=color,
												folderId=self.radioMarkerFID,
												# existingId=existingId,
												# deferredHook=self.radioMarkerDeferredHook,
												callbacks=callbacks)
								except Exception as e:
									logging.info('Exception during addMarker:'+str(e))
								# add or update the dict entry here, with enough detail for createSTS to add any deferred markers
								if r==True:
									logging.info('  marker request queued successfully')
									# if not existingId:
									# 	newId=id # only set caltopoId if this is the first successful request
								else:
									logging.info('  marker request failed: cts='+str(self.cts)+'  caltopoLink='+str(self.caltopoLink))
							else:
								logging.info('  not currently connected to an open writable map; skipping for now')
						except Exception as e:
							logging.info('error: exception during radioMarkerWorker: '+str(e))
						# finally:
						# 	logging.info('radioMarkerQueue.task_done')
						# 	self.radioMarkerQueue.task_done()

	def handleRadioMarkerResponse(self,**kwargs):
		# note that kwargs is now a dict, to be referenced as such
		logging.info('  inside handleRadioMarkerResponse:')
		logging.info(json.dumps(kwargs,indent=3))

		# delete any earlier marker with the same deviceStr due to duplication during disconnect;
		#  this would be the case if the deviceStr already has an entry in radioMarkerDict
		#  but with a different id;
		#  as long as this cleanup is performed after every new marker addition, multiple stale
		#  markers should all be cleaned up because there will only be one after any given addition
		deviceStr=kwargs['deviceStr']
		updateCaltopoIdFlag=False
		# prevHistory=[]
		if deviceStr in self.radioMarkerDict.keys():
			d=self.radioMarkerDict[deviceStr]
			oldId=d['caltopoId']
			if oldId and oldId!=kwargs['id']:
				logging.info(' cleaning up stale radio marker for '+str(deviceStr)+'  id='+str(oldId))
				self.cts.delMarker(oldId,blocking=False)
				updateCaltopoIdFlag=True
			# prevHistory=self.radioMarkerDict[deviceStr].get('history',[])

			# newId=kwargs['existingId'] # preserve the id if this is not the first call from the device
			# if not newId: # this must be the first call from the device
			# 	newId=kwargs['id']
			# logging.info('hrmr2 - prevHistory='+str(prevHistory))
			with self.radioMarkerDictLock:
				# d=self.radioMarkerDict[deviceStr]
				d['lastId']=kwargs['id'] # flag to tell _radioMarkerWorker that this device's marker has been updated
				if d['caltopoId'] is None or updateCaltopoIdFlag:
					d['caltopoId']=kwargs['id']
				# self.radioMarkerDict[deviceStr]={
				# 	'caltopoId': newId, # only set caltopoId if this is the first successful request
				# 	'lastId': kwargs['id'],  # changed on every request: '' = fail on last attempt, real ID = success on last attempt
				# 	'label': kwargs['label'],
				# 	'latestTimeString': kwargs['latestTimeString'],
				# 	'lat': kwargs['lat'],
				# 	'lon': kwargs['lon'],
				# 	'radioMarkerFID': kwargs['radioMarkerFID']
				# }

		logging.info('updated radioMarkerDict at end of handleRadioMarkerResponse:')
		logging.info(json.dumps(self.radioMarkerDict,indent=3))

		# # if the marker didn't have any folder ID, which would be the case if there was no radios folder before disconnect,
		# #  then move it to the radios folder now, which would already exist in the cache by this time
		# if kwargs['radioMarkerFID'] is None:
		# 	logging.info(f'  radio marker for {deviceStr} had no folder ID: Radios folder did not exist when marker was enqueued; moving marker to Radios folder now')
		# 	self.cts.editFeature(id=kwargs['id'],properties={'folderId':self.radioMarkerFID},callbacks=[[self.moveRadioMarkerToFolderCB,[deviceStr]]])
	
	def moveRadioMarkerToFolderCB(self,deviceStr):
		logging.info(f'updating radioMarkerFID for {deviceStr}')
		logging.info('before:')
		logging.info(json.dumps(self.radioMarkerDict[deviceStr],indent=3))
		with self.radioMarkerDictLock:
			self.radioMarkerDict[deviceStr]['radioMarkerFID']=self.radioMarkerFID
		logging.info('after:')
		logging.info(json.dumps(self.radioMarkerDict[deviceStr],indent=3))

	# for fsLog, a dictionary would probably be easier, but we have to use an array
	#  since we will be displaying in a QTableView
	# if callsign is specified, update the callsign but not the time;
	#  if callsign is not specified, udpate the time but not the callsign;
	#  if the entry does not yet exist, add it

	def fsLogUpdate(self,fleet=None,dev=None,uid=None,callsign=False,bump=False,seq=None,result=None):
		#722 added row entries last_sequence and last_result to help in excessive popup reduction
		# row structure: [fleet,dev,callsign,filtered,last_received,com_port,bump_count,total_count,last_sequence,last_result]
		# don't process the dummy default entry
		if callsign=='Default':
			return
		if not ((fleet and dev) or uid):
			logging.info('ERROR in call to fsLogUpdate: either fleet and dev must be specified, or uid must be specified.')
			logging.info('  fleet='+str(fleet)+'  dev='+str(dev)+'  uid='+str(uid))
			return
		# # this clause is dead code now, since enforcing that fleet and dev are always strings throughout the code
		# if fleet and dev: # fleetsync, not nexedge
		# 	try:
		# 		fleet=int(fleet)
		# 		dev=int(dev)
		# 	except:
		# 		logging.info('ERROR in call to fsLogUpdate: fleet and dev must both be integers or integer-strings: fleet='+str(fleet)+'  dev='+str(dev))
		# 		return
		com='<None>'
		if self.fsLatestComPort:
			com=str(self.fsLatestComPort.name)
		if com!='<None>': # suppress printing on initial log population during fsLoadLookup
			if fleet and dev:
				logging.info("updating fsLog (fleetsync): fleet="+fleet+" dev="+dev+" callsign="+(callsign or "<None>")+"  COM port="+com)
			elif uid:
				logging.info("updating fsLog (nexedge): user id = "+uid+" callsign="+(callsign or "<None>")+"  COM port="+com)
		found=False
		t=time.strftime("%a %H:%M:%S")
		for row in self.fsLog:
			if (row[0]==fleet and row[1]==dev) or (row[0]=='' and row[1]==uid):
				found=True
				if callsign:
					row[2]=callsign
				else:
					row[4]=t
				row[5]=com
				if bump:
					row[6]+=1
				row[7]+=1
				row[8]=seq
				row[9]=result
				# logging.info('appending modified row to fsFullLog:'+str(row))
				self.fsFullLog.append(row[:]) # [:] is needed to append static values rather than references https://stackoverflow.com/a/6360319/3577105
				break
		if not found:
			# always update callsign - it may have changed since creation
			if fleet and dev: # fleetsync
				row=[fleet,dev,self.getCallsign(fleet,dev),False,t,com,int(bump),1,seq,result]
				# logging.info('appending initial row: '+str(row))
				self.fsLog.append(row[:])
				self.fsFullLog.append(row[:])
			elif uid: # nexedge
				row=['',uid,self.getCallsign(uid),False,t,com,int(bump),1,seq,result]
				self.fsLog.append(row[:])
				self.fsFullLog.append(row[:])

		# logging.info('fsLog after fsLogUpdate:'+str(self.fsLog))
		# logging.info('fsFullLog after fsLogUpdate:'+str(self.fsFullLog))
# 		if self.fsFilterDialog.ui.tableView:
		self.fsFilterDialog.ui.tableView.model().layoutChanged.emit()
		self.fsBuildTeamFilterDict()
		# 744 - keep track of the time of the latest filtered mic bump for this device
		if bump:
			if fleet and dev:
				self.latestBumpDict[str(fleet)+':'+str(dev)]=time.time()
			elif uid:
				self.latestBumpDict[uid]=time.time()
	
	def fsGetLatestComPort(self,fleetOrBlank,devOrUid):
		logging.info('fsLog:'+str(self.fsLog))
		if fleetOrBlank:
			idStr=fleetOrBlank+':'+devOrUid
		else:
			idStr=devOrUid
		log=[x for x in self.fsLog if x[0:2]==[fleetOrBlank,devOrUid]]
		if len(log)==1:
			comPortName=log[0][5]
		elif len(log)>1:
			logging.info('WARNING: there are multiple fsLog entries for '+idStr)
			comPortName=log[0][5]
		else:
			logging.info('WARNING: '+idStr+' has no fsLog entry so it probably has not been heard from yet')
			comPortName=None
		# logging.info('returning '+str(comPortName))
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
		# richtext doesn't support pt-based font sizes https://stackoverflow.com/a/49397095/3577105
		if filteredHtml != "":
			tt='<span style="font-size: '+str(self.toolTipFontSize)+'pt;">Filtered devices:<br>(left-click to edit)<table border="1" cellpadding="3"><tr><td>Callsign</td><td>Fleet</td><td>ID</td></tr>'+filteredHtml+'</table></span>'
		else:
			tt='<span style="font-size: '+str(self.toolTipFontSize)+'pt;">No devices are currently being filtered.<br>(left-click to edit)</span>'
		self.ui.fsFilterButton.setToolTip(tt)

	def fsIsFiltered(self,fleetOrBlank,devOrUid):
# 		logging.info("checking fsFilter: fleet="+str(fleet)+" dev="+str(dev))
		# disable fsValidFleetList checking to allow arbitrary fleets; this
		#  idea is probably obsolete
		# invalid fleets are always filtered, to prevent fleet-glitches (110-xxxx) from opening new entries
# 		if int(fleet) not in self.fsValidFleetList:
# 			logging.info("true1")
# 			return True
		# if the fleet is valid, check for filtered device ID
		for row in self.fsLog:
			if row[0]==fleetOrBlank and row[1]==devOrUid and row[3]==True:
# 				logging.info("  device is fitlered; returning True")
				return True
# 		logging.info("not filtered; returning False")
		return False

	def fsLoadLookup(self,startupFlag=False,fsFileName=None,hideWarnings=False):
		logging.info("fsLoadLookup called: startupFlag="+str(startupFlag)+"  fsFileName="+str(fsFileName)+"  hideWarnings="+str(hideWarnings))
		if not startupFlag and not fsFileName: # don't ask for confirmation on startup or on restore
			really=QMessageBox(QMessageBox.Warning,'Please Confirm','Are you sure you want to reload the FleetSync lookup table for this session?  This may overwrite any recent callsign changes you have made.',
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
			# logging.info('t1: fsDir='+fsDir+'  fsFileName='+fsFileName)
			fsFullPath=os.path.join(fsDir,fsFileName)
		try:
			# logging.info("  trying "+fsFullPath)
			with open(fsFullPath,'r') as fsFile:
				logging.info("Loading FleetSync Lookup Table from file "+fsFullPath)
				self.fsLookup=[]
				csvReader=csv.reader(fsFile)
				usedCallsignList=[] # keep track of used callsigns to check for duplicates afterwards
				usedIDPairList=[] # keep track of used fleet-dev pairs (or blank-and-unit-ID pairs for NEXEDGE) to check for duplicates afterwards
				duplicateCallsignsAllowed=False
				for row in csvReader:
					# logging.info('row:'+str(row))
					if row:
						if row[0].startswith('#'):
							if 'duplicateCallsignsAllowed' in row[0]:
								duplicateCallsignsAllowed=True
							continue
						[fleet,idOrRange,callsign]=row
						if '-' in idOrRange: # range syntax
							callsignExprRe=re.match(r'.*\[(.*)\]',callsign)
							if not callsignExprRe:
								msg='ERROR: range syntax callsign "'+callsign+'" does not include a valid expression inside brackets, such as "[id-1000]".  Skipping.'
								logging.info(msg)
								self.fsMsgBox=QMessageBox(QMessageBox.Warning,"FleetSync Table Warning",'Error in FleetSync lookup file\n\n'+fsFullPath+'\n\n'+msg,
														QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
								self.fsMsgBox.show()
								self.fsMsgBox.raise_()
								self.fsMsgBox.exec_() # modal
								continue
							callsignExpr=callsignExprRe.group(1)
							callsign=callsign.replace(callsignExpr,'') # turn the expression into a placeholder '[]'
							firstLast=[str(n) for n in row[1].split('-')]
							if firstLast[1]<=firstLast[0]:
								msg='ERROR: range syntax ending value is less than or equal to starting value: "'+row[1]+'".  Skipping.'
								logging.info(msg)
								self.fsMsgBox=QMessageBox(QMessageBox.Warning,"FleetSync Table Warning",'Error in FleetSync lookup file\n\n'+fsFullPath+'\n\n'+msg,
														QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
								self.fsMsgBox.show()
								self.fsMsgBox.raise_()
								self.fsMsgBox.exec_() # modal
								continue
							for id in range(int(firstLast[0]),int(firstLast[1])+1):
								r=eval(callsignExpr)
								cs=callsign.replace('[]',str(r))
								row=[str(fleet),str(id),cs]
								# logging.info(' adding evaluated row: '+str(row))
								self.fsLookup.append(row)
								# self.fsLogUpdate(row[0],row[1],row[2])
								usedCallsignList.append(cs)
								usedIDPairList.append(row[0]+':'+row[1])
						else:
							# logging.info(' adding row: '+str(row))
							self.fsLookup.append([str(fleet),str(idOrRange),callsign])
							# self.fsLogUpdate(row[0],row[1],row[2])
							usedCallsignList.append(row[2])
							usedIDPairList.append(str(row[0])+':'+str(row[1]))
				# logging.info('reading done')
				if not duplicateCallsignsAllowed and len(set(usedCallsignList))!=len(usedCallsignList):
					seen=set()
					duplicatedCallsigns=[x for x in usedCallsignList if x in seen or seen.add(x)]
					n=len(duplicatedCallsigns)
					if n>3:
						duplicatedCallsigns=duplicatedCallsigns[0:3]+['(and '+str(n-3)+' more)']
					msg='Callsigns were repeated in the FleetSync lookup file\n\n'+fsFullPath+'\n\nThis is allowed, but, it is probably a mistake.  Please check the file.  If you want to avoid this message in the future, please add the fillowing line to the file:\n\n# duplicateCallsignsAllowed\n\n'
					msg+='Repeated callsigns:\n\n'+str(duplicatedCallsigns).replace('[','').replace(']','').replace("'","").replace(', (',' (')
					logging.info('FleetSync Table Warning:'+msg)
					self.fsMsgBox=QMessageBox(QMessageBox.Warning,"FleetSync Table Warning",msg,
											QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
					self.fsMsgBox.show()
					self.fsMsgBox.raise_()
					self.fsMsgBox.exec_() # modal
				if len(set(usedIDPairList))!=len(usedIDPairList):
					seen=set()
					duplicatedIDPairs=[x for x in usedIDPairList if x in seen or seen.add(x)]
					n=len(duplicatedIDPairs)
					if n>3:
						duplicatedIDPairs=duplicatedIDPairs[0:3]+['(and '+str(n-3)+' more)']
					msg='Device ID pairs are repeated in the FleetSync lookup file\n\n'+fsFullPath+'\n\nFor this session, the last definition will be used, overwriting definitions that appear earlier in the file.  Please correct the file soon.\n\n'
					msg+='Repeated pairs:\n\n'+str(duplicatedIDPairs).replace('[','').replace(']','').replace("'","").replace(', (',' (')
					logging.info('FleetSync Table Warning:'+msg)
					self.fsMsgBox=QMessageBox(QMessageBox.Warning,"FleetSync Table Warning",msg,
											QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
					self.fsMsgBox.show()
					self.fsMsgBox.raise_()
					self.fsMsgBox.exec_() # modal
				if not startupFlag: # suppress message box on startup
					msg='FleetSync ID table has been re-loaded from file '+fsFullPath+'.'
					logging.info(msg)
					self.fsMsgBox=QMessageBox(QMessageBox.Information,"Information",msg,
											QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
					self.fsMsgBox.show()
					QCoreApplication.processEvents()
					QTimer.singleShot(5000,self.fsMsgBox.close)
		except:
			if not hideWarnings:
				if fsEmptyFlag:
					msg='Cannot read FleetSync ID table file "'+fsFullPath+'" and no FleetSync ID table has yet been loaded.  Callsigns for incoming FleetSync calls will be of the format "KW-<fleet>-<device>".'
					logging.info(msg)
					warn=QMessageBox(QMessageBox.Warning,"Warning",msg+"\n\nThis warning will automatically close in a few seconds.",
									QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
				else:
					msg='Cannot read FleetSync ID table file "'+fsFullPath+'"!  Using existing settings.'
					logging.info(msg)
					warn=QMessageBox(QMessageBox.Warning,"Warning",msg+"\n\nThis warning will automatically close in a few seconds.",
									QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
				warn.show()
				warn.raise_()
				QTimer.singleShot(15000,warn.close)
				warn.exec_()

	# save to fsFileName in the working dir each time, but on startup, load from the default dir;
	#  would only need to load from the working dir if restoring
	def fsSaveLookup(self):
		fsFullPath=os.path.join(self.sessionDir,self.fsFileName)
		try:
			with open(fsFullPath,'w',newline='') as fsFile:
				logging.info("Writing file "+fsFullPath)
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

	def fsSaveLog(self,finalize=False):
		fsLogFullPath=os.path.join(self.sessionDir,self.fsLogFileName)
		try:
			with open(fsLogFullPath,'w',newline='') as fsLogFile:
				logging.info('Writing FleetSync/NEXEDGE log file '+fsLogFullPath)
				csvWriter=csv.writer(fsLogFile)
				csvWriter.writerow(["## Radio Log FleetSync activity log"])
				csvWriter.writerow(["## File written "+time.strftime("%a %b %d %Y %H:%M:%S")])
				csvWriter.writerow(["## Created during Incident Name: "+self.incidentName])
				csvWriter.writerow(['# Fleet/UID','Device','Callsign','N/A','Time','COM port','Bumps','Total','Sequence','Result'])
				for row in self.fsFullLog:
					csvWriter.writerow(row)
				if finalize:
					csvWriter.writerow(["## end"])
		except:
			logging.info("ERROR: cannot write FleetSync log file "+fsLogFullPath)

	def getCallsign(self,fleetOrUid,dev=None):
		if not isinstance(fleetOrUid,str):
			logging.info('WARNING in call to getCallsign: fleetOrId is not a string.')
			return
		if dev and not isinstance(dev,str):
			logging.info('WARNING in call to getCallsign: dev is not a string.')
			return
		matches=[]

		if len(fleetOrUid)==3: # 3 characters - must be fleetsync
			logging.info('getCallsign called for FleetSync fleet='+str(fleetOrUid)+' dev='+str(dev))
			fleet=fleetOrUid
			for entry in self.fsLookup:
				if entry[0] and int(entry[0])==int(fleet) and entry[1] and int(entry[1])==int(dev):
					# check each potential match against existing matches before adding to the list of matches
					found=False
					for match in matches:
						if int(match[0])==int(fleet) and int(match[1])==int(dev) and match[2].lower().replace(' ','')==entry[2].lower().replace(' ',''):
							found=True
					if not found:
						matches.append(entry)
						# matches=[element for element in self.fsLookup if (element[0]==fleet and element[1]==dev)]
			if len(matches)>0:
				logging.info('  found matching entry/entries:'+str(matches))
			else:
				logging.info('  no matches')
			if len(matches)!=1 or len(matches[0][0])!=3: # no match
				return "KW-"+fleet+"-"+dev
			else:
				return matches[0][2]
	
		elif len(fleetOrUid)==5: # 5 characters - must be NEXEDGE
			uid=fleetOrUid
			logging.info('getCallsign called for NEXEDGE UID='+str(uid))
			for entry in self.fsLookup:
				if entry[1]==uid:
					# check each potential match against existing matches before adding to the list of matches
					found=False
					for match in matches:
						if str(match[1])==str(uid) and match[2].lower().replace(' ','')==entry[2].lower().replace(' ',''):
							found=True
					if not found:
						matches.append(entry)
						# matches=[element for element in self.fsLookup if element[1]==uid]
			if len(matches)>0:
				logging.info('  found matching entry/entries:'+str(matches))
			else:
				logging.info('  no matches')
			if len(matches)!=1 or matches[0][0]!='': # no match
				return "KW-NXDN-"+uid
			else:
				return matches[0][2]
		else:
			logging.info('ERROR in call to getCallsign: first argument must be 3 characters (FleetSync) or 5 characters (NEXEDGE): "'+fleetOrUid+'"')

	def fsGetPrevSeq(self,fleetOrUid,dev=None):
		if not isinstance(fleetOrUid,str):
			logging.info('ERROR in call to getPrevSeq: fleetOrId is not a string.')
			return []
		if dev and not isinstance(dev,str):
			logging.info('ERROR in call to getPrevSeq: dev is not a string.')
			return []

		# ignore rows whose sequence is 'CCD'; could get costly as number of fullLog entries increases;
		#  make sure to efficiently walk the list backwards, rather than looking through the whole list every time
		prevSeq=None
		if len(fleetOrUid)==3: # 3 characters - must be fleetsync
			fleet=fleetOrUid
			for i in range(len(self.fsFullLog)-1,-1,-1):
				row=self.fsFullLog[i]
				if row[0]==fleet and row[1]==dev and row[8]!=['CCD']:
					prevSeq=row[8]
					break
		elif len(fleetOrUid)==5: # 5 characters - must be NEXEDGE
			uid=fleetOrUid
			for i in range(len(self.fsFullLog)-1,-1,-1):
				row=self.fsFullLog[i]
				if row[1]==uid and row[8]!=['CCD']:
					prevSeq=row[8]
					break
		return prevSeq or [] # don't return None or False - must return a list

	# not called from anywhere
	# def getIdFromCallsign(self,callsign):
	# 	entry=[element for element in self.fsLookup if (element[2]==callsign)]
	# 	if len(entry)!=1: # no match
	# 		return False
	# 	else:
	# 		return [entry[0][0],entry[0][1]] # for nexEdge, the first value

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
			logging.info("testConvertCoords:"+str(coords)+" --> "+rval)

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
		logging.info("convertCoords called: targetDatum="+targetDatum+" targetFormat="+targetFormat+" coords="+str(coords))
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
			logging.info("valid logo file "+self.printLogoFileName)
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
		logging.info("Page number:"+str(canvas.getPageNumber()))
		logging.info("Height:"+str(h))
		logging.info("Pagesize:"+str(doc.pagesize))
		t.drawOn(canvas,doc.leftMargin,doc.pagesize[1]-h-0.5*inch) # enforce a 0.5 inch top margin regardless of paper size
##		canvas.grid([x*inch for x in [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11]],[y*inch for y in [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5]])
		logging.info("done drawing printLogHeaderFooter canvas")
		canvas.restoreState()
		logging.info("end of printLogHeaderFooter")

	def printPDF(self,pdfName):
		try:
			win32api.ShellExecute(0,"print",pdfName,'/d:"%s"' % win32print.GetDefaultPrinter(),".",0)
		except Exception as e:
			estr=str(e)
			logging.info('Print failed: '+estr)
			if '31' in estr:
				msg='Failed to send PDF to a printer.\n\nThe PDF file has still been generated and saved in the run directory.\n\nThe most likely cause for this error is that there is no PDF viewer application installed on your system.\n\nPlease make sure you have a PDF viewer application such as Acrobat or Acrobat Reader installed and set as the system default application for viewing PDF files.\n\nYou can install that application now without exiting RadioLog, then try printing again.'
				logging.info(msg)
			if not self.printFailMessageBoxShown:
				box=QMessageBox(QMessageBox.Warning,'Print Failed',msg+'\n\nThis message will not appear again for this RadioLog session.',
					QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
				box.show()
				box.raise_()
				box.exec_()
				self.printFailMessageBoxShown=True

	# optonal argument 'teams': if True, generate one pdf of all individual team logs;
	#  so, this function should be called once to generate the overall log pdf, and
	#  again with teams=True to generate team logs pdf
	# if 'teams' is an array of team names, just print those team log(s)
	def printLog(self,opPeriod,teams=False):
		opPeriod=int(opPeriod)
		# pdfName=self.firstWorkingDir+"\\"+self.pdfFileName
		pdfName=os.path.join(self.sessionDir,self.pdfFileName)
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
		logging.info("teamFilterList="+str(teamFilterList))
		pdfName=pdfName.replace('.pdf','_OP'+str(opPeriod)+'.pdf')
		logging.info("generating radio log pdf: "+pdfName)
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
			styles.add(ParagraphStyle(
				name='operator',
				parent=styles['Normal'],
				backColor='lightgrey'
				))
			headers=MyTableModel.header_labels[0:6]
			if self.useOperatorLogin:
				operatorImageFile=os.path.join(iconsDir,'user_icon_80px.png')
				if os.path.isfile(operatorImageFile):
					logging.info('operator image file found: '+operatorImageFile)
					headers.append(Image(operatorImageFile,width=0.16*inch,height=0.16*inch))
				else:
					logging.info('operator image file not found: '+operatorImageFile)
					headers.append('Op.')
			radioLogPrint.append(headers)
##			if teams and opPeriod==1: # if request op period = 1, include 'Radio Log Begins' in all team tables
##				radioLogPrint.append(self.radioLog[0])
			entryOpPeriod=1 # update this number when 'Operational Period <x> Begins' lines are found
##			hits=False # flag to indicate whether this team has any entries in the requested op period; if not, don't make a table for this team
			for row in self.radioLog:
				opStartRow=False
##				logging.info("message:"+row[3]+":"+str(row[3].split()))
				if row[3].startswith("Radio Log Begins:"):
					opStartRow=True
				if row[3].startswith("Operational Period") and row[3].split()[3] == "Begins:":
					opStartRow=True
					entryOpPeriod=int(row[3].split()[2])
				# #523: handled continued incidents
				if row[3].startswith('Radio Log Begins - Continued incident'):
					opStartRow=True
					entryOpPeriod=int(row[3].split(': Operational Period ')[1].split()[0])
##				logging.info("desired op period="+str(opPeriod)+"; this entry op period="+str(entryOpPeriod))
				if entryOpPeriod == opPeriod:
					if team=="" or extTeamNameLower==getExtTeamName(row[2]).lower() or opStartRow: # filter by team name if argument was specified
						style=styles['Normal']
						if 'RADIO OPERATOR LOGGED IN' in row[3]:
							style=styles['operator']
						printRow=[row[0],row[1],row[2],Paragraph(row[3],style),Paragraph(row[4],styles['Normal']),Paragraph(row[5],styles['Normal'])]
						if self.useOperatorLogin:
							if len(row)>10:
								printRow.append(row[10])
							else:
								printRow.append('')
						radioLogPrint.append(printRow)
##						hits=True
			if not teams:
				# #523: avoid exception	
				try:
					radioLogPrint[1][4]=self.datum
				except:
					logging.info('Nothing to print for specified operational period '+str(opPeriod))
					return
			logging.info("length:"+str(len(radioLogPrint)))
			if not teams or len(radioLogPrint)>2: # don't make a table for teams that have no entries during the requested op period
				if self.useOperatorLogin:
					colWidths=[x*inch for x in [0.5,0.6,1.25,5.2,1.25,0.9,0.3]]
				else:
					colWidths=[x*inch for x in [0.5,0.6,1.25,5.5,1.25,0.9]]
				t=Table(radioLogPrint,repeatRows=1,colWidths=colWidths)
				t.setStyle(TableStyle([('FONT',(0,0),(-1,-1),'Helvetica'),
										('FONT',(0,0),(-1,1),'Helvetica-Bold'),
										('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
				  					 ('BOX', (0,0), (-1,-1), 2, colors.black),
					 				  ('BOX', (0,0), (-1,0), 2, colors.black)]))
				elements.append(t)
				if teams and team!=teamFilterList[-1]: # don't add a spacer after the last team - it could cause another page!
					elements.append(Spacer(0,0.25*inch))
		doc.build(elements,onFirstPage=functools.partial(self.printLogHeaderFooter,opPeriod=opPeriod,teams=teams),onLaterPages=functools.partial(self.printLogHeaderFooter,opPeriod=opPeriod,teams=teams))
# 		self.logMsgBox.setInformativeText("Finalizing and Printing...")
		self.printPDF(pdfName)
		self.radioLogNeedsPrint=False

		if self.use2WD and self.secondWorkingDir and os.path.isdir(self.secondWorkingDir):
			logging.info("copying radio log pdf"+msgAdder+" to "+self.secondWorkingDir)
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
		logging.info("Page number:"+str(canvas.getPageNumber()))
		logging.info("Height:"+str(h))
		logging.info("Pagesize:"+str(doc.pagesize))
		t.drawOn(canvas,doc.leftMargin,doc.pagesize[1]-h-0.5*inch) # enforce a 0.5 inch top margin regardless of paper size
		logging.info("done drawing printClueLogHeaderFooter canvas")
##		canvas.grid([x*inch for x in [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11]],[y*inch for y in [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5]])
		canvas.restoreState()
		logging.info("end of printClueLogHeaderFooter")

	def printClueLog(self,opPeriod):
##      header_labels=['#','DESCRIPTION','TEAM','TIME','DATE','O.P.','LOCATION','INSTRUCTIONS','RADIO LOC.']
		opPeriod=int(opPeriod)
		# first, determine if there are any clues to print for this OP; if not, return before generating the pdf
		rowsToPrint=[]
		for row in self.clueLog:
			if (str(row[5])==str(opPeriod) or row[1].startswith("Operational Period "+str(opPeriod)+" Begins:") or row[1].startswith("Radio Log Begins")):
				rowsToPrint.append(row)
				logging.info('appending: '+str(row))
		if len(rowsToPrint)<2:
			logging.info('Nothing to print for specified operational period '+str(opPeriod))
			return
		else:
			# clueLogPdfFileName=self.firstWorkingDir+"\\"+self.pdfFileName.replace(".pdf","_clueLog_OP"+str(opPeriod)+".pdf")
			clueLogPdfFileName=os.path.join(self.sessionDir,self.pdfFileName.replace(".pdf","_clueLog_OP"+str(opPeriod)+".pdf"))
			logging.info("generating clue log pdf: "+clueLogPdfFileName)
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
			headers=clueTableModel.header_labels[0:5]+clueTableModel.header_labels[6:8] # omit operational period
			if self.useOperatorLogin:
				operatorImageFile=os.path.join(iconsDir,'user_icon_80px.png')
				if os.path.isfile(operatorImageFile):
					headers.append(Image(operatorImageFile,width=0.16*inch,height=0.16*inch))
				else:
					logging.info('operator image file not found: '+operatorImageFile)
					headers.append('Op.')
			clueLogPrint.append(headers)
			for row in rowsToPrint:
				locationText=row[6]
				if row[8]:
					locationText='[Radio GPS:\n'+(row[8].replace('\n',' '))+'] '+row[6]
				printRows=[row[0],Paragraph(row[1],styles['Normal']),row[2],row[3],row[4],Paragraph(locationText,styles['Normal']),Paragraph(row[7],styles['Normal'])]
				if self.useOperatorLogin:
					if len(row)>9:
						printRows.append(row[9])
					else:
						printRows.append('')
				clueLogPrint.append(printRows)
			# #523: avoid exception	
			try:
				clueLogPrint[1][5]=self.datum
			except:
				logging.info('Nothing to print for specified Operational Period '+str(opPeriod))
				return
			if len(clueLogPrint)>2:
	##			t=Table(clueLogPrint,repeatRows=1,colWidths=[x*inch for x in [0.6,3.75,.9,0.5,1.25,3]])
				if self.useOperatorLogin:
					colWidths=[x*inch for x in [0.3,3.75,0.9,0.5,0.8,1.25,2.2,0.3]]
				else:
					colWidths=[x*inch for x in [0.3,3.75,0.9,0.5,0.8,1.25,2.5]]
				t=Table(clueLogPrint,repeatRows=1,colWidths=colWidths)
				t.setStyle(TableStyle([('F/generating clue llONT',(0,0),(-1,-1),'Helvetica'),
										('FONT',(0,0),(-1,1),'Helvetica-Bold'),
										('INNERGRID', (0,0), (-1,-1), 0.25, colors.black),
									('BOX', (0,0), (-1,-1), 2, colors.black),
									('BOX', (0,0), (-1,0), 2, colors.black)]))
				elements.append(t)
				doc.build(elements,onFirstPage=functools.partial(self.printClueLogHeaderFooter,opPeriod=opPeriod),onLaterPages=functools.partial(self.printClueLogHeaderFooter,opPeriod=opPeriod))
	# 			self.clueLogMsgBox.setInformativeText("Finalizing and Printing...")
				self.printPDF(clueLogPdfFileName)
				if self.use2WD and self.secondWorkingDir and os.path.isdir(self.secondWorkingDir):
					logging.info("copying clue log pdf to "+self.secondWorkingDir)
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
		# cluePdfName=self.firstWorkingDir+"\\"+self.pdfFileName.replace(".pdf","_clue"+str(clueData[0]).zfill(2)+".pdf")
		cluePdfName=os.path.join(self.sessionDir,self.pdfFileName.replace(".pdf","_clue"+str(clueData[0]).zfill(2)+".pdf"))
		logging.info("generating clue report pdf: "+cluePdfName)
		
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
		instructionsOtherText=''
		# parse to a list of tokens - split on comma or semicolon with space(s) before and/or after
		instructions=re.sub(r' *[,;] *','|',instructions).split('|')
		# remove any empty elements, probably due to back-to-back delimiters
		instructions=[x for x in instructions if x]
		logging.info('parsed instructions:'+str(instructions))
		# look for keywords in the instructions text
		if "collect" in instructions:
			instructionsCollect='X'
			instructions.remove('collect')
		if "mark & leave" in instructions:
			instructionsMarkAndLeave='X'
			instructions.remove('mark & leave')
		if "disregard" in instructions:
			instructionsDisregard='X'
			instructions.remove('disregard')
		if instructions: # is there anything left in the parsed list?
			instructionsOther='X'
			instructionsOtherText=', '.join(instructions)
# 		locText=clueData[6]
		if clueData[8]!="":
# 			locText=locText+"\n(Radio GPS = "+clueData[8]+")"
			radioLocText="(Radio GPS: "+re.sub(r"\n","  x  ",clueData[8])+")"
		else:
			radioLocText=""

		operatorText=''
		if self.useOperatorLogin:
			operatorText='Radio Dispatcher: '
			if self.operatorLastName.startswith('?'):
				operatorText+='Not logged in'
			else:
				operatorText+=self.operatorFirstName[0].upper()+self.operatorLastName[0].upper()+' '+self.operatorId

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
			{ # Name of Individual That Located Clue - not filled by radiolog, but,
			  #  use the right-justified space on this line to show radio dispatch operator
			  #  while still leaving space for someone to hand-write the individual's name
				'data':[[operatorText]],
				'heights':0.54,
				'widths':[1], # width doesn't matter, since text is right-justified
				'hvalign':['right','top'],
				'fontSize':10 # slightly smaller font
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
				# logging.info('   paragraph')
				return Paragraph(d,style)
			else:
				# logging.info('   NOT paragraph')
				return d

		for td in clueTableDicts:
			# logging.info('--- new table ---')
			# logging.info('-- raw table data --')
			# try:
			# 	logging.info(json.dumps(td,indent=3))
			# except:
				# logging.info(str(td))

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
				# see reportlab docs paragraph alignment section for propert alignment values
				# https://docs.reportlab.com/reportlab/userguide/ch6_paragraphs/
				if h=='center':
					style.alignment=1
				elif h=='right':
					style.alignment=2

			data=[[ParagraphOrNot(d,style) for d in row] for row in td['data']]
			# data=td['data']
			# logging.info('data:'+str(data))
			widths=td['widths']
			wsum=sum(td['widths'])
			# if width units are not inches, treat them as proportional units
			if sum(td['widths'])!=tableWidthInches:
				widths=[(w/wsum)*tableWidthInches for w in widths]
			# logging.info('widths='+str(widths))
			heights=td['heights']
			if isinstance(heights,(int,float)):
				heightsList=[heights for x in range(len(data))]
				heights=heightsList
			# logging.info('heights='+str(heights))
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
			# logging.info('setting table style:'+str(styleList))
			elements.append(t)
		doc.build(elements)

		# overlaying on the template https://gist.github.com/vsajip/8166dc0935ee7807c5bd4daa22a20937
		templatePDF=PdfReader(self.clueReportPdfFileName,'rb')
		templatePage=templatePDF.pages[0]
		overlayPDF=PdfReader(cluePdfOverlayName,'rb')
		templatePage.merge_page(overlayPDF.pages[0])
		outputPDF=PdfWriter()
		outputPDF.add_page(templatePage)
		with open(cluePdfName,'wb') as out_pdf:
			outputPDF.write(out_pdf)

		self.printPDF(cluePdfName)
		if self.use2WD and self.secondWorkingDir and os.path.isdir(self.secondWorkingDir):
			logging.info("copying clue report pdf to "+self.secondWorkingDir)
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
		self.optionsDialog.exec_() # force modal
		# show the login dialog after the options form has been closed
		if self.useOperatorLogin:
			self.showLoginDialog()
			
	def showLoginDialog(self):
		self.loginDialog.toggleShow()
		self.loginDialog.exec_() # force modal

	def fontsChanged(self):
		self.limitedFontSize=self.fontSize
		if self.limitedFontSize>self.maxLimitedFontSize:
			self.limitedFontSize=self.maxLimitedFontSize
		if self.limitedFontSize<self.minLimitedFontSize:
			self.limitedFontSize=self.minLimitedFontSize
		self.toolTipFontSize=int(self.limitedFontSize*2/3)
		self.menuFontSize=int(self.limitedFontSize*3/4)
		# preserve the currently selected tab, since something in this function
		#  causes the rightmost tab to be selected
		i=self.ui.tabWidget.currentIndex()
		self.ui.tableView.setStyleSheet("font-size:"+str(self.fontSize)+"pt")
		# for n in self.ui.tableViewList[1:]:
		# 	logging.info("n="+str(n))
		for x in self.ui.tabList:
			try:
				x.setStyleSheet('font-size:'+str(self.menuFontSize)+'pt')
			except: # may fail for elements that don't have styles, like dummies and spacers
				pass
		for x in self.ui.tableViewList: # doesn't inherit from tabList item style sheet
			try:
				# this could be a source of lag if the tableview has a lot of entries
				x.setStyleSheet("font-size:"+str(self.fontSize)+"pt")
			except: # may fail for elements that don't have styles, like dummies and spacers
				pass
		# don't change tab font size unless you find a good way to dynamically
		# change tab size and margins as well
##		self.ui.tabWidget.tabBar().setStyleSheet("font-size:"+str(self.fontSize)+"pt")
		self.redrawTables()
		self.ui.tabWidget.setCurrentIndex(i)
		self.ui.incidentNameLabel.setStyleSheet("font-size:"+str(self.limitedFontSize)+"pt;")

		# NOTE that setStyleSheet is DESTRUCTIVE, not INCREMENTAL.  To set a new style
		#  without affecting previous style settings for the same identifier, you
		#  need to use getStyleSheet()+"....".  To avoid confusion, do as many settings
		#  as possible in one text block as below.
		
		# hardcode dialog button box pushbutton font size to 14pt since QTDesiger-generated code doesn't work
		# self.parent.setStyleSheet("""
		# 	QMessageBox,QDialogButtonBox QPushButton {
		# 		font-size:14pt;
		# 	}
		# 	QToolTip {
		# 		font-size:"""+str(self.fontSize*2/3)+"""pt;
		# 		color:#555;
		# 	}
		# 	QMenu {
		# 		font-size:"""+str(self.limitedFontSize*3/4)+"""pt;
		# 	}
		# """)

		#259 - calling self.parent.setStyleSheet here - regardless of content - causes
		#  big delay when there are already hundreds of entries - 10sec for ~300 entries;
		#  many online posts say stylesheets are slow in general and should be avoided;
		#  so, incorporate methods here and elsewhere to accomplish what the stylesheet
		#  section above was accomplishing, without using stylesheets

		self.fsBuildTooltip()
		self.menuFont.setPointSize(self.menuFontSize)

	def redrawTables(self,index=0):
		# only redraw tables specified by index
		# - if index > 0, redraw that team's table, but don't redraw the main table
		# - if index = 0 (default), redraw main table and all team tables
		# - if index = -1, redraw main table only - don't redraw any team table

		redrawMainTable=index<=0
		# make a list of tables to redraw, since the code below is meant for a list
		if index==0: # redraw all team tables
			teamTablesToRedraw=self.ui.tableViewList[1:]
			tabsToScroll=range(1,self.ui.tabWidget.count())
		else:
			teamTablesToRedraw=[self.ui.tableViewList[index]]
			tabsToScroll=[index]

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
		# logging.info("1: start of redrawTables")
		if redrawMainTable:
			for i in [2,4]: # hardcode results in significant speedup
				self.ui.tableView.resizeColumnToContents(i) # zero is the first column
			# logging.info("2")
			self.ui.tableView.setColumnWidth(0,self.fontSize*5) # wide enough for '2345'
			self.ui.tableView.setColumnWidth(1,self.fontSize*6) # wide enough for 'FROM'
			self.ui.tableView.setColumnWidth(5,self.fontSize*10) # wide enough for 'STATUS'
			self.ui.tableView.setColumnWidth(10,self.fontSize*3) # wide enough for 'WW'
			self.ui.tableView.scrollToBottom()
		# logging.info("3")
##		self.ui.tableView.resizeRowsToContents()
		# logging.info("4")
		for n in teamTablesToRedraw:
			# logging.info(" n="+str(n))
			for i in [2,4]: # hardcode results in significant speedup, but lag still scales with filtered table length
				# logging.info("    i="+str(i))
				n.resizeColumnToContents(i)
			# logging.info("    done with i")
			n.setColumnWidth(0,self.fontSize*5)
			n.setColumnWidth(1,self.fontSize*6)
			n.setColumnWidth(5,self.fontSize*10)
			n.setColumnWidth(10,self.fontSize*3)
			# logging.info("    resizing rows to contents")
##			n.resizeRowsToContents()
		# logging.info("5")
		# logging.info("6")
		# can this section be made to scroll only one table as well?
		#  (is the index the same for tabWidget as for tableViewList?)
		for i in tabsToScroll:
			self.ui.tabWidget.setCurrentIndex(i)
			self.ui.tableViewList[i].scrollToBottom()
		# logging.info("7: end of redrawTables")
##		self.resizeRowsToContentsIfNeeded()
		self.loadFlag=False

	def setTeamStatus(self,extTeamName,status):
		teamStatusDict[extTeamName]=status
		#715 redraw the sidebar here, regardless of visibility but only when needed, rather than
		#  every second in updateTeamTimers, based on visibility, which doesn't happen until the next tick
		self.sidebar.resizeEvent()

	def updateClock(self):
		self.ui.clock.display(time.strftime("%H:%M"))

	def updateTeamTimers(self):
		# logging.info('timers:'+str(teamTimersDict))
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
			if self.newEntryWindowHiddenPopup.isVisible():
				self.newEntryWindowHiddenPopup.setStyleSheet('color:black;background:lightgray')
			# blink finger tabs of new entries that have children
			if teamTimersDict: # to avoid errors before first newEntryWidget is created
				tw=self.newEntryWindow.ui.tabWidget
				for new in newEntryWidget.instances:
					i=tw.indexOf(new)
					tb=tw.tabBar().tabButton(i,QTabBar.LeftSide)
					w=tb.layout().itemAt(1).widget()
					t=time.strftime("%H%M")+" "+new.ui.to_fromField.currentText()+" "+new.ui.teamField.text()
					if new.childDialogs:
						w.setText('<font color="red"><b>'+t+'</b></font>')
					else:
						w.setText(t)

		else:
			self.blinkToggle=0
			# now make sure the help window color code bars blink too
			self.helpWindow.ui.colorLabel4.setStyleSheet(statusStyleDict["Waiting for Transport"])
			self.helpWindow.ui.colorLabel5.setStyleSheet(statusStyleDict[""])
			self.helpWindow.ui.colorLabel6.setStyleSheet(statusStyleDict[""])
			self.helpWindow.ui.colorLabel7.setStyleSheet(statusStyleDict["STANDBY"])
			self.helpWindow.ui.fsSomeFilteredLabel.setFont(self.helpFont1)
			if self.newEntryWindowHiddenPopup.isVisible():
				self.newEntryWindowHiddenPopup.setStyleSheet('color:white;background:red')
			# blink finger tabs of new entries that have children
			if teamTimersDict: # to avoid errors before first newEntryWidget is created
				tw=self.newEntryWindow.ui.tabWidget
				for new in newEntryWidget.instances:
					i=tw.indexOf(new)
					tb=tw.tabBar().tabButton(i,QTabBar.LeftSide)
					w=tb.layout().itemAt(1).widget()
					t=time.strftime("%H%M")+" "+new.ui.to_fromField.currentText()+" "+new.ui.teamField.text()
					color='#999'
					if new==tw.currentWidget():
						color='#ccc'
					if new.childDialogs:
						w.setText('<font color="'+color+'"><b>'+t+'</b></font>')
					else:
						w.setText(t)

		# 751 - these lines are for debug purposes only
		# for widget in newEntryWidget.instances:
		# 	logging.info('lastModAge for '+str(widget)+':'+str(widget.lastModAge))

		teamTabsMoreButtonBlinkNeeded=False
		for extTeamName in teamTimersDict:
			secondsSinceContact=teamTimersDict.get(extTeamName,0)
			# logging.info('extTeamName='+str(extTeamName)+'  secondsSinceContact='+str(secondsSinceContact)+'  hiddenTeamTabsList:'+str(self.hiddenTeamTabsList)+'  extTeamNameList:'+str(self.extTeamNameList))
			if extTeamName not in self.hiddenTeamTabsList:
				# logging.info('updateTeamTimers processing '+extTeamName)
				# if there is a newEntryWidget currently open for this team, don't blink,
				#  but don't reset the timer.  Only reset the timer when the dialog is accepted.
				hold=False
				for widget in newEntryWidget.instances:
					if widget.ui.to_fromField.currentText()=="FROM" and getExtTeamName(widget.ui.teamField.text())==extTeamName:
						hold=True
				i=self.extTeamNameList.index(extTeamName)
				status=teamStatusDict.get(extTeamName,"")
				fsFilter=teamFSFilterDict.get(extTeamName,0)
	##			logging.info("blinking "+extTeamName+": status="+status)
	# 			logging.info("fsFilter "+extTeamName+": "+str(fsFilter))
				# secondsSinceContact=teamTimersDict.get(extTeamName,0)
				button=self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide)
				# logging.info('  i='+str(i)+'  status='+str(status)+'  filter='+str(fsFilter)+'  blink='+str(self.blinkToggle)+'  button='+str(button))
				styleObjectName='tab_'+extTeamName
				#741 wrap this entire if/else clause in a check to see if button exists;
				#  it should always exist now, due to other fixes for #741
				if button:
					if status in ["Waiting for Transport","STANDBY","Available"] or (secondsSinceContact>=self.timeoutOrangeSec):
						# if a team status is blinking, and the tab is not visible due to scrolling of a very wide tab bar,
						#  then blink the three-dots icon; but this test may be expensive so don't test again after the first hit
						#  https://stackoverflow.com/a/28805583/3577105
						if not teamTabsMoreButtonBlinkNeeded and button.visibleRegion().isEmpty():
							teamTabsMoreButtonBlinkNeeded=True
						if self.blinkToggle==0:
							# blink 0: style is one of these:
							# - style as normal per status
							button.setStyleSheet(buildObjSS(styleObjectName,statusStyleDict[status]))
						else:
							# blink 1: style is one of these:
							# - timeout orange
							# - timeout red
							# - no change (if status is anything but 'Waiting for transport' or 'STANDBY')
							# - blank (black on white) (if status is 'Waiting for transport' or 'STANDBY', and not timed out)
							if not hold and status not in ["At IC","Off Duty"] and secondsSinceContact>=self.timeoutRedSec:
								button.setStyleSheet(buildObjSS(styleObjectName,statusStyleDict["TIMED_OUT_RED"]))
							elif not hold and status not in ["At IC","Off Duty"] and (secondsSinceContact>=self.timeoutOrangeSec and secondsSinceContact<self.timeoutRedSec):
								button.setStyleSheet(buildObjSS(styleObjectName,statusStyleDict["TIMED_OUT_ORANGE"]))
							elif status=="Waiting for Transport" or status=="STANDBY" or status=="Available":
								button.setStyleSheet(buildObjSS(styleObjectName,statusStyleDict[""]))
					else:
						# not Waiting for Transport or Available, and not in orange/red time zone: draw the normal style
						button.setStyleSheet(buildObjSS(styleObjectName,statusStyleDict[status]))
				else:
					logging.info('ERROR in updateTeamTimers: attempted to update appearance for a non-existent tab for '+str(extTeamName))
					
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

		if teamTabsMoreButtonBlinkNeeded:
			self.teamTabsMoreButtonIsBlinking=True
			if self.blinkToggle==0:
				self.ui.teamTabsMoreButton.setIcon(self.blankIcon)
			else:
				self.ui.teamTabsMoreButton.setIcon(self.teamTabsMoreButtonIcon)
		# when blinking stops, make sure the normal icon is shown
		elif self.teamTabsMoreButtonIsBlinking:
			self.ui.teamTabsMoreButton.setIcon(self.teamTabsMoreButtonIcon)
			self.teamTabsMoreButtonIsBlinking=False

		#715 redraw the sidebar from setTeamStatus, regardless of visibility but only when needed,
		#  rather than here every second based on visibility which doesn't happen until the next tick
		# if self.sidebarIsVisible: #.isVisible would always return True - it's slid left when 'hidden'
		# 	self.sidebar.resizeEvent()
		self.sidebar.setTeamTableColors()

		for sld in subjectLocatedDialog.instances:
			sld.countdown()
			if sld.lastModAge>=0:
				sld.lastModAge+=1

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
		# update for #683 - get rid of this clause, to allow mainWindow keyPress handling while
		#  pending-entry message box is open
			# if self.newEntryWindow.isVisible():
			if False:
				logging.info("** keyPressEvent ambiguous timing; key press ignored: key="+str(hex(event.key())))
				event.ignore()
			else:
				key=event.text().lower() # hotkeys are case insensitive
				mod=event.modifiers()
				# logging.info("  key:"+QKeySequence(event.key()).toString()+"  mod:"+str(mod))
				# logging.info("  key:"+QKeySequence(event.key()).toString())
				# logging.info('  key:'+key+'  mod:'+str(mod))
				if mod==Qt.ControlModifier and event.key()==Qt.Key_F:
					self.findDialogShowHide()
				elif self.ui.teamHotkeysWidget.isVisible():
					# these key handlers apply only if hotkeys are enabled:
					if key in self.hotkeyDict.keys():
						logging.info('team hotkey "'+str(key)+'" pressed; calling openNewEntry')
						self.openNewEntry(key)
				else:
					# these key handlers apply only if hotkeys are disabled:
					if re.match(r'\d',key):
						logging.info('non-team-hotkey "'+str(key)+'" pressed; calling openNewEntry')
						self.openNewEntry(key)
					elif key=='t' or event.key()==Qt.Key_Right:
						logging.info('non-team-hotkey "'+str(key)+'" pressed; calling openNewEntry')
						self.openNewEntry('t')
					elif key=='f' or event.key()==Qt.Key_Left:
						logging.info('non-team-hotkey "'+str(key)+'" pressed; calling openNewEntry')
						self.openNewEntry('f')
					elif key=='a':
						logging.info('non-team-hotkey "'+str(key)+'" pressed; calling openNewEntry')
						self.openNewEntry('a')
					elif key=='s':
						logging.info('non-team-hotkey "'+str(key)+'" pressed; calling openNewEntry')
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
				elif event.key()==Qt.Key_F9:
					if self.useOperatorLogin:
						self.loginDialog.toggleShow()
				elif event.key()==Qt.Key_F10:
					self.teamNotesDialog.toggleShow()
				elif event.key()==Qt.Key_F12:
					self.toggleTeamHotkeys()
				elif event.key()==Qt.Key_Enter or event.key()==Qt.Key_Return:
					logging.info('Enter or Return pressed; calling openNewEntry')
					self.openNewEntry('pop')
				elif key=='`' or key=='~':
					self.sidebarShowHide()
				elif event.key()==Qt.Key_Escape:
					if self.sidebar.pos().x()>-100:
						self.sidebarShowHide()
				event.accept()
		else:
			event.ignore()

	def closeEvent(self,event):
		# logging.info('closeEvent called.  radioLogNeedsPrint='+str(self.radioLogNeedsPrint)+'  clueLogNeedsPrint='+str(self.clueLogNeedsPrint))
		self.exitClicked=True
		msg=''
		# if radioLogNeedsPrint or clueLogNeedsPrint is True, bring up the print dialog
		if self.radioLogNeedsPrint or self.clueLogNeedsPrint:
			logging.info("needs print!")
			self.printDialog.exec_()
			# logging.info('-->inside closeEvent, after printDialog exec: radioLogNeedsPrint='+str(self.radioLogNeedsPrint)+'  clueLogNeedsPrint='+str(self.clueLogNeedsPrint))
			if self.radioLogNeedsPrint or self.clueLogNeedsPrint:
				msg='\n\n(There is unprinted data.)'
		else:
			logging.info("no print needed")
			msg='\n\n(No printing is required.)'
		# note, this type of messagebox is needed to show above all other dialogs for this application,
		#  even the ones that have WindowStaysOnTopHint.  This works in Vista 32 home basic.
		#  if it didn't show up on top, then, there would be no way to close the radiolog other than kill.
		really=QMessageBox(QMessageBox.Warning,"Please Confirm","Exit the Radio Log program?"+msg,
			QMessageBox.Yes|QMessageBox.No,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
		really.setDefaultButton(QMessageBox.No)
		# really.setFont(self.messageBoxFont)
		# really.font().setPointSize(32)
		really.show()
		really.raise_()
		if really.exec_()==QMessageBox.No:
			event.ignore()
			self.exitClicked=False
			return

		# update the usage dictionaries
		if self.useOperatorLogin:
			logging.info('Updating operator usage statistics from MyWindow.closeEvent.  List of operators before update:\n'+str(self.getOperatorNames()))
			t=int(time.time())
			ods=[d for d in self.operatorsDict['operators'] if d['lastName']==self.operatorLastName and d['firstName']==self.operatorFirstName and d['id']==self.operatorId]
			if len(ods)==1:
				od=ods[0]
				if 'usage' in od.keys():
					# there could be more than one usage dict with stop=null, if radiolog crashed;
					#  we need to make sure we are updating the most recent one
					usageDicts=[d for d in od['usage'] if d['stop']==None]
					usageDicts.sort(key=lambda x:x['start'])
					usageDict=usageDicts[0]
					usageDict['stop']=t
					usageDict['next']=None
			elif not self.operatorLastName.startswith('?'):
				logging.info('ERROR: operatorDict had '+str(len(ods))+' matches; should have exactly one match.  Operator usage will not be updated.')
			self.saveOperators()

		self.save(finalize=True)
		self.fsSaveLookup()
		self.fsSaveLog(finalize=True)
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
			logging.info("restoring initial window tracking behavior ("+str(self.initialWindowTracking)+")")
			win32gui.SystemParametersInfo(win32con.SPI_SETACTIVEWINDOWTRACKING,self.initialWindowTracking)

		# 662 added for debugging - copy the operator file into the run dir on startup and on shutdown
		#  (#724: only if the file exists!)
		if os.path.isfile(os.path.join(self.configDir,self.operatorsFileName)):
			shutil.copy(os.path.join(self.configDir,self.operatorsFileName),os.path.join(self.sessionDir,'operators_at_shutdown.json'))

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

	def checkForResize(self):
		# this is probably cleaner, lighter, and more robust than using resizeEvent
		(x,y,w,h)=self.geometry().getRect()
		if x!=self.x or y!=self.y or w!=self.w or h!=self.h:
			logging.info('resize detected; saving rc file and redawing sidebar')
			self.x=x
			self.y=y
			self.w=w
			self.h=h
			self.saveRcFile()
			self.sidebar.redraw()
		
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

	def loadOperators(self):
		# logging.info('loadOperators called')
		fileName=os.path.join(self.configDir,self.operatorsFileName)
		try:
			with open(fileName,'r') as ofile:
				logging.info('Loading operator data from file '+fileName)
				self.operatorsDict=json.load(ofile)
				logging.info('  loaded these operators:'+str(self.getOperatorNames()))
		except:
			logging.info('WARNING: Could not read operator data file '+fileName)
			logging.info('  isfile: '+str(os.path.isfile(fileName)))

	def saveOperators(self):
		logging.info('saveOperators called')
		names=self.getOperatorNames()
		if len(names)==0:
			logging.info('  the operators list is empty; skipping the operator save operation')
			return
		fileName=os.path.join(self.configDir,self.operatorsFileName)
		try:
			with open(fileName,'w') as ofile:
				logging.info('Saving operator data file '+fileName+' with these operators:'+str(names))
				json.dump(self.operatorsDict,ofile,indent=3)
		except:
			logging.info('WARNING: Could not write operator data file '+fileName)
			logging.info('  isfile: '+str(os.path.isfile(fileName)))

	def getOperatorNames(self):
		errs=[]
		names=[]
		if isinstance(self.operatorsDict,dict) and 'operators' in self.operatorsDict.keys():
			operators=self.operatorsDict['operators']
			for operator in operators:
				if isinstance(operator,dict):
					keys=operator.keys()
					if 'lastName' in operator.keys() and 'firstName' in operator.keys():
						names.append(str(operator['lastName']+','+str(operator['firstName'])))
					else:
						names.append('malformed entry - does not have lastName or firstName')
						errs.append('missing keys in one or more operator elements')
				else:
					errs.append('operator element is not a dictionary')
		else:
			errs.append('self.operatorsDict is not a dictonary and/or does not have an "operators" key')
		if errs:
			logging.info('error(s) on parsing self.operatorsDict:\n  '+'\n  '.join(errs))
			logging.info('printing self.operatorsDict due to errors:')
			if isinstance(self.operatorsDict,dict):
				logging.info(json.dumps(self.operatorsDict))
			else:
				logging.info(str(self.operatorsDict))
		return names

	def save(self,finalize=False):
		csvFileNameList=[os.path.join(self.sessionDir,self.csvFileName)]
		if self.use2WD and self.secondWorkingDir and os.path.isdir(self.secondWorkingDir):
			csvFileNameList.append(os.path.join(self.secondWorkingDir,self.csvFileName)) # save flat in second working dir
		for fileName in csvFileNameList:
			logging.info("  writing "+fileName)
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
			logging.info("  done writing "+fileName)
		# now write the clue log to a separate csv file: same filename appended by '.clueLog'
		if len(self.clueLog)>0:
			for fileName in csvFileNameList:
				fileName=fileName.replace(".csv","_clueLog.csv")
				logging.info("  writing "+fileName)
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
				logging.info("  done writing "+fileName)

	def load(self,sessionToLoad=None,bakAttempt=0):
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

		colCount=10
		if self.useOperatorLogin:
			colCount=11
		if not sessionToLoad:
			sessions=self.getSessions(reverse=True,omitCurrentSession=True)
			if not sessions:
				logging.info('There are no available sessions to load.')
				return
			ld=loadDialog(self)
			ld.ui.theTable.setRowCount(len(sessions))
			row=0
			for session in sessions:
				highestClueNumStr=str(self.getLastClueNumber(session['usedClueNames']))
				if highestClueNumStr=='0':
					highestClueNumStr='--'
				q0=QTableWidgetItem(session['incidentName'])
				q1=QTableWidgetItem(str(session['lastOP']))
				q2=QTableWidgetItem(highestClueNumStr)
				q3=QTableWidgetItem(time.strftime("%m/%d/%Y %H:%M:%S",time.localtime(session['mtime'])))
				q0.setToolTip(session['filenameBase'])
				q0.setData(Qt.UserRole,session)
				q1.setToolTip(session['filenameBase'])
				q2.setToolTip(session['filenameBase'])
				q3.setToolTip(session['filenameBase'])
				ld.ui.theTable.setItem(row,0,q0)
				ld.ui.theTable.setItem(row,1,q1)
				ld.ui.theTable.setItem(row,2,q2)
				ld.ui.theTable.setItem(row,3,q3)
				row+=1
			ld.show()
			ld.raise_()
			rval=ld.exec_()

		else: # entry point when session is specified (from load dialog, or continued incident dialog, or restore)
			filenameBase=sessionToLoad['filenameBase']
			fileName=filenameBase+'.csv'
			if bakAttempt:
				fName=fileName.replace('.csv','_bak'+str(bakAttempt)+'.csv')
				logging.info('Loading backup: '+fName)
			else:
				fName=fileName
				logging.info("Loading: "+fileName)
			progressBox=QProgressDialog("Loading, please wait...","Abort",0,100)
			progressBox.setWindowModality(Qt.WindowModal)
			progressBox.setWindowTitle("Loading")
			progressBox.show()
			QCoreApplication.processEvents()
			self.teamTimer.start(10000) # pause
			# pass 1: count total entries for the progress box, and read incident name
			# logging.info('pass1: '+fName)
			self.incidentName=sessionToLoad['incidentName']
			self.optionsDialog.ui.incidentField.setText(self.incidentName)
			self.ui.incidentNameLabel.setText(self.incidentName)
			logging.info("loaded incident name: '"+self.incidentName+"'")
			self.incidentNameNormalized=normName(self.incidentName)
			logging.info("normalized loaded incident name: '"+self.incidentNameNormalized+"'")
			try: # in case the file is corrupted, i.e. after a power outage
				with open(fName,'r') as csvFile:
					csvReader=csv.reader(csvFile)
					totalEntries=0
					for row in csvReader:
						if not row[0].startswith('#'): # prune comment lines
							if len(row)<9:
								raise Exception('Row does not contain enough columns; the file may be corrupted.\n  File:'+fName+'\n  Row:'+str(row))
							totalEntries=totalEntries+1
				progressBox.setMaximum(totalEntries+14)
				progressBox.setValue(1)
			except Exception as e:
				logging.info('  CSV could not be read: '+str(e))
				if bakAttempt<5 and os.path.isfile(fileName.replace('.csv','_bak'+str(bakAttempt+1)+'.csv')):
					logging.info('Trying to load the next most recent backup file...')
					self.load(sessionToLoad=sessionToLoad,bakAttempt=bakAttempt+1)
					progressBox.close()
					return # to avoid running pass2 and subsequent code for the initial non-bak attempt
				else:
					progressBox.close()
					msg='The original file was corrupted, and none of the availble backup files (if any) could be read.\n\nAborting the load operation.'
					bakMsgBox=QMessageBox(QMessageBox.Critical,"Load failed",msg,
								QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
					bakMsgBox.exec_() # modal
					return False # error
				
			if sessionToLoad['lastOP']!=self.opPeriod:
				self.opPeriod=sessionToLoad['lastOP'] # don't increment - we're not continuing, we're just loading as-is
				self.printDialog.ui.opPeriodComboBox.addItem(str(self.opPeriod))
				self.opPeriodDialog.ui.currentOpPeriodField.setText(str(self.opPeriod))
				self.opPeriodDialog.ui.newOpPeriodField.setMinimum(self.opPeriod+1) # do this before setting the value, in case the new value is less than the old minimum
				self.opPeriodDialog.ui.newOpPeriodField.setValue(self.opPeriod+1)
				logging.info('Setting OP to '+str(self.opPeriod)+' based on loaded session.')

			# pass 2: read and process the file
			# logging.info('pass2: '+fName)
			with open(fName,'r') as csvFile:
				csvReader=csv.reader(csvFile)
				loadedRadioLog=[]
				i=0
				for row in csvReader:
					if not row[0].startswith('#') and len(row)>9: # prune comment lines and lines with not enough elements
						row[6]=float(row[6]) # convert epoch seconds back to float, for sorting
						row += [''] * (colCount-len(row)) # pad the row up to 10 or 11 elements if needed, to avoid index errors elsewhere
						loadedRadioLog.append(row)
						i=i+1
				csvFile.close()
			progressBox.setValue(2)

			logging.info('  t1 - done reading file')
			# now add entries, sort, and prune any Begins lines after the first line
			# edit: don't prune Begins lines - those are needed to indicate start of operational periods
			# move loadFlag True then False closer in to the newEntry commands, to
			#  minimize opportunity for failed entries due to self.loadFlag being
			#  left at True, probably due to early return above (see #340)
			self.loadFlag=True
			i=2
			for row in loadedRadioLog:
				QCoreApplication.processEvents() # required to check for progress box cancel
				if progressBox.wasCanceled():
					progressBox.close()
					msg='Load aborted.\n\nThe radiolog may be in an indeterminate state.\n\nYou should probably exit and restart RadioLog.'
					logging.info(msg.replace('\n',' '))
					box=QMessageBox(QMessageBox.Critical,"Load failed",msg,
								QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
					box.exec_() # modal
					return
				self.newEntry(row)
				i=i+1
				progressBox.setValue(i)
			self.loadFlag=False

			self.loadTeamNotes(os.path.join(os.path.dirname(fName),self.teamNotesFileName))
			self.rebuildTabs() # since rebuildTabs was disabled when loadFlag was True
			logging.info('  t2')
			self.radioLog.sort(key=lambda entry: entry[6]) # sort by epoch seconds
			i=i+1
			progressBox.setValue(i)
##		self.radioLog[1:]=[x for x in self.radioLog[1:] if not x[3].startswith('Radio Log Begins:')]

		# take care of the newEntry cleanup functions that have been put off due to loadFlag

# apparently, we need to emit layoutChanged and then scrollToBottom, before resizeColumnToContents,
#  to make sure column width resizes to fit >all< contents (i.e 'Team 5678'). ??
# they could be put inside redrawTables, but, there's no need to put them inside that
#  function which is called from other places, unless another syptom shows up; so, leave
#  them here for now.
			logging.info('  t3')
			self.ui.tableView.model().layoutChanged.emit()
			i=i+1
			progressBox.setValue(i)
			logging.info('  t4')
			self.ui.tableView.scrollToBottom()
			i=i+1
			progressBox.setValue(i)
			logging.info('  t5')
	##		self.ui.tableView.resizeRowsToContents()
	##		for i in range(self.ui.tabWidget.count()):
	##			self.ui.tabWidget.setCurrentIndex(i)
	##			self.ui.tableViewList[i].scrollToBottom()
	##			self.ui.tableViewList[i].resizeRowsToContents()

	##		self.ui.tableView.model().layoutChanged.emit()

			self.usedClueNames=sessionToLoad['usedClueNames']
			# now load the clue log (same filename appended by .clueLog) if it exists
			clueLogFileName=fileName.replace(".csv","_clueLog.csv")
			# global lastClueNumber
			# global usedClueNames
			if os.path.isfile(clueLogFileName):
				with open(clueLogFileName,'r') as csvFile:
					csvReader=csv.reader(csvFile)
	##				self.clueLog=[] # uncomment this line to overwrite instead of combine
					for row in csvReader:
						# logging.info(f'row:{row}')
						if not row[0].startswith('#'): # prune comment lines
							self.clueLog.append(row)
							clueName=''
							if row[0]!="":
								clueName=row[0]
					csvFile.close()
			logging.info(f'end of load clueLog: usedClueNames={self.usedClueNames}  last clue number={self.getLastClueNumber()}')

			i=i+1
			progressBox.setValue(i)
			logging.info('  t6')
			self.clueLogDialog.ui.tableView.model().layoutChanged.emit()
			i=i+1
			progressBox.setValue(i)
			logging.info('  t7')
			# finished
			# logging.info("Starting redrawTables")
			self.fontsChanged()
			i=i+1
			progressBox.setValue(i)
			logging.info('  t8')
	##		self.ui.tableView.model().layoutChanged.emit()
	##		QCoreApplication.processEvents()
			# logging.info("Returned from redrawTables")
			# progressBox.close()
			i=i+1
			progressBox.setValue(i)
			logging.info('  t9')
			self.ui.opPeriodButton.setText("OP "+str(self.opPeriod))
			i=i+1
			progressBox.setValue(i)
			logging.info('  t10')
			self.teamTimer.start(1000) #resume
			i=i+1
			progressBox.setValue(i)
			logging.info('  t11')
			self.lastSavedFileName="NONE"
			i=i+1
			progressBox.setValue(i)
			logging.info('  t12')
			self.updateFileNames() # note, no file will be saved until the next entry is made
			i=i+1
			progressBox.setValue(i)
			logging.info('  t13')
			self.saveRcFile()
			i=i+1
			progressBox.setValue(i)
			logging.info('  t14')
			if bakAttempt>0:
				msg='RadioLog data file(s) were corrupted.\n\nBackup '+str(bakAttempt)+' was automatically loaded from '+fName+'.\n\nUp to '+str(bakAttempt*5)+' of the most recent entries are lost.'
				bakMsgBox=QMessageBox(QMessageBox.Warning,"Backup file used",msg,
								QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
				bakMsgBox.exec_() # modal
			progressBox.close()
			if self.sidebar.isVisible():
				self.sidebar.showEvent() # refresh display
			#788: not sure why this fixes tabBar width issues; could investigate more in the future
			w=self.width()
			h=self.height()
			self.resize(w+1,h)
			self.resize(w,h)
			return True # success

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
					logging.info(err.replace('\n',' '))
					self.errMsgBox=QMessageBox(QMessageBox.Critical,"Session Directory Error",err,
									QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
					self.errMsgBox.exec_()
				else:
					self.sessionDir=sessionDirAttempt
					setLogHandlers(self.sessionDir) # resume log file in new location, regardless of rename outcome
					logging.info('Renamed session directory to "'+self.sessionDir+'"')
		self.csvFileName=getFileNameBase(self.incidentNameNormalized)+".csv"
		self.pdfFileName=getFileNameBase(self.incidentNameNormalized)+".pdf"
		self.fsFileName=self.csvFileName.replace('.csv','_fleetsync.csv')
		self.fsLogFileName=self.csvFileName.replace('.csv','_fsLog.csv')

	def optionsAccepted(self):
		tmp=self.optionsDialog.ui.incidentField.text()
		if self.incidentName!=tmp:
			logging.info(f'Incident name changed from "{self.incidentName}" to "{tmp}".') # note that this gets called from code as well as GUI
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
		logging.info("openNewEntry called:key="+str(key)+" callsign="+str(callsign)+" formattedLocString="+str(formattedLocString)+" fleet="+str(fleet)+" dev="+str(dev)+" origLocString="+str(origLocString)+" amendFlag="+str(amendFlag)+" amendRow="+str(amendRow)+" isMostRecentForCallsign="+str(isMostRecentForCallsign))
		self.clearSelectionAllTables() # in case copy or context menu was in process
		rval='' # default return value; only used by #761
		# # 671 - setWindowFlags is expensive, increasing the lag based on how many times it's been called;
		# #  this may well be a python bug, but, take steps here to only call it when needed, by
		# #  comparing its previous value (stored in self.NEWFlags) to the new required value
		# nf1=self.NEWFlags
		# if clueDialog.openDialogCount==0:
		# 	self.NEWFlags=Qt.WindowTitleHint|Qt.WindowStaysOnTopHint
		# else:
		# 	self.NEWFlags=Qt.WindowTitleHint
		# if nf1!=self.NEWFlags:
		# 	self.newEntryWindow.setWindowFlags(self.NEWFlags)

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
				elif key=='nex': # spawned by NEXEDGE (Kenwood NXDN); let addTab determine focus
					pass
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
			#726 - don't steal focus to the callsign field unless it's also the active widget
			# if callsign[0:3]=='KW-':
			if callsign[0:3]=='KW-' and self.newEntryWidget==self.newEntryWindow.ui.tabWidget.currentWidget():
				self.newEntryWidget.ui.teamField.setFocus()
				self.newEntryWidget.ui.teamField.selectAll()
			# logging.info('fleet='+str(fleet)+'  dev='+str(dev)+'  fsLog:')
			# logging.info(str(self.fsLog))
			# i[7] = total call count; i[6] = mic bump count; we want to look at the total non-bump count, i[7]-i[6]
			#761 - allow for the case when there is no log entry at all for this device, due to sequence changes in #722
			matchingLogRows=[]
			if fleet and dev: # fleetsync
				matchingLogRows=[i for i in self.fsLog if i[0]==str(fleet) and i[1]==str(dev)]
			elif dev and not fleet: # NXDN
				matchingLogRows=[i for i in self.fsLog if i[0]=='' and i[1]==str(dev)]
			if not matchingLogRows or len([i for i in matchingLogRows if i[7]-i[6]<2])>0:
			# if (fleet and dev and len([i for i in self.fsLog if i[0]==str(fleet) and i[1]==str(dev) and (i[7]-i[6])<2])>0) or \
			#      (dev and not fleet and len([i for i in self.fsLog if i[0]=='' and i[1]==str(dev) and (i[7]-i[6])<2])>0) : # this is the device's first non-mic-bump call
				logging.info('First non-mic-bump call from this device.')
				rval='+CCD'
				if self.isInCCD1List(callsign):
					logging.info('Setting needsChangeCallsign since this is the first call from the device and the beginning of its default callsign "'+callsign+'" is specified in CCD1List')
					self.newEntryWidget.needsChangeCallsign=True
					# if it's the only item on the stack, open the change callsign
					#   dialog right now, since the normal event loop won't process
					#   needsChangeCallsign until the tab changes
					if self.newEntryWidget==self.newEntryWindow.ui.tabWidget.currentWidget():
						QTimer.singleShot(500,lambda:self.newEntryWidget.promptForCallsign())
					# note that self.changeCallsign (formerly changeCallsignDialog.accept) is responsible for
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
		
		return rval # only relevant for #761
	
	def isInCCD1List(self,callsign):
		found=False
		for i in self.CCD1List:
			if isinstance(i,str) and callsign.lower().startswith(i.lower()):
				found=True
		return found

	def getOperatorInitials(self):
		if self.useOperatorLogin:
			if self.operatorLastName.startswith('?'):
				return '??'
			else:
				return self.operatorFirstName[0].upper()+self.operatorLastName[0].upper()
		else:
			return ''

	def newEntry(self,values,amend=False,unhiding=False):
		# values array format: [time,to_from,team,message,locString,status,sec,fleet,dev]
		#  locString is also stored in the table in a column after dev, unmodified;
		#  the value in the 5th column is modified in place based on the datum and
		#  coordinate format; this is cleaner than formatting the coordinates in the
		#  QAbstractTableModel, because the hardcoded table values will show up in the
		#  saved file as expected.
		#  Only columns thru and including status are shown in the tables.
		logging.info("newEntry called with these values:")
		logging.info(values)
		# add operator initials if not already present
		if len(values)==10: 
			if self.useOperatorLogin:
				values.append(self.getOperatorInitials())
			else:
				values.append('')
		niceTeamName=values[2]
		extTeamName=getExtTeamName(niceTeamName)
		#766 force unhiding to True if extTeamName is in hiddenTeamTabsList
		# logging.info('hiddenTeamTabsList:'+str(self.hiddenTeamTabsList))
		if extTeamName in self.hiddenTeamTabsList:
			unhiding=True
		# if self.useOperatorLogin:
		# 	values[0]+=' ['+self.getOperatorInitials()+']'
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
# 			logging.info("new entry sec="+str(sec)+"; prev entry sec="+str(self.radioLog[i+1][6])+"; decrementing: i="+str(i))
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
# 		logging.info("inserting entry at index "+str(i))
		if not self.loadFlag:
			model.endInsertRows()
##		if not values[3].startswith("RADIO LOG SOFTWARE:"):
##			self.newEntryProcessTeam(niceTeamName,status,values[1],values[3])
		self.newEntryProcessTeam(niceTeamName,status,values[1],values[3],amend,unhiding=unhiding)

	def newEntryProcessTeam(self,niceTeamName,status,to_from,msg,amend=False,unhiding=False):
		# logging.info('t1: niceTeamName={} status={} to_from={} msg={} amend={}'.format(niceTeamName,status,to_from,msg,amend))
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
				self.newTeam(niceTeamName,unhiding=unhiding)
			i=self.extTeamNameList.index(extTeamName)
			# teamStatusDict[extTeamName]=status
			self.setTeamStatus(extTeamName,status)
			if not extTeamName in teamFSFilterDict:
				teamFSFilterDict[extTeamName]=0
			# credit to Berryblue031 for pointing out this way to style the tab widgets
			# http://www.qtcentre.org/threads/49025
			# NOTE the following line causes font-size to go back to system default;
			#  can't figure out why it doesn't inherit font-size from the existing
			#  styleSheet; so, each statusStyleDict entry must contain font-size explicitly
			#741 - pass through in case the button is None; shouldn't ever happen due to other fixes fo #741
			if not self.loadFlag:
				button=self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide)
				if button:
					button.setStyleSheet(statusStyleDict[status])
				else:
					logging.info(' ERROR: there was an attempt to set the styleSheet for a non-existent tab button:')
					logging.info('   extTeamName='+str(extTeamName)+'  i='+str(i)+'  tabBar count='+str(self.ui.tabWidget.tabBar().count()))
					logging.info('   extTeamNameList='+str(self.extTeamNameList))
					logging.info(' Skipping this attempt')
			# only reset the team timer if it is a 'FROM' message with non-blank message text
			#  (prevent reset on amend, where to_from can be "AMEND" and msg can be anything)
			# if this was an amendment, set team timer based on the team's most recent 'FROM' entry
			if amend:
				logging.info('t2')
				found=False
				for n in range(len(self.radioLog)-1,-1,-1):
					entry=self.radioLog[n]
					logging.info(' t3:'+str(n)+':'+str(entry))
					if getExtTeamName(entry[2]).lower()==extTeamName.lower() and entry[1]=='FROM':
						logging.info('  t4:match: now='+str(int(time.time())))
						logging.info('  setting teamTimersDict to '+str(time.time()-entry[6]))
						teamTimersDict[extTeamName]=int(time.time()-entry[6])
						found=True
						break
				# if there are 'from' entries for the callsign, use the oldest 'to' entry for the callsign
				if not found:
					for entry in self.radioLog:
						logging.info(' t3b:'+str(entry))
						if getExtTeamName(entry[2]).lower()==extTeamName.lower():
							logging.info('t4b:"TO" match: now='+str(int(time.time())))
							teamTimersDict[extTeamName]=int(time.time()-entry[6])
							found=True
							break
				# this code should never be reached: what does it mean if there are no TO or FROM entries after amend?
				if not found:
					logging.info('WARNING after amend: team timer may be undetermined because no entries (either TO or FROM) were found for '+str(niceTeamName))
			elif to_from=="FROM" and msg != "":
				teamTimersDict[extTeamName]=0
			# finally, disable timeouts as long as status is AT IC
			if status=="At IC":
				teamTimersDict[extTeamName]=-1 # no more timeouts will show up
		if not self.loadFlag:
			QTimer.singleShot(100,lambda:self.newEntryPost(extTeamName))

	def newEntryPost(self,extTeamName=None):
# 		logging.info("1: called newEntryPost")
		self.radioLogNeedsPrint=True
		# don't do any sorting at all since layoutChanged during/after sort is
		#  a huge cause of lag; see notes in newEntry function
# 		logging.info("3")
		# resize the bottom-most rows (up to 10 of them):
		#  this makes lag time independent of total row count for large tables,
		#  and reduces overall lag about 30% vs resizeRowsToContents (about 3 sec vs 4.5 sec for a 1300-row table)
		for n in range(len(self.radioLog)-10,len(self.radioLog)):
			if n>=0:
				self.ui.tableView.resizeRowToContents(n+1)
# 		logging.info("4")
		self.ui.tableView.scrollToBottom()
# 		logging.info("5")
		for i in [2,4]: # hardcode results in significant speedup
			self.ui.tableView.resizeColumnToContents(i)
# 		logging.info("5.1")
		# note, the following clause results in a small lag for very large team count
		#  and large radioLog (about 0.1sec on TomZen for 180kB log file); probably
		#  not worth trying to optimize
		for n in self.ui.tableViewList[1:]:
			for i in [2,4]: # hardcode results in significant speedup
				n.resizeColumnToContents(i)
# 		logging.info("5.2")
		if extTeamName:
# 			logging.info("5.2.1")
			if extTeamName=="ALL TEAMS":
				for i in range(1,len(self.extTeamNameList)):
					self.ui.tabWidget.setCurrentIndex(i)
					self.ui.tableViewList[i].resizeRowsToContents()
					for n in range(len(self.radioLog)-10,len(self.radioLog)):
						if n>=0:
							self.ui.tableViewList[i].resizeRowToContents(n+1)
					self.ui.tableViewList[i].scrollToBottom()
			elif extTeamName!="z_00000":
# 				logging.info("5.2.1.2")
				if extTeamName in self.extTeamNameList:
# 					logging.info("5.2.1.2.1")
					i=self.extTeamNameList.index(extTeamName)
# 					logging.info("  a: i="+str(i))
					self.ui.tabWidget.setCurrentIndex(i)
# 					logging.info("  b")
					self.ui.tableViewList[i].resizeRowsToContents()
# 					logging.info("  c")
					for n in range(len(self.radioLog)-10,len(self.radioLog)):
						if n>=0:
							self.ui.tableViewList[i].resizeRowToContents(n+1)
# 					logging.info("  d")
					self.ui.tableViewList[i].scrollToBottom()
# 					logging.info("  e")
# 		logging.info("6")
		if self.sidebar.isVisible():
			self.sidebar.showEvent() # refresh display
# 		logging.info("7")
		self.save()
		self.showTeamTabsMoreButtonIfNeeded()
##		self.redrawTables()
##		QCoreApplication.processEvents()
# 		logging.info("8: finished newEntryPost")

	def amendEntry(self,row): # row argument is zero-based
		logging.info("Amending row "+str(row))
		# logging.info('radioLog len = '+str(len(self.radioLog)))
		# logging.info(str(self.radioLog))
		# #508 - determine if the row being amended is the most recent row regarding the same callsign
		#    row argument is zero-based, and radiolog always has a dummy row at the end
		team=self.radioLog[row][2]
		extTeamName=getExtTeamName(team)
		found=False
		for n in range(row+1,len(self.radioLog)):
			entry=self.radioLog[n]
			logging.info(' t3:'+str(n)+':'+str(entry))
			if getExtTeamName(entry[2]).lower()==extTeamName.lower():
				found=True
				break
		if found:
			logging.info('found a newer entry for '+team+' than the one being amended')
		else:
			logging.info('did not find a newer entry for '+team+' than the one being amended')
		isMostRecent=not found
		logging.info('calling openNewEntry from amendEntry')
		self.openNewEntry(amendFlag=True,amendRow=row,isMostRecentForCallsign=isMostRecent)

	def rebuildTabs(self):
		# logging.info('calling rebuildTabs')
# 		groupDict=self.rebuildGroupedTabDict()
# 		tabs=[]
# 		for group in groupDict:
# 			tabs.extend(groupDict[group])
# 			tabs.append("")
# 		logging.info("Final tabs list:"+str(tabs))
# 		bar=self.ui.tabWidget.tabBar()
# 		for i in range(len(tabs)):
# 			bar.insertTab(i,tabs[i])
# 			if tabs[i]=="":
# 				bar.setTabEnabled(i,False)
# 		logging.info("extTeamNameList before sort:"+str(self.extTeamNameList))
# # 		self.extTeamNameList.sort()
# 		self.rebuildGroupedTabDict()
# 		logging.info("extTeamNameList after sort:"+str(self.extTeamNameList))
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
		#595: avoid right-left-shift-flicker by setting first tab visibility
		#  before adding other tabs; tab is visible by default
		self.addTab(self.extTeamNameList[0])
		# if not self.hiddenTeamTabsList:
		# 	self.ui.tabWidget.tabBar().setTabVisible(0,False)
		for extTeamName in self.extTeamNameList[1:]:
			self.addTab(extTeamName)
			self.teamNotesBuildTooltip(extTeamName)
# 		self.rebuildTeamHotkeys()
	
	def newTeam(self,newTeamName,unhiding=False):
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
		logging.info('new team: newTeamName='+newTeamName+' extTeamName='+extTeamName+' niceTeamName='+niceTeamName+' shortNiceTeamName='+shortNiceTeamName+' unhiding='+str(unhiding))
		self.extTeamNameList.append(extTeamName)
		logging.info("extTeamNameList before sort:"+str(self.extTeamNameList))
# 		self.extTeamNameList.sort()
		
		# remove from hiddenTeamTabsList immediately, to prevent downsteram errors in teamTabsPopup
		# 741 - keep track of whether this call is restoring a previously hidden team tab
		# restoringHidden=False
		# logging.info('hiddenTeamTabsList:'+str(self.hiddenTeamTabsList))
		if extTeamName in self.hiddenTeamTabsList:
			# restoringHidden=True
			self.hiddenTeamTabsList=[x for x in self.hiddenTeamTabsList if extTeamName!=x]

		# prevGroupCount=self.nonEmptyTabGroupCount
		prevGroups=self.nonEmptyTabGroups
		self.rebuildGroupedTabDict()
		logging.info("extTeamNameList after sort:"+str(self.extTeamNameList))
		if not self.loadFlag:
			# 670 - for the first team of a new session, and when unhiding the only tab
			#  (due to display issues noted in https://github.com/ncssar/radiolog/issues/670#issuecomment-1712814526)
			#  follow the old behavior and rebuild the entire tab bar;
			#  for subsequent teams, only add the tab for the new team
			# 741 - also rebuild tabs if restoring a hidden team tab
			# logging.info('restoringHidden='+str(restoringHidden)+'  prevGroupCount='+str(prevGroupCount)+'  nonEmptyTabGroupCount='+str(self.nonEmptyTabGroupCount)+'  tabBar.count='+str(self.ui.tabWidget.tabBar().count()))
			# logging.info('  prevGroups='+str(prevGroups)+'  nonEmptyTabGroups='+str(self.nonEmptyTabGroups))
			# if restoringHidden or prevGroupCount!=self.nonEmptyTabGroupCount or self.ui.tabWidget.tabBar().count()<2:
			# if restoringHidden or prevGroups!=self.nonEmptyTabGroups or self.ui.tabWidget.tabBar().count()<2:
			if unhiding or prevGroups!=self.nonEmptyTabGroups or self.ui.tabWidget.tabBar().count()<2:
				# logging.info('t1')
				self.rebuildTabs()
			else:
				# display issues when unhiding the rightmost tab
				#  https://github.com/ncssar/radiolog/issues/670#issuecomment-1712814526
				# so, if this would be the rightmost tab, activate a different tab first
				self.ui.tabWidget.tabBar().setCurrentIndex(0)
				# logging.info('t2: extTeamName='+str(extTeamName))
				self.addTab(extTeamName)
				# self.rebuildTabs() # this is the line we wanted to get away from in #670, to reduce lag, which is the reason for this entire if clause
		
		if not extTeamName.startswith("spacer"):
			# add to team name lists and dictionaries
			i=self.extTeamNameList.index(extTeamName) # i is zero-based
			self.teamNameList.insert(i,niceTeamName)
# 			logging.info("   niceTeamName="+str(niceTeamName)+"  allTeamsList before:"+str(self.allTeamsList)+"  count:"+str(self.allTeamsList.count(niceTeamName)))
			if self.allTeamsList.count(niceTeamName)==0:
				self.allTeamsList.insert(i,niceTeamName)
				self.allTeamsList.sort(key=lambda x:getExtTeamName(x))
				logging.info("   allTeamsList after:"+str(self.allTeamsList))
			#710 - preseve teamTimersDict  and teamCreatedTimeDict values e.g. on unhide
			if extTeamName not in teamTimersDict.keys():
				teamTimersDict[extTeamName]=0
			if extTeamName not in teamCreatedTimeDict:
				teamCreatedTimeDict[extTeamName]=time.time()
			# assign team hotkey
			hotkey=self.getNextAvailHotkey()
			logging.info("next available hotkey:"+str(hotkey))
			if hotkey:
				self.hotkeyDict[hotkey]=niceTeamName
			else:
				logging.info("Team hotkey pool has been used up.  Not setting any hotkeyDict entry for "+niceTeamName)
				
		if not self.loadFlag:
			self.rebuildTeamHotkeys()
			self.sidebar.showEvent()

		"""		
		i=self.extTeamNameList.index(extTeamName) # i is zero-based
		if len(self.extTeamNameList)>>i+1:
			if self.extTeamNameList[i+1]=="":
				logging.info("  spacer needed after this new team")
		if i>>0:
			if self.extTeamNameList[i-1]=="":
				logging.info("  spacer needed before this new team")
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
		logging.info("setting tab button #"+str(i)+" to "+label.text())
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
			logging.info("Team hotkey pool has been used up.  Not setting any hotkeyDict entry for "+niceTeamName)
		
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
##		logging.info("deleting")

		"""

	def addTab(self,extTeamName):
		if extTeamName in self.hiddenTeamTabsList:
			self.hiddenTeamTabsList=[x for x in self.hiddenTeamTabsList if extTeamName!=x]
			self.showTeamTabsMoreButtonIfNeeded()
		niceTeamName=getNiceTeamName(extTeamName)
		shortNiceTeamName=getShortNiceTeamName(niceTeamName)
		# logging.info("addTab: extTeamName="+extTeamName+" niceTeamName="+niceTeamName+" shortNiceTeamName="+shortNiceTeamName)
		i=self.extTeamNameList.index(extTeamName) # i is zero-based
		# logging.info("addTab: i="+str(i))
		# logging.info("addTab: tabList before insert:"+str(self.ui.tabList))
		self.ui.tabList.insert(i,QWidget())
		# logging.info("addTab: tabList after insert:"+str(self.ui.tabList))
		self.ui.tabList[i].setStyleSheet('font-size:'+str(self.menuFontSize)+'pt')
		self.ui.tabGridLayoutList.insert(i,QGridLayout(self.ui.tabList[i]))
		self.ui.tabGridLayoutList[i].setContentsMargins(5,2,5,5)
		self.ui.tabGridLayoutList[i].setSpacing(2)
		tv=CustomTableView(self,self.ui.tabList[i])
		tv.horizontalHeader().setMinimumSectionSize(10) # allow tiny column for operator initials
		tv.horizontalHeader().setDefaultAlignment(Qt.AlignHCenter)
		# tv.setEditTriggers(QAbstractItemView.AllEditTriggers)
		self.ui.tableViewList.insert(i,tv)
		self.ui.tableViewList[i].verticalHeader().setVisible(False)
		self.ui.tableViewList[i].setTextElideMode(Qt.ElideNone)
		self.ui.tableViewList[i].setFocusPolicy(Qt.ClickFocus)
		self.ui.tableViewList[i].setSelectionMode(QAbstractItemView.ContiguousSelection)
		self.ui.tableViewList[i].setStyleSheet("font-size:"+str(self.fontSize)+"pt")
		self.ui.tableViewList[i].setPalette(self.teamTablePalette)
		# self.ui.tableViewList[i].horizontalHeader().setMinimumSectionSize(10) # allow tiny column for operator initials
		# self.ui.tabGridLayoutList[i].addWidget(self.ui.tableViewList[i],0,0,1,1)
		if 'spacer' not in extTeamName.lower(): #717 - widgets for spacer tabs should be blank
			notes=QLabel('No notes for this callsign')
			self.ui.tabGridLayoutList[i].addWidget(notes,0,0,1,1)
			self.ui.tabGridLayoutList[i].addWidget(self.ui.tableViewList[i],1,0,1,1)
		self.ui.tabWidget.insertTab(i,self.ui.tabList[i],'')
		label=QLabel(" "+shortNiceTeamName+" ")
		if len(shortNiceTeamName)<2:
			label.setText("  "+shortNiceTeamName+"  ") # extra spaces to make effective tab min width
		if extTeamName.startswith("spacer"):
			label.setText("")
		else:
# 			logging.info("setting style for label "+extTeamName)
			label.setStyleSheet("font-size:18px;qproperty-alignment:AlignCenter")
# 			label.setStyleSheet(statusStyleDict[""])
		# logging.info("setting tab button #"+str(i)+" to "+label.text())
		bar=self.ui.tabWidget.tabBar()
		bar.setTabButton(i,QTabBar.LeftSide,label)
		# during rebuildTeamHotkeys, we need to read the name of currently displayed tabs.
		#  An apparent bug causes the tabButton (a label) to not have a text attrubite;
		#  so, use the whatsThis attribute instead.
		bar.setTabWhatsThis(i,niceTeamName)
# 		logging.info("setting style for tab#"+str(i))
# 		bar.tabButton(i,QTabBar.LeftSide).setStyleSheet("font-size:18px;qproperty-alignment:AlignHCenter")
		button=bar.tabButton(i,QTabBar.LeftSide)
		styleObjectName='tab_'+extTeamName
		button.setObjectName(styleObjectName)
		ss=buildObjSS(styleObjectName,statusStyleDict[""])
		logging.info('setting tab initial style in addTab: '+ss)
		button.setStyleSheet(ss)
# 		if not extTeamName.startswith("spacer"):
# 			label.setStyleSheet("font-size:40px;border:1px outset green;qproperty-alignment:AlignHCenter")
		# spacers should be disabled
		if extTeamName.startswith("spacer"):
			bar.setTabEnabled(i,False)

# 		if not extTeamName.startswith("spacer"):
# 			hotkey=self.getNextAvailHotkey()
# 			logging.info("next available hotkey:"+str(hotkey))
# 			if hotkey:
# 				self.hotkeyDict[hotkey]=niceTeamName
# 			else:
# 				logging.info("Team hotkey pool has been used up.  Not setting any hotkeyDict entry for "+niceTeamName)
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
		if not self.useOperatorLogin:
			self.ui.tableViewList[i].hideColumn(10) # hide operator initials
		self.ui.tableViewList[i].resizeRowsToContents()

		#NOTE if you do this section before the model is assigned to the tableView,
		# python will crash every time!
		# see the QHeaderView.ResizeMode docs for descriptions of each resize mode value
		# note QHeaderView.setResizeMode is deprecated in 5.4, replaced with
		# .setSectionResizeMode but also has both global and column-index forms
		self.ui.tableViewList[i].horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
		# automatically expand the 'message' column width to fill available space
		self.ui.tableViewList[i].horizontalHeader().setSectionResizeMode(3,QHeaderView.Stretch)
		self.redrawTables(i) # adjust columns widths on this table only
		
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
		# for etn in [getExtTeamName(x) for x in self.allTeamsList if not x.startswith("spacer")]: # spacerless list, including hidden tabs
		for etn in [x for x in self.extTeamNameList+self.hiddenTeamTabsList if not x.startswith("spacer")]: # spacerless list, including hidden tabs
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
			
		logging.info("grouped tabs:"+str(grouped))
		self.groupedTabDict=grouped
		
		# rebuild self.extTeamNameList, with groups and spacers in the correct order,
		#  since everything throughout the code keys off its sequence;
		#  note the spacer names need to be unique for later processing
		# also rebuild allTeamsList in the same sequence, which includes hidden teams
		self.extTeamNameList=['spacerLeft']
		self.allTeamsList=[]
		spacerIndex=1 # start with 1 so trailing 0 doesn't get deleted in getNiceTeamName
		for grp in self.tabGroups:
			spacerNeeded=False
# 			logging.info("group:"+str(grp)+":"+str(grouped[grp[0]]))
			for val in grouped[grp[0]]:
				self.allTeamsList.append(getNiceTeamName(val))
				if val not in self.hiddenTeamTabsList:
	# 				logging.info("appending:"+val)
					self.extTeamNameList.append(val)
					spacerNeeded=True
			#766 don't append a spacer after the group if all group members are hidden
			# if len(grouped[grp[0]])>0:
			if spacerNeeded:
				self.extTeamNameList.append("spacer"+str(spacerIndex))
				spacerIndex=spacerIndex+1
		for val in grouped["other"]:
			if val!="dummy":
				self.allTeamsList.append(getNiceTeamName(val))
				if val not in self.hiddenTeamTabsList:
	# 				logging.info("appending other:"+val)
					self.extTeamNameList.append(val)
		# self.nonEmptyTabGroupCount=len([v for v in grouped.values() if v])
		self.nonEmptyTabGroups=[k for k in grouped.keys() if grouped[k]]
		# logging.info('nonEmptyTabGroups:'+str(self.nonEmptyTabGroups))
			
	def tabContextMenu(self,pos):
		menu=QMenu()
		menu.setFont(self.menuFont)
		logging.info("tab context menu requested: pos="+str(pos))
##		menu.setStyleSheet("font-size:"+str(self.fontSize)+"pt")
		bar=self.ui.tabWidget.tabBar()
		pos-=bar.pos() # account for positional shift as set by stylesheet (when 'more' button is shown)
		i=bar.tabAt(pos) # returns -1 if not a valid tab
		logging.info("  i="+str(i)+"  tabRect="+str(bar.tabRect(i).bottomLeft())+":"+str(bar.tabRect(i).topRight()))
		extTeamName=self.extTeamNameList[i]
		niceTeamName=getNiceTeamName(extTeamName)
		logging.info("  extTeamName="+str(extTeamName)+"  niceTeamName="+str(niceTeamName))
# 		if i>0:
		if i>-1 and not extTeamName.lower().startswith("spacer"):
			newEntryFromAction=menu.addAction("New Entry FROM "+str(niceTeamName))
			newEntryToAction=menu.addAction("New Entry TO "+str(niceTeamName))
			menu.addSeparator()
			teamNotesAction=menu.addAction('Team Notes...')
			printTeamLogAction=menu.addAction(QIcon(QPixmap(":/radiolog_ui/icons/print_icon.png")),"Print "+str(niceTeamName)+" Log")
			menu.addSeparator()
##			relabelTeamTabAction=menu.addAction("Change Label / Assignment for "+str(niceTeamName))
##			menu.addSeparator()

		# add fleetsync submenu if there are any fleetsync devices for this callsign
			devices=self.fsGetTeamDevices(extTeamName)
			fsToggleAllAction=False # initialize, so the action checker does not die
			fsSendTextToAllAction=False # initialize, so the action checker does not die
			if len(devices)>0:
				fsMenu=menu.addMenu('FleetSync/NEXEDGE...')
				menu.addSeparator()
				if self.enableSendText:
					if len(devices)>1:
						fsSendTextToAllAction=fsMenu.addAction('Send text message to all '+niceTeamName+' devices')
						fsMenu.addSeparator()
					for device in devices:
						key=(device[0] or 'NX')+':'+device[1]
						fsMenu.addAction('Send text message to '+key).setData([device[0],device[1],'SendText'])
					fsMenu.addSeparator()
				if self.enablePollGPS:
					for device in devices:
						key=(device[0] or 'NX')+':'+device[1]
						fsMenu.addAction('Request location from '+key).setData([device[0],device[1],'PollGPS'])
					fsMenu.addSeparator()
				if len(devices)>1:
					if teamFSFilterDict[extTeamName]==2:
						fsToggleAllAction=fsMenu.addAction('Unfilter all '+niceTeamName+' devices')
					else:
						fsToggleAllAction=fsMenu.addAction('Filter all '+niceTeamName+' devices')
					fsMenu.addSeparator()
					for device in devices:
						key=(device[0] or 'NX')+':'+device[1]
						if self.fsIsFiltered(device[0],device[1]):
							fsMenu.addAction('Unfilter calls from '+key).setData([device[0],device[1],'unfilter'])
						else:
							fsMenu.addAction('Filter calls from '+key).setData([device[0],device[1],'filter'])
				else:
					key=(devices[0][0] or 'NX')+':'+devices[0][1]
					if teamFSFilterDict[extTeamName]==2:
						fsToggleAllAction=fsMenu.addAction('Unfilter calls from '+niceTeamName+' ('+key+')')
					else:
						fsToggleAllAction=fsMenu.addAction('Filter calls from '+niceTeamName+' ('+key+')')
			deleteTeamTabAction=menu.addAction('Hide tab for '+str(niceTeamName))
			#698 - single action to hide all tabs with status 'At IC'
			# - only show this context menu entry if this tab is At IC and
			#    more than one tab with this status exists
			deleteMultiAction=-1 # must exist for later action checking; don't use 'None' since this will trigger on Escape
			if teamStatusDict[extTeamName]=='At IC' and sum(x=='At IC' for x in teamStatusDict.values())>1:
				deleteMultiAction=menu.addAction('Hide tab for all \'At IC\' teams')

			# action handlers
			action=menu.exec_(self.ui.tabWidget.tabBar().mapToGlobal(pos))
			if action==newEntryFromAction:
				logging.info('calling openNewEntry (from '+str(niceTeamName)+') from team tab context menu')
				self.openNewEntry('tab',str(niceTeamName))
			elif action==newEntryToAction:
				logging.info('calling openNewEntry (to '+str(niceTeamName)+') from team tab context menu')
				self.openNewEntry('tab',str(niceTeamName))
				self.newEntryWidget.ui.to_fromField.setCurrentIndex(1)
			elif action==printTeamLogAction:
				logging.info('printing team log for '+str(niceTeamName))
				self.printLog(self.opPeriod,str(niceTeamName))
				self.radioLogNeedsPrint=True # since only one log has been printed; need to enhance this
			elif action==teamNotesAction:
				logging.info('opening team notes for '+str(niceTeamName))
				self.openTeamNotes(str(extTeamName))
			elif action==deleteTeamTabAction:
				logging.info('deleteTeamTabAction clicked')
				self.deleteTeamTab(niceTeamName)
			elif action==deleteMultiAction:
				logging.info('deleteMultiAction clicked')
				for ext in [e for e in self.extTeamNameList if teamStatusDict.get(e,None)=='At IC']:
					self.deleteTeamTab(getNiceTeamName(ext))
			elif action and action.data(): # only the single-device toggle/text/poll actions will have data
				d=action.data()
				if 'filter' in d[2].lower():
					self.fsFilterEdit(d[0],d[1],d[2].lower()=='filter')
					self.fsBuildTeamFilterDict()
				elif d[2]=='SendText':
					if d[0]: # fleetsync
						callsignText=self.getCallsign(d[0],d[1])
					else: # nxdn
						callsignText=self.getCallsign(d[1],None)
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
					logging.info('unknown context menu action:'+str(d))
			elif action==fsToggleAllAction:
				newState=teamFSFilterDict[extTeamName]!=2 # if 2, unfilter all; else, filter all
				for device in self.fsGetTeamDevices(extTeamName):
					self.fsFilterEdit(device[0],device[1],newState)
				self.fsBuildTeamFilterDict()
			elif action==fsSendTextToAllAction:
				theList=[]
				for device in self.fsGetTeamDevices(extTeamName):
					if device[0]: # fleetsync
						callsignText=self.getCallsign(device[0],device[1])
					else: # nxdn
						callsignText=self.getCallsign(device[1],None)
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
	# 	logging.info('trying to send - portList='+str(portList))
	# 	if portList and len(portList)>0:
	# 		for port in portList:
	# 			logging.info('Sending FleetSync data to '+str(port.name)+'...')
	# 			port.write(d.encode())
	# 	else:
	# 		logging.info('Cannot send FleetSync data - no open ports were found.')

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
	# 				logging.info('failed; need to send again')
	# 				if secondPortToTry:
	# 					self.fsAwaitingResponseMessageBox.setText('No response after sending from preferred radio.  Sending from alternate radio; awaiting response up to '+str(self.fsAwaitingResponseTimeout)+' seconds...')
	# 					secondPortToTry.write(d.encode())
	# 					self.fsAwaitingResponse[3]=0 # reset the timer
	# 			else:
	# 				logging.info('apparently successful')
	# 			self.fsAwaitingResponse=None # clear the flag - this will happen after the messagebox is closed (due to valid response, or timeout in fsCheck, or Abort clicked)






	# 	else: # this must be the recursive call where we actually send the data	
	# 		success=False
	# 		if port:
	# 			logging.info('Sending FleetSync data to '+str(port.name)+'...')
	# 			port.write(d.encode())
	# 			return True
	# 		else:
	# 			msg='Cannot send FleetSync data - no valid FleetSync COM ports were found.  Keying the mic on a portable radio will trigger COM port recognition.'
	# 			logging.info(msg)
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
	#   for NEXEDGE, insert 67 hex (lowecase g) after 02
	# <length_code> - indicates max possible message length, though the plain text message is not padded to that length
	#   46 hex (ascii F) - corresponds to 'S' (Short - 48 characters)
	#   47 hex (ascii G) - corresponds to both 'L' (Long - 1024 characters) and 'X' (Extra-long - 4096 characters)
	#   if you send COM port data with message body longer than that limit, the mobile will not transmit
	# <id>
	#   FleetSync: <fleet><dev> - plain-text three-digit fleet ID and four-digit device ID (0000000 for broadcast)
	#   NEXEDGE: U<uid> - U followed by five-digit unit ID
	# <msg> - plain-text message
	# UNUSED: <sequence> - plain-text two-digit decimal sequence identifier - increments with each send - probably not relevant
	#   NOTE: sequnce is generated by radtext, but, it shows up as part of the message body on the
	#          receiving device, which is probably not useful.  Interesting point that we could
	#          add timestamp or such to the message body if needed, but, this is not a separate token.
	# <end> - 03 hex (ascii heart)
	#
	# examples:
	# FleetSync:
	#  broadcast 'test' (short):  02 46 30 30 30 30 30 30 30 74 65 73 74 32 39 03   F0000000test28  (sequence=28)
	#  100:1002 'test' (short):  02 46 31 30 30 31 30 30 32 74 65 73 74 33 31 03   F1001002test31  (sequence=31)
	# NEXEDGE:
	#  03001 'test' (short):  02 67 46 55 30 33 30 30 31 74 65 73 74 31 31 03   gFU03001test10  (sequence=10)


	def sendText(self,fleetOrListOrAll,device=None,message=None):
		logging.info('sendText called: fleetOrListOrAll='+str(fleetOrListOrAll)+'  device='+str(device)+'  message='+str(message))
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
			logging.info('message:'+str(message))
			if broadcast:
				# portable radios will not attempt to send acknowledgement for broadcast
				logging.info('broadcasting text message to all devices')
				# - send fleetsync to all com ports, then nexedge to all com ports
				# - wait 2 seconds between each send - arbitrary amount of time to let
				#   the mobile radio(s) recover between transmissions
				d_fs='\x02F0000000'+timestamp+' '+message+'\x03' # fleetsync
				d_nx='\x02gFG00000'+timestamp+' '+message+'\x03' # nexedge
				stringList=[d_fs,d_nx]
				for d in stringList:
					logging.info('com data: '+str(d))
					suffix=' using one mobile radio'
					self.firstComPort.write(d.encode())
					if self.secondComPort:
						time.sleep(2) # yes, we do want a blocking sleep
						suffix=' using two mobile radios'
						self.secondComPort.write(d.encode())
					if d!=stringList[-1]:
						time.sleep(2)
				# values format for adding a new entry:
				#  [time,to_from,team,message,self.formattedLocString,status,self.sec,self.fleet,self.dev,self.origLocString]
				values=["" for n in range(10)]
				values[0]=time.strftime("%H%M")
				values[3]='TEXT MESSAGE SENT TO ALL DEVICES'+suffix+': "'+str(message)+'"'
				values[6]=time.time()
				self.newEntry(values)
				box=QMessageBox(QMessageBox.Information,'FleetSync & NEXEDGE Broadcast Sent',values[3]+'\n\nNo confirmation signal is expected.  This only indicates that instructions were sent from the computer to the mobile radio, and is not a guarantee that the message was actually transmitted.',
								QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
				box.show()
				box.raise_()
				box.exec_()
			else:
				# recipient portable will send acknowledgement when fleet and device ase specified
				for [fleetOrNone,device] in self.fsSendList:
					aborted=False
					# values format for adding a new entry:
					#  [time,to_from,team,message,self.formattedLocString,status,self.sec,self.fleet,self.dev,self.origLocString]
					values=["" for n in range(10)]
					if fleetOrNone: # fleetsync
						callsignText=self.getCallsign(fleetOrNone,device)
						logging.info('sending FleetSync text message to fleet='+str(fleetOrNone)+' device='+str(device)+' '+callsignText)
						d='\x02F'+str(fleetOrNone)+str(device)+timestamp+' '+message+'\x03'
					else: # NXDN
						callsignText=self.getCallsign(device,None)
						logging.info('sending NEXEDGE text message to device='+str(device)+' '+callsignText)
						d='\x02gFU'+str(device)+timestamp+' '+message+'\x03'
					values[2]=str(callsignText)
					if callsignText:
						callsignText='('+callsignText+')'
					else:
						callsignText='(no callsign)'
					logging.info('com data: '+str(d))
					fsFirstPortToTry=self.fsGetLatestComPort(fleetOrNone,device) or self.firstComPort
					if fsFirstPortToTry==self.firstComPort:
						self.fsSecondPortToTry=self.secondComPort # could be None; inst var so fsCheck can see it
					else:
						self.fsSecondPortToTry=self.firstComPort # could be None; inst var so fsCheck can see it
					self.fsThereWillBeAnotherTry=False
					if self.fsSecondPortToTry:
						self.fsThereWillBeAnotherTry=True
					# logging.info('1: fsThereWillBeAnotherTry='+str(self.fsThereWillBeAnotherTry))
					fsFirstPortToTry.write(d.encode())
					# if self.fsSendData(d,fsFirstPortToTry):
					self.fsAwaitingResponse=[fleetOrNone,device,'Text message sent',0,message]
					[f,dev,t]=self.fsAwaitingResponse[0:3]
					if f:
						h='FLEETSYNC'
						h2='FleetSync'
						sep=':'
					else:
						h='NEXEDGE'
						h2='NEXEDGE'
						sep=''
					self.fsAwaitingResponseMessageBox=QMessageBox(QMessageBox.NoIcon,h2+' '+t,h2+' '+t+' to '+str(f)+sep+str(dev)+' on preferred COM port; awaiting response for '+str(self.fsAwaitingResponseTimeout)+' more seconds...',
									QMessageBox.Abort,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
					self.fsAwaitingResponseMessageBox.show()
					self.fsAwaitingResponseMessageBox.raise_()
					self.fsAwaitingResponseMessageBox.exec_()
					# add a log entry when Abort is pressed
					if self.fsAwaitingResponse and not self.fsTimedOut:
						aborted=True
						values[0]=time.strftime("%H%M")
						values[1]='TO'
						values[3]=h+': Text message sent to '+str(f)+sep+str(dev)+' '+callsignText+' but radiolog operator clicked Abort before delivery could be confirmed: "'+str(message)+'"'
						values[6]=time.time()
						self.newEntry(values)
						self.fsResponseMessage+='\n\n'+str(f)+sep+str(dev)+' '+callsignText+': radiolog operator clicked Abort before delivery could be confirmed'
					if self.fsFailedFlag: # timed out, or, got a '1' response
						if self.fsSecondPortToTry:
							logging.info('failed on preferred COM port; sending on alternate COM port')
							self.fsTimedOut=False
							self.fsFailedFlag=False # clear the flag
							self.fsSecondPortToTry.write(d.encode())
							self.fsThereWillBeAnotherTry=False
							# logging.info('2: fsThereWillBeAnotherTry='+str(self.fsThereWillBeAnotherTry))
							self.fsAwaitingResponse[3]=0 # reset the timer
							self.fsAwaitingResponseMessageBox=QMessageBox(QMessageBox.NoIcon,t,t+' to '+str(f)+sep+str(dev)+' on alternate COM port; awaiting response up to '+str(self.fsAwaitingResponseTimeout)+' seconds...',
											QMessageBox.Abort,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
							self.fsAwaitingResponseMessageBox.show()
							self.fsAwaitingResponseMessageBox.raise_()
							self.fsAwaitingResponseMessageBox.exec_()
							# add a log entry when Abort is pressed
							if self.fsAwaitingResponse and not self.fsTimedOut:
								values[0]=time.strftime("%H%M")
								values[1]='TO'
								values[3]=h+': Text message sent to '+str(f)+sep+str(dev)+' '+callsignText+' but radiolog operator clicked Abort before delivery could be confirmed: "'+str(message)+'"'
								values[6]=time.time()
								self.newEntry(values)
								self.fsResponseMessage+='\n\n'+str(f)+sep+str(dev)+' '+callsignText+': radiolog operator clicked Abort before delivery could be confirmed'
							if self.fsFailedFlag: # timed out, or, got a '1' response
								logging.info('failed on alternate COM port: message delivery not confirmed')
							else:
								logging.info('apparently successful on alternate COM port')
								self.fsResponseMessage+='\n\n'+str(f)+sep+str(dev)+' '+callsignText+': delivery confirmed'
						else:
							logging.info('failed on preferred COM port; no alternate COM port available')
					elif not aborted:
						logging.info('apparently successful on preferred COM port')
						self.fsResponseMessage+='\n\n'+str(f)+sep+str(dev)+' '+callsignText+': delivery confirmed'
					self.fsAwaitingResponse=None # clear the flag - this will happen after the messagebox is closed (due to valid response, or timeout in fsCheck, or Abort clicked)
				if self.fsResponseMessage:
					box=QMessageBox(QMessageBox.Information,h2+' Response Summary',h2+' response summary:'+self.fsResponseMessage,
						QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
					box.open()
					box.raise_()
					box.exec_()


	# pollGPS - outgoing serial port data format:
	#
	# <start><poll_code><fleet><device><sequence><end>
	#
	# <start> - 02 hex (ascii smiley face)
	#   for NEXEDGE, insert 67 hex (lowecase g) after 02
	# <poll_code>
	#   52 33 hex (ascii R3)
	# <id>
	#   FleetSync: <fleet><dev> - plain-text three-digit fleet ID and four-digit device ID (0000000 for broadcast)
	#   NEXEDGE: U<uid> - U followed by five-digit unit ID
	# UNUSED - see sendText notes - <sequence> - plain-text two-digit decimal sequence identifier - increments with each send - probably not relevant
	# <end> - 03 hex (ascii heart)

	# examples:
	# FleetSync:
	#  poll 100:1001:  02 52 33 31 30 30 31 30 30 31 32 35 03   R3100100120  (sequence=20)
	#  poll 100:1002:  02 52 33 31 30 30 31 30 30 32 32 37 03   R3100100221  (sequence=21)
	# NEXEDGE:
	#  poll 03001:  02 67 52 33 55 30 33 30 30 31 30 36 03   gR3U0300108  (sequence=08) 


	
	def pollGPS(self,fleet='',device=None):
		if self.fsShowChannelWarning:
			m='WARNING: You are about to send FleetSync or NEXEDGE data burst noise on one or both mobile radios.\n\nMake sure that neither radio is set to any law or fire channel, or any other channel where FleetSync data bursts would cause problems.'
			box=QMessageBox(QMessageBox.Warning,'FleetSync / NEXEDGE Channel Warning',m,
							QMessageBox.Ok|QMessageBox.Cancel,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			box.show()
			box.raise_()
			box.exec_()
			if box.clickedButton().text()=='Cancel':
				return
		if fleet: # fleetsync
			logging.info('polling GPS for fleet='+str(fleet)+' device='+str(device))
			d='\x02\x52\x33'+str(fleet)+str(device)+'\x03'
		else: # nexedge
			logging.info('polling GPS for NEXEDGE unit ID = '+str(device))
			d='\x02g\x52\x33U'+str(device)+'\x03'
		logging.info('com data: '+str(d))
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
		# logging.info('3: fsThereWillBeAnotherTry='+str(self.fsThereWillBeAnotherTry))
		fsFirstPortToTry.write(d.encode())
		self.fsAwaitingResponse=[fleet,device,'Location request sent',0]
		[f,dev,t]=self.fsAwaitingResponse[0:3]
		if f: # fleetsync
			idStr=f+':'+dev
			h='FleetSync'
			callsignText=self.getCallsign(f,dev)
		else: # nexedge
			idStr=dev
			h='NEXEDGE'
			uid=dev
			callsignText=self.getCallsign(uid)
		self.fsAwaitingResponseMessageBox=QMessageBox(QMessageBox.NoIcon,t,t+' to '+idStr+' on preferred COM port; awaiting response up to '+str(self.fsAwaitingResponseTimeout)+' seconds...',
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
			values[2]=str(callsignText)
			if callsignText:
				callsignText='('+callsignText+')'
			else:
				callsignText='(no callsign)'
			values[3]=h+': GPS location request set to '+idStr+' '+callsignText+' but radiolog operator clicked Abort before response was received'
			values[6]=time.time()
			self.newEntry(values)
		if self.fsFailedFlag: # timed out, or, got a '1' response
			if self.fsSecondPortToTry:
				logging.info('failed on preferred COM port; sending on alternate COM port')
				self.fsTimedOut=False
				self.fsFailedFlag=False # clear the flag
				self.fsThereWillBeAnotherTry=False
				# logging.info('5: fsThereWillBeAnotherTry='+str(self.fsThereWillBeAnotherTry))
				self.fsSecondPortToTry.write(d.encode())
				self.fsAwaitingResponse[3]=0 # reset the timer
				self.fsAwaitingResponseMessageBox=QMessageBox(QMessageBox.NoIcon,t,t+' to '+idStr+' on alternate COM port; awaiting response up to '+str(self.fsAwaitingResponseTimeout)+' seconds...',
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
					values[2]=str(callsignText)
					if callsignText:
						callsignText='('+callsignText+')'
					else:
						callsignText='(no callsign)'
					values[3]=h+': GPS location request set to '+idStr+' '+callsignText+' but radiolog operator clicked Abort before response was received'
					values[6]=time.time()
					self.newEntry(values)
				if self.fsFailedFlag: # timed out, or, got a '1' response
					logging.info('failed on alternate COM port: message delivery not confirmed')
				else:
					logging.info('apparently successful on alternate COM port')
			else:
				logging.info('failed on preferred COM port; no alternate COM port available')
		else:
			logging.info('apparently successful on preferred COM port')
		self.fsAwaitingResponse=None # clear the flag - this will happen after the messagebox is closed (due to valid response, or timeout in fsCheck, or Abort clicked)

	def deleteTeamTab(self,teamName,ext=False):
		# optional arg 'ext' if called with extTeamName
		# must also modify related lists to keep everything in sync
		# logging.info('deleteTeamTab: teamName='+str(teamName)+'  ext='+str(ext))
		extTeamName=getExtTeamName(teamName)
		if ext:
			extTeamName=teamName
		# logging.info('t1: extTeamName='+str(extTeamName))
		niceTeamName=getNiceTeamName(extTeamName)
		# 406: apply the same fix as #393:
		# if the new entry's extTeamName is a case-insensitive match for an
		#   existing extTeamName, use that already-existing extTeamName instead
		for existingExtTeamName in self.extTeamNameList:
			if extTeamName.lower()==existingExtTeamName.lower():
				extTeamName=existingExtTeamName
				break
# 		self.extTeamNameList.sort()
		logging.info("deleting team tab: teamName="+str(teamName)+"  extTeamName="+str(extTeamName)+"  niceTeamName="+str(niceTeamName))
		logging.info("  teamNameList before deletion:"+str(self.teamNameList))
		logging.info("  extTeamNameList before deletion:"+str(self.extTeamNameList))
		if extTeamName in self.extTeamNameList: # pass through if trying to delete a tab that doesn't exist / has already been deleted
			i=self.extTeamNameList.index(extTeamName)
			logging.info("  i="+str(i))
			self.extTeamNameList.remove(extTeamName)
			if not teamName.lower().startswith("spacer"):
				self.teamNameList.remove(niceTeamName)
				#710 - don't delete teamTimersDict entry
				# del teamTimersDict[extTeamName]
				del teamCreatedTimeDict[extTeamName]
			del self.ui.tabList[i]
			del self.ui.tabGridLayoutList[i]
			del self.ui.tableViewList[i]
			self.ui.tabWidget.removeTab(i)
			try:
				del self.proxyModelList[i]
			except:
				logging.info("  ** sync error: proxyModelList current length = "+str(len(self.proxyModelList))+"; requested to delete index "+str(i)+"; continuing...")
			else:
				logging.info("  deleted proxyModelList index "+str(i))
			# free the hotkey, and reassign it to the first (if any) displayed callsign that has no hotkey
			hotkeyRDict={v:k for k,v in self.hotkeyDict.items()}
			if niceTeamName in hotkeyRDict:
				hotkey=hotkeyRDict[niceTeamName]
				logging.info("Freeing hotkey '"+hotkey+"' which was used for callsign '"+niceTeamName+"'")
				del self.hotkeyDict[hotkey]
				bar=self.ui.tabWidget.tabBar()
				taken=False
				for i in range(1,bar.count()):
					if not taken:
						callsign=bar.tabWhatsThis(i)
						logging.info("checking tab#"+str(i)+":"+callsign)
						if callsign not in hotkeyRDict and not callsign.lower().startswith("spacer"):
							logging.info("  does not have a hotkey; using the freed hotkey '"+hotkey+"'")
							self.hotkeyDict[hotkey]=callsign
							taken=True
		self.hiddenTeamTabsList.append(extTeamName)
		self.showTeamTabsMoreButtonIfNeeded()
		self.rebuildTeamHotkeys()
		# logging.info("  extTeamNameList after delete 1: "+str(self.extTeamNameList))
		# if there are two adjacent spacers, delete the second one
		for n in range(len(self.extTeamNameList)-1):
			if self.extTeamNameList[n].lower().startswith("spacer"):
				if self.extTeamNameList[n+1].lower().startswith("spacer"):
					if len(self.extTeamNameList)>2: # but not if there are no visible tabs
						logging.info("  found back-to-back spacers at indices "+str(n)+" and "+str(n+1))
						self.deleteTeamTab(self.extTeamNameList[n+1],True)
						# logging.info('    extTeamNameList on return from recursive deleteTeamTab call:'+str(self.extTeamNameList))
						break
		# 741 call rebuildGroupedTabDict to make sure spacer(s) are in appropriate spots after deleting a team
		# logging.info("  extTeamNameList after delete 2: "+str(self.extTeamNameList))
		# NOTE during #741 work: don't rebuild here - it can create two adjacent spacers which
		#  apparently induces the tracebacks by making extTeamNameList longer than the number
		#  of tabs in the tabbar, unless followed by rebuildTabs; should probably clean up
		#  rebuildGroupedTabDict to not generate two spacers back-to-back
		# self.rebuildGroupedTabDict()
		# logging.info("  extTeamNameList after delete and rebuild: "+str(self.extTeamNameList))
		# self.rebuildTabs()
		# #717 if all tabs are hidden, keep the same look as at startup
		# 741 - make this clause more robust than simply looking at list length
		# if len(self.extTeamNameList)==2:
		if len(self.extTeamNameList)==0 or all(['spacer' in x for x in self.extTeamNameList]):
			logging.info('all teams hidden; clearing tabWidget')
			self.ui.tabWidget.clear()
		#717 if rightmost tab was hidden, select the new rightmost visible tab if one exists
		i=self.ui.tabWidget.currentIndex()
		count=self.ui.tabWidget.count()
		if i==count-1 and count>2:
			logging.info('last tab was hidden; backselecting')
			self.ui.tabWidget.setCurrentIndex(i-1)
		#715 - redraw sidebar now, regardless of visibility
		# if self.sidebarIsVisible: #.isVisible would always return True - it's slid left when 'hidden'
		# 	self.sidebar.resizeEvent()
		self.sidebar.resizeEvent()
		# logging.info('end of deleteTeamTab: hiddenTeamTabsList='+str(self.hiddenTeamTabsList))

	def openTeamNotes(self,extTeamName):
		self.teamNotesDialog.show()
		self.teamNotesDialog.ui.teamField.setCurrentText(getNiceTeamName(extTeamName))

	def loadTeamNotes(self,fileName=None):
		logging.info('loadTeamNotes called')
		if not fileName:
			fileName=os.path.join(self.sessionDir,self.teamNotesFileName)
		try:
			with open(fileName,'r') as tnfile:
				logging.info('Loading team notes data from file '+fileName)
				self.teamNotesDict=json.load(tnfile)
				logging.info('  loaded these team notes:'+str(json.dumps(self.teamNotesDict,indent=3)))
		except:
			logging.info('WARNING: Could not read team notes data file '+fileName)
			logging.info('  isfile: '+str(os.path.isfile(fileName)))

	def saveTeamNotes(self):
		logging.info('saveTeamNotes called')
		# names=self.getOperatorNames()
		# if len(names)==0:
		# 	logging.info('  the operators list is empty; skipping the operator save operation')
		# 	return
		fileName=os.path.join(self.sessionDir,self.teamNotesFileName)
		try:
			with open(fileName,'w') as tnfile:
				logging.info('Saving team notes data file '+fileName)
				json.dump(self.teamNotesDict,tnfile,indent=3)
		except:
			logging.info('WARNING: Could not write team notes data file '+fileName)
			logging.info('  isfile: '+str(os.path.isfile(fileName)))

	def teamNotesBuildTooltip(self,extTeamName):
		logging.info('teamNotesBuildTooltip called for '+str(extTeamName))
		notes=self.teamNotesDict.get(extTeamName,None)
		if extTeamName in self.teamNotesDict.keys() and notes:
			niceTeamName=getNiceTeamName(extTeamName)
			logging.info('  building tooltip: '+str(notes))
			tt='<span style="font-size: 14pt;"><b>'+niceTeamName+' Notes:</b><br>'+notes.replace('\n','<br>')+'</span>'
			i=self.extTeamNameList.index(extTeamName)
			self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).setToolTip(tt)
			oneLineNotes=notes.replace('\n',' | ')
			while ' |  | ' in oneLineNotes:
				oneLineNotes=oneLineNotes.replace(' |  | ',' | ')
			oneLineNotes=oneLineNotes.strip(' |')
			self.ui.tabGridLayoutList[i].itemAtPosition(0,0).widget().setText('Notes for '+niceTeamName+': '+oneLineNotes)

	def getNextAvailHotkey(self):
		# iterate through hotkey pool until finding one that is not taken
		for hotkey in self.hotkeyPool:
			if hotkey not in self.hotkeyDict:
				return hotkey
		return None # no available hotkeys

	def rebuildTeamHotkeys(self):
		# delete all child widgets after the first spacer widget
		while self.ui.teamHotkeysHLayout.count()-1:
			child=self.ui.teamHotkeysHLayout.takeAt(1)
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
# 		logging.info("tab count="+str(bar.count()))
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
		self.sidebar.resizeEvent()

	def showTeamTabsMoreButtonIfNeeded(self):
		#595: setStyleSheet causes a second or two of lag when there are ~300 entries;
		#  instead, just toggle visibility of the leftmost spacer tab
		# if self.hiddenTeamTabsList:
		if True:
			if not self.ui.teamTabsMoreButton.isVisible() or not self.ui.tabWidget.tabBar().isTabVisible(0):
				self.ui.tabWidget.tabBar().setTabVisible(0,True)
				self.ui.teamTabsMoreButton.setVisible(True)
				bgColor=self.ui.frame.palette().color(QPalette.Background).name()
				self.ui.teamTabsMoreButton.setStyleSheet('border:0px;background:'+bgColor)
		else:
			if self.ui.teamTabsMoreButton.isVisible() or self.ui.tabWidget.tabBar().isTabVisible(0):
				self.ui.teamTabsMoreButton.setVisible(False)
				self.ui.tabWidget.tabBar().setTabVisible(0,False)

	def sidebarShowHide(self,e=None):
		self.checkForResize()
		# logging.info('sidebarShowHide: x='+str(self.sidebar.pos().x())+'  e='+str(e))
		hideEvent=False
		w=self.sidebar.width()
		if e and e.type()==11: # hide event
			hideEvent=True
		# logging.info(' hide event? '+str(hideEvent))
		self.sidebar.resize(w,self.sidebar.height())
		self.sidebarShownPos=QPoint(0,self.sidebar.y())
		self.sidebarHiddenPos=QPoint(-w,self.sidebar.y())
		# if self.sidebar2.pos().x()>-100:
		if self.sidebar.pos().x()>-100:
			self.sidebarAnimation.setEndValue(self.sidebarHiddenPos)
			self.sidebarIsVisible=False
		elif not hideEvent: # don't show if this is a hideEvent and it's already hidden, as happens on the first mouse move after clicking a cell
			self.sidebarAnimation.setEndValue(self.sidebarShownPos)
			self.sidebarIsVisible=True
		self.sidebarAnimation.start()

	def findDialogShowHide(self,e=None):
		# logging.info('sidebarShowHide: x='+str(self.sidebar.pos().x())+'  e='+str(e))
		# logging.info('sidebarShowHide: h='+str(self.findDialog.height())+'  e='+str(e))
		hideEvent=False
		# w=self.findDialog.width()
		if e and e.type()==11: # hide event
			hideEvent=True
		# logging.info(' hide event? '+str(hideEvent))
		# self.sidebar.resize(w,self.sidebar.height())
		
		# tvp=self.ui.tableView.pos()
		# tvp=self.ui.tableView.parentWidget().mapToGlobal(self.ui.tableView.pos())
		# tvp=self.ui.tableView.mapToGlobal(QPoint(0,0))
		# tvp=self.ui.tableView.mapToParent(self.ui.tableView.pos())
		tvp=self.ui.tableView.mapTo(self.ui.tableView.parentWidget().parentWidget(),self.ui.tableView.pos())
		tvw=self.ui.tableView.width()
		fpw=self.findDialog.width()
		# logging.info('tableView x='+str(tvp.x())+' y='+str(tvp.y())+' w='+str(tvw))
		self.findDialog.move(tvp.x()+tvw-fpw-7,tvp.y()-7)

		if self.findDialog.isVisible():
			logging.info('findDialog: setVisible false')
			self.findDialog.setVisible(False)
		elif not hideEvent:
			self.findDialog.setVisible(True)
			logging.info('findDialog: setVisible true')
			self.findDialog.ui.findField.setFocus()

		# animation attempts
		# self.findDialogShownPos=QPoint(self.findDialog.x(),200)
		# self.findDialogHiddenPos=QPoint(self.findDialog.x(),150)
		# self.findDialogShownGeom=QRect(200,250,300,50)
		# self.findDialogHiddenGeom=QRect(200,200,200,10)
		# # if self.sidebar2.pos().x()>-100:
		# if self.findDialog.pos().y()>210:
		# 	self.findDialogAnimation.setEndValue(self.findDialogHiddenGeom)
		# 	self.findDialogIsVisible=False
		# elif not hideEvent: # don't show if this is a hideEvent and it's already hidden, as happens on the first mouse move after clicking a cell
		# 	self.findDialogAnimation.setEndValue(self.findDialogShownGeom)
		# 	self.findDialogIsVisible=True
		# self.findDialogAnimation.start()

	def unhideTeamTab(self,niceTeamName):
		if not niceTeamName:
			return
		# Adding a new entry takes care of a lot of tasks; reproducing them without adding a
		#  new entry is cryptic and therefore error-prone.  Safer to just add a new entry.
		# values format for adding a new entry:
		#  [time,to_from,team,message,self.formattedLocString,status,self.sec,self.fleet,self.dev,self.origLocString]
		extTeamName=getExtTeamName(niceTeamName)
		values=["" for n in range(10)]
		values[0]=time.strftime("%H%M")
		values[6]=time.time()
		values[2]=niceTeamName
		values[3]='[RADIOLOG: operator is unhiding hidden team tab for "'+niceTeamName+'"]'
		if (extTeamName in teamStatusDict) and (teamStatusDict[extTeamName]!=''):
			values[5]=teamStatusDict[extTeamName]
		# remove from hiddenTeamTabsList right away, to prevent downstream errors in teamTabsPopup
		#  (this is already done at the start of addTab, which is too late)
		self.hiddenTeamTabsList=[x for x in self.hiddenTeamTabsList if extTeamName!=x]
		self.newEntry(values,unhiding=True)
		#715 - redraw sidebar now, regardless of visibility
		# if self.sidebarIsVisible: #.isVisible would always return True - it's slid left when 'hidden'
		# 	self.sidebar.resizeEvent()
		self.sidebar.resizeEvent()

	def addNonRadioClue(self):
		self.newNonRadioClueDialog=nonRadioClueDialog(self,time.strftime("%H%M"),str(self.getLastClueNumber()+1))
		self.newNonRadioClueDialog.show()

	def showInterviewPopup(self,parent):
		box=QMessageBox(QMessageBox.Warning,'Interview reminder','If this clue or message involves an interview, remind the field team to collect the interviewee\'s name and contact information.',
				QMessageBox.Ok,parent,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
		box.show()
		box.raise_()
		box.exec_()

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
		logging.info('Restoring previous session after unclean shutdown:')
		self.load(self.getSessions(fromCsvFile=fileToLoad)) # loads the radio log and the clue log
		self.loadTeamNotes(os.path.join(os.path.dirname(fileToLoad),self.teamNotesFileName))
		# hide warnings about missing fleetsync file, since it does not get saved until clean shutdown time
		# note, there is no need to load the default table first, since the defaults would exist
		#  in the session fleetsync csv file
		fsFileName=fileToLoad.replace('.csv','_fleetsync.csv')
		if not os.path.isfile(fsFileName): # this could be the case if the incident name was not changed before crash
			fsFileName=os.path.join(os.path.split(fsFileName)[0],'radiolog_fleetsync.csv')
		self.fsLoadLookup(fsFileName=fsFileName,hideWarnings=True)
		self.updateFileNames()
		self.fsSaveLookup()
		self.save()
		self.saveRcFile()

	def resizeEvent(self,e):
		self.findDialog.setVisible(False)
		
	def newEntryWindowHiddenPopupClicked(self,event):
		self.newEntryWindowHiddenPopup.close()
		self.newEntryWindow.raiseWindowAndChildren()
		for win in nonRadioClueDialog.instances:
			win.raise_()
			win.activateWindow()
			win.throb()

	def activationChange(self):
		if self.useNewEntryWindowHiddenPopup:
			QTimer.singleShot(500,self.activationChangeDelayed)

	def activationChangeDelayed(self):
		validActiveWindowClasses=[
							'newEntryWindow',
							'clueDialog',
							'subjectLocatedDialog',
							'nonRadioClueDialog',
							'QMessageBox', # e.g. cancel-clue-confirmation popup shouldn't trigger this popup
							'CustomMessageBox', # at open of 'looks like a clue' message box
							'optionsDialog',
							'helpWindow',
							'loginDialog',
		]
		awName='None'
		aw=QApplication.activeWindow()
		if aw:
			awName=str(aw.__class__.__name__)
		# logging.info('currently active window:'+awName+'  [previous:'+self.previousActiveWindowName+']')
		ok=awName in validActiveWindowClasses
		if not ok:
			# nonRadioClueDialog is spawned from MyWindow, rather than newEntryWindow,
			#  so don't raise the pending message popup after closure of nonRadioClueDialog
			if awName=='MyWindow' and self.previousActiveWindowName=='nonRadioClueDialog' and not self.nonRadioClueDialogIsOpen:
				# logging.info('  looks like nonRadioClueDialog was accepted')
				ok=True
		if ok:
			self.newEntryWindowHiddenPopup.close()
		else:
			# logging.info('  no valid window is active; showing newEntryWindowHiddenPopup')
			if (self.newEntryWindow.ui.tabWidget.count()>2 or self.nonRadioClueDialogIsOpen) and not self.newEntryWindowHiddenPopup.isVisible():
				self.newEntryWindowHiddenPopup.show()
				self.newEntryWindowHiddenPopup.raise_()
				# if main window was clicked, keep it active and ready for keypresses;
				#  but, if some other program is being used, don't steal focus
				if awName=='MyWindow':
					self.activateWindow()
		self.previousActiveWindowName=awName

	# changeActiveMessage - move up and down the message stack (Ctrl-up and Ctrl-down)
	#   called from top level customEventFilter, which passes target from a global variable
	def changeActiveMessage(target,dir):
		count=target.newEntryWindow.ui.tabWidget.count()
		current=target.newEntryWindow.ui.tabWidget.currentIndex()
		new=current
		if dir=='up' and current>1: # ctrl-up pressed: decrement the current index if possible
			new=current-1
		elif dir=='down' and current<(count-2): # ctrl-down pressed: increment current index if possible
			new=current+1
		target.newEntryWindow.ui.tabWidget.setCurrentIndex(new)

	# getLastClueNumber: parse from usedClueNames by default,
	#  or parse from a list of clue names passed as an argument if specified,
	#  which is the case when previewing a list of sessions
	def getLastClueNumber(self,theList=None):
		if not theList:
			theList=self.usedClueNames
		# get just the numeric parts of usedClueNames
		numbers=[]
		for name in theList:
			numericParts=re.findall(r'\d+',name)
			if numericParts:
				number=int(numericParts[0])
				numbers.append(number)
		numbers=list(dict.fromkeys(numbers)) # quickest way to remove duplicates while preserving sequence
		if numbers:
			m=max(numbers)
		else:
			m=0
		# logging.info(f'used clue numbers: {numbers}  max:{m}')
		return m
	
	# since the folder creation request is non-blocking, but this method returns a value immediately,
	#  it's likely that the return value will be None the first time this method is called
	def getOrCreateRadioMarkerFID(self):
		fid=self.radioMarkerFID
		if fid: # create folder if this is the first call (or if it has been deleted)
			return fid
		else:
			# logging.info('t1')
			radioFolders=self.cts.getFeatures(featureClass='Folder',title='Radios',allowMultiTitleMatch=True)
			# logging.info('t2')
			if radioFolders:
				fid=radioFolders[-1]['id'] # if there are multple folders, just pick one
				logging.info('Radios folder already exists: '+str(fid))
				self.radioMarkerFID=fid
				return fid
		if self.radioMarkerFolderHasBeenRequested:
			logging.info('No existing Radios folder found, but, one has already been requested, and should exist after reconnect; not requesting another one')
		else: # only request a folder if a map is already open (even if disconnected)
			if self.cts.mapID:
				logging.info('No existing Radios folder found, and none has yet been requested in this session; requesting one now...')
				self.cts.addFolder('Radios',visible=False,callbacks=[[self.setRadioMarkerFID,['.result.id']]])
				logging.info('back from non-blocking folder request')
				self.radioMarkerFolderHasBeenRequested=True
			else:
				logging.info('Radios folder not found and could not be requested because no map has been opened.')
		return None

	def setRadioMarkerFID(self,fid):
		logging.info('addFolder callback triggered: setting radio FID to '+str(fid))
		self.radioMarkerFID=fid
		self.radioMarkerEvent.set() # start _radioMarkerWorker to process any markers that were skipped because FID wasn't set yet

	def createCTS(self):
		# this method runs in the main thread
		# start the options dialog spinner (regardless of whether the dialog is open),
		#  and do the real work in createCTSThread
		self.optionsDialog.pyqtspinner.start()
		# QApplication.processEvents()
		# # if the operation takes more than 3 seconds, show the overlay label in the options dialog,
		# #  reminding the user that it's safe to close the options dialog
		# QTimer.singleShot(3000,lambda:
		# 			self.optionsDialog.caltopoUpdateOverlayLabel(
		# 				'<span style="font-size:24px;color:#44f;line-height:2">This is taking a while...<br></span><span style="font-size:16px;color:black;line-height:1.5">You can use or close the options dialog;<br>this operation will keep trying in the background<br>and the options dialog will pop up again when finished.</span>'))
		if self.caltopoLink>=0: # only show the blow taking a while overlay if connected
			self.optionsDialog.ctsOverlayTimer.start(3000)
		# self.optionsDialog.caltopoUpdateOverlayLabel('<span style="font-size:24px">Big Text<br></span><span style="font-size:16px">Small Text</span>')
		# QApplication.processEvents()
		self.createCTSThread.start()
		
	# def createCTS(self):
	# 	logging.info('createCTS called')
	# 	time.sleep(5) # pause to show backgrounding effects - hopefully a spinner
	# 	# open a mapless caltopo.com session first, to get the list of maps; if URL is
	# 	#  already specified before the first createCTS call, then openMap will
	# 	#  be called after the mapless session is openend
	# 	# logging.info('createCTS called:')
	# 	if self.cts is not None: # close out any previous session
	# 		# logging.info('Closing previous CaltopoSession')
	# 		# self.closeCTS()
	# 		logging.info('  cts is already open; returning')
	# 		return False
	# 		# self.ui.linkIndicator.setText("")
	# 		# self.updateLinkIndicator()
	# 		# self.link=-1
	# 		# self.updateFeatureList("Folder")
	# 		# self.updateFeatureList("Marker")
	# 	domainAndPort='caltopo.com'
	# 	if self.optionsDialog.ui.caltopoDesktopButton.isChecked():
	# 		domainAndPort=self.optionsDialog.ui.ctdServerComboBox.currentText()
	# 	logging.info('  creating mapless online session for user '+self.caltopoAccountName+' on server '+domainAndPort)
	# 	self.cts=CaltopoSession(domainAndPort=domainAndPort,
	# 							configpath=os.path.join(self.configDir,'cts.ini'),
	# 							account=self.caltopoAccountName,
	# 							syncInterval=10,syncTimeout=20, # reduce log file size and overzealous disconnects
	# 							deletedFeatureCallback=self.caltopoDeletedFeatureCallback,
	# 							disconnectedCallback=self.caltopoDisconnectedCallback,
	# 							reconnectedCallback=self.caltopoReconnectedCallback,
	# 							mapClosedCallback=self.caltopoMapClosedCallback)
	# 	logging.info('  back from CaltopoSession init')
	# 	noMatchDict={
	# 		'groupAccountTitle':'<Choose Acct>',
	# 		'mapList':[{
	# 			'id':'Top',
	# 			'title':'<Choose Map>',
	# 			'updated':0,
	# 			'type':'map',
	# 			'folderId':0,
	# 			'folderName':'<Top Level>'}]}
	# 	# try:
	# 	# 	aml=self.cts.getAllMapLists()
	# 	# except Exception as e:
	# 	# 	logging.info('exception from getAllMapLists: '+str(e))
	# 	# 	if 'Failed to resolve' in str(e):
	# 	# 		logging.info('  failed to resolve')
	# 	# 		self.caltopoDisconnectedCallback()
	# 	# 		self.cts._sendRequest('get','[PING]',j=None,callbacks=[[self.caltopoReconnectedFromCreateCTS]])
	# 	# 	return False
	# 	aml=self.cts.getAllMapLists()
	# 	if not aml or not self.cts.accountData:
	# 		logging.info('Account data is empty; disconnected')
	# 		# self._sig_caltopoDisconnectedFromCreateCTS.emit()
	# 		# box=QMessageBox(QMessageBox.Warning,"Disconnected","You have no connection to the CalTopo server.\n\nYou can close the Options dialog and continue to use RadioLog as normal.\n\nThe Options dialog will pop up again when connection is re-established.",
	# 		# 	QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
	# 		# box.show()
	# 		# box.raise_()
	# 		# self.caltopoDisconnectedCallback()
	# 		# self.cts._sendRequest('get','[PING]',j=None,callbacks=[[self.caltopoReconnectedFromCreateCTS]])
	# 		return False
	# 	self.caltopoMapListDicts=[noMatchDict]+aml
	# 	# logging.info('caltopoMapListDicts:')
	# 	# logging.info(json.dumps(self.caltopoMapListDicts,indent=3))
	# 	self.caltopoLink=1
	# 	# self.accountDataChanged.emit()
	# 	# self.linkChanged.emit() # mapless
	# 	# self.finished.emit()
	# 	logging.info('  end of createCTS')
	# 	return True
	
	def createCTSCB(self,result):
		# this method runs in the main thread
		logging.info(f'createCTSCB called with result={result}')
		self.caltopoUpdateLinkIndicator()
		self.optionsDialog.ctsOverlayTimer.stop()
		if result: # success
			self.optionsDialog.pyqtspinner.stop()
			self.optionsDialog.caltopoUpdateOverlayLabel(None)
			self.optionsDialog.caltopoRedrawAccountData()
			self.optionsDialog.caltopoUpdateGUI()
			self.optionsDialog.show() # in case it was closed by the operator while spinning
		else: # failure - loss of connection during createCTS
			# box=QMessageBox(QMessageBox.Warning,"Disconnected","You have no connection to the CalTopo server.\n\nYou can close the Options dialog and continue to use RadioLog as normal.\n\nThe Options dialog will pop up again when connection is re-established.",
			# 	QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			# box.show()
			# box.raise_()
			self.optionsDialog.pyqtspinner.start()
			# immediately show the overlay label in the options dialog, reminding the user that it's safe to close the options dialog
			self.optionsDialog.caltopoUpdateOverlayLabel(
				'<span style="font-size:24px;color:#f44;line-height:2">No connection to CalTopo server...<br></span><span style="font-size:16px;color:black;line-height:1.5">You can use or close the options dialog;<br>this operation will keep trying in the background;<br>the options dialog will pop up again when connected.</span>')
			self.caltopoDisconnectedCallback()
			self.cts._sendRequest('get','[PING]',j=None,callbacks=[[self.caltopoReconnectedFromCreateCTS]])
		# QCoreApplication.processEvents()

	# # def _createCTSWorker(self):
	# # 	# runs in createCTSThread, in case it takes a while;
	# # 	#  called from optiosnDialog.caltopoEnabledCB
	# # 	# 1. createCTS
	# # 	# 2. set an event indicating the mapless session has been opened
	# # 	self._sig_caltopoCreateCTSCB.emit(self.createCTS())

	# # def caltopoCreateCTSCB_mainThread(self,result):
	# # 	logging.info('caltopoCreateCTSCB_mainThread called')
	# # 	self.optionsDialog.pyqtspinner.stop()
	# # 	if not result:
	# # 		box=QMessageBox(QMessageBox.Warning,"Disconnected","You have no connection to the CalTopo server.\n\nYou can close the Options dialog and continue to use RadioLog as normal.\n\nThe Options dialog will pop up again when connection is re-established.",
	# # 			QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
	# # 		box.show()
	# # 		box.raise_()
	# # 		self.caltopoDisconnectedCallback()
	# # 		self.cts._sendRequest('get','[PING]',j=None,callbacks=[[self.caltopoReconnectedFromCreateCTS]])
		
	def caltopoReconnectedFromCreateCTS(self):
		# called as a _sendRequest callback from the PING request
		# THREAD WARNING: this function is probably not running in the main thread, since it's a callback in _sendRequest;
		#  don't do any GUI calls here
		# logging.info('back to life from createCTS')
		self._sig_caltopoReconnectedFromCreateCTS.emit()
		# logging.info('btl c0')

	def caltopoReconnectedFromCreateCTS_mainThread(self):
		# logging.info('btl c1')
		self.closeCTS()
		# if Caltopo Integration is still checked (even if the dialog has been closed),
		#  we know the user wants to use Caltopo Integration.  So, don't ask, just open the dialog and a mapless session.
		if self.optionsDialog.ui.caltopoGroupBox.isChecked():
			# logging.info('btl c2')
			self.optionsDialog.show()
			self.optionsDialog.raise_()
			self.caltopoUpdateLinkIndicator()
			self.optionsDialog.caltopoEnabledCB()
			self.optionsDialog.caltopoUpdateOverlayLabel(
				'<span style="font-size:24px;color:#0a0;line-height:2">Connection Established;<br>Getting Account Info...<br></span><span style="font-size:16px;color:black;line-height:1.5">You can use or close the options dialog;<br>this operation will keep trying in the background;<br>the options dialog will pop up again when finished.</span>')
			# QCoreApplication.processEvents()
			self.createCTS()
			# box=QMessageBox(QMessageBox.Information,"Reconnected","Connection to CalTopo server is re-established.\n\nYou can open a map now if needed.",
			# 	QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			# box.show()
			# box.raise_()
			# QCoreApplication.processEvents()
			# QTimer.singleShot(2000,self.optionsDialog.lambda:caltopoUpdateOverlayLabel(None))
		# if Caltopo Integration has been unckecked (regardless of whether the dialog is still open),
		#  we aren't sure if the user wants to use it - so ask them.  If yes, then do as above.
		else:
			# logging.info('btl c3')
			box=QMessageBox(QMessageBox.Question,"Reconnected","Connection to CalTopo server is re-established.\n\nDo you still want to use CalTopo Integration?",
				QMessageBox.Yes|QMessageBox.No,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			box.show()
			box.raise_()
			if box.exec_()==QMessageBox.Yes:
				self.optionsDialog.ui.caltopoGroupBox.setChecked(True)
				self.caltopoReconnectedFromCreateCTS_mainThread()

	def openMap(self):
		# this method runs in the main thread
		# start the options dialog spinner (regardless of whether the dialog is open),
		#  and do the real work in openMapThread
		# clear existing radio marker IDs, to avoid attempts to edit markers whose IDs only exist in a previously open map;
		#  this also means that all devices will generate markers on the newly opened map, which is good
		#  NOTE: this could result in duplicate markers in the newly opened map; would be fixed by reading existing markers
		#   after the first sync to populate caltopoId and lastId
		for d in self.radioMarkerDict.values():
			d['caltopoId']=None
			d['lastId']=None
		# clear the radios folder variables, to avoid unnamed folder if one map is closed then another is open
		self.radioMarkerFID=None
		self.radioMarkerFolderHasBeenRequested=False
		self.optionsDialog.pyqtspinner.start()
		# QApplication.processEvents()
		# time.sleep(5)
		# if the operation takes more than 3 seconds, show the overlay label in the options dialog,
		#  reminding the user that it's safe to close the options dialog
		# QTimer.singleShot(3000,lambda:
		# 			self.optionsDialog.caltopoUpdateOverlayLabel(
		# 				'<span style="font-size:24px;color:#44f;line-height:2">This is taking a while...<br></span><span style="font-size:16px;color:black;line-height:1.5">You can use or close the options dialog;<br>this operation will keep trying in the background;<br>the link indicator will turn bright green when finished.</span>'))
		self.optionsDialog.openingOverlayTimer.start(3000)
		self.openMapThread.start()
	
	def openMapCB(self,result):
		# this method runs in the main thread
		logging.info(f'openMapCB called with result={result}')
		self.optionsDialog.openingOverlayTimer.stop()
		if result: # success
			self.caltopoLink=2 # map opened and connected
			self.caltopoOpenMapIsWritable=not self.optionsDialog.caltopoSelectionIsReadOnly
			self.caltopoUpdateLinkIndicator()
			# self.ui.caltopoOpenMapButton.setText('Map Opened - Click to Close Map')
			# self.caltopoGroupFieldsSetEnabled(False) # disallow map field changes while connected
			# self.ui.caltopoOpenMapButton.setEnabled(True)
			# QCoreApplication.processEvents()
			# self.parent.getOrCreateRadioMarkerFID() # call it now so that hopefully the folder exists before the first radio marker
			# self.parent.caltopoProcessLatestMarkers() # add markers for any calls that were made before the map was opened
			if self.caltopoOpenMapIsWritable:
				self.radioMarkerEvent.set() # start _radioMarkerWorker to process any markers sent prior to map opening
			self.optionsDialog.caltopoUpdateGUI()
			self.optionsDialog.caltopoUpdateOverlayLabel(None)
			self.optionsDialog.pyqtspinner.stop()
			if self.optionsDialog.ui.caltopoWebBrowserCheckBox.isChecked():
				try:
					logging.info('Opening map in web browser...')
					webbrowser.open(f'https://{self.cts.domainAndPort}/m/{self.optionsDialog.ui.caltopoMapIDField.text()}')
				except Exception as e:
					logging.info('Failed to open map in web browser: '+str(e))
		# else: # failure - loss of connection during openMap
		# 	self.caltopoLink=1
		# 	logging.info('ERROR: could not open map '+str(self.optionsDialog.ui.caltopoMapIDField.text()))
		else: # failure - loss of connection during openMap
			self.caltopoLink=1
			self.cts.closeMap() # close now, to stop sync attempts etc, since reconnect will trigger openMap
			logging.info('ERROR: could not open map '+str(self.optionsDialog.ui.caltopoMapIDField.text()))
			self.optionsDialog.pyqtspinner.start()
			# immediately show the overlay label in the options dialog, reminding the user that it's safe to close the options dialog
			self.optionsDialog.caltopoUpdateOverlayLabel(
				'<span style="font-size:24px;color:#f44;line-height:2">No connection to CalTopo server...<br></span><span style="font-size:16px;color:black;line-height:1.5">You can use or close the options dialog;<br>this operation will keep trying in the background<br>the link indicator will turn bright green when finished.</span>')
			self.caltopoDisconnectedCallback()
			self.cts._sendRequest('get','[PING]',j=None,callbacks=[[self.caltopoReconnectedFromOpenMap]])
		
	def caltopoReconnectedFromOpenMap(self):
		# called as a _sendRequest callback from the PING request
		# THREAD WARNING: this function is probably not running in the main thread, since it's a callback in _sendRequest;
		#  don't do any GUI calls here
		self._sig_caltopoReconnectedFromOpenMap.emit()

	def caltopoReconnectedFromOpenMap_mainThread(self):
		self.openMap()

	def closeCTS(self):
		logging.info('closeCTS called')
		if self.cts:
			self.cts.closeMap()
			# logging.info(' closeCTS t1')
			# self.cts._stop() # end sync before deleting the object
			# logging.info(' closeCTS t2')
			# self.cts.mapData.clear() # remove all cache elements to free memory
			del self.cts
			# logging.info(' closeCTS t3')
			self.cts=None
		self.caltopoLink=0
		logging.info(' closeCTS t4')
		self.caltopoUpdateLinkIndicator()
		logging.info(' closeCTS t5')

	def caltopoDeletedFeatureCallback(self,id,c):
		# logging.info('deleted callback: id='+str(id)+'  c='+str(c))
		if id==self.radioMarkerFID:
			logging.info("Caltopo 'Radios' folder was deleted; it will be recreated on the next radio marker call.")
			# these two lines in conjuction will force re-creation on the next marker call
			self.radioMarkerFID=None
			self.radioMarkerFolderHasBeenRequested=False
		# if a radio marker was deleted, force its recreation on the next incoming call from >any< device
		#  (its timestamp is preserved since sendRadioMarker is only called by incoming radio calls)
		matchingRadioMarkerDeviceStr=next(iter([deviceStr for deviceStr in self.radioMarkerDict.keys() if self.radioMarkerDict[deviceStr]['caltopoId']==id]),None) # None if there are no matches
		if matchingRadioMarkerDeviceStr:
			self.radioMarkerDict[matchingRadioMarkerDeviceStr]['caltopoId']=None
			self.radioMarkerDict[matchingRadioMarkerDeviceStr]['lastId']=None

	def caltopoDisconnectedCallback(self):
		# called from caltopo_python when unexpectedly disconnected
		#  (not called when disconneted due to user action in the options GUI)
		# THREAD WARNING: don't do GUI actions in this function,
		#  since it could be called from a different thread in caltopo_python;
		#  use thread-safe inter-thread pyqtSignal instead
		self.caltopoLinkPrev=self.caltopoLink
		self.caltopoLink=-1
		self._sig_caltopoDisconnected.emit()
		
	def caltopoDisconnectedCallback_mainThread(self):
		# self.caltopoOpenMapButtonPrevText=self.optionsDialog.ui.caltopoOpenMapButton.text()
		# self.optionsDialog.ui.caltopoOpenMapButton.setText('Offline; attempting to reconnect...')
		# self.caltopoGroupFieldsPrevEnabled=self.optionsDialog.ui.caltopoOpenMapButton.isEnabled()
		self.optionsDialog.caltopoUpdateGUI()
		self.caltopoUpdateLinkIndicator()

	def caltopoReconnectedCallback(self):
		# called from caltopo_python when automatically reconnected after unexpected disconnect
		#  (not called when conneted due to user action in the options GUI)
		# THREAD WARNING: don't do GUI actions in this function,
		#  since it could be called from a different thread in caltopo_python;
		#  use thread-safe inter-thread pyqtSignal instead
		self.caltopoLink=self.caltopoLinkPrev
		self._sig_caltopoReconnected.emit()

	def caltopoReconnectedCallback_mainThread(self):
		# self.optionsDialog.ui.caltopoOpenMapButton.setText(self.caltopoOpenMapButtonPrevText)
		# self.optionsDialog.caltopoGroupFieldsSetEnabled(self.caltopoGroupFieldsPrevEnabled)
		self.optionsDialog.caltopoUpdateGUI()
		self.caltopoUpdateLinkIndicator()
		# start _radioMarkerWorker to process any markers sent to an open map while disconnected
		#  (but this callback could be called before a map is open, in which case no markers will be sent)
		self.radioMarkerEvent.set()

	def caltopoMapClosedCallback(self,badResponse):
		# THREAD WARNING - this is probably called from a different thread; don't try and GUI actions here
		self.caltopoBadResponse=badResponse
		self._sig_caltopoMapClosed.emit()

	def caltopoMapClosedCallback_mainThread(self):
		if self.caltopoBadResponse:
			box=QMessageBox(QMessageBox.Warning,"Map closed","The map or bookmark you opened has been closed due to a bad sync response:"+str(self.caltopoBadResponse),
				QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			box.show()
			box.raise_()
			box.exec_()
			self.optionsDialog.caltopoOpenMapButtonClicked()
			self.optionsDialog.show()
			self.optionsDialog.raise_()

	# def caltopoProcessLatestMarkers(self):
	# 	# this is only called after a map is opened;
	# 	# walk through deviceStrs in radioMarkerDict;
	# 	# for each one, add a radio marker for the latest coords and time string;
	# 	# could call this from the openMap callback, after the cache has been
	# 	#  populated, to see if any of those markers (matching deviceStr/time/coords)
	# 	#  already exist, i.e. if the map was manually disconnected then reconnected;
	# 	# probably best to run this in a separate thread in case it takes several seconds
	# 	for (deviceStr,d) in self.radioMarkerDict.items():
	# 		logging.info('processing latest radio marker for '+str(deviceStr))
	# 		logging.info(json.dumps(d,indent=3))
	# 		fleet=None
	# 		dev=None
	# 		uid=None
	# 		callsign=None # because we will specify the exact label instead
	# 		if ':' in deviceStr:
	# 			(fleet,dev)=map(int,deviceStr.split(':'))
	# 		else:
	# 			uid=int(deviceStr)
	# 		self.sendRadioMarker(fleet,dev,uid,callsign,
	# 					lat=d['lat'],
	# 					lon=d['lon'],
	# 					timeStr=d['latestTimeString'],
	# 					label=d['label'])

	def caltopoUpdateLinkIndicator(self):
		# -1 = unexpectedly disconnected
		# 0 = not connected
		# 1 = connected, mapless session
		# 2 = map opened and connected
		link=self.caltopoLink
		logging.info('caltopoUpdateLinkIndicator called: caltopoLink='+str(link))
		ss=''
		t=''
		if link==2: # map opened and connected
			if self.caltopoOpenMapIsWritable:
				ss='background-color:'+caltopoColors['openedWritable']+';color:black;font-weight:normal' # bright green
			else:
				ss='background-color:'+caltopoColors['openedReadOnly']+';color:black;font-weight:normal;text-decoration:line-through' # orange
			t=str(self.cts.mapID)
		elif link==1: # connected to a mapless session
			ss='background-color:'+caltopoColors['mapless']+';color:#333333;font-weight:normal' # faint green
			t='NO MAP'
		elif link==0: # not connected to any caltopo session
			ss='background-color:'+caltopoColors['disabled']+';font-weight:normal' # light gray
			t=''
		elif link==-1: # error condition
			ss='background-color:'+caltopoColors['disconnected']+';color:white;font-weight:bold' # bright red
			t='OFFLINE'
		self.optionsDialog.ui.caltopoLinkIndicator.setStyleSheet(ss)
		self.ui.caltopoLinkIndicator.setStyleSheet(ss)
		self.ui.caltopoLinkIndicator.setText(t)


class helpWindow(QDialog,Ui_Help):
	def __init__(self, *args):
		QDialog.__init__(self)
		self.ui=Ui_Help()
		self.ui.setupUi(self)
		self.setStyleSheet(globalStyleSheet)
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		self.setFixedSize(self.size())
		self.ui.caltopoDisabledLabel.setStyleSheet('QLabel { background-color: '+caltopoColors['disabled']+'; }')
		self.ui.caltopoMaplessLabel.setStyleSheet('QLabel { background-color: '+caltopoColors['mapless']+'; }')
		self.ui.caltopoOpenedWritableLabel.setStyleSheet('QLabel { background-color: '+caltopoColors['openedWritable']+'; }')
		self.ui.caltopoOpenedReadOnlyLabel.setStyleSheet('QLabel { background-color: '+caltopoColors['openedReadOnly']+'; }')
		self.ui.caltopoDisconnectedLabel.setStyleSheet('QLabel { background-color: '+caltopoColors['disconnected']+'; }')

	def toggleShow(self):
		if self.isVisible():
			self.close()
		else:
			self.show()
			self.raise_()


class teamTabsPopup(QWidget,Ui_teamTabsPopup):
	def __init__(self,parent):
		# the second argument to QWidget.__init__ makes this widget a child of the main window;
		#  without that argument, this widget would get its own top level window
		QWidget.__init__(self,parent)
		self.parent=parent
		self.ui=Ui_teamTabsPopup()
		self.ui.setupUi(self)
		self.ui.teamTabsSummaryTableWidget.verticalHeader().setFixedWidth(100)
		# hardcode the summary table height to be the sum of row heights, plus arbitrary pixel count to account for borders
		self.ui.teamTabsSummaryTableWidget.verticalHeader().setSectionResizeMode(QHeaderView.Fixed)
		self.ttsHeight=\
				sum([self.ui.teamTabsSummaryTableWidget.verticalHeader().sectionSize(n)\
	 			for n in range(self.ui.teamTabsSummaryTableWidget.rowCount())])+2
		self.ui.teamTabsSummaryTableWidget.setFixedHeight(self.ttsHeight)
		self.tttRowHeight=self.ui.teamTabsTableWidget.verticalHeader().defaultSectionSize() # assuming all rows are the same height
		self.ui.teamTabsTableWidget.cellClicked.connect(self.cellClicked)
		# disable mouse wheel scroll: https://stackoverflow.com/a/61085704/3577105
		self.ui.teamTabsTableWidget.wheelEvent=lambda event: None
		self.initialWidth=self.width()
		self.initialHeight=self.height()
		self.teamsRowCount=0
		self.teamsColumnCount=0

	def cellClicked(self,row,col):
		ci=self.ui.teamTabsTableWidget.currentItem()
		self.ui.teamTabsTableWidget.clearSelection() # get rid of fixed gray background, to allow already-set status color to keep showing
		if ci:
			ntn=self.ui.teamTabsTableWidget.currentItem().text()
			# remove any leading team hotkey text (character+colon+space)
			if ntn[1]==':' and len(ntn)>3:
				ntn=ntn[3:]
			etn=getExtTeamName(ntn)
			# logging.info('cell clicked: '+str(ntn)+'  extTeamName='+str(etn))
			# logging.info('extTeamNameList: '+str(self.parent.extTeamNameList))
			try:
				i=self.parent.extTeamNameList.index(etn)
				# logging.info('  i='+str(i))
				self.parent.ui.tabWidget.setCurrentIndex(i)
				# self.hide() # after self.hide, the popup doesn't show again on hover
				self.parent.sidebarShowHide() # sidebarShowHide does a proper hide, but then any mouse movement shows it again - must be leaveEvent even though it's been moved away
			except: # this will get called if the team tab is hidden
				try:
					# logging.info('searching hiddenTeamTabsList:'+str(self.parent.hiddenTeamTabsList))
					ntn=ntn.replace('[','').replace(']','') # might be wrapped in square brackets
					etn=getExtTeamName(ntn)
					i=self.parent.hiddenTeamTabsList.index(etn)
					box=QMessageBox(QMessageBox.Warning,"Hidden tab","The tab for '"+ntn+"' is currently hidden.\n\nDo you want to unhide the tab?",
						QMessageBox.Yes|QMessageBox.No,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
					box.show()
					box.raise_()
					if box.exec_()==QMessageBox.No:
						return
					self.parent.unhideTeamTab(ntn)
					i=self.parent.extTeamNameList.index(etn)
					self.parent.ui.tabWidget.setCurrentIndex(i)
					# self.hide()
				except: # not in either list
					logging.info('ERROR: clicked a cell '+etn+' that does not exist in extTeamNameList or hiddenTeamTabsList')

	def showEvent(self,e=None):
		# logging.info('sidebar showEvent called')
		self.redraw()

	def resizeEvent(self,e=None):
		# logging.info('sidebar resizeEvent called')
		self.redraw()

	def redraw(self):
		# logging.info('redrawing sidebar')
		# 1. calculate and set number of rows and columns required for team table
		# 2. populate team table - done before determining total width, due to resizeColumnsToContents
		# 3. populate summary table
		# 4. set sidebar fixed size based on team table size (and fixed summary table size)
		# 5. move sidebar to correct vertical position

		# 1. calculate and set number of rows and columns required for team table

		theList=self.parent.allTeamsList # same as teamNameList but hidden tabs are still included
		theList=[x for x in theList if 'dummy' not in x and 'spacer' not in x.lower()]
		listCount=len(theList)
		maxSidebarHeight=self.parent.height()
		maxTeamTableHeight=maxSidebarHeight-self.ui.teamTabsSummaryTableWidget.height()-15 # arbirary for padding etc
		maxRowCount=int(maxTeamTableHeight/self.tttRowHeight)
		self.teamsRowCount=min(listCount,maxRowCount)
		self.teamsColumnCount=int((listCount+maxRowCount-1)/maxRowCount) # do the math - this works
		# logging.info(' listCount='+str(listCount)+' maxRowCount='+str(maxRowCount)+' : setting rows='+str(rowCount)+' cols='+str(colCount))
		self.ui.teamTabsTableWidget.setRowCount(self.teamsRowCount)
		self.ui.teamTabsTableWidget.setColumnCount(self.teamsColumnCount)
		if not self.parent.sidebarIsVisible:
			self.move(-self.width(),self.y())

		# 2. populate team table - done before determining total width, due to resizeColumnsToContents

		self.ui.teamTabsTableWidget.clear()
		hotkeyRDict={v:k for k,v in self.parent.hotkeyDict.items()}
		showTeamHotkeys=self.parent.ui.teamHotkeysWidget.isVisible()
		for i in range(listCount):
			col=int(i/self.teamsRowCount)
			row=i-(col*self.teamsRowCount)
			t=theList[i]
			etn=getExtTeamName(t)
			hotkey=hotkeyRDict.get(t,"")
			# status=teamStatusDict.get(etn,None)
			# if status is not None: # could be empty string
			# self.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide).setStyleSheet(statusStyleDict[status])
			twi=QTableWidgetItem(t)
			twi.setWhatsThis(etn) # for use by setTeamTableColors
			hidden=False
			# modifications for hidden tabs:
			#  - always italic
			#  - light gray text if/when background is white; black text otherwise
			#  - always wrap in square brackets []
			#  - use bgHidden for background color, if specificed
			if etn in self.parent.hiddenTeamTabsList:
				hidden=True
				twi.setText('['+t+']')
			if showTeamHotkeys and hotkey:
				twi.setText(hotkey+': '+twi.text())
			if hidden:
				f=twi.font()
				f.setItalic(True)
				twi.setFont(f)
			# logging.info('i='+str(i)+'  row='+str(row)+'  col='+str(col)+'  text='+str(theList[i]))
			self.ui.teamTabsTableWidget.setItem(row,col,twi)
		self.setTeamTableColors() #715 - handle colors and blinking in a separate function

		# 3. populate summary table

		tsdValuesList=list(teamStatusDict.values())
		statusTableDict={}
		# 'other' status could include any status not specifically listed, or no status; mainly shown to
		#   reduce confusion that would arise when 'Total' is greater than the sum of the listed statuses
		# statusList=['At IC','In Transit','Working',['Waiting for Transport','Await.Trans.'],'STANDBY']
		statusList=['At IC','In Transit','Working']
		for status in statusList:
			statusTableDict[status]=tsdValuesList.count(status)
		otherCount=len([x for x in tsdValuesList if x not in statusList])
		for row in range(self.ui.teamTabsSummaryTableWidget.rowCount()):
			rowLabel=self.ui.teamTabsSummaryTableWidget.verticalHeaderItem(row).text()
			if rowLabel in statusList:
				self.ui.teamTabsSummaryTableWidget.setItem(row-1,1,QTableWidgetItem(str(statusTableDict[rowLabel])))
			elif rowLabel=='Other':
				otherItem=QTableWidgetItem(str(otherCount))
				otherItem.setForeground(QColor(100,100,100))
				self.ui.teamTabsSummaryTableWidget.setItem(row-1,1,otherItem)
			elif rowLabel=='Total':
				totalItem=QTableWidgetItem(str(len(tsdValuesList)))
				f=totalItem.font()
				f.setBold(True)
				totalItem.setFont(f)
				self.ui.teamTabsSummaryTableWidget.setItem(row-1,1,totalItem)
			elif rowLabel=='Not At IC':
				notAtICCount=len([key for key,val in teamStatusDict.items() if val!='At IC'])
				notAtICItem=QTableWidgetItem(str(notAtICCount))
				f=notAtICItem.font()
				f.setPointSize(12)
				f.setBold(True)
				notAtICItem.setFont(f)
				self.ui.teamTabsSummaryTableWidget.setItem(row-1,1,notAtICItem)

		# 4. set sidebar fixed size based on team table size (and fixed summary table size)

		self.ui.teamTabsTableWidget.resizeColumnsToContents()
		teamTabsTableRequiredWidth=4 # initial size = borders
		for n in range(self.teamsColumnCount):
			teamTabsTableRequiredWidth+=self.ui.teamTabsTableWidget.columnWidth(n)+4
		newWidth=max(self.initialWidth,teamTabsTableRequiredWidth)
		newHeight=max(self.initialHeight,self.teamsRowCount*self.tttRowHeight+self.ttsHeight+18)
		self.setFixedSize(newWidth,newHeight)

		# 5. move sidebar to correct vertical position

		dotsPos=self.parent.ui.teamTabsMoreButton.pos()
		dotsY=self.parent.ui.teamTabsMoreButton.mapTo(self.parent,dotsPos).y()
		y=int(dotsY-(newHeight/2)) # start with vertically centering on the 3 dots
		if y+newHeight>maxSidebarHeight: # running off the bottom - move upwards as needed
			y=maxSidebarHeight-newHeight
		if y<0: # running off the top
			if y+newHeight<maxSidebarHeight: # there's space to move downwards
				y=0
		self.move(self.x(),y)

	def setTeamTableColors(self):
		# Walk through all cells; extTeamName for that cell is stored in the QTableWidgetItem.whatsThis.
		# Use that to get the status and the age, and use those to determine the color based on blinkToggle.
		for col in range(self.teamsColumnCount):
			for row in range(self.teamsRowCount):
				# logging.info('blink: col='+str(col)+' row='+str(row))
				twi=self.ui.teamTabsTableWidget.item(row,col)
				if twi: # None for empty cells
		# logging.info('teamTabsPopup.blink')
		# self.ui.teamTabsTableWidget.selectAll()
		# logging.info('  selected:'+str(self.ui.teamTabsTableWidget.selectedItems()))
		# for qti in self.ui.teamTabsTableWidget.selectedItems():
					extTeamName=twi.whatsThis()
					# logging.info(' blink: '+str(extTeamName))
					hidden=False
					if extTeamName in self.parent.hiddenTeamTabsList:
						hidden=True
					status=teamStatusDict.get(extTeamName,None)
					age=teamTimersDict.get(extTeamName,0)
					if self.parent.blinkToggle==1 and status not in ["At IC","Off Duty"]:
						if age>=self.parent.timeoutRedSec:
							status='TIMED_OUT_RED'
						elif age>=self.parent.timeoutOrangeSec:
							status='TIMED_OUT_ORANGE'
					ad=statusAppearanceDict.get(status,{})
					fgColor=ad.get('foreground',None)
					bgColor=ad.get('background',None)
					bgHidden=ad.get('bgHidden',None)
					blink=ad.get('blink',False)
					if hidden:
						fgColor=QColor('#555')
						bgColor=bgHidden
					if blink and self.parent.blinkToggle==1:
						fgColor=None
						if hidden:
							fgColor=QColor('#555')
						bgColor=None
					fgColor=fgColor or Qt.black
					bgColor=bgColor or Qt.white
					# logging.info('  status:'+str(status)+'  hidden:'+str(hidden)+'  blink:'+str(blink)+'  fgColor:'+str(fgColor)+'  bgColor:'+str(bgColor))
					twi.setForeground(QBrush(fgColor))
					twi.setBackground(QBrush(bgColor))


class caltopoFolderPopup(QDialog):
	def __init__(self, parent=None):
		super().__init__(parent)
		self.parent=parent

		# Create the TreeView for the dropdown popup
		self.tree_view = QTreeView(self)
		self.tree_view.setHeaderHidden(True)  # Hide the header to look like a simple tree
		self.tree_view.setSelectionMode(QTreeView.SingleSelection)
		self.tree_view.setEditTriggers(QTreeView.NoEditTriggers)
		self.tree_view.setExpandsOnDoubleClick(False)
		self.tree_view.setAnimated(True) # this affects expand/collapse, but does not affect scroll
		self.tree_view.setFont(self.parent.ui.caltopoFolderButton.font())
		self.tree_view.setVerticalScrollMode(QAbstractItemView.ScrollPerPixel)

		self.tree_view.setFixedHeight(300)

		# Create a model for the tree view
		self.model = QStandardItemModel()
		self.tree_view.setModel(self.model)

		self.tree_view.entered.connect(self.enteredCB)
		self.tree_view.clicked.connect(self.clickedCB)
		self.tree_view.expanded.connect(self.expandedCB)
		self.tree_view.collapsed.connect(self.collapsedCB)
		# self.tree_view.verticalScrollBar().valueChanged.connect(lambda:logging.info(f'scroll value changed to {self.tree_view.verticalScrollBar().value()}'))

		self.setWindowTitle("Popup Dialog")
		self.setWindowFlags(Qt.Popup)
		layout = QVBoxLayout(self)
		layout.setContentsMargins(0,0,0,0)
		layout.addWidget(self.tree_view)
		self.setLayout(layout)
		self.tree_view.setMouseTracking(True)
		self.blockPopup=False
		self.padding=10

	def animated_scroll(self,tree_view,index):
		# Get the vertical scroll bar
		v_bar = tree_view.verticalScrollBar()
		val=v_bar.value() # this is a number of pixels within the entire scroll area, i.e. if the view were infinitely tall
		rect = tree_view.visualRect(index)
		top=rect.top() # this is a number of pixels relative to the current top of the view
		# logging.info(f'folder scrollbar min:{v_bar.minimum()}  max:{v_bar.maximum()}  current:{val}  top(index)={top}')
		
		# Calculate the target position
		# target_value=top-50
		# target_value = v_bar.value() + rect.top()
		# target_value=int(rect.top()/2)
		# target_value=v_bar.value()+5
		# target_value=60
		# target_value=top-60 # value relateive to val (the entire bottomless scroll area) to be placed at the top of the view
		target_value=val+top-60
		# target_value=v_bar.maximum()-2
		
		# logging.info(f'starting scroll animation: start={val} end={target_value}')
		# Create animation - must be an instance var, not local var, to avoid deletion when this function ends;
		#  animation will appear to not start if it's a local var
		self.folderScrollAnimation = QPropertyAnimation(v_bar, b"value")
		self.folderScrollAnimation.setDuration(500) # Duration in ms
		self.folderScrollAnimation.setEasingCurve(QEasingCurve.OutCubic)
		self.folderScrollAnimation.setStartValue(val)
		self.folderScrollAnimation.setEndValue(target_value)
		
		# Start animation
		# QTimer.singleShot(100,animation.start)
		self.folderScrollAnimation.start()
		# QTimer.singleShot(100,lambda:v_bar.setValue(target_value))

	def closeEvent(self,e):
		self.blockPopup=True
		QTimer.singleShot(250,self.clearBlock)
		# logging.info('popup closed')

	def clearBlock(self):
		self.blockPopup=False

	def enteredCB(self,i):
		# rect = self.tree_view.visualRect(i)
		# top=rect.top()
		# v_bar=self.tree_view.verticalScrollBar()
		# val=v_bar.value()
		# logging.info(f'entered: top={top}  current={val}')
		self.setFullLabel(i)

	def expandedCB(self,i):
		# logging.info('expanded')
		# self.tree_view.scrollTo(i,QAbstractItemView.PositionAtCenter)
		self.collapseOthers(i)
		QTimer.singleShot(300,lambda:self.animated_scroll(self.tree_view,i))

	def collapsedCB(self,i):
		pass
		# logging.info('collapsed')

	def clickedCB(self,i):
		# logging.info('clicked:'+i.data()+':'+i.data(Qt.UserRole))
		# parent=i.parent()
		# logging.info(f'  model={i.model()} row={i.row()} col={i.column()}')
		# logging.info(f'  parent model={parent.model()} row={parent.row()} col={parent.column()}')
		# Get the full hierarchy path for display
		# current_index = i
		# path_list = [self.model.data(i)]
		# while current_index.parent().isValid():
		# 	parent_index = current_index.parent()
		# 	parent_text = self.model.data(parent_index)
		# 	path_list.insert(0, parent_text)
		# 	current_index = parent_index
		# self.parent.caltopoFolderUpdateButtonText(' > '.join(path_list))
		self.parent.caltopoFolderChanged(i.data(Qt.UserRole))
		self.setFullLabel(i)
		self.close() # close the popup
		self.parent.ui.caltopoFolderButton.clearFocus() # do this AFTER self.close to prevent the button from staying blue

	def setFullLabel(self,i):
		# Get the full hierarchy path for display
		current_index = i
		path_list = [self.model.data(i)]
		while current_index.parent().isValid():
			parent_index = current_index.parent()
			parent_text = self.model.data(parent_index)
			path_list.insert(0, parent_text)
			current_index = parent_index
		# Join path with a separator and set the text
		# self.parent.ui.caltopoFolderButton.setText(' > '.join(path_list))
		self.parent.caltopoFolderButtonUpdateText(' > '.join(path_list))

		# txt=' > '.join(path_list)
		# textWidth=self.parent.fm.size(0,txt).width()
		# buttonWidth=self.parent.ui.caltopoFolderButton.width()
		# # horizontalAdvance=self.parent.fm.horizontalAdvance(txt)
		# # boundingWidth=self.parent.fm.boundingRect(txt).width()
		# # print('new text width = '+str(textWidth)+'   horizontal advance = '+str(horizontalAdvance)+'   boundingRect width = '+str(boundingWidth)+'   button width = '+str(buttonWidth))
		# txtForButton=txt
		# self.parent.ui.caltopoFolderButton.setToolTip('') # only show tooltip if button text is elided
		# # original:   "L1longdirname > L2longdirname > L3longdirname"
		# # first try:  "L1lo... > L2lo... > L3longdirname"
		# # second try: "L1lo..> L2lo..> L3longdirname"
		# # third try:  "L1..>L2..>L3longdirname"
		# # after that, just start a standard right-elide until it fits: "L1..>L2..>L3lon..."
		# # in all cases, the tooltop text should be the full original path
		# if (textWidth+self.padding)>buttonWidth:
		# 	# print('  too wide! elide!  full text = '+txt)
		# 	names=txt.split(' > ')
		# 	a1Names=[]
		# 	a2Names=[]
		# 	a3Names=[]
		# 	for name in names[:-1]: # don't shorten the leaf name
		# 		a1Name=name
		# 		a2Name=name
		# 		a3Name=name
		# 		if len(name)>6:
		# 			a1Name=name[0:4]+'...'
		# 		if len(name)>5:
		# 			a2Name=name[0:4]+'..'
		# 		if len(name)>4:
		# 			a3Name=name[0:2]+'..'
		# 		a1Names.append(a1Name)
		# 		a2Names.append(a2Name)
		# 		a3Names.append(a3Name)
		# 	a1Names.append(names[-1])
		# 	a2Names.append(names[-1])
		# 	a3Names.append(names[-1])
		# 	attempt1=' > '.join(a1Names)
		# 	attempt2='> '.join(a2Names)
		# 	attempt3='>'.join(a3Names)
		# 	attempt4=f'...>{names[-1]}'
		# 	# print(f'attempt1: {attempt1}\nattempt2: {attempt2}\nattempt3: {attempt3}\nattempt4: {attempt4}')
		# 	if self.parent.fm.horizontalAdvance(attempt1)+self.padding<buttonWidth:
		# 		txtForButton=attempt1
		# 	elif self.parent.fm.horizontalAdvance(attempt2)+self.padding<buttonWidth:
		# 		txtForButton=attempt2
		# 	elif self.parent.fm.horizontalAdvance(attempt3)+self.padding<buttonWidth:
		# 		txtForButton=attempt3
		# 	else:
		# 		txtForButton=attempt4
		# 	self.parent.ui.caltopoFolderButton.setToolTip(txt)

		# self.parent.ui.caltopoFolderButton.setText(txtForButton)

	# recursive population code taken from https://stackoverflow.com/a/53747062/3577105
	#  add code to alphabetize within each branch
	def fill_model_from_json(self,parent, d):
		if isinstance(d, dict):
			for k, v in sorted(d.items(),key=lambda item: item[0].lower()): # case insensitive alphabetical sort by key
				[title,id]=k.split('|')
				child = QStandardItem(title)
				child.setData(id,Qt.UserRole)
				parent.appendRow(child)
				self.fill_model_from_json(child, v)
		elif isinstance(d, list):
			for v in d:
				self.fill_model_from_json(parent, v)
		else:
			parent.appendRow(QStandardItem(str(d)))

	# def fill_dict_from_model(self,parent_index, d):
	# 	v = {}
	# 	for i in range(self.model.rowCount(parent_index)):
	# 		ix = self.model.index(i, 0, parent_index)
	# 		self.fill_dict_from_model(ix, v)
	# 	d[parent_index.data()] = v

	# def model_to_dict(self):
	# 	d = dict()
	# 	for i in range(self.model.rowCount()):
	# 		ix = self.model.index(i, 0)
	# 		self.fill_dict_from_model(ix, d)    
	# 	return d
	
	# adapted from https://stackoverflow.com/a/45461474/3577105
	# hierFromList: given a list of (child,parent) tuples, returns a nested dict of key=name, val=dict of children
	def hierFromList(self,lst):
		# lst = [('john','marry'), ('mike','john'), ('mike','hellen'), ('john','elisa')]
		# lst is not directly comparable to folders; the folder list is (child,parent):
		# lst=[('mike',None),('john','mike'),('elisa','john'),('marry','john'),('hellen','mike')]
		# lst=[(f['id'],f['properties']['folderId'] or 'Top') for f in features]

		# Build a directed graph and a list of all names that have no parent
		graph = {name: set() for tup in lst for name in tup}
		# print('graph initial:'+str(graph))
		has_parent = {name: False for tup in lst for name in tup}
		# print('has_parent initial:')
		# print(json.dumps(has_parent,indent=3))
		for child,parent in lst:
			graph[parent].add(child)
			has_parent[child] = True
		# print('graph after:'+str(graph))
		# print('has_parent after:')
		# print(json.dumps(has_parent,indent=3))

		# All names that have absolutely no parent:
		roots = [name for name, parents in has_parent.items() if not parents]

		# traversal of the graph (doesn't care about duplicates and cycles)
		def traverse(hierarchy, graph, names):
			for name in names:
				hierarchy[name] = traverse({}, graph, graph[name])
			return hierarchy

		idHier=traverse({}, graph, roots)['Top|Top']
		return idHier

	def populate(self,accountId):
		"""Populates the tree model from a dictionary."""
		self.model.clear()
		# make sure <Top Level> is always the first (and possibly only) entry
		topLevelItem=QStandardItem('<Top Level>')
		topLevelItem.setData('0',Qt.UserRole) # UserRole is used to store folder ID; use a dummy value here
		self.model.appendRow(topLevelItem)
		acctFolders=[f for f in self.parent.parent.cts.accountData['features'] if f['properties']['accountId']==accountId and f['properties']['class']=='UserFolder']
		if not acctFolders:
			return
		logging.info('acctFolders:')
		logging.info(json.dumps(acctFolders,indent=3))
		folderChildParentList=[]
		for f in acctFolders:
			id=f['id']
			title=f['properties']['title']
			parentId=f['properties']['folderId'] or 'Top'
			logging.info(f'f:id={id} title="{title}" parentId={parentId}')
			if parentId=='Top':
				parentTitle='Top'
			else:
				parentTitle=[pf['properties']['title'] for pf in acctFolders if pf['id']==parentId][0]
			folderChildParentList.append((f'{title}|{id}',f'{parentTitle}|{parentId}'))
		logging.info('folderChildParentList:')
		logging.info(json.dumps(folderChildParentList,indent=3))
		data=self.hierFromList(folderChildParentList)
		logging.info('data:')
		logging.info(json.dumps(data,indent=3))
		self.fill_model_from_json(self.model.invisibleRootItem(),data)
		# two levels at most
		# for key, children in data.items():
		#     parent_item = QStandardItem(key)
		#     for child_text in children:
		#         child_item = QStandardItem(child_text)
		#         parent_item.appendRow(child_item)
		#     self.model.appendRow(parent_item)

		# recursive - any number of levels
		# def populate_recurse(dict,parentItem=None):
		# 	for key in dict.keys():
		# 		print('processing '+str(key))
		# 		if parentItem:
		# 			parentItem.appendRow(QStandardItem(key))
		# 		else:
		# 			parentItem=QStandardItem(key)
		# 		for child in dict[key]:
		# 			populate_recurse(dict[key],parentItem)
		# 	return parentItem
		
		# self.model.appendRow(populate_recurse(data))

		# for key, children in data.items():
		# 	parent_item = QStandardItem(key)
		# 	for child_text in children:
		# 		child_item = QStandardItem(child_text)
		# 		parent_item.appendRow(child_item)
		# 	self.model.appendRow(parent_item)

		# for r in range(self.model.rowCount()):
		# 	for c in range(self.model.columnCount()):
		# 		txt=self.model.item(r,c).text()
		# 		print(f'row {r} col {c} : {txt}')

	# collapse all other indeces, from all levels of nesting, except for ancestors of the index in question
	def collapseOthers(self,expandedIndex):
		QApplication.processEvents()
		# print('collapse_others called: expandedIndex='+str(expandedIndex))
		ancesterIndices=[]
		parent=expandedIndex.parent() # returns a new QModelIndex instance if there are no parents
		# print('building ancesterIndices: first parent='+str(parent))
		# print(f'  model={parent.model()} row={parent.row()} col={parent.column()}')
		while parent.isValid():
			ancesterIndices.append(parent)
			# print('appending '+str(parent))
			parent=parent.parent() # ascend and recurse while valid (new QModelIndex instance if there are no parents)
		# print('ancesterIndices='+str(ancesterIndices))
		def _collapse_recursive(parent_index: QModelIndex,sp='  '):
			for row in range(self.model.rowCount(parent_index)):
				index = self.model.index(row, 0, parent_index)
				item=self.model.itemFromIndex(index)
				txt=item.text()
				# print(sp+f'checking r={row} col=0 : {txt}')
				if index.isValid() and index!=expandedIndex and index not in ancesterIndices:
					# print(sp+'  collapsing')
					self.tree_view.collapse(index)
					# self.tree_view.setExpanded(index,False)
					
					# Recursively process children
					if self.model.hasChildren(index):
						_collapse_recursive(index,sp+'  ')

		# start a fresh recursion for each top level index
		# for row in range(self.model.rowCount()):
		# 	for col in range(self.model.columnCount()):
		# 		_collapse_recursive(self.model.index(row,col))
		
		# Start the recursion from the invisible root item
		_collapse_recursive(QModelIndex())
		QApplication.processEvents()


class caltopoCreateCTSThread(QThread):
	finished=pyqtSignal(bool)

	def __init__(self,parent):
		QThread.__init__(self)
		self.parent=parent
		
	def run(self):
		logging.info('caltopoCreateCTSThread started')
		# time.sleep(5) # pause to show backgrounding effects - hopefully a spinner
		# open a mapless caltopo.com session first, to get the list of maps; if URL is
		#  already specified before the first createCTS call, then openMap will
		#  be called after the mapless session is openend
		# logging.info('createCTS called:')
		if self.parent.cts is not None: # close out any previous session
			# logging.info('Closing previous CaltopoSession')
			# self.closeCTS()
			logging.info('  cts is already open; returning')
			return
			# self.ui.linkIndicator.setText("")
			# self.updateLinkIndicator()
			# self.link=-1
			# self.updateFeatureList("Folder")
			# self.updateFeatureList("Marker")
		domainAndPort='caltopo.com'
		if self.parent.optionsDialog.ui.caltopoDesktopButton.isChecked():
			domainAndPort=self.parent.optionsDialog.ui.ctdServerComboBox.currentText()
		logging.info('  creating mapless online session for user '+self.parent.caltopoAccountName+' on server '+domainAndPort)
		self.parent.cts=CaltopoSession(domainAndPort=domainAndPort,
								configpath=os.path.join(self.parent.configDir,'cts.ini'),
								account=self.parent.caltopoAccountName,
								syncInterval=10,syncTimeout=20, # reduce log file size and overzealous disconnects
								deletedFeatureCallback=self.parent.caltopoDeletedFeatureCallback,
								disconnectedCallback=self.parent.caltopoDisconnectedCallback,
								reconnectedCallback=self.parent.caltopoReconnectedCallback,
								mapClosedCallback=self.parent.caltopoMapClosedCallback)
		# logging.info('  starting visual delay...')
		# time.sleep(10) # visualize delay - otherwise we may never see caltopoOverlayLabel (which is fine!)
		logging.info('  back from CaltopoSession init')
		noMatchDict={
			'groupAccountTitle':'<Choose Acct>',
			'mapList':[{
				'id':'Top',
				'title':'<Choose Map>',
				'updated':0,
				'type':'map',
				'folderId':0,
				'folderName':'<Top Level>'}]}
		# try:
		# 	aml=self.cts.getAllMapLists()
		# except Exception as e:
		# 	logging.info('exception from getAllMapLists: '+str(e))
		# 	if 'Failed to resolve' in str(e):
		# 		logging.info('  failed to resolve')
		# 		self.caltopoDisconnectedCallback()
		# 		self.cts._sendRequest('get','[PING]',j=None,callbacks=[[self.caltopoReconnectedFromCreateCTS]])
		# 	return False
		aml=self.parent.cts.getAllMapLists()
		if not aml or not self.parent.cts.accountData:
			logging.info('Account data is empty; disconnected')
			# self._sig_caltopoDisconnectedFromCreateCTS.emit()
			# box=QMessageBox(QMessageBox.Warning,"Disconnected","You have no connection to the CalTopo server.\n\nYou can close the Options dialog and continue to use RadioLog as normal.\n\nThe Options dialog will pop up again when connection is re-established.",
			# 	QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			# box.show()
			# box.raise_()
			# self.caltopoDisconnectedCallback()
			# self.cts._sendRequest('get','[PING]',j=None,callbacks=[[self.caltopoReconnectedFromCreateCTS]])
			# return False
			self.finished.emit(False)
			return
		self.parent.caltopoMapListDicts=[noMatchDict]+aml
		# logging.info('caltopoMapListDicts:')
		# logging.info(json.dumps(self.caltopoMapListDicts,indent=3))
		self.parent.caltopoLink=1
		# self.accountDataChanged.emit()
		# self.linkChanged.emit() # mapless
		# self.finished.emit()
		logging.info('  end of createCTS')
		# return True
		self.finished.emit(True)


class caltopoOpenMapThread(QThread):
	finished=pyqtSignal(bool)

	def __init__(self,parent):
		QThread.__init__(self)
		self.parent=parent

	def run(self):
		logging.info(f'about to call cts.openMap: apiVersion={self.parent.cts.apiVersion}  mapID={self.parent.cts.mapID}  caltopoLink={self.parent.caltopoLink}')
		# time.sleep(5) # visualize delay like a slow-open
		rval=self.parent.cts.openMap(self.parent.optionsDialog.ui.caltopoMapIDField.text())
		logging.info(f'return from cts.openMap:{rval} apiVersion={self.parent.cts.apiVersion}  mapID={self.parent.cts.mapID}  caltopoLink={self.parent.caltopoLink}')
		self.finished.emit(self.parent.caltopoLink>0) # emit False if failed due to disconnect etc.
		# logging.info('  starting visual delay...')
		# time.sleep(10) # visualize delay - otherwise we may never see caltopoOverlayLabel (which is fine!)


class optionsDialog(QDialog,Ui_optionsDialog):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.parent=parent
		self.ui=Ui_optionsDialog()
		self.ui.setupUi(self)
		self.caltopoNormalFont=QFont(self.ui.caltopoMapNameComboBox.font())
		self.caltopoNormalStrikeFont=QFont(self.caltopoNormalFont)
		self.caltopoNormalStrikeFont.setStrikeOut(True)
		self.caltopoItalicFont=QFont(self.ui.caltopoMapNameComboBox.font())
		self.caltopoItalicFont.setItalic(True)
		self.caltopoItalicStrikeFont=QFont(self.caltopoItalicFont)
		self.caltopoItalicStrikeFont.setStrikeOut(True)
		self.setStyleSheet(globalStyleSheet)
		self.pauseCB=False
		self.pauseIDCB=False
		self.pauseAccountCB=False
		self.ui.timeoutField.valueChanged.connect(self.displayTimeout)
		self.displayTimeout()
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
##		self.setAttribute(Qt.WA_DeleteOnClose)
		self.ui.datumField.setEnabled(False) # since convert menu is not working yet, TMG 4-8-15
		self.ui.formatField.setEnabled(False) # since convert menu is not working yet, TMG 4-8-15
		self.adjustSize()
		self.setFixedSize(self.size())
		self.secondWorkingDirCB()
		self.newEntryWarningCB()
		self.caltopoSelectionIsReadOnly=False
		self.caltopoUpdateGUI()
		self.qle=self.ui.caltopoMapNameComboBox.lineEdit()
		self.qle.setReadOnly(True) # but still editable, as recommended
		self.caltopoMapNameComboBoxHighlightChanged(0)
		# self.ui.caltopoMapNameComboBox.lineEdit().setFont(self.caltopoItalicStrikeFont)
		self.caltopoFolderPopup=caltopoFolderPopup(self)
		self.fm=QFontMetrics(self.ui.caltopoFolderButton.font())
		self.mapToolTip="""
			<style>
				table {
					border-collapse: collapse;
					width: 100%;
				}
				th, td {
					border: 1px solid black;
					padding: 5px;
					text-align: left;
				}
				th {
					background-color: #f2f2f2;
				}
			</style>
			<table>
			<thead>
				<tr>
					<th>Map Font</th>
					<th>Meaning</th>
				</tr>
			</thead>
				<tbody>
					<tr>
						<td>MapName</td>
						<td>Wrtiable Map</td>
					</tr>
					<tr>
						<td><i>MapName</i></td>
						<td>Writable Bookmark</td>
					</tr>
					<tr>
						<td><s>MapName</s></td>
						<td>Read-only Map</td>
					</tr>
					<tr>
						<td><s><i>MapName<i></s></td>
						<td>Read-only Bookmark</td>
					</tr>
				</tbody>
			</table>"""
		self.ui.caltopoMapNameComboBox.setToolTip(self.mapToolTip)
		# self.ui.caltopoMapNameComboBox.view().setToolTip(self.mapToolTip) # too intrusive
		self.ui.caltopoLinkIndicator.setToolTip(caltopoIndicatorToolTip)
		h=self.ui.caltopoGroupBox.height() # make sure adjustSize has been called, otherwise this could be a tiny number
		self.pyqtspinner=WaitingSpinner(self.ui.caltopoGroupBox,True,True,
									roundness=50,
									radius=int(h/6),
									line_length=int(h/6),
									lines=15,
									line_width=int(h/25))
		# self.pyqtspinner.setRadius(int(self.ui.caltopoGroupBox.height()*0.75))
		# self.createCTSThread=caltopoCreateCTSThread(self)
		# self.createCTSThread.finished.connect(self.createCTSCB)
		self.overlayLabel=QLabel('Overlay Label',self) # parent=self so it stays enabled when groupbox is disabled
		self.overlayLabel.setVisible(False)
		self.overlayLabel.setFont(self.ui.caltopoOpenMapButton.font())
		self.overlayLabel.setStyleSheet('QLabel {border:2px outset gray; padding: 5px; background-color:rgba(255,255,255,0.9)}')
		self.overlayLabel.setAlignment(Qt.AlignCenter)
		# self.overlayLabel.adjustSize()
		# self.overlayLabel.move(int((self.width()/2)-(self.overlayLabel.width()/2)),int((self.height()/2)-(self.overlayLabel.height()/2)))
		self.firstShow=True # caltopoIntegrationDefault isn't yet defined; only apply the default on the first showing of the dialog
		
		self.ctsOverlayTimer=QTimer(self)
		self.ctsOverlayTimer.setSingleShot(True)
		self.ctsOverlayTimer.timeout.connect(lambda:
					self.caltopoUpdateOverlayLabel(
						'<span style="font-size:24px;color:#44f;line-height:2">This is taking a while...<br></span><span style="font-size:16px;color:black;line-height:1.5">You can use or close the options dialog;<br>this operation will keep trying in the background<br>and the options dialog will pop up again when finished.</span>'))
		
		self.openingOverlayTimer=QTimer(self)
		self.openingOverlayTimer.setSingleShot(True)
		self.openingOverlayTimer.timeout.connect(lambda:
					self.caltopoUpdateOverlayLabel(
						'<span style="font-size:24px;color:#44f;line-height:2">This is taking a while...<br></span><span style="font-size:16px;color:black;line-height:1.5">You can use or close the options dialog;<br>this operation will keep trying in the background;<br>the link indicator will turn bright green when finished.</span>'))

	def showEvent(self,event):
		# clear focus from all fields, otherwise previously edited field gets focus on next show,
		# which could lead to accidental editing
		self.ui.incidentField.clearFocus()
		self.ui.datumField.clearFocus()
		self.ui.formatField.clearFocus()
		self.ui.timeoutField.clearFocus()
		self.ui.secondWorkingDirCheckBox.clearFocus()
		self.parent.caltopoUpdateLinkIndicator()
		try:
			self.parent.openMapThread.finished.disconnect(self.accept)
		except:
			pass # pass silently if the signal wasn't connected in the first place; see accept()
		# self.caltopoEnabledCB()
		# logging.info(f'fistShow:{self.firstShow} caltopoIntegrationDefault={self.parent.caltopoIntegrationDefault}')
		if self.firstShow:
			self.ui.caltopoGroupBox.setChecked(self.parent.caltopoIntegrationDefault)
			self.ui.caltopoRadioMarkersCheckBox.setChecked(self.parent.caltopoMapMarkersDefault)
			self.ui.caltopoWebBrowserCheckBox.setChecked(self.parent.caltopoWebBrowserDefault)
			self.firstShow=False

	def displayTimeout(self):
		self.ui.timeoutLabel.setText("Timeout: "+timeoutDisplayList[self.ui.timeoutField.value()][0])
	
	def secondWorkingDirCB(self):
		self.parent.use2WD=self.ui.secondWorkingDirCheckBox.isChecked()
	
	def newEntryWarningCB(self):
		self.parent.useNewEntryWindowHiddenPopup=self.ui.newEntryWarningCheckBox.isChecked()

	def fsSendCB(self):
		self.parent.fsSendDialog.show()

	def accept(self):
		# only save the rc file when the options dialog is accepted interactively;
		#  saving from self.optionsAccepted causes errors because that function
		#  is called during init, before the values are ready to save
		self.parent.saveRcFile()
		if self.ui.caltopoGroupBox.isChecked() and self.parent.caltopoLink==1:
			# box=QMessageBox(QMessageBox.Warning,"No map has been opeend","Did you mean to open a map before closing the Options dialog?",
			box=QMessageBox(QMessageBox.Warning,"No map has been opeend","Did you mean to open the selected map?\n\nClick Yes to open the selected map (and to close the Options dialog after opening).",
				QMessageBox.Yes|QMessageBox.No,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			box.show()
			box.raise_()
			if box.exec_()==QMessageBox.Yes: # leave the options dialog open
				box.close()
				# close the options dialog when the map is connected;
				#  connecting the slot here means we have to disconnect it when the dialog is opened,
				#  otherwise it stays connected and would still have effect the next time the dialog is opened
				self.parent.openMapThread.finished.connect(self.accept)
				self.caltopoOpenMapButtonClicked()
			# 	return
			# else:
			# 	return # don't close the options dialog if No is clicked
			return # don't close the options dialog if No is clicked
		super(optionsDialog,self).accept()
		
	def toggleShow(self):
		if self.isVisible():
			self.close()
		else:
			self.show()
			self.raise_()
			self.parent.fsSaveLog()

	# caltopo GUI fields interaction
	# there are four relevant fields: Account, Folder, and Title QComboBoxes, and ID QLineEdit; call them A,F,T,I
	# Here's the intended sequence of field updates, after a given field is edited by the user in the GUI:
	# A : populate F, set F index to 0 --> populate T, set T index to 0 --> set I
	# F : populate T, set T index to 0 --> set I
	# T : set I
	# I : use the Search Tree to find a match; set A, F, and T, all without callbacks

	def caltopoFolderButtonPressed(self):
		logging.info('folder button pressed')
		if self.caltopoFolderPopup.blockPopup:
			logging.info('  blockPopup is True (popup was recently closed); popup not shown; returning')
			return
		# Get the global position of the button's top-left corner
		button_pos = self.ui.caltopoFolderButton.mapToGlobal(QPoint(0, 0))

		# Calculate the desired position for the popup
		popup_x = button_pos.x()+2
		popup_y = button_pos.y() + self.ui.caltopoFolderButton.height()-2
		popup_h=self.caltopoFolderPopup.height()
		screen_bottom_y=self.ui.caltopoFolderButton.screen().geometry().height()
		if popup_y+popup_h>screen_bottom_y:
			popup_y=button_pos.y()-popup_h+2

		# Sample hierarchical data
		# data = {
		# 	"Fruits": ["Apple", "Banana", "Orange"],
		# 	"Vegetables": ["Carrot", "Broccoli", "Spinach"],
		# 	"Dairy": ["Milk", "Cheese", "Yogurt"]
		# }

		# this works, 10/21/25:
		# data={
		# 		"AAAAAAAA": {},
		# 		"V205THU7": {
		# 			"U3762091": {
		# 				"07QF60R8": {},
		# 				"HTVGVJHQ": {}
		# 			},
		# 			"ARB5MEGR": {
		# 				"21C7SNF0": {},
		# 				"5PGQL717": {}
		# 			}
		# 		}
		# 	}
		
		# data={
		# 		"AAAAAAAA|Folder 1": {},
		# 		"V205THU7|Folder 2": {
		# 			"U3762091|Folder2A": {
		# 				"07QF60R8|2A1": {},
		# 				"HTVGVJHQ|2a2": {}
		# 			},
		# 			"ARB5MEGR|2B": {
		# 				"21C7SNF0|2b1": {},
		# 				"5PGQL717|2b2": {}
		# 			}
		# 		}
		# 	}
		
		# self.caltopoFolderPopup.populate()

		self.caltopoFolderPopup.move(popup_x, popup_y)
		self.caltopoFolderPopup.setFixedWidth(self.ui.caltopoFolderButton.width()-2)
		self.caltopoFolderPopup.exec_() # Show as a modal dialog

	def caltopoUpdateGUI(self):
		# self.parent.caltopoLink states:
		#  -1 = offline
		#   0 = not connected to server
		#   1 = connected to mapless caltopo session
		#   2 = map opened and connected
		#   3 = in transition (connecting or disconnecting)
		link=self.parent.caltopoLink
		en=self.ui.caltopoGroupBox.isChecked()
		rm=self.ui.caltopoRadioMarkersCheckBox.isChecked()
		wb=self.ui.caltopoWebBrowserCheckBox.isChecked()
		# dc=self.parent.disconnectedFlag

		# set enabled/disabled for caltopo group fields
		self.ui.caltopoRadioMarkersCheckBox.setEnabled(en)
		self.ui.caltopoWebBrowserCheckBox.setEnabled(en)
		e=en and (rm or wb)
		e2=e and link==1
		# logging.info('e='+str(e)+'  e2='+str(e2))
		self.ui.caltopoComButton.setEnabled(e2)
		# self.ui.caltopoDesktopButton.setEnabled(e2) # leave it disabled for now, pending CTD-slow-GET-while-online issue
		self.ui.ctdServerComboBox.setEnabled(e2 and self.ui.caltopoDesktopButton.isChecked())
		self.ui.caltopoAccountAndFolderLabel.setEnabled(e2)
		self.ui.caltopoAccountComboBox.setEnabled(e2)
		self.ui.caltopoFolderLabel.setEnabled(e2)
		self.ui.caltopoFolderButton.setEnabled(e2)
		self.ui.caltopoMapLabel.setEnabled(e2)
		self.ui.caltopoMapNameComboBox.setEnabled(e2)
		self.ui.caltopoMapIDField.setEnabled(e2)
		self.ui.caltopoLinkIndicator.setEnabled(e2)
		self.ui.caltopoOpenMapButton.setEnabled(e and link in [1,2])
		
		max_accountname_width=0
		fm=QFontMetrics(self.ui.caltopoAccountComboBox.font())
		for i in range(self.ui.caltopoAccountComboBox.count()):
			w=fm.width(self.ui.caltopoAccountComboBox.itemText(i))
			max_accountname_width=max(max_accountname_width,w)
		self.ui.caltopoAccountComboBox.view().setMinimumWidth(max_accountname_width+30)

		# set the Open Map button text
		txt=self.ui.caltopoOpenMapButton.text()
		if e:
			if link==0: # not yet connected to a mapless session, but checkboxes enabled
				txt='Getting Account Data...'
			elif link==1:
				txt='Click to Open Selected Map'
			elif link==2:
				txt='Map Opened - Click to Close Map'
			elif link==-1:
				txt='Offline - Attempting to Reconnect...'
			elif link!=3: # leave as-is if in transition
				txt='-----'
		else:
			txt='Caltopo Integration Disabled'
		self.ui.caltopoOpenMapButton.setText(txt)

		# set the connect button tooltip
		if e:
			self.ui.caltopoOpenMapButton.setToolTip('')
		elif self.parent.caltopoLink>=0:
			self.ui.caltopoOpenMapButton.setToolTip("To enable this button:\nEnable 'Caltopo Integration'\nAND\nat least one Caltopo integration feature.")
		else:
			self.ui.caltopoOpenMapButton.setToolTip('Attempting to reconnect...')
			
		# processEvents, in case this is being called with other GUI actions
		QCoreApplication.processEvents()

	def caltopoUpdateOverlayLabel(self,text):
		# self.overlayLabel.setText('<span style="font-size:24px">Big Text<br></span><span style="font-size:16px">Small Text</span>')
		if text and self.isVisible() and self.pyqtspinner.is_spinning: # don't display if the spinner has already stopped
			self.overlayLabel.setText(text)
			# self.overlayLabel.move(200,400)
			self.overlayLabel.adjustSize()
			x=int((self.width()/2)-(self.overlayLabel.width()/2))
			y=int(self.ui.caltopoGroupBox.pos().y()+(self.ui.caltopoGroupBox.height()/2)-(self.overlayLabel.height()/2))
			self.overlayLabel.move(x,y)
			self.overlayLabel.setVisible(True)
			# QCoreApplication.processEvents()
			# self.overlayLabel.update()
		else:
			self.overlayLabel.setVisible(False)

	# def caltopoSetOverlayText(self):
	# 	# this method runs in the main thread
	# 	# called in a singleshot from createCTS
	# 	if self.isVisible(): # only set the overlay text if the dialog is still open and createCTS is still running
	# 		self.caltopoUpdateOverlayLabel('<span style="font-size:24px">Big Text<br></span><span style="font-size:16px">Small Text</span>')

	def caltopoServerChanged(self): # called when any of the server-related fields have been clicked
		# if a map is already open, confirm with the user that changing the server will close the map
		# box=QMessageBox(QMessageBox.Warning,"A map is open","Changing any of the server selections will close the currently open map.\n\nDo you still want to change the server selections?",
		# 	QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
		# box.show()
		# box.raise_()
		# box.exec_()
		self.parent.closeCTS()
		QApplication.processEvents()
		self.caltopoEnabledCB()
		self.caltopoUpdateGUI()

	def caltopoEnabledCB(self): # called from stateChanged of group box AND of radio markers checkbox
		en=self.ui.caltopoGroupBox.isChecked()
		rm=self.ui.caltopoRadioMarkersCheckBox.isChecked()
		wb=self.ui.caltopoWebBrowserCheckBox.isChecked()
		e=en and (rm or wb)
		self.caltopoUpdateGUI()
		if e:
			if self.parent.caltopoLink==0: # checkboxes enabled but not yet connected to a mapless session
				logging.info('calling createCTS')
				self.ui.caltopoOpenMapButton.setText('Getting account data...')
				self.ui.caltopoOpenMapButton.setEnabled(False)
				# QCoreApplication.processEvents()

				# if not self.parent.createCTS(): # false return from createCTS indicates failure
					# return False
				
				# self.pyqtspinner.start()
				# self.createCTSThread.start()

				self.parent.createCTS()

				# self.parent.createCTSThread=threading.Thread(target=self.parent._createCTSWorker,daemon=True,name='createCTSThread')
				# self.parent.createCTSThread.start()
				# self.parent.createCTSThread.join()
				# self.pyqtspinner.stop()
				# logging.info('createCTS completed')
				# logging.info('caltopoMapListDicts:')
				# logging.info(json.dumps(self.parent.caltopoMapListDicts,indent=3))
				# self.caltopoRedrawAccountData()
				# self.caltopoUpdateGUI()
				# self.ui.caltopoOpenMapButton.setText('Click to Open Selected Map')
				# self.ui.caltopoOpenMapButton.setEnabled(True)
		else:
			self.parent.closeCTS()
			self.caltopoUpdateGUI()
		self.parent.caltopoLink=0
		if self.parent.cts:
			self.parent.caltopoLink=self.parent.cts.apiVersion
			if self.parent.cts.mapID:
				self.parent.caltopoLink=2
		self.caltopoUpdateGUI()
		self.parent.caltopoUpdateLinkIndicator()

	# def createCTSCB(self,result):
	# 	logging.info(f'createCTSCB called with result={result}')
	# 	self.pyqtspinner.stop()
	# 	self.caltopoRedrawAccountData()
	# 	self.caltopoUpdateGUI()
	# 	self.show() # in case it was closed by the operator while spinning

	# def caltopoEnabledCB(self): # called from stateChanged of group box AND of radio markers checkbox
	# 	# if self.parent.caltopoLink>=0: # don't run any of this if currently unexpectedly disconnected
	# 	a=self.ui.caltopoGroupBox.isChecked()
	# 	# if a and self.parent.caltopoLink<1:
	# 	# 	logging.info('checking for latest map in default group "'+str(self.parent.caltopoDefaultTeamAccount))
	# 	# 	logging.info(str(self.parent.cts.getAllMapLists()))
	# 	radios=self.ui.caltopoRadioMarkersCheckBox.isChecked()
	# 	self.ui.caltopoRadioMarkersCheckBox.setEnabled(a)
	# 	enableMapFields=a and radios
	# 	if enableMapFields:
	# 		# self.caltopoURLCB() # try to reconnect if mapURL is not blank
	# 		if self.parent.cts is None:
	# 			logging.info('calling createCTS')
	# 			self.ui.caltopoOpenMapButton.setText('Getting account data...')
	# 			self.ui.caltopoOpenMapButton.setEnabled(False)
	# 			QCoreApplication.processEvents()
	# 			self.parent.createCTS()
	# 			logging.info('createCTS completed')
	# 			logging.info('caltopoMapListDicts:')
	# 			logging.info(json.dumps(self.parent.caltopoMapListDicts,indent=3))
	# 			self.caltopoRedrawAccountData()
	# 			self.ui.caltopoOpenMapButton.setText('Click to Open Selected Map')
	# 			self.ui.caltopoOpenMapButton.setEnabled(True)
	# 			QCoreApplication.processEvents()
	# 	else:
	# 		self.ui.caltopoOpenMapButton.setText('Caltopo Integration Disabled.')
	# 		self.parent.closeCTS()
	# 		logging.info('closeCTS completed')
	# 	self.caltopoGroupFieldsSetEnabled(enableMapFields)
	# 	self.parent.caltopoLink=0
	# 	if self.parent.cts:
	# 		self.parent.caltopoLink=self.parent.cts.apiVersion
	# 		if self.parent.cts.mapID:
	# 			self.parent.caltopoLink=2
	# 	self.parent.caltopoUpdateLinkIndicator()

	# def caltopoGroupFieldsSetEnabled(self,e):
	# 	self.ui.radioButton.setEnabled(e)
	# 	self.ui.radioButton_2.setEnabled(e)
	# 	self.ui.caltopoAccountAndFolderLabel.setEnabled(e)
	# 	self.ui.caltopoAccountComboBox.setEnabled(e)
	# 	self.ui.caltopoFolderComboBox.setEnabled(e)
	# 	self.ui.caltopoMapLabel.setEnabled(e)
	# 	self.ui.caltopoMapNameComboBox.setEnabled(e)
	# 	self.ui.caltopoMapIDField.setEnabled(e)
	# 	self.ui.caltopoLinkIndicator.setEnabled(e)
	# 	self.ui.caltopoOpenMapButton.setEnabled(e)
	# 	if e:
	# 		self.ui.caltopoOpenMapButton.setToolTip('')
	# 	elif self.parent.caltopoLink>=0:
	# 		self.ui.caltopoOpenMapButton.setToolTip("To enable this button:\nEnable 'Caltopo Integration'\nAND\nat least one Caltopo integration feature.")
	# 	else:
	# 		self.ui.caltopoOpenMapButton.setToolTip('Attempting to reconnect...')

	def caltopoRedrawAccountData(self): # called from worker
		# logging.info('caltopoMapListict:')
		# logging.info(json.dumps(self.parent.caltopoWorker.caltopoMapListDicts,indent=3))
		logging.info('rad1')
		logging.info('map items a:'+str([self.ui.caltopoMapNameComboBox.itemText(i) for i in range(self.ui.caltopoMapNameComboBox.count())]))
		# self.pauseAccountCB=True
		self.pauseCB=True
		# clear out combo box choices now, even if they don't redisplay, to avoid conflict later during caltopoAccountComboBoxChanged
		self.ui.caltopoAccountComboBox.clear()
		self.ui.caltopoFolderButton.setText('')
		self.ui.caltopoMapNameComboBox.clear()
		self.ui.caltopoMapIDField.setText('')
		logging.info('rad2')
		# self.ui.caltopoAccountComboBox.addItem('<Choose Account>') # used when MapIDTextChanged has no match
		accounts=sorted([d['groupAccountTitle'] for d in self.parent.caltopoMapListDicts])
		logging.info('accounts:'+str(accounts))
		self.ui.caltopoAccountComboBox.addItems(accounts)
		logging.info('acct items:'+str([self.ui.caltopoAccountComboBox.itemText(i) for i in range(self.ui.caltopoAccountComboBox.count())]))
		logging.info('rad3')
		# self.pauseAccountCB=False
		self.pauseCB=False
		logging.info('map items b:'+str([self.ui.caltopoMapNameComboBox.itemText(i) for i in range(self.ui.caltopoMapNameComboBox.count())]))
		self.ui.caltopoAccountComboBox.setCurrentText(self.parent.caltopoDefaultTeamAccount)
		logging.info('map items c:'+str([self.ui.caltopoMapNameComboBox.itemText(i) for i in range(self.ui.caltopoMapNameComboBox.count())]))
		logging.info('rad4')

	def caltopoMapIDTextChanged(self):
		logging.info('caltopoMapIDTextChanged to "'+str(self.ui.caltopoMapIDField.text())+'"')
		self.ui.caltopoOpenMapButton.setEnabled(bool(self.ui.caltopoMapIDField.text()))
		if self.pauseCB:
			logging.info('mitc: pausCB is set; returning')
			return
		if self.pauseIDCB:
			logging.info('mitc: pauseIDCB is set; returning')
			return
		txt=self.ui.caltopoMapIDField.text()
		# force uppercase
		txtU=txt.upper()
		if txt!=txtU:
			logging.info(' mitc: uppercasing map ID field from '+str(txt)+' to '+str(txtU))
			self.ui.caltopoMapIDField.setText(txtU)
		dl=self.parent.caltopoMapListDicts
		self.pauseIDCB=True # but allow other callbacks to proceed, to populate comboboxes when a match is found
		# deal with multiple matching mapIDs: there could be multiple bookmarks
		#  in different accounts, but there will only be one map
		# if there is a currently selected account, then any match in that account should
		#  be first (so that it is selected in the GUI), even if it's a bookmark; if there
		#  is no currently selected account, or if there is no match in the currently
		#  selected account, then the map (not bookmark/s) should be selected in the GUI
		allMatches=[]
		for d in dl:
			# logging.info(' next d')
			matches=[dd for dd in d['mapList'] if dd['id'].upper()==txtU]
			if matches:
				gat=d.get('groupAccountTitle')
				# logging.info('  mitc all matches from mapList "'+str(gat)+'":')
				for match in matches:
					match['accountTitle']=gat # add account title to dict, to make sorting easier
				# logging.info(json.dumps(matches,indent=3))
				allMatches+=matches
		# logging.info('allMatches:')
		# logging.info(json.dumps(allMatches,indent=3))

		selectedAcctName=self.ui.caltopoAccountComboBox.currentText()
		matchesInThisAcct=[match for match in allMatches if match['accountTitle']==selectedAcctName]
		# logging.info('matchesInThisAcct pre-sort:')
		# logging.info(json.dumps(matchesInThisAcct,indent=3))
		# sort in descending alphabetical order of 'type', i.e. map(s) first then bookmarks
		matchesInThisAcct.sort(key=lambda match: match.get('type'),reverse=True)
		# logging.info('matchesInThisAcct post-sort:')
		# logging.info(json.dumps(matchesInThisAcct,indent=3))
		
		matchesInOtherAccts=[match for match in allMatches if match['accountTitle']!=selectedAcctName]
		# logging.info('matchesInOtherAccts pre-sort:')
		# logging.info(json.dumps(matchesInOtherAccts,indent=3))
		# sort in descending alphabetical order of 'type', i.e. map(s) first then bookmarks
		matchesInOtherAccts.sort(key=lambda match: match.get('type'),reverse=True)
		# logging.info('matchesInOtherAccts post-sort:')
		# logging.info(json.dumps(matchesInOtherAccts,indent=3))
		
		theMatch={}
		if matchesInThisAcct:
			theMatch=matchesInThisAcct[0] # map/s then bookmark/s in the currently selected account
		elif matchesInOtherAccts:
			theMatch=matchesInOtherAccts[0] # map/s then bookmark/s in other accounts

		# the following code runs after the ID text is changed, whether by typing the ID, or by selecting or hovering a different map name
		if theMatch:
			logging.info('  mitc match:')
			logging.info(json.dumps(theMatch,indent=3))
			# logging.info('match:'+str(d['groupAccountTitle'])+'/'+str(map['folderName'])+'/'+str(map['title']))
			logging.info('  mitc match: setting text on account combo box to "'+str(theMatch['accountTitle'])+'"')
			self.ui.caltopoAccountComboBox.setCurrentText(theMatch['accountTitle'])
			logging.info('  mitc match: setting text on folder button to "'+str(theMatch['folderName'])+'"')
			# self.ui.caltopoFolderButton.setText(theMatch['folderName'])
			self.caltopoFolderButtonUpdateText(theMatch['folderName'])
			logging.info('  mitc match: setting text on title combo box to "'+str(theMatch['title'])+'"')
			self.ui.caltopoMapNameComboBox.setCurrentText(theMatch['title'])
			self.caltopoSelectionIsReadOnly=False
			if theMatch['type']=='bookmark':
				if theMatch['permission']=='read':
					self.ui.caltopoMapNameComboBox.lineEdit().setFont(self.caltopoItalicStrikeFont)
					self.caltopoSelectionIsReadOnly=True
				else:
					self.ui.caltopoMapNameComboBox.lineEdit().setFont(self.caltopoItalicFont)
			elif theMatch.get('locked'):
				self.ui.caltopoMapNameComboBox.lineEdit().setFont(self.caltopoNormalStrikeFont)
				self.caltopoSelectionIsReadOnly=True
			else:
				self.ui.caltopoMapNameComboBox.lineEdit().setFont(self.caltopoNormalFont)
			i=self.ui.caltopoMapNameComboBox.currentIndex()
			# itemFont=self.ui.caltopoMapNameComboBox.itemData(i,Qt.FontRole)
			# self.ui.caltopoMapNameComboBox.lineEdit().setFont(itemFont or self.caltopoNormalFont)
			logging.info('  mitc match processing complete; unpausing callbacks; i='+str(i))
		else: # no match
			# logging.info('  no match: setting account combo box index to 0')
			# self.ui.caltopoAccountComboBox.setCurrentIndex(0)
			# logging.info('  no match: setting folder combo box index to 0')
			# self.ui.caltopoFolderComboBox.setCurrentIndex(0)
			logging.info('  no match: setting map name combo box index to 0')
			self.ui.caltopoMapNameComboBox.setCurrentIndex(0)
			logging.info('  no match processing complete; unpausing callbacks')
		self.pauseIDCB=False

		# if selectedAcctName in matchDict.keys():
		# 	theMatch=matchDict[selectedAcctName][0] # pick the first one in the selected account
		# 	theMatch['accountName']=selectedAcctName
		# else: # not in the selected account; find an account where it's a map rather than bookmark
		# 	theMatch=

		# for d in dl:
		# 	for map in d['mapList']:
		# 		# logging.info('  next m')
		# 		if map['id'].upper()==txtU:
		# 			logging.info('  mitc match:')
		# 			logging.info(json.dumps(map,indent=3))
		# 			# logging.info('match:'+str(d['groupAccountTitle'])+'/'+str(map['folderName'])+'/'+str(map['title']))
		# 			logging.info('  mitc match: setting text on account combo box to "'+str(d['groupAccountTitle'])+'"')
		# 			self.ui.caltopoAccountComboBox.setCurrentText(d['groupAccountTitle'])
		# 			logging.info('  mitc match: setting text on folder combo box to "'+str(map['folderName'])+'"')
		# 			self.ui.caltopoFolderComboBox.setCurrentText(map['folderName'])
		# 			logging.info('  mitc match: setting text on title combo box to "'+str(map['title'])+'"')
		# 			self.ui.caltopoMapNameComboBox.setCurrentText(map['title'])
		# 			self.pauseCB=False
		# 			logging.info('  mitc match processing complete; unpausing callbacks')
		# 			return
		# logging.info('  no match: setting account combo box index to 0')
		# self.ui.caltopoAccountComboBox.setCurrentIndex(0)
		# logging.info('  no match: setting folder combo box index to 0')
		# self.ui.caltopoFolderComboBox.setCurrentIndex(0)
		# logging.info('  no match: setting map name combo box index to 0')
		# self.ui.caltopoMapNameComboBox.setCurrentIndex(0)
		# self.pauseCB=False
		# logging.info('  no match processing complete; unpausing callbacks')

	def caltopoAccountComboBoxChanged(self):
		txt=self.ui.caltopoAccountComboBox.currentText()
		logging.info('acct combo box changed to "'+str(txt)+'"')
		# if self.pauseAccountCB:
		if self.pauseCB:
			logging.info(' acbc: paused; returning')
			return
		# logging.info('accountData:')
		# logging.info(json.dumps(self.parent.cts.accountData,indent=3))
		if txt=='<Choose Acct>':
			return
		accountId=[a for a in self.parent.cts.accountData['accounts'] if a['properties']['title']==txt][0]['id']
		logging.info('  accountId='+str(accountId))
		# time.sleep(2)
		# groupAccountNames=[d.get('groupAccountTitle',None) for d in self.parent.caltopoMapListDicts]
		# logging.info('groupAccountNames:'+str(groupAccountNames))
		# logging.info('currentText:'+str(self.ui.caltopoAccountComboBox.currentText()))

		# dicts=[d for d in self.parent.caltopoMapListDicts if d['groupAccountTitle']==self.ui.caltopoAccountComboBox.currentText()]
		# if dicts:
		# 	logging.info('dicts with groupAccountTitle name = '+str(self.ui.caltopoAccountComboBox.currentText()))
		# 	logging.info(json.dumps(dicts,indent=3))
		# 	mapList=dicts[0]['mapList']
		# 	# take the first non-bookmark entry, since the list is already sorted chronologically		
		# 	mapsNotBookmarks=[m for m in mapList if m['type']=='map']
		# 	logging.info('mapsNotBookmarks:'+str(json.dumps(mapsNotBookmarks,indent=3)))
		# 	folderNames=list(set([m['folderName'] for m in mapsNotBookmarks]))
		# 	self.ui.caltopoFolderButton.setText('')
		# 	# if mapsNotBookmarks:
		# 	# 	self.ui.caltopoFolderComboBox.addItems(sorted(folderNames))
		# 	# 	self.ui.caltopoFolderComboBox.setCurrentIndex(0)

		self.caltopoFolderPopup.populate(accountId)
		self.caltopoFolderPopup.setFullLabel(self.caltopoFolderPopup.model.index(0,0))
		# self.ui.caltopoFolderButton.setText(self.caltopoFolderPopup.model.index(0,0).data())
		# self.pauseIDCB=True
		self.caltopoFolderChanged(self.caltopoFolderPopup.model.index(0,0).data(Qt.UserRole)) # folder ID stored in UserRole
		# self.pauseIDCB=False
		# self.getFolderTree(accountId)
		logging.info('acct.end')

	# def getFolderTree(self,accountId):
	# 	logging.info('get folder tree')
	# 	folderTree={}
	# 	# acctDict=[d for d in self.parent.caltopoMapListDicts if d['groupAccountTitle']==self.ui.caltopoAccountComboBox.currentText()][0]
	# 	acctFolders=[f for f in self.parent.cts.accountData['features'] if f['properties']['accountId']==accountId and f['properties']['class']=='UserFolder']
	# 	logging.info('acctFolders:')
	# 	logging.info(json.dumps(acctFolders,indent=3))

	# 	# def getChildFolders(id):
	# 	# 	return [f for f in acctFolders if f['properties']['folderId']==id]
		
	# 	# for folder in acctFolders:
	# 	# 	# parentId=folder['properties']['folderId']
	# 	# 	# this is expensive - it makes n^2 iterations where n is the total number of folders (at all levels) in the account
	# 	# 	#  but that's probably OK since it's not time-sensitive
	# 	# 	id=folder['id']
	# 	# 	children=[{
	# 	# 		'title':f['properties']['title'],
	# 	# 		'id':f['id']} for f in acctFolders if f['properties']['folderId']==id]
	# 	# 	folderTree.append({
	# 	# 		'title':folder['properties']['title'],
	# 	# 		'id':id,
	# 	# 		'children':children
	# 	# 	})
			
	# 	# for folder in acctFolders:
	# 	# 	# parentId=folder['properties']['folderId']
	# 	# 	# this is expensive - it makes n^2 iterations where n is the total number of folders (at all levels) in the account
	# 	# 	#  but that's probably OK since it's not time-sensitive
	# 	# 	id=folder['id']
	# 	# 	children=[{
	# 	# 		'title':f['properties']['title'],
	# 	# 		'id':f['id']} for f in acctFolders if f['properties']['folderId']==id]
	# 	# 	def buildFolderDict(f):
	# 	# 		children=[{
	# 	# 			'title':f['properties']['title'],
	# 	# 			'id':f['id']} for f in acctFolders if f['properties']['folderId']==id]

	# 	# 	d={
	# 	# 		'title':folder['properties']['title'],
	# 	# 		'id':id,
	# 	# 		'children':children
	# 	# 	}
		

	# 	logging.info(json.dumps(folderTree,indent=3))

	def caltopoFolderButtonUpdateText(self,txt):
		padding=10
		textWidth=self.fm.size(0,txt).width()
		buttonWidth=self.ui.caltopoFolderButton.width()
		# horizontalAdvance=self.parent.fm.horizontalAdvance(txt)
		# boundingWidth=self.parent.fm.boundingRect(txt).width()
		# print('new text width = '+str(textWidth)+'   horizontal advance = '+str(horizontalAdvance)+'   boundingRect width = '+str(boundingWidth)+'   button width = '+str(buttonWidth))
		txtForButton=txt
		self.ui.caltopoFolderButton.setToolTip('') # only show tooltip if button text is elided
		# original:   "L1longdirname > L2longdirname > L3longdirname"
		# first try:  "L1lo... > L2lo... > L3longdirname"
		# second try: "L1lo..> L2lo..> L3longdirname"
		# third try:  "L1..>L2..>L3longdirname"
		# fourth try: "...>L3longdirname" (omit the leading ...> if not nested)
		# after that, just start a standard right-elide until it fits: "L1..>L2..>L3lon..."
		# in all cases, the tooltop text should be the full original path
		if (textWidth+padding)>buttonWidth:
			# print('  too wide! elide!  full text = '+txt)
			names=txt.split(' > ')
			a1Names=[]
			a2Names=[]
			a3Names=[]
			for name in names[:-1]: # don't shorten the leaf name
				a1Name=name
				a2Name=name
				a3Name=name
				if len(name)>6:
					a1Name=name[0:4]+'...'
				if len(name)>5:
					a2Name=name[0:4]+'..'
				if len(name)>4:
					a3Name=name[0:2]+'..'
				a1Names.append(a1Name)
				a2Names.append(a2Name)
				a3Names.append(a3Name)
			a1Names.append(names[-1])
			a2Names.append(names[-1])
			a3Names.append(names[-1])
			attempt1=' > '.join(a1Names)
			attempt2='> '.join(a2Names)
			attempt3='>'.join(a3Names)
			attempt4=names[-1]
			if len(names)>1:
				attempt4='...>'+attempt4
			# print(f'attempt1: {attempt1}\nattempt2: {attempt2}\nattempt3: {attempt3}\nattempt4: {attempt4}')
			if self.fm.horizontalAdvance(attempt1)+padding<buttonWidth:
				txtForButton=attempt1
			elif self.fm.horizontalAdvance(attempt2)+padding<buttonWidth:
				txtForButton=attempt2
			elif self.fm.horizontalAdvance(attempt3)+padding<buttonWidth:
				txtForButton=attempt3
			else:
				txtForButton=attempt4
				textWidth=self.fm.size(0,txtForButton).width()
				while (textWidth+padding)>buttonWidth and len(txtForButton)>5:
					txtForButton=txtForButton[0:-3]+'..'
					textWidth=self.fm.size(0,txtForButton).width()
			self.ui.caltopoFolderButton.setToolTip(txt)
		self.ui.caltopoFolderButton.setText(txtForButton)

	def caltopoFolderChanged(self,folderId):
		if str(folderId)=='0':
			folderId=None
		logging.info('folder changed to "'+str(self.ui.caltopoFolderButton.text())+'":'+str(folderId)+' - rebuilding map name choices')
		# time.sleep(2)
		if self.pauseCB:
			logging.info(' fcbc: paused; returning')
			return
		self.pauseCB=True
		self.ui.caltopoMapNameComboBox.clear()
		dicts=[d for d in self.parent.caltopoMapListDicts if d['groupAccountTitle']==self.ui.caltopoAccountComboBox.currentText()]
		if dicts:
			mapList=dicts[0]['mapList']
			# logging.info(' fcbc mapList:')
			# logging.info(json.dumps(mapList,indent=3))
			# relsInFolder=[m for m in mapList if m['folderName']==(self.ui.caltopoFolderButton.text() or '<Top Level>')]
			relsInFolder=[m for m in mapList if m['folderId']==folderId]
			logging.info('relsInFolder:')
			jd(relsInFolder) # print first n lines of json
			# mapsNotBookmarks=[m for m in mapList if m['type']=='map' and m['folderName']==self.ui.caltopoFolderComboBox.currentText()]
			# logging.info(' fcbc: mapsNotBookmarks:')
			# logging.info(json.dumps(mapsNotBookmarks,indent=3))
			if relsInFolder:
				# self.ui.caltopoMapNameComboBox.addItems([m['title'] for m in mapsNotBookmarks])
				self.ui.caltopoMapNameComboBox.addItems(['<Choose Map>']+[r['title'] for r in relsInFolder])
				# self.ui.caltopoMapNameComboBox.addItems([r['title'] for r in relsInFolder])
				# select the most recent entry by default
				self.ui.caltopoMapNameComboBox.setCurrentIndex(1) # this line only runs for non-empty relsInFolder; no need for another 'if'
			# display bookmarks in italics
			for n in range(len(relsInFolder)):
				if relsInFolder[n]['type']=='bookmark':
					# offset by 1 to account for <Choose Map> being the first entry
					if relsInFolder[n]['permission']=='read':
						self.ui.caltopoMapNameComboBox.setItemData(n+1,self.caltopoItalicStrikeFont,Qt.FontRole)
					else:
						self.ui.caltopoMapNameComboBox.setItemData(n+1,self.caltopoItalicFont,Qt.FontRole)
				elif relsInFolder[n].get('locked'):
					logging.info('strike:'+str(n+1))
					self.ui.caltopoMapNameComboBox.setItemData(n+1,self.caltopoNormalStrikeFont,Qt.FontRole)
				# else:
				# 	self.ui.caltopoMapNameComboBox.setItemData(n+1,self.caltopoNormalFont,Qt.FontRole)

				# latestMap=mapsNotBookmarks[0]
				# logging.info('latest map: title="'+str(latestMap['title']+'" ID='+str(latestMap['id'])))
				# self.ui.caltopoMapNameField.setText(str(latestMap['title']))
				# self.ui.caltopoMapIDField.setText(str(latestMap['id']))
			# else:
			# 	self.ui.caltopoMapIDField.setText('')
			# 	self.ui.caltopoMapNameField.setText('Account has no maps')
		self.pauseCB=False
		self.caltopoMapNameComboBoxChanged() # call it once here to do a single update of mapID

	# this gets called when the highlight (the hovered item) changes
	# set the lineEdit text here; lineEdit font is then set during caltopoMapIDTextChanged (via caltopoMapNameComboBoxChanged)
	def caltopoMapNameComboBoxHighlightChanged(self,i):
		if self.isVisible():
			logging.info('name hover changed to '+str(i)+':"'+str(self.ui.caltopoMapNameComboBox.currentText())+'" : calling updateMapIDFieldFromTitle')
		# italic=False
		# strikeOut=False
		self.qle.setText(self.ui.caltopoMapNameComboBox.itemText(i))
		# itemFont=self.ui.caltopoMapNameComboBox.itemData(i,Qt.FontRole)
		# logging.info('  itemFont='+str(itemFont))
		# if itemFont:
		# 	italic=itemFont.italic()
		# 	strikeOut=itemFont.strikeOut()
		# 	logging.info('    itemFont is italic:'+str(itemFont.italic()))
		# 	logging.info('    itemFont is strikeout:'+str(itemFont.strikeOut()))
		# self.qle.setFont(itemFont or self.caltopoNormalFont)
		# self.qle.font().setItalic(italic)
		# self.qle.font().setStrikeOut(strikeOut)
		# self.ui.caltopoMapNameComboBox.lineEdit().setFont(self.caltopoItalicFont)
		self.caltopoMapNameComboBoxChanged() # now call the same callback as when a different item is clicked

	# this only gets called when a (different) item is clicked
	def caltopoMapNameComboBoxChanged(self):
		curr=self.ui.caltopoMapNameComboBox.currentText()
		if self.isVisible():
			logging.info('name changed to "'+str(curr)+'" : calling updateMapIDFieldFromTitle')
		if curr=='<Choose Map>': # force non-italic for placeholder selection
			self.qle.setFont(self.caltopoNormalFont)
		# time.sleep(2)
		if self.pauseCB:
			logging.info(' ncbc: pauseCB set; returning')
			return
		if self.pauseIDCB:
			logging.info(' ncbc: pauseIDCB set; returning')
			return
		self.caltopoUpdateMapIDFieldFromTitle(self.ui.caltopoMapNameComboBox.currentText())

	def caltopoUpdateMapIDFieldFromTitle(self,title):
		if self.isVisible():
			logging.info('update ID from title "'+str(title)+'"')
		# time.sleep(2)
		if self.pauseCB:
			logging.info(' uift: pauseCB set; returning')
			return
		if title=='<Choose Map>' and not self.pauseIDCB:
			self.pauseCB=True
			self.ui.caltopoMapIDField.setText('')
			self.pauseCB=False
			return
		dicts=[d for d in self.parent.caltopoMapListDicts if d['groupAccountTitle']==self.ui.caltopoAccountComboBox.currentText()]
		if dicts:
			mapList=dicts[0]['mapList']
			matches=[m for m in mapList if m['title']==title]
			if matches:
				self.ui.caltopoMapIDField.setText(matches[0]['id'])
				logging.info(' uift: match='+str(matches[0]['id']))
			else:
				self.ui.caltopoMapIDField.setText('')
				logging.info(' uift: no match; clearing id field')

	# def caltopoPrintTimer(self):
	# 	logging.info('caltopo timer')

	def caltopoOpenMapButtonClicked(self):
		logging.info('Open Map button clicked: caltopoLink='+str(self.parent.caltopoLink))
		if self.parent.caltopoLink==1: # mapless session
			if self.caltopoSelectionIsReadOnly:
				box=QMessageBox(QMessageBox.Warning,"Read-only map","The map or bookmark you selected is not writable.\n\nRadiolog can still open the map, but won't be able to write any data to it.\n\nOpen the map anyway?",
					QMessageBox.Yes|QMessageBox.Cancel,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
				box.show()
				box.raise_()
				if box.exec_()==QMessageBox.Cancel:
					box.close()
					return
			self.ui.caltopoOpenMapButton.setText('Opening...')
			self.parent.caltopoLink=3 # in transition
			self.caltopoUpdateGUI()
			# QCoreApplication.processEvents()
			# if self.ui.caltopoWebBrowserCheckBox.isChecked():
			# 	try:
			# 		logging.info('Opening map in web browser...')
			# 		webbrowser.open('https://caltopo.com/m/'+self.ui.caltopoMapIDField.text())
			# 	except Exception as e:
			# 		logging.info('Failed to open map in web browser: '+str(e))
		else: # 2 = map opened and connected
			self.ui.caltopoOpenMapButton.setText('Closing...')
			self.parent.caltopoLink=3 # in transition
			self.caltopoUpdateGUI()
			# QCoreApplication.processEvents()
			self.parent.closeCTS() # sets caltopoLink to 0
			self.caltopoUpdateGUI()
			self.caltopoEnabledCB() # mimic turning both checkboxes on, which gets account data etc.
			return
		# self.caltopoUpdateGUI()
		# self.ui.caltopoOpenMapButton.setEnabled(False)
		# QCoreApplication.processEvents()
		# # threading.Thread(target=self.wrapper).start()
		# self.caltopoConnectThread=QThread()
		# self.worker=CaltopoConnectWorker()
		# self.worker.moveToThread(self.caltopoConnectThread)
		# self.caltopoConnectThread.started.connect(self.worker._caltopoOpenMapButtonClickedThread)
		# self.worker.task_finished.connect(self._caltopoOpenMapButtonComplete)
		# self.caltopoConnectThread.start()
		# self.parent.fastTimer.timeout.connect(self.caltopoPrintTimer)

		# self.CaltopoWorker.moveToThread(self.CaltopoThread)

		self.parent.openMap()

		# if self.parent.cts.openMap(self.ui.caltopoMapIDField.text()):
		# 	self.parent.caltopoLink=2 # map opened and connected
		# 	self.parent.caltopoOpenMapIsWritable=not self.caltopoSelectionIsReadOnly
		# 	self.parent.caltopoUpdateLinkIndicator()
		# 	self.caltopoUpdateGUI()
		# 	# self.ui.caltopoOpenMapButton.setText('Map Opened - Click to Close Map')
		# 	# self.caltopoGroupFieldsSetEnabled(False) # disallow map field changes while connected
		# 	# self.ui.caltopoOpenMapButton.setEnabled(True)
		# 	# QCoreApplication.processEvents()
		# 	# self.parent.getOrCreateRadioMarkerFID() # call it now so that hopefully the folder exists before the first radio marker
		# 	# self.parent.caltopoProcessLatestMarkers() # add markers for any calls that were made before the map was opened
		# 	if self.parent.caltopoOpenMapIsWritable:
		# 		self.parent.radioMarkerEvent.set() # start _radioMarkerWorker to process any markers sent prior to map opening
		# else:
		# 	self.parent.caltopoLink=1
		# 	self.caltopoUpdateGUI()
		# 	logging.info('ERROR: could not open map '+str(self.ui.caltopoMapIDField.text()))

	# def wrapper(self):
	# 	self._caltopoOpenMapButtonClickedThread()
	# 	self._caltopoOpenMapButtonClickedComplete()

	# def _caltopoOpenMapButtonClickedThread(self):
	# 	logging.info('connect thread started')
	# 	u=self.ui.caltopoMapIDField.text()
	# 	if self.parent.caltopoLink!=0 and self.parent.cts and self.parent.cts.mapID:
	# 		logging.info('  disconnecting')
	# 		self.parent.closeCTS()
	# 		# need to open a new CTS as long as the group box is enabled
	# 		logging.info('  opening new mapless session')
	# 		self.parent.createCTS()
	# 		logging.info('  new mapless session opened')
	# 		# self.ui.caltopoOpenMapButton.setText('Click to Connect')
	# 		# self.ui.caltopoOpenMapButton.setEnabled(True)
	# 		# self._caltopoOpenMapButtonClickedCB()
	# 		return
	# 	# time.sleep(5) # test sleep to check responsiveness in main thread
	# 	if ':' in u and self.parent.caltopoAccountName=='NONE':
	# 		logging.info('ERROR: caltopoAccountName was not specified in config file')
	# 		# self._caltopoOpenMapButtonClickedCB()
	# 		return
	# 	# if u==self.parent.caltopoURL and self.parent.cts: # url has not changed; keep the existing link and folder list
	# 	# 	return
	# 	self.parent.caltopoURL=u
	# 	if self.parent.caltopoURL.endswith("#"): # pound sign at end of URL causes crash; brute force fix it here
	# 		self.parent.caltopoURL=self.parent.caltopoURL[:-1]
	# 		self.ui.caltopoMapIDField.setText(self.parent.caltopoURL)
	# 	parse=self.parent.caltopoURL.replace("http://","").replace("https://","").split("/")
	# 	if len(parse)>1:
	# 		domainAndPort=parse[0]
	# 		mapID=parse[-1]
	# 	else:
	# 		domainAndPort='caltopo.com'
	# 		mapID=parse[0]
	# 	# 	print("calling CaltopoSession with domainAndPort="+domainAndPort+" mapID="+mapID)
	# 	# 	if 'caltopo.com' in domainAndPort.lower():
	# 	# 		print("  creating online session for user "+self.caltopoAccountName)
	# 	# 		self.cts=CaltopoSession(domainAndPort=domainAndPort,mapID=mapID,
	# 	# 								configpath=os.path.join(self.configDir,'cts.ini'),
	# 	# 								# sync=False,syncTimeout=0.001,
	# 	# 								account=self.caltopoAccountName)
	# 	# 	else:
	# 	# 		self.cts=CaltopoSession(domainAndPort=domainAndPort,mapID=mapID)
	# 	# 		# self.cts=CaltopoSession(domainAndPort=domainAndPort,mapID=mapID,sync=False,syncTimeout=0.001)
	# 	self.parent.cts.openMap(mapID)
	# 	# self._caltopoOpenMapButtonClickedCB()

	# def _caltopoOpenMapButtonClickedComplete(self):
	# 	self.parent.caltopoLink=self.parent.cts.apiVersion
	# 	self.parent.fastTimer.timeout.disconnect(self.caltopoPrintTimer)
	# 	logging.info('connect thread complete; link status:'+str(self.parent.caltopoLink)+'; cts.mapID='+str(self.parent.cts.mapID))
	# 	self.parent.caltopoUpdateLinkIndicator()
	# 	# 	# self.updateLinkIndicator()
	# 	# 	# if self.link>0:
	# 	# 	# 	self.ui.linkIndicator.setText(self.cts.mapID)
	# 	# 	# 	self.updateFeatureList("Folder")
	# 	# 	# self.optionsDialog.ui.folderComboBox.setHeader("Select a Folder...")
	# 	# 	# if the session is good, process any deferred radio markers
	# 	if self.parent.cts and self.parent.caltopoLink>0 and self.parent.cts.mapID:
	# 		self.ui.caltopoOpenMapButton.setText('Click to Disconnect')
	# 		self.parent.radioMarkerFID=self.parent.getOrCreateRadioMarkerFID()
	# 		# add deferred markers (GPS calls that came in before CTS was created)
	# 		self.parent.sendQueuedRadioMarkers()
	# 	else:
	# 		self.ui.caltopoOpenMapButton.setText('Click to Connect')
	# 	self.ui.caltopoOpenMapButton.setEnabled(True)


# find dialog/completer/popup structure:
#  - the dialog holds the QLineEdit
#  - the completer contains the model (see QCompleter)
#  - the popup is the QListView of matches, so, is not always open

class customCompleterPopup(QListView):
	def __init__(self,parent=None):
		self.parent=parent
		super(customCompleterPopup,self).__init__(parent)
		self.resize(self.parent.width()-25,self.height())
		# self.setFocusPolicy(QtCore.Qt.NoFocus) # doesn't prevent jumping

	def selectionChanged(self,selected,deselected):
		# logging.info('selection changed in subclass')
		ind=selected.indexes()
		if len(selected)>0:
			self.parent.processChangedSelection(ind[0])
		else:
			self.parent.onExit()
		super(customCompleterPopup,self).selectionChanged(selected,deselected)


class findDialog(QWidget,Ui_findDialog):
	def __init__(self,parent):
		self.parent=parent
		QWidget.__init__(self,parent)
		self.ui=Ui_findDialog()
		self.ui.setupUi(self)
		self.setFixedSize(self.size())
		self.teamTabIndexBeforeFind=1
		self.ui.findField.textChanged.connect(self.updateCountLabel)

	def showEvent(self,e):
		logging.info('opening findDialog')
		self.teamTabIndexBeforeFind=self.parent.ui.tabWidget.currentIndex()
		self.theList=[entry[0]+' : '+entry[2]+' : '+entry[3] for entry in self.parent.radioLog]
		self.completer=QCompleter(self.theList)
		self.completer.setFilterMode(Qt.MatchContains)
		# performance speedups: see https://stackoverflow.com/questions/33447843
		self.completer.setCaseSensitivity(Qt.CaseInsensitive)
		self.completer.setModelSorting(QCompleter.CaseSensitivelySortedModel)
		self.customPopup=customCompleterPopup(self)
		self.completer.setPopup(self.customPopup)
		self.completer.popup().installEventFilter(self)
		self.completer.popup().setUniformItemSizes(True)
		self.completer.popup().setLayoutMode(QListView.Batched)
		self.completer.popup().setMouseTracking(True)
		self.completer.popup().entered.connect(self.mouseEnter)
		self.completer.popup().clicked.connect(self.clicked)
		# this doesn't fix the problem of arrow keys jumping to the hovered selection
		#  when scrollbar is visible - not sure what is causing that - but a larger
		#  value of maxVisibleItems does make it less likely that the user will
		#  ever see the problem
		self.completer.setMaxVisibleItems(30)
		self.ui.findField.setCompleter(self.completer)

	def mouseEnter(self,i):
		# select and highlight the hovered row in the popup:
		# logging.info('mouseEnter row '+str(i.row()))
		self.completer.popup().setCurrentIndex(i)
		self.processChangedSelection(i)

	def updateCountLabel(self,*args):
		count=self.completer.completionCount()
		i=self.customPopup.currentIndex().row() # initially -1 if no row is selected
		# Note that after the first time any popup row has been selected,
		#  moving up (from the first row) or down (from the last row) back to the QLineEdit field, such that no rows are selected,
		#  leaves the currentIndex().row() at the last selected row number, instead of going back to -1.
		# Maybe this is a PyQt bug?
		# Catch this case by comparing QLineEdit text to the currentIndex text;
		#  if it's a match, then the corresponding row of the popup is really selected;
		#  if it's not a match, then nothing is really selected.
		# logging.info('updateCountLabel: i='+str(i))
		# if i>0 or (i==0 and self.ui.findField.text()==self.completer.popup().currentIndex().data()): # works for up-from-first, but not for down-from-last
		if self.ui.findField.text()==self.completer.popup().currentIndex().data(): # works for up-from-first and for down-from-last
			prefix=str(i+1)+' of '
			suffix=''
		else:
			prefix=''
			suffix=' match'
			if count!=1:
				suffix+='es'
		self.ui.countLabel.setText(prefix+str(count)+suffix)

	def processChangedSelection(self,i):
		self.customPopup.resize(self.width()-25,self.customPopup.height())
		self.updateCountLabel()
		# select the correct row in the main tableView
		idx=self.theList.index(i.data())
		self.parent.ui.tableView.selectRow(idx)
		completerRowText=i.data()
		[entryTime,teamName,entryText]=completerRowText.split(' : ')[0:3]
		if teamName: # only if it's a valid team name
			extTeamName=getExtTeamName(teamName)
			tabIndex=self.parent.extTeamNameList.index(extTeamName)
			logging.info('mouse enter: findField="'+str(self.ui.findField.text())+'"  row '+str(idx)+' : '+str(i.data()))
			logging.info('  teamName='+str(teamName)+'  extTeamName='+str(extTeamName)+'  tabIndex='+str(tabIndex))

			# select the team tab, combined with more prominent :selected border in tabWidget styleSheet
			self.parent.ui.tabWidget.setCurrentIndex(tabIndex)

			# select and highlight the correct row in the team's tableView, based on time and text
			model=self.parent.ui.tableViewList[tabIndex].model()
			teamTableIndicesByTime=model.match(model.index(0,0),Qt.DisplayRole,entryTime,-1) # -1 = return all matches
			teamTableRowsByTime=[i.row() for i in teamTableIndicesByTime]
			logging.info('  match rows by time '+str(entryTime)+':'+str(teamTableRowsByTime))
			# if there is more than one entry from that team at that time, search for the right one based on text
			if len(teamTableIndicesByTime)>1:
				teamTableIndicesByText=model.match(model.index(0,3),Qt.DisplayRole,entryText,-1) # -1 = return all matches
				teamTableRowsByText=[i.row() for i in teamTableIndicesByText]
				logging.info('  match rows by text "'+str(entryText)+'":'+str(teamTableRowsByText))
				# select the row that is in both lists, in case the team has multiple entries with identical text
				commonIndices=[c for c in teamTableIndicesByText if c.row() in teamTableRowsByTime]
				if len(commonIndices)==0:
					logging.info('ERROR: there are no entries that match both the time and the text selected from the search result popup')
					return
				elif len(commonIndices)>1:
					logging.info('WARNING: there are multiple entries that match the time and text selected from the search result popup; selecting the first one')
				i=commonIndices[0]
			else:
				i=teamTableIndicesByTime[0]
			# logging.info('  match indices:'+str(teamTableIndices))
			# logging.info('  match rows:'+str([i.row() for i in teamTableIndices]))
			# logging.info('  first row:'+str(model.itemData(model.index(0,0))))
			self.parent.ui.tableViewList[tabIndex].selectRow(i.row())

	def closeEvent(self,e):
		# logging.info('  closeEvent')
		self.completer.popup().close()
		self.ui.findField.setText('')
		logging.info('closing findDialog')

	def onExit(self):
		# logging.info('    onExit')
		self.completer.popup().clearSelection()
		self.parent.ui.tableView.clearSelection()
		self.parent.ui.tableView.scrollToBottom()
		self.parent.ui.tabWidget.setCurrentIndex(self.teamTabIndexBeforeFind)
		if len(self.parent.ui.tableViewList)>1:
			self.parent.ui.tableViewList[self.teamTabIndexBeforeFind].clearSelection()
			self.parent.ui.tableViewList[self.teamTabIndexBeforeFind].scrollToBottom()

	def clicked(self,i):
		logging.info('clicked findDialog')
		self.close()

	def keyPressEvent(self,event):
		logging.info('findDialog keyPress event')
		key=event.key()
		if key in [Qt.Key_Enter,Qt.Key_Return]:
			logging.info('  enter/return pressed; closing, but keeping any selection and scroll settings')
			self.close()
		elif key==Qt.Key_Escape:
			logging.info('  esc pressed; closing, and clearing selection and scroll settings')
			self.onExit()
			self.close()
		self.customPopup.resize(self.width()-25,self.customPopup.height())

	def eventFilter(self,obj,e):
		t=e.type()
		self.lastEventType=t
		# logging.info('filtered event: '+str(t))
		if t==QEvent.KeyPress:
			# logging.info('keyPress event (completer popup)')
			key=e.key()
			# self.customPopup.clearFocus() # this causes the popup to close on every other keypress while typing a valid pattern
			if key in [Qt.Key_Enter,Qt.Key_Return]:
				# logging.info('  enter/return pressed; closing, but keeping any selection and scroll settings')
				self.close()
				return True
			elif key==Qt.Key_Escape:
				# logging.info('  esc pressed; closing, and clearing selection and scroll settings')
				self.onExit()
				self.close()
				return True
			else: # pass all other keystrokes including up/down to the parent for handling
				# self.completer.popup().setCurrentIndex(i) # doesn't fix jumping
				# self.processChangedSelection(self.customPopup.currentIndex()) # doesn't fix jumping
				# self.updateGeometry() # doesn't fix jumping
				return False
		elif t==QEvent.MouseMove:
			self.onExit()
			self.updateCountLabel()
			self.customPopup.resize(self.width()-25,self.customPopup.height())
			return True
		elif t==QEvent.Hide:
			# Hide is called for different reasons:
			# 1 - dialog and popup are being closed due to left-click or enter/return
			#     - KeyPress was the previous event
			#     - in this case, do not clear highlights or reset scrolls
			# 2 - dialog and popup are being closed due to esc
			#     - HideToParent was the previous event
			#     - in this case, clear highlights and reset scrolls by calling onExit
			# 3 - findField has been changed such that there is no longer a match
			#     - KeyPress was the previous event
			#     - in this case, clear highlights and reset scrolls by calling onExit
			# logging.info('  hide')
			if self.lastEventType==QEvent.HideToParent:
				self.onExit()
				self.close()
			self.updateCountLabel()
			self.customPopup.resize(self.width()-25,self.customPopup.height())
			return True
		else:
			self.customPopup.resize(self.width()-25,self.customPopup.height())
			return False


class printDialog(QDialog,Ui_printDialog):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.parent=parent
		self.ui=Ui_printDialog()
		self.ui.setupUi(self)
		self.setStyleSheet(globalStyleSheet)
		self.ui.opPeriodComboBox.addItem(str(self.parent.opPeriod))
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		self.setFixedSize(self.size())

	def showEvent(self,event):
		logging.info("show event called")
		logging.info("teamNameList:"+str(self.parent.teamNameList))
		logging.info("allTeamsList:"+str(self.parent.allTeamsList))
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
			logging.info("PRINT radio log")
			self.parent.printLog(opPeriod)
		if self.ui.teamRadioLogsField.isChecked():
			logging.info("PRINT team radio logs")
			self.parent.printTeamLogs(opPeriod)
		if self.ui.clueLogField.isChecked():
			logging.info("PRINT clue log")
# 			logging.info("  printDialog.accept.clueLog.trace1")
			self.parent.printClueLog(opPeriod)
# 			logging.info("  printDialog.accept.clueLog.trace2")
# 		logging.info("  printDialog.accept.end.trace1")
		super(printDialog,self).accept()
# 		logging.info("  printDialog.accept.end.trace2")

	def toggleShow(self):
		if self.isVisible():
			self.close()
		else:
			self.show()
			self.raise_()

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
		self.setStyleSheet(globalStyleSheet)
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
	
	def raiseWindowAndChildren(self):
		self.raise_()
		self.activateWindow()
		currentWidget=self.ui.tabWidget.currentWidget()
		try:
			if currentWidget.childDialogs:
				for childDialog in currentWidget.childDialogs:
					childDialog.raise_()
					childDialog.activateWindow()
					QTimer.singleShot(500,lambda:childDialog.throb())
		except:
			pass # fail gracefully if e.g. widget or child dialogs have been deleted

	def changeEvent(self,event):
		if event.type()==QEvent.ActivationChange:
			self.parent.activationChange()
				
	# prevent 'esc' from closing the newEntryWindow
	def keyPressEvent(self,event):
		if event.key()!=Qt.Key_Escape:
			QDialog.keyPressEvent(self,event)

	def tabChanged(self,throb=True):
##	def throb(self):
		tabCount=self.ui.tabWidget.count()
		currentIndex=self.ui.tabWidget.currentIndex()
# 		logging.info("tabCount="+str(tabCount)+" currentIndex="+str(currentIndex))
		if tabCount>2: # skip all this if 'NEWEST' and 'OLDEST' are the only tabs remaining
			if (tabCount-currentIndex)>1: # don't try to throb the 'OLDEST' label - it has no throb method
				currentWidget=self.ui.tabWidget.widget(currentIndex)
				if currentWidget.needsChangeCallsign:
					QTimer.singleShot(500,lambda:currentWidget.promptForCallsign())
				if throb:
					currentWidget.throb()
				#683 but also general timing: respect hold time of >active< widget,
				# rather than last-typed widget
				self.parent.currentEntryLastModAge=currentWidget.lastModAge

##	def activeTabMessageFieldFocus(self):
##		currentIndex=self.ui.tabWidget.currentIndex()
				self.ui.tabWidget.widget(currentIndex).ui.messageField.setFocus()

				#683 - raise any pending clue/subject dialog(s) related to this call to top;
				#  if there are none, raise the new entry window
				self.raiseWindowAndChildren()

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
		logging.info('newEntryWidget.addTab called: labelText='+str(labelText)+'  widget='+str(widget))
		if widget:
##			widget=newEntryWidget(self.parent) # newEntryWidget constructor calls this function
##			widget=QWidget()
##			self.ui.tabWidget.insertTab(1,widget,labelText)


			logging.info('inserting tab')
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
			#683 - this clause is now redundant with fsParse most of the time,
			# but it does need to be called here too for the first entry, to make sure the
			# active widget actually has a 'ui' element when focus is set in newEntryWidget.__init__
			if self.parent.currentEntryLastModAge>holdSec or self.ui.tabWidget.count()==3:
				self.ui.tabWidget.setCurrentWidget(widget)
				widget.ui.messageField.setFocus()
##			if not self.parent.entryHold:
##			if not hold:
##				self.ui.tabWidget.setCurrentIndex(1)
##				self.parent.entryHold=True

##			self.ui.tabWidget.setStyleSheet("QTabWidget::tab {background-color:lightgray;}")
		else: # this should be fallback dead code since addTab is always called with a widget:
			logging.info('widget was None in call to newEntryWidget.addTab; calling self.parent.openNewEntry')
			self.parent.openNewEntry()

##	def clearHold(self):
##		self.entryHold=False
##
##	def clearContinue(self):
##		self.entryContinue=False

	def removeTab(self,caller):
		# logging.info('removeTab called: caller='+str(caller))
		# determine the current index of the tab that owns the widget that called this function
		i=self.ui.tabWidget.indexOf(caller)
		# determine the number of tabs BEFORE removal of the tab in question
		count=self.ui.tabWidget.count()
		# logging.info('  tab count before removal:'+str(count))
# 		logging.info("removeTab: count="+str(count)+" i="+str(i))
		# remove that tab
		self.ui.tabWidget.removeTab(i)
		# activate the next tab upwards in the stack, if there is one
		if i>1:
			self.ui.tabWidget.setCurrentIndex(i-1)
		# otherwise, activate the tab at the bottom of the stack, if there is one
		elif i<count-3: # count-1 no longer exists; count-2="OLDEST"; count-3=bottom item of the stack
			self.ui.tabWidget.setCurrentIndex(count-3)

		if count<4: # hide the window (don't just lower - #504) if the stack is empty
			# logging.info("lowering: count="+str(count))
			self.setWindowFlags(self.windowFlags() & ~Qt.WindowStaysOnTopHint) # disable always on top
			self.hide()
			if self.parent.findDialog.isVisible():
				logging.info('restoring completer popup')
				self.parent.findDialog.completer.complete() # restore the completer popup if it was previously open
				self.parent.findDialog.ui.findField.setFocus()

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
				# logging.info("lastModAge:"+str(tab.lastModAge))
				# note the pause happens in newEntryWidget.updateTimer()
				#683 - don't pause timers, but do prevent auto-cleanup, if there are child dialog(s)
				if tab.ui.messageField.text()=="" and tab.lastModAge>60 and not tab.childDialogs:
					logging.info('  closing unused new entry widget for '+str(tab.ui.teamField.text())+' due to inactivity')
					tab.closeEvent(QEvent(QEvent.Close),accepted=False,force=True)
					# if this was the only message, and the pending-entry popup was shown, close the popup too
					remaining=len(newEntryWidget.instances)
					if remaining<1:
						self.parent.newEntryWindowHiddenPopup.close()
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

		logging.info('newEntryWidget __init__ called: formattedLocString='+str(formattedLocString)+' fleet='+str(fleet)+' dev='+str(dev)+' origLocString='+str(origLocString)+' amendFlag='+str(amendFlag)+' amendRow='+str(amendRow)+' isMostRecentForCallsign='+str(isMostRecentForCallsign))
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
		self.insideQuickText=False
		self.prevActionWasQuickText=False
		self.newCallsignFromCCD=None
		if fleet:
			self.originalCallsign=parent.getCallsign(fleet,dev)
		elif dev:
			self.originalCallsign=parent.getCallsign(dev)
		else:
			self.originalCallsign=None
		if amendFlag:
			row=parent.radioLog[amendRow]
			self.sec=row[6]
			self.formattedLocString=row[4]
##		newEntryDialog.newEntryDialogUsedPositionList[self.position]=True
		newEntryWidget.instances.append(self)
		self.ui.setupUi(self)

		blockerPalette=QPalette()
		blockerPalette.setColor(QPalette.Background,QColor(255,255,255))
		self.ui.groupBlocker.setPalette(blockerPalette)

		self.setStyleSheet(globalStyleSheet)

		# self.hideChangeCallsignGroup()
		# self.ui.changeCallsignGroupBox.setVisible(False)
		# self.ui.firstCallGroupBox.setVisible(False)

		self.changeCallsignGroupAnimation=QPropertyAnimation(self.ui.changeCallsignGroupBox,b'pos')
		self.changeCallsignGroupAnimation.setDuration(150)
		self.firstCallGroupAnimation=QPropertyAnimation(self.ui.firstCallGroupBox,b'pos')
		self.firstCallGroupAnimation.setDuration(150)

		self.callsignGroupBoxShown='init' # to force 'none' to hide the group boxes on this first call
		self.callsignGroupBoxesShowHide(show='none',animate=False)

		self.setAttribute(Qt.WA_DeleteOnClose) # so that closeEvent gets called when closed by GUI
		self.palette=QPalette()
		self.setAutoFillBackground(True)
		self.clueDialogOpen=False # only allow one clue dialog at a time per newEntryWidget
		self.subjectLocatedDialogOpen=False
		self.locatedKeywords=['located','found'] # define these separately because they also apply to 'subject located'
		self.clueKeywords=self.locatedKeywords+['clue','interview'] # keywords that trigger the 'looks like a clue' popup
		self.cluePopupShown=False
		self.interviewPopupShown=False

		self.completer=QCompleter(self.parent.callsignCompletionWordList)
		# performance speedups: see https://stackoverflow.com/questions/33447843
		self.completer.setCaseSensitivity(Qt.CaseInsensitive)
		self.completer.setModelSorting(QCompleter.CaseSensitivelySortedModel)
		self.completer.popup().setUniformItemSizes(True)
		self.completer.popup().setLayoutMode(QListView.Batched)
		completerFont=self.ui.teamField.font()
		completerFont.setPointSize(int(completerFont.pointSize()*0.60))
		completerFont.setBold(False)
		self.completer.popup().setFont(completerFont)
		self.ui.teamField.setCompleter(self.completer)

# 		logging.info(" new entry widget opened.  allteamslist:"+str(self.parent.allTeamsList))
		if len(self.parent.allTeamsList)<2:
			self.ui.teamComboBox.setEnabled(False)
		else:
			self.ui.teamComboBox.clear()
			for team in self.parent.allTeamsList:
				if team!='dummy':
					self.ui.teamComboBox.addItem(team)
		
##		# close and accept the dialog as a new entry if message is no user input for 30 seconds

##		QTimer.singleShot(100,lambda:self.changeBackgroundColor(0))

# 		logging.info("newEntryWidget created")
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

		#683 - note that radioLocField.textChanged will also trigger on each new
		# fs/nx call (from fsParse), even if there is no radio GPS data; is this appropriate?
		self.ui.teamField.textChanged.connect(self.resetLastModAge)
		self.ui.messageField.textChanged.connect(self.resetLastModAge)
		# 753 - don't reset lastModAge whn radioLocField is changed; see 683 comment above
		# self.ui.radioLocField.textChanged.connect(self.resetLastModAge)
		self.ui.statusButtonGroup.buttonClicked.connect(self.resetLastModAge)

		self.lastModAge=0

		# add this newEntryWidget as a new tab in the newEntryWindow.ui.tabWidget
		self.parent.newEntryWindow.addTab(time.strftime("%H%M"),self)
		# do not raise the window if there is an active clue report form
# 		logging.info("clueLog.openDialogCount="+str(clueDialog.openDialogCount))
# 		logging.info("subjectLocatedDialog.openDialogCount="+str(subjectLocatedDialog.openDialogCount))
# 		logging.info("showing")
		if not self.parent.newEntryWindow.isVisible():
			self.parent.newEntryWindow.show()
# 		self.parent.newEntryWindow.setFocus()
		if clueDialog.openDialogCount==0 and subjectLocatedDialog.openDialogCount==0:
# 			logging.info("raising")
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
##		logging.info("ctrl+z keyBindings:"+str(QKeySequence("Ctrl+Z")))

##		# install actions for messageField
##		for entry in quickTextList:
##			if entry != "separator":
##				logging.info("adding:"+entry[0]+" "+str(entry[1]))
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
##		logging.info("quickText:"+quickText)

##	def changeEvent(self,event):
##		self.throb(0)

	def customFocusOutEvent(self,widget):
		if widget.objectName()=='teamField':
			# self.ui.changeCallsignGroupBox.setVisible(False)
			self.callsignGroupBoxesShowHide(show='none')
			# self.ui.firstCallGroupBox.setVisible(False)
			# but not when the slider is clicked - assured by setting slider focus policy to NoFocus
			self.ui.teamField.setToolTip('Type a callsign, or, choose from existing callsigns') # reset after customFocusInEvent
		elif 'interview' in widget.toPlainText().lower():
			self.parent.showInterviewPopup(widget)

	def customFocusInEvent(self,widget):
		# logging.info('focus in to widget '+str(widget.objectName()))
		if widget.objectName()=='teamField':
			# self.callsignGroupBoxesShowHide(show='changeCallsign')
			self.teamFieldTextChanged()
			self.ui.teamField.setToolTip('') # tooltip gets in the way when field is focused

	def throb(self,n=0):
		# this function calls itself recursivly 25 times to throb the background blue->white
# 		logging.info("throb:n="+str(n))
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
# 			logging.info("throb complete")
			self.throbTimer=None
			self.palette.setColor(QPalette.Background,QColor(255,255,255))
			self.setPalette(self.palette)

	def updateTimer(self):
		# # pause all timers if there are any clue or subject or changeCallsign dialogs open
		# if clueDialog.openDialogCount==0 and subjectLocatedDialog.openDialogCount==0:
		# 	self.lastModAge+=1
		#683 - don't pause timers, but do prevent auto-cleanup, if there are child dialog(s)
		self.lastModAge+=1
		#683 - only increment currentEntryLastModAge if this is actually the current entry
		if self.parent.newEntryWindow.ui.tabWidget.currentWidget()==self:
			self.parent.currentEntryLastModAge=self.lastModAge
		# logging.info('currentEntryLastModAge='+str(self.parent.currentEntryLastModAge))
##		if self.lastModAge>holdSec:
##			if self.entryHold: # each entry widget has its own lastModAge and its last entryHold
##				logging.info("releasing entry hold for self")
##				self.parent.entryHold=False

	def resetLastModAge(self):
		# logging.info("resetting last mod age for "+self.ui.teamField.text())
		self.lastModAge=-1
		self.parent.currentEntryLastModAge=self.lastModAge

	def quickTextAction(self):
		quickText=self.sender().text()
		self.insideQuickText=True
# 		logging.info("  quickTextAction called: text="+str(quickText))
		quickText=re.sub(r' +\[.*$','',quickText) # prune one or more spaces followed by open bracket, thru end
		existingText=self.ui.messageField.text()
		if existingText=="":
			self.quickTextAddedStack.append(quickText)
			self.ui.messageField.setText(quickText)
		else:
			textToAdd=quickText
			# if existing text already ends in a delimiter (possibly followed by one or more spaces), don't add another
			if re.match('.*[;,] *$',existingText):
				# if it does end in a space (after comma or semicolon), don't add any padding
				if existingText[-1]!=' ':
					textToAdd=' '+quickText
			else:
				textToAdd='; '+quickText
			self.quickTextAddedStack.append(textToAdd)
			self.ui.messageField.setText(existingText+textToAdd)
		self.ui.messageField.setFocus()
		self.insideQuickText=False

	def quickTextUndo(self):
		logging.info("ctrl+z keyBindings:"+str(QKeySequence("Ctrl+Z")))
		if len(self.quickTextAddedStack):
			textToRemove=self.quickTextAddedStack.pop()
			existingText=self.ui.messageField.text()
			self.ui.messageField.setText(rreplace(existingText,textToRemove,'',1))
			self.ui.messageField.setFocus()

	def quickTextClueAction(self): # do not push clues on the quick text stack, to make sure they can't be undone
		logging.info(str(self.clueDialogOpen))
		if not self.clueDialogOpen: # only allow one open clue diolog at a time per radio log entry; see init and clueDialog init and closeEvent
			self.newClueDialog=clueDialog(self,self.ui.timeField.text(),self.ui.teamField.text(),self.ui.radioLocField.toPlainText(),str(self.parent.getLastClueNumber()+1))
			self.newClueDialog.show()

	def quickTextSubjectLocatedAction(self,prefixText='',automatic=False):
		self.subjectLocatedDialog=subjectLocatedDialog(self,self.ui.timeField.text(),self.ui.teamField.text(),self.ui.radioLocField.toPlainText(),prefixText=prefixText,automatic=automatic)
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
			logging.info('esc pressed')
			# need to force focus away from callsignField so that
			#  callsignLostFocus gets called, to keep callsign and tab name in sync,
			#  otherwise this will cause a crash (hitting the cancel button does
			#  not cause a crash because the button takes focus before closing)
			# change logic: when esc is pressed while teamField has focus, don't try to close the dialog;
			#  just set focus to the message field
			if self.ui.teamField.hasFocus():
			# if self.ui.teamField.hasFocus() and self.originalCallsign and self.ui.teamField.text()!=self.originalCallsign:
				if self.originalCallsign and self.ui.teamField.text()!=self.originalCallsign:
					self.ui.teamField.setText(self.originalCallsign)
					# self.ui.changeCallsignGroupBox.setVisible(False)
					# self.ui.firstCallGroupBox.setVisible(False)
				self.ui.messageField.setFocus() # leavving focus in teamField after pressing Esc isn't helpful
			else:
				self.ui.messageField.setFocus()
				self.close()
		elif key==Qt.Key_Space and event.modifiers()==Qt.ControlModifier:
			if self.ui.teamField.hasFocus() and self.originalCallsign and self.ui.teamField.text()!=self.originalCallsign:
				self.changeCallsignSliderToggle()
		else:
			super().keyPressEvent(event) # pass the event as normal

	def promptForCallsign(self):
		logging.info('promptForCallsign called')
		# self.needsChangeCallsign=False
		# self.ui.changeCallsignSlider.setValue(0) # enforce the default every time the slider group is opened
		# self.ui.changeCallsignGroupBox.setVisible(False)
		deviceStr=str(self.fleet)+':'+str(self.dev)
		if self.fleet is None:
			deviceStr='NDXN:'+str(self.dev)
		self.ui.firstCallLabel1.setText('This is the first call from device '+deviceStr+'.')
		# self.ui.firstCallGroupBox.setVisible(True)
		self.callsignGroupBoxesShowHide(show='firstCall')
		self.ui.teamField.setText('Team ')
		self.ui.teamField.setFocus()
		self.ui.teamField.setSelection(5,1)

	def accept(self):
		if not self.clueDialogOpen and not self.subjectLocatedDialogOpen:
			# getValues return value: [time,to_from,team,message,self.formattedLocString,status,self.sec,self.fleet,self.dev,self.origLocString]
			logging.info("Accepted")
			val=self.getValues()

			#479 - improve validation
			# If 'not allowed' is in the message text, do not accept the entry and prompt the user to fix the problem;
			#  otherwise, ask the user whether they want to accept the callsign as entered, or if they want to revise it.
			cs=val[2]
			cse=getExtTeamName(cs)
			msg=''
			if cs=='':
				msg='Empty callsign field is not allowed.'
			elif cs.replace(' ','').lower()=='team':
				msg='Callsign "Team" without any other name or number is not allowed.'
			elif cs.replace('.','').replace('-','').isdigit() and cse not in self.parent.extTeamNameList:
				msg='Callsign appears to be only a number, with no words or letters.'
			if msg:
				if 'not allowed' in msg:
					box=QMessageBox(QMessageBox.Critical,"Callsign error","Invalid callsign.  Please change the callsign and try again:\n\n"+msg,
						QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
					box.show()
					box.raise_()
					box.exec_()
					return
				else:
					box=QMessageBox(QMessageBox.Warning,"Callsign warning","The specified callsign looks odd:\n\n"+msg+'\n\nDo you want to keep the callsign, or change it?',
						QMessageBox.Yes|QMessageBox.No,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
					box.button(QMessageBox.Yes).setText('Keep callsign as-is')
					box.button(QMessageBox.No).setText('Modify callsign')
					box.show()
					box.raise_()
					if box.exec_()==QMessageBox.No:
						return

			#752 - add a note if there is significant time difference between dialog open time and message accept time
			# logging.info('val[0]='+str(val[0]))
			nowHHMM=time.strftime('%H%M')
			# logging.info('now:'+nowHHMM)
			prefix=''
			if val[0].isdigit() and nowHHMM.isdigit() and len(val[0])==4 and len(nowHHMM)==4:
				timeDiff=(int(nowHHMM[0:2])-int(val[0][0:2]))*60+(int(nowHHMM[2:])-int(val[0][2:]))
				# logging.info('timeDiff:'+str(timeDiff))
				if timeDiff>5:
					prefix='[DELAYED MESSAGE saved at '+nowHHMM+', more than five minutes after it began at '+val[0]+'] '
				elif timeDiff>1:
					prefix='[DELAYED MESSAGE saved at '+nowHHMM+', more than a minute after it began at '+val[0]+'] '

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
						logging.info("number of entries for the previous team:"+str(prevEntryCount))
						if prevEntryCount==1:
							prevExtTeamName=getExtTeamName(prevTeam)
							self.parent.deleteTeamTab(prevExtTeamName,ext=True) #478: add ext=True
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
				val=self.getValues()
				val[3]=prefix+val[3]
				# make note of callsign change, if the previous callsign already has any saved entries
				#  (that check must be done here instead of in the CCD, in case of repeated CCD calls);
				#  was the change made from CCD (change-and-remember), or typed in (one-time)?
				# logging.info('t1: val[2]='+str(val[2])+'  orig='+str(self.originalCallsign)+'  allTeamsList='+str(self.parent.allTeamsList)+'  teamNameList='+str(self.parent.teamNameList))
				if val[2]!=self.originalCallsign and self.originalCallsign in self.parent.allTeamsList:
					deviceStr=str(self.fleet)+':'+str(self.dev)
					if self.fleet is None:
						deviceStr='NDXN:'+str(self.dev)
					appendText='   [CALLSIGN CHANGE: THIS CALL IS FROM DEVICE '+deviceStr+', previously "'+str(self.originalCallsign)+'"'
					if self.newCallsignFromCCD:
						# but maybe a different callsign was typed, after CCD was accepted
						if str(self.newCallsignFromCCD)==val[2]:
							appendText+='; new callsign association remembered for future calls]'
						else:
							appendText+='; new callsign association was set to "'+str(self.newCallsignFromCCD)+'", but then changed to "'+str(val[2])+'" for this message only]'
					else:
						appendText+='; this was a one-time callsign change for this message only]'
					val[3]=val[3]+appendText
					# inside this clause, i.e. if there are existing entries from the original callsign, save an entry with that original callsign noting the callsign change for this device
					oldCallsignEntry=val[:]
					oldCallsignEntry[2]=self.originalCallsign
					oldCallsignEntry[3]='[CALLSIGN CHANGE: call received from device '+deviceStr
					if self.newCallsignFromCCD:
						# but maybe a different callsign was typed, after CCD was accepted
						if str(self.newCallsignFromCCD)==val[2]:
							oldCallsignEntry[3]+=', previously associated with this callsign, but now associated with callsign "'+str(val[2])+'"; see concurrent message from that callsign]'
						else:
							oldCallsignEntry[3]+=', previously associated with this callsign, but now associated with callsign "'+str(self.newCallsignFromCCD)+'"; used as a one-time callsign change for a new entry from "'+str(val[2])+'"; see concurrent message from "'+str(val[2])+'"]'
					else:
						oldCallsignEntry[3]+=', still associated with this callsign, but used in a one-time callsign change for "'+str(val[2])+'"; see concurrent message from that callsign]'
					self.parent.newEntry(oldCallsignEntry)
				# unhiding=cse in self.hiddenCallsignList
				# logging.info('hiddenCallsignList='+str(self.hiddenCallsignList)+'  unhiding='+str(unhiding))
				# self.parent.newEntry(val,self.amendFlag,unhiding=unhiding)
				self.parent.newEntry(val,self.amendFlag)
	
			# make entries for attached callsigns
			# values array format: [time,to_from,team,message,locString,status,sec,fleet,dev]
# 			logging.info("attached callsigns: "+str(self.attachedCallsignList))
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
			logging.info("Accepted2")
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
# 		logging.info("closeEvent called: accepted="+str(accepted))
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
			warn.show()
			warn.raise_()
			#642 - to make sure the operator sees the child, move it to a location roughly centered on the warning message box
			# warnPos=self.mapToGlobal(warn.pos())
			warnPos=warn.pos()
			warnX=warnPos.x()
			warnY=warnPos.y()
			warnW=warn.width()
			warnH=warn.height()
			warnCenterX=int(warnX+(warnW/2))
			warnCenterY=int(warnY+(warnH/2))
			warn.exec_() # make sure it's modal; raise and center children after the message box is closed
			for child in self.childDialogs:
				child.show()
				logging.info('  activating child1')
				child.activateWindow()
				child.raise_() # don't call setFocus on the child - that steals focus from the child's first widget
				#center on the warning message box, then adjust size in case it was moved from a different-resolution screen
				childW=child.width()
				childH=child.height()
				child.move(int(warnCenterX-(childW/2)),int(warnCenterY-(childH/2)))
				child.adjustSize() # in case it was moved to a different-resolution screen
				child.throb()
			event.ignore()
			return
		else:
			# logging.info('newEntryWidget.closeEvent t3')
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
		flag=bool(self.dev and self.ui.teamField.text()!=self.originalCallsign) # dev could be None, so, convert to False
		logging.info('team field text changed: change needed = '+str(flag))
		self.needsChangeCallsign=flag
		if flag:
			uid=None
			if self.fleet and self.dev: # fleetsync
				deviceStr=str(self.fleet)+':'+str(self.dev)
			elif self.dev:
				deviceStr=str(self.dev)
			else:
				deviceStr='N/A'
			self.ui.changeCallsignLabel3.setText('Was: '+self.originalCallsign+'   [Device: '+deviceStr+']')
			self.ui.changeCallsignSlider.setValue(0) # enforce the default every time the slider group is opened
			if self.callsignGroupBoxShown=='firstCall':
				self.ui.teamField.setStyleSheet('border:3px inset green;')
			else:
				self.ui.teamField.setStyleSheet('border:3px inset blue;')
		else:
			self.ui.teamField.setStyleSheet('border:3px inset gray;')
		# self.ui.changeCallsignGroupBox.setVisible(flag)
		# self.callsignGroupBoxesShowHide(show='changeCallsign')
		if flag and self.callsignGroupBoxShown=='none':
			self.callsignGroupBoxesShowHide(show='changeCallsign')
		if not flag and self.callsignGroupBoxShown=='changeCallsign':
			self.callsignGroupBoxesShowHide(show='none')

	def teamFieldEditingFinished(self):
		cs=re.sub(r' +',r' ',self.ui.teamField.text()).strip() # remove leading and trailing spaces, and reduce chains of spaces to single space
		# logging.info('teamFieldEditingFinished: cs="'+cs+'"')
		if cs=='Team': # probably because a different tab on the stack was activated before a callsign was typed
			return
		if not cs in self.parent.allTeamsList: # if not already an exact case-sensitive match for an existing callsign:
			if re.match(r'.*\D.*',cs): # if there are any characters that are not numbers
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
			logging.info("relay callsign detected")
			# if the relay callsign is already in the callsign list, i.e. if
			#  they have previously called in, then assume they are relaying
			#  a message; if not, assume they are not yet relaying a message
			for t in self.parent.allTeamsList:
				if t.upper()==cs.upper():
					self.ui.relayedCheckBox.setChecked(True)
					self.ui.relayedByComboBox.setCurrentText(t)
					break
		if self.needsChangeCallsign:
			cs=re.sub(r' +',r' ',self.ui.teamField.text()).strip()
			uid=None
			if not self.fleet:
				uid=self.dev
			self.parent.sendRadioMarker(self.fleet,self.dev,uid,cs) # update label; use previous location
			if self.ui.changeCallsignSlider.value()==0:
				self.changeCallsign()
				self.originalCallsign=self.ui.teamField.text()
		# self.ui.changeCallsignGroupBox.setVisible(False)
		self.callsignGroupBoxesShowHide(show='none')
		# self.ui.firstCallGroupBox.setVisible(False)

	# reveal a group box, or hide both group boxes
	def callsignGroupBoxesShowHide(self,show='none',animate=True):
		logging.info('showHide called: show='+str(show)+'  animate='+str(animate))
		if show!=self.callsignGroupBoxShown:
			ccx=self.ui.changeCallsignGroupBox.x()
			fcx=self.ui.firstCallGroupBox.x()
			ccgh=self.ui.changeCallsignGroupBox.height()
			fcgh=self.ui.firstCallGroupBox.height()
			tfBot=self.ui.teamField.y()+self.ui.teamField.height()
			changeCallsignGroupBoxShownPos=QPoint(ccx,tfBot-3)
			changeCallsignGroupBoxHiddenPos=QPoint(ccx,tfBot-ccgh)
			firstCallGroupBoxShownPos=QPoint(fcx,tfBot-3)
			firstCallGroupBoxHiddenPos=QPoint(fcx,tfBot-fcgh)
			# if self.ui.changeCallsignGroupBox.pos().y()>-100:
			# if not self.changeCallsignGroupBoxIsShown:
			duration=150
			if not animate:
				duration=0
			self.changeCallsignGroupAnimation.setDuration(duration)
			self.firstCallGroupAnimation.setDuration(duration)
			if show=='changeCallsign':
				self.changeCallsignGroupAnimation.setEndValue(changeCallsignGroupBoxShownPos)
				self.changeCallsignGroupAnimation.start()
			elif show=='firstCall':
				self.firstCallGroupAnimation.setEndValue(firstCallGroupBoxShownPos)
				self.firstCallGroupAnimation.start()
			else:
				self.changeCallsignGroupAnimation.setEndValue(changeCallsignGroupBoxHiddenPos)
				self.firstCallGroupAnimation.setEndValue(firstCallGroupBoxHiddenPos)
				self.changeCallsignGroupAnimation.start()
				self.firstCallGroupAnimation.start()
			self.callsignGroupBoxShown=show

	def changeCallsignSliderToggle(self):
		val=self.ui.changeCallsignSlider.value()
		self.ui.changeCallsignSlider.setValue((val+1)%2) # invert: 1->0 and 0->1

	def changeCallsignSliderChanged(self):
		val=self.ui.changeCallsignSlider.value()
		logging.info('changeCallsignSlider changed: current value = '+str(val))
		self.ui.changeCallsignLabel1.setEnabled(val==0)
		self.ui.changeCallsignLabel2.setEnabled(val==1)
		self.resetLastModAge()

	# changeCallsign originally ported from changeCallsignDialog.accept
	def changeCallsign(self):
		logging.info('changeCallsign called')
		found=False
		uid=None
		if self.fleet and self.dev: # fleetsync
			deviceStr=str(self.fleet)+':'+str(self.dev)
			logging.info('accept: FleetSync fleet='+str(self.fleet)+'  dev='+str(self.dev))
		elif self.dev:
			uid=self.dev
			deviceStr=str(uid)
			logging.info('accept: NEXEDGE uid='+str(uid))
		# fix #459 (and other places in the code): remove all leading and trailing spaces, and change all chains of spaces to one space
		newCallsign=re.sub(r' +',r' ',self.ui.teamField.text()).strip()
		logging.info(f'changeCallsign for device "{deviceStr}": new callsign:{newCallsign}')
		# change existing device entry if found, otherwise add a new entry
		for n in range(len(self.parent.fsLookup)):
			entry=self.parent.fsLookup[n]
			if (entry[0]==self.fleet and entry[1]==self.dev) or (entry[1]==uid):
				found=True
				self.parent.fsLookup[n][2]=newCallsign
		if not found:
			if self.fleet and self.dev: # fleetsync
				self.parent.fsLookup.append([self.fleet,self.dev,newCallsign])
			else: # nexedge
				self.parent.fsLookup.append(['',uid,newCallsign])
		# logging.info('fsLookup after CCD:'+str(self.parent.parent.fsLookup))
		# set the current radio log entry teamField also
		# self.parent.ui.teamField.setText(newCallsign)
		# save the updated table (filename is set at the same times that csvFilename is set)
		self.parent.fsSaveLookup()
		# change the callsign in fsLog
		if self.fleet: # fleetsync
			# logging.info('calling fsLogUpdate for fleetsync')
			self.parent.fsLogUpdate(fleet=self.fleet,dev=self.dev,callsign=newCallsign,seq=['CCD'],result='newCallsign')
			logging.info("New callsign pairing created from FleetSync: fleet="+self.fleet+"  dev="+self.dev+"  callsign="+newCallsign)
		else: # nexedge
			# logging.info('calling fsLogUpdate for nexedge')
			self.parent.fsLogUpdate(uid=uid,callsign=newCallsign,seq=['CCD'],result='newCallsign')
			logging.info("New callsign pairing created from NEXEDGE: unit ID = "+uid+"  callsign="+newCallsign)
		# finally, pass the 'accept' signal on up the tree as usual
		# set the focus to the messageField of the active stack item - not always
		#  the same as the new entry, as determined by addTab
		# self.parent.ui.tabWidget.currentWidget().ui.messageField.setFocus()
		# 751 - set a flag on the parent newEntryWindow to indicate CCD was used, and what the new value is;
		#  let the newEntryWindow.accept create the change-of-callsign note as needed; in this way,
		#  repeated or superceded calls to CCD can be recorded in the note
		self.newCallsignFromCCD=newCallsign
		# logging.info("New callsign pairing created: fleet="+str(self.fleet)+"  dev="+str(self.dev)+"  uid="+str(uid)+"  callsign="+newCallsign)
		self.needsChangeCallsign=False
		self.ui.teamField.setStyleSheet('border:3px inset gray;')

	def setRelayedPrefix(self,relayedBy=None):
		if relayedBy is None:
			relayedBy=self.ui.relayedByComboBox.currentText()
# 		logging.info("setRelayedPrefix:"+relayedBy)
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
# 			logging.info("before relayed prefix removal:"+mt)
			mt=mt.replace(mt[:relayedEndIndex+2],"")
# 			logging.info("after relayed prefix removal:"+mt)
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
		logging.info("relayedCheckBoxStateChanged; fleet="+str(self.fleet)+"; dev="+str(self.dev))
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
	# 			logging.info("relayed")
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
	# 			logging.info("not relayed")
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
		logging.info("relayedByComboBoxChanged")
		self.relayedBy=self.ui.relayedByComboBox.currentText()
		self.setRelayedPrefix(self.relayedBy)
		self.ui.messageField.setFocus()
			
	def messageTextChanged(self): # gets called after every keystroke or button press, so, should be fast
##		self.timer.start(newEntryDialogTimeoutSeconds*1000) # reset the timeout
		#506 - if the most recent thing entered was a quick text, insert a space before the new typed alphanumeric
		# quick text followed by alphanumeric: add space before new typed character
		# quick text followed by quick text: add semicolon and space before new quick text (done in quickTextAction)
		# alphanumeric followed by alphanumeric: don't add anything
		# alphanumeric followed by quick text: add semicolon and space before new quick text (done in quickTextAction)
		# logging.info('messageTextChanged: insideQuickText='+str(self.insideQuickText)+'  prevActionWasQuickText='+str(self.prevActionWasQuickText))
		# logging.info('messageTextChanged: lastKeyText="'+self.ui.messageField.lastKeyText+'"')
		if self.ui.messageField.lastKeyText.isalpha() and self.prevActionWasQuickText and not self.insideQuickText:
			# # logging.info('  the previous action was a quick text but the current action is not - adding a space')
			prev=self.ui.messageField.text()
			self.prevActionWasQuickText=self.insideQuickText # avoid recursion loop
			self.ui.messageField.setText(prev[:-1]+' '+prev[-1])
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
		elif "completed assignment" in message:
			newStatus=""
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
		
		#577 #578 - check for text that looks like a clue or interview, and show popup as needed
		#642 - don't show the popup if subject located dialog is open

		#676 - 'found/located subject', 'subject [name] found/located' are unambiguous: open the subject located dialog immediately
		if 'subject' in message and not self.subjectLocatedDialogOpen:
			for keyword in self.locatedKeywords:
				if keyword in message:
					# if self.cluePopupShown:
					# 	self.cluePopup.reject()
					try:
						self.cluePopup.reject() # will cause exception if it's not yet defined
					except:
						pass
					QTimer.singleShot(100,QApplication.beep)
					QTimer.singleShot(400,QApplication.beep)
					QTimer.singleShot(700,QApplication.beep)
					self.quickTextSubjectLocatedAction(prefixText=message,automatic=True)
					msg='[SUBJECT LOCATED form opened automatically, based on words previously typed by the operator: "'+message+'"]'
					self.subjectLocatedDialog.ui.otherField.setPlainText(msg)
					logging.info(msg)
					self.ui.messageField.setText('')
					break

		if not self.cluePopupShown and not self.subjectLocatedDialogOpen:
			msg=None
			for keyword in self.clueKeywords:
				if keyword in message:
					msg='Since you typed "'+keyword+'", it looks like you meant to click "LOCATED A CLUE".\n\nDo you want to open a clue report now?\n\n(If so, click \'Yes\' or press Shift-Enter or Ctrl-Enter, and everything typed so far will be copied to the Clue Description field.)\n\n(If not, click \'No\' or press the \'Escape\' key to close this popup and continue the message.)\n\n(If you also type \'subject\', the Subject Located form will open automatically.)'
			if msg:
				logging.info('"Looks like a clue" popup shown; message so far: "'+message+'"')
				self.cluePopup=CustomMessageBox(QMessageBox.Information,"Looks like a clue",msg,
					QMessageBox.Yes|QMessageBox.No,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
				# the two lines below are needed to prevent space bar from triggering the 'Yes' button (opening a clue dialog)
				#  or the 'No' button (closing the popup)
				self.cluePopup.button(QMessageBox.Yes).setFocusPolicy(Qt.NoFocus)
				self.cluePopup.button(QMessageBox.No).setFocusPolicy(Qt.NoFocus)
				self.cluePopup.show()
				messageFieldTopLeft=self.mapToGlobal(self.ui.messageField.pos())
				messageFieldHeight=self.ui.messageField.height()
				boxX=messageFieldTopLeft.x()+10
				boxY=messageFieldTopLeft.y()+messageFieldHeight+10
				self.cluePopup.move(boxX,boxY)
				self.cluePopup.raise_()
				self.cluePopupShown=True
				QTimer.singleShot(100,QApplication.beep)
				QTimer.singleShot(400,QApplication.beep)
				QTimer.singleShot(700,QApplication.beep)
				rval=self.cluePopup.exec_()
				logging.info('rval:'+str(rval))
				if rval in [1,QMessageBox.Yes]: # 1 is returned on accept from keyPressEvent
					logging.info('"Looks like a clue" popup accepted: opening the clue dialog')
					self.quickTextClueAction()
					#642 - to make sure the operator sees the clue dialog, move it to the same location
					#  as the 'looks like a clue' popup (hardcode to 50px above and left, no less than 10,10)
					# moving from a high-res screen to a low-res screen can result in a too-small dialog;
					#  address this by setting to the same size in pixels after the move as it was before the move
					size=self.newClueDialog.size()
					self.newClueDialog.move(max(10,boxX-50),max(10,boxY-50))
					self.newClueDialog.resize(size)
					self.newClueDialog.ui.descriptionField.setPlainText(self.ui.messageField.text())
					# move cursor to end since it doesn't happen automatically
					cursor=self.newClueDialog.ui.descriptionField.textCursor()
					cursor.setPosition(len(self.newClueDialog.ui.descriptionField.toPlainText()))
					self.newClueDialog.ui.descriptionField.setTextCursor(cursor)
					# clear the message text since it has been moved to the clue dialog;
					#  it will be moved back to the message text if the clue dialog is canceled
					self.ui.messageField.setText('')
				else:
					logging.info('"Looks like a clue" popup canceled')


# 		logging.info("message:"+str(message))
# 		logging.info("  previous status:"+str(prevStatus)+"  newStatus:"+str(newStatus))
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
# 	# 			logging.info(" 'with' tail found:"+tail)
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
			# logging.info('newStatus='+newStatus+'  prevStatus='+prevStatus+'  tmpNewStatus='+str(self.tmpNewStatus))
			# #508 - disable status change based on text, and show a warning, if this is an amendment
			#  for an older (not the most recent) message for the callsign
			if (not self.amendFlag) or self.isMostRecentForCallsign:
				# allow it to be set back to blank; must set exclusive to false and iterate over each button
				self.ui.statusButtonGroup.setExclusive(False)
				for button in self.ui.statusButtonGroup.buttons():
		# 			logging.info("checking button: "+button.text())
					if button.text()==newStatus:
						button.setChecked(True)
					else:
						button.setChecked(False)
				self.ui.statusButtonGroup.setExclusive(True)
			else:
				# #508 - don't show a warning on every keystroke - just once per relevant text change
				if newStatus!=self.tmpNewStatus:
					self.warnNoStatusChange()
					# logging.info('setting tmpNewStatus to '+newStatus)
					self.tmpNewStatus=newStatus
		self.ui.messageField.deselect()
		self.prevActionWasQuickText=self.insideQuickText # avoid recursion loop

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
		# teamStatusDict[extTeamName]=clickedStatus
		self.parent.setTeamStatus(extTeamName,clickedStatus)

	def updateTabLabel(self):
		i=self.parent.newEntryWindow.ui.tabWidget.indexOf(self)
		button=self.parent.newEntryWindow.ui.tabWidget.tabBar().tabButton(i,QTabBar.LeftSide)
		newText=time.strftime("%H%M")+" "+self.ui.to_fromField.currentText()+" "+self.ui.teamField.text()
		if button:
			button.layout().itemAt(1).widget().setText(newText)
		else:
			logging.info(' ERROR trying to updateTabLabel for a non-existent tab: i='+str(i)+'  newText='+str(newText))
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


# usedClueNames=['1','2','3']
# usedClueNames=[]
		

class clueDialog(QDialog,Ui_clueDialog):
	instances=[]
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
		self.setStyleSheet(globalStyleSheet)
		self.ui.timeField.setText(t)
		self.ui.dateField.setText(time.strftime("%x"))
		self.ui.callsignField.setText(callsign)
		self.ui.radioLocField.setText(re.sub(' +','\n',radioLoc))
		self.ui.clueNumberField.setText(str(newClueNumber))
		self.clueQuickTextAddedStack=[]
		self.parent=parent
		self.parent.childDialogs.append(self)
##		self.parent.timer.stop() # do not timeout the new entry dialog if it has a child clueDialog open!
		#543 - don't use StaysOnTopHint for the clue dialog, so that incoming calls from different teams,
		# while a clue dialog is open, will still cause the new entry window to raise to the top
		# self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
##		self.setWindowFlags(Qt.FramelessWindowHint)
		self.setAttribute(Qt.WA_DeleteOnClose)

		# set max length to prevent text overrun in generated pdf
		# based on https://stackoverflow.com/a/46550977/3577105
		self.ui.descriptionField.textChanged.connect(self.descriptionTextChanged)
		# for locationField, we could use maxLength or setValidator since it's a QLineEdit, but that lacks audio and visual feedback
		self.ui.locationField.textChanged.connect(self.locationTextChanged)
		self.ui.instructionsField.textChanged.connect(self.parent.resetLastModAge)

		self.ui.descriptionField.setFocus()
##		self.i=0 # dialog box location index; set at runtime, so we know which index to free on close
		clueDialog.instances.append(self)
		[x,y,i]=self.pickXYI()
		self.move(x,y)
		self.i=i # save the index so we can clear it on close
		# save the clue number at init time, so that any new clueDialog opened before this one
		#  is saved will have an incremented clue number.  May need to get fancier in terms
		#  of releasing clue numbers on reject, but, don't worry about it for now - that's why
		#  the clue number field is editable.
		# global lastClueNumber
		# lastClueNumber=int(newClueNumber)
		self.clueName=str(newClueNumber) # initialize instance variable here, so that any changed clue name message will have access to the prior value
		# global usedClueNames
		self.parent.parent.usedClueNames.append(self.clueName)
		self.parent.clueDialogOpen=True
		clueDialog.openDialogCount+=1
		self.values=self.parent.getValues()
		amendText=''
		# amendText2=''
		if self.parent.amendFlag:
			amendText=' during amendment of previous message'
			# amendText2=', which will appear with that amended message when completed'
		# self.values[3]="RADIO LOG SOFTWARE: 'LOCATED A CLUE' form opened"+amendText+"; radio operator is gathering details"+amendText2
		self.values[3]="RADIO LOG SOFTWARE: CLUE FORM OPENED FOR CLUE#"+str(newClueNumber)+amendText
##		self.values[3]="RADIO LOG SOFTWARE: 'LOCATED A CLUE' button pressed for '"+self.values[2]+"'; radio operator is gathering details"
##		self.values[2]='' # this message is not actually from a team
		self.parent.parent.newEntry(self.values)
		self.setFixedSize(self.size())
		self.descriptionTooLongHasBeenShown=False
		self.locationTooLongHasBeenShown=False
		self.interviewPopupShown=False
		self.interviewInstructionsAdded=False
		#683 - since we are not using StaysOnTop, raise the clue dialog to the top initially
		self.raise_()
		self.palette=QPalette()
		self.throb()
		logging.info(f'end of clueDialog init: usedClueNames={self.parent.parent.usedClueNames}  last clue number={self.parent.parent.getLastClueNumber()}')

	def changeEvent(self,event):
		if event.type()==QEvent.ActivationChange:
			self.parent.parent.activationChange()

	#683 - throb - copied from newEntryWidget.throb()
	def throb(self,n=0):
		# this function calls itself recursivly 25 times to throb the background blue->white
# 		logging.info("throb:n="+str(n))
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
# 			logging.info("throb complete")
			self.throbTimer=None
			self.palette.setColor(QPalette.Background,QColor(255,255,255))
			self.setPalette(self.palette)

	def customFocusOutEvent(self,widget):
		if 'interview' in widget.toPlainText().lower():
			if not self.interviewPopupShown:
				self.parent.customFocusOutEvent(widget)
				self.interviewPopupShown=True
			if not self.interviewInstructionsAdded:
				t=self.ui.instructionsField.text()
				if t:
					t+='; '
				self.ui.instructionsField.setText(t+'Get interviewee name and contact info')
				self.interviewInstructionsAdded=True

	def descriptionTextChanged(self):
		self.parent.resetLastModAge()
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
		self.parent.resetLastModAge()
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
		# logging.info('clue dialog key pressed')
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
		operator=self.parent.parent.getOperatorInitials()

		# validation: description, location, instructions fields must all be non-blank
		vText=""
		if description=="":
			vText+="\n'Description' cannot be blank."
		if location=="":
			vText+="\n'Location' cannot be blank."
		if instructions=="":
			vText+="\n'Instructions' cannot be blank."
		logging.info("vText:"+vText)
		if vText!="":
			self.clueMsgBox=QMessageBox(QMessageBox.Critical,"Error","Please complete the form and try again:\n"+vText,
				QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			self.clueMsgBox.show()
			self.clueMsgBox.raise_()
			self.clueMsgBox.exec_()
			return

		self.parent.parent.clueLogNeedsPrint=True
		self.parent.cluePopupShown=True # avoid duplicate popup
		textToAdd=''
		existingText=self.parent.ui.messageField.text()
		if existingText!='':
			textToAdd='; '
		textToAdd+="CLUE#"+number+": "+description+"; LOCATION: "+location+"; INSTRUCTIONS: "+instructions
		self.parent.ui.messageField.setText(existingText+textToAdd)
		# previously, lastClueNumber was saved here - on accept; we need to save it on init instead, so that
		#  multiple concurrent clueDialogs will not have the same clue number!
		# header_labels=['CLUE#','DESCRIPTION','TEAM','TIME','DATE','OP','LOCATION','INSTRUCTIONS','RADIO LOC.']
		clueData=[number,description,team,clueTime,clueDate,self.parent.parent.opPeriod,location,instructions,radioLoc,operator]
		self.parent.parent.clueLog.append(clueData)
		if self.ui.clueReportPrintCheckBox.isChecked():
			self.parent.parent.printClueReport(clueData)
		logging.info("accepted - calling close")
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
			really=QMessageBox(QMessageBox.Warning,"Please Confirm","Close this Clue Report Form?\n\nIt cannot be recovered.\n\nDescription / location / instructions text will be copied to the originating message body.",
				QMessageBox.Yes|QMessageBox.No,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			if really.exec_()==QMessageBox.No:
				event.ignore()
				return
			currentClueName=self.ui.clueNumberField.text()

			# release the clue name if appropriate (so it can be used again)
			# if current clue name is strictly numberic (i.e. not '23A') and is the highest clue number so far, then it's safe to release it;
			#  but if any higher clue numbers have been claimed (e.g. by other currently opened clue dialogs), this one needs to be 'voided';
			#  if current clue name is not numeric (e.g. 23A), then never release it; the automated messages are a good audit trail anyway
			# if clueDialog.openDialogCount==1:
			if currentClueName.isnumeric() and int(currentClueName)>=self.parent.parent.getLastClueNumber():
				# global lastClueNumber
				# global usedClueNames
				if currentClueName in self.parent.parent.usedClueNames:
					self.parent.parent.usedClueNames.remove(currentClueName)
				# if usedClueNames:
				# 	lastClueNumber=usedClueNames[-1]
				# else:
				# 	lastClueNumber=0

			self.values=self.parent.getValues()
			amendText=''
			if self.parent.amendFlag:
				amendText=' during amendment of previous message'
			description=self.ui.descriptionField.toPlainText()
			location=self.ui.locationField.text()
			instructions=self.ui.instructionsField.text()
			# canceledMessage='CLUE REPORT #'+currentClueName+' OPENED BUT CANCELED BY THE OPERATOR'+amendText+'.'
			canceledMessage='CLUE FORM CANCELED FOR CLUE#'+currentClueName+amendText+';'
			canceledMessagePart2=''
			if description or location or instructions:
				canceledMessage+='  CLUE REPORT DATA BEFORE CANCELATION: '
			if description:
				canceledMessagePart2+='DESCRIPTION="'+description+'" '
			if location:
				canceledMessagePart2+='LOCATION="'+location+'" '
			if instructions:
				canceledMessagePart2+='INSTRUCTIONS="'+instructions+'" '
			self.values[3]='RADIO LOG SOFTWARE: '+canceledMessage+canceledMessagePart2
			if not canceledMessagePart2:
				self.values[3]+='  No clue data had been entered before cancelation.'
			self.parent.parent.newEntry(self.values)
			#577 but also general good practice: copy any entered clue data back to the parent NED
			msg=self.parent.ui.messageField.text()
			if canceledMessagePart2:
				if msg:
					msg+='; '
				msg+='from canceled clue report: '+canceledMessagePart2
				self.parent.cluePopupShown=True # to avoid popup
				self.parent.ui.messageField.setText(msg)
		clueDialog.indices[self.i]=False # free up the dialog box location for the next one
		self.parent.clueDialogOpen=False
		clueDialog.openDialogCount-=1
		clueDialog.instances.remove(self)
		self.parent.childDialogs.remove(self)
		event.accept()
		if accepted:
			self.parent.accept()
		logging.info(f'end of closeEvent: usedClueNames={self.parent.parent.usedClueNames}  last clue number={self.parent.parent.getLastClueNumber()}')
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
			textToAdd=quickText
			# if existing text already ends in a delimiter (possibly followed by one or more spaces), don't add another
			if re.match('.*[;,] *$',existingText):
				# if it does end in a space (after comma or semicolon), don't add any padding
				if existingText[-1]!=' ':
					textToAdd=' '+quickText
			else:
				textToAdd='; '+quickText
			self.clueQuickTextAddedStack.append(textToAdd)
			self.ui.instructionsField.setText(existingText+textToAdd)
		self.ui.instructionsField.setFocus()

	def clueQuickTextUndo(self):
		logging.info("ctrl+z keyBindings:"+str(QKeySequence("Ctrl+Z")))
		if len(self.clueQuickTextAddedStack):
			textToRemove=self.clueQuickTextAddedStack.pop()
			existingText=self.ui.instructionsField.text()
			self.ui.instructionsField.setText(rreplace(existingText,textToRemove,'',1))
			self.ui.instructionsField.setFocus()

	def clueNumberChanged(self):
		clueNumberChanged(self,self.parent.parent) # shared callback with nonRadioClueDialog


class nonRadioClueDialog(QDialog,Ui_nonRadioClueDialog):
	openDialogCount=0
	instances=[]
	def __init__(self,parent,t,newClueNumber):
		QDialog.__init__(self)
		self.ui=Ui_nonRadioClueDialog()
		self.ui.setupUi(self)
		self.setStyleSheet(globalStyleSheet)
		self.ui.timeField.setText(t)
		self.ui.dateField.setText(time.strftime("%x"))
		self.ui.clueNumberField.setText(str(newClueNumber))
		self.parent=parent
		# self.setWindowFlags(Qt.WindowStaysOnTopHint)
		# self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		self.setAttribute(Qt.WA_DeleteOnClose)
		# values format for adding a new entry:
		#  [time,to_from,team,message,self.formattedLocString,status,self.sec,self.fleet,self.dev,self.origLocString]
		self.values=["" for n in range(10)]
		self.values[0]=time.strftime("%H%M")
		self.values[3]="RADIO LOG SOFTWARE: NON-RADIO CLUE FORM OPENED FOR CLUE#"+str(newClueNumber)
		self.values[6]=time.time()
		self.parent.newEntry(self.values)
		self.setFixedSize(self.size())
		self.interviewPopupShown=False
		self.interviewInstructionsAdded=False
		#683 - since we are not using StaysOnTop, raise the clue dialog to the top initially
		self.raise_()
		self.palette=QPalette()
		self.throb()
		self.parent.nonRadioClueDialogIsOpen=True
		nonRadioClueDialog.openDialogCount+=1
		nonRadioClueDialog.instances.append(self)
		# save the clue number at init time, so that any new clueDialog opened before this one
		#  is saved will have an incremented clue number.  May need to get fancier in terms
		#  of releasing clue numbers on reject, but, don't worry about it for now - that's why
		#  the clue number field is editable.
		# global lastClueNumber
		# lastClueNumber=newClueNumber
		self.clueName=str(newClueNumber)
		# global usedClueNames
		self.parent.usedClueNames.append(self.clueName)
		logging.info(f'end of NRC init: last clue number={self.parent.getLastClueNumber()}; usedClueNames={self.parent.usedClueNames}')

	def changeEvent(self,event):
		if event.type()==QEvent.ActivationChange:
			self.parent.activationChange()
		
	#683 - throb - copied from newEntryWidget.throb()
	def throb(self,n=0):
		# this function calls itself recursivly 25 times to throb the background blue->white
# 		logging.info("throb:n="+str(n))
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
# 			logging.info("throb complete")
			self.throbTimer=None
			self.palette.setColor(QPalette.Background,QColor(255,255,255))
			self.setPalette(self.palette)

	def customFocusOutEvent(self,widget):
		if 'interview' in widget.toPlainText().lower():
			if not self.interviewPopupShown:
				self.parent.showInterviewPopup(widget)
				self.interviewPopupShown=True
			if not self.interviewInstructionsAdded:
				t=self.ui.instructionsField.text()
				if t:
					t+='; '
				self.ui.instructionsField.setText(t+'Get interviewee name and contact info')
				self.interviewInstructionsAdded=True
			
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
		# previously, lastClueNumber was saved here - on accept; we need to save it on init instead, so that
		#  multiple concurrent clueDialogs will not have the same clue number!
		# global lastClueNumber
		# lastClueNumber=int(self.ui.clueNumberField.text())
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
		logging.info("accepted - calling close")
##		# don't try self.close() here - it can cause the dialog to never close!  Instead use super().accept()
		self.parent.clueLogDialog.ui.tableView.model().layoutChanged.emit()
		self.closeEvent(QEvent(QEvent.Close),True)
		super(nonRadioClueDialog,self).accept()

	def reject(self):
		self.closeEvent(QEvent(QEvent.Close),False)
		super(nonRadioClueDialog,self).reject()

	# Esc in the confirmation dialog will close the clue dialog anyway (event.ignore doesn't prevent closure for QDialog);
	#  options are to switch to inheriting from QWidget instead, or to deal with things here in keyPressEvent;
	#  from Google AI overview: confirmed that QWidget instead of QDialog treats Esc as desired,
	#  but has other behavior changes i.e. has no accept() method:

	# Dialog-Specific Behavior (ESC Key): If the window is a QDialog, pressing the Esc key automatically calls
	# QDialog::reject(), which closes the dialog without triggering an ignorable closeEvent in some cases.
	# Solution: For QDialog to handle the Esc key press, you may need to use an event filter or override the
	# keyPressEvent method to manage the Esc key input manually, or consider using a plain QWidget instead
	# if you need total control over closing behavior.

	# not entirely sure why this is a sufficient fix, but, with this code, hitting esc twice leaves the dialog
	#  open, as expected, i.e. it causes event.ignore to 'work as expected'
	def keyPressEvent(self,event):
		key=event.key()
		if key==Qt.Key_Escape:
			self.close() # calls closeEvent
		else:
			super().keyPressEvent(event)

	def closeEvent(self,event,accepted=False):
		# note, this type of messagebox is needed to show above all other dialogs for this application,
		#  even the ones that have WindowStaysOnTopHint.  This works in Vista 32 home basic.
		#  if it didn't show up on top, then, there would be no way to close the radiolog other than kill.
		if not accepted:
			really=QMessageBox(QMessageBox.Warning,"Please Confirm","Close this Clue Report Form?\nIt cannot be recovered.",
				QMessageBox.Yes|QMessageBox.No,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			really.setDefaultButton(QMessageBox.No)
			really.show()
			really.raise_()
			if really.exec_()==QMessageBox.No:
				event.ignore()
				return
			currentClueName=self.ui.clueNumberField.text()
			# if current clue name is strictly numberic (i.e. not '23A') and is the highest clue number so far, then it's safe to release it;
			#  but if any higher clue numbers have been claimed (e.g. by other currently opened clue dialogs), this one needs to be 'voided';
			#  if current clue name is not numeric (e.g. 23A), then never release it; the automated messages are a good audit trail anyway
			# if clueDialog.openDialogCount==1:
			if currentClueName.isnumeric() and int(currentClueName)>=self.parent.getLastClueNumber():
				if currentClueName in self.parent.usedClueNames:
					self.parent.usedClueNames.remove(currentClueName)
			self.values=["" for n in range(10)]
			self.values[0]=time.strftime("%H%M")
			self.values[6]=time.time()
			# amendText=''
			# if self.parent.amendFlag:
			# 	amendText=' during amendment of previous message'
			reportedBy=self.ui.callsignField.text()
			description=self.ui.descriptionField.toPlainText()
			location=self.ui.locationField.text()
			instructions=self.ui.instructionsField.text()
			# canceledMessage='CLUE REPORT #'+currentClueName+' OPENED BUT CANCELED BY THE OPERATOR'+amendText+'.'
			# canceledMessage='NON-RADIO CLUE FORM CANCELED FOR CLUE#'+currentClueName+amendText+';'
			canceledMessage='NON-RADIO CLUE FORM CANCELED FOR CLUE#'+currentClueName+';'
			canceledMessagePart2=''
			if reportedBy or description or location or instructions:
				canceledMessage+='  CLUE REPORT DATA BEFORE CANCELATION: '
			if reportedBy:
				canceledMessagePart2+='REPORTED BY="'+reportedBy+'" '
			if description:
				canceledMessagePart2+='DESCRIPTION="'+description+'" '
			if location:
				canceledMessagePart2+='LOCATION="'+location+'" '
			if instructions:
				canceledMessagePart2+='INSTRUCTIONS="'+instructions+'" '
			self.values[3]='RADIO LOG SOFTWARE: '+canceledMessage+canceledMessagePart2
			if not canceledMessagePart2:
				self.values[3]+='  No clue data had been entered before cancelation.'
			self.parent.newEntry(self.values)
		logging.info(f'open NRC count before decrement: {nonRadioClueDialog.openDialogCount}; len(instances)={len(nonRadioClueDialog.instances)}')
		nonRadioClueDialog.openDialogCount-=1
		nonRadioClueDialog.instances.remove(self)
		logging.info(f'open NRC count after decrement: {nonRadioClueDialog.openDialogCount}; len(instances)={len(nonRadioClueDialog.instances)}')
		if nonRadioClueDialog.openDialogCount<1:
			self.parent.nonRadioClueDialogIsOpen=False
		logging.info(f'end of NRC closeEvent: last clue number={self.parent.getLastClueNumber()}; usedClueNames={self.parent.usedClueNames}; nonRadioClueDialogIsOpen={self.parent.nonRadioClueDialogIsOpen}')
# 	def reject(self):
# ##		self.parent.timer.start(newEntryDialogTimeoutSeconds*1000) # reset the timeout
# 		logging.info("rejected - calling close")
# 		# don't try self.close() here - it can cause the dialog to never close!  Instead use super().reject()
# 		self.closeEvent(None)
# 		super(nonRadioClueDialog,self).reject()

	def clueNumberChanged(self):
		clueNumberChanged(self,self.parent) # shared callback with clueDialog


class clueLogDialog(QDialog,Ui_clueLogDialog):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.ui=Ui_clueLogDialog()
		self.ui.setupUi(self)
		self.setStyleSheet(globalStyleSheet)
		self.parent=parent
		self.tableModel = clueTableModel(parent.clueLog, self)
		self.ui.tableView.setModel(self.tableModel)

		if not self.parent.useOperatorLogin:
			self.ui.tableView.hideColumn(9) # hide operator initials
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

	def toggleRaise(self):
		if self.isVisible():
			self.hide()
		else:
			self.show()
			self.raise_()


class subjectLocatedDialog(QDialog,Ui_subjectLocatedDialog):
	openDialogCount=0
	instances=[]
	def __init__(self,parent,t,callsign,radioLoc,prefixText='',automatic=False):
		QDialog.__init__(self)
		self.ui=Ui_subjectLocatedDialog()
		self.ui.setupUi(self)
		self.setStyleSheet(globalStyleSheet)
		self.ui.timeField.setText(t)
		self.ui.dateField.setText(time.strftime("%x"))
		self.ui.callsignField.setText(callsign)
		self.ui.radioLocField.setText(re.sub(' +','\n',radioLoc))
		self.parent=parent
		self.parent.subjectLocatedDialogOpen=True
		self.parent.childDialogs.append(self)
		# self.setWindowFlags(Qt.WindowStaysOnTopHint)
		# self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		self.setWindowFlags(self.windowFlags() & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.ui.locationField.setFocus()
		self.values=self.parent.getValues()
		automaticText=''
		if automatic:
			automaticText=' automatically'
		amendText=''
		amendText2=''
		if self.parent.amendFlag:
			amendText=' during amendment of previous message'
			amendText2=', which will appear with that amended message when completed'
		self.values[3]="RADIO LOG SOFTWARE: 'SUBJECT LOCATED' form opened"+automaticText+amendText+"; radio operator is gathering details"+amendText2
		if prefixText:
			self.values[3]=prefixText+' ['+self.values[3]+']'
		self.parent.parent.newEntry(self.values)
		subjectLocatedDialog.openDialogCount+=1
		subjectLocatedDialog.instances.append(self)
		self.setFixedSize(self.size())
		self.ui.locationField.textChanged.connect(self.textChanged)
		self.ui.conditionField.textChanged.connect(self.textChanged)
		self.ui.resourcesField.textChanged.connect(self.textChanged)
		self.ui.otherField.textChanged.connect(self.textChanged)
		self.raise_()
		self.palette=QPalette()
		self.throb()
		self.lastModAge=-1
		self.countdownText='Typing in any field will start the auto-save countdown.'
		self.ui.countdownLabel.setText(self.countdownText)

	def textChanged(self,*args):
		self.parent.resetLastModAge()
		self.resetLastModAge()

	def resetLastModAge(self):
		self.lastModAge=0

	def countdown(self):
		c=15-self.lastModAge
		if self.lastModAge>=0:
			s='s'
			if c==1:
				s=''
			self.countdownText='In '+str(c)+' second'+s+', a log entry will be automatically created\n with the current contents of this form.\nYou can leave this form open until you have something\n to type in all three required fields.'
		if c==0:
			self.values=self.parent.getValues()
			alreadyTyped=self.buildAlreadyTyped(includeTime=False)
			self.values[3]="RADIO LOG SOFTWARE: radio operator is still collecting data for the 'SUBJECT LOCATED' form; values so far: "+alreadyTyped
			self.parent.parent.newEntry(self.values)
			self.lastModAge=-1
			self.countdownText='A log entry has been saved with current values of this form.\nTyping in any field will start another auto-save countdown.'
		self.ui.countdownLabel.setText(self.countdownText)

	def changeEvent(self,event):
		if event.type()==QEvent.ActivationChange:
			self.parent.parent.activationChange()

	#683 - throb - copied from newEntryWidget.throb()
	def throb(self,n=0):
		# this function calls itself recursivly 25 times to throb the background blue->white
# 		logging.info("throb:n="+str(n))
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
# 			logging.info("throb complete")
			self.throbTimer=None
			self.palette.setColor(QPalette.Background,QColor(255,255,255))
			self.setPalette(self.palette)

	def accept(self):
		location=self.ui.locationField.text()
		condition=self.ui.conditionField.toPlainText()
		resources=self.ui.resourcesField.toPlainText()

		# validation: description, location, instructions fields must all be non-blank
		vText=""
		if location=="":
			vText+="\n'Location' cannot be blank."
		if condition=="":
			vText+="\n'Condition' cannot be blank."
		if resources=="":
			vText+="\n'Resources Needed' cannot be blank."
		logging.info("vText:"+vText)
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
		textToAdd+='SUBJECT LOCATED form completed: '+self.buildAlreadyTyped()
		self.parent.ui.messageField.setText(existingText+textToAdd)
		self.closeEvent(QEvent(QEvent.Close),True)
		super(subjectLocatedDialog,self).accept()

# 	def reject(self):
# 		logging.info("rejected - calling close")
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
			# place the triggering text back in the New Entry Dialog message field, as it was before this dialog was opened
			other=self.ui.otherField.toPlainText()
			if ' operator: "' in other:
				self.parent.ui.messageField.setText(other[other.index(' operator: "')+12:-2])
			self.values[3]="RADIO LOG SOFTWARE: radio operator canceled the 'SUBJECT LOCATED' form"+amendText+": "+self.buildAlreadyTyped()
			self.parent.parent.newEntry(self.values)
		self.parent.subjectLocatedDialogOpen=False
		subjectLocatedDialog.openDialogCount-=1
		self.parent.childDialogs.remove(self)
		subjectLocatedDialog.instances.remove(self)
		if accepted:
			self.parent.accept()

	def buildAlreadyTyped(self,includeTime=True,includeRadioLoc=True):
		location=self.ui.locationField.text().rstrip()
		condition=self.ui.conditionField.toPlainText().rstrip()
		resources=self.ui.resourcesField.toPlainText().rstrip()
		other=self.ui.otherField.toPlainText().rstrip()
		alreadyTyped='' # callsign and date are already saved in the log, no need to repeat them here
		if includeTime:
			subjTime=self.ui.timeField.text()
			if subjTime:
				alreadyTyped+='; TIME: '+subjTime
		if includeRadioLoc:
			radioLoc=self.ui.radioLocField.text()
			if radioLoc:
				alreadyTyped+='; RADIO GPS: '+re.sub(r'\n','  ',radioLoc)
		if location:
			alreadyTyped+='; LOCATION: '+location
		if condition:
			alreadyTyped+='; CONDITION: '+condition
		if resources:
			alreadyTyped+='; RESOURCES NEEDED: '+resources
		if other:
			alreadyTyped+='; OTHER: '+other
		# remove leading semicolon-and-space if needed
		if alreadyTyped.startswith('; '):
			alreadyTyped=alreadyTyped[2:]
		return alreadyTyped
	
	# fix issue #338: prevent 'esc' from closing the newEntryWindow
	def keyPressEvent(self,event):
		# logging.info('subject located dialog key pressed')
		if event.key()!=Qt.Key_Escape:
			super().keyPressEvent(event) # pass the event as normal


class printClueLogDialog(QDialog,Ui_printClueLogDialog):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.ui=Ui_printClueLogDialog()
		self.ui.setupUi(self)
		self.setStyleSheet(globalStyleSheet)
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
		logging.info("  printClueLogDialog.accept.trace1")
		if opPeriod=='--':
			crit=QMessageBox(QMessageBox.Critical,"No Clues to Print","There are no clues to print.",QMessageBox.Ok,self.parent,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			crit.show()
			crit.raise_()
			crit.exec_()
			self.reject()
		else:
			self.parent.printClueLog(opPeriod)
			logging.info("  printClueLogDialog.accept.trace2")
			super(printClueLogDialog,self).accept()
			logging.info("  printClueLogDialog.accept.trace3")

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
		self.setStyleSheet(globalStyleSheet)
		self.parent=parent
		self.ui.currentOpPeriodField.setText(str(parent.opPeriod))
		self.ui.newOpPeriodField.setMinimum(parent.opPeriod+1) # do this before setting the value, in case the new value is less than the old minimum
		self.ui.newOpPeriodField.setValue(parent.opPeriod+1)
		# self.setAttribute(Qt.WA_DeleteOnClose)
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		self.adjustSize()
		self.setFixedSize(self.size())

	def accept(self):
		if self.ui.printCheckBox.isChecked():
			self.parent.printDialog.exec_() # instead of show(), to pause execution until the print dialog is closed

		if self.ui.deleteTabsCheckBox.isChecked():
			for extTeamName in teamStatusDict:
				status=teamStatusDict[extTeamName]
				if status == "At IC":
					self.parent.deleteTeamTab(getNiceTeamName(extTeamName))

		self.parent.opPeriod=self.ui.newOpPeriodField.value()
		self.parent.ui.opPeriodButton.setText("OP "+str(self.parent.opPeriod))
		opText="Operational Period "+str(self.parent.opPeriod)+" Begins: "+time.strftime("%a %b %d, %Y")
		self.parent.newEntry([time.strftime("%H%M"),"","",opText,"","",time.time(),"",""])
##      clueData=[number,description,team,clueTime,clueDate,self.parent.parent.opPeriod,location,instructions,radioLoc]
		self.parent.clueLog.append(['',opText,'',time.strftime("%H%M"),'','','','',''])
		self.parent.printDialog.ui.opPeriodComboBox.addItem(str(self.ui.newOpPeriodField.value()))
		super(opPeriodDialog,self).accept()
	
	def deselectAfterChange(self,e): # since QueuedConnection can't be specified in Qt Designer
		QTimer.singleShot(100,self.deselectDeferred)
		
	def deselectDeferred(self):
		self.ui.newOpPeriodField.lineEdit().deselect()

	def toggleShow(self):
		if self.isVisible():
			self.hide()
		else:
			self.show()
			self.raise_()

# allow different justifications for different columns of qtableview
# from https://stackoverflow.com/a/52644764
from PyQt5 import QtCore,QtWidgets
from PyQt5.QtCore import QThread,pyqtSignal
class alignCenterDelegate(QtWidgets.QStyledItemDelegate):
	def initStyleOption(self,option,index):
		super(alignCenterDelegate,self).initStyleOption(option,index)
		option.displayAlignment=QtCore.Qt.AlignCenter

class continuedIncidentDialog(QDialog,Ui_continuedIncidentDialog):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.ui=Ui_continuedIncidentDialog()
		self.ui.setupUi(self)
		self.setStyleSheet(globalStyleSheet)
		self.parent=parent
		self.incidentNameCandidate=''
		self.lastOPCandidate=0
		self.lastClueCandidate=0
		self.usedClueNamesCandidate=[]
		self.setAttribute(Qt.WA_DeleteOnClose)
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		ciwd=self.parent.continuedIncidentWindowDays
		if ciwd==1:
			dayText='day'
		else:
			dayText=str(ciwd)+' days'
		self.ui.instructionsLabel.setText('If so, select a row from the following list of radiolog sessions that were run on this computer within the last '+dayText+', then click YES.')
		self.ui.theTable.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
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
		self.parent.incidentName=self.sessionCandidate['incidentName']
		self.parent.ui.incidentNameLabel.setText(self.parent.incidentName)
		self.parent.optionsDialog.ui.incidentField.setText(self.parent.incidentName)
		self.parent.usedClueNames=self.sessionCandidate['usedClueNames']
		logging.info(f'previously used clue names: {self.parent.usedClueNames}')
		self.parent.opPeriod=self.sessionCandidate['lastOP']+1
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
		# logging.info('row clicked:'+str(row))
		# logging.info('  selected row:'+str(self.ui.theTable.selectedIndexes()[0].row()))
		if self.changed:
			self.ui.yesButton.setEnabled(True)
			session=self.ui.theTable.item(row,0).data(Qt.UserRole)
			logging.info('selected session:'+json.dumps(session,indent=3))
			# self.ui.yesButton.setText('YES: Start a new OP of "'+session['incidentName']+'"\n(OP = '+str(session['lastOP']+1)+'; next clue# = '+str(session['highestClueNumber']+1)+')')
			self.ui.yesButton.setText('YES: Start a new OP of "'+session['incidentName']+'"\n(OP = '+str(session['lastOP']+1)+'; next clue# = '+str(self.parent.getLastClueNumber(session['usedClueNames'])+1)+')')
			self.ui.yesButton.setDefault(True)
			self.changed=False
			self.sessionCandidate=session
		else:
			self.ui.theTable.clearSelection()
			self.ui.noButton.setDefault(True)
			self.ui.yesButton.setEnabled(False)
			self.ui.theTable.clearFocus() # to remove the focus rectangle

	def currentCellChanged(self,r1,c1,r2,c2):
		# logging.info('r1={} c1={}   r2={} c2={}'.format(r1,c1,r2,c2))
		self.changed=True

	def clicked(self,i):
		# logging.info('clicked row: '+str(i.row()))
		si=self.ui.theTable.selectedIndexes()
		if not si: # clicked when already unselected; select it again
			# logging.info('  no row selected when clicked event called')
			self.changed=True
		# else:
			# logging.info('  selected row:'+str(self.ui.theTable.selectedIndexes()[0].row()))

class loadDialog(QDialog,Ui_loadDialog):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.ui=Ui_loadDialog()
		self.ui.setupUi(self)
		self.setStyleSheet(globalStyleSheet)
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
		self.sessionToLoad=None
		self.setFixedSize(self.size())

	def accept(self):
		if self.sessionToLoad:
			self.parent.load(self.sessionToLoad)
			super(loadDialog,self).accept()

	def reject(self):
		super(loadDialog,self).reject()

	def cellClicked(self,row,col):
		self.sessionToLoad=self.ui.theTable.item(row,0).data(Qt.UserRole)

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
		self.setStyleSheet(globalStyleSheet)
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		self.parent=parent
		self.tableModel = fsTableModel(parent.fsLog, self)
		self.ui.tableView.setModel(self.tableModel)
		self.ui.tableView.setSelectionMode(QAbstractItemView.NoSelection)
		self.ui.tableView.clicked.connect(self.tableClicked)
		self.ui.tableView.hideColumn(5) # hide com port
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
		logging.info("closing fsFilterDialog")
			
	def toggleShow(self):
		if self.isVisible():
			self.close()
		else:
			self.show()
			self.raise_()


# class teamTabsListModel(QListModel)
class fsSendDialog(QDialog,Ui_fsSendDialog):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.ui=Ui_fsSendDialog()
		self.ui.setupUi(self)
		self.setStyleSheet(globalStyleSheet)
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		self.parent=parent
		# need to connect apply signal by hand https://stackoverflow.com/a/35444005
		btn=self.ui.buttonBox.button(QDialogButtonBox.Apply)
		btn.clicked.connect(self.apply)
		# 36 character max length - see sendText notes
		self.ui.messageField.setValidator(QRegExpValidator(QRegExp('.{1,36}'),self.ui.messageField))
		self.updateGUI() # to set device validator

	def updateGUI(self):
		sendText=self.ui.sendTextRadioButton.isChecked()
		sendAll=self.ui.sendToAllCheckbox.isChecked()
		fs=self.ui.fsRadioButton.isChecked()
		IDNeeded=not sendText or not sendAll
		self.ui.sendToAllCheckbox.setEnabled(sendText)
		self.ui.fsRadioButton.setEnabled(IDNeeded)
		self.ui.nxRadioButton.setEnabled(IDNeeded)
		self.ui.fleetField.setEnabled(fs and IDNeeded)
		self.ui.fleetField.setValidator(QRegExpValidator(QRegExp('[1-9][0-9][0-9]'),self.ui.fleetField))
		self.ui.fleetLabel.setEnabled(fs and IDNeeded)
		self.ui.deviceField.setEnabled(IDNeeded)
		self.ui.deviceLabel.setEnabled(IDNeeded)
		digitRE='[0-9]'
		if fs:
			deviceDigits=4
			firstDigitRE='[1-9]' # first digit cannot be zero
		else:
			deviceDigits=5
			firstDigitRE=digitRE # first digit can be zero
		deviceSuffix='(s)'
		if not sendText:
			deviceSuffix=''
		self.ui.deviceLabel.setText(str(deviceDigits)+'-digit Device ID'+deviceSuffix)
		# allow multiple devices when sending text, but just one when polling GPS
		coreRE=firstDigitRE+(digitRE*(deviceDigits-1)) # '[1-9][0-9][0-9][0-9]' or '[0-9][0-9][0-9][0-9][0-9]'
		if sendText:
			devValRE='^('+coreRE+'[,]?[ ]*)+$' # delimiter: zero or one commas, followed by zero or more spaces
		else:
			devValRE=coreRE
		# logging.info('setting device validator regex: "'+devValRE+'"')
		self.ui.deviceField.setValidator(QRegExpValidator(QRegExp(devValRE),self.ui.deviceField))
		self.ui.messageField.setEnabled(sendText)
		self.ui.messageLabel1.setEnabled(sendText)
		self.ui.messageLabel2.setEnabled(sendText)

	def apply(self):
		if not self.parent.firstComPort:
			msg='Cannot send FleetSync data - no valid FleetSync COM ports were found.  Keying the mic on a portable radio will trigger COM port recognition.'
			logging.info(msg)
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
		# since trailing comma or spaces would not flag the device validator,
		#  trim them off the device string before applying
		if len(device)>0 and not device[-1].isdigit():
			device=device.rstrip().rstrip(',')
			self.ui.deviceField.setText(device)

		msg=self.ui.messageField.text()
		invalidMsg='The form had error(s).  Please correct and try again:'
		sendText=self.ui.sendTextRadioButton.isChecked()
		sendAll=self.ui.sendToAllCheckbox.isChecked()
		fs=self.ui.fsRadioButton.isChecked()
		if fs:
			digitStr='four'
		else:
			digitStr='five'
		if not sendAll:
			if not self.ui.fleetField.hasAcceptableInput():
				invalidMsg+='\n - Fleet ID must be a three-digit integer'
				valid=False
			if not self.ui.deviceField.hasAcceptableInput():
				if sendText:
					invalidMsg+='\n - Device ID(s) must be a '+digitStr+'-digit integer, or a comma-separated or space-separated list of '+digitStr+'-digit integers'
				else:
					invalidMsg+='\n - Device ID must be a '+digitStr+'-digit integer'
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
					logging.info('ERROR: the form validated, but apparently in error: must specify a device ID or list of device IDs (separated by comma or space)')
		else:
			self.parent.pollGPS(fleet,device)


class fsSendMessageDialog(QDialog,Ui_fsSendMessageDialog):
	def __init__(self,parent,fdcList): # fdcList is a list of [fleet,dev,callsignText] lists
		QDialog.__init__(self)
		self.ui=Ui_fsSendMessageDialog()
		self.ui.setupUi(self)
		self.setStyleSheet(globalStyleSheet)
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		self.parent=parent
		self.fdcList=fdcList
		# 36 character max length - see sendText notes
		self.ui.messageField.setValidator(QRegExpValidator(QRegExp('.{1,36}'),self.ui.messageField))
		if len(fdcList)==1:
			[fleet,device,callsignText]=fdcList[0]
			if not fleet:
				fleet='NEXEDGE'
			self.ui.theLabel.setText('Message for '+str(fleet)+':'+str(device)+' '+str(callsignText)+':')
		else:
			label='Message for multiple radios:\n\n(NOTE: This could take a while: the system will wait up to '+str(self.parent.fsAwaitingResponseTimeout)+' seconds for an acknowledge response from each radio.  If each acknowledge is quick, this might just take a second or so per radio.  Consider whether this is what you really want to do.)\n'
			for fdc in fdcList:
				[fleet,device,callsignText]=fdc
				if not fleet:
					fleet='NEXEDGE'
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
		

class clickableWidget(QWidget):
	clicked=pyqtSignal()
	def __init__(self,parent,*args,**kwargs):
		self.parent=parent
		QWidget.__init__(self,parent)
		self.pressed=False

	def mousePressEvent(self,e):
		# self.move(self.mapToParent(QPoint(2,2)))
		# QCoreApplication.processEvents()
		self.pressed=True

	def mouseOutEvent(self,e):
		# self.move(self.mapToParent(QPoint(0,0)))
		# QCoreApplication.processEvents()
		self.pressed=False

	def mouseReleaseEvent(self,e):
		# self.move(self.mapToParent(QPoint(0,0)))
		# QCoreApplication.processEvents()
		if self.pressed:
			self.clicked.emit()

	# required for stylesheets to apply to subclasses
	# https://stackoverflow.com/a/32889486/3577105
	def paintEvent(self,pe):
		o=QStyleOption()
		o.initFrom(self)
		p=QPainter(self)
		self.style().drawPrimitive(QStyle.PE_Widget,o,p,self)


class loginDialog(QDialog,Ui_loginDialog):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.ui=Ui_loginDialog()
		self.ui.setupUi(self)
		self.setStyleSheet(globalStyleSheet)
		self.ui.buttonBox.button(QDialogButtonBox.Ok).setText('Log In')
		self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
		self.parent=parent
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		self.knownDefaultText=' -- Select a Known Operator -- '
		self.lastNameText=self.ui.lastNameField.text()
		self.firstNameText=self.ui.firstNameField.text()
		self.idText=self.ui.idField.text()
		self.parent.loadOperators()

	def showEvent(self,e):
		self.parent.loadOperators()
		if self.parent.operatorLastName.startswith('?'):
			operatorText='Not logged in'
		else:
			operatorText=self.parent.operatorLastName+', '+self.parent.operatorFirstName+'  '+self.parent.operatorId
		self.ui.currentOperatorLabel.setText('Current Operator: '+operatorText)
		self.ui.knownComboBox.clear()
		self.ui.knownComboBox.addItem(self.knownDefaultText)
		self.ui.lastNameField.setText('')
		self.ui.firstNameField.setText('')
		self.ui.idField.setText('')
		self.items=[] # list of items: first entry is the string, second entry is the variant which is a list [lastName,firstName,id]
		for od in self.parent.operatorsDict['operators']:
			if isinstance(od,dict):
				lastName=od.get('lastName')
				firstName=od.get('firstName')
				id=od.get('id')
				if isinstance(lastName,str) and isinstance(firstName,str) and isinstance(id,str):
					# don't list the current operator
					if not (lastName==self.parent.operatorLastName and firstName==self.parent.operatorFirstName and id==self.parent.operatorId):
						self.items.append([lastName+', '+firstName+'  '+id,[lastName,firstName,id]])
		self.items.sort(key=lambda x:x[0]) # alphabetical sort - could be changed to most-frequent sort if needed
		logging.info('operator items to show in loginDialog knownComboBox (current operator excluded):'+str(self.items))
		for item in self.items:
			self.ui.knownComboBox.addItem(item[0],item[1])

	def toggleShow(self):
		if self.isVisible():
			self.close()
		else:
			self.show()
			self.raise_()

	def knownFieldChanged(self,i):
		self.ui.firstTimeGroupBox.setEnabled(i==0)
		self.checkForValidOperator()

	# always leave known field enabled, so it's easy to override any entered text
	def lastNameFieldTextChanged(self,t):
		self.lastNameText=t
		self.checkForValidOperator()

	def firstNameFieldTextChanged(self,t):
		self.firstNameText=t
		self.checkForValidOperator()

	def idFieldTextChanged(self,t):
		self.idText=t
		self.checkForValidOperator()

	def checkForValidOperator(self):
		# does known field have a valid selection?
		vk=self.ui.knownComboBox.currentIndex()!=0
		# does first-time field group have a valid selection (are all three fields non-empty)?
		vft=(self.lastNameText!='') and (self.firstNameText!='') and (self.idText!='')
		# if either is valid, enable the Log In button
		self.ui.buttonBox.button(QDialogButtonBox.Ok).setEnabled(vk or vft)

	def accept(self):
		oldLastName=self.parent.operatorLastName
		oldFirstName=self.parent.operatorFirstName
		oldId=self.parent.operatorId
		lastName=self.ui.lastNameField.text()
		firstName=self.ui.firstNameField.text()
		id=self.ui.idField.text()
		if lastName or firstName or id: # first-time operator
			if self.ui.knownComboBox.currentText()!=self.knownDefaultText:
				msg='ERROR: you selected a known operator, but one or more of the first-time operator fields contain text.  Select one or the other.'
				logging.info(msg)
				box=QMessageBox(QMessageBox.Warning,'Form data conflict',msg,
						QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
				box.exec_()
				return
			elif not lastName or not firstName or not id:
				msg='ERROR: you must fill out all three fields (Last Name, First Name, ID)'
				logging.info(msg)
				box=QMessageBox(QMessageBox.Warning,'Form data conflict',msg,
						QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
				box.exec_()
				return
			else:
				# check to see if the typed first-time operator is a 'close match' for a known user;
				#  if so, offer to select the known user instead - this is mainly to prevent duplicate
				#  entries in the operator dictionary
				usedKnownMatch=False
				for item in self.items:
					if lastName.lower()==item[1][0].lower() and firstName.lower()==item[1][1].lower() and id.lower().replace(' ','')==item[1][2].lower().replace(' ',''):
						logging.info('  exact case-insensitive match with "'+item[0]+'"')
						box=QMessageBox(QMessageBox.Information,'Exact Match','The specified Last Name, First Name, and ID are the same as this Known Operator:\n\n    '+item[0]+'\n\nYou will be logged in as the existing Known Operator.',
							QMessageBox.Ok,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
						box.show()
						box.raise_()
						box.exec_()
						[newLastName,newFirstName,newId]=item[1]
						usedKnownMatch=True
						break
					r1=SequenceMatcher(None,lastName.lower(),item[1][0].lower()).ratio()
					# logging.info('comparing '+lastName+' to '+item[1][0]+' : ratio='+str(r1))
					r2=SequenceMatcher(None,firstName.lower(),item[1][1].lower()).ratio()
					# logging.info('comparing '+firstName+' to '+item[1][1]+' : ratio='+str(r2))
					if (r1+r2)/2>0.7 or r1>0.8 or r2>0.8:
						# logging.info('  possible match with "'+item[0]+'"')
						tmp=lastName+', '+firstName+'  '+id
						box=QMessageBox(QMessageBox.Information,'Possible Match','The specified First-Time Operator values\n\n    '+tmp+'\n\nare similar to this Known Operator:\n\n    '+item[0]+'\n\nLog in as the specified First-Time Operator, or, as the similar Known Operator?',
							QMessageBox.Yes|QMessageBox.No,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
						box.button(QMessageBox.Yes).setText('First-Time: '+tmp)
						box.button(QMessageBox.No).setText('Known: '+item[0])
						box.show()
						box.raise_()
						r=box.exec_()
						# First-time selected: don't break the loop - in case there are more matches
						if r==QMessageBox.Yes:
							[newLastName,newFirstName,newId]=[lastName,firstName,id]
						# Known selected: break the loop
						elif r==QMessageBox.No:
							[newLastName,newFirstName,newId]=item[1]
							usedKnownMatch=True
							break
					# else:
					# 	logging.info('  no match')
				if not usedKnownMatch:
					newLastName=lastName
					newFirstName=firstName
					newId=id
					self.parent.operatorsDict['operators'].append({
						'lastName':lastName,
						'firstName':firstName,
						'id':id,
						'usage':[]
					})
		elif self.ui.knownComboBox.currentText()!=self.knownDefaultText: # known operator
			[newLastName,newFirstName,newId]=self.ui.knownComboBox.currentData()
		else:
			msg='ERROR: choose a known operator, or, fill out all three fields for a first-time operator.'
			logging.info(msg)
			box=QMessageBox(QMessageBox.Warning,'Form data conflict',msg,
					QMessageBox.Close,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			box.exec_()
			return
		self.parent.operatorLastName=newLastName
		self.parent.operatorFirstName=newFirstName
		self.parent.operatorId=newId
		oldOperatorString=oldLastName+', '+oldFirstName+'  '+oldId
		newOperatorString=newLastName+', '+newFirstName+'  '+newId
		self.parent.ui.loginInitialsLabel.setText(self.parent.getOperatorInitials())
		self.parent.ui.loginIdLabel.setText(newId)
		
		# values format for adding a new entry:
		#  [time,to_from,team,message,self.formattedLocString,status,self.sec,self.fleet,self.dev,self.origLocString]
		values=['' for n in range(10)]
		values[0]=time.strftime("%H%M")
		values[6]=time.time()
		values[3]='RADIO OPERATOR LOGGED IN: '+newOperatorString
		self.parent.newEntry(values)

		# update the usage dictionaries
		logging.info('Updating operator usage statistics from loginDialog.accept.  List of operators before update:\n'+str(self.parent.getOperatorNames()))
		t=int(time.time())
		oldOperatorDicts=[d for d in self.parent.operatorsDict['operators'] if d['lastName']==oldLastName and d['firstName']==oldFirstName and d['id']==oldId]
		if len(oldOperatorDicts)==1:
			oldOperatorDict=oldOperatorDicts[0]
			if 'usage' not in oldOperatorDict.keys():
				oldOperatorDict['usage']=[]
			# there could be more than one usage dict with stop=null, if radiolog crashed;
			#  we need to make sure we are updating the most recent one
			oldUsageDicts=[d for d in oldOperatorDict['usage'] if d['stop']==None]
			oldUsageDicts.sort(key=lambda x:x['start'])
			oldUsageDict=oldUsageDicts[0]
			oldUsageDict['stop']=t
			oldUsageDict['next']=newOperatorString
		elif not oldLastName.startswith('?'):
			logging.info('ERROR: oldOperatorDict had '+str(len(oldOperatorDicts))+' matches; should have exactly one match.  Old operator usage will not be updated.')

		logging.info('Updating operator usage statistics from loginDialog.accept, part 2.  List of operators before update:\n'+str(self.parent.getOperatorNames()))
		newOperatorDicts=[d for d in self.parent.operatorsDict['operators'] if d['lastName']==newLastName and d['firstName']==newFirstName and d['id']==newId]
		if len(newOperatorDicts)==1:
			newOperatorDict=newOperatorDicts[0]
			if 'usage' not in newOperatorDict.keys():
				newOperatorDict['usage']=[]
			prev=oldOperatorString
			if prev.startswith('?'):
				prev=None
			newOperatorDict['usage'].append({
				'start':t,
				'stop':None,
				'incident':self.parent.incidentName,
				'previous':prev,
				'next':None
			})
		else:
			logging.info('ERROR: newOperatorDict had '+str(len(newOperatorDicts))+' matches; should have exactly one match.  New operator usage will not be updated.')

		self.parent.saveOperators()
		super(loginDialog,self).accept()

	# def closeEvent(self,e):
	# 	logging.info('closeEvent called')
	# 	self.parent.saveOperators()

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
##		logging.info("CONVERTING")


class teamNotesDialog(QDialog,Ui_teamNotesDialog):
	def __init__(self,parent):
		QDialog.__init__(self)
		self.ui=Ui_teamNotesDialog()
		self.ui.setupUi(self)
		self.setStyleSheet(globalStyleSheet)
		self.setWindowFlags(Qt.WindowStaysOnTopHint)
		self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
		self.setFixedSize(self.size())
		self.parent=parent
		self.niceTeamName=None
		self.extTeamName=None
		self.skipTeamChangedCB=False

	def teamChanged(self,e):
		if self.skipTeamChangedCB or not str(self.ui.teamField.currentText()):
			self.skipTeamChangedCB=False
			return
		savedNotes=self.parent.teamNotesDict.get(self.extTeamName,None)
		if self.ui.notesField.toPlainText() not in [savedNotes,'','No notes for '+str(self.niceTeamName)]:
			really=QMessageBox(QMessageBox.Warning,"Please Confirm","The text you typed for "+str(self.niceTeamName)+" is not the same as the saved notes for "+str(self.niceTeamName)+".\n\nSwitch to show notes for "+str(self.ui.teamField.currentText())+", discarding what you typed?",
				QMessageBox.Yes|QMessageBox.No,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			if really.exec_()==QMessageBox.No:
				self.skipTeamChangedCB=True
				self.ui.teamField.setCurrentText(self.niceTeamName)
				return
		self.niceTeamName=str(self.ui.teamField.currentText())
		self.extTeamName=getExtTeamName(self.niceTeamName)
		# logging.info('getting team notes for '+str(self.extTeamName))
		notes=str(self.parent.teamNotesDict.get(self.extTeamName,'No notes for '+self.niceTeamName))
		# logging.info('  --> '+notes)
		self.ui.notesField.setPlainText(notes)

	def notesTextChanged(self):
		self.ui.buttonBox.button(QDialogButtonBox.Save).setEnabled(self.ui.notesField.toPlainText()!='No notes for '+self.ui.teamField.currentText())

	def showEvent(self,e):
		self.ui.teamField.clear()
		self.ui.teamField.addItems([getNiceTeamName(x) for x in self.parent.extTeamNameList if 'spacer' not in x])

	def toggleShow(self):
		logging.info('teamNotesDialog toggleShow called')
		if self.isVisible():
			self.close()
		else:
			self.show()
			self.raise_()

	def accept(self):
		if self.ui.notesField.toPlainText() not in ['','No notes for '+self.ui.teamField.currentText()]:
			self.parent.teamNotesDict[self.extTeamName]=self.ui.notesField.toPlainText()
			self.parent.teamNotesBuildTooltip(self.extTeamName)
			self.parent.saveTeamNotes()
		else:
			logging.info('team notes dialog save button clicked for '+self.ui.teamField.currentText()+' with default text in place; nothing to save')
		self.close()
	
	# call closeEvent from Cancel button or Escape key; otherwise, closeEvent is only called by the Red X
	def reject(self):
		self.close()

	def closeEvent(self,event):
		savedNotes=self.parent.teamNotesDict.get(self.extTeamName,None)
		if self.ui.notesField.toPlainText() not in [savedNotes,'','No notes for '+self.ui.teamField.currentText()]:
			really=QMessageBox(QMessageBox.Warning,"Please Confirm","The text you typed is not the same as the saved notes for "+self.ui.teamField.currentText()+".\n\nClose the Team Notes form, discarding what you typed?",
				QMessageBox.Yes|QMessageBox.No,self,Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.Dialog|Qt.MSWindowsFixedSizeDialogHint|Qt.WindowStaysOnTopHint)
			if really.exec_()==QMessageBox.No:
				event.ignore()
				return
			# if confirmed, set the text field to the same as the saved notes, to avoid warning on next open
			notes=str(self.parent.teamNotesDict.get(self.extTeamName,'No notes for '+self.niceTeamName))
			self.ui.notesField.setPlainText(notes)

class clueTableModel(QAbstractTableModel):
	header_labels=['#','DESCRIPTION','TEAM','TIME','DATE','O.P.','LOCATION','INSTRUCTIONS','RADIO LOC.','']
	def __init__(self,datain,parent=None,*args):
		QAbstractTableModel.__init__(self,parent,*args)
		self.arraydata=datain
		self.printIconPixmap=QPixmap(20,20)
		self.printIconPixmap.load(":/radiolog_ui/icons/print_icon.png")
		self.operatorIconPixmap=QPixmap(20,20)
		self.operatorIconPixmap.load(':/radiolog_ui/icons/user_icon_80px.png')
##		self.setEditTriggers(QAbstractItemView.NoEditTriggers)

	def headerData(self,section,orientation,role=Qt.DisplayRole):
		if orientation==Qt.Vertical:
			if role==Qt.DecorationRole and self.arraydata[section][0]!="":
				#icon and button won't display correctly in this use case; just make the entire header item clickable
				return self.printIconPixmap
			if role==Qt.DisplayRole:
				return ""
		elif section==9:
			return self.operatorIconPixmap
		elif role==Qt.DisplayRole:
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
		except Exception as e:
			row=index.row()
			col=index.column()
			logging.info(f'Exception in clueTableModel.data for row={row} col={col}:{e}')
			logging.info("arraydata:")
			logging.info(self.arraydata)
		else:
			return rval

	def dataChangedAll(self):
		self.dataChanged.emit(self.createIndex(0,0),self.createIndex(self.rowCount(self)-1,self.columnCount(self)-1))


class MyTableModel(QAbstractTableModel):
	header_labels=['TIME','T/F','TEAM','MESSAGE','RADIO LOC.','STATUS','sec','fleet','dev','origLoc','']
	def __init__(self, datain, parent=None, *args):
		QAbstractTableModel.__init__(self, parent, *args)
		self.arraydata=datain
		self.operatorIconPixmap=QPixmap(20,20)
		self.operatorIconPixmap.load(':/radiolog_ui/icons/user_icon_80px.png')

	def headerData(self,section,orientation,role=Qt.DisplayRole):
#		print("headerData:",section,",",orientation,",",role)
		if role==Qt.DisplayRole and orientation==Qt.Horizontal:
			return self.header_labels[section]
		if section==10 and role==Qt.DecorationRole:
			return self.operatorIconPixmap
		else:
			return QAbstractTableModel.headerData(self,section,orientation,role)

	def rowCount(self, parent):
		return len(self.arraydata)

	def columnCount(self, parent):
		return len(self.arraydata[0])

	def data(self, index, role):
		# if role==Qt.EditRole:
		# 	logging.info('data called with edit role: index='+str(index)+' role='+str(role))
		if not index.isValid():
			return QVariant()
		elif role not in [Qt.DisplayRole,Qt.EditRole]:
			return QVariant()
		try:
			rval=QVariant(self.arraydata[index.row()][index.column()])
		except Exception as e:
			row=index.row()
			col=index.column()
			logging.info(f'Exception in fsTableModel.data for row={row} col={col}:{e}')
			logging.info("arraydata:")
			logging.info(self.arraydata)
		else:
			return rval

	def flags(self,index):
		return Qt.ItemIsEnabled|Qt.ItemIsSelectable|Qt.ItemIsEditable


class CustomTableItemDelegate(QStyledItemDelegate):
	def __init__(self,parent=None):
		self.parent=parent
		super(CustomTableItemDelegate,self).__init__(parent)

	#568 - from https://stackoverflow.com/a/68626169/3577105
	def createEditor(self,parent,option,index):
		editor=super().createEditor(parent,option,index)
		if isinstance(editor,QtWidgets.QLineEdit):
			editor.setContextMenuPolicy(Qt.CustomContextMenu)
			editor.customContextMenuRequested.connect(self.contextMenuRequested)
			editor.selectionChanged.connect(self.updateSelection)
		return editor

	def updateSelection(self):
		self.parent.sel=str(self.sender().selectedText())
		# logging.info('updating selection: sel='+str(self.sender().selectedText()))

	def contextMenuRequested(self,pos):
		# logging.info('item context menu requested during edit: pos='+str(pos))
		# logging.info("row:"+str(self.parent.row)+":"+str(self.parent.rowData))
		menu=QMenu()
		menu.setFont(self.parent.window().menuFont)
		menu.addAction(self.parent.copyAction)
		self.parent.copyAction.triggered.connect(menu.close)
		menu.addAction(self.parent.amendAction)
		self.parent.contextMenuOpened=True
		action=menu.exec_(self.sender().mapToGlobal(pos))
		self.parent.contextMenuOpened=False

	def eventFilter(self,target,event):
		t=event.type()
		# if event.type() in [QEvent.KeyPress,QEvent.Shortcut,QEvent.ShortcutOverride]:
			# logging.info('event(delegate): target='+str(target)+'  event='+str(event.type())+'  key='+str(event.text())+'  mod='+str(event.modifiers()))
		if(t==QEvent.ShortcutOverride and
				event.modifiers()==Qt.ControlModifier and
				event.key()==Qt.Key_C):
			# logging.info('Ctrl-C detected')
			self.parent.copyText()
			return True
		# elif t==QEvent.KeyPress and event.key()!=Qt.Key_Escape: # prevent all other keypresses from editing cell contents
		# 	return True
		elif t==QEvent.KeyPress:
			key=event.key()
			if key in [Qt.Key_Control]:
				return False
			else:
				logging.info('CustomTableItemDelegate keypress killed')
				# for any other key, cancel the selection and clear focus, but also kill the keystroke
				self.parent.window().clearSelectionAllTables()
				self.parent.window().keyPressEvent(event) # pass the keystroke to the main window
				return True
		return False


class CustomTableView(QTableView):
	def __init__(self,parent,*args,**kwargs):
		self.parent=parent
		QTableView.__init__(self,parent)
		self.setContextMenuPolicy(Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self.contextMenuRequested)
		self.copyAction=QAction('Copy')
		self.copyAction.setShortcut(QKeySequence(Qt.CTRL+Qt.Key_C))
		self.copyAction.setShortcutContext(Qt.WidgetWithChildrenShortcut)
		self.copyAction.triggered.connect(self.copyText)
		self.amendAction=QAction('Amend this entry')
		self.amendAction.triggered.connect(self.amend)
		self.addAction(self.copyAction)
		self.setItemDelegate(CustomTableItemDelegate(self))
		self.sel=''
		self.contextMenuOpened=False
		self.row=None
		self.rowData=None

	# #568 - When the mouse is pressed over the table, first stop any editor and clear the selection,
	#  then open the editor on the clicked cell, with all text selected by default;
	#  this is definitely easier to implement than trying to start the drag-select on the
	#  first mouse press, and probably makes more sense to the user anyway.
	def mousePressEvent(self,e):
		# logging.info('mousePress CustomTableView: pos='+str(e.pos()))
		self.window().clearSelectionAllTables()
		pos=e.pos()
		i=self.indexAt(pos)
		self.setCurrentIndex(i)
		self.edit(i)
		# if called from the top table, self.row is an index into the main radiolog,
		#  but if called from a team table, self.row is an index into that table
		#  so needs to be translated to an index into the main radiolog
		#  see https://stackoverflow.com/questions/61268687
		if self.parent==self.window(): # called from the team tables (parent=MyWindow)
			self.row=self.model().mapToSource(i).row()
		else: # called from the top table (parent=QSplitter)
			self.row=self.rowAt(pos.y())
		self.rowData=self.window().radioLog[self.row]

	# leaveEvent also fires when the context menu is opened; use a flag
	#  here AND in the delegate class to prevent clearSelectionAllTables
	def leaveEvent(self,e):
		# logging.info('customTableView leaveEvent called')
		if not self.contextMenuOpened:
			self.window().clearSelectionAllTables()

	def contextMenuRequested(self,pos):
		# logging.info('custom table context menu requested: pos='+str(pos))
		# logging.info("row:"+str(self.row)+":"+str(self.rowData))
		# only show the context menu if a cell is selected
		# logging.info(' current selection:'+str(self.selectedIndexes()))
		if self.selectedIndexes():
			menu=QMenu()
			menu.setFont(self.window().menuFont)
			self.contextMenuOpened=True
			menu.addAction(self.copyAction)
			self.copyAction.triggered.connect(menu.close)
			menu.addAction(self.amendAction)
			action=menu.exec_(self.mapToGlobal(pos))
			self.contextMenuOpened=False

	def copyText(self):
		t=self.sel
		# logging.info('copyText called: '+t)
		QApplication.clipboard().setText(t)
		self.window().clearSelectionAllTables()
		self.row=None
		self.rowData=None

	def amend(self):
		# logging.info('amend called from table context menu')
		self.window().clearSelectionAllTables()
		# self.row is an index into the main radiolog list;
		#  index conversion was done in mousePressEvent
		self.window().amendEntry(self.row)
		self.row=None
		self.rowData=None


class fsTableModel(QAbstractTableModel):
	header_labels=['Fleet','Device','Callsign','Filtered?','Last Received','','Bumps']
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
		except Exception as e:
			row=index.row()
			col=index.column()
			logging.info(f'Exception in fsTableModel.data for row={row} col={col}:{e}')
			logging.info("arraydata:")
			logging.info(self.arraydata)
		else:
			if index.column()==3:
				if rval==True:
					rval="Filtered"
				if rval==False:
					rval="Unfiltered"
			return rval


# class teamTabsListModel(QAbstractListModel):

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
		if event.type()==QEvent.ShortcutOverride:
			if event.modifiers()==Qt.ControlModifier:
				key=event.key()
				if key==Qt.Key_Up:
					MyWindow.changeActiveMessage(w,'up')
					return True # prevent multiple of these
				elif key==Qt.Key_Down:
					MyWindow.changeActiveMessage(w,'down')
					return True # prevent multiple of these
				elif key==Qt.Key_Z:
					return True # block the default processing of Ctrl+Z
		return super(customEventFilter,self).eventFilter(receiver,event)


class CustomMessageBox(QMessageBox):
	def __init__(self,*args):
		super(CustomMessageBox,self).__init__(*args)
		self.palette=QPalette()

	def keyPressEvent(self,e):
		# - Esc is the same as clicking 'No' on the message box
		# - shift- or ctrl- Enter or Return is the same as clicking 'Yes' on the message box
		# - Enter or Return (without modifier) are blocked, to prevent accidentally finishing the entry
		#    while the message box is open
		# - all other keypresses are preserved as part of the entry, with a beep and throb, so that
		#    typing can continue uninterrupted
		key=e.key()
		mod=e.modifiers()
		if key==Qt.Key_Escape:
			self.close()
		else:
			if mod in [Qt.ShiftModifier,Qt.ControlModifier]: # check this first, since shift or ctrl on their own are an event
				if key in [Qt.Key_Enter,Qt.Key_Return]:
					self.accept()
			elif key in [Qt.Key_Enter,Qt.Key_Return]:
				QApplication.beep()
				logging.info('Enter / Return blocked from custom message box keyPressEvent handler')
			else:
				QApplication.beep()
				self.parent().throb()
				QApplication.sendEvent(self.parent().ui.messageField,e)


def main():
	# better resolution handling on multiple screens
	# from https://stackoverflow.com/a/56140241/3577105
	# Handle high resolution displays:
	if hasattr(Qt, 'AA_EnableHighDpiScaling'):
		QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
	if hasattr(Qt, 'AA_UseHighDpiPixmaps'):
		QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
	app = QApplication(sys.argv)
	eFilter=customEventFilter()
	global w # so that eFilter can call methods of the top level widget
	w = MyWindow(app)
	app.installEventFilter(eFilter)
	w.show()
	sys.exit(app.exec_())

if __name__ == "__main__":
	sys.excepthook = handle_exception
	main()
