from opentap import *
import OpenTap
from enum import Enum
from OpenTap import Log
import System
from System import Array, Double, Byte, Int32, String, Boolean # Import types to reference for generic methods

from moku.instruments import WaveformGenerator

@attribute(OpenTap.Display(Name="Moku Go Waveform Generator", Description="", Groups= ["DLS Python Plugin"]))
class MokuGoWaveformGenerator(Instrument):
    IP = property(String, "10.74.65.215").add_attribute(OpenTap.Display( "IP"))
    def __init__(self):
        super(MokuGoWaveformGenerator,self).__init__()
        self.Name = "Moku Go Waveform Generator"
        

    def Open(self):
        global i
        try:
          i = WaveformGenerator(self.IP, force_connect=True)
        except:
          print("Exception - cannot connect!")
          self.log.Error(self.Name + " Exception - cannot connect!")

    def Close(self):
         i.relinquish_ownership()
   
    def GenerateDC(self,ch,dclevel):
        try:
            i.generate_waveform(channel=ch.value, type='DC', dc_level=dclevel)
        except Exception as e:
            print(f'Exception occurred: {e}')
            self.log.Error(self.Name + f'Exception occurred: {e}')
            return None
            
    def GenerateSineWave(self,ch,freq,ampl,dcoffset,phaseoffset):
        try:
            i.generate_waveform(channel=ch.value, type='Sine', amplitude=ampl, 
                frequency=freq, offset=dcoffset, phase=phaseoffset)
        except Exception as e:
            print(f'Exception occurred: {e}')
            self.log.Error(self.Name + f'Exception occurred: {e}')
            return None
            
    def GenerateSquareWave(self,ch,freq,ampl,dut,dcoffset,phaseoffset):
        try:
            i.generate_waveform(channel=ch.value, type='Square', amplitude=ampl, 
                frequency=freq, duty=dut, offset=dcoffset, phase=phaseoffset)
        except Exception as e:
            print(f'Exception occurred: {e}')
            self.log.Error(self.Name + f'Exception occurred: {e}')
            return None