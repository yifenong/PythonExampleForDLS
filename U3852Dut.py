
import clr
clr.AddReference("System.Collections")
from opentap import *

from OpenTap.Cli import *
import OpenTap
from enum import Enum
from OpenTap import Log
import System
from System import Array, Double, Byte, Int32, String, Boolean # Import types to reference for generic methods
import time
import serial
import re

class U3852Filter(Enum):
    Open = 200
    Short = 201
    Load = 202
    Thru = 203
    FL241 = 204
    FL251 = 205
    FL261 = 206
    LPF = 207
    def __str__(self):
        return self.name


class U3852Amplifier(Enum):
    Open = 300
    Short = 301
    Load = 302
    Thru = 303
    LNAU341 = 304
    GainBlkU351 = 305
    DriverU361 = 306
    Breadboard = 307
    def __str__(self):
        return self.name

class U3852Mixer(Enum):
    Open_RefOscU811_to_J683 = 600
    Short = 601
    Load = 602
    Thru = 603
    Z640_LO_input_to_J683 = 604
    Z650_LO_input_to_J683 = 605
    Z660_LO_input_to_J683 = 606
    Receiver_RefOscU511_to_J683 = 607
    def __str__(self):
        return self.name

@attribute(OpenTap.Display(Name="U3852", Description="", Groups= ["DLS Python Plugin"])) 
class U3852Dut(Dut):
    ComPort = property(Int32, 9).add_attribute(OpenTap.Display( "ComPort"))
    Baud = property(Int32, 9600).add_attribute(OpenTap.Display( "Baud"))
    def __init__(self):
        super(U3852Dut,self).__init__()
        self.Name = "U3852 Dut"

    def Open(self):
        try:
          global ser
          self.log.Info("Trying to connect to COM"+str(self.ComPort))
          ser = serial.Serial(port="COM"+str(self.ComPort), baudrate=self.Baud)
          serial_comm_established = True
          self.log.Info(self.Name + " Opened")
        except:
          print("Exception - cannot connect!")
          self.log.Error(self.Name + " Exception - cannot connect!")

    def Close(self):
        if(ser.isOpen()):
            ser.close()
        self.log.Info(self.Name + " Closed")

    def SetPath(self, path):
        send_data = b"rout:clos " + bytes(str(path.value)[0:3],'ascii') + b"\n"
        print(send_data)
        self.SendData(send_data)

    def SendData(self,send_data):
        """Called by TAP when the test plan starts."""
        ser.write(send_data)
        ser_in = str(ser.readline())
        ser_in = str(ser.readline())
        ser_in = str(ser.readline())
        ser_in = str(ser.readline())

    def Read(self,send_data):
        ser.write(send_data)
        ser_in = str(ser.readline())
        ser_in = str(ser.readline())
        result = re.findall(r"[-+]?\d*\.\d+|\d+", ser_in)
        ser_in = str(ser.readline())
        return str(result[0])