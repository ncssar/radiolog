import sys
import logging
from utility.misc_functions import getFileNameBase

MAIN_LOG_NAME = "RadioLog"

class LoggingFilter(logging.Filter):
	"""Do not pass ERRORs to stdout - they already show up on the screen from stderr"""
	def filter(self,record):
		return record.levelno < logging.ERROR

def newConsoleHandler(entryFormat):
	ch = logging.StreamHandler(stream=sys.stdout)
	ch.setFormatter(entryFormat)
	ch.setLevel(logging.INFO)
	ch.addFilter(LoggingFilter())
	return ch

def newFileHandler(name,entryFormat):
	logFileName = getFileNameBase(name+"_log")+".txt"
	fh = logging.FileHandler(logFileName)
	fh.setFormatter(entryFormat)
	return fh

def newLogger(name=MAIN_LOG_NAME):
	"""
	Fetch the named logger. 
	If one of that name does not already exist, then initialize it according to our usage.
	"""
	LOG = logging.getLogger(name)
	if len(LOG.handlers) > 0:
		return LOG

	# This should be the most chatty level we want (individual handlers can be set to less chatty)
	LOG.setLevel(logging.DEBUG)
	LOG.propagate = False

	# We are currently doing anything multi-threaded, so the verbose format doesn't need thread info at this time
	# verbose = logging.Formatter("%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s")
	VERBOSE = logging.Formatter("%(asctime)s [%(module)s] %(levelname)s %(message)s")
	SIMPLE = logging.Formatter("%(levelname)s %(message)s")
	
	LOG.addHandler(newConsoleHandler(SIMPLE))
	LOG.addHandler(newFileHandler(name, VERBOSE))
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

