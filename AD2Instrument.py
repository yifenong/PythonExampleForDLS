from opentap import *
import OpenTap
from enum import Enum
from OpenTap import Log
import System
from System import Array, Double, Byte, Int32, String, Boolean # Import types to reference for generic methods

from ctypes import *
from .dwfconstants import *
import math
import time
#import matplotlib.pyplot as plt
import sys
import numpy

class AD2Function(Enum):
    funcDC       = 0
    funcSine     = 1
    funcSquare   = 2
    funcTriangle = 3
    funcRampUp   = 4
    funcRampDown = 5
    funcNoise    = 6
    funcPulse    = 7
    funcTrapezium= 8
    funcSinePower= 9
    funcCustom   = 30
    funcPlay     = 31
    def __str__(self):
        return self.name
    
class AD2PowerMonitor(Enum):
    USBVoltage = 0
    USBCurrent = 1
    AUXVoltage = 2
    AUXCurrent = 3
    def __str__(self):
        return self.name
    
class AD2TriggerSource(Enum):
    trigsrcNone                 = 0
    trigsrcPC                   = 1
    trigsrcDetectorAnalogIn     = 2
    trigsrcDetectorDigitalIn    = 3
    trigsrcAnalogIn             = 4
    trigsrcDigitalIn            = 5
    trigsrcDigitalOut           = 6
    trigsrcAnalogOut1           = 7
    trigsrcAnalogOut2           = 8
    trigsrcAnalogOut3           = 9
    trigsrcAnalogOut4           = 10
    trigsrcExternal1            = 11
    trigsrcExternal2            = 12
    trigsrcExternal3            = 13
    trigsrcExternal4            = 14
    trigsrcHigh                 = 15
    trigsrcLow                  = 16
    trigsrcClock                = 17
    def __str__(self):
        return self.name

@attribute(OpenTap.Display(Name="Analog Discovery 2", Description="", Groups= ["DLS Python Plugin"]))
class AD2Instrument(Instrument):

    def __init__(self):
        super(AD2Instrument,self).__init__()
        self.Name = "Analog Discovery 2"
        if sys.platform.startswith("win"):
         self.dwf = cdll.dwf
        elif sys.platform.startswith("darwin"):
         self.dwf = cdll.LoadLibrary("/Library/Frameworks/dwf.framework/dwf")
        else:
         self.dwf = cdll.LoadLibrary("libdwf.so")
        self.hdwf = c_int()
        self.sts = c_byte()

    def Open(self):
        try:
          self.log.Info("Trying to connect to ")
          self.dwf.FDwfDeviceOpen(c_int(-1), byref(self.hdwf))
          if self.hdwf.value == hdwfNone.value:
           szerr = create_string_buffer(512)
           self.dwf.FDwfGetLastErrorMsg(szerr)
           print(str(szerr.value))
           self.log.Error("failed to open device")
          self.log.Info(self.Name + " Opened")
        except:
          print("Exception - cannot connect!")
          self.log.Error(self.Name + " Exception - cannot connect!")

    def Close(self):
        self.dwf.FDwfAnalogOutReset(self.hdwf, c_int(-1))
        self.dwf.FDwfAnalogInReset(self.hdwf, c_int(-1))
        self.dwf.FDwfDigitalIOReset(self.hdwf, c_int(-1))
        self.dwf.FDwfDeviceCloseAll()

    def GenerateSineWave(self,channel=0,freq=1,ampl=2):
        self.dwf.FDwfAnalogOutNodeEnableSet(self.hdwf, c_int(channel), AnalogOutNodeCarrier, c_bool(True))
        self.dwf.FDwfAnalogOutNodeFunctionSet(self.hdwf, c_int(channel), AnalogOutNodeCarrier, funcSine)
        self.dwf.FDwfAnalogOutNodeFrequencySet(self.hdwf, c_int(channel), AnalogOutNodeCarrier, c_double(freq))
        self.dwf.FDwfAnalogOutNodeAmplitudeSet(self.hdwf, c_int(channel), AnalogOutNodeCarrier, c_double(ampl))
        self.dwf.FDwfAnalogOutConfigure(self.hdwf, c_int(channel), c_bool(True))
        
    def AnalogOutEnableSet(self,channel=0,enable=True):
        self.dwf.FDwfAnalogOutNodeEnableSet(self.hdwf, c_int(channel), AnalogOutNodeCarrier, c_bool(enable))

    def AnalogOutFunctionSet(self,channel=0,func=funcSine):
        self.dwf.FDwfAnalogOutNodeFunctionSet(self.hdwf, c_int(channel), AnalogOutNodeCarrier, c_ubyte(func.value))

    def AnalogOutFrequencySet(self,channel=0,freq=1):
        self.dwf.FDwfAnalogOutNodeFrequencySet(self.hdwf, c_int(channel), AnalogOutNodeCarrier, c_double(freq))
        
    def AnalogOutAmplitudeSet(self,channel=0,ampl=2):
        self.dwf.FDwfAnalogOutNodeAmplitudeSet(self.hdwf, c_int(channel), AnalogOutNodeCarrier, c_double(ampl))

    def AnalogOutOffsetVoltage(self,channel=0,offset=0):
        self.dwf.FDwfAnalogOutNodeOffsetSet(self.hdwf, c_int(channel), AnalogOutNodeCarrier, c_double(offset))
    
    def AnalogOutSymmetry(self,channel=0,sympercent=50):
        self.dwf.FDwfAnalogOutNodeSymmetrySet(self.hdwf, c_int(channel), AnalogOutNodeCarrier, c_double(sympercent))

    def AnalogOutPhase(self,channel=0,phase=0):
        self.dwf.FDwfAnalogOutNodePhaseSet(self.hdwf, c_int(channel), AnalogOutNodeCarrier, c_double(phase))


    def AnalogOutConfigure(self,channel=0,enable=True):
        self.dwf.FDwfAnalogOutConfigure(self.hdwf, c_int(channel), c_bool(enable))
        
    def AnalogInEnableSet(self,channel=0,enable=True):
        self.dwf.FDwfAnalogInChannelEnableSet(hdwf, c_int(channel), c_bool(enable)) 
        
    def AnalogInOffsetVoltage(self,channel=0,offset=0):
        self.dwf.FDwfAnalogInChannelOffsetSet(hdwf, c_int(channel), c_double(offset)) 
        
    def AnalogInRangeVoltage(self,channel=0,rang=5):
        self.dwf.FDwfAnalogInChannelRangeSet(hdwf, c_int(channel), c_double(rang)) 
        
    def AnalogInConfigure(self,reconfigure=False,start=True):
        self.dwf.FDwfAnalogInConfigure(hdwf, c_bool(reconfigure), c_bool(start)) 
        
    def GetADCSample(self,channel=0):
        voltage = c_double()
        dwf.FDwfAnalogInStatusSample(hdwf, c_int(0), byref(voltage))
        return voltage.value
        
    def AcquireSamples(self,channel=0,samples=1024):
        rgdSamples1 = (c_double*cSamples)()
        dwf.FDwfAnalogInStatusData(hdwf, c_int(channel), rgdSamples1, len(rgdSamples1))
        return rgdSamples1
        
    def SetAnalogOutRunlength(self,channel=0,lengthseconds=5e-3):  
        dwf.FDwfAnalogOutRunSet(hdwf, c_int(channel), c_double(lengthseconds))
        
    def SetAnalogOutRepeat(self,channel=0,count=1):   
        dwf.FDwfAnalogOutRepeatSet(hdwf, c_int(channel), c_int(count))

    def SetAnalogInBufferSize(self,size=1024):          
        dwf.FDwfAnalogInBufferSizeSet(hdwf, c_int(size))

    def SetAnalogInTriggerSource(self,trigsource): 
        dwf.FDwfAnalogInTriggerSourceSet(hdwf, c_ubyte(trigsource.value)) 

    def SetAnalogInTriggerPosition(self,trigposseconds=0.3):
        dwf.FDwfAnalogInTriggerPositionSet(hdwf, c_double(trigposseconds)) 


    def EnablePositiveSupply(self,enable=True):
        self.dwf.FDwfAnalogIOChannelNodeSet(self.hdwf, c_int(0), c_int(0), c_double(enable)) 
        
    def SetPositiveSupply(self,volt=5.0):
        self.dwf.FDwfAnalogIOChannelNodeSet(self.hdwf, c_int(0), c_int(1), c_double(volt)) 
        
    def EnableNegativeSupply(self,enable=True):
        self.dwf.FDwfAnalogIOChannelNodeSet(self.hdwf, c_int(1), c_int(0), c_double(enable)) 
        
    def SetNegativeSupply(self,volt=-5.0):
        self.dwf.FDwfAnalogIOChannelNodeSet(self.hdwf, c_int(1), c_int(1), c_double(volt)) 
        
    def EnableAnalogIO(self,enable=True):
        self.dwf.FDwfAnalogIOEnableSet(self.hdwf, c_int(enable))
        
    def MonitorPower(self,monitor):
        usbVoltage = c_double()
        usbCurrent = c_double()
        auxVoltage = c_double()
        auxCurrent = c_double()
        if (monitor.name == USBVoltage):
            self.dwf.FDwfAnalogIOChannelNodeStatus(hdwf, c_int(2), c_int(0), byref(usbVoltage))
            return usbVoltage.value
        elif (monitor.name == USBCurrent):
            self.dwf.FDwfAnalogIOChannelNodeStatus(hdwf, c_int(2), c_int(1), byref(usbCurrent))
            return usbCurrent.value
        elif (monitor.name == AUXVoltage):
            self.dwf.FDwfAnalogIOChannelNodeStatus(hdwf, c_int(3), c_int(0), byref(auxVoltage))
            return auxVoltage.value
        elif (monitor.name == AUXCurrent):
            self.dwf.FDwfAnalogIOChannelNodeStatus(hdwf, c_int(3), c_int(1), byref(auxCurrent))  
            return auxCurrent.value            

    def RecordSamples(self,channel=0,acq=100000,samples=200000,voltrange=5):
        hzAcq = c_double(acq)
        nSamples = samples
        rgdSamples = (c_double*nSamples)()
        cAvailable = c_int()
        cLost = c_int()
        cCorrupted = c_int()
        fLost = 0
        fCorrupted = 0
        self.dwf.FDwfAnalogInChannelEnableSet(self.hdwf, c_int(channel), c_bool(True))
        self.dwf.FDwfAnalogInChannelRangeSet(self.hdwf, c_int(channel), c_double(voltrange))
        self.dwf.FDwfAnalogInAcquisitionModeSet(self.hdwf, acqmodeRecord)
        self.dwf.FDwfAnalogInFrequencySet(self.hdwf, hzAcq)
        self.dwf.FDwfAnalogInRecordLengthSet(self.hdwf, c_double(nSamples/hzAcq.value)) # -1 infinite record length
        #wait at least 2 seconds for the offset to stabilize
        time.sleep(2)
        print("Starting oscilloscope")
        self.dwf.FDwfAnalogInConfigure(self.hdwf, c_int(0), c_int(1))
        
        cSamples = 0

        while cSamples < nSamples:
            self.dwf.FDwfAnalogInStatus(self.hdwf, c_int(1), byref(self.sts))
            if cSamples == 0 and (self.sts == DwfStateConfig or self.sts == DwfStatePrefill or self.sts == DwfStateArmed) :
                # Acquisition not yet started.
                continue

            self.dwf.FDwfAnalogInStatusRecord(self.hdwf, byref(cAvailable), byref(cLost), byref(cCorrupted))
            
            cSamples += cLost.value

            if cLost.value :
                fLost = 1
            if cCorrupted.value :
                fCorrupted = 1

            if cAvailable.value==0 :
                continue

            if cSamples+cAvailable.value > nSamples :
                cAvailable = c_int(nSamples-cSamples)
            
            self.dwf.FDwfAnalogInStatusData(self.hdwf, c_int(0), byref(rgdSamples, sizeof(c_double)*cSamples), cAvailable) # get channel 1 data
            #dwf.FDwfAnalogInStatusData(hdwf, c_int(1), byref(rgdSamples, sizeof(c_double)*cSamples), cAvailable) # get channel 2 data
            cSamples += cAvailable.value
            
        if fLost:
            print("Samples were lost! Reduce frequency")
            self.log.Error("Samples were lost! Reduce frequency")
        if fCorrupted:
            print("Samples could be corrupted! Reduce frequency")
            self.log.Error("Samples could be corrupted! Reduce frequency")
        
        return rgdSamples