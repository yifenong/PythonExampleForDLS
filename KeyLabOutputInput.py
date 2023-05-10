from opentap import *
import OpenTap
from OpenTap import Display, Output, Input, ParameterMemberData, EnabledIfAttribute
from OpenTap.Plugins.BasicSteps import SweepRowCollection
from System import Double, String, Array, Int32
from System.Collections.Generic import List, IList
from System.ComponentModel import Browsable
from System.Reflection import PropertyInfo

import numpy as np
from System.Runtime.InteropServices import GCHandle, GCHandleType
import ctypes
import inspect

import collections.abc

from datetime import datetime

map_np_to_net = {
   np.dtype(np.float32): System.Single,
   np.dtype(np.float64): System.Double,
   np.dtype(np.int8)   : System.SByte,
   np.dtype(np.int16)  : System.Int16,
   np.dtype(np.int32)  : System.Int32,
   np.dtype(np.int64)  : System.Int64,
   np.dtype(np.uint8)  : System.Byte,
   np.dtype(np.uint16) : System.UInt16,
   np.dtype(np.uint32) : System.UInt32,
   np.dtype(np.uint64) : System.UInt64,
   np.dtype(np.bool)   : System.Boolean,
}

def toNetArrayFast(npArray):
   dims = npArray.shape
   dtype = npArray.dtype

   if not npArray.flags.c_contiguous or not npArray.flags.aligned:
      npArray = np.ascontiguousarray(npArray)
   try:
      netArray = Array.CreateInstance(map_np_to_net[dtype], *dims)
   except KeyError:
      raise NotImplementedError(f'asNetArray does not yet support dtype {dtype}')

   try:
      destHandle = GCHandle.Alloc(netArray, GCHandleType.Pinned)
      sourcePtr = npArray.__array_interface__['data'][0]
      destPtr = destHandle.AddrOfPinnedObject().ToInt64()
      ctypes.memmove(destPtr, sourcePtr, npArray.nbytes)
   finally:
      if destHandle.IsAllocated:
         destHandle.Free()
   return netArray
   
@attribute(Display("DLS Step", "An example of exposing the properties for DLS to process", "DLS Python Plugin"))
class DLSStep(TestStep):
    InputTestStep = property(OpenTap.TestStep, None).add_attribute(Display("Input Test Step"))
    ColumnNamesList = property(List[List[String]], None).add_attribute(Browsable(False))
    ResultNamesList = property(List[String], None).add_attribute(Browsable(False))
    DataList = property(List[List[Array]], None).add_attribute(Browsable(False))
    AppendIterationInfo = property(bool, False).add_attribute(OpenTap.Display( "Append IterationInfo To ResultName", Order=10))
    IterationLoopOnwards = property(Int32,0).add_attribute(OpenTap.EnabledIf("AppendIterationInfo",True, HideIfDisabled = True))\
    .add_attribute(OpenTap.Display( "From Loop# Onwards", "0 = The most immediate loop of this test step", Order=11))
    StepNameAsResultName = property(bool, False).add_attribute(OpenTap.Display( "Use StepName As ResultName", Order=9))

    def __init__(self):
        super().__init__()
        
    def Run(self):
        pass
        
    def OutputToDLS(self,ResultName,ColumnNames,Data,IsByte=False):
        if (self.StepNameAsResultName == True):
            ResultName = self.Name
        self.ResultNamesList = List[String]()
        self.DataList = List[List[Array]]()
        self.ColumnNamesList = List[List[String]]()
        ColumnNamesTemp = List[String](len(ColumnNames))
        for i in range(len(ColumnNames)):
            ColumnNamesTemp.Add(String(ColumnNames[i]))

        SingleValues = False

        DataTemp = List[Array](len(Data))
        DataTempSingle = List[String](len(Data))
        for i in range(len(Data)):
            if (IsByte == True):
                tempdata = np.fromiter(Data[i],dtype=np.ubyte)
            else:
                tempdata = np.array(Data[i])
            if (tempdata.size == 1):
                SingleValues = True
                break
            if (tempdata.dtype.type is np.str_):
                temp = List[String](tempdata.size)
                for j in range(tempdata.size - 1):
                    temp.Add(String(tempdata[j]))
                DataTemp.Add(temp.ToArray())
            else:
                DataTemp.Add(toNetArrayFast(tempdata))
            
        if (SingleValues == True):
            for i in range(len(Data)):
                DataTempSingle.Add(str(Data[i]))
               
        if (DataTempSingle.Count > 0):
            IterationInfo = self.GetIterationFromParent(self,self.IterationLoopOnwards)
            ResultNameWithIteration = str(ResultName) + str(IterationInfo)
            now = datetime.utcnow()
            ColumnNamesTemp.Add('Timestamp')
            ColumnNamesTemp.Add('IterationInfo')
            DataTempSingle.Add(now.strftime('%Y%m%d%H%M%S%f')[:-3])
            DataTempSingle.Add(IterationInfo)
            self.Results.Publish(ResultNameWithIteration,ColumnNamesTemp,DataTempSingle.ToArray())
            
            DataSingleTemp = List[Array](DataTempSingle.Count)
            for i in range(len(DataTempSingle)):
                datapointtemp = List[String](1)
                datapointtemp.Add(String(DataTempSingle[i]))
                DataSingleTemp.Add(datapointtemp.ToArray())
            self.DataList.Add(DataSingleTemp)    
            
            self.ResultNamesList.Add(String(ResultNameWithIteration))
            self.ColumnNamesList.Add(ColumnNamesTemp)
            self.UpdateSequenceWithOutputs(self,String(ResultNameWithIteration),ColumnNamesTemp,DataSingleTemp)
        
        if (DataTemp.Count > 0):
            IterationInfo = self.GetIterationFromParent(self,self.IterationLoopOnwards)
            ResultNameWithIteration = str(ResultName) + str(IterationInfo)
            self.Results.PublishTable(ResultNameWithIteration,ColumnNamesTemp,DataTemp.ToArray())
            self.DataList.Add(DataTemp) 
        
            self.ResultNamesList.Add(String(ResultNameWithIteration))
            self.ColumnNamesList.Add(ColumnNamesTemp)
            self.UpdateSequenceWithOutputs(self,String(ResultNameWithIteration),ColumnNamesTemp,DataTemp)            

    def UpdateSequenceWithOutputs(self,step,ResultName, ColumnNames, DataArray):
        ParentStep = step.get_Parent()
        for x in range(10):
            if (ParentStep == None):
                break

            if (str(ParentStep.GetType().Name) == 'SequenceWithOutputs'):
                
                resnamesinfo = ParentStep.GetType().GetProperty('ResultNamesList')
                resnames = List[String](resnamesinfo.GetValue(ParentStep, None))
                resnames.Add(ResultName);
                resnamesinfo.SetValue(ParentStep,resnames,None)
                
                colnamesinfo = ParentStep.GetType().GetProperty('ColumnNamesList');
                colnames = List[List[String]](colnamesinfo.GetValue(ParentStep, None))
                colnames.Add(ColumnNames);
                colnamesinfo.SetValue(ParentStep, colnames, None)
                
                datainfo = ParentStep.GetType().GetProperty('DataList');
                data = List[List[Array]](datainfo.GetValue(ParentStep, None))
                data.Add(DataArray)
                datainfo.SetValue(ParentStep, data, None)
                
                break
            else:
                ParentStep = ParentStep.get_Parent()

    def GetIterationFromParent(self, step, iterationonwards = 0, sweeponly= False):
        IterationInfoFromParent = List[String]()
        ParentStep1 = step.get_Parent()
        for x in range(10):
            if (self.AppendIterationInfo == False):
                break
            if (ParentStep1 == None):
                break
            if (x < iterationonwards):
                ParentStep1 = ParentStep1.get_Parent()
                continue
            if (str(ParentStep1.GetType().Name).__contains__('Repeat') or str(ParentStep1.GetType().Name).__contains__('Sweep')):
                if (sweeponly == True and str(ParentStep1.GetType().Name).__contains__('Repeat')):
                    continue
                props = List[PropertyInfo](ParentStep1.GetType().GetProperties())
                sweepcollection = None
                selectedparams = List[ParameterMemberData]();
                iterationinfoprop = "";
                for prop in props:
                    if (prop.Name == "SelectedParameters"):
                        selectedparams = IList[ParameterMemberData](prop.GetValue(ParentStep1, None))

                    if (prop.Name == "SweepValues"):
                        sweepcollection = prop.GetValue(ParentStep1, None)

                    if (prop.Name == "IterationInfo"):
                        iterationinfoprop = String(prop.GetValue(ParentStep1, None))

                    if (str(ParentStep1.GetType().Name).__contains__('Sweep') and sweepcollection is not None and selectedparams.Count > 0
                        and iterationinfoprop != ""):
                        propValue1 = str(iterationinfoprop).split(' ')[0];

                        sweepinfo = "";
                        for item in selectedparams:
                            sweepinfo += item.Name + ":" + str(sweepcollection[int(propValue1) - 1].Values[item.Name]) + "_"
                        sweepinfo = sweepinfo.rstrip(sweepinfo[-1]).replace("Parameters \ ","")

                        IterationInfoFromParent.Add(sweepinfo);

                        iterationinfoprop = "";
                    elif (str(ParentStep1.GetType().Name).__contains__('Repeat') and iterationinfoprop != ""):
                        IterationInfoFromParent.Add(iterationinfoprop);

                        iterationinfoprop = "";
            ParentStep1 = ParentStep1.get_Parent()
    
        IterationInfoFromParent.Reverse()

        info = ""
        for item in IterationInfoFromParent:
            info += "_" + item
        
        return info;
                
    def GetStepData(self,SelectedResultName='',SelectedColumnName=''):

        self.ColumnNamesList = List[List[String]]()
        self.ResultNamesList = List[String]()
        self.DataList = List[List[Array]]()
        
        resnamesinfo = self.InputTestStep.GetType().GetProperty('ResultNamesList')
        self.ResultNamesList = List[String](resnamesinfo.GetValue(self.InputTestStep, None))
        colnamesinfo = self.InputTestStep.GetType().GetProperty('ColumnNamesList');
        self.ColumnNamesList = List[List[String]](colnamesinfo.GetValue(self.InputTestStep, None))
        datainfo = self.InputTestStep.GetType().GetProperty('DataList');
        self.DataList = List[List[Array]](datainfo.GetValue(self.InputTestStep, None))

        for i in range(len(self.ResultNamesList)):
            if (self.ResultNamesList[i] == SelectedResultName):
                for j in range(len(self.ColumnNamesList[i])):
                    if (self.ColumnNamesList[i][j] ==  SelectedColumnName):
                        return self.DataList[i][j]
                        
    def GetStepData1(self,SelectedResultName1='',SelectedColumnName1='',SelectedResultName2='',SelectedColumnName2=''):

        self.ColumnNamesList = List[List[String]]()
        self.ResultNamesList = List[String]()
        self.DataList = List[List[Array]]()
        
        resnamesinfo = self.InputTestStep.GetType().GetProperty('ResultNamesList')
        self.ResultNamesList = List[String](resnamesinfo.GetValue(self.InputTestStep, None))
        colnamesinfo = self.InputTestStep.GetType().GetProperty('ColumnNamesList');
        self.ColumnNamesList = List[List[String]](colnamesinfo.GetValue(self.InputTestStep, None))
        datainfo = self.InputTestStep.GetType().GetProperty('DataList');
        self.DataList = List[List[Array]](datainfo.GetValue(self.InputTestStep, None))
        
        Data1 = None
        Data2 = None
        for i in range(len(self.ResultNamesList)):
            if (self.ResultNamesList[i] == SelectedResultName1):
                for j in range(len(self.ColumnNamesList[i])):
                    if (self.ColumnNamesList[i][j] ==  SelectedColumnName1):
                        Data1 = self.DataList[i][j]
                        
        for i in range(len(self.ResultNamesList)):
            if (self.ResultNamesList[i] == SelectedResultName2):
                for j in range(len(self.ColumnNamesList[i])):
                    if (self.ColumnNamesList[i][j] ==  SelectedColumnName2):
                        Data2 = self.DataList[i][j]
                        
        return [Data1,Data2]
        
