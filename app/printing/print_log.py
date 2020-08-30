import argparse
import functools
import logging
import os
import time

from gwpycore import inform_user_about_issue, print_pdf, view_pdf
from PyQt5.QtCore import QCoreApplication
from reportlab.lib import colors, utils
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (Image, Paragraph, SimpleDocTemplate, Spacer,
                                Table, TableStyle)

from app.db.file_management import make_backup_copy
from app.logic.app_state import CONFIG, SWITCHES
from app.logic.teams import getExtTeamName

LOG = logging.getLogger("main")


def printLogHeaderFooter(canvas, doc, printParams: argparse.Namespace, opPeriod="", teams=False):
    formNameText = "Radio Log"
    if teams:
        if isinstance(teams, str):
            formNameText = "Team: " + teams
        else:
            formNameText = "Team Radio Logs"
    canvas.saveState()
    styles = getSampleStyleSheet()
    logoImage = None
    if os.path.isfile(printParams.printLogoFileName):
        LOG.debug("valid logo file " + printParams.printLogoFileName)
        imgReader = utils.ImageReader(printParams.printLogoFileName)
        imgW, imgH = imgReader.getSize()
        imgAspect = imgH / float(imgW)
        logoImage = Image(printParams.printLogoFileName, width=0.54 * inch / float(imgAspect), height=0.54 * inch)
        headerTable = [
            [logoImage, printParams.agencyNameForPrint, "Incident: " + printParams.incidentName, formNameText + " - Page " + str(canvas.getPageNumber())],
            ["", "", "Operational Period: " + str(opPeriod), "Printed: " + time.strftime("%a %b %d, %Y  %H:%M")],
        ]
        t = Table(headerTable, colWidths=[x * inch for x in [0.8, 4.2, 2.5, 2.5]], rowHeights=[x * inch for x in [0.3, 0.3]])
        t.setStyle(
            TableStyle(
                [
                    ("FONT", (1, 0), (1, 1), "Helvetica-Bold"),
                    ("FONT", (2, 0), (3, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (1, 0), (1, 1), 18),
                    ("SPAN", (0, 0), (0, 1)),
                    ("SPAN", (1, 0), (1, 1)),
                    ("LEADING", (1, 0), (1, 1), 20),
                    ("TOPADDING", (1, 0), (1, 0), 0),
                    ("BOTTOMPADDING", (1, 1), (1, 1), 4),
                    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (1, 0), (1, -1), "CENTER"),
                    ("ALIGN", (0, 0), (0, 1), "CENTER"),
                    ("BOX", (0, 0), (-1, -1), 2, colors.black),
                    ("BOX", (2, 0), (-1, -1), 2, colors.black),
                    ("INNERGRID", (2, 0), (3, 1), 0.5, colors.black),
                ]
            )
        )
    else:
        headerTable = [[logoImage, printParams.agencyNameForPrint, "Incident: " + printParams.incidentName, formNameText + " - Page " + str(canvas.getPageNumber())], ["", "", "Operational Period: ", "Printed: " + time.strftime("%a %b %d, %Y  %H:%M")]]
        t = Table(headerTable, colWidths=[x * inch for x in [0.0, 5, 2.5, 2.5]], rowHeights=[x * inch for x in [0.3, 0.3]])
        t.setStyle(
            TableStyle(
                [
                    ("FONT", (1, 0), (1, 1), "Helvetica-Bold"),
                    ("FONT", (2, 0), (3, 0), "Helvetica-Bold"),
                    ("FONTSIZE", (1, 0), (1, 1), 18),
                    ("SPAN", (0, 0), (0, 1)),
                    ("SPAN", (1, 0), (1, 1)),
                    ("LEADING", (1, 0), (1, 1), 20),
                    ("VALIGN", (1, 0), (-1, -1), "MIDDLE"),
                    ("ALIGN", (1, 0), (1, -1), "CENTER"),
                    ("BOX", (0, 0), (-1, -1), 2, colors.black),
                    ("BOX", (2, 0), (-1, -1), 2, colors.black),
                    ("INNERGRID", (2, 0), (3, 1), 0.5, colors.black),
                ]
            )
        )
    w, h = t.wrapOn(canvas, doc.width, doc.height)
    QCoreApplication.processEvents()
    LOG.debug("Page number:" + str(canvas.getPageNumber()))
    LOG.debug("Height:" + str(h))
    LOG.debug("Pagesize:" + str(doc.pagesize))
    t.drawOn(canvas, doc.leftMargin, doc.pagesize[1] - h - 0.5 * inch)  # enforce a 0.5 inch top margin regardless of paper size
    # canvas.grid([x*inch for x in [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5,9,9.5,10,10.5,11]],[y*inch for y in [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7,7.5,8,8.5]])
    LOG.trace("done drawing printLogHeaderFooter canvas")
    canvas.restoreState()
    LOG.trace("end of printLogHeaderFooter")


def printLog(opPeriod, printParams: argparse.Namespace, teams=False):
    """
    Optional argument 'teams': if True, generate one pdf of all individual team logs;
    so, this function should be called once to generate the overall log pdf, and
    again with teams=True to generate team logs pdf
    if 'teams' is an array of team names, just print those team log(s)
    """
    opPeriod = int(opPeriod)
    pdfName = CONFIG.firstWorkingDir + "\\" + printParams.pdfFileName
    teamFilterList = [""]  # by default, print print all entries; if teams=True, add a filter for each team
    msgAdder = ""
    if teams:
        if isinstance(teams, list):
            # recursively call this function for each team in list of teams
            for team in teams:
                printParams.printLog(opPeriod, team)
        elif isinstance(teams, str):
            pdfName = pdfName.replace(".pdf", "_" + teams.replace(" ", "_").replace(".", "_") + ".pdf")
            msgAdder = " for " + teams
            teamFilterList = [teams]
        else:
            pdfName = pdfName.replace(".pdf", "_teams.pdf")
            msgAdder = " for individual teams"
            teamFilterList = []
            for team in printParams.allTeamsList:
                if team != "dummy":
                    teamFilterList.append(team)
    LOG.debug("teamFilterList=" + str(teamFilterList))
    pdfName = pdfName.replace(".pdf", "_OP" + str(opPeriod) + ".pdf")
    LOG.debug("generating radio log pdf: " + pdfName)
    try:
        f = open(pdfName, "wb")
    except:
        inform_user_about_issue(
            f"PDF could not be generated:\n\n{pdfName}\n\nMaybe the file is currently being viewed by another program?  If so, please close that viewer and try again.  As a last resort, the auto-saved CSV file can be printed from Excel or as a plain text file."
        )
        return
    else:
        f.close()
    # note the topMargin is based on what looks good; you would think that a 0.6 table plus a 0.5 hard
    # margin (see t.drawOn above) would require a 1.1 margin here, but, not so.
    doc = SimpleDocTemplate(pdfName, pagesize=landscape(letter), leftMargin=0.5 * inch, rightMargin=0.5 * inch, topMargin=1.03 * inch, bottomMargin=0.5 * inch)  # or pagesize=letter
    # 		printParams.logMsgBox.show()
    # 		QTimer.singleShot(5000,printParams.logMsgBox.close)
    QCoreApplication.processEvents()
    elements = []
    for team in teamFilterList:
        extTeamNameLower = getExtTeamName(team).lower()
        radioLogPrint = []
        styles = getSampleStyleSheet()
        radioLogPrint.append(printParams.header_labels[0:6])
        entryOpPeriod = 1  # update this number when 'Operational Period <x> Begins' lines are found
        # hits=False # flag to indicate whether this team has any entries in the requested op period; if not, don't make a table for this team
        for row in printParams.radioLog:
            opStartRow = False
            # LOG.debug("message:"+row[3]+":"+str(row[3].split()))
            if row[3].startswith("Radio Log Begins:"):
                opStartRow = True
            if row[3].startswith("Operational Period") and row[3].split()[3] == "Begins:":
                opStartRow = True
                entryOpPeriod = int(row[3].split()[2])
            # LOG.debug("desired op period="+str(opPeriod)+"; this entry op period="+str(entryOpPeriod))
            if entryOpPeriod == opPeriod:
                if team == "" or extTeamNameLower == getExtTeamName(row[2]).lower() or opStartRow:  # filter by team name if argument was specified
                    radioLogPrint.append([row[0], row[1], row[2], Paragraph(row[3], styles["Normal"]), Paragraph(row[4], styles["Normal"]), Paragraph(row[5], styles["Normal"])])
        # hits=True
        if not teams:
            radioLogPrint[1][4] = printParams.datum
        LOG.debug("length:" + str(len(radioLogPrint)))
        if not teams or len(radioLogPrint) > 2:  # don't make a table for teams that have no entries during the requested op period
            t = Table(radioLogPrint, repeatRows=1, colWidths=[x * inch for x in [0.5, 0.6, 1.25, 5.5, 1.25, 0.9]])
            t.setStyle(
                TableStyle([("FONT", (0, 0), (-1, -1), "Helvetica"), ("FONT", (0, 0), (-1, 1), "Helvetica-Bold"), ("INNERGRID", (0, 0), (-1, -1), 0.25, colors.black), ("BOX", (0, 0), (-1, -1), 2, colors.black), ("BOX", (0, 0), (5, 0), 2, colors.black)])
            )
            elements.append(t)
            if teams and team != teamFilterList[-1]:  # don't add a spacer after the last team - it could cause another page!
                elements.append(Spacer(0, 0.25 * inch))
    doc.build(elements, onFirstPage=functools.partial(printLogHeaderFooter, opPeriod=opPeriod, printParams=printParams, teams=teams), onLaterPages=functools.partial(printLogHeaderFooter, opPeriod=opPeriod, printParams=printParams, teams=teams))
    if SWITCHES.devmode:
        view_pdf(pdfName)
    else:
        print_pdf(pdfName)
    printParams.radioLogNeedsPrint = False
    make_backup_copy(pdfName)
