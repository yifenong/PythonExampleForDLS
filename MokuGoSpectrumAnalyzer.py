from opentap import *
import OpenTap
from enum import Enum
from OpenTap import Log
import System
from System import Array, Double, Byte, Int32, String, Boolean # Import types to reference for generic methods

from moku.instruments import SpectrumAnalyzer

class RBWMode(Enum):
    Auto = 0
    Manual = 1
    Minimum = 2
    def __str__(self):
        return self.name

@attribute(OpenTap.Display(Name="Moku Go Spectrum Analyzer", Description="", Groups= ["DLS Python Plugin"]))
class MokuGoSpectrumAnalyzer(Instrument):
    IP = property(String, "10.74.65.215").add_attribute(OpenTap.Display( "IP"))
    def __init__(self):
        super(MokuGoSpectrumAnalyzer,self).__init__()
        self.Name = "Moku Go Spectrum Analyzer"

    def Open(self):
        global i
        try:
          i = SpectrumAnalyzer(self.IP, force_connect=True)
        except:
          print("Exception - cannot connect!")
          self.log.Error(self.Name + " Exception - cannot connect!")

    def Close(self):
         i.relinquish_ownership()
            
    def SetSpan(self,start,stop):
         i.set_span(start, stop)
            
    def SetRBW(self,md,value=5000):
         if (md != md.Auto):
            i.set_rbw(mode=md,rbw_value=value)
         else:
            i.set_rbw(mode=md)

    def GetData(self):
        try:
            data = i.get_data()
            return data
            #print(data['ch1'], data['ch2'], data['frequency'])

        except Exception as e:
            print(f'Exception occurred: {e}')
            self.log.Error(self.Name + f'Exception occurred: {e}')
            return None