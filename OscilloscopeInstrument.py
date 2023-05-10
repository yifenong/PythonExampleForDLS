from System import Double, String, Byte, Int32
from opentap import *
import OpenTap
from OpenTap import Log
import pyvisa

@attribute(OpenTap.Display(Name="Oscilloscope PyVisa", Description="SCPI Instrument using PyVisa", Groups= ["DLS Python Plugin"])) 
class OscilloscopeInstrumentPyVisa(Instrument):
    VISAAdd = property(String, "TCPIP0::10.82.102.73::hislip0::INSTR").add_attribute(OpenTap.Display( "VISA Address",Order=0))
    IoTimeout = property(Int32, 10000).add_attribute(OpenTap.Display( "Time Out")).add_attribute(OpenTap.Unit( "ms"))
    def __init__(self):
        super(OscilloscopeInstrumentPyVisa,self).__init__()
        self.Name = "Oscilloscope PyVisa"
        self.rm = pyvisa.ResourceManager()
        self.inst = None
        
    def Open(self):
        self.inst = self.rm.open_resource(self.VISAAdd)
        self.inst.timeout = int(self.IoTimeout)
        self.log.Info("Resource Opened")

    def Close(self):
        if (self.rm != None):
            self.rm.close()
        #sys.exit
    
    def GetIdnString(self):
        self.inst.query("*IDN?")
        
    def AutoScale(self):
        return self.inst.query(":AUTOSCALE;*OPC?")

    def GetScreenshot(self):
        data = self.inst.query_binary_values(":DISPlay:DATA? BMP,COLOR", datatype='b')
        print(":DISPlay:DATA? BMP,COLOR")
        return data
   
    def GetState(self):
        data = self.inst.query_binary_values("SYSTEM:SET?", datatype='b')
        print("SYSTEM:SET?")
        return data
        
@attribute(OpenTap.Display(Name="Oscilloscope SCPI Instrument", Description="SCPI Instrument using TAP SCPI", Groups= ["DLS Python Plugin"])) 
class OscilloscopeSCPIInstrument(OpenTap.ScpiInstrument):
    def __init__(self):
        super(OscilloscopeSCPIInstrument,self).__init__()
        self.Name = "Oscilloscope SCPI Instrument"
 
    def GetIdnString(self):
        self.ScpiQuery[String]("*IDN?")

    def AutoScale(self):
        return self.ScpiQuery[String](":AUTOSCALE;*OPC?")

    def GetScreenshot(self):
        data = self.ScpiQueryBlock(":DISPlay:DATA? BMP,COLOR")
        print(":DISPlay:DATA? BMP,COLOR")
        return data
   
    def GetState(self):
        data = self.ScpiQueryBlock("SYSTEM:SET?")
        print("SYSTEM:SET?")
        return data