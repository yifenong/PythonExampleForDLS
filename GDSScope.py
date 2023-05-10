#reference: https://www.siglenteu.com/application-note/programming-example-sds-oscilloscope-screen-image-capture-using-python/?pdf=7470

from System import Double, String, Byte,Int32
from opentap import *
import OpenTap
from OpenTap import Log
import socket # for sockets
import sys # for exit
import time # for sleep
from struct import unpack
import struct

from enum import Enum

import pyvisa

import numpy as np

class GDSMeasurement(Enum):
    FALL = 0
    FOVShoot = 1
    FPReshoot = 2
    FREQuency = 3
    NWIDth = 4
    PDUTy = 5
    PERiod = 6
    PWIDth = 7
    RISe = 8
    ROVShoot = 9
    RPReshoot = 10
    PPULSE = 11
    NPULSE = 12
    PEDGE = 13
    NEDGE = 14
    AMPlitude = 15
    MEAN = 16
    CMEan = 17
    HIGH = 18
    LOW = 19
    MAX = 20
    MIN = 21
    PK2PK = 22
    RMS = 23
    CRMS = 24
    AREA = 25
    CARea = 26
    def __str__(self):
        return self.name
        
class GDSMeasurement1(Enum):
    FRRDelay = 0
    FRFDelay = 1
    FFRDelay = 2
    FFFDelay = 3
    LRRDelay = 4
    LRFDelay = 5
    LFRDelay = 6
    LFFDelay = 7
    PHAse = 8
    def __str__(self):
        return self.name

@attribute(OpenTap.Display(Name="GDS Scope", Description="", Groups= ["DLS Python Plugin"])) 
class GDSScope(Instrument):
    VISAAdd = property(String, "ASRL10::INSTR").add_attribute(OpenTap.Display( "VISA Address",Order=0))
    IoTimeout = property(Int32, 10000).add_attribute(OpenTap.Display( "Time Out")).add_attribute(OpenTap.Unit( "ms"))
    def __init__(self):
        super(GDSScope,self).__init__()
        self.Name = "GDS Scope"
        self.rm = pyvisa.ResourceManager()
        self.osc = None
        self.headerlen = 0

    def Open(self):
        self.osc = self.rm.open_resource(self.VISAAdd)
        self.osc.timeout = int(self.IoTimeout)
        self.log.Info("Resource Opened")

    def Close(self):
        if (self.rm != None):
            self.rm.close()
            
    def GetMeasurement(self, source = 1, channel = 1, meas = GDSMeasurement.PK2PK):
        self.osc.write(":MEASure:SOURce"+source+" CH"+channel)
        return self.osc.query(":MEASure:"+meas.name+"?")
        
    def GetMeasurement1(self, channel1 = 1, channel2 = 2, meas1 = GDSMeasurement1.PHAse):
        self.osc.write(":MEASure:SOURce1 CH"+channel1)
        self.osc.write(":MEASure:SOURce2 CH"+channel2)
        return self.osc.query(":MEASure:"+meas1.name+"?")      
        
    def Autoset(self):
        self.osc.write(':AUTOSet')
        return self.osc.query('*OPC?')
        
    def GetRawData(self, ch): #Used to get waveform's raw data.
        global inBuffer
        self.osc.write(":HEAD ON")

        if(self.checkAcqState(ch)== -1):
            return
        self.osc.write(":ACQ%d:MEM?" % ch)                    #Write command(get raw datas) to DSO.

        info=self.osc.read_raw().decode('ascii').split(';')
        print(info)
        for i in info:
            if ("Source," in i):
                global source
                source=i.split(',')[1]
                print("Source:"+str(source))
            if ("Vertical Scale," in i):
                global verticalscale
                verticalscale=float(i.split(',')[1])
                print("Vertical Scale: "+str(verticalscale))
            if ("Vertical Position," in i):
                global verticalposition
                verticalposition=float(i.split(',')[1])
                print("Vertical Position: "+str(verticalposition))
            if ("Horizontal Scale," in i):
                global horizontalscale
                horizontalscale=float(i.split(',')[1])  
                print("Horizontal Scale: "+str(horizontalscale))
            if ("Horizontal Position," in i):
                global horizontalposition
                horizontalposition=float(i.split(',')[1]) 
                print("Horizontal Position: "+str(horizontalposition))                
            if ("Sampling Period," in i):
                global samplingperiod
                samplingperiod=float(i.split(',')[1])  
                print("Sampling Period: "+str(samplingperiod))                
            if ("Vertical Units," in i):
                global verticalunits
                verticalunits=i.split(',')[1]
                print("Vertical Units: "+str(verticalunits))                          

        self.GetBlockData()
        
        points_num=len(inBuffer[self.headerlen:-1])//2   #Calculate sample points length.
        print("Sample Points: "+str(points_num))
        iWave = unpack('>%sh' % points_num, inBuffer[self.headerlen:-1])
        #print(iWave)
        del inBuffer
        
        dv=verticalscale/25
        print("dv: "+str(dv))
        num=points_num
        fWave=[0]*num
        for x in range(num):           #Convert 16 bits signed to floating point number.
            fWave[x]=float(iWave[x])*dv
        t_start=horizontalposition-num*samplingperiod/2
        t_end  =horizontalposition+num*samplingperiod/2
        t = np.arange(t_start, t_end, samplingperiod)
        
        ndata = np.array(fWave)
        #np.savetxt('C:/Users/yifenong/Desktop/gdsdata.csv', ndata, delimiter=',')
        
        return t,ndata
        
    def GetBlockData(self): 
        global inBuffer
        inBuffer=self.osc.read_bytes(10)
        length=len(inBuffer)
        self.headerlen = 2 + int(inBuffer[1:2].decode())
        pkg_length = int(inBuffer[2:self.headerlen]) + self.headerlen + 1 #Block #48000[..8000bytes raw data...]<LF>
        print ("Data transferring...  ")

        pkg_length=pkg_length-length
        while True:
            print('%8d\r' %pkg_length),
            if(pkg_length==0):
                break
            else:
                if(pkg_length > 100000):
                    length=100000
                else:
                    length=pkg_length
                try:
                    buf=self.osc.read_bytes(length)
                except:
                    self.log.Error("Error Transferring data")
                num=len(buf)
                inBuffer+=buf
                pkg_length=pkg_length-num
                
    def checkAcqState(self,  ch):
        str_stat=":ACQ%d:STAT?" % ch
        loop_cnt = 0
        max_cnt=0
        while True:                                #Checking acquisition is ready or not.
            state=self.osc.query(str_stat)
            if(state[0] == '1'):
                break
            time.sleep(0.1)
            loop_cnt +=1
            if(loop_cnt >= 50):
                print('Please check signal!')
                loop_cnt=0
                max_cnt+=1
                if(max_cnt==5):
                    return -1
        return 0
        