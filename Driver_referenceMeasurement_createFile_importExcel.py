#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 14:03:42 2019

@author: tvt22
"""

import referenceMeasurement as refe
import numpy as np
import matplotlib.pyplot as plt

from ImportNmrData import NmrToolbox

import locale


from matplotlib import rcParams


class Driver_referenceMeasurement_createFile_importExcel:
    
     

    
    def runDriver(self, materialName, evaluation, bulkName, user, lang, remarks, temperature, surfaceArea_Argon, densityBulk, particleDensity, date, numofcon, filesT1, filesT2, filespathT1, filespathT2, liquidMass, particleMass  ):

        rcParams.update({'figure.autolayout': True})

        #materialName = '80nmIV'

        thickener = False

        if lang == 'english':
            pass
        elif lang == "german":
            locale.setlocale(locale.LC_NUMERIC, "de_DE")
            plt.rcdefaults()
            plt.rcParams['axes.formatter.use_locale'] = True
            plt.rcParams.update({'font.size': 12})

        #evaluation = 'single'

        #bulkName = 'Milipore-Wasser_LFG'
        #user = 'Alexander Michalowski'
        # german oder english
        #language = 'german'

        # General Remarks, e.g. sediment or suspension, particles were still agglomerated during measurement, sedimentation occured during measurement, ...
        #remarks = '#76,#77,#79'

        ## Additional information about measurement
        #date = '20210317'
        #temperature = '25°C'
        #print (date)
        ## Surface area of particles measured with BET-method and argon in m2/g (Necessary to calculate ka)
        #surfaceArea_Argon = 47.0

        # Density of bulk liquid in g/cm3
        #densityBulk = 1

        # Sceletal density of particles in g/cm3

        #particleDensity = 2.14

        # Mass of particles in g 
        #particleMass = [0, 0.1036, 0.2145, 0.4187]

        # Mass of liquid in g
        #liquidMass = [1, 1.9080, 1.7981, 1.6013]

        # WeightFraction calculated with particleMass and liquidMass (not necessary if particle Mass and liquidMass are defined)
        #weightFraction = [0,10,20,30,40]
        #volumeFraction = ([0,0.0478,0.1076,0.1845,0.287])

        # Relaxation times T1 and T2, defined as T = [[relaxation times of 1st concentration] [relaxation times of 2nd concentration] [...]]
        #T1 = [[1771.9,1791.7,1746.1],[1766.7,1786.4,1854.4],[1843.2,1832.5,1757],[1762.5,1749.3,1733.6],[1774.2,1838.6,1739.1],[1689.2,1997.7,1769.0]]
        #T2 = [[1739.6,1762.1,1749.5],[1576.2,1578.8,1597.4],[1466.8,1463.6,1478.9],[1375.5,1378.7,1379.9],[980.1,989.5,985.8],[902.0,905.1,919.8]]

        # print()
        # print ("T1 FILES PATH")
        # print (filespathT1, filesT1)
        # print ("T2 FILES PATH")
        # print (filespathT2, filesT2)

        # T1 and Mz lists are generated - only select files for T1 here
        #T1, Mz, fileNames_T1 = NmrToolbox.getCalibrationResults('T1', 4)
        T1, Mz, fileNames_T1 = NmrToolbox.getCalibrationResults2(filespathT1, filesT1, numofcon)

        # T2 an Mxy lists are generated - only select files for T2 here
        #T2, Mxy, fileNames_T2 = NmrToolbox.getCalibrationResults('T2', 4)
        T2, Mxy, fileNames_T2 = NmrToolbox.getCalibrationResults2(filespathT2 ,filesT2, numofcon)


        # If porousMaterial=1: Set surface relaxivity calculated from porous material with 2 relaxation times with class porous material
        # If porousMaterial=0; Calculate surface relaxivity of nonporous material (1 relaxation time)
        porousMaterial=0
        surfaceRelaxivity_T2_Mxy =[]

        # Initial magnetization
        # Mz = [[103,105,101],[98,100,97],[92,94,92],[86,83,85]]
        # Mxy = [[288,286,282],[275,274,270],[258,255,258],[227,227,227],[209,206,205]]

        # Mz_Bulk = [102,100,101]
        # Mxy_Bulk = [283,284,285]




        # Create object 'ref' of class referenceMeasurement with properties materialName and bulkName
        ref = refe.referenceMeasurement(materialName, bulkName) 
        ref.setDate(date)
        ref.setTemperature(temperature)
        ref.setUser(user)
        ref.setRemarks(remarks)

        # Set liquid density and particle density
        ref.setDensity(densityBulk,particleDensity)

        ## Set particle mass and liquid mass and calculate weightFraction or alternatively set weightFraction
        ref.setParticleMass(particleMass)
        ref.setLiquidMass(liquidMass)
        ref.calculateWeightFraction()
        #ref.setWeightFraction(weightFraction)

        # Set surface area calculated with BET method and argon
        ref.setSurfaceArea(surfaceArea_Argon)

        # Set relaxation times T1 and T2
        ref.setRelaxationTime('T1',T1)
        if not porousMaterial:
            ref.setRelaxationTime('T2',T2)
        else:
            ref.surfaceRelaxivity['volFrac_Mxy'] = surfaceRelaxivity_T2_Mxy

        # Set initial magnetization of suspension and bulk
        ref.setInitialMagnetization(Mz,'T1')
        ref.setInitialMagnetization(Mxy,'T2')

        # Calculate and set volume Fraction
        volFrac = ref.calculateVolumeFractionFromWeightFraction()
        volFrac = ref.calculateVolumeFractionFromMagnetization('T1')
        volFrac = ref.calculateVolumeFractionFromMagnetization('T2')
        #ref.setVolumeFraction(volumeFraction,'mass')


        # Calculate surface relaxivity ka for T1 and T2 measurement
        if thickener == False:
            ref.calculate_surfaceRelaxivity('T1', evaluation, lang, calculationOfVolFraction='mass', plot=True)
            ref.calculate_surfaceRelaxivity('T1', evaluation, lang, calculationOfVolFraction='Mz', plot=True)
            
            # Create T1/T2 vs. concentration and T1/T2 vs. absolute surface area (information about surface chemistry?)
            # slope_conc, slope_surf = ref.plot_T1_T2_ratio('german')
            
            # Calculate surface relaxivity in case of nonporous material
            if not porousMaterial:
                ref.calculate_surfaceRelaxivity('T2', evaluation, lang, calculationOfVolFraction='mass', plot=True)
                ref.calculate_surfaceRelaxivity('T2', evaluation, lang, calculationOfVolFraction='Mxy', plot=True)
            
            ref.setMeasurementFileNames(fileNames_T1, fileNames_T2)
            ref.createRelaxivityFile(evaluation)    
            
        # Plot calibration for thickener in dispersant    
        else:
            ref.plotCalibrationWithThickener('T1',calculationOfVolFraction='mass', languange = lang)
            ref.plotCalibrationWithThickener('T1',calculationOfVolFraction='Mz', languange = lang)
            
            ref.plotCalibrationWithThickener('T2',calculationOfVolFraction='mass', languange = lang)
            ref.plotCalibrationWithThickener('T2',calculationOfVolFraction='Mxy', languange = lang)
            


if __name__ == '__main__':
    driver = Driver_referenceMeasurement_createFile_importExcel()
    driver.runDriver()
