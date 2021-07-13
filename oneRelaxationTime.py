#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 17:08:15 2019

@author: tvt22
"""
from surfaceCalculation import surfaceCalculation

# import packages
import json
import numpy as np
import pandas as pd

# Create class oneRelaxationTime which inherits from surfaceCalculation for calculation of surface area from measurments exhibiting only one relaxation time
class oneRelaxationTime(surfaceCalculation):

        def __init__(self,materialName=[],bulk=[],surfaceArea_Argon=[],temperature=[],date=[],weightFraction=[],densityBulk=[],densityParticle=[],relaxivityFileName=[]):
            surfaceCalculation.__init__(self,materialName,bulk,surfaceArea_Argon,temperature,date,weightFraction,densityBulk,densityParticle,relaxivityFileName)
            
            
        def calculateSurfaceArea(self,T1_T2='T2',calculationOfVolumeFraction='mass'):
            # Calculate surface area using T1 or T2 (using particle volume to liquid volume ratio), T1_T2 = 'T1' or 'T2', calculationOfVolumeFraction = 'mass', 'Mz' or 'Mxy'
            
            # Calculate surface relaxivity ka
            self.calculateSurfaceRelaxivity()
            
            # Calculate mean bulk relaxation time
            bulkRelaxationTimeMean = self.calculateRelaxationTimeMean(self.relaxationTimeBulk[T1_T2])
            
            # Calculate bulk relaxation rate
            bulkRelaxationRate = self.calculateRelaxationRate(bulkRelaxationTimeMean)
            
            # Calculate suspension relaxation rate
            dispersionRelaxationRate = self.calculateRelaxationRate(np.asarray(self.relaxationTime[T1_T2]))
            Rsp = (dispersionRelaxationRate-bulkRelaxationRate)/bulkRelaxationRate
            
            # Calculate surface area
            if calculationOfVolumeFraction == 'mass':
                self.calculateVolumeFractionFromWeightFraction()
                surfaceArea = bulkRelaxationRate*Rsp/(self.volumeFraction[calculationOfVolumeFraction]*self.surfaceRelaxivity[calculationOfVolumeFraction][T1_T2])
                self.surfaceArea[calculationOfVolumeFraction][T1_T2] = np.mean(surfaceArea)
                self.standardDeviation[calculationOfVolumeFraction][T1_T2] = np.std(surfaceArea)
            else:
                self.calculateVolumeFractionFromMagnetization(T1_T2)
                surfaceArea = bulkRelaxationRate*Rsp/(self.volumeFraction[calculationOfVolumeFraction]*self.surfaceRelaxivity[calculationOfVolumeFraction])
                self.surfaceArea[calculationOfVolumeFraction] = np.mean(surfaceArea)
                self.standardDeviation[calculationOfVolumeFraction] = np.std(surfaceArea)
                
                
                
        def createResultsFile(self):
            # Create excel file with all information about the measurement
            
            # Calculate T1/T2 ratio if both relaxation times were measured
            if self.relaxationTime['T1'] and self.relaxationTime['T2']:
                self.relaxationTime['T1_T2_ratio'] = self.calculateT1_T2_ratio(np.mean(self.relaxationTime['T1']),np.mean(self.relaxationTime['T2']))
                              
            # Define name of excel file    
            fileName = '../Results/' + self.bulk + '/' + str(self.date) + '_' + self.materialName + '_' + self.bulk  + '.xlsx'
            
            # if not isinstance(self.volumeFraction['Mz'],list):
            #     self.volumeFraction['Mz'] = self.volumeFraction['Mz'].tolist()
            # if not isinstance(self.volumeFraction['Mxy'],list):
            #     self.volumeFraction['Mxy'] = self.volumeFraction['Mxy'].tolist()
                
            excel_list = []
            excel_list.append(["materialName", self.materialName])
            excel_list.append([ "bulkName", self.bulk])
            excel_list.append(["User", self.user])
            excel_list.append(["remarks", self.remarks])
            excel_list.append(["surfaceArea(Argon)", self.surfaceArea_Argon])
            excel_list.append(["measurementDate", self.date])
            excel_list.append(["temperature", self.temperature])
            
            excel_list.append([])
            excel_list.append(['Bulk'])
            excel_list.append(["densityBulk", self.densityBulk])
            excel_list.append(['initial magnetization Bulk T1'] + self.initialMagnetizationBulk['T1'])
            excel_list.append(['initial magnetization Bulk T2'] + self.initialMagnetizationBulk['T2'])
            excel_list.append(['relaxationTime Bulk T1'] + self.relaxationTimeBulk['T1'])
            excel_list.append(['relaxationTime Bulk T2'] + self.relaxationTimeBulk['T2'])
            
            excel_list.append([])
            excel_list.append(['Suspension'])
            excel_list.append(["densityParticle", self.densityParticle])
            
            excel_list.append(["particleMass", self.particleMass])
            excel_list.append(["liquidMass", self.liquidMass])
            excel_list.append(["weightFraction", self.weightFraction])
            excel_list.append(['initial magnetization Suspension T1'] + self.initialMagnetization['T1'])
            excel_list.append(['initial magnetization Suspension T2'] + self.initialMagnetization['T2'])
            excel_list.append([])
            
            excel_list.append(['determinationOfCalculation','volumeFraction'])
            excel_list.append(['mass', self.volumeFraction['mass']])
            excel_list.append(['Mz', self.volumeFraction['Mz']])
            excel_list.append(['Mxy',self.volumeFraction['Mxy']])
                
            excel_list.append([])
            excel_list.append(['relaxationTime Suspension T1'] + self.relaxationTime['T1'])
            excel_list.append(['relaxationTime Suspension T2'] + self.relaxationTime['T2'])
            excel_list.append([])
            excel_list.append([])
            excel_list.append(['volumeFraction', 'relaxationTime', 'surfaceArea / m2/g', 'standard deviation'])
            excel_list.append(['mass', 'T1', self.surfaceArea['mass']['T1'], self.standardDeviation['mass']['T1']])
            excel_list.append(['mass', 'T2', self.surfaceArea['mass']['T2'], self.standardDeviation['mass']['T2']])
            excel_list.append(['Mz', 'T1', self.surfaceArea['Mz'], self.standardDeviation['Mz']])
            excel_list.append(['Mxy', 'T2', self.surfaceArea['Mxy'], self.standardDeviation['Mxy']])
            
            excel_list.append([])
            excel_list.append([])
            excel_list.append(['relaxivityFileName', self.relaxivityFileName])
            excel_list.append([])
            excel_list.append(['volumeFraction', 'relaxationTime', 'surfaceRelaxivity'])
            excel_list.append(['mass', 'T1', self.surfaceRelaxivity['mass']['T1']])
            excel_list.append(['mass', 'T2', self.surfaceRelaxivity['mass']['T2']])
            excel_list.append(['Mz', 'T1', self.surfaceRelaxivity['Mz']])
            excel_list.append(['Mxy', 'T2', self.surfaceRelaxivity['Mxy']])
            
            fileContent = pd.DataFrame(excel_list)
            
            excel_list_fileNames = []
            excel_list_fileNames.append(['Bulk'])
            excel_list_fileNames.append(["T1", self.measurementFileNames['T1']['Bulk']])
            excel_list_fileNames.append(["T2", self.measurementFileNames['T2']['Bulk']])
            excel_list.append([])
            excel_list_fileNames.append(['Suspension'])
            excel_list_fileNames.append(["T1", self.measurementFileNames['T1']['Suspension']])
            excel_list_fileNames.append(["T2", self.measurementFileNames['T2']['Suspension']])
            excel_list_fileNames.append([])
            
            excel_sheet_fileNames = pd.DataFrame(excel_list_fileNames)
            
            writer = pd.ExcelWriter(fileName, engine='openpyxl')
            
            fileContent.to_excel(writer, 'general',header = None, index=False)
            excel_sheet_fileNames.to_excel(writer, 'measurement files',header = None, index=False)
            writer.save()
            
        def readResultsFile(self, relaxivityFileName):
            # Load all properties from exisitng relaxivity file
            
            # Read general information
            data = pd.read_excel(relaxivityFileName, sheet_name='general',header=None)
                
            self.materialName = data[1][0]
            self.bulk = data[1][1]
            self.user = data[1][2]
            self.remarks = data[1][3]
            self.surfaceArea_Argon=data[1][4]
            self.date = data[1][5]
            self.temperature=data[1][6]
            
            # Information on bulk
            self.densityBulk = data[1][9]
            Mz = data.to_numpy()[10,1:].tolist()
            self.initialMagnetizationBulk['T1'] = [x for x in Mz if ~np.isnan(x)]
            Mxy = data.to_numpy()[10,1:].tolist()
            self.initialMagnetizationBulk['T2'] = [x for x in Mxy if ~np.isnan(x)]
            T1_Bulk = data.to_numpy()[12,1:].tolist()
            self.relaxationTimeBulk['T1'] = [x for x in T1_Bulk if ~np.isnan(x)]
            T2_Bulk = data.to_numpy()[13,1:].tolist()
            self.relaxationTimeBulk['T2'] = [x for x in T2_Bulk if ~np.isnan(x)]
             
            # Information on suspension
            
            self.densityParticle = data[1][16]
            self.particleMass = data[1][17]
            self.liquidMass = data[1][18]
            self.weightFraction = data[1][19]
            Mz = data.to_numpy()[20,1:].tolist()
            self.initialMagnetization['T1'] = [x for x in Mz if ~np.isnan(x)]
            Mxy = data.to_numpy()[21,1:].tolist()
            self.initialMagnetization['T2'] = [x for x in Mxy if ~np.isnan(x)]
            self.volumeFraction['mass'] = data[1][24]
            self.volumeFraction['Mz'] = data[1][25]
            self.volumeFraction['Mxy'] = data[1][26]
            
            T1 = data.to_numpy()[28, 1:].tolist()
            self.relaxationTime['T1'] = [x for x in T1 if ~np.isnan(x)]
            T2 = data.to_numpy()[29,1:].tolist()
            self.relaxationTime['T2'] = [x for x in T2 if ~np.isnan(x)]
            
            self.surfaceArea['mass']['T1'] = data[2][33]
            self.standardDeviation['mass']['T1'] = data[3][33]
            self.surfaceArea['mass']['T2'] = data[2][34]
            self.standardDeviation['mass']['T2'] = data[3][34]
            self.surfaceArea['Mz'] = data[2][35]
            self.standardDeviation['Mz'] = data[3][35]
            self.surfaceArea['Mxy'] = data[2][36]
            self.standardDeviation['Mxy'] = data[3][36]
            
            self.relaxivityFileName = data[1][39]
            
                
        def readResultsFileFromJson(self, fileName):
            # Load all properties from json file of already existing results file
            with open(fileName) as json_file:
                data = json.load(json_file)
                self.materialName = data['materialName']
                self.bulk = data['bulkName']
                self.user = data['user']
                self.remarks = data['remarks']
                self.surfaceArea_Argon = data['surfaceArea(Argon)']
                self.date = data['measurementDate']
                self.temperature = data['temperature']
                self.weightFraction = data['weightFraction']
                self.densityParticle = data['densityParticle']
                self.densityBulk = data['densityBulk']
                self.liquidMass = data['liquidMass']
                self.particleMass = data['particleMass']
                self.volumeFraction = data['volumeFraction']
                self.relaxationTime = data['relaxationTime']
                self.relaxationTimeBulk = data['relaxationTime(Bulk)']
                self.initialMagnetizationBulk = data['initial magnetization(Bulk)']
                self.initialMagnetization = data['initial magnetization(Suspension)']
                self.relaxivityFileName = data['referenceMeasurementFile']
                if 'surfaceRelaxivity' in data:
                    self.surfaceRelaxivity = data['surfaceRelaxivity']
                self.surfaceArea = data['surfaceArea']
                
               

# test = oneRelaxationTime()
# test.readResultsFile('../Results/MP-H2O(lfg)/20200429_Test_MP-H2O(lfg).xlsx')
