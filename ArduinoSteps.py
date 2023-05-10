import sys
import opentap
import clr
clr.AddReference("System.Collections")
from System.Collections.Generic import List
from opentap import *
import OpenTap

import math
from OpenTap import Log, EnabledIfAttribute



## Import necessary .net APIs
# These represents themselves as regular Python modules but they actually reflect
# .NET libraries.
import System
from System import Array, Double, Byte, Int32, String, Boolean # Import types to reference for generic methods
from System.ComponentModel import BrowsableAttribute # BrowsableAttribute can be used to hide things from the user.
import System.Xml
from System.Xml.Serialization import XmlIgnoreAttribute

from .ArduinoDut import *
from .DLSOutputInput import *

import datetime

@attribute(OpenTap.Display(Name="Read Sine Wave", Description="", Groups= ["DLS Python Plugin", "Arduino Uno"]))
class ReadSineWave(DLSStep):
    Dut = property(ArduinoDut, None).add_attribute(OpenTap.Display( "Arduino Dut"))
    def __init__(self):
        super(ReadSineWave,self).__init__()        
        
        
    def Run(self):
        v = self.Dut.ReadSineWave()
        if (v == ''):
            self.log.Info = 'Empty String'
        else:
            vdata = [float(x) for x in v.split(",")]
            xdata = list(range(len(vdata)))
            super().OutputToDLS("Result",["X","Y"],[xdata, vdata])
            print(vdata)

@attribute(OpenTap.Display(Name="Analog Read", Description="", Groups= ["DLS Python Plugin", "Arduino Uno"]))
class ReadAnalog(TestStep):
    Dut = property(ArduinoDut, None).add_attribute(OpenTap.Display( "Arduino Dut"))  
    def __init__(self):
        super(ReadAnalog,self).__init__()        

    def Run(self):
        v = self.Dut.ReadVoltage()
        if (v == ''):
            self.log.Info = 'Empty String'
        else:
            super().OutputToDLS("Voltage", ["Timestamp", "V"], [float(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")) , float(v)])
            print(v)

@attribute(OpenTap.Display(Name="Blink LED", Description="", Groups= ["DLS Python Plugin", "Arduino Uno"]))
class BlinkLED(TestStep):
    Dut = property(ArduinoDut, None).add_attribute(OpenTap.Display( "Arduino Dut"))
    def __init__(self):
        super().__init__()

    def Run(self):
        self.Dut.BlinkLED()