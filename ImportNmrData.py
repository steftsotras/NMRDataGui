# -*- coding: utf-8 -*-
"""
Created on Tue Jul 21 14:35:44 2020

@author: Simon Eder
"""

import xml.etree.ElementTree as ET
import pandas as pd
from easygui import fileopenbox
import platform
import matplotlib.pyplot as plt

class NmrToolbox():

# Number of concentrations should be inserted as reference for NmrToolbox
    
    def importNMRDATA(path):
        """This function extracts results and rawdata from an .nmrdata file
        
        Attributes:
            path (str):         path to the file. So far, this method doesn't check if
                                the file has a valide ending for this method
                        
        Returns:
            results (dict):     List that contains key parameters of the result
                                worksheet of the xml
            data (pd.Series):   Pandas.Series object that contains the raw data
                                of the measurement. The index is the measurement
                                time in ms
                                
                                
        Note: 
            Extracted XML-Strucutre: <worksheet>
                                         <cell>
                                             <rows>
                                                 <data>
                                                     Information
                                                 <\data>
                                             <\rows>
                                         <\cell>
                                         <cell>
                                             <rows>
                                                 <data>
                                                     Information
                                                 <\data>
                                             <\rows>
                                         <\cell>
                                         <cell>
                                             <rows>
                                                 <data>
                                                     Information
                                                 <\data>
                                             <\rows>
                                         <\cell>
                                     <\worksheet>
                                     
            The original xml sheet contains more layers. First the worksheet
            layers (6 in total) are extracted and saved into WorkSheets list. 
            Inside a single WorkSheet, the cell layer is extracted.
            Afterwards, information from a cell is extracted
            straigt forward cell[row][data].text
        """
        #load xml file
        tree = ET.parse(path)
        
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
            
        #Save results. RowPositioins are fixed
        results = list()
        
        
        #Extract data from xml <first worksheet><rows [14-34]><data[0}>.text
        if str(RowsInWorksheet[13][0].text)=='T1':
        
            # T1 Files            
           
            results.append(float(RowsInWorksheet[14][0].text))      #"T1"
            results.append(float(RowsInWorksheet[18][0].text))      #"Mz0"
            results.append(float(RowsInWorksheet[22][0].text))      #"alpha"
            
        else:    
            # T2 Files         
            
            results.append(float(RowsInWorksheet[14][0].text))          #"T2A"
            results.append(float(RowsInWorksheet[18][0].text))          #"Mxy0A"
            results.append(float(RowsInWorksheet[22][0].text))          #"T2B"
            results.append(float(RowsInWorksheet[26][0].text))          #"C"
            results.append(float(RowsInWorksheet[30][0].text))          #"Cphase"
            results.append(float(RowsInWorksheet[34][0].text))          #"M0phase"
        
        #Test
        #print(results)
        
        
        
        #Extract rows from the second worksheet <data>
        RowsInWorksheet = list()
        for item in WorkSheets[1].iter('{urn:schemas-microsoft-com:office:spreadsheet}Cell'):
            RowsInWorksheet.append(item)
            
        
        #extract data from the table
        time = list()
        mxy = list()
        mz = list()
    
         
        if str(RowsInWorksheet[5][0].text)=='time /ms':
        
            # T2 Files            
        
            for row in range(9, len(RowsInWorksheet), 6):
                time.append(float(RowsInWorksheet[row][0].text))
                mxy.append(float(RowsInWorksheet[row+1][0].text))
            
            #save raw data into a pd Series
            data = pd.Series(mxy, index=time)
            return(results, data)
        
        
        else:
            
            # T1 Files
            
            for row in range(9, len(RowsInWorksheet), 4):
                time.append(float(RowsInWorksheet[row][0].text))
                mz.append(float(RowsInWorksheet[row+3][0].text))
                
            #save raw data into a pd Series
            data = pd.Series(mz, index=time)
            return(results, data)
    
    def getCalibrationResults2(filespath, files, numberOfConcentrations):
        # if __name__ == "__main__":
            
        #numberOfConcentrations = 2
    
        
        allRelaxationTimes = list()
        allMagnetizations = list()
        allFiles = list()
        i=0
        for f in files:
            
                
            allFiles.append(f)
            
            relaxationTimes = list()
            magnetization = list()
            
    
            for fileName in filespath[i]:
            # Results, Plot of all Files
                results, data = NmrToolbox.importNMRDATA(fileName)
            
                relaxationTimes.append(results[0])
                magnetization.append(results[1])
                
            
            allRelaxationTimes.append([])
            allMagnetizations.append([])
            
            allRelaxationTimes[i] = relaxationTimes
            allMagnetizations[i] = magnetization
            i+=1
    
        return allRelaxationTimes, allMagnetizations, allFiles


    def getCalibrationResults(T1_T2, numberOfConcentrations):
        # if __name__ == "__main__":
            
        #numberOfConcentrations = 2
    
        
        allRelaxationTimes = list()
        allMagnetizations = list()
        allFiles = list()
        
        for concentrationNumber in range(1, numberOfConcentrations+1):
            textForOpeningFiles = "Please select Files for Concentration #" + str(concentrationNumber)
            if 'Windows' in platform.platform():
                # Rechner Uni
                if T1_T2 == 'T1':
                    files = fileopenbox(textForOpeningFiles, "RELAXATION T1", default = "m:/AcornArea/Alexander Michalowski/*", filetypes= "*.txt", multiple=True)
                else:
                    files = fileopenbox(textForOpeningFiles, "RELAXATION T2", default = "m:/AcornArea/Alexander Michalowski/*", filetypes= "*.txt", multiple=True)
                # # Laptop Ute
                # if T1_T2 == 'T1':
                #     files = fileopenbox(textForOpeningFiles, "RELAXATION T1", default = "T:/Ute Schmidt/Ute Schmidt/*", filetypes= "*.txt", multiple=True)
                # else:
                #     files = fileopenbox(textForOpeningFiles, "RELAXATION T2", default = "T:/Ute Schmidt/Ute Schmidt/*", filetypes= "*.txt", multiple=True)
                # Save only realtive path starting from the folder 'AcornArea/'
                files_forExcel = []
                for file in files:
                    files_forExcel.append(file.replace('m:/AcornArea/Alexander Michalowski/', ''))
            if 'Linux' in platform.platform():
                if T1_T2 == 'T1':
                    files = fileopenbox(textForOpeningFiles, "RELAXATION T1", default = "/mnt/Messdaten/AcornArea/*", filetypes= "*.txt", multiple=True)
                else:
                    files = fileopenbox(textForOpeningFiles, "RELAXATION T2", default = "/mnt/Messdaten/AcornArea/*", filetypes= "*.txt", multiple=True)
                
                # Save only realtive path starting from the folder 'AcornArea/'
                files_forExcel = []
                for file in files:
                    files_forExcel.append(file.replace('/mnt/Messdaten/AcornArea/', ''))
                
            allFiles.append(files_forExcel)
            
            relaxationTimes = list()
            magnetization = list()
            
    
            for fileName in files:
            # Results, Plot of all Files
                results, data = NmrToolbox.importNMRDATA(fileName)
            
                relaxationTimes.append(results[0])
                magnetization.append(results[1])
                
            
            allRelaxationTimes.append([])
            allMagnetizations.append([])
            
            allRelaxationTimes[concentrationNumber-1] = relaxationTimes
            allMagnetizations[concentrationNumber-1] = magnetization
    
        return allRelaxationTimes, allMagnetizations, allFiles
    

    def getSurfaceAreaMeasuremntResults(T1_T2, bulk_suspension):
        
        if bulk_suspension == 'Bulk':
            textForOpeningFiles = "Please select Files for " + 'Bulk' 
        else:
            textForOpeningFiles = "Please select Files for " + 'Suspension' 
            
        if 'Windows' in platform.platform():
            if T1_T2 == 'T1':
                files = fileopenbox(textForOpeningFiles, "RELAXATION T1", default = "m:/AcornArea/Ute Schmidt/*", filetypes= "*.txt", multiple=True)
            else:
                files = fileopenbox(textForOpeningFiles, "RELAXATION T2", default = "m:/AcornArea/Ute Schmidt/*", filetypes= "*.txt", multiple=True)
           
            # Save only realtive path starting from the folder 'AcornArea/'
            files_forExcel = []
            for file in files:
                files_forExcel.append(file.replace('m:/AcornArea/Ute Schmidt/', ''))
        
        if 'Linux' in platform.platform():
            if T1_T2 == 'T1':
                files = fileopenbox(textForOpeningFiles, "RELAXATION T1", default = "/mnt/Messdaten/AcornArea/*", filetypes= "*.txt", multiple=True)
            else:
                files = fileopenbox(textForOpeningFiles, "RELAXATION T2", default = "/mnt/Messdaten/AcornArea/*", filetypes= "*.txt", multiple=True)
            
            # Save only realtive path starting from the folder 'AcornArea/'
            files_forExcel = []
            for file in files:
                files_forExcel.append(file.replace('/mnt/Messdaten/AcornArea/', ''))
                
            
        relaxationTimes = list()
        magnetization = list()

        for fileName in files:
        # Results, Plot of all Files
            results, data = NmrToolbox.importNMRDATA(fileName)
        
            relaxationTimes.append(results[0])
            magnetization.append(results[1])
    
        return relaxationTimes, magnetization, files_forExcel    
    
    def getMagnetization_T2(path):
        #load xml file
        tree = ET.parse(path)
        
        #Create a list that will contain the different worksheet items
        WorkSheets = list()
        
        #Add Worksheet-items to list 
        #[results, data, experiment, instrument, programmsettings, generator]
        for item in tree.iter("{urn:schemas-microsoft-com:office:spreadsheet}Worksheet"):
            WorkSheets.append(item)
            
        #Extract rows from the first worksheet <results>
        RowsInWorksheet = list()
        for item in WorkSheets[1].iter('{urn:schemas-microsoft-com:office:spreadsheet}Cell'):
            RowsInWorksheet.append(item)



#results, datat = NmrToolbox.getMagnetization_T2('experiment-T₂ measurement-0004.nmrdata')    
