import os,shutil,logging
import utility.logging_helpers

LOG = utility.logging_helpers.getLogger()

def ensureLocalDirectoryExists():
	"""
	create the local dir if it doesn't already exist, and populate it
	with files from local_default.
	"""
	issue = ""
	if not os.path.isdir("local"):
		issue = "'local' directory not found; copying 'local_default' to 'local'; you may want to edit local/radiolog.cfg"
		LOG.warn(issue)
		shutil.copytree("local_default", "local")
	elif not os.path.isfile("local/radiolog.cfg"):
		issue = "'local' directory was found but did not contain radiolog.cfg; copying from local_default"
		LOG.warn(issue)
		shutil.copyfile("local_default/radiolog.cfg", "local/radiolog.cfg")
	return issue
