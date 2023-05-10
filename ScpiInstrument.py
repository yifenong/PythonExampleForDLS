from System import Double, String, Byte, Int32
from opentap import *
import OpenTap

import numpy as np

from .DLSOutputInput import *

@attribute(OpenTap.Display(Name="SCPI Instrument", Description="SCPI Instrument using TAP SCPI", Groups= ["DLS Python Plugin"])) 
class SCPIInstrument(OpenTap.ScpiInstrument):
    def __init__(self):
        super(SCPIInstrument,self).__init__()
        self.Name = "SCPI Instrument"
    def GetIdnString(self):
        return self.ScpiQuery[String]("*IDN?")
    def GetByte(self,cmd):
        data = self.ScpiQueryBlock(cmd)
        print(cmd)
        return data
    def GetString(self,cmd):
        return self.ScpiQuery[String](cmd)
        
@attribute(OpenTap.Display(Name="SCPI Get Byte Array", Description="", Groups= ["DLS Python Plugin", "SCPI"]))
class SCPIGetByte(DLSStep):
    ScpiInst = property(SCPIInstrument, None).add_attribute(OpenTap.Display( "SCPI Instrument"))
    Cmd = property(String, '').add_attribute(OpenTap.Display( "Command"))
    def __init__(self):
        super(SCPIGetByte,self).__init__()
        
    def Run(self):
        y = self.ScpiInst.GetByte(self.Cmd)
        super().OutputToDLS("ByteArray",["ByteArray"] ,[y], True)
        
@attribute(OpenTap.Display(Name="SCPI Get String", Description="", Groups= ["DLS Python Plugin", "SCPI"]))
class SCPIGetString(DLSStep):
    ScpiInst = property(SCPIInstrument, None).add_attribute(OpenTap.Display( "SCPI Instrument"))
    Cmd = property(String, '*IDN?').add_attribute(OpenTap.Display( "Command"))
    def __init__(self):
        super(SCPIGetString,self).__init__()
        
    def Run(self):
        y = self.ScpiInst.GetString(self.Cmd)
        super().OutputToDLS("String",["String"] ,[y])
        print(y)