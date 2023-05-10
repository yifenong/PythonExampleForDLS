from opentap import *
import OpenTap
from enum import Enum
from OpenTap import Log
import System
from System import Array, Double, Byte, Int32, String, Boolean # Import types to reference for generic methods

from moku.instruments import Oscilloscope

class MokuGoSource(Enum):
    Input1 = 0
    Input2 = 1
    Output1 = 2
    Output2 = 3
    def __str__(self):
        return self.name
    
class MokuGoChannel(Enum):
    One = 1
    Two = 2
    def __str__(self):
        return self.name
    
class MokuGoTrigger(Enum):
    Edge = 0
    Pulse = 1
    def __str__(self):
        return self.name

@attribute(OpenTap.Display(Name="Moku Go Oscilloscope", Description="", Groups= ["DLS Python Plugin"]))
class MokuGoOscilloscope(Instrument):
    IP = property(String, "10.74.65.215").add_attribute(OpenTap.Display( "IP"))
    def __init__(self):
        super(MokuGoOscilloscope,self).__init__()
        self.Name = "Moku Go Oscilloscope"
        

    def Open(self):
        global i
        try:
          i = Oscilloscope(self.IP, force_connect=True)
        except:
          print("Exception - cannot connect!")
          self.log.Error(self.Name + " Exception - cannot connect!")

    def Close(self):
         i.relinquish_ownership()

    def RecordSignal(self,SpanStart,SpanStop):
        try:
            # Set the span to from -1ms to 1ms i.e. trigger point centred
            i.set_timebase(SpanStart, SpanStop)

            # Get and print a single frame  of data (time series
            # of voltage per channel)
            data = i.get_data()
            return data
            #print(data['ch1'], data['ch2'], data['time'])

        except Exception as e:
            print(f'Exception occurred: {e}')
            self.log.Error(self.Name + f'Exception occurred: {e}')
            return None
            
    def SetTrigger(self,trigtype,source,level):
        i.set_trigger(type=trigtype.name, source=source.name, level=level)
            
    def GenerateSineWave(self,channel,amp,freq):
        i.generate_waveform(channel.value, 'Sine', amplitude=amp, frequency=freq)
            
    def SetSource(self,channel,source):
        i.set_source(channel.value, source.name)
            
    def SetPowerSupply(self,channel,enab,volt,curr):
        i.set_power_supply(channel.value, enable=enab,voltage=volt,current=curr)