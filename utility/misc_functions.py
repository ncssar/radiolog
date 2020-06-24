import time

def getFileNameBase(root):
	"""Adds a timestamp to the given string (a root filename)."""
	return root+"_"+time.strftime("%Y_%m_%d_%H%M%S")

