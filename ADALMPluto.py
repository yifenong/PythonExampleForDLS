#https://wiki.analog.com/resources/tools-software/linux-software/pyadi-iio#supported_devicesparts
# install https://github.com/analogdevicesinc/libiio/releases
#Install the libIIO bindings through pip install pylibiio
#Install the PyADI-IIO through pip install pyadi-iio
# sample can be found here https://github.com/analogdevicesinc/pyadi-iio/blob/master/examples/pluto.py
# more samples her https://pysdr.org/content/pluto.html

from opentap import *
import OpenTap
from enum import Enum
from OpenTap import Log
import System
from System import Array, Double, Byte, Int32, String, Boolean # Import types to reference for generic methods

import adi
#import matplotlib.pyplot as plt
import time

import numpy as np


class GetSet(Enum):
    Get = 0
    Set = 1
    def __str__(self):
        return self.name

class PlutoAGC(Enum):
    slow_attack = 0
    fast_attack = 1
    manual = 2
    def __str__(self):
        return self.name
    
class PlutoLoopBack(Enum):
    Disabled = 0
    Digital = 1
    RF = 2
    def __str__(self):
        return self.name
    

class TXRX(Enum):
    Tx = 0
    Rx = 1
    def __str__(self):
        return self.name

@attribute(OpenTap.Display(Name="ADALM Pluto", Description="", Groups= ["DLS Python Plugin"]))
class ADALMPluto(Instrument):
    IP = property(String, "192.168.2.1").add_attribute(OpenTap.Display( "IP",Order=0))
    def __init__(self):
        super(ADALMPluto,self).__init__()
        self.Name = "ADALMPluto"
        self.sdr = None
        
    def Open(self):
        self.log.Info("Connecting to ip:"+self.IP)
        try:
            self.sdr = adi.Pluto("ip:"+self.IP)
            if self.sdr is None:
                print("Connection Error: No ADALM Pluto device available/connected to your PC.")
                self.log.Error("Connection Error: No ADALM Pluto device available/connected to your PC.")
        except:
            print("Exception - cannot connect!")
            self.log.Error(self.Name + " Exception - cannot connect!")

    def Close(self):
        if (self.sdr != None):
            del self.sdr
        
    def RXCarrierFrequency(self,getset=GetSet.Set,freqHz=1000000000):
        if (getset==GetSet.Get):
            return self.sdr.rx_lo
        self.sdr.rx_lo = freqHz

    def RXFrontEndFilterBandwith(self,getset=GetSet.Set,freqHz=4000000):
        if (getset==GetSet.Get):
            return self.sdr.rx_rf_bandwidth
        self.sdr.rx_rf_bandwidth = freqHz
        
    def RXAGCOption(self,getset=GetSet.Set,mode=PlutoAGC.slow_attack):
        if (getset==GetSet.Get):
            return self.sdr.gain_control_mode_chan0
        self.sdr.gain_control_mode_chan0 = mode.name
        
    def RXGain(self,getset=GetSet.Set,gaindb=70):
        if (getset==GetSet.Get):
            return self.sdr.rx_hardwaregain_chan0
        self.sdr.rx_hardwaregain_chan0  = gaindb
        
    def TXCarrierFrequency(self,getset=GetSet.Set,freqHz=1000000000):
        if (getset==GetSet.Get):
            return self.sdr.tx_lo
        self.sdr.tx_lo = freqHz
        
    def TXGain(self,getset=GetSet.Set,gaindb=-50):
        if (getset==GetSet.Get):
            return self.sdr.tx_hardwaregain_chan0
        self.sdr.tx_hardwaregain_chan0  = gaindb
        
    def TXFrontEndFilterBandwith(self,getset=GetSet.Set,freqHz=4000000):
        if (getset==GetSet.Get):
            return self.sdr.tx_rf_bandwidth
        self.sdr.tx_rf_bandwidth = freqHz
        
    def TXCyclicBuffer(self,getset=GetSet.Set,enable=True):
        if (getset==GetSet.Get):
            return self.sdr.tx_cyclic_buffer
        self.sdr.tx_cyclic_buffer = enable
        
    def FIRFilterFile(self,getset=GetSet.Set,path=""):
        if (getset==GetSet.Get):
            return self.sdr.filter
        self.sdr.filter = path
        
    def SampleRate(self,getset=GetSet.Set,rate=1000000):
        if (getset==GetSet.Get):
            return self.sdr.sample_rate
        self.sdr.sample_rate = rate
        
    def LoopBack(self,getset=GetSet.Set,loop=PlutoLoopBack.Disabled):
        if (getset==GetSet.Get):
            return self.sdr.loopback
        self.sdr.loopback = loop.value
        
    def RXBufferSize(self,getset=GetSet.Set,size=10000):
        if (getset==GetSet.Get):
            return self.sdr.rx_buffer_size
        self.sdr.rx_buffer_size = size
        
    def TransmitSamples(self,samples):
        self.sdr.tx(samples)
        
    def StopTransmitting(self):
        self.sdr.tx_destroy_buffer()
        
    def ReceiveSamples(self):
        return self.sdr.rx()
        
    def CreateSineWaveSamples(self,freq=3000000,N=1024):
        fs = self.sdr.sample_rate
        ts = 1 / float(fs)
        t = np.arange(0, N * ts, ts)
        fc = int(freq / (fs / N)) * (fs / N)
        i = np.cos(2 * np.pi * t * fc) * 2 ** 14
        q = np.sin(2 * np.pi * t * fc) * 2 ** 14
        samples = i + 1j * q
        return samples
