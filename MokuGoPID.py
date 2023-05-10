from opentap import *
import OpenTap
from enum import Enum
from OpenTap import Log
import System
from System import Array, Double, Byte, Int32, String, Boolean # Import types to reference for generic methods

from moku.instruments import PIDController

class PIDProbeMonitor(Enum):
    Input1 = 1
    Control1 = 2
    Output1 = 3
    Input2 = 4
    Control2 = 5
    Output2 = 6
    def __str__(self):
        return self.name
    
    
class PIDTriggerSource(Enum):
    ProbeA = 0
    ProbeB = 1
    def __str__(self):
        return self.name
    
class PIDEdgeTrigger(Enum):
    Rising = 0
    Falling = 1
    Both = 2
    def __str__(self):
        return self.name

@attribute(OpenTap.Display(Name="Moku Go PID", Description="", Groups= ["DLS Python Plugin"]))
class MokuGoPID(Instrument):
    IP = property(String, "10.74.65.215").add_attribute(OpenTap.Display( "IP"))
    def __init__(self):
        super(MokuGoPID,self).__init__()
        self.Name = "Moku Go PID"

    def Open(self):
        global i
        try:
          i = PIDController(self.IP, force_connect=True)
        except:
          print("Exception - cannot connect!")
          self.log.Error(self.Name + " Exception - cannot connect!")

    def Close(self):
        i.relinquish_ownership()
            
    def SetControlMatrix(self,ch=1,ig1db=1,ing2db=0):
        i.set_control_matrix(channel=ch,input_gain1=ig1db,input_gain2=ing2db)
        
    def SetByFrequency(self,ch=1,pgain=-10,icross=1e2,\
                       dcross=1e4, isaturation=10,\
                       dsaturation=10,dicross=31):
        i.set_by_frequency(channel=ch,prop_gain=pgain,int_crossover=icross,\
                       diff_crossover=dcross,double_int_crossover=dicross,\
                       int_saturation=isaturation,diff_saturation=dsaturation)
                       
    def SetByGain(self,ch=2,ogain=0,pgain=10,igain=40,dgain=-5,icorner=5,dcorner=5e3):
        i.set_by_gain(channel=ch,overall_gain=ogain,\
            prop_gain=pgain,int_gain=igain,\
            diff_gain=dgain,int_corner=icorner,\
            diff_corner=dcorner)
        
    def EnableOutput(self,ch=1,sig=True,out=True):
        i.enable_output(ch, signal=sig, output=out)
        
    def SetProbeMonitor(self,ch=1,source=1):
        i.set_monitor(ch, source.name)
         
    def SetEdgeTrigger(self,auto_sens=True,edg=PIDEdgeTrigger.Rising,hf_rej=False,\
                    hoff=0.0,triglevel=0,nreject=False,nth_eve=1,\
                    trigsource=PIDTriggerSource.ProbeA):
        i.set_trigger(type='Edge', source=trigsource.name, level=triglevel,\
                auto_sensitivity=auto_sens,edge=edg.name,\
                hf_reject=hf_rej,holdoff=hoff,noise_reject=nreject,nth_event=nth_eve)
        
    def GetData(self):
        return i.get_data()