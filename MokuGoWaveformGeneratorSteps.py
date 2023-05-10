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

from .MokuGoWaveformGenerator import *
from .DLSOutputInput import *

import datetime

class MokuGoChannel(Enum):
    One = 1
    Two = 2
    def __str__(self):
        return self.name

@attribute(OpenTap.Display(Name="Generate Square Wave", Description="", Groups= ["DLS Python Plugin", "Moku Go WaveformGenerator"]))   
class MGGenerateSqWave1(TestStep):
    Inst = property(MokuGoWaveformGenerator, None).add_attribute(OpenTap.Display( "MokuGo Waveform Generator", Order=0))
    Duty = property(Double, 50).add_attribute(OpenTap.Display( "Duty Cycle", Order=1)).add_attribute(OpenTap.Unit( "%"))
    Dcoffset = property(Double, 0).add_attribute(OpenTap.Display( "DC Offset", Order=2)).add_attribute(OpenTap.Unit( "V"))
    Phaseoffset = property(Double, 0).add_attribute(OpenTap.Display( "DC Offset", Order=3)).add_attribute(OpenTap.Unit( "Deg"))
    Channel = property(MokuGoChannel, MokuGoChannel.One).add_attribute(OpenTap.Display( "Channel", Order=4))
    Amplitude = property(Double, 1).add_attribute(OpenTap.Display( "Amplitude", Order=5)).add_attribute(OpenTap.Unit( "V"))
    Frequency = property(Double, 1e6).add_attribute(OpenTap.Display( "Frequency", Order=6)).add_attribute(OpenTap.Unit( "Hz"))    
    def __init__(self):
        super(MGGenerateSqWave1,self).__init__()
        
    def Run(self):
        v = self.Inst.GenerateSquareWave(self.Channel,self.Frequency,self.Amplitude,self.Duty,self.Dcoffset,self.Phaseoffset)

@attribute(OpenTap.Display(Name="Generate Sine Wave", Description="", Groups= ["DLS Python Plugin", "Moku Go WaveformGenerator"]))   
class MGGenerateSineWave1(TestStep):
    Inst = property(MokuGoWaveformGenerator, None).add_attribute(OpenTap.Display( "MokuGo WaveformGenerator", Order=0))
    Dcoffset = property(Double, 0).add_attribute(OpenTap.Display( "DC Offset", Order=1)).add_attribute(OpenTap.Unit( "V"))
    Phaseoffset = property(Double, 0).add_attribute(OpenTap.Display( "DC Offset", Order=2)).add_attribute(OpenTap.Unit( "Deg"))
    Channel = property(MokuGoChannel, MokuGoChannel.One).add_attribute(OpenTap.Display( "Channel", Order=3))
    Amplitude = property(Double, 1).add_attribute(OpenTap.Display( "Amplitude", Order=4)).add_attribute(OpenTap.Unit( "V"))
    Frequency = property(Double, 1e6).add_attribute(OpenTap.Display( "Frequency", Order=5)).add_attribute(OpenTap.Unit( "Hz")) 
    def __init__(self):
        super(MGGenerateSineWave1,self).__init__()
        
    def Run(self):
        v = self.Inst.GenerateSineWave(self.Channel,self.Frequency,self.Amplitude,self.Dcoffset,self.Phaseoffset)