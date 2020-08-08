# On Windows, make uses the shell specified by the SHELL environment variable if it exists (otherwise the ComSpec envvar)
VENV_NAME?=.venv  # ?= means only assign if it doesn't already have a value
BIN=$(VENV_NAME)\Scripts
LIB=${VENV_NAME}\Lib\site-packages
PYTHON=${VENV_NAME}\Scripts\python3
NON_VIRTUAL_PYTHON?=C:\Python38\python
HOST=127.0.0.1
TEST_PATH=.\tests

.PHONY: help clean clean-pyc test examples activate linters requirements gwpycore dev-env format isort lint

help: # If you just say `make`, then this first target is assumed as the goal
	@echo "== One-Time Setup Goals =="
	@echo
	@echo "dev-env -- Prepares for development, including setting up a virtual environment"
	@echo "    (implies: gwpycore and requirements)."
	@echo "qt-designer -- Installs the QT-designer tool."
	@echo
	@echo "== Regular Goals =="
	@echo
	@echo "test -- Runs all of the unit tests."
	@echo "prep -- Prepares for a possible release."
	@echo "standardize -- Apply of the linting tools (format, isort, and lint) to all of the .py files."
	@echo "clean -- Deletes all temporary files."
	@echo "help -- This list."
	@echo
	@echo "== Sub-Goals (can be executed explicitly, if desired) =="
	@echo
	@echo "activate -- 'Activate' the virtual environment."
	@echo "gwpycore -- Clones the gwpycore source code and installs it (symlink-ish)."
	@echo "requirements -- Ensures that all of the modules required by this project are installed (in the virtual env)."
	@echo "format -- Re-formats all of the Python code (with black)."
	@echo "isort -- Cleans up all of the imports (using isort)."
	@echo "lint -- Lints code (using flake8)."

clean: clean-pyc # Deletes all temporary files
	del /F /S build\
	del /F /S dist\
	del /F /S *.pyo
	del /F /S *.egg-info

clean-pyc:
	del /F /S *.pyc

test: clean-pyc | .venv # Runs all of the unit tests
	${PYTHON} -m pytest --verbose --color=yes $(TEST_PATH)


.venv: # Installs a virtual environment for this project
	${NON_VIRTUAL_PYTHON} -m pip install --upgrade pip
	${NON_VIRTUAL_PYTHON} -m venv .venv

activate: | .venv # Force activate the virtual environment
		${BIN}\activate.bat

..\gwpycore\README.adoc: .venv # Clones the gwpycore source code and installs it (symlink-ish)
	git clone git@github.com:gruntwurk/gwpycore.git "..\gwpycore"

gwpycore: ..\gwpycore\README.adoc
	${BIN}\pip install -e ..\gwpycore`

qt-designer: # Install the QT-designer tool
	${NON_VIRTUAL_PYTHON} -m pip install pyqt5_tools

linters: | .venv
	${BIN}\pip install black isort flake8

requirements: | .venv # Ensures that all of the modules required by this project are installed (in the virtual env)
	${BIN}\pip install -r requirements.txt

dev-env: gwpycore requirements linters # Prepares the development environment -- use only once.

# doc: activate | .venv
#     $(VENV_ACTIVATE) && cd docs; make html

prep: standardize # Prepares for a possible release
	${BIN}\pip freeze > frozen_requirements.txt
	# TODO verify the version number

standardize: format isort lint # Apply of the linting tools to all of the .py files

format: | .venv # Re-formats all of the Python code (with black)
	${BIN}\black *.py

isort: | .venv # Cleans up all of the imports (using isort)
	${BIN}\isort *.py

lint: | .venv  # Lints code (using flake8)
	${BIN}\flake8 *.py

