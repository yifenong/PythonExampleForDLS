import sys
import opentap
import clr
clr.AddReference("System.Collections")
from System.Collections.Generic import List
from opentap import *
import OpenTap 

import math
from OpenTap import Log, EnabledIfAttribute, Output

import numpy as np

import matplotlib.pyplot as plt

import datetime
import time
## Import necessary .net APIs
# These represents themselves as regular Python modules but they actually reflect
# .NET libraries.
import System
from System import Array, Double, Byte, Int32, String, Boolean # Import types to reference for generic methods
from System.ComponentModel import BrowsableAttribute # BrowsableAttribute can be used to hide things from the user.
import System.Xml
from System.Xml.Serialization import XmlIgnoreAttribute

from .ADALMPluto import *
from .DLSOutputInput import *

@attribute(OpenTap.Display(Name="Generate Sine Wave", Description="", Groups= ["DLS Python Plugin", "ADALMPluto"]))
class ADALMPlutoGenerateSineWave(TestStep):
    Inst = property(ADALMPluto, None).add_attribute(OpenTap.Display( "ADALMPluto", Order=0))
    Freq = property(Int32, 3000000).add_attribute(OpenTap.Display( "Frequency", Order=1)).add_attribute(OpenTap.Unit( "Hz"))
    CarrierFreq = property(Int32, 2000000000).add_attribute(OpenTap.Display( "Carrier Frequency", Order=2)).add_attribute(OpenTap.Unit( "Hz"))
    Samples = property(Int32, 1024).add_attribute(OpenTap.Display( "Samples", Order=3))
    SampleRate = property(Int32, 30000000).add_attribute(OpenTap.Display( "Sample Rate", Order=4)).add_attribute(OpenTap.Unit( "Hz"))
    TXGain = property(Double, -30).add_attribute(OpenTap.Display( "TX Gain", Order=5)).add_attribute(OpenTap.Unit( "dB"))
    OutputValue = property(Double, 0.0)\
        .add_attribute(Display("Output Value", "", "Output", 0))\
        .add_attribute(Output())
    def __init__(self):
        super(ADALMPlutoGenerateSineWave,self).__init__()        
        
    def Run(self):
        self.Inst.StopTransmitting()
        self.Inst.SampleRate(GetSet.Set,self.SampleRate)
        self.Inst.TXGain(GetSet.Set,self.TXGain)
        self.Inst.TXCarrierFrequency(GetSet.Set,self.CarrierFreq)
        s = self.Inst.CreateSineWaveSamples(self.Freq,self.Samples)
        self.Inst.TXCyclicBuffer(GetSet.Set,True)
        self.Inst.TransmitSamples(s)
        print(s)
    

@attribute(OpenTap.Display(Name="Receive Samples", Description="", Groups= ["DLS Python Plugin", "ADALMPluto"]))
class ADALMPlutoReceiveSamples(DLSStep):
    Inst = property(ADALMPluto, None).add_attribute(OpenTap.Display( "ADALMPluto", Order=0))
    BufferSize = property(Int32, 1024).add_attribute(OpenTap.Display( "Buffer Size", Order=1))
    CarrierFreq = property(Int32, 2000000000).add_attribute(OpenTap.Display( "Carrier Frequency", Order=2)).add_attribute(OpenTap.Unit( "Hz"))
    Repeat = property(Int32, 10).add_attribute(OpenTap.Display( "Repeat Count", Order=3))

    def __init__(self):
        super(ADALMPlutoReceiveSamples,self).__init__()      
        
    def Run(self):
        self.Inst.RXCarrierFrequency(GetSet.Set,self.CarrierFreq)
        self.Inst.RXBufferSize(GetSet.Set,self.BufferSize)
        sr = int(self.Inst.SampleRate(GetSet.Get))
        for r in range(self.Repeat):
            print('Count:'+str(r))
            rx_samples = self.Inst.ReceiveSamples()
            # try:
                # Pxx_den, f = plt.psd(rx_samples, Fs=sr, sides='twosided')
                # time.sleep(0.1)
                # #self.log.Info("PSD finished")
            # except Exception as e:
                # print(str(e))
                # self.log.Error(str(e))
                # return
                
        real = np.real(rx_samples)
        imag = np.imag(rx_samples)
        mag = np.absolute(rx_samples)
        phase = np.angle(rx_samples)
        xdata = np.arange(len(real))
        super().OutputToDLS("ReceivedSamples",["X", "Real", "Imaginary", "Magnitude", "Phase"] , [xdata, real, imag, mag, phase])
        # super().OutputToDLS("ReceivedSamplesPSD",["Frequency" , "PowerSpectralDensity"] ,[f, Pxx_den])  
       
@attribute(OpenTap.Display(Name="Carrier Frequency", Description="", Groups= ["DLS Python Plugin", "ADALMPluto"]))
class ADALMPlutoCarrierFrequency(DLSStep):
    Inst = property(ADALMPluto, None).add_attribute(OpenTap.Display( "ADALMPluto", Order=0))
    GetOrSet = property(GetSet, GetSet.Set).add_attribute(OpenTap.Display( "Get Or Set", Order=1))
    
    @property(Boolean)
    @attribute(Browsable(False))
    def IsSet(self):
        return self.GetOrSet == GetSet.Set
    
    TxRx = property(TXRX, TXRX.Tx).add_attribute(OpenTap.Display( "TX or RX", Order=2))
    Freq = property(Int32, 1000000000).add_attribute(OpenTap.Display( "Frequency", Order=3)).add_attribute(OpenTap.Unit( "Hz"))\
            .add_attribute(OpenTap.EnabledIf( "IsSet", True, HideIfDisabled=True))
            
    def __init__(self):
        super(ADALMPlutoCarrierFrequency,self).__init__()        
        
    def Run(self):
        if (self.IsSet):
            if (self.TxRx == TXRX.Rx):
                self.Inst.RXCarrierFrequency(GetSet.Set,self.Freq)
            elif (self.TxRx == TXRX.Tx):
                self.Inst.TXCarrierFrequency(GetSet.Set,self.Freq)
        else:
            v = 0
            if (self.TxRx == TXRX.Rx):
                v = self.Inst.RXCarrierFrequency(GetSet.Get)
            elif (self.TxRx == TXRX.Tx):
                v = self.Inst.TXCarrierFrequency(GetSet.Get)
            print(v)
            super().OutputToDLS("Frequency", ["Timestamp", "Hz"], [float(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")) , float(v)])
            
@attribute(OpenTap.Display(Name="Front End Filter Bandwith", Description="", Groups= ["DLS Python Plugin", "ADALMPluto"]))
class ADALMPlutoFrontEndFilterBandwith(TestStep):
    Inst = property(ADALMPluto, None).add_attribute(OpenTap.Display( "ADALMPluto", Order=0))
    GetOrSet = property(GetSet, GetSet.Set).add_attribute(OpenTap.Display( "Get Or Set", Order=1))
    
    @property(Boolean)
    @attribute(Browsable(False))
    def IsSet(self):
        return self.GetOrSet == GetSet.Set
    
    TxRx = property(TXRX, TXRX.Tx).add_attribute(OpenTap.Display( "TX or RX", Order=2))
    BW = property(Int32, 4000000).add_attribute(OpenTap.Display( "Bandwidth", Order=3)).add_attribute(OpenTap.Unit( "Hz"))\
            .add_attribute(OpenTap.EnabledIf( "IsSet", True, HideIfDisabled=True))
            
    def __init__(self):
        super(ADALMPlutoFrontEndFilterBandwith,self).__init__()        
        
    def Run(self):
        if (self.IsSet):
            if (self.TxRx == TXRX.Rx):
                self.Inst.RXFrontEndFilterBandwith(GetSet.Set,self.BW)
            elif (self.TxRx == TXRX.Tx):
                self.Inst.TXFrontEndFilterBandwith(GetSet.Set,self.BW)
        else:
            v = 0
            if (self.TxRx == TXRX.Rx):
                v = self.Inst.RXFrontEndFilterBandwith(GetSet.Get)
            elif (self.TxRx == TXRX.Tx):
                v = self.Inst.TXFrontEndFilterBandwith(GetSet.Get)
            print(v)
            super().OutputToDLS("Bandwidth", ["Timestamp", "Hz"], [float(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")) , float(v)])
            
@attribute(OpenTap.Display(Name="Gain", Description="", Groups= ["DLS Python Plugin", "ADALMPluto"]))
class ADALMPlutoGain(TestStep):
    Inst = property(ADALMPluto, None).add_attribute(OpenTap.Display( "ADALMPluto", Order=0))
    GetOrSet = property(GetSet, GetSet.Set).add_attribute(OpenTap.Display( "Get Or Set", Order=1))
    
    @property(Boolean)
    @attribute(Browsable(False))
    def IsSet(self):
        return self.GetOrSet == GetSet.Set
    
    TxRx = property(TXRX, TXRX.Tx).add_attribute(OpenTap.Display( "TX or RX", Order=2))
    Gain = property(Double, 0).add_attribute(OpenTap.Display( "Gain", Order=3)).add_attribute(OpenTap.Unit( "dB"))\
            .add_attribute(OpenTap.EnabledIf( "IsSet", True, HideIfDisabled=True))
            
    def __init__(self):
        super(ADALMPlutoGain,self).__init__()        
        
    def Run(self):
        if (self.IsSet):
            if (self.TxRx == TXRX.Rx):
                self.Inst.RXGain(GetSet.Set,self.Gain)
            elif (self.TxRx == TXRX.Tx):
                self.Inst.TXGain(GetSet.Set,self.Gain)
        else:
            v = 0
            if (self.TxRx == TXRX.Rx):
                v = self.Inst.RXGain(GetSet.Get)
            elif (self.TxRx == TXRX.Tx):
                v = self.Inst.TXGain(GetSet.Get)
            print(v)
            super().OutputToDLS("Gain", ["Timestamp", "dB"], [float(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")) , float(v)])
            
@attribute(OpenTap.Display(Name="RX AGC Mode", Description="", Groups= ["DLS Python Plugin", "ADALMPluto"]))
class ADALMPlutoRXAGCMode(TestStep):
    Inst = property(ADALMPluto, None).add_attribute(OpenTap.Display( "ADALMPluto", Order=0))
    GetOrSet = property(GetSet, GetSet.Set).add_attribute(OpenTap.Display( "Get Or Set", Order=1))
    
    @property(Boolean)
    @attribute(Browsable(False))
    def IsSet(self):
        return self.GetOrSet == GetSet.Set
        
    AGCMode = property(PlutoAGC, PlutoAGC.slow_attack).add_attribute(OpenTap.Display( "AGC Mode", Order=1))\
            .add_attribute(OpenTap.EnabledIf( "IsSet", True, HideIfDisabled=True))
    
    def __init__(self):
        super(ADALMPlutoRXAGCMode,self).__init__()        
        
    def Run(self):
        if (self.IsSet):
            self.Inst.RXAGCOption(GetSet.Set,self.AGCMode)
        else:
            v = self.Inst.RXAGCOption(GetSet.Get)
            print(v)
            
@attribute(OpenTap.Display(Name="TX Cyclic Buffer", Description="", Groups= ["DLS Python Plugin", "ADALMPluto"]))
class ADALMPlutoTXCyclicBuffer(TestStep):
    Inst = property(ADALMPluto, None).add_attribute(OpenTap.Display( "ADALMPluto", Order=0))
    GetOrSet = property(GetSet, GetSet.Set).add_attribute(OpenTap.Display( "Get Or Set", Order=1))
    
    @property(Boolean)
    @attribute(Browsable(False))
    def IsSet(self):
        return self.GetOrSet == GetSet.Set
        
    Enable = property(bool, True).add_attribute(OpenTap.Display( "Enable", Order=1))\
            .add_attribute(OpenTap.EnabledIf( "IsSet", True, HideIfDisabled=True))
    
    def __init__(self):
        super(ADALMPlutoTXCyclicBuffer,self).__init__()        
        
    def Run(self):
        if (self.IsSet):
            self.Inst.TXCyclicBuffer(GetSet.Set,self.Enable)
        else:
            v = self.Inst.TXCyclicBuffer(GetSet.Get)
            print(v)
            super().OutputToDLS("TXCyclicBufferEnable", ["Timestamp", "Enable"], [float(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")) , v])
            
@attribute(OpenTap.Display(Name="FIR Filter File", Description="", Groups= ["DLS Python Plugin", "ADALMPluto"]))
class ADALMPlutoFIRFilterFile(TestStep):
    Inst = property(ADALMPluto, None).add_attribute(OpenTap.Display( "ADALMPluto", Order=0))
    GetOrSet = property(GetSet, GetSet.Set).add_attribute(OpenTap.Display( "Get Or Set", Order=1))
    
    @property(Boolean)
    @attribute(Browsable(False))
    def IsSet(self):
        return self.GetOrSet == GetSet.Set
        
    Path = property(String, "").add_attribute(OpenTap.Display( "Path", Order=1))\
            .add_attribute(OpenTap.EnabledIf( "IsSet", True, HideIfDisabled=True))
    
    def __init__(self):
        super(ADALMPlutoFIRFilterFile,self).__init__()        
        
    def Run(self):
        if (self.IsSet):
            self.Inst.FIRFilterFile(GetSet.Set,self.Path)
        else:
            v = self.Inst.FIRFilterFile(GetSet.Get)
            print(v)
            
@attribute(OpenTap.Display(Name="Sample Rate", Description="", Groups= ["DLS Python Plugin", "ADALMPluto"]))
class ADALMPlutoSampleRate(TestStep):
    Inst = property(ADALMPluto, None).add_attribute(OpenTap.Display( "ADALMPluto", Order=0))
    GetOrSet = property(GetSet, GetSet.Set).add_attribute(OpenTap.Display( "Get Or Set", Order=1))
    
    @property(Boolean)
    @attribute(Browsable(False))
    def IsSet(self):
        return self.GetOrSet == GetSet.Set
        
    SR = property(Int32, 1000000).add_attribute(OpenTap.Display( "Sample Rate", Order=1))\
            .add_attribute(OpenTap.EnabledIf( "IsSet", True, HideIfDisabled=True)).add_attribute(OpenTap.Unit( "Hz"))
    
    def __init__(self):
        super(ADALMPlutoSampleRate,self).__init__()        
        
    def Run(self):
        if (self.IsSet):
            self.Inst.SampleRate(GetSet.Set,self.SR)
        else:
            v = self.Inst.SampleRate(GetSet.Get)
            print(v)
            super().OutputToDLS("SampleRate", ["Timestamp", "Sample Rate"], [float(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")) , v])
            
@attribute(OpenTap.Display(Name="Loop Back", Description="", Groups= ["DLS Python Plugin", "ADALMPluto"]))
class ADALMPlutoLoopBack(TestStep):
    Inst = property(ADALMPluto, None).add_attribute(OpenTap.Display( "ADALMPluto", Order=0))
    GetOrSet = property(GetSet, GetSet.Set).add_attribute(OpenTap.Display( "Get Or Set", Order=1))
    
    @property(Boolean)
    @attribute(Browsable(False))
    def IsSet(self):
        return self.GetOrSet == GetSet.Set
        
    LoopBack = property(PlutoLoopBack, PlutoLoopBack.Disabled).add_attribute(OpenTap.Display( "LoopBack", Order=1))\
            .add_attribute(OpenTap.EnabledIf( "IsSet", True, HideIfDisabled=True))
    
    def __init__(self):
        super(ADALMPlutoLoopBack,self).__init__()        
        
    def Run(self):
        if (self.IsSet):
            self.Inst.LoopBack(GetSet.Set,self.LoopBack)
        else:
            v = self.Inst.LoopBack(GetSet.Get)
            print(v)
            
@attribute(OpenTap.Display(Name="RX Buffer Size", Description="", Groups= ["DLS Python Plugin", "ADALMPluto"]))
class ADALMPlutoRXBufferSize(TestStep):
    Inst = property(ADALMPluto, None).add_attribute(OpenTap.Display( "ADALMPluto", Order=0))
    GetOrSet = property(GetSet, GetSet.Set).add_attribute(OpenTap.Display( "Get Or Set", Order=1))
    
    @property(Boolean)
    @attribute(Browsable(False))
    def IsSet(self):
        return self.GetOrSet == GetSet.Set
        
    Size = property(Int32, 10000).add_attribute(OpenTap.Display( "RX Buffer Size", Order=1))\
            .add_attribute(OpenTap.EnabledIf( "IsSet", True, HideIfDisabled=True))
    
    def __init__(self):
        super(ADALMPlutoRXBufferSize,self).__init__()        
        
    def Run(self):
        if (self.IsSet):
            self.Inst.RXBufferSize(GetSet.Set,self.Size)
        else:
            v = self.Inst.RXBufferSize(GetSet.Get)
            super().OutputToDLS("RXBufferSize", ["Timestamp", "Size"], [float(datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")) , v])
            
@attribute(OpenTap.Display(Name="Stop Transmitting", Description="", Groups= ["DLS Python Plugin", "ADALMPluto"]))
class ADALMPlutoStopTransmitting(TestStep):
    Inst = property(ADALMPluto, None).add_attribute(OpenTap.Display( "ADALMPluto", Order=0))

    def __init__(self):
        super(ADALMPlutoStopTransmitting,self).__init__()        
        
    def Run(self):
        self.Inst.StopTransmitting()