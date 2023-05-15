from System.Collections.Generic import List
from opentap import *
import OpenTap

from OpenTap import TestStep

import numpy as np
from scipy import stats

from .DLSOutputInput import * 

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
        super().OutputToDLS('NumpyDifference',['Data2-Data1'],[Data2-Data1])
        
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

        
