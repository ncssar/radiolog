import os
import logging
from gwpycore import AppActions

LOG = logging.getLogger('main')

KEYMAP_FILENAME = "local/keymap.csv"
DEFAULT_KEYMAP = [
"Action Identifier,Action Label,Key Seq 1,Key Seq 2,Key Seq 3,Key Seq 4,Tip",
"helpInfo,Help Info,F1,,,,Display the help info box",
"optionsDialog,Options Dialog,F2,,,,Open the options dialog",
"printDialog,Print Dialog,F3,,,,Print reports",
"openLog,Open Log,F4,,,,Open a previous log",
"reloadFleetsync,Reload FleetSync,F5,,,,Reload the FleetSync table",
"restoreLastSaved,Restore Last Saved,F6,,,,Restore the last saved files",
"muteFleetsync,Mute FleetSync,F7,,,,Toggle muting FleetSync",
"filterFleetsync,Filter FleetSync,F8,,,,Filter FleetSync",
"toggleTeamHotkeys,Toggle Team Hotkeys,F12,,,,Toggle team hotkeys",
"increaseFont,&Increase Font,=,,,,Increase the font size of the log text by 2 points.",
"decreaseFont,&Decrease Font,-,,,,Decrease the font size of the log text by 2 points.",
"toTeam,To a team,Right,t,,,New Entry: To a Team",
"toTeamsAll,To &All Teams,a,,,,New Entry: To All Teams",
"fromTeam,From a Team,Left,f,Enter,Space,New Entry: From a Team",
"fromTeam1,From Team &1,1,,,,New Entry: From Team 1",
"fromTeam2,From Team &2,2,,,,New Entry: From Team 2",
"fromTeam3,From Team &3,3,,,,New Entry: From Team 3",
"fromTeam4,From Team &4,4,,,,New Entry: From Team 4",
"fromTeam5,From Team &5,5,,,,New Entry: From Team 5",
"fromTeam6,From Team &6,6,,,,New Entry: From Team 6",
"fromTeam7,From Team &7,7,,,,New Entry: From Team 7",
"fromTeam8,From Team &8,8,,,,New Entry: From Team 8",
"fromTeam9,From Team &9,9,,,,New Entry: From Team 9",
"fromTeam10,From Team 1&0,0,,,,New Entry: From Team 10",
"fromSar,From $SAR,s,,,,New entry: From SAR"
]

def initializeMainWindowActions(parent):
    parent.act = AppActions(parent)
    parent.act.loadKeyMapData(DEFAULT_KEYMAP, init_mode=True)
    if os.path.isfile(KEYMAP_FILENAME):
        LOG.info(f"Using shortcut key assignments per: {KEYMAP_FILENAME}")
        try:
            parent.act.loadKeyMapFile(KEYMAP_FILENAME)
        except Exception as e:
            LOG.exception(e)
    parent.act.attachActions()
