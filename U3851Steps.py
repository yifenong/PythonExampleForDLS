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

from .U3851Dut import *

import datetime

@attribute(OpenTap.Display(Name="Output", Description="", Groups= ["DLS Python Plugin", "U3851"]))
class Output(TestStep):
    Dut = property(U3851Dut, None).add_attribute(OpenTap.Display( "U3851 Dut"))
    VName = property(U3851OutputName, U3851OutputName.vout1).add_attribute(OpenTap.Display( "Output Name"))
    Value = property(Double,3).add_attribute(OpenTap.Display( "Value"))
    def __init__(self):
        super(Output, self).__init__() 
        
    def Run(self):
        self.log.Info("Output"+str(self.VName));
        v = self.Dut.Output(self.VName,self.Value)
        self.log.Info(str(v))

@attribute(OpenTap.Display(Name="Measure", Description="", Groups= ["DLS Python Plugin", "U3851"]))       
class Measure(TestStep):
    Dut = property(U3851Dut, None).add_attribute(OpenTap.Display( "U3851 Dut"))
    MName = property(U3851MeasurementName, U3851MeasurementName.vout1).add_attribute(OpenTap.Display( "Measurement Name"))

    def __init__(self):
        super(Measure,self).__init__()
       
    def Run(self):
        self.log.Info("Measure"+str(self.MName));
        v = self.Dut.Measure(self.MName)
        self.log.Info(str(v))
        super().OutputToDLS("Measure", ["Timestamp", str(self.MName)], [float(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")) , float(v)])



        