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

from .GDSScope import *
from .DLSOutputInput import *

@attribute(OpenTap.Display(Name="Get Waveform", Description="", Groups= ["DLS Python Plugin", "GDSScope"]))
class GDSGetWaveform(DLSStep):
    Inst = property(GDSScope, None).add_attribute(OpenTap.Display( "GDSScope",Order=0))
    Channel = property(Int32, 1).add_attribute(OpenTap.Display( "Channel", Order=1))  
    def __init__(self):
        super(GDSGetWaveform,self).__init__()
        
    def Run(self):
        Time,Volts = self.Inst.GetRawData(self.Channel)
        super().OutputToDLS("Waveform",["Time","Volts"],[Time, Volts])
        print(xdata)
        print(ydata)
        
@attribute(OpenTap.Display(Name="Get Measurement", Description="", Groups= ["DLS Python Plugin", "GDSScope"]))
class GDSGetMeasurement(TestStep):
    Inst = property(GDSScope, None).add_attribute(OpenTap.Display( "GDSScope",Order=0))
    Channel = property(Int32, 1).add_attribute(OpenTap.Display( "Channel", Order=1))
    Meas = property(GDSMeasurement, GDSMeasurement.PK2PK).add_attribute(OpenTap.Display( "Measurement", Order=2))
    def __init__(self):
        super(GDSGetMeasurement,self).__init__()
        
    def Run(self):
        self.Inst.GetMeasurement(self.Channel,self.Meas)
        
@attribute(OpenTap.Display(Name="Get Measurement Relative", Description="", Groups= ["DLS Python Plugin", "GDSScope"]))
class GDSGetMeasurement1(TestStep):
    Inst = property(GDSScope, None).add_attribute(OpenTap.Display( "GDSScope",Order=0))
    Channel1 = property(Int32, 1).add_attribute(OpenTap.Display( "Source 1 Channel", Order=1))
    Channel2 = property(Int32, 2).add_attribute(OpenTap.Display( "Source 2 Channel", Order=2))
    Meas = property(GDSMeasurement1, GDSMeasurement1.PHAse).add_attribute(OpenTap.Display( "Measurement", Order=3))
    def __init__(self):
        super(GDSGetMeasurement1,self).__init__()
        
    def Run(self):
        self.Inst.GetMeasurement1(self.Channel1, self.Channel2, self.Meas)
        
@attribute(OpenTap.Display(Name="Autoset", Description="", Groups= ["DLS Python Plugin", "GDSScope"]))
class GDSAutoset(TestStep):
    Inst = property(GDSScope, None).add_attribute(OpenTap.Display( "GDSScope",Order=0))
    def __init__(self):
        super(GDSAutoset,self).__init__()
        
    def Run(self):
        self.Inst.Autoset()