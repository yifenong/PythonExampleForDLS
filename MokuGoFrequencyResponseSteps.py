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

from .MokuGoFrequencyResponse import *
from .DLSOutputInput import *

import datetime



@attribute(OpenTap.Display(Name="Get Frequency Response", Description="", Groups= ["DLS Python Plugin", "Moku Go Frequency Response"]))
class MGGetSpectrum(DLSStep):
    Inst = property(MokuGoFrequencyResponse, None).add_attribute(OpenTap.Display( "MokuGo Frequency Response", Order=0))
    StartFrequency = property(Double, 20e6).add_attribute(OpenTap.Display( "StartFrequency", Order=1)).add_attribute(OpenTap.Unit( "Hz"))
    StopFrequency = property(Double, 100).add_attribute(OpenTap.Display( "StopFrequency", Order=2)).add_attribute(OpenTap.Unit( "Hz"))
    NumPoints = property(Int32, 256).add_attribute(OpenTap.Display( "NumPoints", Order=3))
    AveragingTime = property(Double, 1e-3).add_attribute(OpenTap.Display( "AveragingTime", Order=4)).add_attribute(OpenTap.Unit( "s"))
    AveragingCycles = property(Int32, 5).add_attribute(OpenTap.Display( "AveragingCycles", Order=5))
    SettlingCycles = property(Int32, 5).add_attribute(OpenTap.Display( "SettlingCycles", Order=6))
    SettlingTime = property(Double, 1e-3).add_attribute(OpenTap.Display( "SettlingTime", Order=7)).add_attribute(OpenTap.Unit( "s"))
    Output1Amplitude = property(Double, 0.1).add_attribute(OpenTap.Display( "Output1Amplitude", Order=8)).add_attribute(OpenTap.Unit( "V"))
    Output2Amplitude = property(Double, 0.1).add_attribute(OpenTap.Display( "Output2Amplitude", Order=9)).add_attribute(OpenTap.Unit( "V"))   
    def __init__(self):
        super(MGGetSpectrum,self).__init__()
        
    def Run(self):
        v = self.Inst.GetData(self.StartFrequency,self.StopFrequency,\
            self.NumPoints,self.AveragingTime,self.AveragingCycles,\
            self.SettlingCycles,self.SettlingTime,self.Output1Amplitude,self.Output2Amplitude)
        if (v == ''):
            self.log.Info = 'Empty String'
        else:
            #print(v['ch1']['frequency'])
            #print(v['ch1']['magnitude'])
            #print(v['ch2']['frequency'])
            #print(v['ch2']['magnitude'])
            ch1freq = v['ch1']['frequency']
            ch1mag = v['ch1']['magnitude']
            ch1phase = v['ch1']['phase']
            ch2freq = v['ch2']['frequency']
            ch2mag = v['ch2']['magnitude']
            ch2phase = v['ch2']['phase']
            columnNames = ["ch1_freq", "ch1_magnitude", "ch1_phase", "ch2_freq", "ch2_magnitude","ch2_phase"]
            super().OutputToDLS("Result",columnNames ,[ch1freq,ch1mag,ch1phase,ch2freq,ch2mag,ch2phase])

