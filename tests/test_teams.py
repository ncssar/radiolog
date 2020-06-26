from app_logic.teams import *

def test_getExtTeamName():
	assert getExtTeamName("all") == "ALL TEAMS"
	assert getExtTeamName("all units") == "ALL TEAMS"
	assert getExtTeamName("all teams") == "ALL TEAMS"
	assert getExtTeamName("All Teams") == "ALL TEAMS"
	assert getExtTeamName("ALL TEAMS") == "ALL TEAMS"
	# TODO (more)

def test_getNiceTeamName():
	assert getNiceTeamName("Team1") == "Team1"
	assert getNiceTeamName("Team02") == "Team 2"
	assert getNiceTeamName("TeamAlpha") == "TeamAlpha"
	assert getNiceTeamName("z_TeamBravo") == "TeamBravo"
	# TODO (more)


def test_getShortNiceTeamName():
	assert getShortNiceTeamName("Team 01") == "1"
	assert getShortNiceTeamName("Team 2") == "2"
	assert getShortNiceTeamName(" Team3") == "3"
	assert getShortNiceTeamName(" Team400") == "400"
	assert getShortNiceTeamName("5") == "5"
	assert getShortNiceTeamName("Team Alpha") == "Alpha"
	assert getShortNiceTeamName("Bravo") == "Bravo"
	# TODO (more)


