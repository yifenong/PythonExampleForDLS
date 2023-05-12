import sys
import opentap
from opentap import *
import OpenTap
import math
from OpenTap import Log, EnabledIfAttribute
import System
from System import Array, Double, Byte, Int32, String, Boolean 
from System.ComponentModel import BrowsableAttribute 
import System.Xml
from System.Xml.Serialization import XmlIgnoreAttribute
from .OscilloscopeInstrument import *
from .DLSOutputInput import *
     
@attribute(OpenTap.Display(Name="Identify", Description="", Groups= ["DLS Python Plugin", "Oscilloscope"]))
class OscilloscopeIdentify(TestStep):
    ScpiInst = property(OscilloscopeSCPIInstrument, None).add_attribute(OpenTap.Display( "Oscilloscope"))
    
    def __init__(self):
        super(OscilloscopeIdentify,self).__init__()
        
    def Run(self):
        idn = self.ScpiInst.GetIdnString()
        self.log.Info("IDN: "+str(idn))

@attribute(OpenTap.Display(Name="Autoscale", Description="", Groups= ["DLS Python Plugin", "Oscilloscope"]))
class OscilloscopeAutoScale(TestStep):
    ScpiInst = property(OscilloscopeSCPIInstrument, None).add_attribute(OpenTap.Display( "Oscilloscope"))
    
    def __init__(self):
        super(OscilloscopeAutoScale,self).__init__()
        
    def Run(self):
        self.ScpiInst.AutoScale()
        
@attribute(OpenTap.Display(Name="Measure Frequency", Description="", Groups= ["DLS Python Plugin", "Oscilloscope"]))
class OscilloscopeMeasureFrequency(TestStep):
    ScpiInst = property(OscilloscopeSCPIInstrument, None).add_attribute(OpenTap.Display( "Oscilloscope"))
    Channel = property(Int32, 1).add_attribute(OpenTap.Display( "Channel"))
    
    def __init__(self):
        super(OscilloscopeMeasureFrequency,self).__init__()
        
    def Run(self):
        freq = self.ScpiInst.MeasureFrequency(self.Channel)
        self.log.Info("Frequency: "+str(freq))
        self.PublishResult("Measure Frequency", ["Frequency"], [freq])  
        
@attribute(OpenTap.Display(Name="Screenshot", Description="", Groups= ["DLS Python Plugin", "Oscilloscope"]))
class OscilloscopeGetScreenshot(DLSStep):
    ScpiInst = property(OscilloscopeSCPIInstrument, None).add_attribute(OpenTap.Display( "Oscilloscope"))
    
    def __init__(self):
        super(OscilloscopeGetScreenshot,self).__init__()
        
    def Run(self):
        y = self.ScpiInst.GetScreenshot()
        super().OutputToDLS("Screenshot",["Screenshot"] ,[y], True)
        
@attribute(OpenTap.Display(Name="Trace Data", Description="", Groups= ["DLS Python Plugin", "Oscilloscope"]))
class OscilloscopeGetTraceData(DLSStep):
    ScpiInst = property(OscilloscopeSCPIInstrument, None).add_attribute(OpenTap.Display( "Oscilloscope"))
    Channel = property(Int32, 1).add_attribute(OpenTap.Display( "Channel"))
    
    def __init__(self):
        super(OscilloscopeGetTraceData,self).__init__()
        
    def Run(self):
        x,y = self.ScpiInst.GetTraceData(self.Channel)
        super().OutputToDLS("TraceData1",["X","Y"] ,[x,y])
        
        
        
        
        
        
        
        
        

        
