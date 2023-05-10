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

from .OscilloscopeInstrument import *
from .DLSOutputInput import *

from inspect import signature

from enum import Enum

import numpy as np

class ScipInstrumentType(Enum):
    PyVisa = 0
    ScpiInstrument = 1
    def __str__(self):
        return self.name
        
@attribute(OpenTap.Display(Name="Screenshot", Description="", Groups= ["DLS Python Plugin", "Oscilloscope"]))
class OscilloscopeGetScreenshot(DLSStep):
    ScpiType = property(ScipInstrumentType, ScipInstrumentType.ScpiInstrument).add_attribute(OpenTap.Display( "Oscilloscope"))
    
    @property(Boolean)
    @attribute(Browsable(False))
    def IsPyVisa(self):
        return self.ScpiType  == ScipInstrumentType.PyVisa
    
    ScpiInst = property(OscilloscopeSCPIInstrument, None).add_attribute(OpenTap.Display( "Oscilloscope"))\
        .add_attribute(OpenTap.EnabledIf( "IsPyVisa", False, HideIfDisabled=True))
    PyVisaInst = property(OscilloscopeInstrumentPyVisa, None).add_attribute(OpenTap.Display( "Oscilloscope"))\
        .add_attribute(OpenTap.EnabledIf( "IsPyVisa", True, HideIfDisabled=True))
    
    def __init__(self):
        super(OscilloscopeGetScreenshot,self).__init__()
        
    def Run(self):
        if (self.IsPyVisa):
            y = self.PyVisaInst.GetScreenshot()
        else:
            y = self.ScpiInst.GetScreenshot()
        super().OutputToDLS("Screenshot",["Screenshot"] ,[y], True)

@attribute(OpenTap.Display(Name="Get State", Description="", Groups= ["DLS Python Plugin", "Oscilloscope"]))
class OscilloscopeGetState(DLSStep):
    ScpiType = property(ScipInstrumentType, ScipInstrumentType.ScpiInstrument).add_attribute(OpenTap.Display( "Oscilloscope"))
    
    @property(Boolean)
    @attribute(Browsable(False))
    def IsPyVisa(self):
        return self.ScpiType  == ScipInstrumentType.PyVisa
    
    ScpiInst = property(OscilloscopeSCPIInstrument, None).add_attribute(OpenTap.Display( "Oscilloscope"))\
        .add_attribute(OpenTap.EnabledIf( "IsPyVisa", False, HideIfDisabled=True))
    PyVisaInst = property(OscilloscopeInstrumentPyVisa, None).add_attribute(OpenTap.Display( "Oscilloscope"))\
        .add_attribute(OpenTap.EnabledIf( "IsPyVisa", True, HideIfDisabled=True))
        
    def __init__(self):
        super(OscilloscopeGetState,self).__init__()
        
    def Run(self):
        if (self.IsPyVisa):
            y = self.PyVisaInst.GetState()
        else:
            y = self.ScpiInst.GetState()
        super().OutputToDLS("State",["State"] ,[y], True)
        
@attribute(OpenTap.Display(Name="Autoscale", Description="", Groups= ["DLS Python Plugin", "Oscilloscope"]))
class OscilloscopeAutoScale(TestStep):
    ScpiType = property(ScipInstrumentType, ScipInstrumentType.ScpiInstrument).add_attribute(OpenTap.Display( "Oscilloscope"))
    
    @property(Boolean)
    @attribute(Browsable(False))
    def IsPyVisa(self):
        return self.ScpiType  == ScipInstrumentType.PyVisa
    
    ScpiInst = property(OscilloscopeSCPIInstrument, None).add_attribute(OpenTap.Display( "Oscilloscope"))\
        .add_attribute(OpenTap.EnabledIf( "IsPyVisa", False, HideIfDisabled=True))
    PyVisaInst = property(OscilloscopeInstrumentPyVisa, None).add_attribute(OpenTap.Display( "Oscilloscope"))\
        .add_attribute(OpenTap.EnabledIf( "IsPyVisa", True, HideIfDisabled=True))
        
    def __init__(self):
        super(OscilloscopeAutoScale,self).__init__()
        
    def Run(self):
        if (self.IsPyVisa):
            self.PyVisaInst.AutoScale()
        else:
            self.ScpiInst.AutoScale()