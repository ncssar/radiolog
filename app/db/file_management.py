import logging
import os
import shutil
from pathlib import Path
from typing import Optional, Tuple
from gwpycore import inform_user_about_issue, ICON_INFO

from app.logic.app_state import CONFIG

LOG = logging.getLogger("main")
FIRST_TIME_INSTALL_FLAG = "first_time_install.txt"


def getFileNameBase(root):
    """Adds a timestamp to the given string (a root filename)."""
    return root  # +"_"+timestamp()


def ensureLocalDirectoryExists():
    """
    create the local dir if it doesn't already exist, and populate it
    with files from local_default.
    """
    if os.path.isfile(FIRST_TIME_INSTALL_FLAG):
        CONFIG.first_time_install = True
        os.remove(FIRST_TIME_INSTALL_FLAG)

    issue = ""
    if not os.path.isdir("local"):
        if CONFIG.first_time_install:
            inform_user_about_issue("Created a 'local' folder based on 'local_default'. You may want to edit local/radiolog.cfg", icon=ICON_INFO,
                                    title="First Time Install")
        else:
            issue = "Not a first-time install, yet 'local' directory not found; copying 'local_default' to 'local'; you may want to edit local/radiolog.cfg"
            LOG.error(issue)
        shutil.copytree("local_default", "local")
    elif not os.path.isfile("local/radiolog.cfg"):
        issue = "'local' directory was found but did not contain radiolog.cfg; copying from local_default"
        LOG.error(issue)
        shutil.copyfile("local_default/radiolog.cfg", "local/radiolog.cfg")
    return issue


def determine_rotate_method() -> Tuple[Optional[str], Optional[str]]:
    rotateScript = None
    rotateDelimiter = None
    if os.name == "nt":
        LOG.info("Operating system is Windows.")
        if shutil.which("powershell.exe"):
            LOG.info("PowerShell.exe is in the path.")
            rotateScript = "powershell.exe -ExecutionPolicy Bypass .\\resources\\rotateCsvBackups.ps1 -filenames "
            rotateDelimiter = ","
        else:
            LOG.warn("PowerShell.exe is not in the path; poweshell-based backup rotation script cannot be used.")
    else:
        LOG.warn("Operating system is not Windows.  Powershell-based backup rotation script cannot be used.")
    return (rotateScript, rotateDelimiter)


def viable_2wd():
    """
    Returns the Path() of the second working dir, if it exists and we're using it.
    Otherwise, None.
    """
    if CONFIG.use2WD and CONFIG.secondWorkingDir and os.path.isdir(CONFIG.secondWorkingDir):
        return Path(CONFIG.secondWorkingDir)
    return None


def make_backup_copy(filename):
    if (path2wd := viable_2wd()) :
        LOG.debug(f"Copying {filename} to {path2wd}")
        shutil.copy(filename, path2wd)


__all__ = ("getFileNameBase", "ensureLocalDirectoryExists", "determine_rotate_method", "make_backup_copy", "viable_2wd")
