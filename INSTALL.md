#Installation

As of Nov 19, 2016, there is no installation script or program.  Installation just involves cloning or downloading this repository, but, there is an important list of prerequisites.  You could consider these to be part of the installation procedure:

1. Python 3.4.2 or higher (32 or 64 bit should be fine since currently this is not compiled)
2. Python modules
 * PyQt 5.4 or higher (pip install pyqt)
 * reportlab (pip install reportlab)
 * pyserial (pip install pyserial)
 * requests (pip install requests)
 * fdfgen (pip install fdfgen)
 * win32api (pip install pypiwin32)
3. GISInternals SDK (http://www.gisinternals.com/release.php - pick the latest release for your platform, such as release-1800-x64-gdal-2-1-2-mapserver-7-0-2)
4. PDFtk Free (https://www.pdflabs.com/tools/pdftk-the-pdf-toolkit/ - download and install the free version; during install, you will be asked if the pdftk directory should be added to your path; make sure you answer 'yes')

After you have all the files from this repo, and all the above prerequisites are in place, you may need to check and/or edit some hardcoded paths in radiolog.py:

Path to the logo that, if the file exists, will appear in the top left of generated printouts:
self.printLogoFileName="radiolog_logo.jpg"
(Note that this file is intentionally not part of the repo, to make sure that only NCSSAR will be using the NCSSAR logo; each SAR group should use their own logo.)

Filename (in the same directory as radiolog.py) of fillable clue report PDF:
self.fillableClueReportPdfFileName="clueReportFillable.pdf"

Path to GISInternals installation:
self.GISInternalsSDKRoot="C:\\GISInternals" # avoid spaces in the path - demons be here

That should do it!  Just run 'python radiolog.py' to run the program.
