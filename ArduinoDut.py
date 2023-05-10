from opentap import *
import OpenTap
from enum import Enum
from OpenTap import Log
import System
from System import Array, Double, Byte, Int32, String, Boolean # Import types to reference for generic methods
import time
import serial

@attribute(OpenTap.Display(Name="Arduino Uno", Description="", Groups= ["DLS Python Plugin"]))
class ArduinoDut(Dut):
    ComPort = property( Int32, 9).add_attribute(OpenTap.Display( "ComPort"))
    Timeout = property(Double, 0.1).add_attribute(OpenTap.Display( "Timeout"))
    Baud = property(Int32, 9600).add_attribute(OpenTap.Display( "Baud"))
    def __init__(self):
        super(ArduinoDut,self).__init__()
        self.Name = "Arduino Uno"
       

    def Open(self):
        try:
          global ser
          self.log.Info("Trying to connect to COM"+str(self.ComPort))
          ser = serial.Serial(port="COM"+str(self.ComPort), baudrate=self.Baud)
          serial_comm_established = True
          ser.timeout = self.Timeout
          self.log.Info(self.Name + " Opened")
        except:
          print("Exception - cannot connect!")
          self.log.Error(self.Name + " Exception - cannot connect!")

    def Close(self):
        """Called by TAP when the test plan ends."""
        if(ser.isOpen()):
            ser.close()
        self.log.Info(self.Name + " Closed")
        #self.HighPowerOn = False

    def ReadSineWave(self):
        ser.write(b"0")
        data = ser.readline().decode('ascii')
        return data.rstrip(",")

    def ReadVoltage(self):
        ser.write(b"1")
        data = ser.readline().decode('ascii')
        return data

    def BlinkLED(self):
        ser.write(b"2")