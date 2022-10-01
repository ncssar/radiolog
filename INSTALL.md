# Installation

## Binary Installer:
There is a binary installer located here: https://github.com/ncssar/radiolog/releases

Download and run radiolog-setup.exe

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

After you have all the files from this repo (download the zip and extract to C:\), 
and all the above prerequisites are in place, you will need to set up the 'local' 
directory.  As of 8-1-19 there is no code in place to create the local directory 
for a fresh installation: you will need to create a dir named 'local' in the 
radiolog install dir (such as C:\radiolog-master\local) and in that directory 
you will need to place radiolog.cfg (can be blank) and an optional logo file 
as spelled out below.

# RadioLog.ini optional settings
Optional file local/radiolog.cfg can be used to change various settings.  That 
file is plain text, and has documentation inside it.

If the 'local' directory does not exist yet, i.e. the first time you run 
radiolog, it will be created as a copy of the 'local_default' directory included 
as part of the installation.

If new radiolog versions contain new user-definable options, 
local_default/radiolog.cfg will contain the new options and documentation.

# radiolog_logo.jpg
You can optionally provide a logo image to be incldued on radiolog printouts 
(except for clue reports).  The file will be scaled to print in the pdf files, 
so a starting size of 200x200 pixels or less should be fine.  Name the file 
local/radiolog_logo.jpg.  Note that a default logo is included in local_default 
so will be copied in to place the first time you run radiolog.  You can then 
delete local/radiolog_logo.jpg or overwrite it with your own logo.


That should do it!  Just run 'python radiolog.py' to run the program.  You may 
want to create a desktop shortcut and use the included icon.
