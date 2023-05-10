from opentap import *
import OpenTap
from enum import Enum
from OpenTap import Log
import System
from System import Array, Double, Byte, Int32, String, Boolean # Import types to reference for generic methods

import time

from moku.instruments import FrequencyResponseAnalyzer

@attribute(OpenTap.Display(Name="Moku Go Frequency Response", Description="", Groups= ["DLS Python Plugin"]))
class MokuGoFrequencyResponse(Instrument):
    IP = property(String, "10.74.65.215").add_attribute(OpenTap.Display( "IP"))
    def __init__(self):
        super(MokuGoFrequencyResponse,self).__init__()
        self.Name = "Moku Go Frequency Response"

    def Open(self):
        global i
        try:
          i = FrequencyResponseAnalyzer(self.IP, force_connect=True)
        except:
          print("Exception - cannot connect!")
          self.log.Error(self.Name + " Exception - cannot connect!")

    def Close(self):
         i.relinquish_ownership()

    def GetData(self,startf=20e6,stopf=100,points=256,avgtime=1e-3,avgcycles=5,settlecycles=5,settletime=1e-3,ch1amp=0.1,ch2amp=0.1):
        try:
            i.set_sweep(start_frequency=startf, stop_frequency=stopf, num_points=points,averaging_time=avgtime,\
                averaging_cycles=avgcycles, settling_cycles=settlecycles,settling_time=settletime)
            i.set_output(1, ch1amp)
            i.set_output(2, ch2amp)
            i.start_sweep(single=True)
            data = i.get_data()
            return data
            #print(data['ch1'], data['ch2'], data['time'])

        except Exception as e:
            print(f'Exception occurred: {e}')
            self.log.Error(self.Name + f'Exception occurred: {e}')
            return None