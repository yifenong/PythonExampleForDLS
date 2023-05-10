#instruction https://wiki.analog.com/university/tools/m2k/libm2k/libm2k#building_bindings
#install driver from https://github.com/analogdevicesinc/plutosdr-m2k-drivers-win/releases
#install python library from https://test.pypi.org/project/libm2k/#description

from opentap import *
import OpenTap
from enum import Enum
from OpenTap import Log
import System
from System import Array, Double, Byte, Int32, String, Boolean # Import types to reference for generic methods

import libm2k
#import matplotlib.pyplot as plt
import time

import numpy as np

class InputOutput(Enum):
    Input = 0
    Output = 1
    def __str__(self):
        return self.name

class SMethod(Enum):
    Samples = 0
    Duration = 1
    def __str__(self):
        return self.name
    
class Channel(Enum):
    AnalogIn = 0
    AnalogOut = 1
    PowerSupply = 2
    Digital = 3
    def __str__(self):
        return self.name
    
class ChannelEN(Enum):
    AnalogIn = 0
    AnalogOut = 1
    PowerSupply = 2
    Digital = 3
    def __str__(self):
        return self.name
    
class ChannelSR(Enum):
    AnalogIn = 0
    AnalogOut = 1
    DigitalIn = 2
    DigitalOut = 3
    def __str__(self):
        return self.name
        
@attribute(OpenTap.Display(Name="ADALM2000", Description="", Groups= ["DLS Python Plugin"]))
class ADALM2000Instrument(Instrument):

    def __init__(self):
        super(ADALM2000Instrument,self).__init__()
        self.Name = "ADALM2000"
        self.ctx = None
        self.ain = None
        self.aout = None
        self.trig = None
       
    def Open(self):
        try:
            self.ctx=libm2k.m2kOpen()
            if self.ctx is None:
                print("Connection Error: No ADALM2000 device available/connected to your PC.")
                self.log.Error("Connection Error: No ADALM2000 device available/connected to your PC.")
            else:
                self.ain=self.ctx.getAnalogIn()
                self.aout=self.ctx.getAnalogOut()
                self.trig=self.ain.getTrigger()
                self.ps=self.ctx.getPowerSupply()
                self.dig=ctx.getDigital()
        except:
            print("Exception - cannot connect!")
            self.log.Error(self.Name + " Exception - cannot connect!")

    def Close(self):
        libm2k.contextClose(self.ctx)

    def ResetAnalogIn(self):
        self.ain.reset()
        
    def ResetAnalogOut(self):
        self.aout.reset()
        
    def ResetPowerSupply(self):
        self.ps.reset()
        
    def ResetDigital(self):
        self.dig.reset()
        
    def CalibrateADC(self):
        self.ctx.calibrateADC()
        
    def CalibrateDAC(self):
        self.ctx.calibrateDAC()
        
    def EnableAnalogInputChannel(self,channel=0,enable=True):
        self.ain.enableChannel(channel,enable)
        
    def EnableAnalogOutputChannel(self,channel=0,enable=True):
        self.aout.enableChannel(channel,enable)
        
    def EnablePowerSupplyChannel(self,channel=0,enable=True):
        self.ps.enableChannel(channel,enable)
        
    def EnableDigitalChannel(self,channel=0,enable=True):
        self.dig.enableChannel(channel,enable)
        
    def SetPowerSupplyVoltage(self,channel=0,voltage=1.7):
        self.ps.pushChannel(channel,voltage)
        
    def GetVoltage(self,channel=0):
        return self.ain.getVoltage()[channel]
        
    def SetAnalogInputSampleRate(self,samplerate=100000):
        self.ain.setSampleRate(samplerate)
        
    def SetDigitalInputSampleRate(self,samplerate=100000):
        self.dig.setSampleRateIn(samplerate)
        
    def GetAnalogInputSampleRate(self):
        self.ain.getSampleRate()
        
    def SetRange(self,channel=0,mininmum=-10,maximum=10):
        self.ain.setRange(channel,mininmum,maximum)
        
    def SetAnalogOutputSampleRate(self,channel=0,samplerate=750000):
        self.aout.setSampleRate(channel,samplerate)
        
    def SetDigitalOutputSampleRate(self,samplerate=100000):
        self.dig.setSampleRateOut(samplerate)
        
    def GenerateBinaryCounter(self,nbits=3):
        buff=range(2**nbits)
        self.dig.setCyclic(True)
        self.dig.push(buff)
        
    def GetDigitalSamples(self,samples=100):
        return self.dig.getSamples(samples)

    def GenerateSineWave(self,vneg=-2.0,vpos=2.0,points=1024):
        x=np.linspace(-np.pi,np.pi,points)
        buffer1=np.linspace(vneg,vpos,points)
        buffer2=np.sin(x)
        buffer = [buffer1, buffer2]
        self.aout.setCyclic(True)
        self.aout.push(buffer)
        
    def GetAnalogInputSamples(self,samples=1000):
        return self.ain.getSamples(samples)

    def GetAnalogInputSamples1(self,duration=3):
        return self.ain.getSamples(duration*self.GetInputSampleRate())
        
    def SetDigitalDirectionOutput(self,channel=0):
        self.dig.setDirection(channel,libm2k.DIO_OUTPUT)
        
    def SetDigitalDirectionInput(self,channel=0):
        self.dig.setDirection(channel,libm2k.DIO_INPUT)