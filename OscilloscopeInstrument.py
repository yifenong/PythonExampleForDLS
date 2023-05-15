from System import Double, String, Byte, Int32
from opentap import *
import OpenTap
from OpenTap import Log
import numpy as np
        
@attribute(OpenTap.Display(Name="Oscilloscope", Groups= ["DLS Python Plugin"])) 
class OscilloscopeSCPIInstrument(OpenTap.ScpiInstrument):
    def __init__(self):
        super(OscilloscopeSCPIInstrument,self).__init__()
        self.Name = "Oscilloscope"
        self.IoTimeout = 10000
 
    def GetIdnString(self):
        return self.ScpiQuery[String]("*IDN?")

    def AutoScale(self):
        return self.ScpiQuery[String](":AUTOSCALE;*OPC?")
        
    def MeasureFrequency(self,channel):
        return self.ScpiQuery[String]("MEASURE:FREQUENCY? CHANNEL" + str(channel))

    def GetScreenshot(self):
        data = self.ScpiQueryBlock(":DISPlay:DATA? BMP,COLOR")
        print(":DISPlay:DATA? BMP,COLOR")
        return data
        
    def GetTraceData(self,channel):
        self.ScpiCommand("WAVEFORM:SOURCE CHANNEL" + str(channel))
        self.ScpiCommand("WAVEFORM:POINTS:MODE MAXIMUM")
        self.ScpiCommand(":WAVeform:FORMat BYTE")
        preamble = self.ScpiQuery[String](":WAVEFORM:PREAMBLE?").split(",")
        t = int(preamble[1])
        fPoints = int(preamble[2])
        fCount = int(preamble[3])
        fXincrement = float(preamble[4])
        fXorigin = float(preamble[5])
        fXreference = float(preamble[6])
        fYincrement = float(preamble[7])
        fYorigin = float(preamble[8])
        fYreference = float(preamble[9])
        rawdata = self.ScpiQueryBlock(":WAVeform:DATA?")
        x = np.empty(len(rawdata),dtype=np.double)
        y = np.empty(len(rawdata),dtype=np.double)
        for idx, d in enumerate(rawdata):
            x[idx] = (fXorigin + ( ( float(idx) - fXreference) * fXincrement))
            y[idx] = ((d - fYreference) * fYincrement) + fYorigin
        return [x,y]
        
        
        
        
        
        
        
        
        
        
        
        
        
        
 