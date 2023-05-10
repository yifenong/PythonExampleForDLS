
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

class U3851OutputName(Enum):
    vout1 = 0
    vout2 = 1
    gpio0 = 2
    gpio1 = 3
    gpio2 = 4
    gpio3 = 5
    gpio4 = 6
    gpio5 = 7
    gpio6 = 8
    gpio7 = 9
    def __str__(self):
        return self.name
    
class U3851MeasurementName(Enum):
    vout1 = 0
    vout2 = 1
    iout1 = 2
    iout2 = 3
    iout3 = 4
    vaux1 = 5
    vaux2 = 6
    vina3 = 7
    vina4 = 8
    gpio0 = 9
    gpio1 = 10
    gpio2 = 11
    gpio3 = 12
    gpio4 = 13
    gpio5 = 14
    gpio6 = 15
    gpio7 = 16
    def __str__(self):
        return self.name


@attribute(OpenTap.Display(Name="U3851", Description="", Groups= ["DLS Python Plugin"])) 
class U3851Dut(Dut):
    ComPort = property(Int32, 9).add_attribute(OpenTap.Display( "ComPort"))
    Baud = property(Int32, 9600).add_attribute(OpenTap.Display( "Baud"))
    def __init__(self):
        super(U3851Dut,self).__init__()
        self.Name = "U3851 Dut"

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
        """Called by TAP when the test plan ends."""
        if(ser.isOpen()):
            ser.close()
        self.log.Info(self.Name + " Closed")

    def Output(self,output,data):
        send_data = b"sour:"+ bytes(str(output.name)+" "+str(data),'ascii') + b"\n"
        self.log.Info(str(send_data))
        self.Write(send_data)

    def Measure(self,meas):
        send_data = b"meas:"+bytes(str(meas.name),'ascii') + b"?\n"
        self.log.Info(str(send_data))
        return self.Read(send_data)

    def Write(self,send_data):
        """Called by TAP when the test plan starts."""
        ser.write(send_data)
        ser_in = str(ser.readline())
        ser_in = str(ser.readline())
        ser_in = str(ser.readline())
        ser_in = str(ser.readline())

    def Read(self,send_data):
        """Called by TAP when the test plan starts."""
        ser.write(send_data)
        ser_in = str(ser.readline())
        ser_in = str(ser.readline())
        ser_in = str(ser.readline())
        result = re.findall(r"[-+]?\d*\.\d+|\d+", ser_in)
        ser_in = str(ser.readline())
        print(ser_in)
        return str(result[0])