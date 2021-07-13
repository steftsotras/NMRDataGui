#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep 26 10:44:52 2019

@author: tvt22
"""
from NMR import NMR
import numpy as np
import json
import pandas as pd

# Create class surface calculation which inherits from class NMR and has additional properties relaxationTimeBulk and surfaceArea
class surfaceCalculation(NMR):

        def __init__(self,materialName=[],bulk=[],surfaceArea_Argon=[],temperature=[],date=[],weightFraction=[],densityBulk=[],densityParticle=[],relaxivityFileName=[]):
            NMR.__init__(self,materialName,bulk,surfaceArea_Argon,temperature,date,weightFraction,densityBulk,densityParticle,relaxivityFileName)
            
            self.initialMagnetizationBulk = {'T1':[],'T2':[]} 
          
            
            # Create property relaxationTimeBulk as dict
            self.relaxationTimeBulk = {'T1':[],'T2':[]}
            
            self.measurementFileNames = {'T1': {'Bulk':[],'Suspension':[]},'T2': {'Bulk':[],'Suspension':[]}}

            # Create property surface area as dict for surface area calculated with T1 and T2, in m2/g 
            # Additional entry 'mass' for alternative calculation of surface area via molar ratio: k_a = l_ads*rho_ads*(1/T_ads - 1/T_Bulk) and S = (1/T - 1/T_Bulk)/(m_p/m_F * k_a), in m2/g
            self.surfaceArea = {'mass':{'T1':[],'T2':[]}, 'Mz':[], 'Mxy':[]}
            self.standardDeviation = {'mass':{'T1':[],'T2':[]}, 'Mz':[], 'Mxy':[]} # Standard Deviation of surface area (due to repeated measurement of T1 or T2 of the suspension)
            
            
        def setInitialMagnetizationBulk (self,initialMagnetizationBulk,T1_T2):
            self.initialMagnetizationBulk[T1_T2] = initialMagnetizationBulk
            
        
        def setMeasurementFileNames(self, fileNames_T1, fileNames_T2, bulk_suspension):
            self.measurementFileNames['T1'][bulk_suspension] = fileNames_T1
            self.measurementFileNames['T2'][bulk_suspension] = fileNames_T2

            
        def calculateVolumeFractionFromMagnetization(self,T1_T2='T2'):
            # Calculate volume fraction with difference of initial magnetization of bulk and suspension 
    
            particleVolume = np.mean(np.asarray(self.initialMagnetizationBulk[T1_T2]))-np.mean(np.asarray(self.initialMagnetization[T1_T2]))
            if T1_T2 == 'T1':
                self.volumeFraction['Mz'] = (particleVolume/np.mean(np.asarray(self.initialMagnetization[T1_T2])))
            elif T1_T2 == 'T2':
                self.volumeFraction['Mxy'] = (particleVolume/np.mean(np.asarray(self.initialMagnetization[T1_T2])))
            return particleVolume/np.mean(np.asarray(self.initialMagnetization[T1_T2])) 
        
        def setRelaxivityFileName(self,relaxivityFileName):
            # Set name of relaxivityFile which contains ka for surface area calculation
            self.relaxivityFileName = relaxivityFileName
        
        def setRelaxationTimeBulk(self,T1_T2,relaxationTimes):
            # Set relaxation time of bulk in ms
            if T1_T2 == 'T1':
                self.relaxationTimeBulk['T1'] = relaxationTimes
            else:
                self.relaxationTimeBulk['T2'] = relaxationTimes
            
        def calculateSurfaceRelaxivity(self):
            # Calculate value of surface relaxivity ka from reference measurement 
            
            # Get surface relaxivity from calibration measurement of relaxivityFile and get density of reference material
            # Uncomment if reference measurement file is an excel file
            # with open(self.relaxivityFileName) as json_file:
            #     data = json.load(json_file)
            #     surfaceRelaxivityRef = data['surfaceRelaxivity']
            #     densityRef = data['densityParticle']
            
            # Read surface relaxivity and particle density from xlsx file, Uncomment if reference measurement file is a xls-file
            data = pd.read_excel(self.relaxivityFileName, sheet_name='general',header=None)
            densityRef = data[1][7]
            
            surfaceRelaxivityRef={'mass':{'T1':[],'T2':[]},'Mz':[],'Mxy':[]}
            surfaceRelaxivityRef['mass']['T1'] = data[2][11]
            surfaceRelaxivityRef['mass']['T2'] = data[2][12]
            surfaceRelaxivityRef['Mz'] = data[2][13]
            surfaceRelaxivityRef['Mxy'] = data[2][14]
            
            # Calculate surface relaxivity of the measured suspension with reference material (volume fraction calcuated from weight fraction) from relaxivityFile if T1 was measured
            if surfaceRelaxivityRef['mass']['T1']:
                self.surfaceRelaxivity['mass']['T1'] = surfaceRelaxivityRef['mass']['T1']*self.densityParticle/densityRef
            
            # Calculate surface relaxivity of the measured suspension with reference material (volume fraction calcuated from weight fraction) from relaxivityFile if T2 was measured
            if surfaceRelaxivityRef['mass']['T2']:    
                self.surfaceRelaxivity['mass']['T2'] = surfaceRelaxivityRef['mass']['T2']*self.densityParticle/densityRef
                
            # Calculate surface relaxivity of the measured suspension with reference material (volume fraction calcuated from initial magnetization Mxy) from relaxivityFile
            if surfaceRelaxivityRef['Mxy']:    
                self.surfaceRelaxivity['Mxy'] = surfaceRelaxivityRef['Mxy']*self.densityParticle/densityRef
            
            # Calculate surface relaxivity of the measured suspension with reference material (volume fraction calcuated from initial magnetization Mz) from relaxivityFile
            if surfaceRelaxivityRef['Mz']:    
                self.surfaceRelaxivity['Mz'] = surfaceRelaxivityRef['Mz']*self.densityParticle/densityRef
            
        


