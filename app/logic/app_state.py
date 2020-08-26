"""
Various globals and constants used through the application
"""

import sys
from app.command_line import parse_args
import argparse


SWITCHES: argparse.Namespace = parse_args(sys.argv[1:])
# print(f"SWITCHES = {SWITCHES}")

CONFIG: argparse.Namespace = argparse.Namespace()

TIMEOUT_DISPLAY_LIST = [["10 sec", 10]]
for n in range(1, 13):
    TIMEOUT_DISPLAY_LIST.append([str(n * 10) + " min", n * 600])



holdSec = 20
continueSec = 20

lastClueNumber = 0
teamStatusDict = {}


