import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui

from easygui import fileopenbox
import platform
import xml.etree.ElementTree as ET
import functools
import json
import pandas as pd

from MainWindow import Ui_MainWindow_NMR

class TableModelData():
    

    def __init__(self):
        self.model = QtGui.QStandardItemModel(0,6)
        self.model.setHorizontalHeaderLabels(('Sample Name','T1 Value','T2 Value','Liquid Mass','Particle Mass', 'Position'))
        
        self.numberOfConcentrations = 0
        self.groupedT1 = list()
        self.groupedT2 = list()

    def getGroupedT1(self):
        return self.groupedT1
    def getGroupedT2(self):
        return self.groupedT2
    def getNumOfConcentrations(self):
        return self.numberOfConcentrations

    def DelRows(self, selectedRowsDEL):
        
        selectedRowsDEL.sort(reverse = True)

        for i in selectedRowsDEL:
            if(i >= 1 or i <= self.model.rowCount()):
                self.model.removeRow(i-1)
                
                j = (i-1)*3
                self.groupedT1[j].pop()
                self.groupedT1[j+1].pop()
                self.groupedT1[j+2].pop()

                self.groupedT2[j].pop()
                self.groupedT2[j+1].pop()
                self.groupedT2[j+2].pop()

                self.numberOfConcentrations -= 1
            

    def RemoveAllRows(self):
        self.groupedT1 = list()
        self.groupedT2 = list()
        self.numberOfConcentrations = 0
        for row in range(self.model.rowCount()):
            self.model.removeRow(0)

    def AddRows(self, num, group1, group2, sheet_name):
        
        
        i=0
        
        for row in range(self.model.rowCount(), self.model.rowCount() + num):
            
            self.groupedT1.append(group1[i])
            self.groupedT1.append(group1[i+1])
            self.groupedT1.append(group1[i+2])

            self.groupedT2.append(group2[i])
            self.groupedT2.append(group2[i+1])
            self.groupedT2.append(group2[i+2])

            self.numberOfConcentrations += 1
            self.model.insertRow(self.model.rowCount())
            
            #Data from excel
            item = QtGui.QStandardItem(group1[i][1])
            self.model.setItem(row, 0, item)
            #item = QtGui.QStandardItem("{0:.2f}, {0:.2f}, {0:.2f}".format( group1[i][3], group1[i+1][3], group1[i+2][3] ) )
            item = QtGui.QStandardItem('%.2f - %.2f - %.2f' % (group1[i][3], group1[i+1][3], group1[i+2][3]) ) 
            self.model.setItem(row, 1, item)
            item = QtGui.QStandardItem('%.2f -  %.2f - %.2f' % (group2[i][3], group2[i+1][3], group2[i+2][3]) )
            self.model.setItem(row, 2, item) 

            
            data = self.NMRWeightData(group1[i][1].split('-'), sheet_name)
            #print(data)

            item = QtGui.QStandardItem(str(data[0])[0:6])
            self.model.setItem(row, 3, item)
            item = QtGui.QStandardItem(str(data[1])[0:6])
            self.model.setItem(row, 4, item)
            i+=3
            
            #Position
            item = QtGui.QStandardItem(str(row+1))
            self.model.setItem(row, 5, item)

        return self.model
    
    def NMRWeightData(self, remark, sheetname):

        data = pd.read_excel("Data\\NMR_weights.xlsx", sheet_name=sheetname,header=None)
        #print(remark[0])
        for i in range(1,len(data.index)):
            #print(remark[0])
            #print(data[0][i])
            if str(data[0][i]) == str(remark[0]):
                results = [data[7][i], data[8][i]]
                return results
        return [1,0]

    def updateWeights(self, sheetname, row):
        
        item0 = self.model.item(row,0)
        item0Text = str(item0.text())    
        data = self.NMRWeightData(item0Text.split('-'), sheetname)
        if data != [1,0]:
            item3 = self.model.item(row,3)
            item4 = self.model.item(row,4)
            item3.setText(str(data[0])[0:6])
            item4.setText(str(data[1])[0:6])

    def updateAllWeights(self, sheetname):
        for row in range(0, self.model.rowCount()):
            self.updateWeights(sheetname, row)
    def updateSelWeights(self, sheetname, selectedRowsUPD):
        for i in selectedRowsUPD:
            if(i >= 1 or i <= self.model.rowCount()):
                self.updateWeights(sheetname, i-1)

class ComparisonTableModelData():
    def __init__(self):
        self.model = QtGui.QStandardItemModel(0,3)
        self.model.setHorizontalHeaderLabels(('File Name','Legend','Position'))

    def DelRows(self, selectedRowsDEL):
        
        selectedRowsDEL.sort(reverse = True)

        for i in selectedRowsDEL:
            if(i >= 1 or i <= self.model.rowCount()):
                self.model.removeRow(i-1)
            
    def RemoveAllRows(self):
        for row in range(self.model.rowCount()):
            self.model.removeRow(0)

    def AddRows(self, files):
        
        i=0
        
        for row in range(self.model.rowCount(), self.model.rowCount() + len(files)):
        
            self.model.insertRow(self.model.rowCount())
            
            temp = files[i].split('\\')
            temp2 = temp[len(temp)-1].split('.xlsx')

            #Data from excel
            item = QtGui.QStandardItem(temp2[0])
            self.model.setItem(row, 0, item)
            item = QtGui.QStandardItem(self.getMaterialNamefromFile(files[i]))
            self.model.setItem(row, 1, item)
            
            i+=1
            
            #Position
            item = QtGui.QStandardItem(str(row+1))
            self.model.setItem(row, 2, item)

        return self.model

    def getMaterialNamefromFile(self, filepath):
        data = pd.read_excel(filepath, sheet_name='general',header=None)

        return data[1][0]
    

class NMRData:

    #Here we get info for each file
    def getNMRinfo(self, nmrfile):

        #load xml file
        tree = ET.parse(nmrfile)
        
        #Create a list that will contain the different worksheet items
        WorkSheets = list()
        
        #Add Worksheet-items to list 
        #[results, data, experiment, instrument, programmsettings, generator]
        for item in tree.iter("{urn:schemas-microsoft-com:office:spreadsheet}Worksheet"):
            WorkSheets.append(item)
            

        #Extract rows from the first worksheet <results>
        RowsInWorksheet = list()
        for item in WorkSheets[0].iter('{urn:schemas-microsoft-com:office:spreadsheet}Cell'):
            RowsInWorksheet.append(item)

        t_value = 0
        exp_name = ""
        sample_name = ""
        file_name = ""

        for row in range(0, len(RowsInWorksheet), 1):
            #print(str(RowsInWorksheet[row][0].text))
            if str(RowsInWorksheet[row][0].text)=='T1' or str(RowsInWorksheet[row][0].text)=='T2A':
                exp_name = str(RowsInWorksheet[row][0].text)
                t_value = float(str(RowsInWorksheet[row+1][0].text))
                #print(t_value)

        #Extract rows from the third worksheet <experiment>
        RowsInWorksheet = list()
        for item in WorkSheets[2].iter('{urn:schemas-microsoft-com:office:spreadsheet}Cell'):
            RowsInWorksheet.append(item)

        sample_name = str(RowsInWorksheet[70][0].text)
        file_name = str(RowsInWorksheet[34][0].text)

        results = [exp_name, sample_name, file_name, t_value  ]

        return results