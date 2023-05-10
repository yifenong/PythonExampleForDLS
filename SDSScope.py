#reference: https://www.siglenteu.com/application-note/programming-example-sds-oscilloscope-screen-image-capture-using-python/?pdf=7470

from System import Double, String, Byte,Int32
from opentap import *
import OpenTap
from OpenTap import Log
import socket # for sockets
import sys # for exit
import time # for sleep

from enum import Enum

import pyvisa

import numpy as np

class SDSMeasurement(Enum):
    AMPL = 0
    BASE = 1
    CMEAN = 2
    CRMS = 3
    DUTY = 4
    FALL = 5
    FREQ = 6
    FPRE = 7
    MAX = 8
    MIN = 9
    MEAN = 10
    NDUTY = 11
    NWID = 12
    OVSN = 13
    OVSP = 14
    PKPK = 15
    PER = 16
    RPRE = 17
    PWID = 18
    RMS = 19
    RISE = 20
    TOP = 21
    WID = 22
    def __str__(self):
        return self.name

@attribute(OpenTap.Display(Name="SDSScope", Description="", Groups= ["DLS Python Plugin"])) 
class SDSScope(Instrument):
    VISAAdd = property(String, "USB0::0xF4ED::0xEE3A::SDS1EDED5R1177::0::INSTR").add_attribute(OpenTap.Display( "VISA Address",Order=0))
    IoTimeout = property(Int32, 10000).add_attribute(OpenTap.Display( "Time Out")).add_attribute(OpenTap.Unit( "ms"))
    def __init__(self):
        super(SDSScope,self).__init__()
        self.Name = "SDS Scope"
       
        self.rm = pyvisa.ResourceManager()
        self.osc = None
    
    def GetScreenshot(self):
        self.osc.write("SCDP")
        print("SCDP")
        return self.osc.read_raw()

    def Open(self):
        self.osc = self.rm.open_resource(self.VISAAdd)
        self.osc.timeout = int(self.IoTimeout)
        self.log.Info("Resource Opened")

    def Close(self):
        if (self.rm != None):
            self.rm.close()
            
    def GetMeasurement(self, channel = 1, meas = SDSMeasurement.PKPK):
        return self.osc.query('C'+str(channel)+':PAVA? '+meas.name)
    
    def Autoset(self):
        self.osc.write('AUTO_SETUP')
        return self.osc.query('*OPC?')
        
    def GetWaveform(self, channel):

        self.osc.write("CHDR SHORT")
        
        vDiv = float(self.osc.query('C{0}:VDIV?'.format(str(channel))).split(" ")[1][:-2])

        vOffset = float(self.osc.query('C{0}:OFST?'.format(str(channel))).split(" ")[1][:-2])

        tDiv = float(self.osc.query('TDIV?').split(" ")[1][:-2])

        tOffset = float(self.osc.query('TRDL?').split(" ")[1][:-2])

        self.osc.write("WFSU SP,0,NP,0,F,0")

        sample_rate = float(self.osc.query('SARA?').split(" ")[1].replace("Sa/s",''))
        time_interval = 1 / sample_rate
        
        #desc = device.write('C%d:WF? DESC' % channel)
        #logger.info(repr(device.read_raw()))

        # the response to this is binary data so we need to write() and then read_raw()
        # to avoid encode() call and relative UnicodeError
        self.osc.write('C{0}:WF? DAT2'.format(str(channel)))
        self.log.Info('C{0}:WF? DAT2'.format(str(channel)))
        
        response = self.osc.read_raw()

        index = response.index(b'#9')
        index_start_data = index + 2 + 9
        data_size = int(response[index + 2:index_start_data])
        # the reponse terminates with the sequence '\n\n\x00' so
        # is a bit longer that the header + data
        data = response[index_start_data:index_start_data + data_size]
        self.log.Info('data size: %d' % data_size)
        
        ndata = np.fromiter(data,dtype=np.double)
        #print(ndata)
        fdata = np.empty(len(ndata),dtype=np.double)
        
        for idx, x in enumerate(ndata):
            if (x > 127):
                fdata[idx] = x - 255
            else:
                fdata[idx] = x
                
        print(fdata)
        #np.savetxt('C:/Users/yifenong/Desktop/sdsdata.csv', fdata, delimiter=',')
        Volts = fdata * vDiv / 25 - vOffset
        Time = np.arange(tOffset-tDiv*14/2, tOffset-tDiv*14/2 + (time_interval * len(Volts)), time_interval)

        return Time,Volts
