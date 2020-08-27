import logging

import serial
from serial.serialutil import SerialException
from serial.tools.list_ports import comports

LOG = logging.getLogger("main")


class FleetSync:
    def __init__(self, devmode=False) -> None:
        self.comPortTryList = []
        self.openPortsActivelyScanning = []
        self.fsBuffer = ""
        self.comPortScanInProgress = False
        self.firstComPortAlive = False
        self.secondComPortAlive = False
        self.firstComPortFound = False
        self.secondComPortFound = False

    ##		if devmode:
    ##			self.comPortTryList=[serial.Serial("\\\\.\\CNCB0")] # DEVEL

    def search_for_active_com_ports(self):
        """
        opening a port quickly, checking for waiting input, and closing on each iteration does not work; the
        com port must be open when the input begins, in order to catch it in the inWaiting internal buffer.
        1. go through each already-open com port to check for waiting data; if valid Fleetsync data is
                found, then we have the correct com port, abort the rest of the scan
        2. (only if no valid data was found in step 1) list com ports; open any new finds and close any
                stale ports (i.e. existed in the list in previous iterations but not in the list now)
        """
        if self.comPortScanInProgress:
            # If a scan is already in progress (taking longer than 1 second) don't start another one.
            return

        if self.firstComPortFound and self.secondComPortFound:
            # We already found two FleetSync ports, no need to keep scanning
            return

        LOG.trace("Two COM ports not yet found.  Scanning...")
        self.comPortScanInProgress = True

        for comPortTry in self.comPortTryList:
            isWaiting = False
            LOG.trace(f"Checking buffer for already-open port {comPortTry.name}")
            try:
                isWaiting = comPortTry.inWaiting()
            except SerialException as err:
                if "ClearCommError failed" in str(err):
                    LOG.debug(f"COM port {comPortTry.name} unplugged.  Scan continues...")
                    self.stop_tracking_port(comPortTry.name)
                    self.comPortTryList.remove(comPortTry)
            except:
                pass  # unicode decode errors may occur here for non-radio com devices
            else:
                if isWaiting:
                    LOG.debug(f"Data is waiting on comm port {comPortTry.name}.")
                    tmpData = comPortTry.read(comPortTry.inWaiting()).decode("utf-8")
                    if "\x02I" in tmpData:
                        LOG.debug(f"Incoming data on comm port {comPortTry.name} appears to be valid FleetSync data.")
                        self.fsBuffer += tmpData
                        self.actively_track_port(comPortTry, alive=True)  # pass the actual open com port object, to keep it open
                    else:
                        LOG.debug("But it's not valid fleetsync data. Scan continues...")
                else:
                    LOG.trace(f"No data on comm port {comPortTry.name}.")
        self.discover_ports()
        self.comPortScanInProgress = False

    def discover_ports(self):
        for portIterable in comports():
            port_name = portIterable[0]
            if port_name not in [x.name for x in self.comPortTryList]:
                try:
                    com_port = serial.Serial(port_name)
                    self.comPortTryList.append(com_port)
                    LOG.debug(f"Discovered port {port_name}")
                    self.actively_track_port(com_port, alive=False)
                except:
                    LOG.debug(f"Discovered port {port_name}, but not actually able to open it for some reason.")

    def actively_track_port(self, com_port, alive: bool):
        """
        RadioLog is capable of working with two fleetsync ports.
        """
        # Are we already tracking this port?
        if self.firstComPort == com_port:
            self.firstComPortAlive = alive
        elif self.secondComPort == com_port:
            self.secondComPortAlive = alive
        elif not self.firstComPortAlive:
            self.firstComPortFound = True
            self.firstComPortAlive = alive
            self.firstComPort = com_port
        elif not self.secondComPortAlive:
            self.secondComPortFound = True
            self.secondComPortAlive = alive
            self.secondComPort = com_port
        else:
            LOG.error(f"Attempting to track com port {com_port.name} as active, but we are already tracking two others.")
        # We can stop scanning this port. We know it's good.
        self.comPortTryList.remove(com_port)

    def stop_tracking_port(self, port_name):
        """
        If the named port is one of the ones we're featuringh on the main window, show that it's no longer alive.
        (Making room for us to feature another one.)
        """
        if self.firstComPort and self.firstComPort.name == port_name:
            self.firstComPortAlive = False
        elif self.secondComPort and self.secondComPort.name == port_name:
            self.secondComPortAlive = False


def main():
    fleetsync = FleetSync(devmode=True)
    fleetsync.search_for_active_com_ports()
