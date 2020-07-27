from app.logic.exceptions import *
import sys, pytest
from utility.command_line import parse_args

def test_parse():

	# the first argument of sys.argv is the name of the program we are running. The switches start with the second arg.
	switches = parse_args([])
	assert not switches.devmode
	assert not switches.minmode
	assert not switches.nosend

	switches = parse_args(["-d"])
	assert switches.devmode
	assert not switches.minmode
	assert not switches.nosend

	switches = parse_args(["--devel"])
	assert switches.devmode
	assert not switches.minmode
	assert not switches.nosend

	switches = parse_args(["-m"])
	assert not switches.devmode
	assert switches.minmode
	assert not switches.nosend

	switches = parse_args(["--min"])
	assert not switches.devmode
	assert switches.minmode
	assert not switches.nosend

	switches = parse_args(["--nosend"])
	assert not switches.devmode
	assert not switches.minmode
	assert switches.nosend

	switches = parse_args(["--nosend","--devel"])
	assert switches.devmode
	assert not switches.minmode
	assert switches.nosend



def test_help(capsys):
	# When you specifically ask for help, it goes to stdout
	sys.stdout.write("==START==\n")
	with pytest.raises(SystemExit) as pytest_wrapped_e:
		switches = parse_args(["--help"])
		assert pytest_wrapped_e.type is SystemExit
		assert pytest_wrapped_e.value.code == 0
	sys.stdout.write("==END==")
	captured = capsys.readouterr()
	assert captured.out.startswith("==START==\nusage: ")


def test_bad_argument(capsys):
	# When the help is in response to a bad argument, it goes to stderr
	sys.stderr.write("==START==\n")
	with pytest.raises(SystemExit) as pytest_wrapped_e:
		switches = parse_args(["--nosuch"])
		assert pytest_wrapped_e.type is SystemExit
		assert pytest_wrapped_e.value.code == 0
	sys.stderr.write("==END==")
	captured = capsys.readouterr()
	assert captured.err.startswith("==START==\nusage: ")


