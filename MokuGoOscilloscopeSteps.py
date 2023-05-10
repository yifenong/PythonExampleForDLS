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

from .MokuGoOscilloscope import *
from .DLSOutputInput import *

import datetime

@attribute(OpenTap.Display(Name="Record Signal", Description="", Groups= ["DLS Python Plugin", "Moku Go Oscilloscope"]))
class MGRecordSignal(DLSStep):
    Inst = property(MokuGoOscilloscope, None).add_attribute(OpenTap.Display( "MokuGo Oscilloscope", Order=0))
    SpanStart = property(Double, -1e-3).add_attribute(OpenTap.Display( "Span Start", Order=1)).add_attribute(OpenTap.Unit( "Hz"))
    SpanStop = property(Double, 1e-3).add_attribute(OpenTap.Display( "Span Stop", Order=2)).add_attribute(OpenTap.Unit( "Hz"))
    def __init__(self):
        super(MGRecordSignal,self).__init__()
        
    def Run(self):
        v = self.Inst.RecordSignal(self.SpanStart,self.SpanStop)
        if (v == ''):
            self.log.Info = 'Empty String'
        else:
            ch1data = v['ch1']
            ch2data = v['ch2']
            timedata = v['time']
            super().OutputToDLS("Result",["time","ch1","ch2"],[timedata,ch1data,ch2data])

@attribute(OpenTap.Display(Name="Set Trigger", Description="", Groups= ["DLS Python Plugin", "Moku Go Oscilloscope"]))
class MGSetTrigger(TestStep):
    Inst = property(MokuGoOscilloscope, None).add_attribute(OpenTap.Display( "MokuGo Oscilloscope", Order=0))
    TriggerType = property(MokuGoTrigger, MokuGoTrigger.Edge).add_attribute(OpenTap.Display( "Trigger Type", Order=0))
    Source = property(MokuGoSource, MokuGoSource.Input1).add_attribute(OpenTap.Display( "Source", Order=1))
    Level = property(Double, 0).add_attribute(OpenTap.Display( "Level")).add_attribute(OpenTap.Unit( "V"))
    def __init__(self):
        super(MGSetTrigger,self).__init__()
        
    def Run(self):
        v = self.Inst.SetTrigger(self.TriggerType,self.Source,self.Level)

@attribute(OpenTap.Display(Name="Set Source", Description="", Groups= ["DLS Python Plugin", "Moku Go Oscilloscope"]))
class MGSetSource(TestStep):
    Inst = property(MokuGoOscilloscope, None).add_attribute(OpenTap.Display( "MokuGo Oscilloscope", Order=0))
    Channel = property(MokuGoChannel, MokuGoChannel.One).add_attribute(OpenTap.Display( "Channel", Order=1))
    Source = property(MokuGoSource, MokuGoSource.Input1).add_attribute(OpenTap.Display( "Source", Order=2)) 
    def __init__(self):
        super(MGSetSource,self).__init__()

    def Run(self):
        v = self.Inst.SetSource(self.Channel,self.Source)

@attribute(OpenTap.Display(Name="Set Power Supply", Description="", Groups= ["DLS Python Plugin", "Moku Go Oscilloscope"]))
class MGSetPowerSupply(TestStep):
    Inst = property(MokuGoOscilloscope, None).add_attribute(OpenTap.Display( "MokuGo Oscilloscope", Order=0))
    Channel = property(MokuGoChannel, MokuGoChannel.One).add_attribute(OpenTap.Display( "Channel", Order=1))
    Enable = property(bool, True).add_attribute(OpenTap.Display( "Enable", Order=2))
    Voltage = property(Double, 2).add_attribute(OpenTap.Display( "Voltage", Order=3)).add_attribute(OpenTap.Unit( "V"))
    Current = property(Double, 0.1).add_attribute(OpenTap.Display( "Current", Order=4)).add_attribute(OpenTap.Unit( "A"))
    def __init__(self):
        super(MGSetPowerSupply,self).__init__()
       
    def Run(self):
        v = self.Inst.SetPowerSupply(self.Channel,self.Enable,self.Voltage,self.Current)


@attribute(OpenTap.Display(Name="Generate Sine Wave", Description="", Groups= ["DLS Python Plugin", "Moku Go Oscilloscope"]))   
class MGGenerateSineWave(TestStep):
    Inst = property(MokuGoOscilloscope, None).add_attribute(OpenTap.Display( "MokuGo Oscilloscope", Order=0))
    Channel = property(MokuGoChannel, MokuGoChannel.One).add_attribute(OpenTap.Display( "Channel", Order=1))
    Amplitude = property(Double, 1).add_attribute(OpenTap.Display( "Amplitude", Order=2)).add_attribute(OpenTap.Unit( "V"))
    Frequency = property(Double, 1e6).add_attribute(OpenTap.Display( "Frequency", Order=3)).add_attribute(OpenTap.Unit( "Hz"))    
    def __init__(self):
        super(MGGenerateSineWave,self).__init__()
        
    def Run(self):
        v = self.Inst.GenerateSineWave(self.Channel,self.Amplitude,self.Frequency)