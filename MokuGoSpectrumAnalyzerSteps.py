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

from .MokuGoSpectrumAnalyzer import *
from .DLSOutputInput import *

import datetime

@attribute(OpenTap.Display(Name="Get Data", Description="", Groups= ["DLS Python Plugin", "Moku Go Spectrum Analyzer"]))
class MGGetData(DLSStep):
    Inst = property(MokuGoSpectrumAnalyzer, None).add_attribute(OpenTap.Display( "MokuGo Spectrum Analyzer", Order=0))
    def __init__(self):
        super(MGGetData,self).__init__()
        
        
    def Run(self):
        v = self.Inst.GetData()
        if (v == ''):
            self.log.Info = 'Empty String'
        else:
            ch1data = v['ch1']
            ch2data = v['ch2']
            freqdata = v['frequency']
            super().OutputToDLS("Result",["frequency","ch1","ch2"] ,[freqdata,ch1data,ch2data])
            
@attribute(OpenTap.Display(Name="Set Span", Description="", Groups= ["DLS Python Plugin", "Moku Go Spectrum Analyzer"]))
class MGSetSpan(TestStep):
    Inst = property(MokuGoSpectrumAnalyzer, None).add_attribute(OpenTap.Display( "MokuGo Spectrum Analyzer", Order=0))
    SpanStart = property(Double, -1e-3).add_attribute(OpenTap.Display( "Span Start", Order=1)).add_attribute(OpenTap.Unit( "Hz"))
    SpanStop = property(Double, 1e-3).add_attribute(OpenTap.Display( "Span Stop", Order=2)).add_attribute(OpenTap.Unit( "Hz"))  
    def __init__(self):
        super(MGSetSpan,self).__init__()

    def Run(self):
        self.Inst.SetSpan(self.SpanStart,self.SpanStop)
        
@attribute(OpenTap.Display(Name="Set RBW", Description="", Groups= ["DLS Python Plugin", "Moku Go Spectrum Analyzer"]))
class MGSetRBW(TestStep):
    Inst = property(MokuGoSpectrumAnalyzer, None).add_attribute(OpenTap.Display( "MokuGo Spectrum Analyzer", Order=0))
    Mode = property(RBWMode, RBWMode.Auto).add_attribute(OpenTap.Display( "Mode", Order=1))
    
    @property(Boolean)
    @attribute(Browsable(False))
    def ModeIsManual(self):
        return Mode == RBWMode.Manual
    
    RBWValue = property(Double, 5000).add_attribute(OpenTap.Display( "RBW Value", Order=2))\
        .add_attribute(OpenTap.Unit( "Hz")).add_attribute(OpenTap.EnabledIf("ModeIsManual", True , HideIfDisabled=True))
    def __init__(self):
        super(MGSetRBW,self).__init__()
       
    def Run(self):
        self.Inst.SetRBW(self.Mode,self.RBWValue)