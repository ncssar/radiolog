#Installation

As of Nov 19, 2016, there is no installation script or program.  Installation just involves cloning or downloading this repository, but, there is an important list of prerequisites.  You could consider these to be part of the installation procedure:

1. Python 3.4.2 or higher - install for All Users, which may require you to run the installer as Administrator, and also to check 'install for all users' in the Advanced Options, which should place python in the Program Files [(x86] directory - this is important for subsequent steps, i.e. for GISInternals to be able to detect the python installation (32 or 64 bit should be fine since currently this is not compiled)
2. Python modules
 * PyQt 5.4 or higher (pip install pyqt5)
 * reportlab (pip install reportlab)
 * pyserial (pip install pyserial)
 * requests (pip install requests)
 * fdfgen (pip install fdfgen)
 * win32api (pip install pypiwin32)
3. GISInternals SDK (http://www.gisinternals.com/release.php - pick the latest release for your platform, such as release-1911-x64-gdal-3-0-0-mapserver-7-4-0, and within that, select the compiled binaries in a single .zip package; life will be easier in later steps if you unzip to C:\ then rename C:\release-..... to C:\GISInternals, such that C:\GISInternals\bin\proj\apps\cs2cs.exe exists  (the .msi installers may have a problem detecting your python installation))
4. PDFtk Free (https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/ - download and install the free version; during install, you will be asked if the pdftk directory should be added to your path; make sure you answer 'yes')
5. Adobe Acrobat Reader must be installed and must have been run once to initialize itself; otherwise the terminal will show a win32api error during printing.  Not sure why this is, but, we found a stackoverflow thread where someone else had the same issue.
6. Liberation Sans font, if not already installed through the operating system (acquire the Liberation Sans .ttf file, right-click to install).  You will know if you are missing it when a generated PDF during print will show up with a bunch of dots instead of letters.

After you have all the files from this repo, and all the above prerequisites are in place, you may need to check and/or edit some hardcoded paths in radiolog.py:

Path to the logo that, if the file exists, will appear in the top left of generated printouts:
self.printLogoFileName="radiolog_logo.jpg"
(Note that this file is intentionally not part of the repo, to make sure that only NCSSAR will be using the NCSSAR logo; each SAR group should use their own logo.)

Filename (in the same directory as radiolog.py) of fillable clue report PDF:
self.fillableClueReportPdfFileName="clueReportFillable.pdf"

Path to GISInternals installation, i.e. the directory that contains bin\proj\apps\cs2cs.exe:
self.GISInternalsSDKRoot="C:\\GISInternals" # avoid spaces in the path - demons be here

That should do it!  Just run 'python radiolog.py' to run the program.
