import argparse
import logging
import re
import time

from gwpycore.gw_gui.gw_gui_dialogs import ICON_WARN, inform_user_about_issue
from gwpycore.gw_windows_specific.gw_windows_printing import (fill_in_pdf,
                                                              print_pdf,
                                                              view_pdf)
from PyQt5.QtCore import QCoreApplication

from app.db.file_management import make_backup_copy
from app.logic.app_state import CONFIG, SWITCHES

LOG = logging.getLogger("main")


def printClueReport(clueData, printParams: argparse.Namespace):
    if not printParams.fillableClueReportPdfFileName:
        inform_user_about_issue(
            "Reminder: no Clue Report form will be printed, since the fillable clue report PDF does not exist.\n\nThe clue report text is stored as part of the radio message text.\n\nThis warning will automatically close in a few seconds.",
            icon=ICON_WARN,
            title="Clue Report PDF Unavailable",
            timeout=8000,
        )
        return

    ##		header_labels=['#','DESCRIPTION','TEAM','TIME','DATE','O.P.','LOCATION','INSTRUCTIONS','RADIO LOC.']
    # do not use ui object here, since this could be called later, when the clueDialog is not open
    cluePdfName = CONFIG.firstWorkingDir + "\\" + printParams.pdfFileName.replace(".pdf", "_clue" + str(clueData[0]).zfill(2) + ".pdf")
    LOG.trace("generating clue report pdf: " + cluePdfName)

    instructions = clueData[7].lower()
    # initialize all checkboxes to OFF
    instructionsCollect = "collect" in instructions
    instructionsMarkAndLeave = "mark & leave" in instructions
    instructionsDisregard = "disregard" in instructions
    # now see if there are any instructions other than the standard ones above; if so, print them in 'other'
    instructions = re.sub(r"collect", "", instructions)
    instructions = re.sub(r"mark & leave", "", instructions)
    instructions = re.sub(r"disregard", "", instructions)
    instructions = re.sub(r"^[; ]+", "", instructions)  # only get rid of semicolons and spaces before the first word
    instructions = re.sub(r" ; ", "", instructions)  # also get rid of remaining ' ; ' i.e. when first word is not a keyword
    instructions = re.sub(r"; *$", "", instructions)  # also get rid of trailing ';' i.e. when last word is a keyword
    instructionsOther = instructions != ""
    instructionsOtherText = instructions

    if clueData[8] != "":
        radioLocText = "(Radio GPS: " + re.sub(r"\n", "  x  ", clueData[8]) + ")"
    else:
        radioLocText = ""
    fields = {
        "titleField": printParams.agencyNameForPrint,
        "incidentNameField": printParams.incidentName,
        "dateField": time.strftime("%x"),
        "operationalPeriodField": clueData[5],
        "clueNumberField": clueData[0],
        "dateTimeField": clueData[4] + "   " + clueData[3],
        "teamField": clueData[2],
        "descriptionField": clueData[1],
        "locationRadioGPSField": radioLocText,
        "locationField": clueData[6],
        "instructionsCollectField": instructionsCollect,
        "instructionsDisregardField": instructionsDisregard,
        "instructionsMarkAndLeaveField": instructionsMarkAndLeave,
        "instructionsOtherField": instructionsOther,
        "instructionsOtherTextField": instructionsOtherText,
    }
    fill_in_pdf(printParams.fillableClueReportPdfFileName, fields, cluePdfName)
    if SWITCHES.devmode:
        view_pdf(cluePdfName)
    else:
        print_pdf(cluePdfName)
    make_backup_copy(cluePdfName)
