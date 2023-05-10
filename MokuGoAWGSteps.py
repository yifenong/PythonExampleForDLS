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

from .MokuGoAWG import *
from .DLSOutputInput import *

import datetime

class MokuGoChannel(Enum):
    One = 1
    Two = 2
    def __str__(self):
        return self.name

@attribute(OpenTap.Display(Name="Generate Square Wave", Description="", Groups= ["DLS Python Plugin", "Moku Go AWG"]))   
class MGGenerateSqWave(TestStep):
    Inst = property(MokuGoAWG, None).add_attribute(OpenTap.Display( "MokuGo AWG"))
    Points = property(Int32, 100).add_attribute(OpenTap.Display( "Points"))
    SampleRate = property(MokuGoSampleRate, MokuGoSampleRate.Auto).add_attribute(OpenTap.Display( "Sample Rate"))
    Channel = property(MokuGoChannel, MokuGoChannel.One).add_attribute(OpenTap.Display( "Channel"))
    Amplitude = property(Double, 1).add_attribute(OpenTap.Display( "Amplitude")).add_attribute(OpenTap.Unit( "V"))
    Frequency = property(Double, 1e6).add_attribute(OpenTap.Display( "Frequency")).add_attribute(OpenTap.Unit( "Hz"))
    def __init__(self):
        super(MGGenerateSqWave,self).__init__()
        
    def Run(self):
        v = self.Inst.GenerateSquareWave(Points,Channel,SampleRate,Frequency,Amplitude)