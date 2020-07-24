import re
import logging
import utility.logging_helpers

LOG = utility.logging_helpers.getLogger()

PHONETIC_DICT = {"A": "Alpha",
                 "B": "Bravo",
                 "C": "Charlie",
                 "D": "Delta",
                 "E": "Echo",
                 "F": "Foxtrot",
                 "G": "Golf",
                 "H": "Hotel",
                 "I": "India",
                 "J": "Juliet",
                 "K": "Kilo",
                 "L": "Lima",
                 "M": "Mike",
                 "N": "November",
                 "O": "Oscar",
                 "P": "Papa",
                 "Q": "Quebec",
                 "R": "Romeo",
                 "S": "Sierra",
                 "T": "Tango",
                 "U": "Uniform",
                 "V": "Victor",
                 "W": "Whiskey",
                 "X": "Xray",
                 "Y": "Yankee",
                 "Z": "Zulu"}
PHONETIC_RE_GROUP = r"(alpha|bravo|charlie|delta|echo|foxtrot|golf|hotel|india|juliet|kilo|lima|mike|november|oscar|papa|quebec|romeo|sierra|tango|uniform|victor|whiskey|xray|yankee|zulu)"

flags = re.IGNORECASE
ALL_TEAMS_PATTERN = re.compile(r"all", flags)
# In all of the following patterns, the first group of parens is the prefix, the second is the team identifier, and the third is the suffix
NUMERIC_NAME_PATTERN = re.compile(r"([^0-9]*)([0-9]+)(.*)", flags)
PHONETIC_NAME_PATTERN = re.compile(r"(.*)" + PHONETIC_RE_GROUP + r"(.*)", flags)
SINGLE_LETTER_NAME_PATTERN = re.compile(r"(.+)\s+([A-Z])([^A-Z]*)", flags)
SINGLE_LETTER_ONLY_PATTERN = re.compile(r"()([A-Z])([^A-Z]*)", flags)

def getExtTeamName(teamName):
	"""
	Given a haphazardly typed in team name, extend it into something formal and sortable.

	- "t" is short for "team"
	- No prefix at all is assumed to be "team"
	- Any other prefix is allowed (e.g. transport, ranger, CAP) but it will be prefixed with "z_" so that it will sort after the regular teams.
	- Team names can be numeric (team 1, Team 101, 1)
	- Numeric team names can have non-numeric suffixes (1a, 1lead, 1 driver)
	- Team names can be phonetic (team alpha, Team Bravo, charlie, t delta)
	- Team names can be single letter (team a, Team B, c, t d), but there must be a space before the letter (so not "teama" nor "td")
	- Full phonetic team names can have a suffix of any kind (alpha1, alpha 1, Alpha1, Alpha Lead, alphalead)
	- Letter-only team names can have numeric suffixes (a1, t a1, team a 1, transp a1)

	Note: Single letter team names are automatically expanded to the full phonetic (a -> Alpha)
	"""
	(prefix, ident, suffix) = ("","","")
	name = teamName.strip()
	LOG.debug(f"teamName = {teamName} -> name = {name}")

	if (m := ALL_TEAMS_PATTERN.match(name)):
		return "ALL TEAMS"

	if (m := PHONETIC_NAME_PATTERN.fullmatch(name)):
		LOG.debug("Matched phonetic")
		(prefix, ident, suffix) = m.group(1, 2, 3)
		ident = ident.capitalize()
	elif (m := SINGLE_LETTER_NAME_PATTERN.fullmatch(name)) or (m := SINGLE_LETTER_ONLY_PATTERN.fullmatch(name)):
		LOG.debug("Matched single letter")
		(prefix, ident, suffix) = m.group(1, 2, 3)
		suffix = suffix.strip()
		LOG.debug(f"Single letter as parsed: prefix = {prefix}, team identifier = {ident}, suffix = {suffix}")
		# In the special case of the letter T followed by digits, it's considered "Team 123" not "Team Tango 123"
		if prefix == "" and ident.lower() == "t" and suffix.isdigit():
			(prefix, ident, suffix) = (ident, suffix.zfill(5), "")
		else:
			ident = PHONETIC_DICT[ident.upper()]
	elif (m := NUMERIC_NAME_PATTERN.fullmatch(name)):
		# Note: the single-letter test needs to come before this one so that "x1", for example, is considered Team Xray with a suffix of 1, rather than Team 1 with a prefix of x
		LOG.debug("Matched numeric")
		(prefix, ident, suffix) = m.group(1, 2, 3)
		ident = ident.zfill(5)
	else:
		LOG.warning(f"Conversion from a typed-in team name ({teamName}) to a formal/extended name failed. Leaving as is.")
		return teamName

	LOG.debug(f"As parsed: prefix = {prefix}, team identifier = {ident}, suffix = {suffix}")
	prefix = prefix.lower().strip()

	# Ensure that regular teams sort to the front
	if prefix in ('', 't', 'team'):
		prefix = 'team'
	else:
		prefix = "z_"+prefix

	extTeamName = prefix + ident + suffix
	LOG.debug(f"Team Name: {teamName} -> extended team name: {extTeamName}")
	return extTeamName


def getNiceTeamName(extTeamName):
	"""
	Converts a formal, expanded team name (see above) to something that is more human readable.
	e.g. z_TransportAlpha2 -> Transport Alpha2
	"""
	# prune any leading 'z_' that may have been added for sorting purposes
	name=extTeamName.strip().replace('z_','')

	if (m := ALL_TEAMS_PATTERN.match(name)):
		return "ALL TEAMS"

	if (m := PHONETIC_NAME_PATTERN.fullmatch(name)):
		LOG.debug("Matched phonetic")
		(prefix, ident, suffix) = m.group(1, 2, 3)
	elif (m := NUMERIC_NAME_PATTERN.fullmatch(name)):
		LOG.debug("Matched numeric")
		(prefix, ident, suffix) = m.group(1, 2, 3)
		ident = ident.lstrip('0')
	else:
		LOG.warning(f"Conversion from a formal/extended name ({extTeamName}) to a nice name failed. Leaving as is.")
		return name

	return prefix.capitalize() + " " + ident + suffix


def getShortNiceTeamName(niceTeamName):
	if niceTeamName.upper() == "ALL TEAMS":
		return "ALL"
	return niceTeamName.replace(' ','').replace('Team','').lstrip('0')
