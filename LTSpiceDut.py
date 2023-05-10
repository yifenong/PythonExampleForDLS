"""
 A basic example of how to define a DUT driver.
"""
from opentap import *
import OpenTap
from OpenTap import Log
import System
from System import String
import ltspice
import subprocess

@attribute(OpenTap.Display(Name="LTSpice", Description="", Groups= ["DLS Python Plugin"]))
class LTSpiceDut(Dut):
    LtspicePath = property(String, r"C:\Program Files\LTC\LTspiceXVII\XVIIx64.exe").add_attribute(OpenTap.Display( "LTSpice Executable"))
    def __init__(self):
        super(LTSpiceDut,self).__init__()
       
        self.Name = "LTSpice"

    def ReadRawData(self,path,dataname):
        l = ltspice.Ltspice(path)
        l.parse()
        d = l.get_data(dataname)
        return d

    def RunSimulation(self,ascpath):
        subprocess.run([self.LtspicePath,"-run","-ascii",ascpath])

    def Open(self):
        """Called by TAP when the test plan starts."""
        self.log.Info(self.Name + " Opened")

    def Close(self):
        """Called by TAP when the test plan ends."""
        self.log.Info(self.Name + " Closed")