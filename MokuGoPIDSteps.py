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

from .MokuGoPID import *
from .DLSOutputInput import *

import datetime

@attribute(OpenTap.Display(Name="Set Control Matrix", Description="", Groups= ["DLS Python Plugin", "Moku Go PID"]))   
class MGSetControlMatrix(TestStep):
    Inst = property(MokuGoPID, None).add_attribute(OpenTap.Display( "MokuGo PID"))
    Channel = property(Int32, 1).add_attribute(OpenTap.Display( "Channel"))
    Input1gain = property(Double, 1).add_attribute(OpenTap.Display( "Input 1 gain")).add_attribute(OpenTap.Unit( "dB"))
    Input2gain = property(Double, 0).add_attribute(OpenTap.Display( "Input 2 gain")).add_attribute(OpenTap.Unit( "dB") )   
    def __init__(self):
        super(MGSetControlMatrix,self).__init__()
        
    def Run(self):
        self.Inst.SetControlMatrix(self.Channel,self.Input1gain,self.Input2gain)
        
@attribute(OpenTap.Display(Name="Configure By Frequency", Description="", Groups= ["DLS Python Plugin", "Moku Go PID"]))   
class MGSetByFrequency(TestStep):
    Inst = property(MokuGoPID, None).add_attribute(OpenTap.Display( "MokuGo PID"))
    Channel = property(Int32, 1).add_attribute(OpenTap.Display( "Channel"))
    ProportionalGainFactor = property(Double, -10.0).add_attribute(OpenTap.Display( "Proportional Gain Factor")).add_attribute(OpenTap.Unit( "dB"))
    IntegratorCrossoverFrequency = property(Double, 310.0).add_attribute(OpenTap.Display( "Integrator Crossover Frequency")).add_attribute(OpenTap.Unit( "Hz"))
    IntegratorGainSaturation = property(Double,  40.0).add_attribute(OpenTap.Display( "Integrator Gain Saturation")).add_attribute(OpenTap.Unit( "dB"))
    SecondIntegratorCrossoverFrequency = property(Double, 31.0).add_attribute(OpenTap.Display( "Second Integrator Crossover Frequency")).add_attribute(OpenTap.Unit( "Hz"))
    DifferentiatorCrossoverFrequency = property(Double, 16000.0).add_attribute(OpenTap.Display( "Differentiator Crossover Frequency")).add_attribute(OpenTap.Unit( "Hz"))
    DifferentiatorGainSaturation = property(Double, 15.0).add_attribute(OpenTap.Display( "Differentiator Gain Saturation")).add_attribute(OpenTap.Unit( "dB") )   
    def __init__(self):
        super(MGSetByFrequency,self).__init__()
        
    def Run(self):
        self.Inst.SetByFrequency(self.Channel,self.ProportionalGainFactor,self.IntegratorCrossoverFrequency,\
                       self.DifferentiatorCrossoverFrequency, self.IntegratorGainSaturation,\
                       self.DifferentiatorGainSaturation,self.SecondIntegratorCrossoverFrequency)
                       
@attribute(OpenTap.Display(Name="Configure By Gain", Description="", Groups= ["DLS Python Plugin", "Moku Go PID"]))   
class MGSetByGain(TestStep):
    Inst = property(MokuGoPID, None).add_attribute(OpenTap.Display( "MokuGo PID"))
    Channel = property(Int32, 1).add_attribute(OpenTap.Display( "Channel"))
    OverallGain = property(Double, 6.0).add_attribute(OpenTap.Display( "OverallGain")).add_attribute(OpenTap.Unit( "dB"))
    ProportionalGainFactor = property(Double, 20.0).add_attribute(OpenTap.Display( "ProportionalGainFactor")).add_attribute(OpenTap.Unit( "dB"))
    IntegratorGainFactor = property(Double,  40.0).add_attribute(OpenTap.Display( "IntegratorGainFactor")).add_attribute(OpenTap.Unit( "dB"))
    DifferentiatorGainFactor = property(Double, 0.0).add_attribute(OpenTap.Display( "DifferentiatorGainFactor")).add_attribute(OpenTap.Unit( "dB"))
    IntegratorGainSaturationCorner = property(Double, 40.0).add_attribute(OpenTap.Display( "IntegratorGainSaturationCorner")).add_attribute(OpenTap.Unit( "Hz"))
    DifferentiatorGainSaturationCorner = property(Double, 100.0).add_attribute(OpenTap.Display( "DifferentiatorGainSaturationCorner")).add_attribute(OpenTap.Unit( "Hz"))    
    def __init__(self):
        super(MGSetByFrequency,self).__init__()
       
    def Run(self):
        self.Inst.SetByGain(self.Channel,self.OverallGain,self.ProportionalGainFactor,self.IntegratorGainFactor,\
            self.DifferentiatorGainFactor,self.IntegratorGainSaturationCorner,self.DifferentiatorGainSaturationCorner)

@attribute(OpenTap.Display(Name="Set Edge Trigger", Description="", Groups= ["DLS Python Plugin", "Moku Go PID"]))   
class MGSetEdgeTrigger(TestStep):
    Inst = property(MokuGoPID, None).add_attribute(OpenTap.Display( "MokuGo PID"))
    AutoHysteresis = property(bool, True).add_attribute(OpenTap.Display( "AutoHysteresis"))
    Edge = property(PIDEdgeTrigger, PIDEdgeTrigger.Rising).add_attribute(OpenTap.Display( "Edge"))
    HFReject = property(bool,  False).add_attribute(OpenTap.Display( "HF Reject"))
    NoiseReject = property(bool,  False).add_attribute(OpenTap.Display( "Noise Reject"))
    HoldOff = property(Double, 0.0).add_attribute(OpenTap.Display( "HoldOff")).add_attribute(OpenTap.Unit( "s"))
    NumberOfEventsToWait = property(Int32, 1).add_attribute(OpenTap.Display( "Number Of Trigger Events To Wait"))
    Source = property(PIDTriggerSource, PIDTriggerSource.ProbeA).add_attribute(OpenTap.Display( "Source"))
    Level = property(Double, 100.0).add_attribute(OpenTap.Display( "Level")).add_attribute(OpenTap.Unit( "V")  ) 
    def __init__(self):
        super(MGSetByFrequency,self).__init__()
       
    def Run(self):
        self.Inst.SetEdgeTrigger(self,self.AutoHysteresis,self.Edge,self.HFReject,\
                    self.HoldOff,self.Level,self.NoiseReject,self.NumberOfEventsToWait,\
                    self.Source)

@attribute(OpenTap.Display(Name="Enable Output", Description="", Groups= ["DLS Python Plugin", "Moku Go PID"]))   
class MGPIDEnableOutput(TestStep):
    Inst = property(MokuGoPID, None).add_attribute(OpenTap.Display( "MokuGo PID"))
    Channel = property(Int32, 1).add_attribute(OpenTap.Display( "Channel"))
    Signal = property(bool, True).add_attribute(OpenTap.Display( "Signal"))
    Output = property(bool, True).add_attribute(OpenTap.Display( "Output")) 
    def __init__(self):
        super(MGPIDEnableOutput,self).__init__()
       
    def Run(self):
        self.Inst.EnableOutput(self.Channel,self.Signal,self.Output)
        
@attribute(OpenTap.Display(Name="Set Monitor", Description="", Groups= ["DLS Python Plugin", "Moku Go PID"]))   
class MGPIDSetMonitor(TestStep):
    Inst = property(MokuGoPID, None).add_attribute(OpenTap.Display( "MokuGo PID"))
    Channel = property(Int32, 1).add_attribute(OpenTap.Display( "Channel"))
    Source = property(PIDProbeMonitor, PIDProbeMonitor.Input1).add_attribute(OpenTap.Display( "Source"))  
    def __init__(self):
        super(MGPIDEnableOutput,self).__init__()
        
    def Run(self):
        self.Inst.SetProbeMonitor(self.Channel,self.Source)
        
@attribute(OpenTap.Display(Name="Get Data", Description="", Groups= ["DLS Python Plugin", "Moku Go PID"]))
class MGPIDGetData(DLSStep):
    Inst = property(MokuGoPID, None).add_attribute(OpenTap.Display( "MokuGo PID"))
    def __init__(self):
        super(MGPIDGetData,self).__init__()

    def Run(self):
        v = self.Inst.GetData()
        if (v == ''):
            self.log.Info = 'Empty String'
        else:
            ch1data = v['ch1']
            ch2data = v['ch2']
            timedata = v['time']
            super().OutputToDLS("Result",["time","ch1","ch2"] ,[timedata,ch1data,ch2data])
   