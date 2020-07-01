import re
import logging
import utility.logging_helpers

LOG = utility.logging_helpers.getLogger()


def getExtTeamName(teamName):
	if teamName.lower().startswith("all ") or teamName.lower() == "all":
		return "ALL TEAMS"
	name = teamName.replace(' ', '')
	# find index of first number in the name; everything left of that is the 'prefix';
	# assume that everything after the prefix is a number
	firstNum = re.search("[0..9]", name)
	firstNumIndex = -1  # assume there is no number at all
	if firstNum != None:
		firstNumIndex = firstNum.start()
	if firstNumIndex > 0:
		prefix = name[:firstNumIndex]
	else:
		prefix = ""
	LOG.debug("FirstNumIndex:"+str(firstNumIndex)+" Prefix:'"+prefix+"'")
	# allow shorthand team names (t2) to still be inserted in the same sequence as
	# full team names (team2) so the tab list could be: team1 t2 team3
	# but other team names starting with t (tr1, transport1) would be added at the end
	if prefix == 't':
		prefix = 'team'
	# now force everything other than 'team' to be added alphabetically at the end,
	# by prefixing the prefix with 'z_' (the underscore makes it unique for easy pruning later)
	if prefix != 'team':
		prefix = "z_"+prefix
	if firstNum != None:
		rest = name[firstNumIndex:].zfill(5)
	else:
		rest = teamName  # preserve case if there are no numbers
	LOG.debug("prefix="+prefix+" rest="+rest+" name="+name)
	extTeamName = prefix+rest
	LOG.debug("Team Name:"+teamName+": extended team name:"+extTeamName)
	return extTeamName


def getNiceTeamName(extTeamName):
	# prune any leading 'z_' that may have been added for sorting purposes
	extTeamName=extTeamName.replace('z_','')

	# find index of first number in the name; everything left of that is the 'prefix';
	# assume that everything after the prefix is a number
	#  (left-zero-padded to 5 digits)
	firstNum=re.search("[0..9]",extTeamName)
	firstNumIndex=-1 # assume there is no number at all
	prefix=""
	if firstNum:
		firstNumIndex=firstNum.start()
	if firstNumIndex>0:
		prefix=extTeamName[:firstNumIndex]
#		name=prefix.capitalize()+" "+str(int(str(extTeamName[firstNumIndex:])))
		name=prefix.capitalize()+" "+str(extTeamName[firstNumIndex:]).lstrip('0')
	else:
		name=extTeamName
	# finally, remove any leading zeros (necessary for non-'Team' callsigns)
	name=name.lstrip('0')
	LOG.debug("getNiceTeamName("+extTeamName+")")
	LOG.debug("FirstNumIndex:"+str(firstNumIndex)+" Prefix:'"+prefix+"'")
	LOG.debug("Human Readable Name:'"+name+"'")
	return name


def getShortNiceTeamName(niceTeamName):
	# 1. remove spaces, then prune leading 'Team'
	shortNiceTeamName=niceTeamName.replace(' ','')
	shortNiceTeamName=shortNiceTeamName.replace('Team','')

	# 2. remove any leading zeros since this is only used for the tab label
	shortNiceTeamName=shortNiceTeamName.lstrip('0')

	return shortNiceTeamName
