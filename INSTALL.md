# Installation

## Binary Installer:
There is a binary installer located here: https://github.com/ncssar/radiolog/releases

Download and run radiolog-setup.exe to install on Windows.

## To Install from Source:

1. Python 3.4.2 or higher - install for All Users, which may require you to run 
the installer as Administrator, and also to check 'install for all users' in the 
Advanced Options, and change the installation directory to C:\Python-<version> 
to avoid spaces in the directory name, but this will require you to edit the 
properties of Lib\site-packages in the python install directory to remove the 
read-only flag (and apply to all subdirectories) in order to allow the following 
steps.
2. Python Modules:
   1. pip install -r requirements.txt
3. Adobe Acrobat Reader must be installed and must have been run once to 
initialize itself and to set itself as the default application for pdf viewing; 
otherwise the terminal will show a win32api error during printing.  Not sure why 
this is, but, we found a stackoverflow thread where someone else had the same issue.
4. Liberation Sans font, if not already installed through the operating system 
(acquire the Liberation Sans .ttf file(s), right-click to install).  You will 
know if you are missing it when a generated PDF during print will show up with 
a bunch of dots instead of letters.

# RadioLog.ini Optional Settings
On Windows settings for RadioLog can be configured in an INI file. This file
on Windows is generally located here:
<Drive>:\Users\<Current User>\AppData\Roaming\NCSSAR\RadioLog.ini

If new RadioLog versions contain new user-definable options, 
local_default/Radiolog.ini will contain the new options and documentation.

# radiolog_logo.jpg
You can optionally provide a logo image to be included on RadioLog printouts 
(except for clue reports).  The file will be scaled to print in the pdf files, 
so a starting size of 200x200 pixels or less should be fine. On Windows this 
file should be located at: 
<Drive>:\Users\<Current User>\AppData\Roaming\NCSSAR\RadioLog\
Name the file radiolog_logo.jpg.  Note that a default logo is included in local_default 
so will be copied in to place the first time you run RadioLog.  You can then 
delete radiolog_logo.jpg or overwrite it with your own logo.


That should do it!  Just run 'python radiolog.py' to run the program.  You may 
want to create a desktop shortcut and use the included icon.
