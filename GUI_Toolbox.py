import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui

from easygui import fileopenbox
import platform
import xml.etree.ElementTree as ET
import functools
import json
import pandas as pd
import re

import numpy as np
from scipy.optimize import curve_fit
import warnings 

from MainWindow import Ui_MainWindow_NMR

warnings.filterwarnings("ignore")

class TableModelData():
    

    def __init__(self):
        self.model = QtGui.QStandardItemModel(0,6)
        self.model.setHorizontalHeaderLabels(('Position','Sample Name','T1 Value','T2 Value','Liquid Mass','Particle Mass','Volume Fraction'))
        
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
                for k in range(3):
                    self.groupedT1.pop(j)
                    self.groupedT2.pop(j)
                
                

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
            self.model.setItem(row, 1, item)
            #item = QtGui.QStandardItem("{0:.2f}, {0:.2f}, {0:.2f}".format( group1[i][3], group1[i+1][3], group1[i+2][3] ) )
            item = QtGui.QStandardItem('%.2f - %.2f - %.2f' % (group1[i][3], group1[i+1][3], group1[i+2][3]) ) 
            self.model.setItem(row, 2, item)
            item = QtGui.QStandardItem('%.2f -  %.2f - %.2f' % (group2[i][3], group2[i+1][3], group2[i+2][3]) )
            self.model.setItem(row, 3, item) 

            sample_name = group1[i][1]
            #print(sample_name)
            #match = re.match('#([0-9]\.*)*', sample_name)
            match = re.search('(#[0-9]+\.*)', sample_name)

            #print(match)

            if match is not None:
                remark = match[0]
            else:
                remark = ''

            data = self.NMRWeightData(remark, sheet_name)

            if data == 0:
                liq_mass = 1
                par_mass = 0
            else:
                liq_mass = data[0]
                par_mass = data[1]
            #print(data)
            

            item = QtGui.QStandardItem(str(liq_mass)[0:6])
            self.model.setItem(row, 4, item)
            item = QtGui.QStandardItem(str(par_mass)[0:6])
            self.model.setItem(row, 5, item)
            i+=3
            
            #Position
            item = QtGui.QStandardItem(str(row+1))
            self.model.setItem(row, 0, item)

            #Volume Fraction
            vf = par_mass / (liq_mass + par_mass)
            item = QtGui.QStandardItem(str(vf)[0:6])
            self.model.setItem(row, 6, item)

        return self.model
    
    def NMRWeightData(self, remark, sheetname):

        data = pd.read_excel("Data\\NMR_weights.xlsx", sheet_name=sheetname,header=None)
        #print(remark[0])
        for i in range(1,len(data.index)):
            #print(remark[0])
            #print(data[0][i])
            if str(data[0][i]) == remark:
                results = [data[7][i], data[8][i]]
                return results
        return 0

    def updateWeights(self, sheetname, row):
        
        item0 = self.model.item(row,1)
        item0Text = str(item0.text())   

        sample_name = item0Text
        match = re.search('(#[0-9]+\.*)', sample_name)

        if match is not None:
            remark = match[0]
        else:
            remark = ''

        data = self.NMRWeightData(remark, sheetname)
        if data != 0:
            item3 = self.model.item(row,4)
            item4 = self.model.item(row,5)
            item5 = self.model.item(row,6)

            liq_mass = data[0]
            par_mass = data[1]

            item3.setText(str(data[0])[0:6])
            item4.setText(str(data[1])[0:6])

            vf = par_mass / (liq_mass + par_mass)
            item5.setText(str(vf)[0:6])

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

        self.numberOfRelaxativityFiles = 0
        self.RelaxativityFiles = list()

    def getRelaxativityFiles(self):
        return self.RelaxativityFiles
    def getNumOfRelaxativityFiles(self):
        return self.numberOfRelaxativityFiles

    def DelRows(self, selectedRowsDEL):
        
        selectedRowsDEL.sort(reverse = True)

        for i in selectedRowsDEL:
            if(i >= 1 or i <= self.model.rowCount()):
                self.model.removeRow(i-1)

                self.RelaxativityFiles.pop(i-1)
                self.numberOfRelaxativityFiles -= 1
            
    def RemoveAllRows(self):
        self.numberOfRelaxativityFiles = 0
        self.RelaxativityFiles = list()
        for row in range(self.model.rowCount()):
            self.model.removeRow(0)

    def AddRows(self, files):
        
        i=0
        
        for row in range(self.model.rowCount(), self.model.rowCount() + len(files)):
            
            
            self.RelaxativityFiles.append(files[i])
            self.numberOfRelaxativityFiles += 1

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


    #def getSpinsolveData(self, nmrfile):

    def SpinsolveT1_graphdata(self, file):

        # Import Graph data

        df = pd.read_csv (file, decimal='.', delimiter='\t', header=None)

        # print (df)
        Intensity_list_graph = np.asarray(df[1].tolist())
        Frequency_list_graph = np.asarray(df[0].tolist())

        # plt.figure()
        # plt.scatter(Frequency_list_graph,Intensity_list_graph)
        # plt.xlabel('Time / s')
        # plt.ylabel('Intensity')
        # # plt.savefig('20210607-095459-T2 Bulk-Wasser_raw-data.png')
        # plt.show()

        def fit_func(x, y_0, A, R_0):
            y = y_0 + A * np.exp(- R_0*x)
            return y

        anonymous_fun = lambda x, y_0, R_0, A: fit_func(x, y_0, A, R_0) 

        popt, pcov = curve_fit(anonymous_fun, xdata = Frequency_list_graph, ydata = Intensity_list_graph)

        R_0_fit = popt[1]
        T1_long = (1/R_0_fit)*1000 #ms
        T1 = round(T1_long, 1)

        #print('T1 = ', T1, 'ms')
        return T1

    def SpinsolveT2_log(self,file):
        
        valuesFrom0to1 = [x * 0.3 for x in range(0, 5)]
        valuesFrom1to30 = [x * 0.5 for x in range(3, 80)]
        valuesFrom0to1.extend(valuesFrom1to30)
        valuesFrom0to1.reverse()


        df = pd.read_csv (file, decimal=',', delimiter=';', header=0)
        Intensity_list = np.asarray(df['Intensity'].tolist())
        Frequency_list = np.asarray(df['Frequency(ppm)'].tolist())


        for i in valuesFrom0to1: 
            try:
                Frequency_list_short = Frequency_list[Frequency_list<i]  #evtl bis zur fehlermeldung
                Intensity_list_short = Intensity_list[Frequency_list<i]
                
                Intensity_list_log = np.log(Intensity_list_short)
                
                def fit_func(x, y_0, A, R_0):
                    y = np.log(y_0 + A * np.exp(- R_0*x))
                    return y
                
                anonymous_fun = lambda x, y_0, R_0, A: fit_func(x, y_0, A, R_0) 
                
                popt, pcov = curve_fit(anonymous_fun, xdata = Frequency_list_short, ydata = Intensity_list_log)
                
                R_0_fit = popt[1]
                T2_long = (1/R_0_fit)*1000 #ms
                T2 = round(T2_long, 1)

                #print('T2 = ', T2, 'ms')
                return T2
                
            except ValueError: 
                continue
