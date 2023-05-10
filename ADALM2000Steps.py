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

from .ADALM2000Instrument import *
from .DLSOutputInput import *

import datetime

@attribute(OpenTap.Display(Name="Generate Sine Wave", Description="", Groups= ["DLS Python Plugin", "ADALM2000"]))
class ADALM2000GenerateSineWave(TestStep):
    Inst = property(ADALM2000Instrument, None).add_attribute(OpenTap.Display( "ADALM2000", Order=0))
    VPos = property(Double, 2.0).add_attribute(OpenTap.Display( "V+", Order=1)).add_attribute(OpenTap.Unit( "V"))
    VNeg = property(Double, -2.0).add_attribute(OpenTap.Display( "V-", Order=2)).add_attribute(OpenTap.Unit( "V"))
    Points = property(Int32, 1024).add_attribute(OpenTap.Display( "Points", Order=3))
    def __init__(self):
        super(ADALM2000GenerateSineWave,self).__init__()        
        
    def Run(self):
        self.Inst.GenerateSineWave(self.VNeg,self.VPos,self.Points)
        
@attribute(OpenTap.Display(Name="Generate Binary Counter", Description="", Groups= ["DLS Python Plugin", "ADALM2000"]))
class ADALM2000GenerateBinaryCounter(TestStep):
    Inst = property(ADALM2000Instrument, None).add_attribute(OpenTap.Display( "ADALM2000", Order=0))
    NBits = property(Int32, 3).add_attribute(OpenTap.Display( "Number of Bits", Order=1))
    def __init__(self):
        super(ADALM2000GenerateBinaryCounter,self).__init__()        
        
    def Run(self):
        self.Inst.GenerateBinaryCounter(self.NBits)
        
@attribute(OpenTap.Display(Name="Reset Channel", Description="", Groups= ["DLS Python Plugin", "ADALM2000"]))
class ADALM2000ResetChannel(TestStep):
    Inst = property(ADALM2000Instrument, None).add_attribute(OpenTap.Display( "ADALM2000", Order=0))
    Channel = property(ChannelEN,ChannelEN.AnalogIn).add_attribute(OpenTap.Display( "Channel", Order = 1))
    def __init__(self):
        super(ADALM2000ResetChannel,self).__init__()        
        
    def Run(self):
        if (self.Channel == ChannelEN.AnalogIn):
            self.Inst.ResetAnalogIn()
        elif (self.Channel == ChannelEN.AnalogOut):
            self.Inst.ResetAnalogOut()
        elif (self.Channel == ChannelEN.PowerSupply):
            self.Inst.ResetPowerSupply()
        elif (self.Channel == ChannelEN.Digital):
            self.Inst.ResetDigitalt()

        
@attribute(OpenTap.Display(Name="Calibrate ADC", Description="", Groups= ["DLS Python Plugin", "ADALM2000"]))
class ADALM2000CalibrateADC(TestStep):
    Inst = property(ADALM2000Instrument, None).add_attribute(OpenTap.Display( "ADALM2000", Order=0)) 
    def __init__(self):
        super(ADALM2000CalibrateADC,self).__init__()        

    def Run(self):
        self.Inst.CalibrateADC()
        
@attribute(OpenTap.Display(Name="Calibrate DAC", Description="", Groups= ["DLS Python Plugin", "ADALM2000"]))
class ADALM2000CalibrateDAC(TestStep):
    Inst = property(ADALM2000Instrument, None).add_attribute(OpenTap.Display( "ADALM2000", Order=0))
    def __init__(self):
        super(ADALM2000CalibrateDAC,self).__init__()         
        
    def Run(self):
        self.Inst.CalibrateDAC()

        
@attribute(OpenTap.Display(Name="Get Analog Input Samples", Description="", Groups= ["DLS Python Plugin", "ADALM2000"]))
class ADALM2000GetAnalogInputSamples(DLSStep):
    Inst = property(ADALM2000Instrument, None).add_attribute(OpenTap.Display( "ADALM2000"))
    SD = property(SMethod,SMethod.Samples).add_attribute(OpenTap.Display( "Samples/Duration", Order = 1))
    
    @property(Boolean)
    @attribute(Browsable(False))
    def SDIsSamples(self):
        return SD == SMethod.Samples
        
    @property(Boolean)
    @attribute(Browsable(False))
    def SDIsDuration(self):
        return SD == SMethod.Duration
       
    Samples = property(Int32, 1000).add_attribute(OpenTap.Display( "Samples", Order=2))\
        .add_attribute(OpenTap.EnabledIf( "SDIsSamples", True, HideIfDisabled=True))
    Duration = property(Double, 3).add_attribute(OpenTap.Display( "Duration", Order=2))\
        .add_attribute(OpenTap.EnabledIf( "SDIsDuration", True, HideIfDisabled=True))\
        .add_attribute(OpenTap.Unit( "s"))
    def __init__(self):
        super(ADALM2000GetAnalogInputSamples,self).__init__()
        
    def Run(self):
        if (self.SD == SMethod.Samples):
            v = self.Inst.GetAnalogInputSamples(self.Samples)
        else:
            v = self.Inst.GetAnalogInputSamples(self.Duration)
        y0data = v[0]
        y1data = v[1]
        xdata = list(range(len(ydata)))
        super().OutputToDLS("Result",["X","Channel0","Channel1"] ,[xdata, y0data, y1data])  

@attribute(OpenTap.Display(Name="Get Digital Samples", Description="", Groups= ["DLS Python Plugin", "ADALM2000"]))
class ADALM2000GetDigitalSamples(DLSStep):
    Inst = property(ADALM2000Instrument , None).add_attribute(OpenTap.Display( "ADALM2000"))
    Samples = property(Int32, 100).add_attribute(OpenTap.Display( "Samples", Order=1))
    def __init__(self):
        super(ADALM2000GetDigitalSamples,self).__init__()
        
    def Run(self):
        v = self.Inst.GetDigitalSamples()
        ydata = v
        xdata = list(range(len(ydata)))
        super().OutputToDLS("Result",["X","Y"] ,[xdata, ydata])  
            
@attribute(OpenTap.Display(Name="Enable Channel", Description="", Groups= ["DLS Python Plugin", "ADALM2000"]))
class ADALM2000EnableChannel(TestStep):
    Inst = property(ADALM2000Instrument, None).add_attribute(OpenTap.Display( "ADALM2000", Order=0))
    Channel = property(ChannelEN,ChannelEN.AnalogIn).add_attribute(OpenTap.Display( "Channel", Order = 1))
    ChannelNumber = property(Int32,0).add_attribute(OpenTap.Display( "Channel Number", Order = 2))
    Enable = property(bool,True).add_attribute(OpenTap.Display( "Enable", Order = 3))
    def __init__(self):
        super(ADALM2000EnableChannel,self).__init__()        
        
    def Run(self):
        if (self.Channel == ChannelEN.AnalogIn):
            self.Inst.EnableAnalogInputChannel(self.ChannelNumber,self.Enable)
        elif (self.Channel == ChannelEN.AnalogOut):
            self.Inst.EnableAnalogOutputChannel(self.ChannelNumber,self.Enable)
        elif (self.Channel == ChannelEN.PowerSupply):
            self.Inst.EnablePowerSupplyChannel(self.ChannelNumber,self.Enable)
        elif (self.Channel == ChannelEN.Digital):
            self.Inst.EnableDigitalChannel(self.ChannelNumber,self.Enable)
            
@attribute(OpenTap.Display(Name="Set Sample Rate", Description="", Groups= ["DLS Python Plugin", "ADALM2000"]))
class ADALM2000SetSampleRate(TestStep):
    Inst = property(ADALM2000Instrument, None).add_attribute(OpenTap.Display( "ADALM2000", Order=0))
    Channel = property(ChannelSR,ChannelSR.AnalogIn).add_attribute(OpenTap.Display( "Channel", Order = 1))
    
    @property(Boolean)
    @attribute(Browsable(False))
    def ChannelIsAnalogOut(self):
        return Channel == ChannelSR.AnalogOut
    
    ChannelNumber = property(Int32,0).add_attribute(OpenTap.Display( "Channel Number", Order = 2))\
            .add_attribute(OpenTap.EnabledIf( "ChannelIsAnalogOut", True, HideIfDisabled=True))
    SampleRate = property(Double,100000).add_attribute(OpenTap.Display( "Sample Rate", Order = 3))
    def __init__(self):
        super(ADALM2000SetSampleRate,self).__init__()        
       
    def Run(self):
        if (self.Channel == ChannelSR.AnalogIn):
            self.Inst.SetAnalogInputSampleRate(self.SampleRate)
        elif (self.Channel == ChannelSR.AnalogOut):
            self.Inst.SetAnalogOutputSampleRate(self.ChannelNumber,self.SampleRate)
        elif (self.Channel == ChannelSR.DigitalIn):
            self.Inst.SetDigitalInputSampleRate(self.SampleRate)
        elif (self.Channel == ChannelSR.DigitalOut):
            self.Inst.SetDigitalOutputSampleRate(self.SampleRate)

@attribute(OpenTap.Display(Name="Set Digital Channel Direction", Description="", Groups= ["DLS Python Plugin", "ADALM2000"]))
class ADALM2000SetDigitalChannelDirection(TestStep):
    Inst = property(ADALM2000Instrument, None).add_attribute(OpenTap.Display( "ADALM2000", Order=0))
    IO = property(InputOutput,InputOutput.Output).add_attribute(OpenTap.Display( "Input/Output", Order = 1))
    ChannelNumber = property(Int32,0).add_attribute(OpenTap.Display( "Channel Number", Order = 2))
    def __init__(self):
        super(ADALM2000SetDigitalChannelDirection,self).__init__()        
        
    def Run(self):
        if (self.IO == InputOutput.Input):
            self.Inst.SetDigitalDirectionInput(self.ChannelNumber)
        elif (self.IO == InputOutput.Output):
            self.Inst.SetDigitalDirectionOutput(self.ChannelNumber)