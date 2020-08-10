import re, time

def getFileNameBase(root):
	"""Adds a timestamp to the given string (a root filename)."""
	return root ################################################################# +"_"+timestamp()


def rreplace(s, old, new, occurrence):
	"""
	Replaces only the rightmost <occurrence> occurrences of <old> in <s> with <new>.
	(Used by the undo function when adding new entry text.)
	Credit to 'mg.' at http://stackoverflow.com/questions/2556108
	"""
	li = s.rsplit(old, occurrence)
	return new.join(li)


