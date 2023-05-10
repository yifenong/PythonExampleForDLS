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

from .AD2Instrument import *
from .DLSOutputInput import *

import datetime

@attribute(OpenTap.Display(Name="Generate Sine Wave", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2GenerateSineWave(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Channel =  property(Int32, 0).add_attribute(OpenTap.Display( "Channel", Order=1))
    Frequency = property(Double, 1).add_attribute(OpenTap.Display( "Frequency", Order=2)).add_attribute(OpenTap.Unit( "Hz"))
    Amplitude = property(Double, 2).add_attribute(OpenTap.Display( "Amplitude", Order=3)).add_attribute(OpenTap.Unit( "V"))
    def __init__(self):
        super(AD2GenerateSineWave,self).__init__()        

    def Run(self):
        self.Inst.GenerateSineWave(self.Channel,self.Frequency,self.Amplitude)

@attribute(OpenTap.Display(Name="Record Samples", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2RecordSamples(DLSStep):
    Inst = property(AD2Instrument, None, ).add_attribute(OpenTap.Display( "AD2 Inst"))
    Channel = property(Int32, 0 ).add_attribute(OpenTap.Display( "Channel", Order=1))
    SampleRate = property(Int32, 100000 ).add_attribute(OpenTap.Display( "Sample Rate", Order=2)).add_attribute(OpenTap.Unit( "Hz"))
    Samples = property(Int32, 200000 ).add_attribute(OpenTap.Display( "Samples", Order=3))
    VoltageRange = property(Double, 5 ).add_attribute(OpenTap.Display( "Voltage Range", Order=4)).add_attribute(OpenTap.Unit( "V"))
    
    def __init__(self):
        super(AD2RecordSamples,self).__init__()
        
    def Run(self):
        v = self.Inst.RecordSamples(self.Channel,self.SampleRate,self.Samples,self.VoltageRange)
        if (v == ''):
            self.log.Info = 'Empty String'
        else:
            vdata = np.fromiter(v, dtype = numpy.float)
            xdata = np.arange(len(vdata))
            super().OutputToDLS("Result",["X","Y"] ,[xdata, vdata])
            print(vdata)
            
@attribute(OpenTap.Display(Name="Enable Analog Out", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2AnalogOutEnable(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Channel = property(Int32, 0).add_attribute(OpenTap.Display( "Channel", Order=1))
    Enable = property(bool, True).add_attribute(OpenTap.Display( "Enable", Order=2))
    def __init__(self):
        super(AD2AnalogOutEnable,self).__init__()        
        
    def Run(self):
        self.Inst.AnalogOutEnableSet(self.Channel,self.Enable)

@attribute(OpenTap.Display(Name="Analog Out Function", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2AnalogOutFunction(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Channel = property(Int32, 0).add_attribute(OpenTap.Display( "Channel", Order=1))
    Function = property(AD2Function, AD2Function.funcSine).add_attribute(OpenTap.Display( "Function", Order=2))
    def __init__(self):
        super(AD2AnalogOutFunction,self).__init__()        
       
    def Run(self):
        self.Inst.AnalogOutFunctionSet(self.Channel,self.Function)
        
@attribute(OpenTap.Display(Name="Analog Out Frequency", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2AnalogOutFrequency(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Channel = property(Int32, 0).add_attribute(OpenTap.Display( "Channel", Order=1))
    Frequency = property(Double, 1).add_attribute(OpenTap.Display( "Frequency", Order=2)).add_attribute(OpenTap.Unit( "Hz"))
    def __init__(self):
        super(AD2AnalogOutFrequency,self).__init__()        
    def Run(self):
        self.Inst.AnalogOutFrequencySet(self.Channel,self.Frequency)
        
@attribute(OpenTap.Display(Name="Analog Out Amplitude", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2AnalogOutAmplitude(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Channel = property(Int32, 0).add_attribute(OpenTap.Display( "Channel", Order=1))
    Amplitude = property(Double, 2).add_attribute(OpenTap.Display( "Amplitude", Order=2)).add_attribute(OpenTap.Unit( "V"))
    def __init__(self):
        super(AD2AnalogOutAmplitude,self).__init__()        
    def Run(self):
        self.Inst.AnalogOutAmplitudeSet(self.Channel,self.Amplitude)
        
@attribute(OpenTap.Display(Name="Analog Out Offset", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2AnalogOutOffset(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Channel = property(Int32, 0).add_attribute(OpenTap.Display( "Channel", Order=1))
    Offset = property(Double, 0).add_attribute(OpenTap.Display( "Offset", Order=2)).add_attribute(OpenTap.Unit( "V"))
    def __init__(self):
        super(AD2AnalogOutOffset,self).__init__()         
    def Run(self):
        self.Inst.AnalogOutOffsetVoltage(self.Channel,self.Offset)
        
@attribute(OpenTap.Display(Name="Analog Out Symmetry", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2AnalogOutSymmetry(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Channel = property(Int32, 0).add_attribute(OpenTap.Display( "Channel", Order=1))
    Symmetry = property(Double, 50).add_attribute(OpenTap.Display( "Symmetry", Order=2)).add_attribute(OpenTap.Unit( "%"))
    def __init__(self):
        super(AD2AnalogOutSymmetry,self).__init__()        
        
    def Run(self):
        self.Inst.AnalogOutSymmetry(self.Channel,self.Symmetry)
        
@attribute(OpenTap.Display(Name="Analog Out Phase", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2AnalogOutPhase(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Channel = property(Int32, 0).add_attribute(OpenTap.Display( "Channel", Order=1))
    Phase = property(Double, 0).add_attribute(OpenTap.Display( "Phase", Order=2)).add_attribute(OpenTap.Unit( "Deg"))
    def __init__(self):
        super(AD2AnalogOutPhase,self).__init__()        
        
    def Run(self):
        self.Inst.AnalogOutPhase(self.Channel,self.Phase)
        
@attribute(OpenTap.Display(Name="Analog Out Configure", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2AnalogOutConfigure(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Channel = property(Int32, 0).add_attribute(OpenTap.Display( "Channel", Order=1))
    Start = property(bool, True).add_attribute(OpenTap.Display( "Start", Order=2))
    def __init__(self):
        super(AD2AnalogOutConfigure,self).__init__()        
        
    def Run(self):
        self.Inst.AnalogOutConfigure(self.Channel,self.Start)
        
@attribute(OpenTap.Display(Name="Enable Analog In", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2AnalogInEnable(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Channel = property(Int32, 0).add_attribute(OpenTap.Display( "Channel", Order=1))
    Enable = property(bool, True).add_attribute(OpenTap.Display( "Enable", Order=2))
    def __init__(self):
        super(AD2AnalogInEnable,self).__init__()        
        
    def Run(self):
        self.Inst.AnalogInEnableSet(self.Channel,self.Enable)
        
@attribute(OpenTap.Display(Name="Analog In Offset", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2AnalogInOffset(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Channel = property(Int32, 0).add_attribute(OpenTap.Display( "Channel", Order=1))
    Offset = property(Double, 0).add_attribute(OpenTap.Display( "Offset", Order=2)).add_attribute(OpenTap.Unit( "V"))
    def __init__(self):
        super(AD2AnalogInOffset,self).__init__()        
        
    def Run(self):
        self.Inst.AnalogInOffsetVoltage(self.Channel,self.Offset)
        
@attribute(OpenTap.Display(Name="Analog In Range", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2AnalogInRange(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Channel = property(Int32, 0).add_attribute(OpenTap.Display( "Channel", Order=1))
    Range = property(Double, 0).add_attribute(OpenTap.Display( "Range", Order=2)).add_attribute(OpenTap.Unit( "V"))
    def __init__(self):
        super(AD2AnalogInRange,self).__init__()        
        
    def Run(self):
        self.Inst.AnalogInRangeVoltage(self.Channel,self.Range)
        
@attribute(OpenTap.Display(Name="Analog In Configure", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2AnalogInConfigure(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Reconfigure = property(bool, False).add_attribute(OpenTap.Display( "Reconfigure", Order=1))
    Start = property(bool, True).add_attribute(OpenTap.Display( "Start", Order=2))
    def __init__(self):
        super(AD2AnalogInConfigure,self).__init__()        
       
    def Run(self):
        self.Inst.AnalogInConfigure(self.Reconfigure,self.Start)

        
@attribute(OpenTap.Display(Name="Analog In Get ADC Sample", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2GetADCSample(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Channel = property(Int32, 0).add_attribute(OpenTap.Display( "Channel", Order=1))
    def __init__(self):
        super(AD2GetADCSample,self).__init__()        
        
    def Run(self):
        v = self.Inst.GetADCSample(self.Channel)
        self.log.Info(str(v))
        super().OutputToDLS("Measure", ["Timestamp", str(self.Name)], [float(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")) , float(v)])

@attribute(OpenTap.Display(Name="Analog In Acquire Samples", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2AcquireSamples(DLSStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Channel = property(Int32, 0).add_attribute(OpenTap.Display( "Channel", Order=1))
    Samples = property(Int32, 1024).add_attribute(OpenTap.Display( "Samples", Order=3))
    def __init__(self):
        super(AD2AcquireSamples,self).__init__()
        
    def Run(self):
        v = self.Inst.AcquireSamples(self.Channel,self.Samples)
        if (v == ''):
            self.log.Info = 'Empty String'
        else:
            vdata = np.fromiter(v, dtype = numpy.float)
            xdata = np.arange(len(vdata))
            super().OutputToDLS("Result",["X","Y"] ,[xdata, vdata])
            print(vdata)
            
@attribute(OpenTap.Display(Name="Analog Out Run Length", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2AnalogOutRunlength(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Channel = property(Int32, 0).add_attribute(OpenTap.Display( "Channel", Order=1))
    Length = property(Double, 5e-3).add_attribute(OpenTap.Display( "Length", Order=2)).add_attribute(OpenTap.Unit( "s"))
    def __init__(self):
        super(AD2AnalogOutRunlength,self).__init__()        
        
    def Run(self):
        self.Inst.SetAnalogOutRunlength(self.Channel,self.Length)
        
@attribute(OpenTap.Display(Name="Analog Out Repeat", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2AnalogOutRepeat(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Channel = property(Int32, 0).add_attribute(OpenTap.Display( "Channel", Order=1))
    Repeat = property(Int32, 1).add_attribute(OpenTap.Display( "Repeat", Order=2))
    def __init__(self):
        super(AD2AnalogOutRepeat,self).__init__()        
       
    def Run(self):
        self.Inst.SetAnalogOutRepeat(self.Channel,self.Repeat)
        
@attribute(OpenTap.Display(Name="Analog In Buffer Size", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2AnalogInBufferSize(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Size = property(Int32, 1024).add_attribute(OpenTap.Display( "Size", Order=2))
    def __init__(self):
        super(AD2AnalogInBufferSize,self).__init__()        
        
    def Run(self):
        self.Inst.SetAnalogInBufferSize(self.Size)
        
@attribute(OpenTap.Display(Name="Analog In Trigger Source", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2AnalogInTriggerSource(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    TriggerSource = property(AD2TriggerSource, AD2TriggerSource.trigsrcNone).add_attribute(OpenTap.Display( "Trigger Source", Order=2))
    def __init__(self):
        super(AD2AnalogInTriggerSource,self).__init__()        
       
    def Run(self):
        self.Inst.SetAnalogInTriggerSource(self.TriggerSource)
        
@attribute(OpenTap.Display(Name="Analog In Trigger Position", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2AnalogInTriggerPosition(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    HorizontalPosition = property(Double, 0.3).add_attribute(OpenTap.Display( "Horizontal Position", Order=2)).add_attribute(OpenTap.Unit( "s"))
    def __init__(self):
        super(AD2AnalogInTriggerPosition,self).__init__()        
        
    def Run(self):
        self.Inst.SetAnalogInTriggerPosition(self.HorizontalPosition)
        
@attribute(OpenTap.Display(Name="Enable Positive Supply", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2PositiveSupplyEnable(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Enable = property(bool, True).add_attribute(OpenTap.Display( "Enable", Order=1))
    def __init__(self):
        super(AD2PositiveSupplyEnable,self).__init__()        
        
    def Run(self):
        self.Inst.EnablePositiveSupply(self.Enable)
        
@attribute(OpenTap.Display(Name="Enable Negative Supply", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2NegativeSupplyEnable(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Enable = property(bool, True).add_attribute(OpenTap.Display( "Enable", Order=1))
    def __init__(self):
        super(AD2NegativeSupplyEnable,self).__init__()        
        
    def Run(self):
        self.Inst.EnableNegativeSupply(self.Enable)
        
@attribute(OpenTap.Display(Name="Set Positive Supply", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2PositiveSupply(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Voltage = property(Double, 5).add_attribute(OpenTap.Display( "Voltage", Order=1)).add_attribute(OpenTap.Unit( "V"))
    def __init__(self):
        super(AD2PositiveSupply,self).__init__()        
        
    def Run(self):
        self.Inst.SetPositiveSupply(self.Voltage)
        
@attribute(OpenTap.Display(Name="Set Negative Supply", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2NegativeSupply(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Voltage = property(Double, -5).add_attribute(OpenTap.Display( "Voltage", Order=1)).add_attribute(OpenTap.Unit( "V"))
    def __init__(self):
        super(AD2NegativeSupply,self).__init__()        
      
    def Run(self):
        self.Inst.SetNegativeSupply(self.Voltage)
        
@attribute(OpenTap.Display(Name="Enable Analog IO", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2AnalogIOEnable(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Enable = property(bool, True).add_attribute(OpenTap.Display( "Enable", Order=1))
    def __init__(self):
        super(AD2AnalogIOEnable,self).__init__()        
       
    def Run(self):
        self.Inst.EnableAnalogIO(self.Enable)
        
@attribute(OpenTap.Display(Name="Monitor Power", Description="", Groups= ["DLS Python Plugin", "Analog Discovery 2"]))
class AD2MonitorPower(TestStep):
    Inst = property(AD2Instrument, None).add_attribute(OpenTap.Display( "AD2 Inst"))
    Monitor = property(AD2PowerMonitor, AD2PowerMonitor.USBVoltage).add_attribute(OpenTap.Display( "Monitor", Order=1))
    def __init__(self):
        super(AD2MonitorPower,self).__init__()        
        
    def Run(self):
        v = self.Inst.MonitorPower(self.Monitor)
        self.log.Info(str(v))
        super().OutputToDLS("Measure", ["Timestamp", str(self.Monitor.name)], [float(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")) , float(v)])
