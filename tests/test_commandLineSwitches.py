from utility.command_line import CommandLineSwitches

def test_parse():

	switches = CommandLineSwitches()
	
	# the first argument of sys.argv is the name of the program we are running. The switches start with the second arg.
	switches.parse(["test"])
	assert not switches.develMode
	assert not switches.minMode
	assert not switches.noSend

	switches.parse(["test", "-devel"])
	assert switches.develMode
	assert not switches.minMode
	assert not switches.noSend

	switches.parse(["test", "-min"])
	assert not switches.develMode
	assert switches.minMode
	assert not switches.noSend

	switches.parse(["test", "-noSend"])
	assert not switches.develMode
	assert not switches.minMode
	assert switches.noSend

	switches.parse(["test", "-noSend","-devel"])
	assert switches.develMode
	assert not switches.minMode
	assert switches.noSend

	switches.parse(["test", "-NoSuchArg"])
	assert not switches.develMode
	assert not switches.minMode
	assert not switches.noSend



