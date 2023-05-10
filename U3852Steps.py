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

from .U3852Dut import *

@attribute(OpenTap.Display(Name="Filter", Description="", Groups= ["DLS Python Plugin", "U3852"]))     
class SetFilter(TestStep):
    Dut = property(U3852Dut, None).add_attribute(OpenTap.Display( "U3852 Dut"))
    FName = property(U3852Filter, U3852Filter.Open).add_attribute(OpenTap.Display( "Filter Path"))
    def __init__(self):
        super(SetFilter,self).__init__()        
        
    def Run(self):
        self.log.Info("Setting Filter "+str(self.FName));
        self.Dut.SetPath(self.FName)
        
@attribute(OpenTap.Display(Name="Mixer", Description="", Groups= ["DLS Python Plugin", "U3852"]))     
class SetMixer(TestStep):
    Dut = property(U3852Dut, None).add_attribute(OpenTap.Display( "U3852 Dut"))
    Mixer = property(U3852Mixer, U3852Mixer.Thru).add_attribute(OpenTap.Display( "Mixer Path"))
    def __init__(self):
        super(SetMixer,self).__init__()        
        
    def Run(self):
        self.log.Info("Setting Mixer "+str(self.Mixer));
        self.Dut.SetPath(self.Mixer)
        
@attribute(OpenTap.Display(Name="Amplifier", Description="", Groups= ["DLS Python Plugin", "U3852"]))     
class SetAmplifier(TestStep):
    Dut = property(U3852Dut, None).add_attribute(OpenTap.Display( "U3852 Dut"))
    Amplifier = property(U3852Amplifier, U3852Amplifier.Thru).add_attribute(OpenTap.Display( "Amplifier Path"))
    def __init__(self):
        super(SetAmplifier,self).__init__()        
        
    def Run(self):
        self.log.Info("Setting Amplifier "+str(self.Amplifier));
        self.Dut.SetPath(self.Amplifier)