from System.Collections.Generic import List
from opentap import *
import OpenTap

from OpenTap import TestStep

import numpy as np
from scipy import stats

from .DLSOutputInput import * 

@attribute(OpenTap.Display(Name="Numpy Sine Wave", Description="", Groups= ["DLS Python Plugin", "Numpy Step"]))
class NumpySineWave(DLSStep):
   #Points = property(System.Int32, 32).add_attribute(OpenTap.Display( "Points"))
    def __init__(self):
      super().__init__()
      
    def Run(self):
        F = 10
        Fs = 5000
        Ts = 1./Fs
        N = 1000
        t = np.linspace(0, N*Ts, N)
        Signal = np.sin(2*np.pi*F*t)
        noise = np.random.normal(0, .1, Signal.shape)
        Signal1 = Signal + noise
        super().OutputToDLS("Get Waveform Data", ["t","Data"], [t[:250], Signal1[:250]])
        
@attribute(OpenTap.Display(Name="Numpy Single Value", Description="", Groups= ["DLS Python Plugin", "Numpy Step"]))
class NumpySingleValue(DLSStep):
   #Points = property(System.Int32, 32).add_attribute(OpenTap.Display( "Points"))
    def __init__(self):
      super().__init__()
      
    def Run(self):
        Noise = np.random.normal(0, .1)
        super().OutputToDLS("Signal", ["Signal"], [Noise])
        
@attribute(OpenTap.Display(Name="Numpy Standard Deviation", Description="", Groups= ["DLS Python Plugin", "Numpy Step"]))
class NumpyStandardDeviation(DLSStep):
    ResultName = property(String, 'Get Measurement').add_attribute(OpenTap.Display( 'Result Name', Order=10))
    ColumnName = property(String, 'Data').add_attribute(OpenTap.Display( 'Column Name', Order=11))
    def __init__(self):
      super().__init__()
      
    def Run(self):
        SelectedData = super().GetStepData(self.ResultName,self.ColumnName)
        Data = np.fromiter(SelectedData,dtype=np.float)
        print(Data)
        print(np.std(Data))  
        
@attribute(OpenTap.Display(Name="Numpy Difference", Description="", Groups= ["DLS Python Plugin", "Numpy Step"]))
class NumpyDifference(DLSStep):
    ResultName1 = property(String, 'Get Measurement').add_attribute(OpenTap.Display( 'Result Name 1', Order=10))
    ColumnName1 = property(String, 'Data').add_attribute(OpenTap.Display( 'Column Name 1', Order=11))
    ResultName2 = property(String, 'Get Measurement (1)').add_attribute(OpenTap.Display( 'Result Name 2', Order=12))
    ColumnName2 = property(String, 'Data').add_attribute(OpenTap.Display( 'Column Name 2', Order=13))
    def __init__(self):
      super().__init__()
      
    def Run(self):
        [SelectedData1,SelectedData2] = super().GetStepData1(self.ResultName1,self.ColumnName1,self.ResultName2,self.ColumnName2)
        Data1 = np.fromiter(SelectedData1,dtype=np.float)
        Data2 = np.fromiter(SelectedData2,dtype=np.float)
        super().OutputToDLS('ScipyTTest',['Data2-Data1'],[Data2-Data1])
        
@attribute(OpenTap.Display(Name="Scipy T Test", Description="", Groups= ["DLS Python Plugin", "Scipy Step"]))
class ScipyTTest(DLSStep):
    ResultName1 = property(String, 'Get Measurement').add_attribute(OpenTap.Display( 'Result Name 1', Order=10))
    ColumnName1 = property(String, 'Data').add_attribute(OpenTap.Display( 'Column Name 1', Order=11))
    ResultName2 = property(String, 'Get Measurement (1)').add_attribute(OpenTap.Display( 'Result Name 2', Order=12))
    ColumnName2 = property(String, 'Data').add_attribute(OpenTap.Display( 'Column Name 2', Order=13))
    def __init__(self):
      super().__init__()
      
    def Run(self):
        [SelectedData1,SelectedData2] = super().GetStepData1(self.ResultName1,self.ColumnName1,self.ResultName2,self.ColumnName2)
        Data1 = np.fromiter(SelectedData1,dtype=np.float)
        Data2 = np.fromiter(SelectedData2,dtype=np.float)
        Statistic = stats.ttest_ind(Data1,Data2).statistic
        PValue = stats.ttest_ind(Data1,Data2).pvalue
        print(stats.ttest_ind(Data1,Data2))    
        super().OutputToDLS('ScipyTTest',['statistic','pvalue'],[Statistic,PValue])

        
