from app.db.file_management import make_backup_copy
import logging
import functools
import argparse
import os
from time import time

from app.logic.app_state import SWITCHES
from PyQt5.QtCore import QCoreApplication
from gwpycore import inform_user_about_issue, print_pdf, view_pdf
from reportlab.lib import colors, utils
from reportlab.lib.pagesizes import letter, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

LOG = logging.getLogger('main')


def printClueLogHeaderFooter(canvas, doc, printParams: argparse.Namespace, opPeriod=""):
    canvas.saveState()
    styles = getSampleStyleSheet()
    logoImage = None
    if os.path.isfile(printParams.printLogoFileName):
        imgReader = utils.ImageReader(printParams.printLogoFileName)
        imgW, imgH = imgReader.getSize()
        imgAspect = imgH / float(imgW)
        logoImage = Image(printParams.printLogoFileName, width=0.54 * inch / float(imgAspect), height=0.54 * inch)
        headerTable = [
            [logoImage, printParams.agencyNameForPrint, "Incident: " + printParams.incidentName, "Clue Log - Page " + str(canvas.getPageNumber())],
                ["", "", "Operational Period: " + str(opPeriod), "Printed: " + time.strftime("%a %b %d, %Y  %H:%M")]]
        t = Table(headerTable, colWidths=[x * inch for x in [0.8, 4.2, 2.5, 2.5]], rowHeights=[x * inch for x in [0.3, 0.3]])
        t.setStyle(TableStyle([('FONT', (1, 0), (1, 1), 'Helvetica-Bold'),
                                ('FONTSIZE', (1, 0), (1, 1), 18),
                                        ('SPAN', (0, 0), (0, 1)),
                                        ('SPAN', (1, 0), (1, 1)),
                                        ('LEADING', (1, 0), (1, 1), 20),
                                        ('TOPADDING', (1, 0), (1, 0), 0),
                                        ('BOTTOMPADDING', (1, 1), (1, 1), 4),
                                ('VALIGN', (0, 0), (-1, -1), "MIDDLE"),
                                ('ALIGN', (1, 0), (1, -1), "CENTER"),
                                        ('ALIGN', (0, 0), (0, 1), "CENTER"),
                                        ('BOX', (0, 0), (-1, -1), 2, colors.black),
                                        ('BOX', (2, 0), (-1, -1), 2, colors.black),
                                        ('INNERGRID', (2, 0), (3, 1), 0.5, colors.black)]))
    else:
        headerTable = [
            [logoImage, printParams.agencyNameForPrint, "Incident: " + printParams.incidentName, "Clue Log - Page " + str(canvas.getPageNumber())],
                ["", "", "Operational Period: " + str(opPeriod), "Printed: " + time.strftime("%a %b %d, %Y  %H:%M")]]
        t = Table(headerTable, colWidths=[x * inch for x in [0.0, 5, 2.5, 2.5]], rowHeights=[x * inch for x in [0.3, 0.3]])
        t.setStyle(TableStyle([('FONT', (1, 0), (1, 1), 'Helvetica-Bold'),
                                ('FONTSIZE', (1, 0), (1, 1), 18),
                                        ('SPAN', (0, 0), (0, 1)),
                                        ('SPAN', (1, 0), (1, 1)),
                                        ('LEADING', (1, 0), (1, 1), 20),
                                ('VALIGN', (1, 0), (-1, -1), "MIDDLE"),
                                ('ALIGN', (1, 0), (1, -1), "CENTER"),
                                        ('BOX', (0, 0), (-1, -1), 2, colors.black),
                                        ('BOX', (2, 0), (-1, -1), 2, colors.black),
                                        ('INNERGRID', (2, 0), (3, 1), 0.5, colors.black)]))
    w, h = t.wrapOn(canvas, doc.width, doc.height)
# 		self.clueLogMsgBox.setInformativeText("Generating page "+str(canvas.getPageNumber()))
    QCoreApplication.processEvents()
    LOG.debug("Page number:" + str(canvas.getPageNumber()))
    LOG.debug("Height:" + str(h))
    LOG.debug("Pagesize:" + str(doc.pagesize))
    t.drawOn(canvas, doc.leftMargin, doc.pagesize[1] - h - 0.5 * inch)  # enforce a 0.5 inch top margin regardless of paper size
    LOG.trace("done drawing printClueLogHeaderFooter canvas")
    canvas.restoreState()
    LOG.trace("end of printClueLogHeaderFooter")


def printClueLog(opPeriod, printParams: argparse.Namespace):
    ##      header_labels=['#','DESCRIPTION','TEAM','TIME','DATE','O.P.','LOCATION','INSTRUCTIONS','RADIO LOC.']
    opPeriod = int(opPeriod)
    clueLogPdfFileName = printParams.firstWorkingDir + "\\" + printParams.pdfFileName.replace(".pdf", "_clueLog_OP" + str(opPeriod) + ".pdf")
    LOG.trace("generating clue log pdf: " + clueLogPdfFileName)
    try:
        f = open(clueLogPdfFileName, "wb")
    except:
        inform_user_about_issue("PDF could not be generated:\n\n" + clueLogPdfFileName + "\n\nMaybe the file is currently being viewed by another program?  If so, please close that viewer and try again.  As a last resort, the auto-saved CSV file can be printed from Excel or as a plain text file.",
                                timeout=10000)
        return
    else:
        f.close()
    # note the topMargin is based on what looks good; you would think that a 0.6 table plus a 0.5 hard
    # margin (see t.drawOn above) would require a 1.1 margin here, but, not so.
    doc = SimpleDocTemplate(clueLogPdfFileName, pagesize=landscape(letter), leftMargin=0.5*inch, rightMargin=0.5*inch, topMargin=1.03*inch, bottomMargin=0.5*inch) # or pagesize=letter
    QCoreApplication.processEvents()
    elements = []
    styles = getSampleStyleSheet()
    clueLogPrint = []
    clueLogPrint.append(printParams.clue_log_header_labels[0:5] + printParams.clue_log_header_labels[6:8])  # omit operational period
    for row in printParams.clueLog:
        LOG.debug("clue: opPeriod=" + str(opPeriod) + "; row=" + str(row))
        if (str(row[5]) == str(opPeriod) or row[1].startswith("Operational Period "+str(opPeriod)+" Begins:") or (opPeriod == 1 and row[1].startswith("Radio Log Begins:"))):
            clueLogPrint.append([row[0], Paragraph(row[1], styles['Normal']), row[2], row[3],row[4],Paragraph(row[6],styles['Normal']),Paragraph(row[7],styles['Normal'])])
    clueLogPrint[1][5] = printParams.datum
    if len(clueLogPrint) > 2:
        ##			t=Table(clueLogPrint,repeatRows=1,colWidths=[x*inch for x in [0.6,3.75,.9,0.5,1.25,3]])
        t = Table(clueLogPrint, repeatRows=1, colWidths=[x*inch for x in [0.3, 3.75,0.9,0.5,0.8,1.25,2.5]])
        t.setStyle(TableStyle([('F/generating clue llONT', (0, 0), (-1, -1),'Helvetica'),
                                ('FONT', (0, 0), (-1, 1),'Helvetica-Bold'),
                                ('INNERGRID', (0, 0), (-1, -1), 0.25, colors.black),
                                ('BOX', (0, 0), (-1, -1), 2, colors.black),
                                ('BOX', (0, 0), (6, 0), 2, colors.black)]))
        elements.append(t)
        doc.build(elements, onFirstPage=functools.partial(printClueLogHeaderFooter, printParams=printParams, opPeriod=opPeriod), onLaterPages=functools.partial(printClueLogHeaderFooter, printParams=printParams, opPeriod=opPeriod))
# 			self.clueLogMsgBox.setInformativeText("Finalizing and Printing...")
        if SWITCHES.devmode:
            view_pdf(clueLogPdfFileName)
        else:
            print_pdf(clueLogPdfFileName)
        make_backup_copy(clueLogPdfFileName)

