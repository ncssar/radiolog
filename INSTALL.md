# Installation

As of Nov 19, 2016, there is no installation script or program.  Installation just involves cloning or downloading this repository, but, there is an important list of prerequisites.  You could consider these to be part of the installation procedure:

1. Python 3.4.2 or higher - install for All Users, which may require you to run the installer as Administrator, and also to check 'install for all users' in the Advanced Options, and change the installation directory to C:\Python-<version> to avoid spaces in the directory name, but this will require you to edit the properties of Lib\site-packages in the python install directory to remove the read-only flag (and apply to all subdirectories) in order to allow the following steps
2. Python modules
 * PyQt 5.4 or higher (pip install pyqt5)
 * reportlab (pip install reportlab)
 * pyserial (pip install pyserial)
 * requests (pip install requests)
 * fdfgen (pip install fdfgen)
 * win32api (pip install pypiwin32)
3. GISInternals SDK (http://www.gisinternals.com/release.php - pick the latest release for your platform, such as release-1911-x64-gdal-3-0-0-mapserver-7-4-0, and within that, select the compiled binaries in a single .zip package; life will be easier in later steps if you unzip to C:\ then rename C:\release-..... to C:\GISInternals, such that C:\GISInternals\bin\proj\apps\cs2cs.exe exists  (the .msi installers may have a problem detecting your python installation))
4. PDFtk Free (https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/ - download and install the free version; during install, you will be asked if the pdftk directory should be added to your path; make sure you answer 'yes')
5. Adobe Acrobat Reader must be installed and must have been run once to initialize itself and to set itself as the default application for pdf viewing; otherwise the terminal will show a win32api error during printing.  Not sure why this is, but, we found a stackoverflow thread where someone else had the same issue.
6. Liberation Sans font, if not already installed through the operating system (acquire the Liberation Sans .ttf file(s), right-click to install).  You will know if you are missing it when a generated PDF during print will show up with a bunch of dots instead of letters.

After you have all the files from this repo (download the zip and extract to C:\), and all the above prerequisites are in place, you will need to set up the 'local' directory.  As of 8-1-19 there is no code in place to create the local directory for a fresh installation: you will need to create a dir named 'local' in the radiolog install dir (such as C:\radiolog-master\local) and in that directory you will need to place radiolog.cfg (can be blank) and an optional logo file as spelled out below.

# radiolog.cfg optional settings
Optional file local/radiolog.cfg can be used to change various settings.  That file is plain text, and has documentation inside it.

If the 'local' directory does not exist yet, i.e. the first time you run radiolog, it will be created as a copy of the 'local_default' directory included as part of the installation.

If new radiolog versions contain new user-definable options, local_default/radiolog.cfg will contain the new options and documentation.

# radiolog_logo.jpg
You can optionally provide a logo image to be incldued on radiolog printouts (except for clue reports).  The file will be scaled to print in the pdf files, so a starting size of 200x200 pixels or less should be fine.  Name the file local/radiolog_logo.jpg.  Note that a default logo is included in local_default so will be copied in to place the first time you run radiolog.  You can then delete local/radiolog_logo.jpg or overwrite it with your own logo.


That should do it!  Just run 'python radiolog.py' to run the program.  You may want to create a desktop shortcut and use the included icon.
