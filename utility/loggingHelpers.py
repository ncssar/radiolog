import sys
import logging
from utility.misc_functions import *

MAIN_LOG_NAME = "RadioLog"

class LoggingFilter(logging.Filter):
	"""Do not pass ERRORs to stdout - they already show up on the screen from stderr"""
	def filter(self,record):
		return record.levelno < logging.ERROR

def newLogger(name=MAIN_LOG_NAME):
	"""Initialize a logger (according to how we use it)."""
	logFileName=getFileNameBase("radiolog_log")+".txt"
	LOG = logging.getLogger(name)
	LOG.setLevel(logging.INFO)
	
	# verbose = logging.Formatter("%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s")
	verbose = logging.Formatter("%(levelname)s %(asctime)s %(module)s %(message)s")
	simple = logging.Formatter("%(levelname)s %(message)s")
	
	fh=logging.FileHandler(logFileName)
	fh.setFormatter(verbose)
	fh.setLevel(logging.INFO)
	
	ch=logging.StreamHandler(stream=sys.stdout)
	ch.setFormatter(simple)
	ch.setLevel(logging.INFO)
	ch.addFilter(LoggingFilter())
	
	LOG.addHandler(fh)
	LOG.addHandler(ch)
	LOG.__format__
	return LOG

def handle_exception(exc_type, exc_value, exc_traceback):
	"""
	An override for excepthook that logs uncaught exceptions.
	Note: 'sys.excepthook = handle_exception' must be done inside main().
	See https://stackoverflow.com/a/16993115/3577105
	and https://www.programcreek.com/python/example/1013/sys.excepthook
	"""
	LOG = logging.getLogger(MAIN_LOG_NAME)
	if not issubclass(exc_type, KeyboardInterrupt):
		LOG.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))
	sys.__excepthook__(exc_type, exc_value, exc_traceback)
	# interesting that the program no longer exits after uncaught exceptions
	#  if this function replaces __excepthook__.  Probably a good thing but
	#  it would be nice to undertstand why.
	return

