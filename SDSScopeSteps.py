import sys
import opentap
import clr
clr.AddReference("System.Collections")
from System.Collections.Generic import List
from opentap import *
import OpenTap

import math
from OpenTap import Log, EnabledIfAttribute

import numpy as np

## Import necessary .net APIs
# These represents themselves as regular Python modules but they actually reflect
# .NET libraries.
import System
from System import Array, Double, Byte, Int32, String, Boolean # Import types to reference for generic methods
from System.ComponentModel import BrowsableAttribute # BrowsableAttribute can be used to hide things from the user.
import System.Xml
from System.Xml.Serialization import XmlIgnoreAttribute

from .SDSScope import *
from .DLSOutputInput import *

@attribute(OpenTap.Display(Name="Screenshot", Description="", Groups= ["DLS Python Plugin", "SDSScope"]))
class SDSGetScreenshot(TestStep):
    Inst = property(SDSScope, None).add_attribute(OpenTap.Display( "SDSScope",Order=0))
    def __init__(self):
        super(SDSGetScreenshot,self).__init__() 

    def Run(self):
        y = self.Inst.GetScreenshot()
        super().OutputToDLS("Screenshot",["Screenshot"] ,[y], True)
        # file_name = r'C:\Users\yifenong\Desktop\scdp.bmp'
        # f=open(file_name,'wb')
        # f.write(y)
        # f.flush()
        # f.close()
        
@attribute(OpenTap.Display(Name="Get Waveform", Description="", Groups= ["DLS Python Plugin", "SDSScope"]))
class SDSGetWaveform(TestStep):
    Inst = property(SDSScope, None).add_attribute(OpenTap.Display( "SDSScope",Order=0))
    Channel = property(Int32, 1).add_attribute(OpenTap.Display( "Channel", Order=1))
    def __init__(self):
        super(SDSGetWaveform,self).__init__()
        
    def Run(self):
        Time,Volts = self.Inst.GetWaveform(self.Channel)
        super().OutputToDLS("Waveform",["Time","Volts"],[Time, Volts])
        print(xdata)
        print(ydata)

@attribute(OpenTap.Display(Name="Get Measurement", Description="", Groups= ["DLS Python Plugin", "SDSScope"]))
class SDSGetMeasurement(TestStep):
    Inst = property(SDSScope, None).add_attribute(OpenTap.Display( "SDSScope",Order=0))
    Channel = property(Int32, 1).add_attribute(OpenTap.Display( "Channel", Order=1))
    Meas = property(SDSMeasurement, SDSMeasurement.PKPK).add_attribute(OpenTap.Display( "Channel", Order=2))
    def __init__(self):
        super(SDSGetMeasurement,self).__init__()
        
    def Run(self):
        self.Inst.GetMeasurement(self.Channel,self.Meas)
        
@attribute(OpenTap.Display(Name="Autoset", Description="", Groups= ["DLS Python Plugin", "SDSScope"]))
class SDSAutoset(TestStep):
    Inst = property(SDSScope, None).add_attribute(OpenTap.Display( "SDSScope",Order=0))
    def __init__(self):
        super(SDSAutoset,self).__init__()
        
    def Run(self):
        self.Inst.Autoset()
