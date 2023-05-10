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

from enum import Enum

import numpy as np

from .LTSpiceDut import LTSpiceDut
from .DLSOutputInput import *

class ComplexFormat(Enum):
    Real = 1
    Imaginary = 2
    Magnitude = 3
    Phase = 4
    def __str__(self):
        return self.name

@attribute(OpenTap.Display(Name="Read RAW Data", Description="", Groups= ["DLS Python Plugin", "LTSpice"]))
class ReadData(DLSStep):
    Dut = property(LTSpiceDut,None).add_attribute(OpenTap.Display( "LTSpice Dut"))
    Path = property(String, r"C:\Users\yifenong\Desktop\opamp.raw").add_attribute(OpenTap.Display( "Raw File Path"))
    DataName = property(String, "V(LP)").add_attribute(OpenTap.Display( "Data Name"))
    ComplexData = property(ComplexFormat, ComplexFormat.Real).add_attribute(OpenTap.Display( "Complex Format"))
    def __init__(self):
        super(ReadData,self).__init__()


    def Run(self):
        self.log.Info("Reading"+str(self.Path))
        y = np.array(self.Dut.ReadRawData(self.Path,self.DataName))
        if self.ComplexData == ComplexFormat.Real:
            ydata = y.real
        elif self.ComplexData == ComplexFormat.Imaginary:
            ydata = y.imag
        elif self.ComplexData == ComplexFormat.Magnitude:
            ydata = np.array([np.abs(x) for x in y])
        elif self.ComplexData == ComplexFormat.Phase:
            ydata = np.array([np.angle(x) for x in y])
        else:
            ydata = np.array([np.abs(x) for x in y])

        xdata = toNetArrayFast(np.arange(len(ydata)))
        super().OutputToDLS("Result",["X","Y"],[xdata, ydata])
        print(ydata)

@attribute(OpenTap.Display(Name="Run Simulation", Description="", Groups= ["DLS Python Plugin", "LTSpice"]))
class RunSimulation(TestStep):
    Dut = property(LTSpiceDut,None).add_attribute(OpenTap.Display( "LTSpice Dut"))
    AscPath = property(String,r"C:\Users\yifenong\Desktop\opamp.asc").add_attribute(OpenTap.Display( "Schematic Path"))
    def __init__(self):
        super(RunSimulation,self).__init__()
        
    def Run(self):
        self.log.Info("Reading"+str(self.AscPath))
        self.Dut.RunSimulation(self.AscPath)