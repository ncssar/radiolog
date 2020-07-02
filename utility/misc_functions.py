import re, time

def getFileNameBase(root):
	"""Adds a timestamp to the given string (a root filename)."""
	return root ################################################################# +"_"+timestamp()

def timestamp(theTime=time.localtime()):
	return time.strftime("%Y_%m_%d_%H%M%S",theTime)

def rreplace(s, old, new, occurrence):
	"""
	Replaces only the rightmost <occurrence> occurrences of <old> in <s> with <new>.
	(Used by the undo function when adding new entry text.)
	Credit to 'mg.' at http://stackoverflow.com/questions/2556108
	"""
	li = s.rsplit(old, occurrence)
	return new.join(li)


def normName(name):
	"""Normalizes a name by replacing all non-alphanumeric characters with underscores."""
	return re.sub("[^A-Za-z0-9_]+", "_", name)
