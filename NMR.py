#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 10:43:41 2019

@author: tvt22
"""

# import packages
import numpy as np
import matplotlib.pyplot as plt

# Define class NMR with properties materialName, bulk, surfaceArea_Argon, temperature, ...
class NMR:

        def __init__(self,materialName=[],bulk=[],user=[],surfaceArea_Argon=[],temperature=[],date=[],weightFraction=[],liquidMass=[],particleMass=[],densityBulk=[],densityParticle=[],relaxivityFileName=[]):
            self.materialName = materialName
            self.bulk = bulk
            self.user = user
            self.remarks = []
            self.surfaceArea_Argon = surfaceArea_Argon # BET surface area measured with argon in m2/g
            self.temperature = temperature # Temperature during measurement in °C
            self.date = date
            self.weightFraction = weightFraction
            self.densityBulk = densityBulk # density of bulk in g/cm3
            self.densityParticle = densityParticle # skeletal density of particles in g/cm3
            self.particleMass = particleMass # in g
            self.liquidMass = liquidMass # in g
            self.volumeFraction = {'mass':[], 'Mz':[], 'Mxy':[]} # Volume fraction calculated with weight of particle and liquid or with initial magnetization Mz and Mxy
            self.relaxationTime = {'T1':[],'T2':[],'T1_T2_ratio':[]} # dict with entries for T1 and T2 in ms and for T1/T2-ratio
            self.surfaceRelaxivity = {'mass':{'T1':[],'T2':[]}, 'Mz':[], 'Mxy':[]} # Surface relaxivity k_a (calculated with reference material) for different calculations of volume fraction (with mass ot initial magnetization Mz or Mxy)
            self.relaxivityFileName = relaxivityFileName # Name of file with reference measurement          
            self.measurementFileNames = {'T1': [],'T2': []}
            self.initialMagnetization = {'T1':[],'T2':[]}
    
                    
        def cm2inch(self,value):
            # Conversion of cm to inch, necessary to set size of plots in cm
            return value/2.54
       
        def setRemarks(self,remarks):
            self.remarks = remarks
        
        def setWeightFraction(self,weightFraction):
            # Set weight fraction of suspension
            self.weightFraction = weightFraction
        
        def setDensity(self,densityBulk,densityParticle):
            # Set bulk density and particle density in g/cm3
            self.densityBulk = densityBulk      
            self.densityParticle = densityParticle
            
        def setInitialMagnetization(self,initialMagnetization,T1_T2):
            # Set initial magnetization of bulk and suspension Mz(0) for T1 and Mxy(0) for T2 measurements, variable T1_T2 = 'T1' bzw. T1_T2 = 'T2'
            self.initialMagnetization[T1_T2] = initialMagnetization
            
        def setDate(self,date):
            # Set measurement date
            self.date = date
        
        def setTemperature(self,temperature):
            # Set tempeature in acorn area/flow cell during measurement
            self.temperature = temperature
            
        def setUser(self, user):
            self.user = user
            
        def setSurfaceArea(self,surfaceArea_Argon):
            # Set surface area calculated with BET-method and argon in m2/g
            self.surfaceArea_Argon = surfaceArea_Argon
        
        def setParticleMass(self,particleMass):
            # Set mass of particles in g
            self.particleMass = particleMass
            
        def setLiquidMass(self,liquidMass):
            # Set mass of liquid in g
            self.liquidMass = liquidMass
            
        def setRelaxationTime(self,T1_T2,relaxationTime):
            # Set relaxation times T1 and T2 in ms
            self.relaxationTime[T1_T2] = relaxationTime
            
        def setMeasurementFileNames(self, fileNames_T1, fileNames_T2):
            self.measurementFileNames['T1'] = fileNames_T1
            self.measurementFileNames['T2'] = fileNames_T2

        
        def setVolumeFraction(self,volumeFraction=[],calculationOfVolFrac='mass'):
            # Set measured volume fraction (calculated with particle and liquid mass or with initial magnetization of suspension and bulk)
            self.volumeFraction[calculationOfVolFrac] = volumeFraction
        
        def calculateWeightFraction(self):
            # Calculate weight fraction
            # Dividing lists not possible -> Change list to array for calculation
            if type(self.particleMass) == list:
                weigthFractionArray = np.asarray(self.particleMass) / (np.asarray(self.particleMass) + np.asarray(self.liquidMass))
                self.weightFraction = weigthFractionArray.tolist()
            else:
                self.weightFraction = self.particleMass/(self.particleMass+self.liquidMass)
            return self.weightFraction
            
        def calculateVolumeFractionFromWeightFraction(self):
            # Calculate volume fraction from weight fraction with bulk density and particle density
            volumeFraction = np.asarray(self.weightFraction)*self.densityBulk/((1-np.asarray(self.weightFraction))*self.densityParticle)
            self.volumeFraction['mass'] = volumeFraction.tolist()
            return volumeFraction.tolist()
            
        def calculateT1_T2_ratio(self,T1,T2):
            # Calculate relaxation time ratio T1/T2
            # relaxationTimesRatio = np.asarray(self.calculateRelaxationTimeMean(T1))/np.asarray(self.calculateRelaxationTimeMean(T2))
            relaxationTimesRatio = np.asarray(T1)/np.asarray(T2)
            return relaxationTimesRatio.tolist()
            
        def calculateRelaxationTimeMean(self,relaxationTimes):
            # Calculate mean relaxation time for repeated measurements
            if relaxationTimes:
                relaxationTimeMean = np.mean(np.asarray(relaxationTimes)) 
            elif relaxationTimes == []:
                relaxationTimeMean = []
            return relaxationTimeMean
        
        def calculateRelaxationRate(self,relaxationTime):
            # Calculate the relaxation rate 1/T1 or 1/T2
            return 1/relaxationTime
        

                
            
        
    