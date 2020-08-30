import logging

from PyQt5 import uic
from PyQt5.QtCore import QAbstractTableModel, Qt, QVariant
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import QAbstractItemView, QDialog, QHeaderView

LOG = logging.getLogger("main")


FsFilterDialogSpec = uic.loadUiType("app/ui/fsFilterDialog.ui")[0]


class fsFilterDialog(QDialog, FsFilterDialogSpec):
    """
    fleetsync filtering scheme:
    - maintain a table of all known (received) fleetsync device IDs.  This table is empty at startup.
      columns: fleet, id, callsign, last time, filtered
         callsign may be blank
         filtered is true/false
    - for each incoming FS transmission, add/update the entry for that device, regardless of whether it is filtered.
    - allow the filtered value to be changed from various places
      - fitler dialog - allow click in table cell to toggle
      - team tab right-click menu - should this affect all callsigns belonging to that team?
      - change callsign dialog - show filtered status and allow click to toggle
    - show filtered status in various places
      - team tab - one symbology for all devices filtered, another for some devices filtered
      - main UI filter button - flash a color if anything is filtered (or if FS is muted??)
      - table cell in filter dialog - maybe show rows in groups - filtered first?  or sort by filtered?
    """

    def __init__(self, parent):
        QDialog.__init__(self)
        self.setupUi(self)
        self.setWindowFlags((self.windowFlags() | Qt.WindowStaysOnTopHint) & ~Qt.WindowMinMaxButtonsHint & ~Qt.WindowContextHelpButtonHint)
        self.parent = parent
        self.tableModel = fsTableModel(parent.fsLog, self)
        self.tableView.setModel(self.tableModel)
        self.tableView.setSelectionMode(QAbstractItemView.NoSelection)
        self.tableView.clicked.connect(self.tableClicked)
        self.tableView.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.setFixedSize(self.size())
        self.tableView.setStyleSheet("font-size:12pt")

    def tableClicked(self, index):
        if index.column() == 3:
            self.parent.fsLog[index.row()][index.column()] = not self.parent.fsLog[index.row()][index.column()]
            self.tableView.model().layoutChanged.emit()
            self.parent.fsBuildTeamFilterDict()
            self.parent.fsBuildTooltip()

    def closeEvent(self, event):
        LOG.trace("closing fsFilterDialog")


class fsTableModel(QAbstractTableModel):
    header_labels = ["Fleet", "Device", "Callsign", "Filtered?", "Last Received"]

    def __init__(self, datain, parent=None, *args):
        QAbstractTableModel.__init__(self, parent, *args)
        self.arraydata = datain
        self.filteredIcon = QIcon(QPixmap(":/radiolog_ui/fs_redcircleslash.png"))
        self.unfilteredIcon = QIcon(QPixmap(":/radiolog_ui/fs_greencheckbox.png"))

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        # 		print("headerData:",section,",",orientation,",",role)
        if role == Qt.DisplayRole and orientation == Qt.Horizontal:
            return self.header_labels[section]
        return QAbstractTableModel.headerData(self, section, orientation, role)

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
        elif role == Qt.DecorationRole and index.column() == 3:
            if self.arraydata[index.row()][index.column()] is True:
                # 			return QColor(128,128,255)
                return self.filteredIcon
            else:
                return self.unfilteredIcon
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
            if index.column() == 3:
                if rval is True:
                    rval = "Filtered"
                if rval is False:
                    rval = "Unfiltered"
            return rval
