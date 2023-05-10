from opentap import *
import OpenTap
from enum import Enum
from OpenTap import Log
import System
from System import Array, Double, Byte, Int32, String, Boolean # Import types to reference for generic methods

from moku.instruments import ArbitraryWaveformGenerator

import numpy as np

class MokuGoSampleRate(Enum):
    Auto = 0
    _125Ms = 1
    _62_5Ms = 2
    _31_25Ms = 3
    _15_625Ms = 4
    def __str__(self):
        return self.name

@attribute(OpenTap.Display(Name="Moku Go AWG", Description="", Groups= ["DLS Python Plugin"]))
class MokuGoAWG(Instrument):
    IP = property(String, "10.74.65.215").add_attribute(OpenTap.Display( "IP"))
    def __init__(self):
        super(MokuGoAWG,self).__init__()
        self.Name = "Moku Go AWG"

    def Open(self):
        global i
        try:
          i = ArbitraryWaveformGenerator(self.IP, force_connect=True)
        except:
          print("Exception - cannot connect!")
          self.log.Error(self.Name + " Exception - cannot connect!")

    def Close(self):
         i.relinquish_ownership()
            
    def GenerateSquareWave(self,points,ch,sr,freq,ampl):
        try:
            t = np.linspace(0, 1, points)
            sq_wave = np.array([-1.0 if x < 0.5 else 1.0 for x in t])
            i.generate_waveform(channel=ch.value, sample_rate=sr.name,
                        lut_data=list(sq_wave), frequency=freq,
                        amplitude=ampl)
        except Exception as e:
            print(f'Exception occurred: {e}')
            self.log.Error(self.Name + f'Exception occurred: {e}')
            return None