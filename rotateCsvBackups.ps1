#  rotateCsvBackups.ps1

#  Windows PowerShell sript to rotate RadioLog CSV backup files
#   (this script is intended to be called from python using
#   subprocess.Popen so that no lag is created in radiolog itself)

#   10-3-18   TMG    First version
#  11-17-18   TMG    do not abort if a file is not found; just go to the next one

param (
	[string[]]$filenames
)

$versionDepth=5

foreach($filename in $filenames) {
	Write-Output "Beginning rotation for $filename..."
	
	if (!(Test-Path $filename)) {
		Write-Warning "$filename could not be found; skipping backup rotation"
	} else {
    	for($i=$versionDepth-1;$i -gt 0; $i--) {
    	#	Write-Output "$i[$filename]"
    		$ip1=$i+1
    		$istr="{0}" -f $i
    		$ip1str="{0}" -f $ip1
    		$src=$filename -replace ".csv","_bak$istr.csv"
    		$dst=$filename -replace ".csv","_bak$ip1str.csv"
    	#	Write-Output "checking for exstince of $src..."
    		if (Test-Path $src) {
    	#		Write-Output "  yes it exists...  $istr --> $ip1str"
    			Move-Item -Force $src $dst
    	#	} else {
    	#		Write-Output "  no it does not exist."
    		}
    	}
    	$bak1=$filename -replace ".csv","_bak1.csv"
    	# Copy-Item will overwrite by default, which is what we want
    	Copy-Item $filename $bak1
    }
}
