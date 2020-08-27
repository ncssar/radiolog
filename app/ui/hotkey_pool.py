import logging

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QBoxLayout, QLabel, QTabWidget

from app.logic.teams import getShortNiceTeamName

LOG = logging.getLogger("main")


class TeamHotKeys:
    """
    The team hotkeys are what appear above the team tabs when you use F12 to toggle them on.
    While they are on, the assigned hotkeys take precendence over the normal meaning of that key.
    """

    def __init__(self) -> None:
        self.hotkeyDict = {}
        self.nextAvailHotkeyIndex = 0
        self.hotkeyPool = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "q", "w", "e", "r", "t", "y", "u", "i", "o", "p", "a", "s", "d", "f", "g", "h", "j", "k", "l", "z", "x", "c", "v", "b", "n", "m"]

    def getNextAvailHotkey(self):
        """
        Iterate through hotkey pool until finding one that is not taken
        """
        for hotkey in self.hotkeyPool:
            if hotkey not in self.hotkeyDict:
                return hotkey
        return None  # no available hotkeys

    def assignTeamHotkey(self, niceTeamName: str):
        # if the first initial of the team name is availabe, use it; otherwise assign the next available key
        hotkey = getShortNiceTeamName(niceTeamName)[0].lower()
        if hotkey in self.hotkeyDict:
            hotkey = self.getNextAvailHotkey()
        LOG.debug(f"Assigning hotkey '{hotkey}' to {niceTeamName}")
        if hotkey:
            self.hotkeyDict[hotkey] = niceTeamName
        else:
            LOG.debug("Team hotkey pool has been used up.  Not setting any hotkeyDict entry for " + niceTeamName)
        return hotkey

    def getTeam(self, key):
        if key in self.hotkeyDict.keys():
            return self.hotkeyDict[key]
        return None

    def freeHotkey(self, niceTeamName, tabWidget: QTabWidget):
        """
        Free the hotkey, and reassign it to the first (if any) displayed callsign that has no hotkey
        """
        hotkeyRDict = {v: k for k, v in self.hotkeyDict.items()}
        if niceTeamName in hotkeyRDict:
            hotkey = hotkeyRDict[niceTeamName]
            LOG.debug("Freeing hotkey '" + hotkey + "' which was used for callsign '" + niceTeamName + "'")
            del self.hotkeyDict[hotkey]
            bar = tabWidget.tabBar()
            taken = False
            for i in range(1, bar.count()):
                if not taken:
                    callsign = bar.tabWhatsThis(i)
                    LOG.debug("checking tab#" + str(i) + ":" + callsign)
                    if callsign not in hotkeyRDict and not callsign.lower().startswith("spacer"):
                        LOG.debug("  does not have a hotkey; using the freed hotkey '" + hotkey + "'")
                        self.hotkeyDict[hotkey] = callsign
                        taken = True

    def rebuildTeamHotkeys(self, teamHotkeysHLayout: QBoxLayout, tabWidget: QTabWidget):
        """
        Delete all child widgets
        """
        while teamHotkeysHLayout.count():
            child = teamHotkeysHLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        bar = tabWidget.tabBar()

        hotkeyRDict = {v: k for k, v in self.hotkeyDict.items()}
        # 		LOG.debug("tab count="+str(bar.count()))
        for i in range(0, bar.count()):
            #  An apparent bug causes the tabButton (a label) to not have a text attrubite;
            #  so, use the whatsThis attribute instead.
            callsign = bar.tabWhatsThis(i)
            hotkey = hotkeyRDict.get(callsign, "")
            l = QLabel(hotkey)
            l.setFixedWidth(bar.tabRect(i).width())
            l.setStyleSheet("border:0px solid black;margin:0px;font-style:italic;font-size:14px;background-image:url(:/radiolog_ui/blank-computer-key.png) 0 0 30 30;")
            l.setAlignment(Qt.AlignCenter)
            teamHotkeysHLayout.addWidget(l)
        teamHotkeysHLayout.addStretch()
