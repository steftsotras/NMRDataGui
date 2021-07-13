import sys
from PyQt5 import QtWidgets
from PyQt5 import QtCore, QtGui

from easygui import fileopenbox
import platform
import xml.etree.ElementTree as ET
import functools
import json

from MainWindow import Ui_MainWindow_NMR

class TableModelData():
    

    def __init__(self):
        self.model = QtGui.QStandardItemModel(0,6)
        self.model.setHorizontalHeaderLabels(('Sample Name','T1 Value','T2 Value','Liquid Mass','Particle Mass', 'Position'))
        

    def DelRows(self, selectedRowsDEL):
        
        selectedRowsDEL.sort(reverse = True)

        for i in selectedRowsDEL:
            if(i >= 1 or i <= self.model.rowCount()):
                self.model.removeRow(i-1)
            

    def RemoveAllRows(self):
        
        for row in range(self.model.rowCount()):
            self.model.removeRow(0)

    def AddRows(self, num, group1, group2):
        
        i=0
        
        for row in range(self.model.rowCount(), self.model.rowCount() + num):
        
            self.model.insertRow(self.model.rowCount())
            
            #Data from excel
            item = QtGui.QStandardItem(group1[i][1])
            self.model.setItem(row, 0, item)
            #item = QtGui.QStandardItem("{0:.2f}, {0:.2f}, {0:.2f}".format( group1[i][3], group1[i+1][3], group1[i+2][3] ) )
            item = QtGui.QStandardItem('%.2f - %.2f - %.2f' % (group1[i][3], group1[i+1][3], group1[i+2][3]) ) 
            self.model.setItem(row, 1, item)
            item = QtGui.QStandardItem('%.2f -  %.2f - %.2f' % (group2[i][3], group2[i+1][3], group2[i+2][3]) )
            self.model.setItem(row, 2, item) 

            i+=3
            
            #Position
            item = QtGui.QStandardItem(str(row+1))
            self.model.setItem(row, 5, item)

        return self.model


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