#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 14:03:42 2019

@author: tvt22
"""

import referenceMeasurement as refe
import numpy as np
import matplotlib.pyplot as plt
import locale

from ImportNmrData import NmrToolbox

from matplotlib import rcParams


class Driver_referenceMeasurement_createFile_withoutExcel:
    def runDriver(self, materialName, evaluation, bulkName, user, lang, remarks, temperature, surfaceArea_Argon, densityBulk, particleDensity, date, numofcon, T1, T2, filespathT1, filespathT2, liquidMass, particleMass):
        
        
        rcParams.update({'figure.autolayout': True})

        thickener = False

        if lang == 'english':
            locale.setlocale(locale.LC_NUMERIC, "en_US")
            plt.rcdefaults()
            plt.rcParams['axes.formatter.use_locale'] = True
            plt.rcParams.update({'font.size': 12})

        elif lang == "german":
            locale.setlocale(locale.LC_NUMERIC, "de_DE")
            plt.rcdefaults()
            plt.rcParams['axes.formatter.use_locale'] = True
            plt.rcParams.update({'font.size': 12})

        # Material name and name of bulk


        # Relaxation times T1 and T2, defined as T = [[relaxation times of 1st concentration] [relaxation times of 2nd concentration] [...]]
        #T1 = [[1771.9,1791.7,1746.1],[1766.7,1786.4,1854.4],[1843.2,1832.5,1757],[1762.5,1749.3,1733.6],[1774.2,1838.6,1739.1]]
        #T2 = [[2619.9,2639.4,2642.4],[662.1,675.6,677.6],[363.8,362.7,363.0],[220.8,224.0,224.1],[165.0,167.3,167.5]]

        # T1 and Mz lists are generated - only select files for T1 here
        #T1, Mz, fileNames_T1 = NmrToolbox.getCalibrationResults('T1', 5)

        # T2 an Mxy lists are generated - only select files for T2 here
        #T2, Mxy, fileNames_T2 = NmrToolbox.getCalibrationResults('T2', 5)


        # If porousMaterial=1: Set surface relaxivity calculated from porous material with 2 relaxation times with class porous material
        # If porousMaterial=0; Calculate surface relaxivity of nonporous material (1 relaxation time)
        porousMaterial=0
        surfaceRelaxivity_T2_Mxy =[]

        # Initial magnetization
        # Mz = [[103,105,101],[98,100,97],[92,94,92],[86,83,85]]
        # Mxy= [[288,286,282],[275,274,270],[258,255,258],[227,227,227],[209,206,205]]

        # Mz_Bulk = [102,100,101]
        # Mxy_Bulk = [283,284,285]

        Mz = [[0 for x in range(3)] for y in range(numofcon)]
        Mxy = [[0 for x in range(3)] for y in range(numofcon)]



        # Create object 'ref' of class referenceMeasurement with properties materialName and bulkName
        ref = refe.referenceMeasurement(materialName, bulkName) 
        ref.setDate(date)
        ref.setTemperature(temperature)
        ref.setUser(user)
        ref.setRemarks(remarks)

        ref.MakeDirectory()

        # Set liquid density and particle density
        ref.setDensity(densityBulk,particleDensity)

        ## Set particle mass and liquid mass and calculate weightFraction or alternatively set weightFraction
        ref.setParticleMass(particleMass)
        ref.setLiquidMass(liquidMass)
        ref.calculateWeightFraction()
        # ref.setWeightFraction(weightFraction)

        # Set surface area calculated with BET method and argon
        ref.setSurfaceArea(surfaceArea_Argon)

        # Set relaxation times T1 and T2
        ref.setRelaxationTime('T1',T1)
        if not porousMaterial:
            ref.setRelaxationTime('T2',T2)
        else:
            ref.surfaceRelaxivity['volFrac_Mxy'] = surfaceRelaxivity_T2_Mxy

        # # Set initial magnetization of suspension and bulk
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
            #ref.calculate_surfaceRelaxivity('T1', evaluation, lang,calculationOfVolFraction='Mz', plot=True)
            
            # Create T1/T2 vs. concentration and T1/T2 vs. absolute surface area (information about surface chemistry?)
            # slope_conc, slope_surf = ref.plot_T1_T2_ratio('german')
            
            # Calculate surface relaxivity in case of nonporous material
            if not porousMaterial:
                ref.calculate_surfaceRelaxivity('T2', evaluation, lang, calculationOfVolFraction='mass', plot=True)
                #ref.calculate_surfaceRelaxivity('T2', evaluation, lang, calculationOfVolFraction='Mxy', plot=True)
            
            ref.setMeasurementFileNames(filespathT1, filespathT2)
            #ref.createRelaxivityFile(evaluation) 
            ref.createRelaxivityFile(evaluation) 
            
        # Plot calibration for thickener in dispersant    
        else:
            ref.plotCalibrationWithThickener('T1',calculationOfVolFraction='mass', language='german')
            # ref.plotCalibrationWithThickener('T1',calculationOfVolFraction='Mz', language='german')
            
            ref.plotCalibrationWithThickener('T2',calculationOfVolFraction='mass', language='german')
            # ref.plotCalibrationWithThickener('T2',calculationOfVolFraction='Mxy', language='german')
            
            